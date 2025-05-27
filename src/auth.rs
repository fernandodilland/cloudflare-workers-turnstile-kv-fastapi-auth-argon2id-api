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
