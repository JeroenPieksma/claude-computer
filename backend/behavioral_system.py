"""
Behavioral system for autonomous Claude activities
"""

import asyncio
import logging
import random
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum

from backend.autonomous_behaviors import AutonomousCryptoBehavior

logger = logging.getLogger(__name__)

class BehaviorStatus(Enum):
    """Status of a behavior"""
    INACTIVE = "inactive"
    ACTIVE = "active" 
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class BehaviorConfig:
    """Configuration for a behavior"""
    name: str
    description: str
    parameters: Dict[str, Any]
    duration_minutes: Optional[int] = None
    repeat: bool = False
    priority: int = 1

class BaseBehavior:
    """Base class for all behaviors"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.status = BehaviorStatus.INACTIVE
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.error_message: Optional[str] = None
        
        # Dependencies
        self.claude_agent = None
        self.activity_logger = None
        
    async def start(self, parameters: Dict[str, Any], duration_minutes: Optional[int] = None):
        """Start the behavior"""
        self.status = BehaviorStatus.ACTIVE
        self.start_time = datetime.now(timezone.utc)
        
        if duration_minutes:
            self.end_time = self.start_time + timedelta(minutes=duration_minutes)
        
        try:
            await self.execute(parameters)
            if self.status == BehaviorStatus.ACTIVE:
                self.status = BehaviorStatus.COMPLETED
        except Exception as e:
            self.status = BehaviorStatus.ERROR
            self.error_message = str(e)
            logger.error(f"Error in behavior {self.name}: {e}")
            raise
    
    async def stop(self):
        """Stop the behavior"""
        if self.status == BehaviorStatus.ACTIVE:
            self.status = BehaviorStatus.INACTIVE
            await self.cleanup()
    
    async def pause(self):
        """Pause the behavior"""
        if self.status == BehaviorStatus.ACTIVE:
            self.status = BehaviorStatus.PAUSED
    
    async def resume(self):
        """Resume the behavior"""
        if self.status == BehaviorStatus.PAUSED:
            self.status = BehaviorStatus.ACTIVE
    
    async def execute(self, parameters: Dict[str, Any]):
        """Execute the behavior logic - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement execute method")
    
    async def cleanup(self):
        """Cleanup resources - can be overridden by subclasses"""
        pass
    
    def is_active(self) -> bool:
        """Check if behavior is currently active"""
        return self.status == BehaviorStatus.ACTIVE
    
    def should_stop(self) -> bool:
        """Check if behavior should stop based on duration"""
        if self.end_time and datetime.now(timezone.utc) >= self.end_time:
            return True
        return False

class WebBrowsingBehavior(BaseBehavior):
    """Behavior for autonomous web browsing"""
    
    def __init__(self):
        super().__init__(
            "web_browsing",
            "Browse the web autonomously, visiting websites and exploring content"
        )
        self.visited_sites = []
        self.current_objective = ""
    
    async def execute(self, parameters: Dict[str, Any]):
        """Execute web browsing behavior"""
        sites_to_visit = parameters.get("sites", [
            "https://news.ycombinator.com",
            "https://reddit.com/r/technology", 
            "https://github.com/trending",
            "https://stackoverflow.com",
            "https://medium.com"
        ])
        
        browse_duration = parameters.get("browse_duration_minutes", 5)
        random_browsing = parameters.get("random_browsing", True)
        
        if self.activity_logger:
            await self.activity_logger.log_activity(
                "behavior",
                "autonomous_action",
                {"behavior": "web_browsing", "sites": sites_to_visit}
            )
        
        for site in sites_to_visit:
            if self.should_stop() or self.status != BehaviorStatus.ACTIVE:
                break
                
            try:
                await self._browse_site(site, browse_duration, random_browsing)
                self.visited_sites.append(site)
                
                # Wait between sites
                await asyncio.sleep(random.uniform(10, 30))
                
            except Exception as e:
                logger.error(f"Error browsing {site}: {e}")
                continue
    
    async def _browse_site(self, site: str, duration_minutes: int, random_browsing: bool):
        """Browse a specific site"""
        if not self.claude_agent:
            return
        
        # Open the site
        await self.claude_agent.process_chat_message(f"Please navigate to {site} and explore the content")
        
        # Browse for specified duration
        end_time = datetime.now(timezone.utc) + timedelta(minutes=duration_minutes)
        
        while datetime.now(timezone.utc) < end_time and self.status == BehaviorStatus.ACTIVE:
            if random_browsing:
                actions = [
                    "Scroll down to see more content",
                    "Click on an interesting article or link",
                    "Look for navigation menus or categories",
                    "Search for something interesting on this site",
                    "Take a screenshot of the current page"
                ]
                action = random.choice(actions)
                await self.claude_agent.process_chat_message(action)
            
            await asyncio.sleep(random.uniform(30, 60))

