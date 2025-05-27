use argon2::{
    password_hash::{rand_core::OsRng, PasswordHash, PasswordHasher, PasswordVerifier, SaltString},
    Argon2,
};
use chrono::{Duration, Utc};
use jsonwebtoken::{encode, decode, DecodingKey, EncodingKey, Header, Validation};
use worker::*;
use rand_core::RngCore;
use base64::{Engine as _, engine::general_purpose};

mod turnstile;
mod auth;
mod kv_store;

use turnstile::verify_turnstile_token;
use auth::{LoginRequest, LoginResponse, Claims, UserData, DeleteResponse, UpdateUserRequest, UpdateUserResponse};
use kv_store::{get_user_from_kv, store_user_in_kv, delete_user_from_kv, update_user_in_kv};

// Generate a secure 512-bit (64 bytes) JWT secret key
fn generate_jwt_secret() -> String {
    let mut secret = [0u8; 64]; // 512 bits = 64 bytes
    OsRng.fill_bytes(&mut secret);
    general_purpose::STANDARD.encode(secret)
}

// Generate JWT token using user's unique secret
fn generate_jwt_token(user_data: &UserData, jwt_expiration_minutes: i64) -> std::result::Result<String, Box<dyn std::error::Error>> {
    let now = Utc::now();
    let expiration = now + Duration::minutes(jwt_expiration_minutes);
      let claims = Claims {
        sub: user_data.username.clone(),
        exp: expiration.timestamp() as usize,
        iat: now.timestamp() as usize,
        ver: user_data.jwt_version,
    };

    let secret_bytes = general_purpose::STANDARD.decode(&user_data.jwt_secret)?;
    let token = encode(
        &Header::default(),
        &claims,
        &EncodingKey::from_secret(&secret_bytes),
    )?;

    Ok(token)
}

// Verify JWT token using user's unique secret
async fn verify_jwt_token_with_user_secret(
    token: &str, 
    user_data: &UserData
) -> std::result::Result<Claims, Box<dyn std::error::Error>> {
    let secret_bytes = general_purpose::STANDARD.decode(&user_data.jwt_secret)?;
    
    let token_data = decode::<Claims>(
        token,
        &DecodingKey::from_secret(&secret_bytes),
        &Validation::default(),
    )?;

    // Verify JWT version matches current user version
    if token_data.claims.ver != user_data.jwt_version {
        return Err("Token version mismatch - token has been invalidated".into());
    }

    Ok(token_data.claims)
}

#[event(fetch)]
async fn main(req: Request, env: Env, _ctx: Context) -> Result<Response> {
    // Enable CORS for all requests
    let cors_headers = [
        ("Access-Control-Allow-Origin", "*"),
        ("Access-Control-Allow-Methods", "GET, POST, DELETE, PATCH, OPTIONS"),
        ("Access-Control-Allow-Headers", "Content-Type, cf-turnstile-response, Authorization"),
    ];

    // Handle preflight requests
    if req.method() == Method::Options {
        return Response::empty()
            .map(|mut res| {
                for (key, value) in cors_headers.iter() {
                    res.headers_mut().set(key, value).ok();
                }
                res            });
    }

    let result = match (req.method(), req.path().as_ref()) {
        (Method::Post, "/login") => login_handler(req, env).await,
        (Method::Post, "/register") => register_handler(req, env).await,
        (Method::Delete, "/user") => delete_user_handler(req, env).await,
        (Method::Patch, "/user") => update_user_handler(req, env).await,
        (Method::Get, "/health") => health_handler().await,
        _ => Err(Error::InvalidRoute),
    };

    match result {
        Ok(mut response) => {
            // Add CORS headers to successful responses
            for (key, value) in cors_headers.iter() {
                response.headers_mut().set(key, value).ok();
            }
            Ok(response)
        }
        Err(err) => {
            let mut error_response = err.to_response()?;
            // Add CORS headers to error responses
            for (key, value) in cors_headers.iter() {
                error_response.headers_mut().set(key, value).ok();
            }
            Ok(error_response)
        }
    }
}

