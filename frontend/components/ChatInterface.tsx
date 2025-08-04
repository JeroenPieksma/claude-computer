import { ChatInterfaceProps } from '../types';

export default function ChatInterface({ 
  messages, 
  onSendMessage, 
  isConnected 
}: ChatInterfaceProps) {
  return (
    <div className="flex-1 flex flex-col p-6">
      <div className="bg-white rounded-lg border border-gray-200 shadow-sm flex-1 flex flex-col">
        <div className="p-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Chat with Claude</h2>
          <p className="text-sm text-gray-600">Send messages to interact with Claude</p>
        </div>
        
        <div className="flex-1 flex items-center justify-center text-gray-500">
          Chat interface coming soon...
        </div>
      </div>
    </div>
  );
}