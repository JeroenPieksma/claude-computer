import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  MagnifyingGlassIcon,
  ArrowsPointingOutIcon,
  ArrowDownTrayIcon
} from '@heroicons/react/24/outline';
import { Screenshot } from '../types';

interface ScreenViewerProps {
  screenshot?: Screenshot | null;
  isLive?: boolean;
  onScreenshotClick?: (screenshot: Screenshot) => void;
}

export default function ScreenViewer({ 
  screenshot, 
  isLive = false,
  onScreenshotClick 
}: ScreenViewerProps) {
  const [isZoomed, setIsZoomed] = useState(false);
  const [lastUpdate, setLastUpdate] = useState<string>('');

  useEffect(() => {
    if (screenshot) {
      setLastUpdate(new Date(screenshot.timestamp).toLocaleTimeString());
    }
  }, [screenshot]);

  const handleDownload = () => {
    if (!screenshot?.base64_image) return;

    const link = document.createElement('a');
    link.href = `data:image/png;base64,${screenshot.base64_image}`;
    link.download = `claude-screenshot-${screenshot.id}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleFullscreen = () => {
    setIsZoomed(!isZoomed);
  };

  if (!screenshot) {
    return (
      <div className="flex-1 flex items-center justify-center bg-gray-100">
        <div className="text-center">
          <div className="animate-pulse">
            <div className="w-16 h-16 bg-gray-300 rounded-lg mx-auto mb-4"></div>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Waiting for Claude's screen...
          </h3>
          <p className="text-gray-600">
            {isLive ? 'Connecting to live stream...' : 'No screenshot available'}
          </p>
          {isLive && (
            <div className="mt-4">
              <div className="loading-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <>
      <div className="flex-1 flex flex-col bg-gray-100">
        {/* Controls Header */}
        <div className="bg-white border-b border-gray-200 px-6 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center">
                <div className={`
                  w-2 h-2 rounded-full mr-2
                  ${isLive ? 'bg-green-500 animate-pulse' : 'bg-gray-400'}
                `} />
                <span className="text-sm font-medium text-gray-900">
                  {isLive ? 'Live Stream' : 'Static View'}
                </span>
              </div>
              
              {lastUpdate && (
                <div className="text-sm text-gray-600">
                  Last updated: {lastUpdate}
                </div>
              )}
              
              <div className="text-sm text-gray-600">
                {screenshot.resolution.width} × {screenshot.resolution.height}
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <button
                onClick={handleFullscreen}
                className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100 transition-colors"
                title="Toggle fullscreen"
              >
                <ArrowsPointingOutIcon className="w-5 h-5" />
              </button>
              
              <button
                onClick={handleDownload}
                className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100 transition-colors"
                title="Download screenshot"
              >
                <ArrowDownTrayIcon className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>

        {/* Screenshot Display */}
        <div className="flex-1 p-6 overflow-auto">
          <motion.div
            className="screenshot-container max-w-full mx-auto"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
            onClick={() => onScreenshotClick?.(screenshot)}
          >
            {screenshot.base64_image ? (
              <img
                src={`data:image/png;base64,${screenshot.base64_image}`}
                alt="Claude's screen"
                className="cursor-pointer transition-transform hover:scale-105"
              />
            ) : (
              <div className="flex items-center justify-center h-full bg-gray-200 text-gray-500">
                <div className="text-center">
                  <MagnifyingGlassIcon className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <p>Screenshot not available</p>
                </div>
              </div>
            )}
          </motion.div>
        </div>

        {/* Screenshot Info */}
        <div className="bg-white border-t border-gray-200 px-6 py-3">
          <div className="flex items-center justify-between text-sm text-gray-600">
            <div>
              File: {screenshot.filename}
            </div>
            <div>
              Size: {(screenshot.size_bytes / 1024).toFixed(1)} KB
            </div>
            <div>
              ID: {screenshot.id.slice(-8)}
            </div>
          </div>
        </div>
      </div>

      {/* Fullscreen Modal */}
      <AnimatePresence>
        {isZoomed && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-90 z-50 flex items-center justify-center p-4"
            onClick={handleFullscreen}
          >
            <motion.div
              initial={{ scale: 0.8 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.8 }}
              className="max-w-full max-h-full"
              onClick={(e) => e.stopPropagation()}
            >
              {screenshot.base64_image && (
                <img
                  src={`data:image/png;base64,${screenshot.base64_image}`}
                  alt="Claude's screen (fullscreen)"
                  className="max-w-full max-h-full object-contain"
                />
              )}
            </motion.div>
            
            <button
              onClick={handleFullscreen}
              className="absolute top-4 right-4 text-white text-2xl hover:text-gray-300"
            >
              ×
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}