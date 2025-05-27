use worker::*;
use crate::auth::UserData;

pub async fn get_user_from_kv(env: &Env, username: &str) -> std::result::Result<UserData, Box<dyn std::error::Error>> {
    let kv = env.kv("USERS_KV")?;
    
    match kv.get(username).text().await? {
        Some(user_data_json) => {
            let user_data: UserData = serde_json::from_str(&user_data_json)?;
            Ok(user_data)
        }
        None => Err("User not found".into())
    }
}

pub async fn store_user_in_kv(env: &Env, username: &str, user_data: &UserData) -> std::result::Result<(), Box<dyn std::error::Error>> {
    let kv = env.kv("USERS_KV")?;
    let user_data_json = serde_json::to_string(user_data)?;
    
    kv.put(username, user_data_json)?.execute().await?;
    Ok(())
}

pub async fn delete_user_from_kv(env: &Env, username: &str) -> std::result::Result<(), Box<dyn std::error::Error>> {
    let kv = env.kv("USERS_KV")?;
    
    // Check if user exists first
    match kv.get(username).text().await? {
        Some(_) => {
            kv.delete(username).await?;
            Ok(())
        }
        None => Err("User not found".into())
    }
}
