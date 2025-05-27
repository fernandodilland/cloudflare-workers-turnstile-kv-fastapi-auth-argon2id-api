# Configuración del Proyecto

Este documento explica cómo configurar el proyecto para desarrollo y producción.

## Configuración Inicial

### 1. KV Namespaces

Crear los KV namespaces necesarios en Cloudflare Dashboard:

```bash
# Crear namespace de producción
wrangler kv:namespace create "USERS_KV"

# Crear namespace de preview/desarrollo
wrangler kv:namespace create "USERS_KV" --preview
```

Estos comandos te darán los IDs que necesitas reemplazar en `wrangler.toml`:
- `YOUR_PRODUCTION_KV_NAMESPACE_ID`
- `YOUR_PREVIEW_KV_NAMESPACE_ID`

### 2. Turnstile Configuration

1. Ve a Cloudflare Dashboard > Turnstile
2. Crea un nuevo sitio de Turnstile
3. Guarda la **Secret Key** (la necesitarás para los secretos)
4. Guarda la **Site Key** (la necesitarás en tu frontend)

### 3. Secrets Configuration

#### Desarrollo Local

1. Copia el archivo de ejemplo:
```bash
cp .env.example .env.local
# o
cp .dev.vars.example .dev.vars
```

2. Edita `.dev.vars` con tus valores reales:
```bash
TURNSTILE_SECRET_KEY=tu_clave_secreta_de_turnstile
JWT_SECRET=tu_clave_jwt_muy_segura_de_al_menos_32_caracteres
```

#### Producción

Configura los secretos usando Wrangler CLI:

```bash
# Para producción
wrangler secret put TURNSTILE_SECRET_KEY --env production
wrangler secret put JWT_SECRET --env production

# Para staging
wrangler secret put TURNSTILE_SECRET_KEY --env staging
wrangler secret put JWT_SECRET --env staging
```

O usa el Dashboard de Cloudflare:
1. Ve a Workers & Pages > Tu Worker > Settings
2. En "Variables and Secrets", añade los secretos:
   - `TURNSTILE_SECRET_KEY`: Tu clave secreta de Turnstile
   - `JWT_SECRET`: Una clave fuerte para firmar JWT (mínimo 32 caracteres)

## Comandos de Desarrollo

```bash
# Desarrollo local (usa .dev.vars)
npm run dev

# Desarrollo remoto con preview
wrangler dev --remote --env development

# Deploy a staging
wrangler deploy --env staging

# Deploy a producción
wrangler deploy --env production
```

## Estructura de Ambientes

- **development**: Para desarrollo local y testing
- **staging**: Para pruebas pre-producción
- **production**: Para el entorno de producción

Cada ambiente puede tener:
- Sus propios KV namespaces
- Sus propios secretos
- Configuración diferente (como JWT expiration)

## Seguridad

### ✅ Buenas Prácticas Implementadas

- Secretos encriptados para información sensible
- Variables de entorno no comiteadas al repositorio
- Diferentes configuraciones por ambiente
- Placeholders en lugar de IDs hardcodeados

### ⚠️ Importante

- **NUNCA** commitees archivos `.dev.vars` o `.env*`
- **SIEMPRE** usa secretos para API keys y tokens
- **VERIFICA** que `.gitignore` excluya archivos sensibles
- **USA** claves JWT fuertes (mínimo 32 caracteres aleatorios)

## Generación de Claves Seguras

```bash
# Generar una clave JWT segura
openssl rand -base64 32

# Alternativa usando Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

## Troubleshooting

### Error: "KV namespace not found"
- Verifica que hayas creado los KV namespaces
- Asegúrate de haber actualizado los IDs en `wrangler.toml`

### Error: "Turnstile verification failed"
- Verifica que la clave secreta esté configurada correctamente
- Asegúrate de usar la Site Key correcta en el frontend

### Error: "JWT secret not found"
- Configura el secreto `JWT_SECRET` usando `wrangler secret put`
- Para desarrollo local, añádelo a `.dev.vars`
