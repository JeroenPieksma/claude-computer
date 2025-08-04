#!/bin/bash

# Start script for Claude Live Viewer
# Runs both the computer-use-demo environment and the backend server

set -e

echo "Starting Claude Live Viewer environment..."

# Apply startup fixes
echo "Applying startup fixes..."
/app/fix-startup.sh

# Start the computer-use-demo desktop environment
echo "Starting desktop environment..."
cd /home/computeruse
./start_all.sh &

# Start noVNC web interface
echo "Starting noVNC web interface..."
cd /home/computeruse
./novnc_startup.sh &

# Start HTTP server for combined interface
echo "Starting HTTP server..."
cd /home/computeruse
python3 http_server.py &

# Wait for desktop to be ready
echo "Waiting for desktop environment..."
sleep 10

# Start Redis if available (optional for basic functionality)
echo "Starting Redis..."
if command -v redis-server >/dev/null 2>&1; then
    redis-server --daemonize yes
    echo "Redis started successfully"
else
    echo "Redis not available, skipping..."
fi

# Start the Claude Live Viewer backend
echo "Starting Claude Live Viewer backend..."
cd /app
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &

# Start the original streamlit interface (optional)
echo "Starting Streamlit interface..."
cd /home/computeruse
python3 -m streamlit run computer_use_demo/streamlit_app.py --server.port 8501 --server.address 0.0.0.0 &

echo "All services started!"
echo "Claude Live Viewer Backend: http://localhost:8000"
echo "Original Streamlit UI: http://localhost:8501"
echo "VNC Desktop: http://localhost:6080/vnc.html"
echo "Combined Interface: http://localhost:8080"

# Keep the container running
wait