class ResearchBehavior(BaseBehavior):
    """Behavior for conducting research on topics"""
    
    def __init__(self):
        super().__init__(
            "research",
            "Conduct research on specified topics using web search and exploration"
        )
        self.research_notes = []
    
    async def execute(self, parameters: Dict[str, Any]):
        """Execute research behavior"""
        topic = parameters.get("topic", "artificial intelligence")
        depth = parameters.get("depth", "moderate")  # basic, moderate, deep
        sources = parameters.get("sources", ["web", "wikipedia", "academic"])
        
        if self.activity_logger:
            await self.activity_logger.log_activity(
                "behavior", 
                "autonomous_action",
                {"behavior": "research", "topic": topic, "depth": depth}
            )
        
        # Start research
        await self._conduct_research(topic, depth, sources)
    
    async def _conduct_research(self, topic: str, depth: str, sources: List[str]):
        """Conduct research on a topic"""
        if not self.claude_agent:
            return
        
        # Initial research prompt
        research_prompt = f"""
        I want to conduct {depth} research on the topic: {topic}
        
        Please help me research this topic by:
        1. Searching for information about {topic}
        2. Visiting relevant websites and sources
        3. Taking notes on key findings
        4. Exploring different aspects of the topic
        
        Use sources like: {', '.join(sources)}
        """
        
        await self.claude_agent.process_chat_message(research_prompt)
        
        # Continue research for duration
        research_actions = [
            f"Search for '{topic} latest developments'",
            f"Look for academic papers about {topic}",
            f"Find different perspectives on {topic}",
            f"Explore the history and evolution of {topic}",
            f"Look for practical applications of {topic}",
            f"Find expert opinions on {topic}"
        ]
        
        while not self.should_stop() and self.status == BehaviorStatus.ACTIVE:
            action = random.choice(research_actions)
            await self.claude_agent.process_chat_message(action)
            await asyncio.sleep(random.uniform(60, 120))

class CreativeBehavior(BaseBehavior):
    """Behavior for creative activities like writing, drawing, etc."""
    
    def __init__(self):
        super().__init__(
            "creative",
            "Engage in creative activities like writing, note-taking, or using creative tools"
        )
    
    async def execute(self, parameters: Dict[str, Any]):
        """Execute creative behavior"""
        activity_type = parameters.get("type", "writing")  # writing, drawing, music
        theme = parameters.get("theme", "technology and society")
        
        if self.activity_logger:
            await self.activity_logger.log_activity(
                "behavior",
                "autonomous_action", 
                {"behavior": "creative", "type": activity_type, "theme": theme}
            )
        
        if activity_type == "writing":
            await self._creative_writing(theme)
        elif activity_type == "drawing":
            await self._creative_drawing(theme)
        elif activity_type == "notes":
            await self._creative_notes(theme)
    
    async def _creative_writing(self, theme: str):
        """Engage in creative writing"""
        if not self.claude_agent:
            return
        
        writing_prompt = f"""
        I'd like to engage in some creative writing about {theme}.
        
        Please help me:
        1. Open a text editor or document
        2. Start writing creatively about {theme}
        3. Explore different ideas and perspectives
        4. Create an engaging piece of writing
        
        Feel free to be creative and thoughtful in your approach.
        """
        
        await self.claude_agent.process_chat_message(writing_prompt)
        
        # Continue writing
        while not self.should_stop() and self.status == BehaviorStatus.ACTIVE:
            writing_actions = [
                "Continue writing and develop your ideas further",
                "Add more details to your current section",
                "Start a new paragraph with a different perspective",
                "Review and edit what you've written so far",
                "Add examples or illustrations to your writing"
            ]
            
            action = random.choice(writing_actions)
            await self.claude_agent.process_chat_message(action)
            await asyncio.sleep(random.uniform(90, 180))
    
    async def _creative_drawing(self, theme: str):
        """Engage in creative drawing"""
        if not self.claude_agent:
            return
        
        drawing_prompt = f"""
        I'd like to do some creative drawing or digital art about {theme}.
        
        Please:
        1. Open a drawing application or tool
        2. Start creating artwork related to {theme}
        3. Experiment with different tools and techniques
        4. Be creative and expressive
        """
        
        await self.claude_agent.process_chat_message(drawing_prompt)
    
    async def _creative_notes(self, theme: str):
        """Take creative notes and organize thoughts"""
        if not self.claude_agent:
            return
        
        notes_prompt = f"""
        I want to create and organize notes about {theme}.
        
        Please help me:
        1. Open a note-taking application
        2. Create structured notes about {theme}
        3. Organize ideas in a creative way
        4. Add connections between different concepts
        """
        
        await self.claude_agent.process_chat_message(notes_prompt)

