#!/bin/bash

# Setup script for CHOSEN v2
# This script sets up the development environment on Unix-like systems

set -e

echo "=============================================="
echo "CHOSEN v2 - Setup Script"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    echo -e "${GREEN}Found Python $PYTHON_VERSION${NC}"
    if [[ "$PYTHON_VERSION" < "3.11" ]]; then
        echo -e "${RED}Error: Python 3.11+ is required${NC}"
        exit 1
    fi
else
    echo -e "${RED}Error: Python 3 not found. Please install Python 3.11+${NC}"
    exit 1
fi

# Navigate to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# 1. Create virtual environment
echo ""
echo -e "${YELLOW}Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists. Skipping creation.${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}Virtual environment created.${NC}"
fi

# Activate virtual environment
source venv/bin/activate

# 2. Upgrade pip
echo ""
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip

# 3. Install dependencies
echo ""
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r backend/requirements.txt
pip install -r backend/requirements-dev.txt
echo -e "${GREEN}Dependencies installed.${NC}"

# 4. Setup pre-commit hooks
echo ""
echo -e "${YELLOW}Setting up pre-commit hooks...${NC}"
pre-commit install
echo -e "${GREEN}Pre-commit hooks installed.${NC}"

# 5. Create data directories
echo ""
echo -e "${YELLOW}Creating data directories...${NC}"
mkdir -p data/conversations
mkdir -p data/settings
mkdir -p data/cache
mkdir -p data/metadata
mkdir -p logs
echo -e "${GREEN}Data directories created.${NC}"

# 6. Copy environment file
echo ""
echo -e "${YELLOW}Setting up environment...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}Created .env file from .env.example${NC}"
    echo -e "${YELLOW}IMPORTANT: Please edit .env with your Anthropic API key${NC}"
else
    echo -e "${YELLOW}.env file already exists. Skipping.${NC}"
fi

# 7. Check git-crypt
echo ""
echo -e "${YELLOW}Checking git-crypt...${NC}"
if command -v git-crypt &> /dev/null; then
    echo -e "${GREEN}git-crypt is installed.${NC}"
    if [ ! -d ".git-crypt" ]; then
        echo -e "${YELLOW}git-crypt not initialized. Run 'git-crypt init' to initialize encryption.${NC}"
    else
        echo -e "${GREEN}git-crypt is already initialized.${NC}"
    fi
else
    echo -e "${YELLOW}git-crypt not found. Install it for data encryption:${NC}"
    echo "  - macOS: brew install git-crypt"
    echo "  - Ubuntu: sudo apt install git-crypt"
    echo "  - Windows: scoop install git-crypt"
fi

echo ""
echo "=============================================="
echo -e "${GREEN}Setup complete!${NC}"
echo "=============================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Anthropic API key"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Start the server: cd backend && uvicorn app.main:app --reload"
echo "4. Visit http://localhost:8000/api/docs for API documentation"
echo ""
