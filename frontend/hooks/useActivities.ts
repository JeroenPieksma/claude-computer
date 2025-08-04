import { useState, useEffect, useCallback } from 'react';
import { Activity, UseActivitiesOptions, ApiResponse } from '../types';

interface UseActivitiesReturn {
  activities: Activity[];
  isLoading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
  addActivity: (activity: Activity) => void;
}

export function useActivities({
  limit = 50,
  activityType,
  autoRefresh = false,
  refreshInterval = 10000,
}: UseActivitiesOptions = {}): UseActivitiesReturn {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchActivities = useCallback(async () => {
    try {
      setError(null);
      
      const params = new URLSearchParams({
        limit: limit.toString(),
      });
      
      if (activityType) {
        params.append('type', activityType);
      }

      const response = await fetch(`/api/activities?${params}`);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch activities: ${response.statusText}`);
      }

      const data: ApiResponse<{ activities: Activity[] }> = await response.json();
      
      if (data.success && data.data) {
        setActivities(data.data.activities);
      } else {
        throw new Error(data.error || 'Failed to fetch activities');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      setError(errorMessage);
      console.error('Error fetching activities:', err);
    } finally {
      setIsLoading(false);
    }
  }, [limit, activityType]);

  const addActivity = useCallback((activity: Activity) => {
    setActivities(prev => {
      const updated = [...prev, activity];
      // Keep only the most recent items based on limit
      return updated.slice(-limit);
    });
  }, [limit]);

  // Initial fetch
  useEffect(() => {
    fetchActivities();
  }, [fetchActivities]);

  // Auto refresh
  useEffect(() => {
    if (!autoRefresh) return;

    const interval = setInterval(fetchActivities, refreshInterval);
    return () => clearInterval(interval);
  }, [autoRefresh, refreshInterval, fetchActivities]);

  return {
    activities,
    isLoading,
    error,
    refetch: fetchActivities,
    addActivity,
  };
}