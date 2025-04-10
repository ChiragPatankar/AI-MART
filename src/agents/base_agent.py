from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import logging
from ..database.database_manager import DatabaseManager

class BaseAgent(ABC):
    def __init__(self, agent_id: str, db_manager: DatabaseManager):
        self.agent_id = agent_id
        self.db_manager = db_manager
        self.logger = logging.getLogger(f"{self.__class__.__name__}_{agent_id}")
        
    @abstractmethod
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming data and return results"""
        pass
    
    @abstractmethod
    async def learn(self, feedback: Dict[str, Any]) -> None:
        """Learn from feedback to improve future performance"""
        pass
    
    def log_event(self, event_type: str, details: Dict[str, Any]) -> None:
        """Log an event for monitoring and debugging"""
        self.logger.info(f"Event: {event_type}, Details: {details}")
    
    def handle_error(self, error: Exception, context: Dict[str, Any]) -> None:
        """Handle errors and log them appropriately"""
        self.logger.error(f"Error in {self.agent_id}: {str(error)}", extra=context)
        
    async def validate_input(self, data: Dict[str, Any], required_fields: List[str]) -> bool:
        """Validate input data against required fields"""
        return all(field in data for field in required_fields)
    
    async def get_state(self) -> Dict[str, Any]:
        """Get the current state of the agent"""
        return {
            "agent_id": self.agent_id,
            "status": "active",
            "last_processed": None
        }
    
    async def update_state(self, new_state: Dict[str, Any]) -> None:
        """Update the agent's state"""
        self.logger.info(f"State updated: {new_state}") 