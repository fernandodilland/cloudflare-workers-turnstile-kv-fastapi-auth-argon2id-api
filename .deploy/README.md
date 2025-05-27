# Deploy to Cloudflare Configuration

This directory contains configuration files for the Deploy to Cloudflare button functionality.

The Deploy to Cloudflare service will automatically:

1. **Clone your repository** into the user's GitHub/GitLab account
2. **Create KV namespaces** automatically based on wrangler.toml configuration
3. **Set up the build environment** with the correct Rust toolchain
4. **Deploy the Worker** to Cloudflare's edge network

## Automatic Resource Provisioning

The following resources will be automatically created:

- **KV Namespace**: `USERS_KV` (for user data storage)
- **Preview KV Namespace**: For development and testing

## Required Secrets

Users will need to manually configure these secrets after deployment:

```bash
wrangler secret put TURNSTILE_SECRET_KEY
wrangler secret put JWT_SECRET
```

## Build Process

The deployment service will:

1. Install Rust toolchain
2. Install `worker-build` via cargo
3. Run `npm run build` (which executes `worker-build --release`)
4. Deploy using `wrangler deploy`

## User Instructions

After deployment, users should:

1. Get their Turnstile keys from Cloudflare Dashboard
2. Generate a secure JWT secret
3. Set the required secrets via Wrangler CLI
4. Test the API endpoints

The deployment button provides a streamlined experience for getting started with this authentication API.
