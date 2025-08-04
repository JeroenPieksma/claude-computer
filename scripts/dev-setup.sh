#!/bin/bash

# Development setup script for Claude Live Viewer

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Setting up Claude Live Viewer development environment..."

# Check for required tools
echo "Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "Error: Node.js is required but not installed"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "Error: Docker is required but not installed"
    exit 1
fi

# Set up backend
echo "Setting up backend..."
cd "$PROJECT_DIR/backend"

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

echo "Backend setup complete!"

# Set up frontend
echo "Setting up frontend..."
cd "$PROJECT_DIR/frontend"

if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

echo "Frontend setup complete!"

# Create .env file if it doesn't exist
cd "$PROJECT_DIR"
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOF
# Claude Live Viewer Environment Variables

# Anthropic API Key (required)
ANTHROPIC_API_KEY=your_api_key_here

# Backend Configuration
BACKEND_HOST=localhost
BACKEND_PORT=8000

# Frontend Configuration
FRONTEND_HOST=localhost
FRONTEND_PORT=3000

# VM Configuration
VM_WIDTH=1024
VM_HEIGHT=768
VM_DISPLAY_NUM=1

# Development Mode
NODE_ENV=development
DEBUG=true
EOF
    echo "Created .env file. Please edit it with your API key and configuration."
fi

echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Anthropic API key"
echo "2. Start the VM: ./scripts/start-vm.sh"
echo "3. In another terminal, start the frontend: cd frontend && npm run dev"
echo ""
echo "Access points:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:8000"
echo "- VM Desktop: http://localhost:6080/vnc.html"
echo ""