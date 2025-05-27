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

pub async fn update_user_in_kv(
    env: &Env, 
    old_username: &str, 
    new_username: Option<&str>, 
    user_data: &UserData
) -> std::result::Result<(), Box<dyn std::error::Error>> {
    let kv = env.kv("USERS_KV")?;
    
    // Check if the old user exists
    match kv.get(old_username).text().await? {
        Some(_) => {
            // If username is changing, check if new username is available
            if let Some(new_user) = new_username {
                if new_user != old_username {
                    // Check if new username already exists
                    match kv.get(new_user).text().await? {
                        Some(_) => return Err("New username already exists".into()),
                        None => {
                            // Delete old username entry
                            kv.delete(old_username).await?;
                            // Store with new username
                            let user_data_json = serde_json::to_string(user_data)?;
                            kv.put(new_user, user_data_json)?.execute().await?;
                        }
                    }
                } else {
                    // Username not changing, just update the data
                    let user_data_json = serde_json::to_string(user_data)?;
                    kv.put(old_username, user_data_json)?.execute().await?;
                }
            } else {
                // Username not changing, just update the data
                let user_data_json = serde_json::to_string(user_data)?;
                kv.put(old_username, user_data_json)?.execute().await?;
            }
            Ok(())
        }
        None => Err("User not found".into())
    }
}
