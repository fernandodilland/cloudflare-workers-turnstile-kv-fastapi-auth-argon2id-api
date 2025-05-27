# Cloudflare Workers Rust Auth API

A secure authentication API built with Cloudflare Workers and Rust featuring:

- ✅ **Bot Protection**: Cloudflare Turnstile verification
- ✅ **Secure Storage**: User data stored in Cloudflare KV
- ✅ **Password Security**: Argon2id password hashing
- ✅ **JWT Authentication**: Configurable token expiration
- ✅ **Global Scale**: Leverages Cloudflare's edge network

## 🚀 Setup and Installation

### 📋 Prerequisites

Before starting, make sure you have:

- [ ] **Cloudflare Account** ([Sign up for free](https://cloudflare.com))
- [ ] **Workers Plan enabled** (Free tier included)
- [ ] **Node.js** (version 18 or higher) - [Download](https://nodejs.org)
- [ ] **Rust** installed - [Install](https://rustup.rs/)
- [ ] **LLVM** installed - [Download](https://releases.llvm.org/download.html) or install via package manager
- [ ] **Git** installed - [Download](https://git-scm.com/)

### ⚡ Quick Installation

#### **Step 1: Clone the Repository**

```powershell
# Clone the repository
git clone https://github.com/YOUR_USERNAME/cloudflare-workers-turnstile-kv-rust-auth-argon2id-api.git
cd cloudflare-workers-turnstile-kv-rust-auth-argon2id-api

# Install dependencies
npm install
```

#### **Step 2: Install Wrangler CLI**

```powershell
# Install Wrangler globally
npm install -g wrangler

# Authenticate with Cloudflare
wrangler login
```

#### **Step 3: Create KV Namespaces**

Create the required KV storage namespaces:

```powershell
# Create production namespace
wrangler kv:namespace create "USERS_KV"

# Create preview namespace for development
wrangler kv:namespace create "USERS_KV" --preview
```

Copy the generated namespace IDs and update `wrangler.toml`:

```toml
[[kv_namespaces]]
binding = "USERS_KV"
id = "your_production_namespace_id"        # Replace with your production ID
preview_id = "your_preview_namespace_id"   # Replace with your preview ID
```

#### **Step 4: Configure Turnstile (Bot Protection)**

1. **Go to Cloudflare Dashboard:**
   - Navigate to [Cloudflare Dashboard → Turnstile](https://dash.cloudflare.com/?to=/:account/turnstile)
   - Click **"Add Site"**

2. **Configure the site:**
   ```
   Site name: My Auth API (or your preference)
   Domain: your-domain.com (or localhost for testing)
   Widget Mode: Managed (recommended)
   ```

3. **📝 SAVE THESE KEYS** (you'll need them in the next step):
   - 🔑 **Site Key**: `0x4AAAAAAAxxxxxxxxxxxxxxxx` (for frontend)
   - 🔐 **Secret Key**: `0x4AAAAAAAxxxxxxxxxxxxxxxx` (for Worker - KEEP PRIVATE!)

#### **Step 5: Generate JWT Secret**

Generate a strong JWT secret for token signing:

```powershell
# PowerShell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))

# Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"

# OpenSSL
openssl rand -base64 32
```

**📝 Keep these ready:**
- [ ] **Turnstile Secret Key** (from Step 4)
- [ ] **JWT Secret** (generated above)

#### **Step 6: Configure Local Development**

1. **Create local environment file:**
```powershell
# Copy the example file
cp .dev.vars.example .dev.vars
```

2. **Edit `.dev.vars` with your actual values:**
```bash
# Cloudflare Turnstile Secret Key
TURNSTILE_SECRET_KEY=your_turnstile_secret_key_here

# JWT Secret Key for signing tokens
JWT_SECRET=your_very_secure_jwt_secret_key_here_at_least_32_chars
```

#### **Step 7: Set Production Secrets**

Configure the secrets for production deployment:

```powershell
# Set Turnstile secret key
wrangler secret put TURNSTILE_SECRET_KEY
# When prompted, paste your Turnstile Secret Key

# Set JWT secret
wrangler secret put JWT_SECRET
# When prompted, paste your generated JWT secret
```

#### **Step 8: Deploy the Worker**

Now you're ready to deploy:

```powershell
# Build and deploy to production
npm run build
npm run deploy

# Or deploy to staging first
npm run deploy:staging
```

#### **Step 9: Test Your Deployment**

Verify your API is working:

```powershell
# Test health endpoint (replace with your worker URL)
curl https://your-worker-name.your-subdomain.workers.dev/health

# Expected response:
# {"status": "healthy", "message": "API is running"}
```

---

## 🛠️ Development

#### **🧪 Test Your Deployment (Recommended)**

Update the test scripts with your Worker URL:

1. **Edit test scripts:**
```powershell
# Update test_api.ps1 or test_api.sh
# Replace $API_URL with your actual Worker URL
# Replace $TURNSTILE_TOKEN with a valid token from your frontend
```

2. **Run tests:**
```powershell
# Windows
.\test_api.ps1

# Linux/macOS
chmod +x test_api.sh
./test_api.sh
```

**🎨 Want to test with a real frontend?** Check out our example implementations:
- [React Example](https://github.com/cloudflare/turnstile-demo)
- [Vanilla JS Example](https://developers.cloudflare.com/turnstile/get-started/client-side-rendering/)

#### **🌐 Production Recommendations**

**🔒 Security Enhancements:**
- Set up a custom domain for production use
- Enable Cloudflare's security features (Bot Fight Mode, Rate Limiting)
- Use different secrets for staging/production environments
- Monitor your Worker logs regularly

**⚡ Performance Optimization:**
```powershell
# Optional: Set up multiple environments
wrangler secret put TURNSTILE_SECRET_KEY --env production
wrangler secret put JWT_SECRET --env production
```

**📊 Monitoring Setup:**
1. Go to **Workers & Pages** → **Your Worker** → **Metrics**
2. Set up alerts for error rates or high usage
3. Monitor KV operations in the **KV** section

#### **🔄 Update Turnstile Configuration**

After deployment, update your Turnstile site settings:
1. Go back to [Cloudflare Dashboard → Turnstile](https://dash.cloudflare.com/?to=/:account/turnstile)
2. Edit your site
3. Add your Worker URL to the **Domain** field:
   ```
   your-worker-name.your-subdomain.workers.dev
   ```
4. Save changes

---

### 🎉 **Congratulations!**

Your secure authentication API is now live! Here's what you've achieved:

✅ **Deployed** a production-ready Rust API to Cloudflare's edge network  
✅ **Secured** with Turnstile bot protection and Argon2id password hashing  
✅ **Configured** with proper secrets management  
✅ **Ready** for frontend integration  

**🚀 Next Steps:**
- Integrate with your frontend application
- Customize the API for your specific needs
- Set up monitoring and alerts
- Consider adding rate limiting for additional security

**📖 Need help?** Check out the detailed [API documentation](#-api-endpoints) below or visit our [Setup Guide](SETUP.md).

---

## 🛠️ Manual Setup

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

## 📦 Environment Variables

| Variable | Description | Where to get it |
|----------|-------------|-----------------|
| `TURNSTILE_SECRET_KEY` | Cloudflare Turnstile secret key | Dashboard > Turnstile > Settings |
| `JWT_SECRET` | JWT signing key (min. 32 chars) | Generate with `openssl rand -base64 32` |
| `JWT_EXPIRATION_MINUTES` | JWT token expiration (optional, default: 15) | Any number in minutes |

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

## 💻 Development Commands

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

## 🌍 Environment Configuration

The project supports multiple environments:

### Development
- **Purpose**: Local development and testing
- **JWT Expiration**: 60 minutes
- **Secrets**: From `.dev.vars` file

### Staging
- **Purpose**: Pre-production testing
- **JWT Expiration**: 30 minutes
- **Deploy**: `npm run deploy:staging`

### Production
- **Purpose**: Live production environment
- **JWT Expiration**: 15 minutes
- **Deploy**: `npm run deploy:production`

## 🚀 Deployment

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

## 🚨 Troubleshooting

### API Response Issues

**❌ "Invalid turnstile token" responses**
- Verify your Turnstile Site Key is correct in your frontend
- Ensure your Turnstile site domain matches your Worker URL
- Check that `TURNSTILE_SECRET_KEY` secret is set correctly
- Test with a fresh Turnstile token (they expire quickly)

**❌ "Internal server error" responses**
```powershell
# Check Worker logs for detailed error messages
wrangler tail your-worker-name

# Common causes:
# 1. Missing secrets (JWT_SECRET or TURNSTILE_SECRET_KEY)
# 2. KV namespace not properly configured
# 3. Invalid JSON in request body
```

**❌ CORS errors in browser**
- The Worker includes CORS headers, but check your request format
- Ensure you're sending `Content-Type: application/json` header
- Try the request with curl first to isolate browser issues

### Local Development Issues

**❌ "Missing .dev.vars file" errors**
```powershell
# Copy the example file and edit it
cp .dev.vars.example .dev.vars
# Edit .dev.vars with your actual secrets
```

**❌ "KV namespace not found" in development**
- Ensure your `wrangler.toml` has the correct namespace IDs
- Run `wrangler kv:namespace list` to verify namespaces exist
- For local dev, you can use `--local` flag: `wrangler dev --local`

**❌ Rust build errors**
- Ensure you have the Rust toolchain installed
- Run `rustup target add wasm32-unknown-unknown`
- Clear cache: `cargo clean` then `wrangler deploy`

### Performance Issues

**❌ Slow response times**
- Check your Worker's metrics in Cloudflare Dashboard
- Monitor KV operations (they have small latency)
- Consider using a custom domain for better performance

**❌ "Script exceeded CPU time limit"**
- This usually indicates an issue with Argon2id hashing settings
- Check if you're using reasonable password lengths (<1000 characters)
- Contact support if this persists with normal usage

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `Missing required header: cf-turnstile-response` | Frontend not sending Turnstile token | Add Turnstile widget to your frontend |
| `Invalid JSON body` | Malformed request | Check request format matches API docs |
| `User already exists` | Attempting to register existing username | Use a different username or implement login |
| `Invalid credentials` | Wrong username/password in login | Verify credentials or register new user |
| `Token verification failed` | Invalid JWT in Authorization header | Check token format: `Bearer <token>` |

### Getting Help

If you're still having issues:

1. **Check the logs**: `wrangler tail your-worker-name`
2. **Verify your setup**: Compare with [SETUP.md](./SETUP.md)
3. **Test with curl**: Use the provided curl commands to isolate issues
4. **Create an issue**: Include:
   - Error message or behavior
   - Steps to reproduce
   - Your `wrangler.toml` (remove sensitive data)
   - Worker logs if available

**🔍 Debug mode**: Set `LOG_LEVEL=debug` in your environment variables for verbose logging.

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
