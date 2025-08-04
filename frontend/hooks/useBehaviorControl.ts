import { useState, useEffect, useCallback } from 'react';
import { BehaviorStatus, BehaviorConfig, ApiResponse } from '../types';

interface UseBehaviorControlReturn {
  currentBehavior: BehaviorStatus | null;
  availableBehaviors: string[];
  isLoading: boolean;
  error: string | null;
  startBehavior: (config: BehaviorConfig) => Promise<void>;
  stopBehavior: () => Promise<void>;
  pauseBehavior: () => Promise<void>;
  resumeBehavior: () => Promise<void>;
}

export function useBehaviorControl(): UseBehaviorControlReturn {
  const [currentBehavior, setCurrentBehavior] = useState<BehaviorStatus | null>(null);
  const [availableBehaviors] = useState<string[]>(['web_browsing', 'research', 'creative', 'exploration']);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const startBehavior = useCallback(async (config: BehaviorConfig) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/behavior/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config),
      });

      const data: ApiResponse = await response.json();
      
      if (!data.success) {
        throw new Error(data.error || 'Failed to start behavior');
      }

      // Set mock current behavior
      setCurrentBehavior({
        name: config.behavior_type,
        description: `Running ${config.behavior_type} behavior`,
        status: 'active',
        start_time: new Date().toISOString(),
      });
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const stopBehavior = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/behavior/stop', {
        method: 'POST',
      });

      const data: ApiResponse = await response.json();
      
      if (!data.success) {
        throw new Error(data.error || 'Failed to stop behavior');
      }

      setCurrentBehavior(null);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const pauseBehavior = useCallback(async () => {
    // Implementation would go here
  }, []);

  const resumeBehavior = useCallback(async () => {
    // Implementation would go here
  }, []);

  return {
    currentBehavior,
    availableBehaviors,
    isLoading,
    error,
    startBehavior,
    stopBehavior,
    pauseBehavior,
    resumeBehavior,
  };
}