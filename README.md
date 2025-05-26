# Secure Auth API - Cloudflare Workers (Python)

Secure authentication API using Cloudflare Workers with **Python**, Turnstile, Argon2id, and JWT.

> **Note**: This project uses Python Workers which are currently in beta. Only standard library modules are supported in production deployment.

## Features

- ✅ **Python Workers** - Native Python support in Cloudflare Workers
- ✅ **Cloudflare Turnstile** validation for bot protection
- ✅ **Argon2id** password hashing (simplified implementation)
- ✅ **JWT** token generation
- ✅ **Workers KV** storage for user data
- ✅ **CORS** support for web applications

## Prerequisites

1. **Cloudflare account** with Workers enabled
2. **Node.js and npm** installed
3. **Wrangler CLI** installed: `npm install -g wrangler`

## Important Notes

- **Python Workers are in beta** - External packages cannot be deployed to production
- Only **Python standard library** modules work in production
- This implementation uses simplified Argon2id (for production, consider using Workers with JavaScript/TypeScript for full library support)

## Setup Instructions

### 1. Clone and Install Dependencies

```powershell
git clone <repository-url>
cd cloudflare-workers-turnstile-kv-fastapi-auth-argon2id-api
npm install
```

### 2. Login to Cloudflare

```powershell
npx wrangler auth login
```

### 3. Create KV Namespace

```powershell
# Create KV namespace for users
npx wrangler kv:namespace create "USERS_KV"
```

Copy the namespace ID from the output and update `wrangler.toml`:

```toml
[[kv_namespaces]]
binding = "USERS_KV"
id = "your-actual-kv-namespace-id"  # Replace with your ID
preview_id = "your-preview-kv-namespace-id"  # Replace with preview ID
```

### 4. Set Environment Variables

```powershell
# Set Turnstile secret key
npx wrangler secret put TURNSTILE_SECRET_KEY

# Set JWT secret key
npx wrangler secret put JWT_SECRET_KEY
```

### 5. Development

```powershell
# Start local development server
npx wrangler dev
```

### 6. Deploy to Production

```powershell
# Deploy to Cloudflare Workers
npx wrangler deploy
```

## Configuration

### Turnstile Setup

1. Go to [Cloudflare Turnstile](https://developers.cloudflare.com/turnstile/)
2. Create a new site
3. Add your domain(s)
4. Copy the site key (for frontend) and secret key (for this API)
5. Set the secret key using `wrangler secret put TURNSTILE_SECRET_KEY`

### KV Storage Structure

Users are stored in KV with the key format: `user:username`

```json
{
  "id": "user-uuid",
  "username": "testuser",
  "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$salt$hash",
  "created_at": "2024-01-01T00:00:00Z",
  "last_login": "2024-01-01T00:00:00Z"
}
```

## API Endpoints

### POST `/auth/login`

Authenticate user and return JWT token.

**Headers:**
- `Content-Type: application/json`
- `cf-turnstile-token: <turnstile-token>`

**Request Body:**
```json
{
  "username": "testuser",
  "password": "password123"
}
```

**Response (Success):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": "user-uuid",
  "username": "testuser"
}
```

**Response (Error):**
```json
{
  "error": "Invalid credentials"
}
```

### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "auth-api",
  "timestamp": 1640995200
}
```

## Testing

### Create Test User

You can manually add a test user to KV for testing:

```powershell
# Create a test user in KV
npx wrangler kv:key put --binding=USERS_KV "user:testuser" '{
  "id": "test-user-123",
  "username": "testuser", 
  "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$dGVzdHNhbHQ$testhash",
  "created_at": "2024-01-01T00:00:00Z"
}'
```

### Frontend Integration Example

```javascript
// Get Turnstile token first
turnstile.render('#turnstile-widget', {
  sitekey: 'your-turnstile-site-key',
  callback: function(token) {
    // Use token for login
    fetch('https://your-worker.your-subdomain.workers.dev/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'cf-turnstile-token': token
      },
      body: JSON.stringify({
        username: 'testuser',
        password: 'password123'
      })
    })
    .then(response => response.json())
    .then(data => console.log(data));
  }
});
```

## Security Considerations

1. **Simplified Argon2id**: This implementation uses a simplified version of Argon2id. For production with full security requirements, consider using Workers with JavaScript/TypeScript for access to proper cryptographic libraries.

2. **HTTPS Only**: Always use HTTPS in production.

3. **Rate Limiting**: Consider implementing rate limiting for login attempts.

4. **Token Expiration**: JWT tokens expire in 1 hour by default.

5. **Secret Management**: Never commit secrets to version control. Always use `wrangler secret put`.

## Limitations

- **Python Workers Beta**: External packages cannot be deployed to production
- **Standard Library Only**: Only Python standard library modules are supported in production
- **Simplified Crypto**: Uses simplified implementations for compatibility

## Troubleshooting

### Common Issues

1. **Import errors during development**: This is normal - modules like `workers`, `js`, and `pyodide.ffi` are only available in the Workers runtime.

2. **KV namespace not found**: Make sure you've created the KV namespace and updated the ID in `wrangler.toml`.

3. **Secret not found**: Use `wrangler secret put` to set environment variables.

4. **Turnstile validation fails**: Check that your Turnstile secret key is correct and the domain is configured.

## License

MIT License - see LICENSE file for details.
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
