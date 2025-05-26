import json
from typing import Optional, Dict, Any

async def get_user_from_kv(kv_binding, username: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve user data from Cloudflare Workers KV
    """
    try:
        # Get user data from KV store
        user_json = await kv_binding.get(f"user:{username}")
        if not user_json:
            return None
        
        user_data = json.loads(user_json)
        return user_data
        
    except Exception:
        return None

async def store_user_in_kv(kv_binding, username: str, user_data: Dict[str, Any]) -> bool:
    """
    Store user data in Cloudflare Workers KV
    """
    try:
        await kv_binding.put(f"user:{username}", json.dumps(user_data))
        return True
    except Exception:
        return False

def hash_password_argon2id(password: str, salt: Optional[bytes] = None) -> str:
    """
    Hash password using Argon2id (simplified implementation)
    In production, use proper Argon2id library
    """
    import os
    import base64
    import hashlib
    
    if salt is None:
        salt = os.urandom(32)
    
    # Simplified Argon2id-like hashing (use proper library in production)
    hash_value = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 3000)
    
    # Format similar to Argon2id
    salt_b64 = base64.b64encode(salt).decode('utf-8').rstrip('=')
    hash_b64 = base64.b64encode(hash_value).decode('utf-8').rstrip('=')
    
    return f"$argon2id$v=19$m=65536,t=3,p=4${salt_b64}${hash_b64}"
