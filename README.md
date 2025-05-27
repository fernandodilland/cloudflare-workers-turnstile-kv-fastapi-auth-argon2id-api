# Cloudflare Workers Rust Auth API

A secure authentication API built with Cloudflare Workers and Rust featuring:

- ✅ **Bot Protection**: Cloudflare Turnstile verification
- ✅ **Secure Storage**: User data stored in Cloudflare KV
- ✅ **Password Security**: Argon2id password hashing
- ✅ **JWT Authentication**: Configurable token expiration
- ✅ **Global Scale**: Leverages Cloudflare's edge network

## 🚀 Quick Deploy

[![Deploy to Cloudflare](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/YOUR_USERNAME/cloudflare-workers-turnstile-kv-rust-auth-argon2id-api)

*Replace `YOUR_USERNAME` with your GitHub username*

## 📋 API Endpoints

### `POST /register`
Register a new user account.

**Headers:**
- `Content-Type: application/json`
- `cf-turnstile-response: <turnstile_token>`

**Request Body:**
```json
{
    "user": "username",
    "password": "password123"
}
```

**Response:**
```json
{
    "success": true,
    "message": "User registered successfully"
}
```

### `POST /login`
Authenticate an existing user.

**Headers:**
- `Content-Type: application/json`
- `cf-turnstile-response: <turnstile_token>`

**Request Body:**
```json
{
    "user": "username",
    "password": "password123"
}
```

**Response:**
```json
{
    "success": true,
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "message": "Login successful",
    "expires_in": 900
}
```

### `DELETE /user`
Delete the authenticated user's account.

**Headers:**
- `Authorization: Bearer <jwt_token>`

**Response:**
```json
{
    "success": true,
    "message": "User 'username' deleted successfully"
}
```

### `GET /health`
Check API health status.

**Response:**
```json
{
    "status": "healthy",
    "message": "API is running"
}
```

## ⚡ Quick Setup

### Option 1: Automated Setup (Recommended)

1. **Clone and install:**
```powershell
git clone https://github.com/YOUR_USERNAME/cloudflare-workers-turnstile-kv-rust-auth-argon2id-api
cd cloudflare-workers-turnstile-kv-rust-auth-argon2id-api
npm install
```

2. **Run setup script:**
```powershell
# Windows
.\setup.ps1

# Linux/macOS
chmod +x setup.sh
./setup.sh
```

3. **Configure your secrets:**
   - Edit `.dev.vars` with your actual keys
   - Set production secrets: `wrangler secret put TURNSTILE_SECRET_KEY`

### Option 2: Manual Setup

<details>
<summary>Click to expand manual setup instructions</summary>

#### 1. Prerequisites
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/install-and-update/) installed
- Cloudflare account with Workers enabled
- Rust toolchain (for local builds)

#### 2. Create KV Namespaces
```powershell
# Create production namespace
wrangler kv:namespace create "USERS_KV"

# Create preview namespace
wrangler kv:namespace create "USERS_KV" --preview
```

Copy the generated IDs and update `wrangler.toml`:
```toml
[[kv_namespaces]]
binding = "USERS_KV"
id = "your_production_namespace_id"
preview_id = "your_preview_namespace_id"
```

