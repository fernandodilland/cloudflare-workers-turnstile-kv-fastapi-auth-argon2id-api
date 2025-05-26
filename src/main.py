from fastapi import FastAPI, HTTPException, Header, Depends, Request
from fastapi.responses import JSONResponse
import json
import os
from .models import LoginRequest, LoginResponse
from .auth import verify_turnstile, verify_password, generate_jwt
from .utils import get_user_from_kv

app = FastAPI(title="Secure Auth API", version="1.0.0")

def get_env_from_request(request: Request):
    """Get Cloudflare Workers environment from request"""
    return getattr(request.state, 'env', None)

async def get_kv_binding(request: Request):
    """Get KV binding from Cloudflare Workers environment"""
    if hasattr(request.state, 'env') and hasattr(request.state.env, 'USERS_KV'):
        return request.state.env.USERS_KV
    # Fallback for local development
    return None

@app.post("/auth/login", response_model=LoginResponse)
async def login(
    request_data: LoginRequest,
    request: Request,
    turnstile_token: str = Header(..., alias="cf-turnstile-token")
):
    """
    Authenticate user with Turnstile, verify credentials, and return JWT
    """
    try:
        # Get KV binding
        kv = await get_kv_binding(request)
        if not kv:
            raise HTTPException(status_code=500, detail="KV store not available")
        
        # Get environment variables from Workers context
        env = get_env_from_request(request)
        turnstile_secret = getattr(env, 'TURNSTILE_SECRET_KEY', None) if env else os.environ.get("TURNSTILE_SECRET_KEY")
        jwt_secret = getattr(env, 'JWT_SECRET_KEY', None) if env else os.environ.get("JWT_SECRET_KEY")
        
        if not turnstile_secret or not jwt_secret:
            raise HTTPException(status_code=500, detail="Missing required secrets")
        
        # 1. Verify Turnstile token
        if not await verify_turnstile(turnstile_token, turnstile_secret):
            raise HTTPException(status_code=401, detail="Invalid Turnstile token")
        
        # 2. Get user from KV store
        user_data = await get_user_from_kv(kv, request_data.username)
        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # 3. Verify password with Argon2id
        if not verify_password(request_data.password, user_data["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # 4. Generate JWT
        token = generate_jwt(
            user_id=user_data["id"],
            username=request_data.username,
            secret_key=jwt_secret
        )
        
        return LoginResponse(
            access_token=token,
            token_type="bearer",
            user_id=user_data["id"],
            username=request_data.username
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "auth-api"}

# Cloudflare Workers handler function
async def on_fetch(request, env, ctx):
    """Main handler for Cloudflare Workers"""
    # For Cloudflare Workers, we handle requests manually
    # This is a simplified version - full ASGI integration would require additional setup
    
    try:
        # Get request details
        url = str(request.url)
        method = request.method
        
        # Simple routing
        if method == "GET" and url.endswith("/health"):
            # Health check endpoint
            response_data = {"status": "healthy", "service": "auth-api"}
            return new_response(json.dumps(response_data), 200, {"Content-Type": "application/json"})
        
        elif method == "POST" and "/auth/login" in url:
            # Login endpoint - this would need full implementation
            # For now, return a placeholder
            return new_response(
                json.dumps({"error": "Login endpoint not fully implemented"}),
                501,
                {"Content-Type": "application/json"}
            )
        
        else:
            # Not found
            return new_response(
                json.dumps({"error": "Not found"}),
                404,
                {"Content-Type": "application/json"}
            )
            
    except Exception as e:
        return new_response(
            json.dumps({"error": "Internal server error"}),
            500,
            {"Content-Type": "application/json"}
        )

def new_response(body, status=200, headers=None):
    """Helper function to create HTTP response"""
    if headers is None:
        headers = {}
    
    # This is a placeholder - actual implementation depends on Cloudflare Workers Python runtime
    # You would typically use the Response constructor from the Workers runtime
    class SimpleResponse:
        def __init__(self, body, status, headers):
            self.body = body
            self.status = status
            self.headers = headers
    
    return SimpleResponse(body, status, headers)
