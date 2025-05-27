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

echo "Testing Delete User Endpoint..."
if [ -n "$JWT_TOKEN" ]; then
  echo "Using JWT token: $JWT_TOKEN"
  curl -X DELETE "$API_URL/user" \
    -H "Authorization: Bearer $JWT_TOKEN"
  echo -e "\n"
else
  echo "Skipping delete test - no JWT token available"
fi
