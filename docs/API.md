# Claude Live Viewer API Documentation

## Base URL
```
http://localhost:8000/api
```

## WebSocket Endpoint
```
ws://localhost:8000/ws
```

## REST API Endpoints

### Health & Status

#### `GET /health`
Get system health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "services": {
    "claude_agent": true,
    "screen_capture": true,
    "activity_logger": true,
    "behavioral_system": true
  }
}
```

#### `GET /status`
Get current system status.

**Response:**
```json
{
  "connected_clients": 2,
  "agent_active": true,
  "current_behavior": "web_browsing",
  "screen_resolution": {"width": 1024, "height": 768},
  "activity_count": 150
}
```

### Agent Control

#### `POST /agent/command`
Send a command to Claude agent.

**Request:**
```json
{
  "command": "Take a screenshot of the current screen",
  "parameters": {}
}
```

**Response:**
```json
{
  "success": true,
  "result": "Screenshot taken successfully"
}
```

### Behavior Control

#### `POST /behavior/start`
Start a behavioral pattern.

**Request:**
```json
{
  "behavior_type": "web_browsing",
  "parameters": {
    "sites": ["https://example.com"],
    "duration_minutes": 30
  },
  "duration_minutes": 30
}
```

**Response:**
```json
{
  "success": true,
  "message": "Started behavior: web_browsing"
}
```

#### `POST /behavior/stop`
Stop current behavioral pattern.

**Response:**
```json
{
  "success": true,
  "message": "Stopped current behavior"
}
```

### Chat Interface

#### `POST /chat`
Send a chat message to Claude.

**Request:**
```json
{
  "message": "Hello Claude, how are you?",
  "sender": "user"
}
```

**Response:**
```json
{
  "success": true,
  "response": "Hello! I'm doing well, thank you for asking."
}
```

### Activity Logging

#### `GET /activities`
Get recent activities.

**Query Parameters:**
- `limit` (int): Maximum number of activities (default: 50)
- `type` (string): Filter by activity type
- `action` (string): Filter by action

**Response:**
```json
{
  "activities": [
    {
      "id": "activity_1",
      "timestamp": "2024-01-01T12:00:00Z",
      "activity_type": "tool",
      "action": "screenshot_taken",
      "data": {"filename": "screenshot_123.png"},
      "duration_ms": 500
    }
  ],
  "total_count": 150
}
```

### Screenshots

#### `GET /screenshots`
Get recent screenshots.

**Query Parameters:**
- `limit` (int): Maximum number of screenshots (default: 10)

**Response:**
```json
{
  "screenshots": [
    {
      "id": "screenshot_1",
      "timestamp": "2024-01-01T12:00:00Z",
      "filename": "screenshot_123.png",
      "resolution": {"width": 1024, "height": 768},
      "size_bytes": 45678
    }
  ]
}
```

## WebSocket Messages

### Message Format
```json
{
  "type": "message_type",
  "data": {}
}
```

### Message Types

#### `screenshot`
Real-time screenshot update.

```json
{
  "type": "screenshot",
  "data": {
    "image": "base64_encoded_png",
    "timestamp": "2024-01-01T12:00:00Z",
    "resolution": {"width": 1024, "height": 768}
  }
}
```

#### `new_activities`
New activity notifications.

```json
{
  "type": "new_activities",
  "data": [
    {
      "id": "activity_1",
      "timestamp": "2024-01-01T12:00:00Z",
      "activity_type": "tool",
      "action": "mouse_click",
      "data": {"coordinate": [100, 200]}
    }
  ]
}
```

#### `chat_message`
Chat message exchange.

```json
{
  "type": "chat_message",
  "data": {
    "user_message": "Hello",
    "claude_response": "Hi there!",
    "timestamp": "2024-01-01T12:00:00Z"
  }
}
```

#### `behavior_update`
Behavior status change.

```json
{
  "type": "behavior_update",
  "data": {
    "behavior": "web_browsing",
    "status": "active",
    "start_time": "2024-01-01T12:00:00Z"
  }
}
```

## Error Responses

All endpoints return errors in this format:

```json
{
  "success": false,
  "error": "Error message description",
  "details": "Additional error details if available"
}
```

## Status Codes

- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized  
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error
- `503` - Service Unavailable