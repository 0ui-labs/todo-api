#!/bin/bash
# Validation script for Docker secrets implementation

echo "=== Docker Secrets Validation Script ==="
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the docker directory
if [ ! -f "docker-compose.prod.yml" ]; then
    echo -e "${RED}Error: Please run this script from the docker/ directory${NC}"
    exit 1
fi

echo "1. Checking Docker Compose files..."
if [ -f "docker-compose.yml" ]; then
    echo -e "${GREEN}✓ docker-compose.yml exists${NC}"
else
    echo -e "${RED}✗ docker-compose.yml missing${NC}"
fi

if [ -f "docker-compose.prod.yml" ]; then
    echo -e "${GREEN}✓ docker-compose.prod.yml exists${NC}"
else
    echo -e "${RED}✗ docker-compose.prod.yml missing${NC}"
fi

echo
echo "2. Checking secrets directory..."
if [ -d "secrets" ]; then
    echo -e "${GREEN}✓ secrets/ directory exists${NC}"
    
    # Check for .gitignore in secrets
    if [ -f "secrets/.gitignore" ]; then
        echo -e "${GREEN}✓ secrets/.gitignore exists${NC}"
    else
        echo -e "${RED}✗ secrets/.gitignore missing - credentials might be committed!${NC}"
    fi
    
    # Check for README
    if [ -f "secrets/README.md" ]; then
        echo -e "${GREEN}✓ secrets/README.md exists${NC}"
    else
        echo -e "${YELLOW}! secrets/README.md missing${NC}"
    fi
else
    echo -e "${RED}✗ secrets/ directory missing${NC}"
    exit 1
fi

echo
echo "3. Checking for hardcoded credentials..."
# Check docker-compose files for hardcoded passwords
if grep -i "password\s*[:=]\s*[\"'][^\"']*[\"']" docker-compose.yml docker-compose.prod.yml 2>/dev/null | grep -v "PASSWORD" | grep -v "#"; then
    echo -e "${RED}✗ Found potential hardcoded credentials!${NC}"
else
    echo -e "${GREEN}✓ No hardcoded credentials found in Docker Compose files${NC}"
fi

echo
echo "4. Validating docker-compose.prod.yml syntax..."
if docker-compose -f docker-compose.prod.yml config > /dev/null 2>&1; then
    echo -e "${GREEN}✓ docker-compose.prod.yml syntax is valid${NC}"
else
    echo -e "${RED}✗ docker-compose.prod.yml has syntax errors${NC}"
    docker-compose -f docker-compose.prod.yml config 2>&1 | head -10
fi

echo
echo "5. Checking required secret files..."
REQUIRED_SECRETS=("db_user.txt" "db_password.txt" "redis_password.txt" "jwt_secret_key.txt")
SECRETS_EXIST=true

for secret in "${REQUIRED_SECRETS[@]}"; do
    if [ -f "secrets/$secret" ]; then
        echo -e "${GREEN}✓ secrets/$secret exists${NC}"
        
        # Check if file has content
        if [ ! -s "secrets/$secret" ]; then
            echo -e "${YELLOW}  ! Warning: $secret is empty${NC}"
        fi
        
        # Check for newlines (should not have any)
        if [ -f "secrets/$secret" ] && [ "$(tail -c 1 "secrets/$secret" | wc -l)" -eq 1 ]; then
            echo -e "${YELLOW}  ! Warning: $secret contains a newline at the end${NC}"
        fi
    else
        echo -e "${YELLOW}! secrets/$secret missing (create it for production)${NC}"
        SECRETS_EXIST=false
    fi
done

echo
echo "6. Security scan recommendations..."
echo "   Run these commands to scan for vulnerabilities:"
echo "   - docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image todo-api:latest"
echo "   - pip-audit (for Python dependencies)"
echo "   - safety check (for known vulnerabilities)"

echo
echo "=== Validation Summary ==="
if [ "$SECRETS_EXIST" = true ]; then
    echo -e "${GREEN}All secret files exist. Ready for production deployment!${NC}"
    echo "Deploy with: docker-compose -f docker-compose.prod.yml up -d"
else
    echo -e "${YELLOW}Secret files need to be created before production deployment.${NC}"
    echo "See secrets/README.md for instructions."
fi

echo
echo "For development, use: docker-compose up -d"
echo "For production, use: docker-compose -f docker-compose.prod.yml up -d"