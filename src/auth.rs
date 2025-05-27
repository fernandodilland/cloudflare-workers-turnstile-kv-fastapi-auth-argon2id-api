use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
pub struct LoginRequest {
    pub user: String,
    pub password: String,
}

#[derive(Serialize)]
pub struct LoginResponse {
    pub success: bool,
    pub token: Option<String>,
    pub message: String,
    pub expires_in: i64, // Duration in seconds
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Claims {
    pub sub: String, // Subject (username)
    pub exp: usize,  // Expiration time
    pub iat: usize,  // Issued at
}

#[derive(Serialize, Deserialize)]
pub struct UserData {
    pub username: String,
    pub password_hash: String,
    pub created_at: i64,
}

#[derive(Serialize)]
pub struct DeleteResponse {
    pub success: bool,
    pub message: String,
}

#[derive(Deserialize)]
pub struct UpdateUserRequest {
    pub new_username: Option<String>,
    pub new_password: Option<String>,
}

#[derive(Serialize)]
pub struct UpdateUserResponse {
    pub success: bool,
    pub message: String,
    pub new_token: Option<String>, // New JWT token if username changed
    pub expires_in: Option<i64>,   // Token expiration in seconds
}
