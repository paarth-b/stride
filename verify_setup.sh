#!/bin/bash

# Stride Setup Verification Script
# Checks if all components are properly configured

echo "=================================="
echo "Stride Setup Verification"
echo "=================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Docker
echo "Checking Docker..."
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓${NC} Docker is installed"
    if docker ps &> /dev/null; then
        echo -e "${GREEN}✓${NC} Docker is running"
    else
        echo -e "${RED}✗${NC} Docker is not running. Please start Docker Desktop."
    fi
else
    echo -e "${RED}✗${NC} Docker is not installed. Please install Docker Desktop."
fi
echo ""

# Check Python
echo "Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✓${NC} Python is installed (version $PYTHON_VERSION)"
else
    echo -e "${RED}✗${NC} Python 3 is not installed"
fi
echo ""

# Check Node.js
echo "Checking Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓${NC} Node.js is installed (version $NODE_VERSION)"
else
    echo -e "${RED}✗${NC} Node.js is not installed"
fi

if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✓${NC} npm is installed (version $NPM_VERSION)"
else
    echo -e "${RED}✗${NC} npm is not installed"
fi
echo ""

# Check Backend Files
echo "Checking Backend Files..."
if [ -f "backend/requirements.txt" ]; then
    echo -e "${GREEN}✓${NC} requirements.txt exists"
else
    echo -e "${RED}✗${NC} requirements.txt missing"
fi

if [ -f "backend/app/main.py" ]; then
    echo -e "${GREEN}✓${NC} main.py exists"
else
    echo -e "${RED}✗${NC} main.py missing"
fi

if [ -f "backend/.env" ]; then
    echo -e "${GREEN}✓${NC} .env exists"
else
    echo -e "${YELLOW}⚠${NC} .env missing (will use defaults)"
fi
echo ""

# Check Frontend Files
echo "Checking Frontend Files..."
if [ -f "frontend/package.json" ]; then
    echo -e "${GREEN}✓${NC} package.json exists"
else
    echo -e "${RED}✗${NC} package.json missing"
fi

if [ -f "frontend/src/App.tsx" ]; then
    echo -e "${GREEN}✓${NC} App.tsx exists"
else
    echo -e "${RED}✗${NC} App.tsx missing"
fi

if [ -d "frontend/node_modules" ]; then
    echo -e "${GREEN}✓${NC} node_modules exists"
else
    echo -e "${YELLOW}⚠${NC} node_modules missing (run 'npm install' in frontend/)"
fi
echo ""

# Check Docker Compose
echo "Checking Docker Compose..."
if [ -f "docker-compose.yml" ]; then
    echo -e "${GREEN}✓${NC} docker-compose.yml exists"
else
    echo -e "${RED}✗${NC} docker-compose.yml missing"
fi
echo ""

# Check if PostgreSQL container is running
echo "Checking PostgreSQL Container..."
if docker ps | grep -q stride-postgres; then
    echo -e "${GREEN}✓${NC} PostgreSQL container is running"
else
    echo -e "${YELLOW}⚠${NC} PostgreSQL container not running. Run 'docker-compose up -d'"
fi
echo ""

# Summary
echo "=================================="
echo "Verification Complete"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. If Docker is not running, start Docker Desktop"
echo "2. Run: docker-compose up -d"
echo "3. Run: cd backend && ./start_backend.sh"
echo "4. Run: cd frontend && ./start_frontend.sh"
echo "5. Open: http://localhost:5173"
echo ""
