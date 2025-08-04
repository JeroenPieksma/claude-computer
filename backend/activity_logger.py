"""
Activity logging service for tracking Claude's actions
"""

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)

class ActivityType(Enum):
    """Types of activities that can be logged"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
    SCREEN = "screen"
    BEHAVIOR = "behavior"

class ActivityAction(Enum):
    """Specific actions within activity types"""
    # System actions
    AGENT_INITIALIZED = "agent_initialized"
    AGENT_SHUTDOWN = "agent_shutdown"
    ERROR = "error"
    
    # User actions
    COMMAND_SENT = "command_sent"
    CHAT_MESSAGE = "chat_message"
    BEHAVIOR_START = "behavior_start"
    BEHAVIOR_STOP = "behavior_stop"
    
    # Assistant actions
    CHAT_RESPONSE = "chat_response"
    OUTPUT_BLOCK = "output_block"
    THINKING = "thinking"
    
    # Tool actions
    TOOL_EXECUTION = "tool_execution"
    SCREENSHOT_TAKEN = "screenshot_taken"
    MOUSE_CLICK = "mouse_click"
    KEYBOARD_INPUT = "keyboard_input"
    
    # Screen actions
    SCREEN_CHANGE = "screen_change"
    WINDOW_FOCUS = "window_focus"
    
    # Behavior actions
    AUTONOMOUS_ACTION = "autonomous_action"
    OBJECTIVE_SET = "objective_set"

@dataclass
class Activity:
    """Represents a single logged activity"""
    id: str
    timestamp: str
    activity_type: str
    action: str
    data: Dict[str, Any]
    duration_ms: Optional[int] = None
    parent_id: Optional[str] = None

class ActivityLogger:
    """Service for logging and tracking Claude's activities"""
    
    def __init__(self, max_activities: int = 10000):
        self.activities: List[Activity] = []
        self.max_activities = max_activities
        self.activity_counter = 0
        
        # Callbacks for real-time activity streaming
        self.callbacks: List = []
        
        logger.info("Activity logger initialized")
    
    async def log_activity(
        self, 
        activity_type: str, 
        action: str, 
        data: Dict[str, Any],
        duration_ms: Optional[int] = None,
        parent_id: Optional[str] = None
    ) -> str:
        """Log a new activity"""
        self.activity_counter += 1
        activity_id = f"activity_{self.activity_counter}"
        
        activity = Activity(
            id=activity_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            activity_type=activity_type,
            action=action,
            data=data,
            duration_ms=duration_ms,
            parent_id=parent_id
        )
        
        self.activities.append(activity)
        
        # Maintain max activities limit
        if len(self.activities) > self.max_activities:
            self.activities.pop(0)
        
        # Notify callbacks
        await self._notify_callbacks(activity)
        
        logger.debug(f"Logged activity: {activity_type}.{action}")
        return activity_id
    
    def get_recent_activities(self, limit: int = 50) -> List[Dict]:
        """Get recent activities as dictionaries"""
        recent = self.activities[-limit:] if limit > 0 else self.activities
        return [asdict(activity) for activity in recent]
    
    def get_activities_by_type(self, activity_type: str, limit: int = 50) -> List[Dict]:
        """Get activities filtered by type"""
        filtered = [
            activity for activity in self.activities
            if activity.activity_type == activity_type
        ]
        recent = filtered[-limit:] if limit > 0 else filtered
        return [asdict(activity) for activity in recent]
    
    def get_activities_by_action(self, action: str, limit: int = 50) -> List[Dict]:
        """Get activities filtered by action"""
        filtered = [
            activity for activity in self.activities
            if activity.action == action
        ]
        recent = filtered[-limit:] if limit > 0 else filtered
        return [asdict(activity) for activity in recent]
    
    def get_activity_by_id(self, activity_id: str) -> Optional[Dict]:
        """Get a specific activity by ID"""
        for activity in self.activities:
            if activity.id == activity_id:
                return asdict(activity)
        return None
    
    def get_total_count(self) -> int:
        """Get total number of activities logged"""
        return len(self.activities)
    
    def get_activity_statistics(self) -> Dict[str, Any]:
        """Get statistics about logged activities"""
        if not self.activities:
            return {
                "total_activities": 0,
                "activity_types": {},
                "actions": {},
                "time_range": None
            }
        
        # Count by type
        type_counts = {}
        action_counts = {}
        
        for activity in self.activities:
            type_counts[activity.activity_type] = type_counts.get(activity.activity_type, 0) + 1
            action_counts[activity.action] = action_counts.get(activity.action, 0) + 1
        
        return {
            "total_activities": len(self.activities),
            "activity_types": type_counts,
            "actions": action_counts,
            "time_range": {
                "start": self.activities[0].timestamp,
                "end": self.activities[-1].timestamp
            }
        }
    
    def search_activities(
        self, 
        query: str, 
        activity_type: Optional[str] = None,
        action: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict]:
        """Search activities by text query in data"""
        query_lower = query.lower()
        results = []
        
        for activity in self.activities:
            # Filter by type and action if specified
            if activity_type and activity.activity_type != activity_type:
                continue
            if action and activity.action != action:
                continue
            
            # Search in data
            data_str = json.dumps(activity.data).lower()
            if query_lower in data_str:
                results.append(activity)
        
        # Return most recent matches
        recent_results = results[-limit:] if limit > 0 else results
        return [asdict(activity) for activity in recent_results]
    
    def add_callback(self, callback):
        """Add callback for real-time activity notifications"""
        self.callbacks.append(callback)
    
    def remove_callback(self, callback):
        """Remove callback"""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
    
    async def _notify_callbacks(self, activity: Activity):
        """Notify all callbacks of new activity"""
        if not self.callbacks:
            return
        
        activity_dict = asdict(activity)
        
        for callback in self.callbacks[:]:  # Copy to avoid modification during iteration
            try:
                await callback(activity_dict)
            except Exception as e:
                logger.error(f"Error in activity callback: {e}")
    
    def export_activities(
        self, 
        format: str = "json",
        activity_type: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> str:
        """Export activities in specified format"""
        # Filter activities
        filtered_activities = self.activities
        
        if activity_type:
            filtered_activities = [
                a for a in filtered_activities 
                if a.activity_type == activity_type
            ]
        
        if start_time:
            filtered_activities = [
                a for a in filtered_activities 
                if a.timestamp >= start_time
            ]
        
        if end_time:
            filtered_activities = [
                a for a in filtered_activities 
                if a.timestamp <= end_time
            ]
        
        # Convert to dictionaries
        activity_dicts = [asdict(activity) for activity in filtered_activities]
        
        if format.lower() == "json":
            return json.dumps(activity_dicts, indent=2)
        elif format.lower() == "csv":
            # Basic CSV export
            if not activity_dicts:
                return ""
            
            import csv
            import io
            
            output = io.StringIO()
            fieldnames = activity_dicts[0].keys()
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            
            for activity in activity_dicts:
                # Convert complex data to JSON string for CSV
                row = activity.copy()
                row['data'] = json.dumps(row['data'])
                writer.writerow(row)
            
            return output.getvalue()
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def clear_activities(self):
        """Clear all logged activities"""
        self.activities.clear()
        self.activity_counter = 0
        logger.info("All activities cleared")


class ActivityAnalyzer:
    """Analyzer for activity patterns and insights"""
    
    def __init__(self, activity_logger: ActivityLogger):
        self.activity_logger = activity_logger
    
    def get_activity_timeline(self, hours: int = 24) -> List[Dict]:
        """Get activity timeline for specified hours"""
        from datetime import timedelta
        
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        cutoff_str = cutoff_time.isoformat()
        
        recent_activities = [
            activity for activity in self.activity_logger.activities
            if activity.timestamp >= cutoff_str
        ]
        
        return [asdict(activity) for activity in recent_activities]
    
    def get_tool_usage_stats(self) -> Dict[str, int]:
        """Get statistics on tool usage"""
        tool_stats = {}
        
        for activity in self.activity_logger.activities:
            if activity.activity_type == "tool":
                tool_name = activity.data.get("tool_name", "unknown")
                tool_stats[tool_name] = tool_stats.get(tool_name, 0) + 1
        
        return tool_stats
    
    def get_error_summary(self) -> List[Dict]:
        """Get summary of errors"""
        errors = []
        
        for activity in self.activity_logger.activities:
            if activity.action == "error" or activity.data.get("error"):
                errors.append({
                    "timestamp": activity.timestamp,
                    "type": activity.activity_type,
                    "error": activity.data.get("error", "Unknown error"),
                    "context": activity.data
                })
        
        return errors
    
    def get_behavior_analysis(self) -> Dict[str, Any]:
        """Analyze behavioral patterns"""
        behavior_activities = self.activity_logger.get_activities_by_type("behavior")
        
        if not behavior_activities:
            return {"active_behaviors": [], "completed_behaviors": [], "total_time": 0}
        
        # Analyze behavior patterns
        behaviors = {}
        for activity in behavior_activities:
            behavior_type = activity["data"].get("behavior_type", "unknown")
            if behavior_type not in behaviors:
                behaviors[behavior_type] = {
                    "count": 0,
                    "total_duration": 0,
                    "sessions": []
                }
            
            behaviors[behavior_type]["count"] += 1
            duration = activity.get("duration_ms", 0)
            behaviors[behavior_type]["total_duration"] += duration
            behaviors[behavior_type]["sessions"].append({
                "timestamp": activity["timestamp"],
                "duration_ms": duration
            })
        
        return {
            "behaviors": behaviors,
            "total_behavior_sessions": len(behavior_activities)
        }