# Cloudflare Workers Rust Auth API

A secure authentication API built with Cloudflare Workers and Rust featuring:

- ✅ **Bot Protection**: Cloudflare Turnstile verification
- ✅ **Secure Storage**: User data stored in Cloudflare KV
- ✅ **Password Security**: Argon2id password hashing
- ✅ **JWT Authentication**: Configurable token expiration
- ✅ **Global Scale**: Leverages Cloudflare's edge network

## 🚀 Quick Deploy

> **⚡ Get your secure auth API running in under 5 minutes!**

### 📋 Pre-deployment Checklist

**Before clicking the Deploy button, ensure you have completed ALL these steps:**

#### ☑️ **STEP 1: Fork & Customize Repository**

1. **🍴 Fork this repository:**
   - Click the **"Fork"** button at the top of this page
   - Select your GitHub account
   - Wait for the fork to complete

2. **📝 Update YOUR repository (in your fork):**
   - **In `README.md`**: Replace `YOUR_USERNAME` with your GitHub username (line 58)
   - **In `package.json`**: Update all repository URLs to use your username

   💡 **Quick find & replace**: Search for `YOUR_USERNAME` and replace all instances with your actual GitHub username.

#### ☑️ **STEP 2: Cloudflare Account Setup**

**📋 Account Requirements:**
- [ ] Active Cloudflare account ([Sign up free](https://cloudflare.com))
- [ ] Workers plan enabled (Free tier included)
- [ ] Logged into Cloudflare Dashboard

#### ☑️ **STEP 3: Create Turnstile Site (REQUIRED)**

**🛡️ Bot Protection Setup:**
1. Navigate to [Cloudflare Dashboard → Turnstile](https://dash.cloudflare.com/?to=/:account/turnstile)
2. Click **"Add Site"**
3. **Configure your site:**
   ```
   Site name: My Auth API (or your choice)
   Domain: your-domain.com (or localhost for testing)
   Widget mode: Managed (recommended)
   ```
4. **📝 SAVE THESE KEYS** (you'll need them in the next step):
   - 🔑 **Site Key**: `0x4AAAAAAAxxxxxxxxxxxxxxxx` (for frontend)
   - 🔐 **Secret Key**: `0x4AAAAAAAxxxxxxxxxxxxxxxx` (for Worker - KEEP PRIVATE!)

   ⚠️ **Important**: Don't close this tab! You'll need these keys immediately after deployment.

#### ☑️ **STEP 4: Prepare Your Secrets**

**🔐 Generate a strong JWT secret NOW** (you'll need it right after deployment):

**Option A - Online Generator (easiest):**
- Visit [generate-secret.vercel.app](https://generate-secret.vercel.app/32) 
- Copy the generated 32-character secret

**Option B - Command Line:**
```bash
# Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"

# PowerShell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))

# OpenSSL
openssl rand -base64 32
```

**📝 Keep these ready:**
- [ ] **Turnstile Secret Key** (from Step 3)
- [ ] **JWT Secret** (generated above)

### 🚀 **DEPLOY NOW!**

**✅ Completed all pre-deployment steps above?** Great! Click the button below:

<div align="center">

[![Deploy to Cloudflare](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/YOUR_USERNAME/cloudflare-workers-turnstile-kv-rust-auth-argon2id-api)

**⚠️ Replace `YOUR_USERNAME` with your GitHub username before clicking!**

</div>

**📋 What happens when you click:**
1. Cloudflare will clone your fork
2. Build the Rust Worker automatically
3. Create the required KV namespace (`USERS_KV`)
4. Deploy to your chosen subdomain
5. Provide you with a Worker URL

**⏱️ Expected deployment time: 2-3 minutes**

---

### 🔧 **IMMEDIATE Post-deployment Steps**

**🚨 COMPLETE THESE STEPS RIGHT AFTER DEPLOYMENT OR YOUR API WON'T WORK!**

#### **Step 1: Add Required Secrets (2 minutes)**

The deployment creates the Worker structure, but you must add the secrets manually for security:

```bash
# Navigate to your project (if working locally)
cd your-project-folder

# Add your Turnstile secret key (from pre-deployment Step 3)
wrangler secret put TURNSTILE_SECRET_KEY
# When prompted, paste your Turnstile Secret Key

# Add your JWT secret (from pre-deployment Step 4)
wrangler secret put JWT_SECRET
# When prompted, paste your generated JWT secret
```

**🌐 Alternative: Use Cloudflare Dashboard**
1. Go to [Cloudflare Dashboard → Workers & Pages](https://dash.cloudflare.com/?to=/:account/workers)
2. Click on your newly deployed Worker
3. Go to **Settings** → **Variables and Secrets**
4. Click **Add Variable** → **Environment Variable** (for secrets):
   - Add `TURNSTILE_SECRET_KEY` with your Turnstile secret
   - Add `JWT_SECRET` with your generated JWT secret

#### **Step 2: Verify Deployment (1 minute)**

**✅ Quick Health Check:**
```bash
# Test if your API is responding
curl https://your-worker-name.your-subdomain.workers.dev/health

# Expected response:
# {"status": "healthy", "timestamp": "2024-01-01T12:00:00.000Z"}
```

**📋 Verify KV Namespace Creation:**
```bash
wrangler kv:namespace list
# Should show: USERS_KV namespace
```

#### **Step 3: Get Your API Credentials**

**🔑 For Frontend Integration:**
- **API URL**: `https://your-worker-name.your-subdomain.workers.dev`
- **Turnstile Site Key**: Use the Site Key from pre-deployment Step 3
- **Available Endpoints**: `/register`, `/login`, `/protected`, `/health`

**📝 Save these details** - you'll need them for your frontend application!

---

### 🎯 **OPTIONAL: Advanced Configuration**

#### **🧪 Test Your Deployment (Recommended)**

**Test the registration endpoint:**
```bash
# Replace YOUR_WORKER_URL with your actual Worker URL
curl -X POST https://YOUR_WORKER_URL/register \
  -H "Content-Type: application/json" \
  -H "cf-turnstile-response: DEMO_TOKEN" \
  -d '{
    "user": "testuser",
    "password": "testpassword123"
  }'
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
```bash
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

## ⚡ **TL;DR for Experienced Developers**

<details>
<summary><b>🚀 Skip the detailed guide - Quick commands for experienced devs</b></summary>

```bash
# 1. Fork repo, replace YOUR_USERNAME in README.md and package.json

# 2. Create Turnstile site at https://dash.cloudflare.com/?to=/:account/turnstile
#    Save your SITE_KEY and SECRET_KEY

# 3. Deploy via button (after updating YOUR_USERNAME):
#    https://deploy.workers.cloudflare.com/?url=https://github.com/YOUR_USERNAME/cloudflare-workers-turnstile-kv-rust-auth-argon2id-api

# 4. Set secrets immediately after deployment:
wrangler secret put TURNSTILE_SECRET_KEY    # Your Turnstile secret
wrangler secret put JWT_SECRET              # Generate with: openssl rand -base64 32

# 5. Test endpoints:
curl -X POST https://YOUR_WORKER.workers.dev/register \
  -H "Content-Type: application/json" \
  -H "cf-turnstile-response: YOUR_TURNSTILE_TOKEN" \
  -d '{"user":"test","password":"test123"}'

curl -X POST https://YOUR_WORKER.workers.dev/login \
  -H "Content-Type: application/json" \
  -H "cf-turnstile-response: YOUR_TURNSTILE_TOKEN" \
  -d '{"user":"test","password":"test123"}'

# Done! Your API is live with:
# - Turnstile bot protection
# - Argon2id password hashing  
# - JWT authentication
# - KV storage
# - Global edge deployment
```

**📋 Required Setup:**
- Cloudflare account with Workers enabled
- Turnstile site created (get Site Key + Secret Key)
- Replace YOUR_USERNAME in deploy URL
- Set 2 secrets post-deployment: TURNSTILE_SECRET_KEY + JWT_SECRET

**🔗 Key URLs:**
- **Turnstile Setup**: https://dash.cloudflare.com/?to=/:account/turnstile
- **Deploy Button**: Replace YOUR_USERNAME then click
- **API Docs**: See below for endpoint details

</details>

---

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

## 🚨 Troubleshooting

### Deploy Button Issues

**❌ "Repository not found" error**
- Ensure you've forked the repository to your GitHub account
- Replace `YOUR_USERNAME` in the deploy URL with your actual GitHub username
- Make sure your fork is public (Deploy to Cloudflare can't access private repos)

**❌ "Build failed" during deployment**
- Check that all required files are present in your fork
- Ensure `wrangler.toml` is valid (no syntax errors)
- Wait a few minutes and try again (sometimes it's a temporary issue)

**❌ Deployment succeeds but API returns errors**
- Most likely cause: Missing secrets (see [Post-deployment Steps](#-immediate-post-deployment-steps))
- Check that both `TURNSTILE_SECRET_KEY` and `JWT_SECRET` are set

### API Response Issues

**❌ "Invalid turnstile token" responses**
- Verify your Turnstile Site Key is correct in your frontend
- Ensure your Turnstile site domain matches your Worker URL
- Check that `TURNSTILE_SECRET_KEY` secret is set correctly
- Test with a fresh Turnstile token (they expire quickly)

**❌ "Internal server error" responses**
```bash
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
```bash
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
