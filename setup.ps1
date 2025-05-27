# Setup script for Cloudflare Workers Rust Auth API (PowerShell)
# This script helps configure the project for first-time use

param(
    [switch]$SkipAuth
)

Write-Host "🚀 Configurando Cloudflare Workers Rust Auth API..." -ForegroundColor Blue

# Function to print colored output
function Write-Status {
    param($Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Success {
    param($Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param($Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param($Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Check if wrangler is installed
try {
    wrangler --version | Out-Null
    Write-Success "Wrangler está instalado"
} catch {
    Write-Error "Wrangler no está instalado. Instalando..."
    npm install -g wrangler
}

# Check if user is logged in to Wrangler
if (-not $SkipAuth) {
    try {
        $user = wrangler whoami 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Status "Usuario autenticado: $user"
        } else {
            throw "Not authenticated"
        }
    } catch {
        Write-Warning "No estás autenticado en Wrangler."
        Write-Host "Ejecuta: wrangler auth login" -ForegroundColor Yellow
        exit 1
    }
}

# Create KV namespaces
Write-Status "Creando KV namespaces..."

Write-Host "Creando namespace de producción..."
try {
    $prodResult = wrangler kv:namespace create "USERS_KV" --json | ConvertFrom-Json
    $prodNs = $prodResult.id
    Write-Success "Namespace de producción creado: $prodNs"
} catch {
    Write-Error "Error creando namespace de producción: $_"
    exit 1
}

Write-Host "Creando namespace de preview..."
try {
    $previewResult = wrangler kv:namespace create "USERS_KV" --preview --json | ConvertFrom-Json
    $previewNs = $previewResult.id
    Write-Success "Namespace de preview creado: $previewNs"
} catch {
    Write-Error "Error creando namespace de preview: $_"
    exit 1
}

# Update wrangler.toml
Write-Status "Actualizando wrangler.toml..."
try {
    $content = Get-Content -Path "wrangler.toml" -Raw
    $content = $content -replace "YOUR_PRODUCTION_KV_NAMESPACE_ID", $prodNs
    $content = $content -replace "YOUR_PREVIEW_KV_NAMESPACE_ID", $previewNs
    Set-Content -Path "wrangler.toml" -Value $content
    Write-Success "wrangler.toml actualizado"
} catch {
    Write-Error "Error actualizando wrangler.toml: $_"
    exit 1
}

# Create .dev.vars file
if (-not (Test-Path ".dev.vars")) {
    Write-Status "Creando archivo .dev.vars..."
    Copy-Item ".dev.vars.example" ".dev.vars"
    Write-Warning "IMPORTANTE: Edita .dev.vars con tus claves reales"
    Write-Warning "- TURNSTILE_SECRET_KEY: De Cloudflare Dashboard > Turnstile"
    Write-Warning "- JWT_SECRET: Usa el generado abajo o crea uno nuevo"
} else {
    Write-Warning ".dev.vars ya existe, no se sobrescribirá"
}

# Generate a JWT secret
Write-Status "Generando clave JWT de ejemplo..."
$bytes = New-Object byte[] 32
[Security.Cryptography.RNGCryptoServiceProvider]::Create().GetBytes($bytes)
$jwtSecret = [Convert]::ToBase64String($bytes)
Write-Host "Clave JWT generada: $jwtSecret" -ForegroundColor Magenta
Write-Warning "Guarda esta clave en un lugar seguro y úsala para JWT_SECRET"

Write-Host ""
Write-Success "✅ Configuración inicial completa!"
Write-Host ""
Write-Warning "Pasos siguientes:"
Write-Host "1. 🔑 Configura Turnstile en Cloudflare Dashboard" -ForegroundColor White
Write-Host "2. 📝 Edita .dev.vars con tus claves reales" -ForegroundColor White
Write-Host "3. 🚀 Ejecuta: npm run dev" -ForegroundColor White
Write-Host "4. 🌐 Para producción: wrangler secret put TURNSTILE_SECRET_KEY" -ForegroundColor White
Write-Host "5. 🔐 Para producción: wrangler secret put JWT_SECRET" -ForegroundColor White
Write-Host ""
Write-Status "Ver SETUP.md para instrucciones detalladas"
