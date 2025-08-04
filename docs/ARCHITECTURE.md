# Claude Live Viewer Architecture

## Overview

Claude Live Viewer is a web application that provides real-time monitoring of Claude's autonomous computer interactions. Built on top of Anthropic's computer-use-demo, it adds streaming capabilities, behavioral frameworks, and a modern web interface.

## System Components

### 1. Backend Server (`/backend`)
- **FastAPI** application with WebSocket support
- Real-time screenshot streaming
- Activity logging and analytics  
- RESTful API for frontend communication
- Integration with Anthropic's computer-use tools

### 2. Frontend Interface (`/frontend`)
- **Next.js** React application with TypeScript
- Real-time WebSocket connections
- Multiple view modes (Live, Timeline, Chat, Control, Dashboard)
- Responsive design with Tailwind CSS

### 3. VM Environment (`/docker-environment`)
- Extended Docker container based on computer-use-demo
- Ubuntu desktop environment with VNC access
- Enhanced with live streaming capabilities
- Redis for session management

### 4. Behavioral System
- Autonomous behavior patterns for Claude
- Configurable objectives and tasks
- Web browsing, research, creative, and exploration modes
- Safety controls and monitoring

## Data Flow

```
[Claude Agent] → [Computer Use Tools] → [Screen Capture] → [WebSocket] → [Frontend]
      ↓                    ↓                   ↓
[Activity Logger] → [Backend API] → [Database] → [Analytics Dashboard]
```

## Key Features

### Real-time Streaming
- Screenshot capture at configurable FPS
- WebSocket-based live updates
- Activity timeline with filtering
- Connection status monitoring

### Behavioral Framework
- Pre-configured behavior patterns
- Custom objective setting
- Safety controls and intervention
- Activity logging and replay

### Multi-modal Interface
- Live desktop view with zoom/fullscreen
- Activity timeline with search/filter
- Chat interface for direct interaction
- Behavior control panel
- System dashboard with metrics

## Security Considerations

- VM isolation for safe computer use
- API key management and rotation
- Activity monitoring and alerting
- User oversight and intervention capabilities
- Rate limiting and resource management

## Extensibility

The architecture supports:
- Custom behavior implementations
- Additional tool integrations  
- Third-party service connections
- Advanced analytics and reporting
- Multi-agent coordination

## Technology Stack

**Backend:**
- FastAPI (Python)
- WebSockets
- Anthropic SDK
- Computer-use-demo tools

**Frontend:**
- Next.js (React/TypeScript)
- Tailwind CSS
- Framer Motion
- Socket.io-client

**Infrastructure:**
- Docker containers
- Ubuntu desktop environment
- VNC for remote access
- Redis for caching