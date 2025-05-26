# Secure Auth API - Cloudflare Workers

Secure authentication API using Cloudflare Workers with Python, FastAPI, Turnstile, Argon2id, and JWT.

[![Deploy to Cloudflare](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/fernandodilland/cloudflare-workers-turnstile-kv-fastapi-auth-argon2id-api)

> **One-click deployment!** Use the button above to deploy this application directly to your Cloudflare account. Required resources (KV namespaces) will be automatically created and everything will be configured for you.

## Features

- ✅ Cloudflare Turnstile validation
- ✅ Argon2id authentication
- ✅ JWT token generation
- ✅ Workers KV storage
- ✅ FastAPI with Python

## Prerequisites

1. Cloudflare account with Workers enabled
2. Node.js and npm installed (for manual setup only)
3. Wrangler CLI installed (for manual setup only): `npm install -g wrangler`

## Quick Deployment (Recommended)

### Option 1: Deploy to Cloudflare (One-click)

Click the **Deploy to Cloudflare** button above to:

- ✅ Automatically clone this repository to your GitHub account
- ✅ Automatically create required KV namespaces
- ✅ Configure the Worker with all dependencies
- ✅ Deploy the application to your Cloudflare account

**Post-deployment configuration:**

After automatic deployment, you only need to configure the secrets:

1. **Configure Turnstile:**
   - Go to [Cloudflare Dashboard > Turnstile](https://dash.cloudflare.com/profile/api-tokens)
   - Create a new site and get the Site Key and Secret Key

2. **Configure Worker Secrets:**
   ```bash
   # Turnstile secret key
   wrangler secret put TURNSTILE_SECRET_KEY
   
   # JWT signing key (generate a strong random key)
   wrangler secret put JWT_SECRET_KEY
   ```

3. **Create test user:**
   ```bash
   wrangler kv:key put --binding=USERS_KV "user:testuser" '{"id":"user123","username":"testuser","password_hash":"$argon2id$v=19$m=65536,t=3,p=4$abcdefghijklmnop$qrstuvwxyzABCDEF","created_at":"2024-01-01T00:00:00Z"}'
   ```

### Option 2: Manual Setup

If you prefer to configure everything manually, follow these steps:

#### 1. Install Wrangler and login

```bash
npm install -g wrangler
wrangler login
```

#### 2. Create KV Namespace

```bash
wrangler kv:namespace create "USERS_KV"
wrangler kv:namespace create "USERS_KV" --preview
```

Update `wrangler.toml` with the generated IDs.

#### 3. Configure Turnstile

1. Go to Cloudflare Dashboard > Turnstile
2. Create a new site
3. Get Site Key and Secret Key

#### 4. Configure Secrets

```bash
# Turnstile secret key
wrangler secret put TURNSTILE_SECRET_KEY

# JWT signing key
wrangler secret put JWT_SECRET_KEY
```

#### 5. Create test user

```bash
# Create user in KV
wrangler kv:key put --binding=USERS_KV "user:testuser" '{"id":"user123","username":"testuser","password_hash":"$argon2id$v=19$m=65536,t=3,p=4$abcdefghijklmnop$qrstuvwxyzABCDEF","created_at":"2024-01-01T00:00:00Z"}'
```

#### 6. Manual deployment

**Deploy to staging:**

```bash
wrangler deploy --env staging
```

**Deploy to production:**

```bash
wrangler deploy --env production
```

## Local Development

```bash
# Run in development mode
wrangler dev

# With local KV
wrangler dev --local
```

## API Usage

### Login Endpoint

```bash
curl -X POST "https://your-worker.your-subdomain.workers.dev/auth/login" \
  -H "Content-Type: application/json" \
  -H "cf-turnstile-token: YOUR_TURNSTILE_TOKEN" \
  -d '{
    "username": "testuser",
    "password": "testpassword"
  }'
```

### Successful Response

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": "user123",
  "username": "testuser"
}
```

## KV Data Structure

### User in KV

```json
{
  "id": "user123",
  "username": "testuser",
  "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$...",
  "created_at": "2024-01-01T00:00:00Z",
  "last_login": "2024-01-01T12:00:00Z"
}
```

## Security

- Passwords are stored with Argon2id hash
- Mandatory Turnstile validation
- JWT signed with secret key
- Tokens with 1-hour expiration

## Monitoring

```bash
# View real-time logs
wrangler tail

# View metrics
wrangler metrics
```

## Local Development

```bash
# Run in development mode
wrangler dev

# With local KV
wrangler dev --local
```

## Deploy to Cloudflare

This project includes a **Deploy to Cloudflare** button that allows:

- 🚀 **One-click deployment**: No need to manually clone the repository
- 🔧 **Automatic configuration**: KV namespaces are created automatically
- 📦 **Managed resources**: All dependencies are configured automatically
- 🔄 **Automatic fork**: A copy of the repository is created in your GitHub account

### What happens when you click "Deploy to Cloudflare"?

1. **Repository fork**: A copy is created in your GitHub/GitLab account
2. **Project configuration**: You can customize the Worker name and other details
3. **Resource provisioning**: Required KV namespaces are automatically created
4. **Build & Deploy**: The application is built and deployed to the Cloudflare network

> **Important note**: Remember to configure the secrets (TURNSTILE_SECRET_KEY and JWT_SECRET_KEY) after automatic deployment for the application to work correctly.