#### 3. Setup Turnstile
1. Go to [Cloudflare Dashboard > Turnstile](https://dash.cloudflare.com/?to=/:account/turnstile)
2. Create a new site
3. Note down your **Site Key** (for frontend) and **Secret Key** (for backend)

#### 4. Configure Secrets

**For local development:**
```powershell
cp .dev.vars.example .dev.vars
# Edit .dev.vars with your actual values
```

**For production:**
```powershell
wrangler secret put TURNSTILE_SECRET_KEY
wrangler secret put JWT_SECRET
```

Generate a secure JWT secret:
```powershell
# PowerShell
$bytes = New-Object byte[] 32; [Security.Cryptography.RNGCryptoServiceProvider]::Create().GetBytes($bytes); [Convert]::ToBase64String($bytes)

# Or use OpenSSL
openssl rand -base64 32
```

</details>

## 🛠️ Development

```powershell
# Local development (uses .dev.vars)
npm run dev

# Remote development
npm run dev:remote

# Build the project
npm run build

# Deploy to staging
npm run deploy:staging

# Deploy to production
npm run deploy:production

# View logs
npm run logs
```

## 📦 Required Environment Variables

| Variable | Description | Where to get it |
|----------|-------------|-----------------|
| `TURNSTILE_SECRET_KEY` | Cloudflare Turnstile secret key | Dashboard > Turnstile > Settings |
| `JWT_SECRET` | JWT signing key (min. 32 chars) | Generate with `openssl rand -base64 32` |

### Optional Configuration Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `JWT_EXPIRATION_MINUTES` | `15` | JWT token expiration time in minutes |

## 🏗️ Project Structure

```
src/
├── lib.rs           # Main entry point and request routing
├── auth.rs          # Authentication types and structures
├── kv_store.rs      # KV storage operations
└── turnstile.rs     # Turnstile verification logic

test_api.ps1         # PowerShell API testing script
test_api.sh          # Bash API testing script
setup.ps1            # Windows setup automation
setup.sh             # Unix setup automation
SETUP.md             # Detailed setup documentation
```

## 🌍 Environment Configuration

The project supports multiple environments with different configurations:

### Development
- **Purpose**: Local development and testing
- **JWT Expiration**: 60 minutes
- **Storage**: Local KV simulation
- **Secrets**: From `.dev.vars` file

### Staging
- **Purpose**: Pre-production testing
- **JWT Expiration**: 30 minutes
- **Deploy**: `npm run deploy:staging`
- **Secrets**: Set via `wrangler secret put --env staging`

### Production
- **Purpose**: Live production environment
- **JWT Expiration**: 15 minutes
- **Deploy**: `npm run deploy:production`
- **Secrets**: Set via `wrangler secret put --env production`

## 🧪 Testing

Test your API endpoints using the provided scripts:

```powershell
# Update the API URL and get a Turnstile token first
# Then run:

# Windows
.\test_api.ps1

# Linux/macOS
chmod +x test_api.sh
./test_api.sh
```

**Before testing:**
1. Update `$API_URL` in the test script with your Worker URL
2. Get a valid Turnstile token from your frontend
3. Replace `$TURNSTILE_TOKEN` in the script

## 🔒 Security Features

- **🛡️ Bot Protection**: Cloudflare Turnstile verification on all authentication endpoints
- **🔐 Secure Password Storage**: Argon2id hashing with random salts
- **🎟️ JWT Authentication**: Stateless token-based authentication
- **⏰ Token Expiration**: Configurable JWT expiration times
- **🌐 CORS Support**: Proper CORS headers for web applications
- **🔄 Environment Isolation**: Separate configurations for dev/staging/production

## 🚀 Deployment

### Deploy with Button (Easiest)
Click the "Deploy to Cloudflare" button above for one-click deployment.

### Deploy with CLI

```powershell
# Deploy to production
wrangler deploy --env production

# Deploy to staging
wrangler deploy --env staging

# Deploy with custom name
wrangler deploy --name my-custom-worker-name
```

### Deployment Checklist

- [ ] KV namespaces created and configured
- [ ] Turnstile site configured
- [ ] Production secrets set (`TURNSTILE_SECRET_KEY`, `JWT_SECRET`)
- [ ] `wrangler.toml` updated with correct namespace IDs
- [ ] Custom domain configured (optional)

## 📊 Monitoring

```powershell
# View real-time logs
npm run logs

# View logs for specific environment
npm run logs:staging
npm run logs:production

# View KV storage usage
wrangler kv:namespace list
```

## 🛠️ Customization

### Adjusting JWT Expiration

Update the `JWT_EXPIRATION_MINUTES` variable in `wrangler.toml` or set it as an environment variable:

```toml
[vars]
JWT_EXPIRATION_MINUTES = "30"  # 30 minutes
```

### Adding Custom Endpoints

1. Add your handler in `src/lib.rs`
2. Update the routing logic in the `main` function
3. Redeploy with `wrangler deploy`

### Custom Password Requirements

Modify the password validation logic in your frontend application. The API accepts any password and hashes it securely with Argon2id.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

- 📖 **Documentation**: [SETUP.md](./SETUP.md) for detailed setup
- 🐛 **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/cloudflare-workers-turnstile-kv-rust-auth-argon2id-api/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/cloudflare-workers-turnstile-kv-rust-auth-argon2id-api/discussions)

## 🔗 Related Resources

- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
- [Cloudflare Turnstile](https://developers.cloudflare.com/turnstile/)
- [Workers KV](https://developers.cloudflare.com/kv/)
- [Rust and WebAssembly](https://rustwasm.github.io/docs/book/)

---

**⭐ If this project helped you, please give it a star!**
