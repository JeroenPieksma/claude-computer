"""
Screen capture service for real-time streaming
"""

import asyncio
import base64
import logging
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional
from uuid import uuid4

logger = logging.getLogger(__name__)

class ScreenCaptureService:
    """Service for capturing and streaming screen content"""
    
    def __init__(self, output_dir: str = "/tmp/claude_screenshots"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Screenshot history
        self.screenshot_history: List[Dict] = []
        self.max_history = 100
        
        # Display configuration
        self.display_num = os.getenv("DISPLAY_NUM", "1")
        self.width = int(os.getenv("WIDTH", "1024"))
        self.height = int(os.getenv("HEIGHT", "768"))
        
        self._display_prefix = f"DISPLAY=:{self.display_num} " if self.display_num else ""
        
        logger.info(f"Screen capture service initialized: {self.width}x{self.height}")
    
    async def capture_screenshot(self) -> Optional[Dict]:
        """Capture a screenshot and return base64 encoded image"""
        # Check if we're in a VM environment with screenshot capabilities
        if not self._command_exists("gnome-screenshot") and not self._command_exists("scrot"):
            # Return a mock screenshot for local development
            return self._create_mock_screenshot()
        
        try:
            timestamp = datetime.now(timezone.utc)
            filename = f"screenshot_{uuid4().hex}.png"
            filepath = self.output_dir / filename
            
            # Use gnome-screenshot or scrot
            if self._command_exists("gnome-screenshot"):
                cmd = f"{self._display_prefix}gnome-screenshot -f {filepath} -p"
            else:
                cmd = f"{self._display_prefix}scrot -p {filepath}"
            
            # Execute screenshot command
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                logger.error(f"Screenshot command failed: {stderr.decode()}")
                return None
            
            # Check if file was created
            if not filepath.exists():
                logger.error("Screenshot file was not created")
                return None
            
            # Read and encode the image
            image_data = filepath.read_bytes()
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            # Create screenshot record
            screenshot = {
                "id": str(uuid4()),
                "timestamp": timestamp.isoformat(),
                "filename": filename,
                "filepath": str(filepath),
                "base64_image": base64_image,
                "resolution": {"width": self.width, "height": self.height},
                "size_bytes": len(image_data)
            }
            
            # Add to history
            self.screenshot_history.append(screenshot)
            
            # Maintain history limit
            if len(self.screenshot_history) > self.max_history:
                old_screenshot = self.screenshot_history.pop(0)
                self._cleanup_screenshot_file(old_screenshot["filepath"])
            
            logger.debug(f"Screenshot captured: {filename}")
            return screenshot
            
        except Exception as e:
            logger.error(f"Error capturing screenshot: {e}")
            return None
    
    def get_recent_screenshots(self, limit: int = 10) -> List[Dict]:
        """Get recent screenshots (without base64 data for efficiency)"""
        recent = self.screenshot_history[-limit:] if limit > 0 else self.screenshot_history
        
        # Return without base64 data to reduce payload size
        return [
            {
                "id": shot["id"],
                "timestamp": shot["timestamp"],
                "filename": shot["filename"],
                "resolution": shot["resolution"],
                "size_bytes": shot["size_bytes"]
            }
            for shot in recent
        ]
    
    def get_screenshot_by_id(self, screenshot_id: str) -> Optional[Dict]:
        """Get a specific screenshot by ID"""
        for screenshot in self.screenshot_history:
            if screenshot["id"] == screenshot_id:
                return screenshot
        return None
    
    def get_resolution(self) -> Dict[str, int]:
        """Get current screen resolution"""
        return {"width": self.width, "height": self.height}
    
    async def start_continuous_capture(self, interval_seconds: float = 1.0, callback=None):
        """Start continuous screenshot capture"""
        logger.info(f"Starting continuous capture every {interval_seconds}s")
        
        while True:
            try:
                screenshot = await self.capture_screenshot()
                if screenshot and callback:
                    await callback(screenshot)
                
                await asyncio.sleep(interval_seconds)
                
            except asyncio.CancelledError:
                logger.info("Continuous capture cancelled")
                break
            except Exception as e:
                logger.error(f"Error in continuous capture: {e}")
                await asyncio.sleep(interval_seconds)
    
    def _command_exists(self, command: str) -> bool:
        """Check if a command exists in the system"""
        try:
            subprocess.run(['which', command], check=True, 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _create_mock_screenshot(self) -> Dict:
        """Create a mock screenshot for local development"""
        from PIL import Image, ImageDraw, ImageFont
        import io
        
        # Create a simple placeholder image
        img = Image.new('RGB', (self.width, self.height), color='#f0f0f0')
        draw = ImageDraw.Draw(img)
        
        # Add some text
        try:
            # Try to use a default font
            font = ImageFont.load_default()
        except:
            font = None
        
        text_lines = [
            "Claude Live Viewer",
            "Local Development Mode",
            f"Resolution: {self.width}x{self.height}",
            "",
            "This is a mock screenshot.",
            "In VM environment, real screenshots",
            "will be captured from Claude's desktop.",
            "",
            f"Timestamp: {datetime.now().strftime('%H:%M:%S')}"
        ]
        
        y_offset = 50
        for line in text_lines:
            draw.text((50, y_offset), line, fill='#666666', font=font)
            y_offset += 30
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        timestamp = datetime.now(timezone.utc)
        screenshot = {
            "id": str(uuid4()),
            "timestamp": timestamp.isoformat(),
            "filename": f"mock_screenshot_{uuid4().hex}.png",
            "filepath": "mock",
            "base64_image": base64_image,
            "resolution": {"width": self.width, "height": self.height},
            "size_bytes": len(buffer.getvalue())
        }
        
        # Add to history
        self.screenshot_history.append(screenshot)
        if len(self.screenshot_history) > self.max_history:
            self.screenshot_history.pop(0)
        
        logger.debug("Created mock screenshot for local development")
        return screenshot
    
    def _cleanup_screenshot_file(self, filepath: str):
        """Clean up old screenshot files"""
        try:
            Path(filepath).unlink(missing_ok=True)
        except Exception as e:
            logger.warning(f"Failed to cleanup screenshot file {filepath}: {e}")
    
    async def cleanup(self):
        """Cleanup service resources"""
        logger.info("Cleaning up screen capture service")
        
        # Clean up all screenshot files
        for screenshot in self.screenshot_history:
            self._cleanup_screenshot_file(screenshot["filepath"])
        
        self.screenshot_history.clear()
        
        # Clean up output directory if empty
        try:
            if self.output_dir.exists() and not any(self.output_dir.iterdir()):
                self.output_dir.rmdir()
        except Exception as e:
            logger.warning(f"Failed to cleanup output directory: {e}")


class ScreenStreamManager:
    """Manager for streaming screenshots to multiple clients"""
    
    def __init__(self, screen_service: ScreenCaptureService):
        self.screen_service = screen_service
        self.streaming_task: Optional[asyncio.Task] = None
        self.callbacks: List = []
        self.is_streaming = False
    
    def add_callback(self, callback):
        """Add a callback for screen updates"""
        self.callbacks.append(callback)
    
    def remove_callback(self, callback):
        """Remove a callback"""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
    
    async def start_streaming(self, fps: float = 1.0):
        """Start streaming screenshots"""
        if self.is_streaming:
            return
        
        self.is_streaming = True
        interval = 1.0 / fps
        
        logger.info(f"Starting screen streaming at {fps} FPS")
        
        async def stream_callback(screenshot):
            """Callback for new screenshots"""
            for callback in self.callbacks[:]:  # Copy list to avoid modification during iteration
                try:
                    await callback(screenshot)
                except Exception as e:
                    logger.error(f"Error in stream callback: {e}")
        
        self.streaming_task = asyncio.create_task(
            self.screen_service.start_continuous_capture(interval, stream_callback)
        )
    
    async def stop_streaming(self):
        """Stop streaming screenshots"""
        if not self.is_streaming:
            return
        
        self.is_streaming = False
        
        if self.streaming_task:
            self.streaming_task.cancel()
            try:
                await self.streaming_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Screen streaming stopped")
    
    async def cleanup(self):
        """Cleanup streaming resources"""
        await self.stop_streaming()
        self.callbacks.clear()