async fn login_handler(mut req: Request, env: Env) -> std::result::Result<Response, Error> {
    // Get Turnstile token from header
    let turnstile_token = req
        .headers()
        .get("cf-turnstile-response")
        .map_err(|_| Error::MissingTurnstileToken)?
        .ok_or(Error::MissingTurnstileToken)?;

    // Get Turnstile secret from environment
    let turnstile_secret = env
        .secret("TURNSTILE_SECRET_KEY")
        .map_err(|_| Error::MissingTurnstileSecret)?
        .to_string();

    // Verify Turnstile token
    verify_turnstile_token(&turnstile_token, &turnstile_secret).await
        .map_err(|_| Error::InvalidTurnstileToken)?;

    // Parse login request
    let login_req: LoginRequest = req
        .json()
        .await
        .map_err(|err| Error::DecodeBody(err.to_string()))?;

    // Get user from KV store
    let user_data = get_user_from_kv(&env, &login_req.user).await
        .map_err(|_| Error::UserNotFound)?;

    // Verify password
    let password_hash = PasswordHash::new(&user_data.password_hash)
        .map_err(|err| Error::InvalidPasswordHash(err.to_string()))?;

    let argon2 = Argon2::default();
    match argon2.verify_password(login_req.password.as_bytes(), &password_hash) {
        Ok(()) => {
            // Password is correct, generate JWT using user's unique secret
            let expiration_minutes = env
                .var("JWT_EXPIRATION_MINUTES")
                .map(|v| v.to_string().parse::<i64>().unwrap_or(15))
                .unwrap_or(15);

            let token = generate_jwt_token(&user_data, expiration_minutes)
                .map_err(|err| Error::JwtGeneration(err.to_string()))?;

            let response = LoginResponse {
                success: true,
                token: Some(token),
                message: "Login successful".to_string(),
                expires_in: expiration_minutes * 60, // Convert to seconds
            };

            Response::from_json(&response)
                .map_err(|err| Error::EncodeBody(err.to_string()))
        }
        Err(argon2::password_hash::Error::Password) => {
            let response = LoginResponse {
                success: false,
                token: None,
                message: "Invalid credentials".to_string(),
                expires_in: 0,
            };
            Response::from_json(&response)
                .map_err(|err| Error::EncodeBody(err.to_string()))
        }
        Err(err) => Err(Error::Verify(err.to_string())),
    }
}

async fn register_handler(mut req: Request, env: Env) -> std::result::Result<Response, Error> {
    // Get Turnstile token from header
    let turnstile_token = req
        .headers()
        .get("cf-turnstile-response")
        .map_err(|_| Error::MissingTurnstileToken)?
        .ok_or(Error::MissingTurnstileToken)?;

    // Get Turnstile secret from environment
    let turnstile_secret = env
        .secret("TURNSTILE_SECRET_KEY")
        .map_err(|_| Error::MissingTurnstileSecret)?
        .to_string();

    // Verify Turnstile token
    verify_turnstile_token(&turnstile_token, &turnstile_secret).await
        .map_err(|_| Error::InvalidTurnstileToken)?;

    // Parse register request
    let register_req: LoginRequest = req
        .json()
        .await
        .map_err(|err| Error::DecodeBody(err.to_string()))?;

    // Check if user already exists
    if let Ok(_) = get_user_from_kv(&env, &register_req.user).await {
        return Response::from_json(&serde_json::json!({
            "success": false,
            "message": "User already exists"
        })).map_err(|err| Error::EncodeBody(err.to_string()));
    }

    // Hash password with Argon2id
    let salt = SaltString::generate(&mut OsRng);
    let argon2 = Argon2::default();
    let password_hash = argon2
        .hash_password(register_req.password.as_bytes(), &salt)
        .map(|password_hash| password_hash.to_string())
        .map_err(|err| Error::Hash(err.to_string()))?;

    // Store user in KV
    let user_data = UserData {
        username: register_req.user.clone(),
        password_hash,
        created_at: Utc::now().timestamp(),
        jwt_secret: generate_jwt_secret(),
        jwt_version: 1,
    };    store_user_in_kv(&env, &register_req.user, &user_data).await
        .map_err(|_| Error::KvStoreError)?;

    Response::from_json(&serde_json::json!({
        "success": true,
        "message": "User registered successfully"
    })).map_err(|err| Error::EncodeBody(err.to_string()))
}

