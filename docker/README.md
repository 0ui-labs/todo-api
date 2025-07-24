# Docker Deployment Guide

This directory contains Docker configuration files for the Todo API.

## Files Overview

- `Dockerfile` - Multi-stage build for the application
- `docker-compose.yml` - Development configuration (uses .env file)
- `docker-compose.prod.yml` - Production configuration (uses Docker secrets)
- `secrets/` - Directory for Docker secrets (see secrets/README.md)

## Development Deployment

For development, use the standard docker-compose.yml:

```bash
# From project root, copy and configure environment
cp .env.example .env
# Edit .env with your development values

# From docker directory
cd docker
docker-compose up -d
```

## Production Deployment

For production, use docker-compose.prod.yml with Docker secrets:

### 1. Set up secrets

```bash
cd docker/secrets

# Create secret files (no newlines at end)
echo -n "produser" > db_user.txt
echo -n "secure_db_password_here" > db_password.txt  
echo -n "secure_redis_password_here" > redis_password.txt

# Generate JWT secret
python -c "import secrets; print(secrets.token_urlsafe(64))" | tr -d '\n' > jwt_secret_key.txt

# Set proper permissions
chmod 600 *.txt
```

### 2. Configure environment

Create a minimal .env file for non-sensitive configuration:

```bash
# In project root
cat > .env.prod << EOF
DATABASE_NAME=todo_db_prod
BACKEND_CORS_ORIGINS=["https://api.yourdomain.com","https://yourdomain.com"]
EOF
```

### 3. Deploy

```bash
cd docker
docker-compose -f docker-compose.prod.yml --env-file ../.env.prod up -d
```

## Security Features

The production configuration implements several security improvements:

1. **Docker Secrets** - Sensitive credentials are stored as Docker secrets, not environment variables
2. **Network Isolation** - Services communicate over an internal Docker network
3. **No Plaintext Credentials** - All passwords are loaded from secret files at runtime
4. **Redis Authentication** - Redis requires password authentication
5. **Health Checks** - All services have proper health checks

## Verification

After deployment, verify the security configuration:

```bash
# Check no credentials in environment
docker-compose -f docker-compose.prod.yml exec app env | grep -E '(PASSWORD|SECRET)'
# Should return empty

# Verify services are healthy
docker-compose -f docker-compose.prod.yml ps

# Check logs for errors
docker-compose -f docker-compose.prod.yml logs --tail=50

# Test API endpoint
curl http://localhost:8000/health
```

## Container Security Scan

Run security scans on the built image:

```bash
# Build the image
docker build -t todo-api:latest .

# Scan with Trivy
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image todo-api:latest

# Scan with Docker Scout
docker scout cves todo-api:latest
```

## Troubleshooting

### Secrets not found
- Ensure all .txt files exist in docker/secrets/
- Check file permissions (should be readable by Docker)
- Verify no trailing newlines in secret files

### Database connection issues
- Check db_user.txt and db_password.txt match PostgreSQL configuration
- Verify DATABASE_NAME environment variable is set
- Check service health: `docker-compose -f docker-compose.prod.yml ps`

### Redis authentication failures
- Ensure redis_password.txt exists and contains the password
- Check Redis logs: `docker-compose -f docker-compose.prod.yml logs redis`