# Cloudflare Workers Rust Auth API

Una API de autenticación construida con Cloudflare Workers y Rust que incluye:

- ✅ Verificación de Cloudflare Turnstile
- ✅ Almacenamiento de usuarios en Cloudflare KV
- ✅ Hashing de contraseñas con Argon2id
- ✅ Generación de JWT con tiempo de expiración configurable

## Características

- **Seguridad**: Protección contra bots con Cloudflare Turnstile
- **Hashing seguro**: Argon2id para el almacenamiento seguro de contraseñas
- **Escalabilidad**: Aprovecha la infraestructura global de Cloudflare
- **JWT**: Autenticación basada en tokens con expiración configurable

## Endpoints

### POST /login
Autentica un usuario existente.

**Headers:**
- `cf-turnstile-response`: Token de Cloudflare Turnstile

**Body:**
```json
{
    "user": "username",
    "password": "password"
}
```

### POST /register
Registra un nuevo usuario.

**Headers:**
- `cf-turnstile-response`: Token de Cloudflare Turnstile

**Body:**
```json
{
    "user": "username",
    "password": "password"
}
```

### GET /health
Verifica el estado de la API.

## Configuración

### Variables de entorno (Secrets en Cloudflare)
- `TURNSTILE_SECRET_KEY`: Clave secreta de Cloudflare Turnstile
- `JWT_SECRET`: Clave secreta para firmar los JWT

### Variables de configuración
- `JWT_EXPIRATION_MINUTES`: Tiempo de expiración de los JWT (default: 15 minutos)

## Desarrollo

```bash
# Instalar dependencias
npm install

# Desarrollo local
npm run dev

# Deploy a Cloudflare
npm run deploy
```

## Configuración inicial

1. Crear un KV namespace en Cloudflare Dashboard
2. Actualizar `wrangler.toml` con el ID del KV namespace
3. Configurar las variables de entorno en Cloudflare Dashboard
4. Configurar Cloudflare Turnstile y obtener las claves

## Estructura del proyecto

```
src/
├── lib.rs          # Punto de entrada principal
├── auth.rs         # Estructuras de autenticación
├── turnstile.rs    # Verificación de Turnstile
└── kv_store.rs     # Operaciones con KV storage
```
