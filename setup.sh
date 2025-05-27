#!/bin/bash

# Setup script for Cloudflare Workers Rust Auth API
# This script helps configure the project for first-time use

set -e

echo "🚀 Configurando Cloudflare Workers Rust Auth API..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if wrangler is installed
if ! command -v wrangler &> /dev/null; then
    print_error "Wrangler no está instalado. Instalando..."
    npm install -g wrangler
fi

# Check if user is logged in to Wrangler
if ! wrangler whoami &> /dev/null; then
    print_warning "No estás autenticado en Wrangler."
    echo "Ejecuta: wrangler auth login"
    exit 1
fi

print_status "Usuario autenticado: $(wrangler whoami)"

# Create KV namespaces
print_status "Creando KV namespaces..."

echo "Creando namespace de producción..."
PROD_NS=$(wrangler kv:namespace create "USERS_KV" --json | jq -r '.id')
print_success "Namespace de producción creado: $PROD_NS"

echo "Creando namespace de preview..."
PREVIEW_NS=$(wrangler kv:namespace create "USERS_KV" --preview --json | jq -r '.id')
print_success "Namespace de preview creado: $PREVIEW_NS"

# Update wrangler.toml
print_status "Actualizando wrangler.toml..."
sed -i.bak "s/YOUR_PRODUCTION_KV_NAMESPACE_ID/$PROD_NS/g" wrangler.toml
sed -i.bak "s/YOUR_PREVIEW_KV_NAMESPACE_ID/$PREVIEW_NS/g" wrangler.toml
rm wrangler.toml.bak
print_success "wrangler.toml actualizado"

# Create .dev.vars file
if [ ! -f .dev.vars ]; then
    print_status "Creando archivo .dev.vars..."
    cp .dev.vars.example .dev.vars
    print_warning "IMPORTANTE: Edita .dev.vars con tus claves reales"
    print_warning "- TURNSTILE_SECRET_KEY: De Cloudflare Dashboard > Turnstile"
    print_warning "- JWT_SECRET: Genera uno con: openssl rand -base64 32"
else
    print_warning ".dev.vars ya existe, no se sobrescribirá"
fi

# Generate a JWT secret
print_status "Generando clave JWT de ejemplo..."
JWT_SECRET=$(openssl rand -base64 32)
echo "Clave JWT generada: $JWT_SECRET"
print_warning "Guarda esta clave en un lugar seguro y úsala para JWT_SECRET"

echo ""
print_success "✅ Configuración inicial completa!"
echo ""
print_warning "Pasos siguientes:"
echo "1. 🔑 Configura Turnstile en Cloudflare Dashboard"
echo "2. 📝 Edita .dev.vars con tus claves reales"
echo "3. 🚀 Ejecuta: npm run dev"
echo "4. 🌐 Para producción: wrangler secret put TURNSTILE_SECRET_KEY"
echo "5. 🔐 Para producción: wrangler secret put JWT_SECRET"
echo ""
print_status "Ver SETUP.md para instrucciones detalladas"
