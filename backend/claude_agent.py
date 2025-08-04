"""
Enhanced Claude Agent for autonomous computer use
Based on Anthropic's computer-use-demo with behavioral extensions
"""

import asyncio
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# Import from the computer-use-demo (now in project directory)
import os
from pathlib import Path
# Get the claude-live-viewer project root (parent of backend)
project_root = Path(__file__).parent.parent
computer_demo_path = str(project_root / 'computer-use-demo')
sys.path.append(computer_demo_path)

from anthropic import Anthropic
from anthropic.types.beta import BetaMessageParam

from computer_use_demo.loop import sampling_loop, APIProvider
from computer_use_demo.tools import ToolCollection, ToolResult

logger = logging.getLogger(__name__)

class ClaudeAgent:
    """Enhanced Claude agent with behavioral capabilities"""
    
    def __init__(self, activity_logger=None, screen_service=None, behavioral_system=None):
        self.client = None
        self.is_active = False
        self.conversation_history: List[BetaMessageParam] = []
        
        # Service dependencies
        self.activity_logger = activity_logger
        self.screen_service = screen_service
        self.behavioral_system = behavioral_system
        
        # Configuration
        self.model = "claude-sonnet-4-20250514"
        self.provider = APIProvider.ANTHROPIC
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
    
    async def initialize(self):
        """Initialize the Claude agent"""
        try:
            self.client = Anthropic(api_key=self.api_key)
            self.is_active = True
            
            # Log initialization
            if self.activity_logger:
                await self.activity_logger.log_activity(
                    "system",
                    "agent_initialized",
                    {"model": self.model, "provider": str(self.provider)}
                )
            
            logger.info("Claude agent initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Claude agent: {e}")
            raise
    
    async def execute_command(self, command: str, parameters: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute a specific command"""
        if not self.is_active:
            raise RuntimeError("Claude agent is not active")
        
        try:
            # Log the command
            if self.activity_logger:
                await self.activity_logger.log_activity(
                    "user",
                    "command_sent",
                    {"command": command, "parameters": parameters}
                )
            
            # Add command to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": [{"type": "text", "text": command}]
            })
            
            # Execute using the sampling loop
            result = await self._run_sampling_loop()
            
            return {"success": True, "response": result}
            
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            if self.activity_logger:
                await self.activity_logger.log_activity(
                    "system",
                    "command_error",
                    {"error": str(e), "command": command}
                )
            raise
    
    async def process_chat_message(self, message: str) -> str:
        """Process a chat message and return Claude's response"""
        if not self.is_active:
            raise RuntimeError("Claude agent is not active")
        
        try:
            # Log the chat message
            if self.activity_logger:
                await self.activity_logger.log_activity(
                    "user",
                    "chat_message",
                    {"message": message}
                )
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": [{"type": "text", "text": message}]
            })
            
            # Get Claude's response
            response = await self._run_sampling_loop()
            
            # Log Claude's response
            if self.activity_logger:
                await self.activity_logger.log_activity(
                    "assistant",
                    "chat_response",
                    {"response": response}
                )
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing chat message: {e}")
            raise
    
    async def autonomous_action(self, objective: str) -> Dict[str, Any]:
        """Perform autonomous action based on objective"""
        if not self.is_active:
            raise RuntimeError("Claude agent is not active")
        
        try:
            # Create autonomous prompt
            autonomous_prompt = f"""
            You are an autonomous agent with the objective: {objective}
            
            Please take appropriate actions to work toward this objective.
            Consider the current screen state and decide on the next best action.
            
            Be thoughtful and explain your reasoning for each action.
            """
            
            # Log autonomous action start
            if self.activity_logger:
                await self.activity_logger.log_activity(
                    "system",
                    "autonomous_action_start",
                    {"objective": objective}
                )
            
            # Execute autonomous action
            result = await self.process_chat_message(autonomous_prompt)
            
            return {"success": True, "objective": objective, "result": result}
            
        except Exception as e:
            logger.error(f"Error in autonomous action: {e}")
            raise
    
    async def _run_sampling_loop(self) -> str:
        """Run the Anthropic sampling loop"""
        try:
            # Callbacks for tool outputs and API responses
            def output_callback(content_block):
                if self.activity_logger:
                    asyncio.create_task(
                        self.activity_logger.log_activity(
                            "assistant",
                            "output_block",
                            {"content": str(content_block)}
                        )
                    )
            
            def tool_output_callback(tool_result: ToolResult, tool_id: str):
                if self.activity_logger:
                    asyncio.create_task(
                        self.activity_logger.log_activity(
                            "tool",
                            "tool_execution",
                            {
                                "tool_id": tool_id,
                                "output": tool_result.output,
                                "error": tool_result.error,
                                "has_screenshot": bool(tool_result.base64_image)
                            }
                        )
                    )
            
            def api_response_callback(request, response, error):
                if self.activity_logger and error:
                    asyncio.create_task(
                        self.activity_logger.log_activity(
                            "system",
                            "api_error",
                            {"error": str(error)}
                        )
                    )
            
            # Load system prompt from file
            system_prompt = ""
            try:
                system_prompt_path = Path(__file__).parent.parent / 'SYSTEM_PROMPT.md'
                if system_prompt_path.exists():
                    with open(system_prompt_path, 'r') as f:
                        system_prompt = f.read()
                else:
                    system_prompt = "You are being observed in real-time by humans. Please be thoughtful and explain your actions clearly."
            except Exception as e:
                logger.warning(f"Failed to load system prompt: {e}")
                system_prompt = "You are being observed in real-time by humans. Please be thoughtful and explain your actions clearly."
            
            # Run the sampling loop
            updated_messages = await sampling_loop(
                model=self.model,
                provider=self.provider,
                system_prompt_suffix=system_prompt,
                messages=self.conversation_history,
                output_callback=output_callback,
                tool_output_callback=tool_output_callback,
                api_response_callback=api_response_callback,
                api_key=self.api_key,
                only_n_most_recent_images=3,
                max_tokens=4096,
                tool_version="computer_use_20250124"
            )
            
            # Update conversation history
            self.conversation_history = updated_messages
            
            # Extract the last assistant message
            last_message = None
            for msg in reversed(updated_messages):
                if msg["role"] == "assistant":
                    last_message = msg
                    break
            
            if last_message and isinstance(last_message["content"], list):
                # Extract text content from the message
                text_content = []
                for block in last_message["content"]:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text_content.append(block.get("text", ""))
                
                return " ".join(text_content) if text_content else "No text response"
            
            return "No response generated"
            
        except Exception as e:
            logger.error(f"Error in sampling loop: {e}")
            raise
    
    async def start_autonomous_mode(self, behavior_type: str, parameters: Dict):
        """Start autonomous behavior"""
        if self.behavioral_system:
            await self.behavioral_system.start_behavior(behavior_type, parameters)
        else:
            logger.warning("Behavioral system not available")
    
    async def stop_autonomous_mode(self):
        """Stop autonomous behavior"""
        if self.behavioral_system:
            await self.behavioral_system.stop_current_behavior()
    
    async def get_current_screen(self) -> Optional[Dict]:
        """Get current screen capture"""
        if self.screen_service:
            return await self.screen_service.capture_screenshot()
        return None
    
    async def start_autonomous_exploration(self):
        """Start Claude's autonomous exploration based on system prompt"""
        if not self.is_active:
            raise RuntimeError("Claude agent is not active")
        
        try:
            # Log autonomous start
            if self.activity_logger:
                await self.activity_logger.log_activity(
                    "system",
                    "autonomous_exploration_start",
                    {"mode": "gen_z_crypto_enthusiast"}
                )
            
            # Initial message to kick off autonomous behavior
            initial_prompt = """yo bet! just got access to my own VM and i'm lowkey hyped rn 🔥
            
time to set up my digital space and check what's poppin in the solana ecosystem. gonna make this VM feel like home fr fr

let me start by getting my bearings and seeing what i can do here... maybe check some charts, set up my desktop vibe, and see what tools i got to work with

no cap this hits different having my own computer space 💫"""
            
            # Process as a chat message to trigger autonomous behavior
            response = await self.process_chat_message(initial_prompt)
            
            # Start the crypto enthusiast behavior for continuous autonomous activity
            if self.behavioral_system:
                await self.behavioral_system.start_behavior("crypto_enthusiast", {})
            
            return {"success": True, "mode": "autonomous", "initial_response": response}
            
        except Exception as e:
            logger.error(f"Error starting autonomous exploration: {e}")
            raise
    
    async def shutdown(self):
        """Shutdown the agent"""
        self.is_active = False
        
        if self.activity_logger:
            await self.activity_logger.log_activity(
                "system",
                "agent_shutdown",
                {}
            )
        
        logger.info("Claude agent shut down")