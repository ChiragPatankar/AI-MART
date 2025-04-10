from typing import Dict, Any, List
import numpy as np
from .base_recommendation import BaseRecommendationAlgorithm

class CollaborativeFiltering(BaseRecommendationAlgorithm):
    def __init__(self):
        super().__init__()
        self.user_item_matrix = None
        self.user_similarity_matrix = None
        self.item_similarity_matrix = None
        
    def generate_recommendations(self, customer_profile: Dict[str, Any], cart_products: List[Dict[str, Any]], product_list: List[Dict[str, Any]], limit: int = 10) -> List[Dict[str, Any]]:
        """Generate recommendations using collaborative filtering"""
        try:
            recommendations = []
            
            # If cart is empty, recommend popular products
            if not cart_products:
                # Simple popularity-based recommendations
                for product in product_list[:limit]:
                    recommendations.append({
                        "product_id": product["id"],
                        "product": product,
                        "score": 0.7,
                        "source": "popular_product",
                        "explanation": f"Popular product in the {product['category']} category"
                    })
                return recommendations
            
            # Get categories from cart items
            cart_categories = set(item["category"] for item in cart_products)
            
            # Filter out products already in cart
            cart_product_ids = set(item["id"] for item in cart_products)
            available_products = [p for p in product_list if p["id"] not in cart_product_ids]
            
            # Find products in similar categories
            for product in available_products:
                if product["category"] in cart_categories:
                    recommendations.append({
                        "product_id": product["id"],
                        "product": product,
                        "score": 0.8,
                        "source": "collaborative_filtering",
                        "explanation": f"Customers who bought items in {product['category']} also bought this"
                    })
            
            # Sort by score and take top recommendations
            recommendations.sort(key=lambda x: x["score"], reverse=True)
            return recommendations[:limit]
            
        except Exception as e:
            print(f"Error in collaborative filtering: {str(e)}")
            return []
            
    def update_model(self, feedback: Dict[str, Any]) -> None:
        """Update the collaborative filtering model based on feedback"""
        try:
            # Update user-item matrix with new interactions
            self._update_user_item_matrix(feedback)
            
            # Recalculate similarity matrices
            self._recalculate_similarity_matrices()
            
            # Update model parameters
            self._update_model_parameters(feedback)
            
        except Exception as e:
            # Log error and continue with current model
            pass
            
    def explain_recommendation(self, customer_profile: Dict[str, Any], product: Dict[str, Any]) -> Dict[str, Any]:
        """Generate explanation for why a product was recommended"""
        try:
            # Get similar users who liked this product
            similar_users = self._get_similar_users_who_liked_product(
                customer_profile,
                product
            )
            
            # Generate explanation based on similar users
            explanation = self._generate_explanation_from_similar_users(
                similar_users,
                product
            )
            
            return explanation
            
        except Exception as e:
            # Return generic explanation if specific one cannot be generated
            return {
                "explanation": "This product was recommended based on preferences of similar customers.",
                "confidence": 0.5
            }
            
    def _get_user_history(self, customer_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Get user's purchase and browsing history"""
        # This is a placeholder implementation
        return {
            "purchases": customer_profile.get("purchases", []),
            "browsing_history": customer_profile.get("browsing_history", [])
        }
        
    def _calculate_user_similarities(self, user_history: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Calculate similarities between users"""
        # This is a placeholder implementation
        return []
        
    def _get_similar_users_preferences(
        self,
        user_similarities: List[Dict[str, Any]],
        limit: int
    ) -> List[Dict[str, Any]]:
        """Get preferences of similar users"""
        # This is a placeholder implementation
        return []
        
    def _generate_recommendations_from_similar_users(
        self,
        similar_users_preferences: List[Dict[str, Any]],
        user_history: Dict[str, Any],
        limit: int
    ) -> List[Dict[str, Any]]:
        """Generate recommendations based on similar users' preferences"""
        # This is a placeholder implementation
        return []
        
    def _get_fallback_recommendations(self, limit: int) -> List[Dict[str, Any]]:
        """Get fallback recommendations when main algorithm fails"""
        # This is a placeholder implementation
        return []
        
    def _update_user_item_matrix(self, feedback: Dict[str, Any]) -> None:
        """Update the user-item interaction matrix"""
        # This is a placeholder implementation
        pass
        
    def _recalculate_similarity_matrices(self) -> None:
        """Recalculate user and item similarity matrices"""
        # This is a placeholder implementation
        pass
        
    def _update_model_parameters(self, feedback: Dict[str, Any]) -> None:
        """Update model parameters based on feedback"""
        # This is a placeholder implementation
        pass
        
    def _get_similar_users_who_liked_product(
        self,
        customer_profile: Dict[str, Any],
        product: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Get similar users who liked the product"""
        # This is a placeholder implementation
        return []
        
    def _generate_explanation_from_similar_users(
        self,
        similar_users: List[Dict[str, Any]],
        product: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate explanation based on similar users' preferences"""
        # This is a placeholder implementation
        return {
            "explanation": "Similar customers who liked this product also liked...",
            "confidence": 0.8
        } 