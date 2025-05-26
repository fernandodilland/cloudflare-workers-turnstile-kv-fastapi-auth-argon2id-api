# Setup script for Cloudflare Workers Python Auth API

Write-Host "Setup for Cloudflare Workers Python Auth API" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Check if wrangler is available
try {
    $wranglerVersion = npx wrangler --version 2>$null
    Write-Host "Wrangler CLI is available" -ForegroundColor Green
} catch {
    Write-Host "Wrangler CLI not found. Please run: npm install" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Setup Checklist:" -ForegroundColor Yellow
Write-Host "1. Login to Cloudflare: npx wrangler auth login"
Write-Host "2. Create KV namespace: npx wrangler kv:namespace create USERS_KV"
Write-Host "3. Update wrangler.toml with your KV namespace ID"
Write-Host "4. Set secrets:"
Write-Host "   - npx wrangler secret put TURNSTILE_SECRET_KEY"
Write-Host "   - npx wrangler secret put JWT_SECRET_KEY"
Write-Host "5. Test locally: npx wrangler dev"
Write-Host "6. Deploy: npx wrangler deploy"
Write-Host ""

# Check if user is logged in
Write-Host "Checking Cloudflare authentication..." -ForegroundColor Blue
try {
    $whoami = npx wrangler whoami 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "You are logged in to Cloudflare" -ForegroundColor Green
    } else {
        Write-Host "Not logged in. Run: npx wrangler auth login" -ForegroundColor Red
    }
} catch {
    Write-Host "Not logged in. Run: npx wrangler auth login" -ForegroundColor Red
}

Write-Host ""
Write-Host "To get started:" -ForegroundColor Cyan
Write-Host "1. Run: npx wrangler auth login" -ForegroundColor White
Write-Host "2. Run: npx wrangler kv:namespace create USERS_KV" -ForegroundColor White
Write-Host "3. Update the namespace ID in wrangler.toml" -ForegroundColor White
Write-Host "4. Set your secrets (Turnstile and JWT keys)" -ForegroundColor White
Write-Host "5. Run: npx wrangler dev" -ForegroundColor White
Write-Host ""