// Extract username from JWT token (without verification)
fn extract_username_from_token(token: &str) -> std::result::Result<String, Box<dyn std::error::Error>> {
    // Decode without verification to get the username
    let mut validation = Validation::default();
    validation.insecure_disable_signature_validation();
    
    let token_data = decode::<Claims>(
        token,
        &DecodingKey::from_secret("dummy".as_ref()),
        &validation,
    )?;
    
    Ok(token_data.claims.sub)
}

async fn delete_user_handler(req: Request, env: Env) -> std::result::Result<Response, Error> {
    // Get JWT token from Authorization header
    let auth_header = req
        .headers()
        .get("Authorization")
        .map_err(|_| Error::MissingAuthToken)?
        .ok_or(Error::MissingAuthToken)?;

    // Extract token from "Bearer <token>" format
    let token = if auth_header.starts_with("Bearer ") {
        &auth_header[7..]
    } else {
        return Err(Error::InvalidAuthFormat);
    };

    // Extract username from token to get user data
    let username = extract_username_from_token(token)
        .map_err(|_| Error::InvalidJwtToken)?;

    // Get user from KV store
    let user_data = get_user_from_kv(&env, &username).await
        .map_err(|_| Error::UserNotFound)?;

    // Verify JWT token using user's unique secret
    let claims = verify_jwt_token_with_user_secret(token, &user_data).await
        .map_err(|_| Error::InvalidJwtToken)?;

    // Check if token is expired
    let current_time = Utc::now().timestamp() as usize;
    if claims.exp < current_time {
        return Err(Error::ExpiredJwtToken);
    }

    // Delete user from KV store
    delete_user_from_kv(&env, &claims.sub).await
        .map_err(|_| Error::UserNotFound)?;

    let response = DeleteResponse {
        success: true,
        message: format!("User '{}' deleted successfully", claims.sub),
    };

    Response::from_json(&response)
        .map_err(|err| Error::EncodeBody(err.to_string()))
}

async fn update_user_handler(mut req: Request, env: Env) -> std::result::Result<Response, Error> {
    // Get JWT token from Authorization header
    let auth_header = req
        .headers()
        .get("Authorization")
        .map_err(|_| Error::MissingAuthToken)?
        .ok_or(Error::MissingAuthToken)?;

    // Extract token from "Bearer <token>" format
    let token = if auth_header.starts_with("Bearer ") {
        &auth_header[7..]
    } else {
        return Err(Error::InvalidAuthFormat);
    };

    // Extract username from token to get user data
    let username = extract_username_from_token(token)
        .map_err(|_| Error::InvalidJwtToken)?;

    // Get user from KV store
    let mut user_data = get_user_from_kv(&env, &username).await
        .map_err(|_| Error::UserNotFound)?;

    // Verify JWT token using user's unique secret
    let claims = verify_jwt_token_with_user_secret(token, &user_data).await
        .map_err(|_| Error::InvalidJwtToken)?;

    // Check if token is expired
    let current_time = Utc::now().timestamp() as usize;
    if claims.exp < current_time {
        return Err(Error::ExpiredJwtToken);
    }

    // Parse update request
    let update_req: UpdateUserRequest = req
        .json()
        .await
        .map_err(|err| Error::DecodeBody(err.to_string()))?;

    // Validate that at least one field is being updated
    if update_req.new_username.is_none() && update_req.new_password.is_none() {
        return Response::from_json(&UpdateUserResponse {
            success: false,
            message: "At least one field (new_username or new_password) must be provided".to_string(),
            new_token: None,
            expires_in: None,
        }).map_err(|err| Error::EncodeBody(err.to_string()));
    }

    let mut jwt_rotated = false;

    // Update password if provided (this rotates JWT)
    if let Some(new_password) = &update_req.new_password {
        // Hash new password with Argon2id
        let salt = SaltString::generate(&mut OsRng);
        let argon2 = Argon2::default();
        let password_hash = argon2
            .hash_password(new_password.as_bytes(), &salt)
            .map(|password_hash| password_hash.to_string())
            .map_err(|err| Error::Hash(err.to_string()))?;
        
        user_data.password_hash = password_hash;
        
        // Rotate JWT secret and version when password changes (for security)
        user_data.jwt_secret = generate_jwt_secret();
        user_data.jwt_version += 1;
        jwt_rotated = true;
    }

    // Update username in user data if provided (this also rotates JWT)
    let new_username = update_req.new_username.as_deref();
    if let Some(new_user) = new_username {
        user_data.username = new_user.to_string();
        
        // Rotate JWT secret and version when username changes
        if !jwt_rotated {
            user_data.jwt_secret = generate_jwt_secret();
            user_data.jwt_version += 1;
            jwt_rotated = true;
        }
    }

    // Update user in KV store
    update_user_in_kv(&env, &claims.sub, new_username, &user_data).await
        .map_err(|err| {
            if err.to_string().contains("already exists") {
                Error::UsernameExists
            } else {
                Error::KvStoreError
            }
        })?;

    // Generate new JWT token since we rotated the secret
    let (new_token, expires_in) = if jwt_rotated {
        let expiration_minutes = env
            .var("JWT_EXPIRATION_MINUTES")
            .map(|v| v.to_string().parse::<i64>().unwrap_or(15))
            .unwrap_or(15);

        let token = generate_jwt_token(&user_data, expiration_minutes)
            .map_err(|err| Error::JwtGeneration(err.to_string()))?;

        (Some(token), Some(expiration_minutes * 60))
    } else {
        (None, None)
    };

    let message = match (update_req.new_username.is_some(), update_req.new_password.is_some()) {
        (true, true) => "Username and password updated successfully. Previous tokens are now invalid.",
        (true, false) => "Username updated successfully. Previous tokens are now invalid.",
        (false, true) => "Password updated successfully. Previous tokens are now invalid.",
        (false, false) => unreachable!(), // Already validated above
    };

    let response = UpdateUserResponse {
        success: true,
        message: message.to_string(),
        new_token,
        expires_in,
    };

    Response::from_json(&response)
        .map_err(|err| Error::EncodeBody(err.to_string()))
}