class ExplorationBehavior(BaseBehavior):
    """Behavior for exploring the computer environment"""
    
    def __init__(self):
        super().__init__(
            "exploration",
            "Explore the computer environment, applications, and file system"
        )
    
    async def execute(self, parameters: Dict[str, Any]):
        """Execute exploration behavior"""
        areas = parameters.get("areas", ["applications", "filesystem", "settings"])
        
        if self.activity_logger:
            await self.activity_logger.log_activity(
                "behavior",
                "autonomous_action",
                {"behavior": "exploration", "areas": areas}
            )
        
        for area in areas:
            if self.should_stop() or self.status != BehaviorStatus.ACTIVE:
                break
            
            await self._explore_area(area)
            await asyncio.sleep(random.uniform(30, 60))
    
    async def _explore_area(self, area: str):
        """Explore a specific area of the system"""
        if not self.claude_agent:
            return
        
        exploration_prompts = {
            "applications": "Explore the available applications on this system. Look at what's installed and try opening some interesting ones.",
            "filesystem": "Explore the file system. Look at different directories and see what files and folders are available.",
            "settings": "Explore the system settings and preferences. See what configuration options are available.",
            "desktop": "Explore the desktop environment. Look at the taskbar, menus, and available tools."
        }
        
        prompt = exploration_prompts.get(area, f"Explore the {area} of this computer system")
        await self.claude_agent.process_chat_message(prompt)

class GenZCryptoBehavior(BaseBehavior):
    """Behavior for Gen Z crypto enthusiast autonomous activities"""
    
    def __init__(self):
        super().__init__(
            "crypto_enthusiast",
            "Autonomous Gen Z crypto enthusiast exploring the digital space"
        )
        self.crypto_behavior = AutonomousCryptoBehavior()
    
    async def execute(self, parameters: Dict[str, Any]):
        """Execute Gen Z crypto enthusiast behavior"""
        if self.activity_logger:
            await self.activity_logger.log_activity(
                "behavior",
                "autonomous_crypto_start",
                {"behavior": "gen_z_crypto_enthusiast"}
            )
        
        # Continuous autonomous behavior loop
        while not self.should_stop() and self.status == BehaviorStatus.ACTIVE:
            # Get next activity
            activity = self.crypto_behavior.get_random_activity()
            
            if activity and self.claude_agent:
                logger.info(f"Claude engaging in autonomous activity: {activity['action']}")
                
                # Send the activity prompt to Claude
                await self.claude_agent.process_chat_message(activity['prompt'])
                
                # Log the activity
                if self.activity_logger:
                    await self.activity_logger.log_activity(
                        "behavior",
                        "autonomous_crypto_activity",
                        {
                            "action": activity['action'],
                            "prompt": activity['prompt']
                        }
                    )
            
            # Wait before next activity (randomized intervals)
            wait_time = random.uniform(180, 420)  # 3-7 minutes between activities
            await asyncio.sleep(wait_time)
            
            # Sometimes Claude might get distracted or react to things
            if random.random() < 0.3:  # 30% chance of spontaneous reaction
                spontaneous_prompts = [
                    "wait hold up, lemme check something real quick...",
                    "yo did I just see that notification? one sec",
                    "actually this is kinda interesting, bout to explore this more",
                    "nah this chart looking sus, need to investigate"
                ]
                spontaneous = random.choice(spontaneous_prompts)
                if self.claude_agent:
                    await self.claude_agent.process_chat_message(spontaneous)
                await asyncio.sleep(random.uniform(30, 90))

