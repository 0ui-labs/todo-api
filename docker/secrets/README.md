# Docker Secrets Management

This directory contains Docker secrets for production deployment. All files except this README and .gitignore are ignored by git to prevent accidental credential exposure.

## Required Secret Files

Create the following files in this directory before deploying to production:

### 1. `db_user.txt`
PostgreSQL database username (no newline at end)
```bash
echo -n "your_db_user" > db_user.txt
```

### 2. `db_password.txt`
PostgreSQL database password (no newline at end)
```bash
echo -n "your_secure_db_password" > db_password.txt
```

### 3. `redis_password.txt`
Redis password for authentication (no newline at end)
```bash
echo -n "your_secure_redis_password" > redis_password.txt
```

### 4. `jwt_secret_key.txt`
JWT secret key for token signing (no newline at end)
```bash
# Generate a secure random key:
python -c "import secrets; print(secrets.token_urlsafe(64))" | tr -d '\n' > jwt_secret_key.txt
```

## Security Best Practices

1. **Never commit secret files to git** - The .gitignore in this directory ensures all files except README.md and .gitignore are ignored

2. **Use strong passwords** - Generate passwords with sufficient entropy:
   ```bash
   # Example: Generate a 32-character password
   openssl rand -base64 32 | tr -d '\n' > password.txt
   ```

3. **Set proper file permissions**:
   ```bash
   chmod 600 *.txt
   ```

4. **Rotate secrets regularly** - Update secrets periodically and after any potential compromise

5. **Use a secrets management system** in production (e.g., HashiCorp Vault, AWS Secrets Manager, Kubernetes Secrets)

## Production Deployment

To deploy with Docker Compose in production:

```bash
# From the docker directory
docker-compose -f docker-compose.prod.yml up -d
```

## Alternative: Docker Swarm Secrets

For Docker Swarm deployments, create secrets using:

```bash
# Create secrets in Docker Swarm
echo -n "your_db_user" | docker secret create db_user -
echo -n "your_db_password" | docker secret create db_password -
echo -n "your_redis_password" | docker secret create redis_password -
echo -n "your_jwt_secret" | docker secret create jwt_secret_key -
```

Then update `docker-compose.prod.yml` to use external secrets:

```yaml
secrets:
  db_user:
    external: true
  db_password:
    external: true
  redis_password:
    external: true
  jwt_secret_key:
    external: true
```

## Environment Variables Alternative

For non-Docker deployments or development, you can still use environment variables by creating a `.env` file in the project root (never commit this file):

```bash
# Copy from .env.example and update with real values
cp ../.env.example ../.env
# Edit ../.env with your secure credentials
```

## Verification

After setting up secrets, verify they're working:

```bash
# Check if secrets are readable
docker-compose -f docker-compose.prod.yml config

# Test the deployment
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs app
```