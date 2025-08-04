#!/bin/bash
set -e

./start_all.sh
./novnc_startup.sh

# Setup GitHub environment for PR development
echo "🔧 Running GitHub setup script..."
./setup_github.sh || {
    echo "⚠️  GitHub setup failed! Claude won't be able to create PRs."
    echo "⚠️  Please check the logs and ensure the repository is cloned."
}

# Double-check the repository exists
if [ ! -d "$HOME/claude-computer" ]; then
    echo "🚨 CRITICAL: Repository not found at ~/claude-computer!"
    echo "🚨 Attempting manual clone..."
    git clone https://github.com/claude-code-fun/claude-computer.git "$HOME/claude-computer" || {
        echo "❌ Manual clone also failed. Network issues?"
    }
fi

python http_server.py > /tmp/server_logs.txt 2>&1 &

STREAMLIT_SERVER_PORT=8501 python -m streamlit run computer_use_demo/streamlit_app.py > /tmp/streamlit_stdout.log &

echo "✨ Computer Use Demo is ready!"
echo "➡️  Open http://localhost:8080 in your browser to begin"

# Keep the container running
tail -f /dev/null
