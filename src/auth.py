import hashlib
import hmac
import base64
import json
import time
from urllib.parse import urlencode
import urllib.request
from typing import Optional

async def verify_turnstile(token: str, secret_key: str) -> bool:
    """
    Verify Cloudflare Turnstile token
    """
    if not token or not secret_key:
        return False
    
    try:
        # Prepare data for Turnstile verification
        data = {
            'secret': secret_key,
            'response': token
        }
        
        # Make request to Turnstile API
        req_data = urlencode(data).encode('utf-8')
        req = urllib.request.Request(
            'https://challenges.cloudflare.com/turnstile/v0/siteverify',
            data=req_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('success', False)
            
    except Exception:
        return False

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against Argon2id hash
    Note: This is a simplified implementation. In production, use proper Argon2id library
    """
    try:
        # Parse Argon2id hash format: $argon2id$v=19$m=65536,t=3,p=4$salt$hash
        parts = hashed_password.split('$')
        if len(parts) != 6 or parts[1] != 'argon2id':
            return False
        
        # Extract parameters
        version = parts[2]
        params = dict(param.split('=') for param in parts[3].split(','))
        salt = base64.b64decode(parts[4] + '==')
        stored_hash = base64.b64decode(parts[5] + '==')
        
        # Simple verification (in production, use proper Argon2id)
        # This is a placeholder - actual Argon2id verification would be more complex
        test_hash = hashlib.pbkdf2_hmac(
            'sha256',
            plain_password.encode('utf-8'),
            salt,
            int(params.get('t', 3)) * 1000
        )
        
        return hmac.compare_digest(test_hash[:len(stored_hash)], stored_hash)
        
    except Exception:
        return False

def generate_jwt(user_id: str, username: str, secret_key: str) -> str:
    """
    Generate JWT token (simplified implementation)
    """
    import base64
    import json
    import time
    import hmac
    import hashlib
    
    # Header
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    
    # Payload
    now = int(time.time())
    payload = {
        "sub": user_id,
        "username": username,
        "iat": now,
        "exp": now + 3600,  # 1 hour expiration
        "iss": "auth-api"
    }
    
    # Encode header and payload
    header_encoded = base64.urlsafe_b64encode(
        json.dumps(header, separators=(',', ':')).encode('utf-8')
    ).decode('utf-8').rstrip('=')
    
    payload_encoded = base64.urlsafe_b64encode(
        json.dumps(payload, separators=(',', ':')).encode('utf-8')
    ).decode('utf-8').rstrip('=')
    
    # Create signature
    message = f"{header_encoded}.{payload_encoded}"
    signature = hmac.new(
        secret_key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
    
    signature_encoded = base64.urlsafe_b64encode(signature).decode('utf-8').rstrip('=')
    
    return f"{message}.{signature_encoded}"
