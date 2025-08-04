import { BehaviorControlProps } from '../types';

export default function BehaviorControl({
  currentBehavior,
  availableBehaviors,
  onStartBehavior,
  onStopBehavior
}: BehaviorControlProps) {
  return (
    <div className="flex-1 p-6">
      <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Behavior Control</h2>
        <p className="text-gray-600 mb-6">Configure Claude's autonomous behavior patterns</p>
        
        <div className="space-y-4">
          {currentBehavior ? (
            <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-medium text-green-900">Active: {currentBehavior.name}</h3>
                  <p className="text-sm text-green-700">{currentBehavior.description}</p>
                  <p className="text-xs text-green-600 mt-1">Status: {currentBehavior.status}</p>
                </div>
                <button
                  onClick={onStopBehavior}
                  className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                >
                  Stop
                </button>
              </div>
            </div>
          ) : (
            <div className="text-center py-8">
              <p className="text-gray-500 mb-4">No active behavior</p>
              <div className="grid grid-cols-2 gap-4">
                {availableBehaviors.map((behavior) => (
                  <button
                    key={behavior}
                    onClick={() => onStartBehavior({ 
                      behavior_type: behavior, 
                      parameters: {},
                      duration_minutes: 30
                    })}
                    className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    <h3 className="font-medium text-gray-900 capitalize">{behavior}</h3>
                    <p className="text-sm text-gray-600 mt-1">Start {behavior} behavior</p>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}