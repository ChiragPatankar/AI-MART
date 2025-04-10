from typing import Dict, Any, List
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .base_agent import BaseAgent
from ..database.database_manager import DatabaseManager
from ..database.models import Customer
import json
import logging

class CustomerAgent(BaseAgent):
    def __init__(self, agent_id: str, db_manager: DatabaseManager):
        super().__init__(agent_id, db_manager)
        self.required_fields = ["customer_id", "action_type"]
        self.logger = logging.getLogger(__name__)
        
    async def process(self, data: Dict[str, Any], db: AsyncSession) -> Dict[str, Any]:
        """Process customer-related actions"""
        if not await self.validate_input(data, self.required_fields):
            return {"error": "Missing required fields"}
            
        try:
            action_type = data["action_type"]
            customer_id = data["customer_id"]
            
            if action_type == "get_profile":
                return await self._get_customer_profile(customer_id, db)
            elif action_type == "update_preferences":
                return await self._update_customer_preferences(customer_id, data.get("preferences", {}), db)
            elif action_type == "track_behavior":
                return await self._track_customer_behavior(customer_id, data.get("behavior_data", {}), db)
            else:
                return {"error": f"Unknown action type: {action_type}"}
                
        except Exception as e:
            self.handle_error(e, {"action_type": data.get("action_type"), "customer_id": data.get("customer_id")})
            return {"error": str(e)}
            
    async def learn(self, feedback: Dict[str, Any], db: AsyncSession) -> None:
        """Learn from customer feedback to improve recommendations"""
        try:
            customer_id = feedback.get("customer_id")
            if not customer_id:
                return
                
            # Update customer embeddings based on feedback
            current_profile = await self._get_customer_profile(customer_id, db)
            if current_profile:
                new_embedding = self._generate_updated_embedding(current_profile, feedback)
                await self._update_customer_embedding(customer_id, new_embedding, db)
                
        except Exception as e:
            self.handle_error(e, feedback)
            
    async def _get_customer_profile(self, customer_id: str, db: AsyncSession) -> Dict[str, Any]:
        """Get detailed customer profile"""
        try:
            # Query the customer from the database
            stmt = select(Customer).where(Customer.id == customer_id)
            result = await db.execute(stmt)
            customer = result.scalar_one_or_none()
            
            if not customer:
                self.logger.warning(f"Customer {customer_id} not found, returning default profile")
                # Return default profile if not found
                return {
                    "profile": {
                        "id": customer_id,
                        "name": f"Customer {customer_id}",
                        "email": f"customer{customer_id}@example.com",
                        "created_at": None,
                        "last_active": None
                    },
                    "preferences": {
                        "categories": [],
                        "price_range": {"min": 0, "max": 1000},
                        "preferred_algorithms": ["hybrid"]
                    }
                }
            
            # Parse preferences from JSON string
            preferences = {
                "categories": [],
                "price_range": {"min": 0, "max": 1000},
                "preferred_algorithms": ["hybrid"]
            }
            try:
                if customer.preferences:
                    preferences = json.loads(customer.preferences)
            except:
                self.logger.warning(f"Failed to parse preferences for customer {customer_id}")
            
            return {
                "profile": {
                    "id": customer.id,
                    "name": customer.name,
                    "email": customer.email,
                    "created_at": customer.created_at.isoformat() if customer.created_at else None,
                    "updated_at": customer.updated_at.isoformat() if customer.updated_at else None
                },
                "preferences": preferences
            }
            
        except Exception as e:
            self.logger.error(f"Error getting customer profile: {str(e)}")
            self.handle_error(e, {"customer_id": customer_id})
            return {"error": str(e)}
            
    async def _update_customer_preferences(self, customer_id: str, preferences: Dict[str, Any], db: AsyncSession) -> Dict[str, Any]:
        """Update customer preferences"""
        try:
            # Get current customer
            stmt = select(Customer).where(Customer.id == customer_id)
            result = await db.execute(stmt)
            customer = result.scalar_one_or_none()
            
            if not customer:
                return {"error": "Customer not found"}
            
            # Update preferences
            current_preferences = {}
            try:
                if customer.preferences:
                    current_preferences = json.loads(customer.preferences)
            except:
                pass
            
            current_preferences.update(preferences)
            customer.preferences = json.dumps(current_preferences)
            
            await db.commit()
            return {"status": "success", "message": "Preferences updated"}
            
        except Exception as e:
            await db.rollback()
            self.handle_error(e, {"customer_id": customer_id, "preferences": preferences})
            return {"error": str(e)}
            
    async def _track_customer_behavior(self, customer_id: str, behavior_data: Dict[str, Any], db: AsyncSession) -> Dict[str, Any]:
        """Track and log customer behavior"""
        try:
            # Get current customer
            stmt = select(Customer).where(Customer.id == customer_id)
            result = await db.execute(stmt)
            customer = result.scalar_one_or_none()
            
            if not customer:
                return {"error": "Customer not found"}
            
            # Update preferences based on behavior
            current_preferences = {}
            try:
                if customer.preferences:
                    current_preferences = json.loads(customer.preferences)
            except:
                pass
            
            # Update browsing history
            if "browsing" in behavior_data:
                browsing = behavior_data["browsing"]
                if "categories" not in current_preferences:
                    current_preferences["categories"] = []
                if browsing.get("category") and browsing["category"] not in current_preferences["categories"]:
                    current_preferences["categories"].append(browsing["category"])
            
            # Update purchase history
            if "purchase" in behavior_data:
                purchase = behavior_data["purchase"]
                if "purchased_categories" not in current_preferences:
                    current_preferences["purchased_categories"] = []
                for item in purchase.get("items", []):
                    if item.get("category") and item["category"] not in current_preferences["purchased_categories"]:
                        current_preferences["purchased_categories"].append(item["category"])
            
            customer.preferences = json.dumps(current_preferences)
            await db.commit()
            
            return {"status": "success", "message": "Behavior tracked"}
            
        except Exception as e:
            await db.rollback()
            self.handle_error(e, {"customer_id": customer_id, "behavior_data": behavior_data})
            return {"error": str(e)}
            
    async def _update_customer_embedding(self, customer_id: str, embedding: np.ndarray, db: AsyncSession) -> None:
        """Update customer embedding in the database"""
        try:
            # Get current customer
            stmt = select(Customer).where(Customer.id == customer_id)
            result = await db.execute(stmt)
            customer = result.scalar_one_or_none()
            
            if not customer:
                return
            
            # Update embedding in CustomerEmbedding table
            # This is a placeholder - you would implement this based on your embedding storage strategy
            pass
            
        except Exception as e:
            await db.rollback()
            self.handle_error(e, {"customer_id": customer_id})
            
    def _generate_updated_embedding(self, current_profile: Dict[str, Any], feedback: Dict[str, Any]) -> np.ndarray:
        """Generate updated customer embedding based on feedback"""
        # This is a placeholder implementation
        # In a real system, you would use a more sophisticated approach
        # to update the embedding based on the feedback
        return np.random.rand(128)  # Example 128-dimensional embedding 