# Configuración del Proyecto

Este documento explica cómo configurar el proyecto para desarrollo y producción.

## 🔐 Sistema de Seguridad JWT Mejorado

### **Características de Seguridad Avanzadas**

Este proyecto implementa un sistema de JWT con seguridad mejorada:

- **JWT Secrets Únicos por Usuario**: Cada usuario tiene su propia clave JWT de 512-bit
- **Rotación Automática**: Las claves JWT se rotan automáticamente cuando:
  - Se cambia la contraseña del usuario
  - Se cambia el nombre de usuario
- **Invalidación Inmediata**: Los tokens existentes se invalidan automáticamente en cambios de credenciales
- **Sin Secreto Global**: No se requiere configurar `JWT_SECRET` global

### **Beneficios de Seguridad**

1. **Aislamiento Total**: Compromiso de un token no afecta otros usuarios
2. **Rotación Automática**: Elimina la necesidad de rotación manual de secretos
3. **Respuesta a Incidentes**: Cambio de contraseña invalida inmediatamente todos los tokens
4. **Configuración Simplificada**: Un secreto menos que gestionar en producción

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
cp .dev.vars.example .dev.vars
```

2. Edita `.dev.vars` con tu valor real:
```bash
TURNSTILE_SECRET_KEY=tu_clave_secreta_de_turnstile
# Nota: JWT_SECRET ya no es necesario - se genera automáticamente por usuario
```

#### Producción

Configura el secreto usando Wrangler CLI:

```bash
# Para producción
wrangler secret put TURNSTILE_SECRET_KEY --env production

# Para staging  
wrangler secret put TURNSTILE_SECRET_KEY --env staging
```

O usa el Dashboard de Cloudflare:
1. Ve a Workers & Pages > Tu Worker > Settings
2. En "Variables and Secrets", añade el secreto:
   - `TURNSTILE_SECRET_KEY`: Tu clave secreta de Turnstile

**Nota**: `JWT_SECRET` ya no es necesario - el sistema genera automáticamente claves JWT únicas de 512-bit para cada usuario.

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
