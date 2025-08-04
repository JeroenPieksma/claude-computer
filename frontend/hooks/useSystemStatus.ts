import { useState, useEffect, useCallback } from 'react';
import { SystemStatus, HealthStatus, ApiResponse } from '../types';

interface UseSystemStatusReturn {
  status: SystemStatus | null;
  healthStatus: HealthStatus | null;
  isLoading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export function useSystemStatus(refreshInterval: number = 30000): UseSystemStatusReturn {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [healthStatus, setHealthStatus] = useState<HealthStatus | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStatus = useCallback(async () => {
    try {
      setError(null);
      
      const [statusResponse, healthResponse] = await Promise.all([
        fetch('/api/status'),
        fetch('/api/health')
      ]);

      if (!statusResponse.ok || !healthResponse.ok) {
        throw new Error('Failed to fetch system status');
      }

      const statusData: ApiResponse<SystemStatus> = await statusResponse.json();
      const healthData: ApiResponse<HealthStatus> = await healthResponse.json();

      if (statusData.success && statusData.data) {
        setStatus(statusData.data);
      }

      if (healthData.success && healthData.data) {
        setHealthStatus(healthData.data);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      setError(errorMessage);
      console.error('Error fetching system status:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Initial fetch
  useEffect(() => {
    fetchStatus();
  }, [fetchStatus]);

  // Auto refresh
  useEffect(() => {
    const interval = setInterval(fetchStatus, refreshInterval);
    return () => clearInterval(interval);
  }, [fetchStatus, refreshInterval]);

  return {
    status,
    healthStatus,
    isLoading,
    error,
    refetch: fetchStatus,
  };
}