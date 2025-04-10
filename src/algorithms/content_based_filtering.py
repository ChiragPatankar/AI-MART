from typing import Dict, Any, List
import numpy as np
from .base_recommendation import BaseRecommendationAlgorithm

class ContentBasedFiltering(BaseRecommendationAlgorithm):
    def __init__(self):
        super().__init__()
        self.product_features = None
        self.feature_weights = None
        self.tfidf_vectorizer = None
        
    def generate_recommendations(self, customer_profile: Dict[str, Any], cart_products: List[Dict[str, Any]], product_list: List[Dict[str, Any]], limit: int = 10) -> List[Dict[str, Any]]:
        """Generate recommendations using content-based filtering"""
        try:
            recommendations = []
            
            # If cart is empty, recommend diverse products
            if not cart_products:
                # Get unique categories
                categories = set(p["category"] for p in product_list)
                for category in categories:
                    category_products = [p for p in product_list if p["category"] == category]
                    if category_products:
                        recommendations.append({
                            "product_id": category_products[0]["id"],
                            "product": category_products[0],
                            "score": 0.7,
                            "source": "content_based",
                            "explanation": f"Featured product in {category}"
                        })
                        if len(recommendations) >= limit:
                            break
                return recommendations[:limit]
            
            # Get average price from cart items
            avg_cart_price = sum(float(item["price"]) for item in cart_products) / len(cart_products)
            
            # Filter out products already in cart
            cart_product_ids = set(item["id"] for item in cart_products)
            available_products = [p for p in product_list if p["id"] not in cart_product_ids]
            
            # Find products with similar attributes
            for product in available_products:
                # Calculate price similarity
                price_diff = abs(float(product["price"]) - avg_cart_price)
                price_score = 1 / (1 + price_diff/100)  # Normalize price difference
                
                recommendations.append({
                    "product_id": product["id"],
                    "product": product,
                    "score": price_score,
                    "source": "content_based",
                    "explanation": f"Similar to your preferred price range (${avg_cart_price:.2f})"
                })
            
            # Sort by score and take top recommendations
            recommendations.sort(key=lambda x: x["score"], reverse=True)
            return recommendations[:limit]
            
        except Exception as e:
            print(f"Error in content-based filtering: {str(e)}")
            return []
            
    def update_model(self, feedback: Dict[str, Any]) -> None:
        """Update the content-based filtering model based on feedback"""
        try:
            # Update user preferences
            self._update_user_preferences(feedback)
            
            # Update feature weights
            self._update_feature_weights(feedback)
            
            # Update TF-IDF vectorizer if needed
            self._update_vectorizer(feedback)
            
        except Exception as e:
            # Log error and continue with current model
            pass
            
    def explain_recommendation(self, customer_profile: Dict[str, Any], product: Dict[str, Any]) -> Dict[str, Any]:
        """Generate explanation for why a product was recommended"""
        try:
            # Extract product features
            product_features = self._extract_product_features(product)
            
            # Get user preferences
            user_preferences = self._extract_user_preferences(customer_profile)
            
            # Generate explanation based on feature matching
            explanation = self._generate_explanation_from_features(
                product_features,
                user_preferences
            )
            
            return explanation
            
        except Exception as e:
            # Return generic explanation if specific one cannot be generated
            return {
                "explanation": "This product matches your preferences based on its features.",
                "confidence": 0.5
            }
            
    def _extract_user_preferences(self, customer_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Extract user preferences from profile"""
        # This is a placeholder implementation
        return {
            "categories": [],
            "attributes": {},
            "price_range": None
        }
        
    def _get_product_features(self) -> Dict[str, Any]:
        """Get product features from database"""
        # This is a placeholder implementation
        return {}
        
    def _calculate_content_similarity(
        self,
        user_preferences: Dict[str, Any],
        product_features: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Calculate similarity between user preferences and product features"""
        # This is a placeholder implementation
        return []
        
    def _generate_recommendations_from_similarity(
        self,
        similarities: List[Dict[str, Any]],
        limit: int
    ) -> List[Dict[str, Any]]:
        """Generate recommendations based on content similarity"""
        # This is a placeholder implementation
        return []
        
    def _get_fallback_recommendations(self, limit: int) -> List[Dict[str, Any]]:
        """Get fallback recommendations when main algorithm fails"""
        # This is a placeholder implementation
        return []
        
    def _update_user_preferences(self, feedback: Dict[str, Any]) -> None:
        """Update user preferences based on feedback"""
        # This is a placeholder implementation
        pass
        
    def _update_feature_weights(self, feedback: Dict[str, Any]) -> None:
        """Update feature weights based on feedback"""
        # This is a placeholder implementation
        pass
        
    def _update_vectorizer(self, feedback: Dict[str, Any]) -> None:
        """Update TF-IDF vectorizer based on feedback"""
        # This is a placeholder implementation
        pass
        
    def _extract_product_features(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features from product data"""
        # This is a placeholder implementation
        return {}
        
    def _generate_explanation_from_features(
        self,
        product_features: Dict[str, Any],
        user_preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate explanation based on feature matching"""
        # This is a placeholder implementation
        return {
            "explanation": "This product matches your preferences in the following ways...",
            "confidence": 0.8
        } 