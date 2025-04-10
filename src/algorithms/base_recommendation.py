from abc import ABC, abstractmethod
from typing import Dict, Any, List
import numpy as np

class BaseRecommendationAlgorithm(ABC):
    def __init__(self):
        self.model = None
        self.parameters = {}
        
    @abstractmethod
    def generate_recommendations(self, customer_profile: Dict[str, Any], limit: int = 10) -> List[Dict[str, Any]]:
        """Generate recommendations for a customer"""
        pass
        
    @abstractmethod
    def update_model(self, feedback: Dict[str, Any]) -> None:
        """Update the recommendation model based on feedback"""
        pass
        
    @abstractmethod
    def explain_recommendation(self, customer_profile: Dict[str, Any], product: Dict[str, Any]) -> Dict[str, Any]:
        """Generate explanation for why a product was recommended"""
        pass
        
    def preprocess_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Preprocess input data for the algorithm"""
        # This is a placeholder implementation
        # In a real system, you would implement actual preprocessing
        return data
        
    def postprocess_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Postprocess recommendation results"""
        # This is a placeholder implementation
        # In a real system, you would implement actual postprocessing
        return results
        
    def calculate_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate similarity between two vectors"""
        # This is a placeholder implementation
        # In a real system, you would implement actual similarity calculation
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        
    def validate_input(self, data: Dict[str, Any]) -> bool:
        """Validate input data"""
        # This is a placeholder implementation
        # In a real system, you would implement actual validation
        return True
        
    def get_model_parameters(self) -> Dict[str, Any]:
        """Get current model parameters"""
        return self.parameters
        
    def set_model_parameters(self, parameters: Dict[str, Any]) -> None:
        """Set model parameters"""
        self.parameters.update(parameters)
        
    def save_model(self, filepath: str) -> None:
        """Save the model to a file"""
        # This is a placeholder implementation
        # In a real system, you would implement actual model saving
        pass
        
    def load_model(self, filepath: str) -> None:
        """Load the model from a file"""
        # This is a placeholder implementation
        # In a real system, you would implement actual model loading
        pass 