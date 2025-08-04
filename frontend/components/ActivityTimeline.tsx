import { useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { formatDistanceToNow } from 'date-fns';
import {
  UserIcon,
  ComputerDesktopIcon,
  ChatBubbleLeftIcon,
  WrenchScrewdriverIcon,
  CpuChipIcon,
  EyeIcon,
  FunnelIcon,
} from '@heroicons/react/24/outline';

import { Activity, ActivityType } from '../types';

interface ActivityTimelineProps {
  activities: Activity[];
  maxItems?: number;
  showFilter?: boolean;
}

const activityIcons: Record<ActivityType, any> = {
  user: UserIcon,
  assistant: ChatBubbleLeftIcon,
  tool: WrenchScrewdriverIcon,
  system: CpuChipIcon,
  screen: EyeIcon,
  behavior: ComputerDesktopIcon,
};

const activityColors: Record<ActivityType, string> = {
  user: 'bg-blue-500',
  assistant: 'bg-claude-500',
  tool: 'bg-green-500',
  system: 'bg-gray-500',
  screen: 'bg-purple-500',
  behavior: 'bg-orange-500',
};

export default function ActivityTimeline({ 
  activities, 
  maxItems = 50,
  showFilter = false 
}: ActivityTimelineProps) {
  const [selectedTypes, setSelectedTypes] = useState<Set<ActivityType>>(new Set());
  const [searchQuery, setSearchQuery] = useState('');
  const [isFilterOpen, setIsFilterOpen] = useState(false);

  // Filter and limit activities
  const filteredActivities = useMemo(() => {
    let filtered = activities;

    // Filter by type
    if (selectedTypes.size > 0) {
      filtered = filtered.filter(activity => 
        selectedTypes.has(activity.activity_type)
      );
    }

    // Filter by search query
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(activity =>
        activity.action.toLowerCase().includes(query) ||
        JSON.stringify(activity.data).toLowerCase().includes(query)
      );
    }

    // Limit results
    return filtered.slice(-maxItems);
  }, [activities, selectedTypes, searchQuery, maxItems]);

  const toggleTypeFilter = (type: ActivityType) => {
    const newTypes = new Set(selectedTypes);
    if (newTypes.has(type)) {
      newTypes.delete(type);
    } else {
      newTypes.add(type);
    }
    setSelectedTypes(newTypes);
  };

  const clearFilters = () => {
    setSelectedTypes(new Set());
    setSearchQuery('');
  };

  const formatActivityData = (data: Record<string, any>) => {
    const keys = Object.keys(data);
    if (keys.length === 0) return null;

    // Show first few key-value pairs
    const preview = keys.slice(0, 3).map(key => {
      let value = data[key];
      if (typeof value === 'string' && value.length > 50) {
        value = value.substring(0, 50) + '...';
      } else if (typeof value === 'object') {
        value = JSON.stringify(value).substring(0, 50) + '...';
      }
      return `${key}: ${value}`;
    }).join(', ');

    return preview;
  };

  const getActivityTypeCount = (type: ActivityType) => {
    return activities.filter(a => a.activity_type === type).length;
  };

  if (activities.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mx-auto mb-4">
            <ComputerDesktopIcon className="w-8 h-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            No Activities Yet
          </h3>
          <p className="text-gray-600">
            Activities will appear here as Claude interacts with the computer.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col">
      {/* Header with filters */}
      {showFilter && (
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">
              Activity Timeline ({filteredActivities.length})
            </h2>
            
            <button
              onClick={() => setIsFilterOpen(!isFilterOpen)}
              className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <FunnelIcon className="w-4 h-4 mr-2" />
              Filters
            </button>
          </div>

          {isFilterOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="space-y-4"
            >
              {/* Search */}
              <div>
                <input
                  type="text"
                  placeholder="Search activities..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-claude-500 focus:border-transparent"
                />
              </div>

              {/* Type filters */}
              <div>
                <label className="text-sm font-medium text-gray-700 mb-2 block">
                  Activity Types
                </label>
                <div className="flex flex-wrap gap-2">
                  {Object.keys(activityIcons).map((type) => {
                    const activityType = type as ActivityType;
                    const Icon = activityIcons[activityType];
                    const isSelected = selectedTypes.has(activityType);
                    const count = getActivityTypeCount(activityType);

                    return (
                      <button
                        key={type}
                        onClick={() => toggleTypeFilter(activityType)}
                        className={`
                          flex items-center px-3 py-1 rounded-full text-sm font-medium transition-colors
                          ${isSelected
                            ? `${activityColors[activityType]} text-white`
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                          }
                        `}
                      >
                        <Icon className="w-4 h-4 mr-1" />
                        {type} ({count})
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Clear filters */}
              {(selectedTypes.size > 0 || searchQuery) && (
                <div>
                  <button
                    onClick={clearFilters}
                    className="text-sm text-claude-600 hover:text-claude-700 font-medium"
                  >
                    Clear all filters
                  </button>
                </div>
              )}
            </motion.div>
          )}
        </div>
      )}

      {/* Timeline */}
      <div className="flex-1 overflow-y-auto custom-scrollbar">
        {filteredActivities.length === 0 ? (
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <p className="text-gray-600">No activities match your filters.</p>
              <button
                onClick={clearFilters}
                className="mt-2 text-claude-600 hover:text-claude-700 font-medium"
              >
                Clear filters
              </button>
            </div>
          </div>
        ) : (
          <div className="activity-timeline p-6">
            {filteredActivities.map((activity, index) => {
              const Icon = activityIcons[activity.activity_type];
              const colorClass = activityColors[activity.activity_type];
              const dataPreview = formatActivityData(activity.data);

              return (
                <motion.div
                  key={activity.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className="activity-item"
                >
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
                    <div className="flex items-start">
                      <div className={`
                        p-2 rounded-lg ${colorClass.replace('bg-', 'bg-').replace('-500', '-100')} mr-4 flex-shrink-0
                      `}>
                        <Icon className={`w-5 h-5 ${colorClass.replace('bg-', 'text-')}`} />
                      </div>
                      
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between mb-2">
                          <div>
                            <span className="text-sm font-medium text-gray-900">
                              {activity.activity_type}
                            </span>
                            <span className="mx-2 text-gray-300">•</span>
                            <span className="text-sm text-gray-600">
                              {activity.action}
                            </span>
                          </div>
                          
                          <time className="text-xs text-gray-500">
                            {formatDistanceToNow(new Date(activity.timestamp), { addSuffix: true })}
                          </time>
                        </div>
                        
                        {dataPreview && (
                          <div className="text-sm text-gray-600 mb-2">
                            {dataPreview}
                          </div>
                        )}
                        
                        {activity.duration_ms && (
                          <div className="text-xs text-gray-500">
                            Duration: {activity.duration_ms}ms
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}