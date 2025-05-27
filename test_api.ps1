# Test script for the API in PowerShell
# Make sure to replace the URL with your actual worker URL
# and get a valid Turnstile token from your frontend

$API_URL = "https://your-worker.your-subdomain.workers.dev"
$TURNSTILE_TOKEN = "your_turnstile_token_here"

Write-Host "Testing Health Endpoint..."
try {
    $response = Invoke-RestMethod -Uri "$API_URL/health" -Method Get
    $response | ConvertTo-Json
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}

Write-Host "`nTesting Register Endpoint..."
try {
    $headers = @{
        "Content-Type" = "application/json"
        "cf-turnstile-response" = $TURNSTILE_TOKEN
    }
    $body = @{
        user = "testuser"
        password = "testpassword123"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "$API_URL/register" -Method Post -Headers $headers -Body $body
    $response | ConvertTo-Json
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}

Write-Host "`nTesting Login Endpoint..."
try {
    $headers = @{
        "Content-Type" = "application/json"
        "cf-turnstile-response" = $TURNSTILE_TOKEN
    }
    $body = @{
        user = "testuser"
        password = "testpassword123"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "$API_URL/login" -Method Post -Headers $headers -Body $body
    $response | ConvertTo-Json
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}