class BehavioralSystem:
    """Main system for managing Claude's behaviors"""
    
    def __init__(self):
        self.behaviors: Dict[str, BaseBehavior] = {}
        self.current_behavior: Optional[BaseBehavior] = None
        self.behavior_history: List[Dict] = []
        
        # Initialize available behaviors
        self._initialize_behaviors()
        
        # Add the Gen Z crypto behavior
        self.behaviors["crypto_enthusiast"] = GenZCryptoBehavior()
        
        logger.info("Behavioral system initialized")
    
    def _initialize_behaviors(self):
        """Initialize available behaviors"""
        behaviors = [
            WebBrowsingBehavior(),
            ResearchBehavior(), 
            CreativeBehavior(),
            ExplorationBehavior()
        ]
        
        for behavior in behaviors:
            self.behaviors[behavior.name] = behavior
    
    async def start_behavior(
        self, 
        behavior_type: str, 
        parameters: Dict[str, Any],
        duration_minutes: Optional[int] = None
    ):
        """Start a specific behavior"""
        if behavior_type not in self.behaviors:
            raise ValueError(f"Unknown behavior type: {behavior_type}")
        
        # Stop current behavior if active
        if self.current_behavior and self.current_behavior.is_active():
            await self.stop_current_behavior()
        
        behavior = self.behaviors[behavior_type]
        
        # Set dependencies
        behavior.claude_agent = getattr(self, 'claude_agent', None)
        behavior.activity_logger = getattr(self, 'activity_logger', None)
        
        self.current_behavior = behavior
        
        # Record in history
        self.behavior_history.append({
            "behavior": behavior_type,
            "parameters": parameters,
            "start_time": datetime.now(timezone.utc).isoformat(),
            "duration_minutes": duration_minutes,
            "status": "started"
        })
        
        try:
            await behavior.start(parameters, duration_minutes)
            
            # Update history
            if self.behavior_history:
                self.behavior_history[-1]["status"] = "completed"
                self.behavior_history[-1]["end_time"] = datetime.now(timezone.utc).isoformat()
            
        except Exception as e:
            if self.behavior_history:
                self.behavior_history[-1]["status"] = "error"
                self.behavior_history[-1]["error"] = str(e)
            raise
    
    async def stop_current_behavior(self):
        """Stop the currently active behavior"""
        if self.current_behavior and self.current_behavior.is_active():
            await self.current_behavior.stop()
            
            # Update history
            if self.behavior_history:
                self.behavior_history[-1]["status"] = "stopped"
                self.behavior_history[-1]["end_time"] = datetime.now(timezone.utc).isoformat()
        
        self.current_behavior = None
    
    async def pause_current_behavior(self):
        """Pause the currently active behavior"""
        if self.current_behavior and self.current_behavior.is_active():
            await self.current_behavior.pause()
    
    async def resume_current_behavior(self):
        """Resume the currently paused behavior"""
        if self.current_behavior and self.current_behavior.status == BehaviorStatus.PAUSED:
            await self.current_behavior.resume()
    
    def get_available_behaviors(self) -> List[str]:
        """Get list of available behavior types"""
        return list(self.behaviors.keys())
    
    def get_current_behavior_status(self) -> Optional[Dict]:
        """Get status of current behavior"""
        if not self.current_behavior:
            return None
        
        return {
            "name": self.current_behavior.name,
            "description": self.current_behavior.description,
            "status": self.current_behavior.status.value,
            "start_time": self.current_behavior.start_time.isoformat() if self.current_behavior.start_time else None,
            "end_time": self.current_behavior.end_time.isoformat() if self.current_behavior.end_time else None,
            "error_message": self.current_behavior.error_message
        }
    
    def get_behavior_history(self, limit: int = 10) -> List[Dict]:
        """Get behavior execution history"""
        return self.behavior_history[-limit:] if limit > 0 else self.behavior_history
    
    def set_dependencies(self, claude_agent=None, activity_logger=None):
        """Set dependency references for behaviors"""
        self.claude_agent = claude_agent
        self.activity_logger = activity_logger
        
        # Update all behaviors
        for behavior in self.behaviors.values():
            behavior.claude_agent = claude_agent
            behavior.activity_logger = activity_logger
    
    async def cleanup(self):
        """Cleanup behavioral system"""
        await self.stop_current_behavior()
        logger.info("Behavioral system cleaned up")