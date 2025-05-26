"""
Secure Authentication API for Cloudflare Workers in Python

This module provides a Python-based authentication service that integrates
with Cloudflare Turnstile for bot protection, uses Argon2id for password
hashing, and returns JWT tokens for authenticated users.

Features:
- Cloudflare Turnstile validation
- Argon2id password hashing
- JWT token generation
- KV storage for user data
"""

from workers import Response
from js import Object, JSON
from pyodide.ffi import to_js as _to_js
import json
import time
from urllib.parse import urlparse, parse_qs
from .auth import verify_turnstile, verify_password, generate_jwt
from .utils import get_user_from_kv
from .models import LoginRequest, LoginResponse


def to_js(obj):
    """Convert Python dict to JavaScript Object"""
    return _to_js(obj, dict_converter=Object.fromEntries)


async def handle_login(request, env):
    """
    Handle login requests with Turnstile validation and JWT generation.
    
    Args:
        request: Cloudflare Workers Request object
        env: Environment bindings and secrets
        
    Returns:
        Response object with login result
    """
    try:
        # Parse request body
        request_body = await request.json()
        username = request_body.get("username")
        password = request_body.get("password")
        
        # Get Turnstile token from headers
        turnstile_token = request.headers.get("cf-turnstile-token")
        
        # Validate required fields
        if not username or not password:
            return Response.json(
                to_js({"error": "Username and password are required"}),
                status=400
            )
        
        if not turnstile_token:
            return Response.json(
                to_js({"error": "Turnstile token is required"}),
                status=400
            )
        
        # Get environment variables
        turnstile_secret = getattr(env, 'TURNSTILE_SECRET_KEY', None)
        jwt_secret = getattr(env, 'JWT_SECRET_KEY', None)
        kv = getattr(env, 'USERS_KV', None)
        
        if not turnstile_secret or not jwt_secret:
            return Response.json(
                to_js({"error": "Server configuration error"}),
                status=500
            )
        
        if not kv:
            return Response.json(
                to_js({"error": "KV store not available"}),
                status=500
            )
        
        # Step 1: Verify Turnstile token
        turnstile_valid = await verify_turnstile(turnstile_token, turnstile_secret)
        if not turnstile_valid:
            return Response.json(
                to_js({"error": "Invalid Turnstile token"}),
                status=401
            )
        
        # Step 2: Get user data from KV
        user_data = await get_user_from_kv(kv, username)
        if not user_data:
            return Response.json(
                to_js({"error": "Invalid credentials"}),
                status=401
            )
        
        # Step 3: Verify password
        password_valid = verify_password(password, user_data["password_hash"])
        if not password_valid:
            return Response.json(
                to_js({"error": "Invalid credentials"}),
                status=401
            )
        
        # Step 4: Generate JWT token
        token = generate_jwt(
            user_id=user_data["id"],
            username=username,
            secret_key=jwt_secret
        )
        
        # Return successful login response
        response_data = {
            "access_token": token,
            "token_type": "bearer",
            "user_id": user_data["id"],
            "username": username
        }
        
        return Response.json(to_js(response_data), status=200)
        
    except Exception as e:
        return Response.json(
            to_js({"error": "Internal server error"}),
            status=500
        )


async def handle_health(request, env):
    """
    Handle health check requests.
    
    Args:
        request: Cloudflare Workers Request object
        env: Environment bindings and secrets
        
    Returns:
        Response object with health status
    """
    response_data = {
        "status": "healthy",
        "service": "auth-api",
        "timestamp": int(time.time()) if 'time' in globals() else None
    }
    return Response.json(to_js(response_data), status=200)


async def on_fetch(request, env, ctx):
    """
    Main handler for Cloudflare Workers requests.
    
    This function routes incoming requests to appropriate handlers.
    
    Args:
        request: Cloudflare Workers Request object
        env: Environment bindings and secrets
        ctx: Execution context
        
    Returns:
        Response object for the client
    """
    try:
        # Parse request URL and method
        url = urlparse(request.url)
        method = request.method
        path = url.path
        
        # Add CORS headers for all responses
        cors_headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, cf-turnstile-token",
        }
        
        # Handle preflight OPTIONS requests
        if method == "OPTIONS":
            return Response(None, status=204, headers=cors_headers)
        
        # Route requests
        if method == "GET" and path == "/health":
            response = await handle_health(request, env)
        elif method == "POST" and path == "/auth/login":
            response = await handle_login(request, env)
        else:
            # Route not found
            response = Response.json(
                to_js({"error": "Not found"}),
                status=404
            )        
        # Add CORS headers to response
        for key, value in cors_headers.items():
            response.headers.set(key, value)
        
        return response
        
    except Exception as e:
        # Add CORS headers for all responses
        cors_headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, cf-turnstile-token",
        }
        
        # Return error response with CORS headers
        error_response = Response.json(
            to_js({"error": "Internal server error"}),
            status=500
        )
        
        for key, value in cors_headers.items():
            error_response.headers.set(key, value)
        
        return error_response
