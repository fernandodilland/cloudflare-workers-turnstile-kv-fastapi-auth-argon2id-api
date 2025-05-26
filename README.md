# Secure Auth API - Cloudflare Workers

API de autenticación segura usando Cloudflare Workers con Python, FastAPI, Turnstile, Argon2id y JWT.

## Características

- ✅ Validación con Cloudflare Turnstile
- ✅ Autenticación con Argon2id
- ✅ Generación de JWT
- ✅ Storage en Workers KV
- ✅ FastAPI con Python

## Prerequisitos

1. Cuenta de Cloudflare con Workers habilitado
2. Node.js y npm instalados
3. Wrangler CLI instalado: `npm install -g wrangler`

## Configuración

### 1. Instalar Wrangler y hacer login

```bash
npm install -g wrangler
wrangler login
```

### 2. Crear KV Namespace

```bash
wrangler kv:namespace create "USERS_KV"
wrangler kv:namespace create "USERS_KV" --preview
```

Actualiza el `wrangler.toml` con los IDs generados.

### 3. Configurar Turnstile

1. Ve a Cloudflare Dashboard > Turnstile
2. Crea un nuevo sitio
3. Obtén las claves Site Key y Secret Key

### 4. Configurar Secrets

```bash
# Clave secreta de Turnstile
wrangler secret put TURNSTILE_SECRET_KEY

# Clave para firmar JWT
wrangler secret put JWT_SECRET_KEY
```

### 5. Crear usuario de prueba

```bash
# Crear usuario en KV
wrangler kv:key put --binding=USERS_KV "user:testuser" '{"id":"user123","username":"testuser","password_hash":"$argon2id$v=19$m=65536,t=3,p=4$abcdefghijklmnop$qrstuvwxyzABCDEF","created_at":"2024-01-01T00:00:00Z"}'
```

## Despliegue

### 1. Desplegar a staging

```bash
wrangler deploy --env staging
```

### 2. Desplegar a producción

```bash
wrangler deploy --env production
```

## Uso de la API

### Endpoint de Login

```bash
curl -X POST "https://your-worker.your-subdomain.workers.dev/auth/login" \
  -H "Content-Type: application/json" \
  -H "cf-turnstile-token: YOUR_TURNSTILE_TOKEN" \
  -d '{
    "username": "testuser",
    "password": "testpassword"
  }'
```

### Respuesta exitosa

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": "user123",
  "username": "testuser"
}
```

## Estructura de datos en KV

### Usuario en KV

```json
{
  "id": "user123",
  "username": "testuser",
  "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$...",
  "created_at": "2024-01-01T00:00:00Z",
  "last_login": "2024-01-01T12:00:00Z"
}
```

## Seguridad

- Las contraseñas se almacenan con hash Argon2id
- Validación obligatoria de Turnstile
- JWT firmado con clave secreta
- Tokens con expiración de 1 hora

## Monitoreo

```bash
# Ver logs en tiempo real
wrangler tail

# Ver métricas
wrangler metrics
```

## Desarrollo local

```bash
# Ejecutar en modo desarrollo
wrangler dev

# Con KV local
wrangler dev --local
```
