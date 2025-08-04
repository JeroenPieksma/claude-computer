// Type definitions for Claude Live Viewer

export interface Activity {
  id: string;
  timestamp: string;
  activity_type: 'system' | 'user' | 'assistant' | 'tool' | 'screen' | 'behavior';
  action: string;
  data: Record<string, any>;
  duration_ms?: number;
  parent_id?: string;
}

export interface Screenshot {
  id: string;
  timestamp: string;
  filename: string;
  filepath?: string;
  base64_image?: string;
  resolution: {
    width: number;
    height: number;
  };
  size_bytes: number;
}

export interface BehaviorStatus {
  name?: string;
  description?: string;
  status: 'inactive' | 'active' | 'paused' | 'completed' | 'error';
  start_time?: string;
  end_time?: string;
  error_message?: string;
}

export interface SystemStatus {
  connected_clients: number;
  agent_active: boolean;
  current_behavior?: string;
  screen_resolution?: {
    width: number;
    height: number;
  };
  activity_count: number;
}

export interface WebSocketMessage {
  type: 'screenshot' | 'new_activities' | 'chat_message' | 'behavior_update' | 'system_status';
  data: any;
}

export interface ChatMessage {
  id: string;
  message: string;
  sender: 'user' | 'assistant' | 'system';
  timestamp: string;
  claude_response?: string;
}

export interface BehaviorConfig {
  behavior_type: string;
  parameters: Record<string, any>;
  duration_minutes?: number;
}

export interface AgentCommand {
  command: string;
  parameters?: Record<string, any>;
}

export interface ActivityStats {
  total_activities: number;
  activity_types: Record<string, number>;
  actions: Record<string, number>;
  time_range?: {
    start: string;
    end: string;
  };
}

export interface HealthStatus {
  status: 'healthy' | 'degraded' | 'unhealthy';
  timestamp: string;
  services: {
    claude_agent: boolean;
    screen_capture: boolean;
    activity_logger: boolean;
    behavioral_system: boolean;
  };
}

// Component Props Types
export interface ScreenViewerProps {
  screenshot?: Screenshot;
  isLive?: boolean;
  onScreenshotClick?: (screenshot: Screenshot) => void;
}

export interface ActivityTimelineProps {
  activities: Activity[];
  maxItems?: number;
  showFilter?: boolean;
}

export interface ChatInterfaceProps {
  messages: ChatMessage[];
  onSendMessage: (message: string) => void;
  isConnected: boolean;
}

export interface BehaviorControlProps {
  currentBehavior?: BehaviorStatus | null;
  availableBehaviors: string[];
  onStartBehavior: (config: BehaviorConfig) => void;
  onStopBehavior: () => void;
  onPauseBehavior?: () => void;
  onResumeBehavior?: () => void;
}

export interface StatusPanelProps {
  status: SystemStatus | null;
  healthStatus: HealthStatus | null;
  connectionStatus: 'connected' | 'disconnected' | 'connecting';
}

// Utility Types
export type ActivityType = Activity['activity_type'];
export type BehaviorType = 'web_browsing' | 'research' | 'creative' | 'exploration';
export type ViewMode = 'live' | 'timeline' | 'chat' | 'control' | 'dashboard';

// API Response Types
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  has_next: boolean;
  has_prev: boolean;
}

// Hook Types
export interface UseWebSocketOptions {
  url: string;
  onMessage?: (message: WebSocketMessage) => void;
  onConnect?: () => void;
  onDisconnect?: () => void;
  onError?: (error: Event) => void;
  reconnectAttempts?: number;
  reconnectInterval?: number;
}

export interface UseActivitiesOptions {
  limit?: number;
  activityType?: ActivityType;
  autoRefresh?: boolean;
  refreshInterval?: number;
}

export interface UseScreenshotsOptions {
  limit?: number;
  autoRefresh?: boolean;
  refreshInterval?: number;
}