#!/bin/bash

# Test script for the API
# Make sure to replace the URL with your actual worker URL
# and get a valid Turnstile token from your frontend

API_URL="https://your-worker.your-subdomain.workers.dev"
TURNSTILE_TOKEN="your_turnstile_token_here"
JWT_TOKEN=""

echo "Testing Health Endpoint..."
curl -X GET "$API_URL/health"
echo -e "\n"

echo "Testing Register Endpoint..."
curl -X POST "$API_URL/register" \
  -H "Content-Type: application/json" \
  -H "cf-turnstile-response: $TURNSTILE_TOKEN" \
  -d '{
    "user": "testuser",
    "password": "testpassword123"
  }'
echo -e "\n"

echo "Testing Login Endpoint..."
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/login" \
  -H "Content-Type: application/json" \
  -H "cf-turnstile-response: $TURNSTILE_TOKEN" \
  -d '{
    "user": "testuser",
    "password": "testpassword123"
  }')

echo "$LOGIN_RESPONSE"
echo -e "\n"

# Extract JWT token from login response
JWT_TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

echo "Testing Update User Endpoint (Password Change)..."
if [ -n "$JWT_TOKEN" ]; then
  echo "Using JWT token for password update"
  curl -X PATCH "$API_URL/user" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $JWT_TOKEN" \
    -d '{
      "new_password": "newpassword456"
    }'
  echo -e "\n"
else
  echo "Skipping password update test - no JWT token available"
fi

echo "Testing Update User Endpoint (Username Change)..."
if [ -n "$JWT_TOKEN" ]; then
  echo "Using JWT token for username update"
  UPDATE_RESPONSE=$(curl -s -X PATCH "$API_URL/user" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $JWT_TOKEN" \
    -d '{
      "new_username": "newtestuser"
    }')
  
  echo "$UPDATE_RESPONSE"
  echo -e "\n"
  
  # Extract new JWT token if username changed
  NEW_JWT_TOKEN=$(echo "$UPDATE_RESPONSE" | grep -o '"new_token":"[^"]*"' | cut -d'"' -f4)
  if [ -n "$NEW_JWT_TOKEN" ]; then
    JWT_TOKEN="$NEW_JWT_TOKEN"
    echo "JWT token updated after username change"
  fi
else
  echo "Skipping username update test - no JWT token available"
fi

echo "Testing Delete User Endpoint..."
if [ -n "$JWT_TOKEN" ]; then
  echo "Using JWT token: $JWT_TOKEN"
  curl -X DELETE "$API_URL/user" \
    -H "Authorization: Bearer $JWT_TOKEN"
  echo -e "\n"
else
  echo "Skipping delete test - no JWT token available"
fi
