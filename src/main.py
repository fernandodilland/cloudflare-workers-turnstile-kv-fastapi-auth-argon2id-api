"""
Secure Authentication API for Cloudflare Workers

This module provides a FastAPI-based authentication service that integrates
with Cloudflare Turnstile for bot protection, uses Argon2id for password
hashing, and returns JWT tokens for authenticated users.

Features:
- Cloudflare Turnstile validation
- Argon2id password hashing
- JWT token generation
- KV storage for user data
"""

from fastapi import FastAPI, HTTPException, Header, Depends, Request
from fastapi.responses import JSONResponse
import json
import os
from .models import LoginRequest, LoginResponse
from .auth import verify_turnstile, verify_password, generate_jwt
from .utils import get_user_from_kv

app = FastAPI(title="Secure Auth API", version="1.0.0")

def get_env_from_request(request: Request):
    """
    Extract Cloudflare Workers environment from request state.
    
    Args:
        request: FastAPI request object
        
    Returns:
        Environment object containing Workers bindings and secrets
    """
    return getattr(request.state, 'env', None)

async def get_kv_binding(request: Request):
    """
    Get KV namespace binding from Cloudflare Workers environment.
    
    Args:
        request: FastAPI request object
        
    Returns:
        KV binding object or None if not available
    """
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
    Authenticate user with Turnstile validation, verify credentials, and return JWT.
    
    This endpoint performs the following steps:
    1. Validates the Turnstile token to prevent bot attacks
    2. Retrieves user data from KV storage
    3. Verifies the password using Argon2id
    4. Generates and returns a JWT token
    
    Args:
        request_data: Login credentials (username and password)
        request: FastAPI request object
        turnstile_token: Cloudflare Turnstile token from cf-turnstile-token header
        
    Returns:
        LoginResponse containing JWT token and user information
        
    Raises:
        HTTPException: For authentication failures or server errors
    """
    try:
        # Get KV binding for user data storage
        kv = await get_kv_binding(request)
        if not kv:
            raise HTTPException(status_code=500, detail="KV store not available")
        
        # Extract environment variables from Workers context
        env = get_env_from_request(request)
        turnstile_secret = getattr(env, 'TURNSTILE_SECRET_KEY', None) if env else os.environ.get("TURNSTILE_SECRET_KEY")
        jwt_secret = getattr(env, 'JWT_SECRET_KEY', None) if env else os.environ.get("JWT_SECRET_KEY")
        
        if not turnstile_secret or not jwt_secret:
            raise HTTPException(status_code=500, detail="Missing required secrets")
        
        # Step 1: Verify Turnstile token to prevent bot attacks
        if not await verify_turnstile(turnstile_token, turnstile_secret):
            raise HTTPException(status_code=401, detail="Invalid Turnstile token")
        
        # Step 2: Retrieve user data from KV store
        user_data = await get_user_from_kv(kv, request_data.username)
        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid credentials")
          # Step 3: Verify password using Argon2id hashing
        if not verify_password(request_data.password, user_data["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Step 4: Generate JWT token with user information
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
    """
    Health check endpoint for monitoring service availability.
    
    Returns:
        dict: Service status and name
    """
    return {"status": "healthy", "service": "auth-api"}

# Cloudflare Workers handler function
async def on_fetch(request, env, ctx):
    """
    Main handler for Cloudflare Workers requests.
    
    This function provides a simplified routing mechanism for Workers.
    In production, you would use proper ASGI integration.
    
    Args:
        request: Cloudflare Workers Request object
        env: Environment bindings and secrets
        ctx: Execution context
        
    Returns:
        Response object for the client
    """
    # For Cloudflare Workers, we handle requests manually
    # This is a simplified version - full ASGI integration would require additional setup
      try:
        # Extract request details for routing
        url = str(request.url)
        method = request.method
        
        # Simple routing logic
        if method == "GET" and url.endswith("/health"):
            # Health check endpoint
            response_data = {"status": "healthy", "service": "auth-api"}
            return new_response(json.dumps(response_data), 200, {"Content-Type": "application/json"})
        
        elif method == "POST" and "/auth/login" in url:
            # Login endpoint - this would need full implementation
            # For now, return a placeholder response
            return new_response(
                json.dumps({"error": "Login endpoint not fully implemented"}),
                501,
                {"Content-Type": "application/json"}
            )
        
        else:
            # Route not found
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
    """
    Helper function to create HTTP response for Cloudflare Workers.
    
    Args:
        body: Response body content
        status: HTTP status code (default: 200)
        headers: Optional headers dictionary
        
    Returns:
        Response object compatible with Cloudflare Workers
        
    Note:
        This is a placeholder implementation. In production, you would
        use the actual Response constructor from the Workers runtime.
    """
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
