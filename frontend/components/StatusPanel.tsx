import { StatusPanelProps } from '../types';

export default function StatusPanel({ 
  status, 
  healthStatus, 
  connectionStatus 
}: StatusPanelProps) {
  const getConnectionStatusColor = () => {
    switch (connectionStatus) {
      case 'connected': return 'text-green-600';
      case 'connecting': return 'text-yellow-600';
      default: return 'text-red-600';
    }
  };

  return (
    <div className="flex items-center space-x-4 text-sm">
      <div className={`flex items-center ${getConnectionStatusColor()}`}>
        <div className={`w-2 h-2 rounded-full mr-2 ${
          connectionStatus === 'connected' ? 'bg-green-500' : 
          connectionStatus === 'connecting' ? 'bg-yellow-500' : 'bg-red-500'
        }`} />
        {connectionStatus}
      </div>
      
      {status && (
        <div className="text-gray-600">
          {status.connected_clients} clients • {status.activity_count} activities
        </div>
      )}
    </div>
  );
}