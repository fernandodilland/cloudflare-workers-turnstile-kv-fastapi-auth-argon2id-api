# Test User Creation Script for Cloudflare Workers Python Auth API

import json
import base64
import hashlib
import os
import uuid
from datetime import datetime

def create_test_user_data():
    """Create test user data with hashed password"""
    
    # Test user credentials
    username = "testuser"
    password = "password123"
    user_id = str(uuid.uuid4())
    
    # Simple password hashing (mimicking our simplified Argon2id)
    salt = os.urandom(32)
    # Using PBKDF2 as a simplified replacement for Argon2id
    hash_value = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 3000)
    
    # Format similar to Argon2id
    salt_b64 = base64.b64encode(salt).decode('utf-8').rstrip('=')
    hash_b64 = base64.b64encode(hash_value).decode('utf-8').rstrip('=')
    password_hash = f"$argon2id$v=19$m=65536,t=3,p=4${salt_b64}${hash_b64}"
    
    # Create user data
    user_data = {
        "id": user_id,
        "username": username,
        "password_hash": password_hash,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "last_login": None
    }
    
    return user_data

def main():
    """Generate test user data and print KV command"""
    user_data = create_test_user_data()
    user_json = json.dumps(user_data, indent=2)
    
    print("Test User Data Generated:")
    print("========================")
    print(f"Username: {user_data['username']}")
    print(f"Password: password123")
    print(f"User ID: {user_data['id']}")
    print()
    print("To add this user to KV, run:")
    print("============================")
    
    # Escape the JSON for command line
    escaped_json = json.dumps(user_json)
    
    print(f'npx wrangler kv:key put --binding=USERS_KV "user:{user_data["username"]}" {escaped_json}')
    print()
    print("User Data (formatted):")
    print("=====================")
    print(user_json)

if __name__ == "__main__":
    main()
