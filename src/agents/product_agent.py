from typing import Dict, Any, List
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from .base_agent import BaseAgent
from ..database.database_manager import DatabaseManager
from ..database.models import Product
import logging
import json

class ProductAgent(BaseAgent):
    def __init__(self, agent_id: str, db_manager: DatabaseManager):
        super().__init__(agent_id, db_manager)
        self.required_fields = ["action_type"]
        self.logger = logging.getLogger(__name__)
        
    async def process(self, data: Dict[str, Any], db: AsyncSession) -> Dict[str, Any]:
        """Process product-related actions"""
        try:
            action = data.get("action_type", "")
            if action == "search_products":
                return await self._search_products(data, db)
            elif action == "get_categories":
                return await self._get_categories(db)
            elif action == "get_product":
                return await self._get_product_details(data.get("product_id"), db)
            elif action == "get_similar_products":
                return await self._get_similar_products(data.get("product_id"), data.get("limit", 10), db)
            elif action == "update_product":
                return await self._update_product(data.get("product_id"), data.get("product_data", {}))
            else:
                return {"error": f"Unknown action: {action}"}
                
        except Exception as e:
            self.handle_error(e, {"action": action})
            return {"error": str(e)}
            
    async def learn(self, feedback: Dict[str, Any]) -> None:
        """Learn from product interactions to improve recommendations"""
        try:
            product_id = feedback.get("product_id")
            if not product_id:
                return
                
            # Update product embeddings based on feedback
            current_product = await self._get_product_details(product_id, None)
            if current_product:
                new_embedding = self._generate_updated_embedding(current_product, feedback)
                self.db_manager.update_product_embedding(product_id, new_embedding)
                
        except Exception as e:
            self.handle_error(e, feedback)
            
    async def _search_products(self, data: Dict[str, Any], db: AsyncSession) -> Dict[str, Any]:
        """Search for products based on query parameters"""
        try:
            query = data.get("query", "")
            category = data.get("category", "")
            sort_by = data.get("sort_by", "relevance")
            page = data.get("page", 1)
            limit = data.get("limit", 12)
            offset = (page - 1) * limit
            
            self.logger.info(f"Searching products with params: query='{query}', category='{category}', sort_by='{sort_by}', page={page}, limit={limit}")
            
            # Build base query
            stmt = select(Product)
            
            # Apply filters
            if query:
                stmt = stmt.where(
                    Product.name.ilike(f"%{query}%") |
                    Product.description.ilike(f"%{query}%") |
                    Product.category.ilike(f"%{query}%")
                )
            
            if category:
                stmt = stmt.where(Product.category == category)
            
            # Apply sorting
            if sort_by == "price_asc":
                stmt = stmt.order_by(Product.price.asc())
            elif sort_by == "price_desc":
                stmt = stmt.order_by(Product.price.desc())
            
            # Get total count
            count_stmt = select(func.count()).select_from(stmt.subquery())
            total = await db.scalar(count_stmt)
            
            self.logger.info(f"Found {total} total products matching criteria")
            
            # Apply pagination
            stmt = stmt.offset(offset).limit(limit)
            
            # Execute query
            result = await db.execute(stmt)
            products = result.scalars().all()
            
            self.logger.info(f"Returning {len(products)} products for current page")
            
            # Format products
            formatted_products = []
            for product in products:
                features = {}
                try:
                    if product.features:
                        features = json.loads(product.features)
                except:
                    pass
                
                formatted_products.append({
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "category": product.category,
                    "price": product.price,
                    "image_url": product.image_url,
                    "features": features
                })
            
            return {
                "products": formatted_products,
                "total": total,
                "page": page,
                "limit": limit,
                "total_pages": (total + limit - 1) // limit
            }
            
        except Exception as e:
            self.logger.error(f"Error searching products: {str(e)}")
            return {"error": str(e)}
            
    async def _get_categories(self, db: AsyncSession) -> Dict[str, Any]:
        """Get all unique product categories"""
        try:
            stmt = select(Product.category).distinct()
            result = await db.execute(stmt)
            categories = result.scalars().all()
            
            return {
                "categories": sorted(categories)
            }
            
        except Exception as e:
            return {"error": str(e)}
            
    async def _get_product_details(self, product_id: str, db: AsyncSession) -> Dict[str, Any]:
        """Get detailed product information"""
        try:
            stmt = select(Product).where(Product.id == product_id)
            result = await db.execute(stmt)
            product = result.scalar_one_or_none()
            
            if not product:
                return {"error": "Product not found"}
            
            features = {}
            try:
                if product.features:
                    features = json.loads(product.features)
            except:
                pass
            
            return {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "category": product.category,
                "price": product.price,
                "image_url": product.image_url,
                "features": features,
                "created_at": product.created_at.isoformat() if product.created_at else None,
                "updated_at": product.updated_at.isoformat() if product.updated_at else None
            }
            
        except Exception as e:
            self.handle_error(e, {"product_id": product_id})
            return {"error": str(e)}
            
    async def _get_similar_products(self, product_id: str, limit: int, db: AsyncSession) -> Dict[str, Any]:
        """Get similar products based on category and features"""
        try:
            # Get the source product
            product = await self._get_product_details(product_id, db)
            if "error" in product:
                return product
            
            # Find products in the same category
            stmt = select(Product).where(
                Product.category == product["category"],
                Product.id != product_id
            ).limit(limit)
            
            result = await db.execute(stmt)
            similar_products = result.scalars().all()
            
            formatted_products = []
            for p in similar_products:
                features = {}
                try:
                    if p.features:
                        features = json.loads(p.features)
                except:
                    pass
                
                formatted_products.append({
                    "id": p.id,
                    "name": p.name,
                    "description": p.description,
                    "category": p.category,
                    "price": p.price,
                    "image_url": p.image_url,
                    "features": features
                })
            
            return {
                "similar_products": formatted_products
            }
            
        except Exception as e:
            self.handle_error(e, {"product_id": product_id, "limit": limit})
            return {"error": str(e)}
            
    async def _update_product(self, product_id: int, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update product information"""
        try:
            # Update product in database
            self.db_manager.update_product(product_id, product_data)
            return {"status": "success", "message": "Product updated"}
        except Exception as e:
            self.handle_error(e, {"product_id": product_id, "product_data": product_data})
            return {"error": str(e)}
            
    def _generate_updated_embedding(self, current_product: Dict[str, Any], feedback: Dict[str, Any]) -> np.ndarray:
        """Generate updated product embedding based on feedback"""
        # This is a placeholder implementation
        # In a real system, you would use a more sophisticated approach
        # to update the embedding based on the feedback
        return np.random.rand(128)  # Example 128-dimensional embedding 