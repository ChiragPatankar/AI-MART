from typing import Dict, Any, List
import numpy as np
from .base_agent import BaseAgent
from ..database.database_manager import DatabaseManager
from ..algorithms.recommendation_algorithms import (
    CollaborativeFiltering,
    ContentBasedFiltering,
    SequentialPatternMining,
    HybridApproach
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database.models import Product, Cart, Customer

class RecommendationAgent(BaseAgent):
    def __init__(self, agent_id: str, db_manager: DatabaseManager):
        super().__init__(agent_id, db_manager)
        self.required_fields = ["customer_id", "action_type"]
        
        # Initialize recommendation algorithms
        self.collaborative_filtering = CollaborativeFiltering()
        self.content_based_filtering = ContentBasedFiltering()
        self.sequential_pattern_mining = SequentialPatternMining()
        self.hybrid_approach = HybridApproach()
        
    async def process(self, data: Dict[str, Any], db: AsyncSession) -> Dict[str, Any]:
        """Process recommendation requests"""
        if not await self.validate_input(data, self.required_fields):
            return {"error": "Missing required fields"}
            
        try:
            action_type = data["action_type"]
            customer_id = data["customer_id"]
            
            if action_type == "get_recommendations":
                return await self._generate_recommendations(
                    customer_id,
                    data.get("algorithm", "hybrid"),
                    data.get("limit", 10),
                    db
                )
            elif action_type == "get_explanation":
                return await self._explain_recommendations(
                    customer_id,
                    data.get("product_id"),
                    db
                )
            else:
                return {"error": f"Unknown action type: {action_type}"}
                
        except Exception as e:
            self.handle_error(e, {"action_type": data.get("action_type"), "customer_id": data.get("customer_id")})
            return {"error": str(e)}
            
    async def learn(self, feedback: Dict[str, Any]) -> None:
        """Learn from recommendation feedback to improve future recommendations"""
        try:
            customer_id = feedback.get("customer_id")
            if not customer_id:
                return
                
            # Update recommendation models based on feedback
            self._update_models(feedback)
            
            # Log the feedback for future analysis
            self.db_manager.log_recommendation_feedback(
                feedback.get("recommendation_id"),
                feedback.get("clicked", False)
            )
            
        except Exception as e:
            self.handle_error(e, feedback)
            
    async def _generate_recommendations(self, customer_id: int, algorithm: str, limit: int = 10, db: AsyncSession = None) -> Dict[str, Any]:
        """Generate product recommendations using specified algorithm"""
        try:
            # Get customer profile and history
            customer_profile = await self._get_customer_profile(customer_id)
            if not customer_profile:
                return {"error": "Customer not found"}
                
            # Get cart items for the customer
            stmt = select(Cart, Product).join(Product).where(Cart.customer_id == customer_id)
            result = await db.execute(stmt)
            cart_items = result.all()
            
            # Format cart items for recommendation algorithms
            cart_products = [{
                "id": product.id,
                "name": product.name,
                "category": product.category,
                "price": float(product.price),
                "quantity": cart_item.quantity,
                "description": product.description
            } for cart_item, product in cart_items]
            
            # Get all products from the database
            stmt = select(Product)
            result = await db.execute(stmt)
            products = result.scalars().all()
            
            # Convert products to list of dictionaries
            product_list = [{
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": float(product.price),
                "category": product.category,
                "image_url": product.image_url
            } for product in products]
            
            # Generate recommendations based on selected algorithm
            recommendations = []
            
            if algorithm == "collaborative":
                recommendations = self.collaborative_filtering.generate_recommendations(
                    customer_profile,
                    cart_products,
                    product_list,
                    limit
                )
            elif algorithm == "content":
                recommendations = self.content_based_filtering.generate_recommendations(
                    customer_profile,
                    cart_products,
                    product_list,
                    limit
                )
            elif algorithm == "sequential":
                recommendations = self.sequential_pattern_mining.generate_recommendations(
                    customer_profile,
                    cart_products,
                    product_list,
                    limit
                )
            else:  # hybrid
                recommendations = self.hybrid_approach.generate_recommendations(
                    customer_profile,
                    cart_products,
                    product_list,
                    limit
                )
            
            # Add algorithm and confidence score to each recommendation
            for rec in recommendations:
                rec["algorithm"] = algorithm
                if "confidence_score" not in rec:
                    rec["confidence_score"] = rec.get("score", 0.0)  # Use the calculated score if no confidence score
            
            return {
                "status": "success",
                "recommendations": recommendations,
                "algorithm": algorithm,
                "based_on_cart": len(cart_products) > 0
            }
            
        except Exception as e:
            print(f"Error generating recommendations: {str(e)}")
            return {"error": str(e)}
            
    async def _explain_recommendations(self, customer_id: int, product_id: int, db: AsyncSession = None) -> Dict[str, Any]:
        """Generate explanation for why a product was recommended"""
        try:
            # Get customer profile and product details
            customer_profile = await self._get_customer_profile(customer_id)
            product_details = await self._get_product_details(product_id, db)
            
            if not customer_profile or not product_details:
                return {"error": "Customer or product not found"}
                
            # Generate explanation using hybrid approach
            explanation = self.hybrid_approach.explain_recommendation(
                customer_profile,
                product_details
            )
            
            return {
                "status": "success",
                "explanation": explanation
            }
            
        except Exception as e:
            self.handle_error(e, {"customer_id": customer_id, "product_id": product_id})
            return {"error": str(e)}
            
    async def _get_customer_profile(self, customer_id: int) -> Dict[str, Any]:
        """Get customer profile from database"""
        # For now, return a default profile
        return {
            "id": customer_id,
            "preferences": {},
            "history": []
        }
        
    async def _get_product_details(self, product_id: int, db: AsyncSession) -> Dict[str, Any]:
        """Get product details from database"""
        stmt = select(Product).where(Product.id == product_id)
        result = await db.execute(stmt)
        product = result.scalar_one_or_none()
        
        if not product:
            return None
            
        return {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": float(product.price),
            "category": product.category,
            "image_url": product.image_url
        }
        
    def _update_models(self, feedback: Dict[str, Any]) -> None:
        """Update recommendation models based on feedback"""
        # Update collaborative filtering model
        self.collaborative_filtering.update_model(feedback)
        
        # Update content-based filtering model
        self.content_based_filtering.update_model(feedback)
        
        # Update sequential pattern mining model
        self.sequential_pattern_mining.update_model(feedback)
        
        # Update hybrid approach
        self.hybrid_approach.update_model(feedback) 