interface DashboardProps {
  systemStatus: any;
  healthStatus: any;
  activities: any[];
  currentScreenshot: any;
}

export default function Dashboard({ 
  systemStatus, 
  healthStatus, 
  activities, 
  currentScreenshot 
}: DashboardProps) {
  return (
    <div className="flex-1 p-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">System Overview</h2>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Agent Status:</span>
              <span className={systemStatus?.agent_active ? 'text-green-600' : 'text-red-600'}>
                {systemStatus?.agent_active ? 'Active' : 'Inactive'}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Connected Clients:</span>
              <span className="text-gray-900">{systemStatus?.connected_clients || 0}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Total Activities:</span>
              <span className="text-gray-900">{systemStatus?.activity_count || 0}</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h2>
          <div className="space-y-2">
            {activities.slice(-5).map((activity, index) => (
              <div key={activity.id || index} className="text-sm">
                <span className="font-medium text-gray-900">{activity.activity_type}</span>
                <span className="text-gray-600 ml-2">{activity.action}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}