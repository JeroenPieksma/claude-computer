import { useState, useEffect } from 'react';
import Head from 'next/head';
import { motion } from 'framer-motion';
import { 
  ComputerDesktopIcon,
  ChatBubbleLeftRightIcon,
  ClockIcon,
  Cog6ToothIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';

import Layout from '../components/Layout';
import ScreenViewer from '../components/ScreenViewer';
import ActivityTimeline from '../components/ActivityTimeline';
import ChatInterface from '../components/ChatInterface';
import BehaviorControl from '../components/BehaviorControl';
import StatusPanel from '../components/StatusPanel';
import Dashboard from '../components/Dashboard';

import { useWebSocket } from '../hooks/useWebSocket';
import { useActivities } from '../hooks/useActivities';
import { useSystemStatus } from '../hooks/useSystemStatus';
import { useBehaviorControl } from '../hooks/useBehaviorControl';
import { useChat } from '../hooks/useChat';

import { ViewMode, Screenshot, WebSocketMessage } from '../types';

const viewModes: { key: ViewMode; label: string; icon: any }[] = [
  { key: 'live', label: 'Live View', icon: ComputerDesktopIcon },
  { key: 'timeline', label: 'Activity Timeline', icon: ClockIcon },
  { key: 'chat', label: 'Chat', icon: ChatBubbleLeftRightIcon },
  { key: 'control', label: 'Behavior Control', icon: Cog6ToothIcon },
  { key: 'dashboard', label: 'Dashboard', icon: ChartBarIcon },
];

export default function Home() {
  const [currentView, setCurrentView] = useState<ViewMode>('live');
  const [currentScreenshot, setCurrentScreenshot] = useState<Screenshot | null>(null);

  // Custom hooks
  const { 
    isConnected, 
    connectionStatus, 
    sendMessage,
    lastMessage 
  } = useWebSocket({
    url: process.env.NODE_ENV === 'production' 
      ? 'wss://your-domain.com/ws' 
      : 'ws://localhost:8000/ws',
  });

  const { activities, isLoading: activitiesLoading } = useActivities({
    limit: 50,
    autoRefresh: true,
  });

  const { status: systemStatus, healthStatus } = useSystemStatus();

  const {
    currentBehavior,
    availableBehaviors,
    startBehavior,
    stopBehavior,
    pauseBehavior,
    resumeBehavior,
  } = useBehaviorControl();

  const {
    messages: chatMessages,
    sendMessage: sendChatMessage,
    isLoading: chatLoading,
  } = useChat();

  // Handle WebSocket messages
  useEffect(() => {
    if (!lastMessage) return;

    try {
      const message: WebSocketMessage = JSON.parse(lastMessage.data);
      
      switch (message.type) {
        case 'screenshot':
          setCurrentScreenshot(message.data);
          break;
        case 'new_activities':
          // Activities are handled by the useActivities hook
          break;
        case 'chat_message':
          // Chat messages are handled by the useChat hook
          break;
        case 'behavior_update':
          // Behavior updates are handled by the useBehaviorControl hook
          break;
        default:
          console.log('Unknown message type:', message.type);
      }
    } catch (error) {
      console.error('Error parsing WebSocket message:', error);
    }
  }, [lastMessage]);

  const renderCurrentView = () => {
    switch (currentView) {
      case 'live':
        return (
          <ScreenViewer 
            screenshot={currentScreenshot}
            isLive={isConnected}
          />
        );
      
      case 'timeline':
        return (
          <ActivityTimeline 
            activities={activities}
            showFilter={true}
          />
        );
      
      case 'chat':
        return (
          <ChatInterface
            messages={chatMessages}
            onSendMessage={sendChatMessage}
            isConnected={isConnected}
          />
        );
      
      case 'control':
        return (
          <BehaviorControl
            currentBehavior={currentBehavior}
            availableBehaviors={availableBehaviors}
            onStartBehavior={startBehavior}
            onStopBehavior={stopBehavior}
            onPauseBehavior={pauseBehavior}
            onResumeBehavior={resumeBehavior}
          />
        );
      
      case 'dashboard':
        return (
          <Dashboard
            systemStatus={systemStatus}
            healthStatus={healthStatus}
            activities={activities}
            currentScreenshot={currentScreenshot}
          />
        );
      
      default:
        return <div>Unknown view mode</div>;
    }
  };

  return (
    <>
      <Head>
        <title>Claude Live Viewer</title>
        <meta name="description" content="Real-time view into Claude's computer interactions" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Layout>
        {/* Header */}
        <div className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Claude Live Viewer
              </h1>
              <p className="text-sm text-gray-600 mt-1">
                Real-time monitoring of Claude's autonomous computer interactions
              </p>
            </div>
            
            <StatusPanel 
              status={systemStatus}
              healthStatus={healthStatus}
              connectionStatus={connectionStatus}
            />
          </div>
        </div>

        {/* Navigation */}
        <div className="bg-gray-50 border-b border-gray-200">
          <nav className="px-6">
            <div className="flex space-x-8">
              {viewModes.map((mode) => {
                const Icon = mode.icon;
                const isActive = currentView === mode.key;
                
                return (
                  <button
                    key={mode.key}
                    onClick={() => setCurrentView(mode.key)}
                    className={`
                      flex items-center px-3 py-4 text-sm font-medium border-b-2 transition-colors duration-200
                      ${isActive 
                        ? 'border-claude-500 text-claude-600' 
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                      }
                    `}
                  >
                    <Icon className="w-5 h-5 mr-2" />
                    {mode.label}
                  </button>
                );
              })}
            </div>
          </nav>
        </div>

        {/* Main Content */}
        <div className="flex-1 overflow-hidden">
          <motion.div
            key={currentView}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="h-full"
          >
            {renderCurrentView()}
          </motion.div>
        </div>

        {/* Connection Status Indicator */}
        <div className="fixed bottom-4 right-4">
          <div className={`
            px-3 py-2 rounded-full text-xs font-medium flex items-center shadow-lg
            ${isConnected 
              ? 'bg-green-100 text-green-800 border border-green-200' 
              : 'bg-red-100 text-red-800 border border-red-200'
            }
          `}>
            <div className={`
              w-2 h-2 rounded-full mr-2
              ${isConnected ? 'bg-green-500' : 'bg-red-500'}
            `} />
            {isConnected ? 'Connected' : 'Disconnected'}
          </div>
        </div>
      </Layout>
    </>
  );
}