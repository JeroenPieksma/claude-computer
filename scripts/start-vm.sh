#!/bin/bash

# Start VM script for Claude Live Viewer
# Builds and runs the Docker container with proper configuration

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Starting Claude Live Viewer VM environment..."

# Load environment variables from .env file
if [ -f "$PROJECT_DIR/.env" ]; then
    echo "Loading environment variables from .env file..."
    export $(grep -v '^#' "$PROJECT_DIR/.env" | xargs)
fi

# Check for required environment variables
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "Error: ANTHROPIC_API_KEY environment variable is required"
    echo "Please set it in .env file or export ANTHROPIC_API_KEY=your_key_here"
    exit 1
fi

# Build the Docker image
echo "Building Docker image..."
cd "$PROJECT_DIR"
docker build -f docker-environment/Dockerfile -t claude-live-viewer .

# Run the container
echo "Starting container..."
docker run \
    --name claude-live-viewer \
    --rm \
    --entrypoint /app/start-live-viewer.sh \
    -e ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
    -e WIDTH=1024 \
    -e HEIGHT=768 \
    -e DISPLAY_NUM=1 \
    -v "$HOME/.anthropic:/home/computeruse/.anthropic" \
    -p 5900:5900 \
    -p 8501:8501 \
    -p 6080:6080 \
    -p 8080:8080 \
    -p 8000:8000 \
    -p 3000:3000 \
    -it claude-live-viewer

echo "Claude Live Viewer VM stopped."