async fn health_handler() -> std::result::Result<Response, Error> {
    Response::from_json(&serde_json::json!({
        "status": "healthy",
        "timestamp": Utc::now().timestamp()
    })).map_err(|err| Error::EncodeBody(err.to_string()))
}

// ERROR HANDLING

#[derive(Debug)]
enum Error {
    InvalidRoute,
    DecodeBody(String),
    EncodeBody(String),
    Hash(String),
    InvalidPasswordHash(String),
    Verify(String),
    MissingTurnstileToken,
    MissingTurnstileSecret,
    InvalidTurnstileToken,
    JwtGeneration(String),
    UserNotFound,
    KvStoreError,
    MissingAuthToken,
    InvalidAuthFormat,
    InvalidJwtToken,
    ExpiredJwtToken,
    UsernameExists,
}

impl Error {
    fn to_response(&self) -> worker::Result<Response> {
        match self {
            Error::InvalidRoute => Response::error("Route not found", 404),
            Error::DecodeBody(err) => {
                Response::error(format!("Failed to decode request body: {}", err), 400)
            }
            Error::EncodeBody(err) => {
                Response::error(format!("Failed to encode response body: {}", err), 500)
            }
            Error::Hash(err) => Response::error(format!("Failed to hash password: {}", err), 500),
            Error::InvalidPasswordHash(err) => {
                Response::error(format!("Invalid password hash: {}", err), 400)
            }
            Error::Verify(err) => {
                Response::error(format!("Failed to verify password: {}", err), 500)
            }
            Error::MissingTurnstileToken => {
                Response::error("Missing Turnstile token in cf-turnstile-response header", 400)
            }
            Error::MissingTurnstileSecret => {
                Response::error("Missing Turnstile secret key in environment", 500)
            }            Error::InvalidTurnstileToken => {
                Response::error("Invalid Turnstile token", 401)
            }
            Error::JwtGeneration(err) => {
                Response::error(format!("Failed to generate JWT: {}", err), 500)
            }Error::UserNotFound => {
                Response::error("Invalid credentials", 401)
            }
            Error::KvStoreError => {
                Response::error("Internal server error", 500)
            }
            Error::MissingAuthToken => {
                Response::error("Missing Authorization header", 401)
            }
            Error::InvalidAuthFormat => {
                Response::error("Invalid Authorization format. Use 'Bearer <token>'", 401)
            }            Error::InvalidJwtToken => {
                Response::error("Invalid JWT token", 401)
            }
            Error::ExpiredJwtToken => {
                Response::error("JWT token has expired", 401)
            }
            Error::UsernameExists => {
                Response::error("Username already exists", 409)
            }
        }
    }
}
