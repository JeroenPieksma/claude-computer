"""
Claude Live Viewer Backend Server
Streams Claude's computer interactions in real-time
"""

import asyncio
import base64
import json
import logging
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path="../.env")

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.claude_agent import ClaudeAgent
from backend.screen_capture import ScreenCaptureService
from backend.activity_logger import ActivityLogger
from backend.behavioral_system import BehavioralSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Claude Live Viewer", version="1.0.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global services
claude_agent: Optional[ClaudeAgent] = None
screen_service: Optional[ScreenCaptureService] = None
activity_logger: Optional[ActivityLogger] = None
behavioral_system: Optional[BehavioralSystem] = None

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, data: dict):
        """Broadcast data to all connected clients"""
        if not self.active_connections:
            return
        
        message = json.dumps(data)
        disconnected = []
        
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.append(connection)
        
        # Remove disconnected clients
        for conn in disconnected:
            self.disconnect(conn)

manager = ConnectionManager()

# Pydantic models
class AgentCommand(BaseModel):
    command: str
    parameters: Optional[Dict] = None

class BehaviorConfig(BaseModel):
    behavior_type: str
    parameters: Dict
    duration_minutes: Optional[int] = None

class ChatMessage(BaseModel):
    message: str
    sender: str = "user"

# API Routes
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "services": {
            "claude_agent": claude_agent is not None,
            "screen_capture": screen_service is not None,
            "activity_logger": activity_logger is not None,
            "behavioral_system": behavioral_system is not None
        }
    }

@app.get("/api/status")
async def get_status():
    """Get current system status"""
    return {
        "connected_clients": len(manager.active_connections),
        "agent_active": claude_agent.is_active if claude_agent else False,
        "current_behavior": behavioral_system.current_behavior if behavioral_system else None,
        "screen_resolution": screen_service.get_resolution() if screen_service else None,
        "activity_count": len(activity_logger.get_recent_activities()) if activity_logger else 0
    }

@app.post("/api/agent/command")
async def send_agent_command(command: AgentCommand):
    """Send a command to Claude agent"""
    if not claude_agent:
        raise HTTPException(status_code=503, detail="Claude agent not initialized")
    
    try:
        result = await claude_agent.execute_command(command.command, command.parameters)
        return {"success": True, "result": result}
    except Exception as e:
        logger.error(f"Error executing agent command: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/behavior/start")
async def start_behavior(config: BehaviorConfig):
    """Start a behavioral pattern for Claude"""
    if not behavioral_system:
        raise HTTPException(status_code=503, detail="Behavioral system not initialized")
    
    try:
        await behavioral_system.start_behavior(
            config.behavior_type, 
            config.parameters, 
            config.duration_minutes
        )
        return {"success": True, "message": f"Started behavior: {config.behavior_type}"}
    except Exception as e:
        logger.error(f"Error starting behavior: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/behavior/stop")
async def stop_behavior():
    """Stop current behavioral pattern"""
    if not behavioral_system:
        raise HTTPException(status_code=503, detail="Behavioral system not initialized")
    
    await behavioral_system.stop_current_behavior()
    return {"success": True, "message": "Stopped current behavior"}

@app.post("/api/chat")
async def send_chat_message(message: ChatMessage):
    """Send a chat message to Claude"""
    if not claude_agent:
        raise HTTPException(status_code=503, detail="Claude agent not initialized")
    
    try:
        response = await claude_agent.process_chat_message(message.message)
        
        # Broadcast chat exchange to all clients
        await manager.broadcast({
            "type": "chat_message",
            "data": {
                "user_message": message.message,
                "claude_response": response,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        })
        
        return {"success": True, "response": response}
    except Exception as e:
        logger.error(f"Error processing chat message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/activities")
async def get_activities(limit: int = 50):
    """Get recent activities"""
    if not activity_logger:
        raise HTTPException(status_code=503, detail="Activity logger not initialized")
    
    return {
        "activities": activity_logger.get_recent_activities(limit),
        "total_count": activity_logger.get_total_count()
    }

@app.get("/api/screenshots")
async def get_screenshots(limit: int = 10):
    """Get recent screenshots"""
    if not screen_service:
        raise HTTPException(status_code=503, detail="Screen service not initialized")
    
    return {
        "screenshots": screen_service.get_recent_screenshots(limit)
    }

# WebSocket endpoint for real-time streaming
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Background tasks
async def screen_streaming_task():
    """Background task for streaming screen captures"""
    if not screen_service:
        return
    
    while True:
        try:
            screenshot = await screen_service.capture_screenshot()
            if screenshot:
                await manager.broadcast({
                    "type": "screenshot",
                    "data": {
                        "image": screenshot["base64_image"],
                        "timestamp": screenshot["timestamp"],
                        "resolution": screenshot["resolution"]
                    }
                })
            await asyncio.sleep(1)  # 1 FPS for live streaming
        except Exception as e:
            logger.error(f"Error in screen streaming: {e}")
            await asyncio.sleep(5)

async def activity_streaming_task():
    """Background task for streaming activities"""
    if not activity_logger:
        return
    
    last_activity_count = 0
    while True:
        try:
            current_count = activity_logger.get_total_count()
            if current_count > last_activity_count:
                new_activities = activity_logger.get_recent_activities(
                    current_count - last_activity_count
                )
                await manager.broadcast({
                    "type": "new_activities",
                    "data": new_activities
                })
                last_activity_count = current_count
            await asyncio.sleep(0.5)
        except Exception as e:
            logger.error(f"Error in activity streaming: {e}")
            await asyncio.sleep(5)

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global claude_agent, screen_service, activity_logger, behavioral_system
    
    logger.info("Starting Claude Live Viewer...")
    
    try:
        # Initialize services
        activity_logger = ActivityLogger()
        screen_service = ScreenCaptureService()
        behavioral_system = BehavioralSystem()
        claude_agent = ClaudeAgent(
            activity_logger=activity_logger,
            screen_service=screen_service,
            behavioral_system=behavioral_system
        )
        
        # Initialize the Claude agent
        await claude_agent.initialize()
        
        # Start background tasks
        asyncio.create_task(screen_streaming_task())
        asyncio.create_task(activity_streaming_task())
        
        # Check if autonomous mode is enabled
        autonomous_mode = os.getenv("CLAUDE_AUTONOMOUS_MODE", "true").lower() == "true"
        if autonomous_mode:
            logger.info("Starting Claude in autonomous mode...")
            # Give services a moment to fully initialize
            await asyncio.sleep(2)
            # Start autonomous exploration
            asyncio.create_task(claude_agent.start_autonomous_exploration())
        
        logger.info("Claude Live Viewer started successfully!")
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Claude Live Viewer...")
    
    if claude_agent:
        await claude_agent.shutdown()
    if screen_service:
        await screen_service.cleanup()
    if behavioral_system:
        await behavioral_system.cleanup()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)