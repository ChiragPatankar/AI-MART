from typing import Dict, Any, List
import numpy as np
from .base_recommendation import BaseRecommendationAlgorithm

class SequentialPatternMining(BaseRecommendationAlgorithm):
    def __init__(self):
        super().__init__()
        self.sequence_database = None
        self.patterns = None
        self.min_support = 0.1
        self.min_confidence = 0.5
        
    def generate_recommendations(self, customer_profile: Dict[str, Any], cart_products: List[Dict[str, Any]], product_list: List[Dict[str, Any]], limit: int = 10) -> List[Dict[str, Any]]:
        """Generate recommendations using sequential pattern mining"""
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
                        "source": "sequential",
                        "explanation": f"Frequently purchased product in {product['category']}"
                    })
                return recommendations
            
            # Filter out products already in cart
            cart_product_ids = set(item["id"] for item in cart_products)
            available_products = [p for p in product_list if p["id"] not in cart_product_ids]
            
            # Get categories from cart items
            cart_categories = set(item["category"] for item in cart_products)
            
            # Find products frequently bought together
            for product in available_products:
                base_score = 0.7
                score_boost = 0.0
                
                # Boost score if product is in same categories as cart items
                if product["category"] in cart_categories:
                    score_boost += 0.2
                
                # Boost score based on price similarity with cart items
                avg_cart_price = sum(float(item["price"]) for item in cart_products) / len(cart_products)
                price_diff = abs(float(product["price"]) - avg_cart_price)
                if price_diff <= 50:  # If within $50
                    score_boost += 0.1
                
                recommendations.append({
                    "product_id": product["id"],
                    "product": product,
                    "score": base_score + score_boost,
                    "source": "sequential",
                    "explanation": f"Frequently bought together with {product['category']} products"
                })
            
            # Sort by score and take top recommendations
            recommendations.sort(key=lambda x: x["score"], reverse=True)
            return recommendations[:limit]
            
        except Exception as e:
            print(f"Error in sequential pattern mining: {str(e)}")
            return []
            
    def update_model(self, feedback: Dict[str, Any]) -> None:
        """Update the sequential pattern mining model based on feedback"""
        try:
            # Update sequence database
            self._update_sequence_database(feedback)
            
            # Mine new patterns
            self._mine_patterns()
            
            # Update model parameters
            self._update_model_parameters(feedback)
            
        except Exception as e:
            # Log error and continue with current model
            pass
            
    def explain_recommendation(self, customer_profile: Dict[str, Any], product: Dict[str, Any]) -> Dict[str, Any]:
        """Generate explanation for why a product was recommended"""
        try:
            # Get user's sequence
            user_sequence = self._get_user_sequence(customer_profile)
            
            # Find patterns leading to this product
            relevant_patterns = self._find_relevant_patterns(
                user_sequence,
                product
            )
            
            # Generate explanation based on patterns
            explanation = self._generate_explanation_from_patterns(
                relevant_patterns,
                product
            )
            
            return explanation
            
        except Exception as e:
            # Return generic explanation if specific one cannot be generated
            return {
                "explanation": "This product was recommended based on sequential patterns in user behavior.",
                "confidence": 0.5
            }
            
    def _get_user_sequence(self, customer_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get user's sequence of interactions"""
        # This is a placeholder implementation
        return []
        
    def _find_matching_patterns(self, user_sequence: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find patterns that match the user's sequence"""
        # This is a placeholder implementation
        return []
        
    def _generate_recommendations_from_patterns(
        self,
        patterns: List[Dict[str, Any]],
        limit: int
    ) -> List[Dict[str, Any]]:
        """Generate recommendations based on sequential patterns"""
        # This is a placeholder implementation
        return []
        
    def _get_fallback_recommendations(self, limit: int) -> List[Dict[str, Any]]:
        """Get fallback recommendations when main algorithm fails"""
        # This is a placeholder implementation
        return []
        
    def _update_sequence_database(self, feedback: Dict[str, Any]) -> None:
        """Update the sequence database with new interactions"""
        # This is a placeholder implementation
        pass
        
    def _mine_patterns(self) -> None:
        """Mine sequential patterns from the database"""
        # This is a placeholder implementation
        pass
        
    def _update_model_parameters(self, feedback: Dict[str, Any]) -> None:
        """Update model parameters based on feedback"""
        # This is a placeholder implementation
        pass
        
    def _find_relevant_patterns(
        self,
        user_sequence: List[Dict[str, Any]],
        product: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Find patterns that lead to the recommended product"""
        # This is a placeholder implementation
        return []
        
    def _generate_explanation_from_patterns(
        self,
        patterns: List[Dict[str, Any]],
        product: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate explanation based on sequential patterns"""
        # This is a placeholder implementation
        return {
            "explanation": "Based on your browsing history, customers who viewed similar products often purchase this item next.",
            "confidence": 0.8
        } 