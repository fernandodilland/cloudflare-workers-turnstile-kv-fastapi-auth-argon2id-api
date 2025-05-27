#!/bin/bash

# Test script for the API
# Make sure to replace the URL with your actual worker URL
# and get a valid Turnstile token from your frontend

API_URL="https://your-worker.your-subdomain.workers.dev"
TURNSTILE_TOKEN="your_turnstile_token_here"

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
curl -X POST "$API_URL/login" \
  -H "Content-Type: application/json" \
  -H "cf-turnstile-response: $TURNSTILE_TOKEN" \
  -d '{
    "user": "testuser",
    "password": "testpassword123"
  }'
echo -e "\n"
