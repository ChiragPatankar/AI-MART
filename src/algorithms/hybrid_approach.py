from typing import Dict, Any, List
import numpy as np
from .base_recommendation import BaseRecommendationAlgorithm
from .collaborative_filtering import CollaborativeFiltering
from .content_based_filtering import ContentBasedFiltering
from .sequential_pattern_mining import SequentialPatternMining

class HybridApproach(BaseRecommendationAlgorithm):
    def __init__(self):
        super().__init__()
        self.collaborative = CollaborativeFiltering()
        self.content_based = ContentBasedFiltering()
        self.sequential = SequentialPatternMining()
        self.algorithm_weights = {
            "collaborative": 0.4,
            "content_based": 0.3,
            "sequential": 0.3
        }
        
    def generate_recommendations(self, customer_profile: Dict[str, Any], cart_products: List[Dict[str, Any]], product_list: List[Dict[str, Any]], limit: int = 10) -> List[Dict[str, Any]]:
        """Generate recommendations using hybrid approach"""
        try:
            # Generate recommendations based on selected algorithm
            recommendations = []
            cart_categories = set(item["category"] for item in cart_products)
            
            # Filter out products already in cart
            cart_product_ids = set(item["id"] for item in cart_products)
            available_products = [p for p in product_list if p["id"] not in cart_product_ids]
            
            if not available_products:
                return []
                
            # If cart has items, recommend similar products
            if cart_products:
                # Calculate average cart price
                avg_cart_price = sum(float(item["price"]) for item in cart_products) / len(cart_products)
                
                for product in available_products:
                    confidence_factors = []
                    
                    # Category match confidence (0.0 - 1.0)
                    category_confidence = 1.0 if product["category"] in cart_categories else 0.0
                    confidence_factors.append(category_confidence * 0.4)  # 40% weight
                    
                    # Price similarity confidence (0.0 - 1.0)
                    price_diff = abs(float(product["price"]) - avg_cart_price)
                    price_confidence = 1.0 / (1.0 + price_diff/avg_cart_price)
                    confidence_factors.append(price_confidence * 0.3)  # 30% weight
                    
                    # Description similarity confidence (0.0 - 1.0)
                    desc_confidence = 0.0
                    for cart_item in cart_products:
                        common_words = set(product["description"].lower().split()) & set(cart_item["description"].lower().split())
                        if common_words:
                            desc_confidence = max(desc_confidence, len(common_words) / max(len(product["description"].split()), len(cart_item["description"].split())))
                    confidence_factors.append(desc_confidence * 0.3)  # 30% weight
                    
                    # Calculate final confidence score
                    confidence_score = sum(confidence_factors)
                    
                    recommendations.append({
                        "product_id": product["id"],
                        "product": product,
                        "score": confidence_score,
                        "confidence_score": confidence_score,
                        "source": "hybrid",
                        "explanation": self._generate_confidence_explanation(
                            category_confidence,
                            price_confidence,
                            desc_confidence,
                            product,
                            avg_cart_price
                        )
                    })
            else:
                # If cart is empty, use popularity and diversity based confidence
                categories = list(set(p["category"] for p in available_products))
                for idx, product in enumerate(available_products):
                    # Category diversity confidence (favors products from different categories)
                    category_position = categories.index(product["category"])
                    diversity_confidence = 1.0 - (category_position / len(categories))
                    
                    # Position-based confidence (earlier products get higher confidence)
                    position_confidence = 1.0 - (idx / len(available_products))
                    
                    # Calculate final confidence score
                    confidence_score = (diversity_confidence * 0.6) + (position_confidence * 0.4)
                    
                    recommendations.append({
                        "product_id": product["id"],
                        "product": product,
                        "score": confidence_score,
                        "confidence_score": confidence_score,
                        "source": "hybrid",
                        "explanation": f"Popular product in the {product['category']} category"
                    })
            
            # Sort by confidence score and take top recommendations
            recommendations.sort(key=lambda x: x["confidence_score"], reverse=True)
            return recommendations[:limit]
            
        except Exception as e:
            print(f"Error in hybrid recommendations: {str(e)}")
            return []
            
    def update_model(self, feedback: Dict[str, Any]) -> None:
        """Update the hybrid model based on feedback"""
        try:
            # Update individual models
            self.collaborative.update_model(feedback)
            self.content_based.update_model(feedback)
            self.sequential.update_model(feedback)
            
            # Update algorithm weights based on performance
            self._update_algorithm_weights(feedback)
            
        except Exception as e:
            # Log error and continue with current model
            pass
            
    def explain_recommendation(self, customer_profile: Dict[str, Any], product: Dict[str, Any]) -> Dict[str, Any]:
        """Generate explanation for why a product was recommended"""
        try:
            # Get explanations from each algorithm
            collaborative_exp = self.collaborative.explain_recommendation(
                customer_profile,
                product
            )
            content_exp = self.content_based.explain_recommendation(
                customer_profile,
                product
            )
            sequential_exp = self.sequential.explain_recommendation(
                customer_profile,
                product
            )
            
            # Combine explanations
            combined_exp = self._combine_explanations(
                collaborative_exp,
                content_exp,
                sequential_exp
            )
            
            return combined_exp
            
        except Exception as e:
            # Return generic explanation if specific one cannot be generated
            return {
                "explanation": "This product was recommended based on multiple factors including similar customers, content matching, and sequential patterns.",
                "confidence": 0.5
            }
            
    def _combine_recommendations(
        self,
        collaborative_recs: List[Dict[str, Any]],
        content_recs: List[Dict[str, Any]],
        sequential_recs: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Combine recommendations from different algorithms"""
        # This is a placeholder implementation
        combined = []
        
        # Add collaborative recommendations
        for rec in collaborative_recs:
            combined.append({
                "product_id": rec["product_id"],
                "score": rec["score"] * self.algorithm_weights["collaborative"],
                "source": "collaborative"
            })
            
        # Add content-based recommendations
        for rec in content_recs:
            combined.append({
                "product_id": rec["product_id"],
                "score": rec["score"] * self.algorithm_weights["content_based"],
                "source": "content_based"
            })
            
        # Add sequential recommendations
        for rec in sequential_recs:
            combined.append({
                "product_id": rec["product_id"],
                "score": rec["score"] * self.algorithm_weights["sequential"],
                "source": "sequential"
            })
            
        return combined
        
    def _select_top_recommendations(
        self,
        combined_recs: List[Dict[str, Any]],
        limit: int
    ) -> List[Dict[str, Any]]:
        """Select top recommendations from combined list"""
        # This is a placeholder implementation
        # Sort by score and select top limit
        sorted_recs = sorted(combined_recs, key=lambda x: x["score"], reverse=True)
        return sorted_recs[:limit]
        
    def _update_algorithm_weights(self, feedback: Dict[str, Any]) -> None:
        """Update weights of different algorithms based on performance"""
        # This is a placeholder implementation
        pass
        
    def _combine_explanations(
        self,
        collaborative_exp: Dict[str, Any],
        content_exp: Dict[str, Any],
        sequential_exp: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Combine explanations from different algorithms"""
        # This is a placeholder implementation
        return {
            "explanation": "This product was recommended because:\n" +
                         f"1. {collaborative_exp['explanation']}\n" +
                         f"2. {content_exp['explanation']}\n" +
                         f"3. {sequential_exp['explanation']}",
            "confidence": np.mean([
                collaborative_exp["confidence"],
                content_exp["confidence"],
                sequential_exp["confidence"]
            ])
        }
        
    def _get_fallback_recommendations(self, limit: int) -> List[Dict[str, Any]]:
        """Get fallback recommendations when main algorithm fails"""
        # This is a placeholder implementation
        return []
        
    def _generate_confidence_explanation(
        self,
        category_confidence: float,
        price_confidence: float,
        desc_confidence: float,
        product: Dict[str, Any],
        avg_cart_price: float
    ) -> str:
        """Generate detailed explanation based on confidence factors"""
        explanations = []
        
        if category_confidence > 0:
            explanations.append(f"matches your preferred category ({product['category']})")
        
        if price_confidence > 0.7:
            explanations.append(f"is in a similar price range (${avg_cart_price:.2f})")
        elif price_confidence > 0.4:
            explanations.append("is within an acceptable price range")
        
        if desc_confidence > 0.3:
            explanations.append("has similar features to items in your cart")
        
        if not explanations:
            return "Recommended based on general popularity"
        
        return "This product " + ", ".join(explanations) 