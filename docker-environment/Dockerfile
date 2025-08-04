# Extended Dockerfile based on Anthropic's computer-use-demo
# Adds Claude Live Viewer backend integration

FROM ghcr.io/anthropics/anthropic-quickstarts:computer-use-demo-latest

# Switch to root to install packages
USER root

# Install additional dependencies for Claude Live Viewer
RUN apt-get update && apt-get install -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set up Python environment for backend
WORKDIR /app
COPY backend/requirements.txt .
RUN pip3 install -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy the computer-use-demo dependency
COPY computer-use-demo/ ./computer-use-demo/

# Fix the streamlit.py naming conflict
RUN if [ -f /home/computeruse/computer_use_demo/streamlit.py ]; then \
    mv /home/computeruse/computer_use_demo/streamlit.py /home/computeruse/computer_use_demo/streamlit_app.py; \
    fi

# Set environment variables
ENV PYTHONPATH=/app:/home/computeruse/computer_use_demo
ENV CLAUDE_LIVE_VIEWER=true

# Expose additional ports for backend
EXPOSE 8000

# Create startup script that runs both computer-use-demo and backend
COPY docker-environment/start-live-viewer.sh /app/start-live-viewer.sh
COPY docker-environment/fix-startup.sh /app/fix-startup.sh
RUN chmod +x /app/start-live-viewer.sh /app/fix-startup.sh

# Switch back to the computeruse user
USER computeruse

# Set the default command
CMD ["/app/start-live-viewer.sh"]