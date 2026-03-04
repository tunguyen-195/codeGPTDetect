"""
ML Model Service - Integration with CodeBERT models
Handles loading and inference for Java and Python models
"""

import torch
import logging
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import Dict, Optional, Tuple
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# Get project root directory (parent of app directory)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class MLModelService:
    """Service for managing ML models and predictions"""
    
    def __init__(self):
        self.models = {}
        self.tokenizers = {}
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.loaded = False
        
        # Model paths - use absolute paths from project root
        self.model_paths = {
            "python": str(PROJECT_ROOT / "models" / "python-detector-finetuned"),
            "java": str(PROJECT_ROOT / "models" / "java-detector-finetuned"),
            "base": str(PROJECT_ROOT / "models" / "java-detector-finetuned")  # Fallback to Java model
        }
        
        logger.info(f"ML Service initialized. Device: {self.device}")
        logger.info(f"Project root: {PROJECT_ROOT}")
        logger.info(f"Model paths: {self.model_paths}")
    
    def load_models(self):
        """Load all available models"""
        if self.loaded:
            logger.info("Models already loaded")
            return
        
        logger.info("Loading ML models...")
        
        for model_name, model_path in self.model_paths.items():
            try:
                if os.path.exists(model_path):
                    logger.info(f"Loading {model_name} model from {model_path}")
                    
                    # Load tokenizer
                    tokenizer = AutoTokenizer.from_pretrained(model_path)
                    self.tokenizers[model_name] = tokenizer
                    
                    # Load model
                    model = AutoModelForSequenceClassification.from_pretrained(model_path)
                    model.to(self.device)
                    model.eval()
                    self.models[model_name] = model
                    
                    logger.info(f"✅ {model_name} model loaded successfully")
                else:
                    logger.warning(f"❌ Model path not found: {model_path}")
            except Exception as e:
                logger.error(f"Failed to load {model_name} model: {e}")
        
        if self.models:
            self.loaded = True
            logger.info(f"Loaded {len(self.models)} models: {list(self.models.keys())}")
        else:
            logger.warning("No models were loaded!")
    
    def get_available_models(self) -> list:
        """Get list of available loaded models"""
        return list(self.models.keys())
    
    def predict(
        self,
        code: str,
        model_name: str = "python",
        max_length: int = 512
    ) -> Dict[str, any]:
        """
        Predict if code is AI-generated or Human-written
        
        Args:
            code: Source code to analyze
            model_name: Model to use (python, java, base)
            max_length: Maximum token length
            
        Returns:
            Dictionary with prediction results
        """
        # Load models if not loaded
        if not self.loaded:
            self.load_models()
        
        # Check if model exists
        if model_name not in self.models:
            logger.warning(f"Model {model_name} not available, using fallback")
            # Fallback to first available model
            if self.models:
                model_name = list(self.models.keys())[0]
            else:
                raise ValueError("No models available")
        
        try:
            # Get model and tokenizer
            model = self.models[model_name]
            tokenizer = self.tokenizers[model_name]
            
            # Tokenize input
            inputs = tokenizer(
                code,
                return_tensors="pt",
                max_length=max_length,
                truncation=True,
                padding=True
            )
            
            # Move to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Predict
            with torch.no_grad():
                outputs = model(**inputs)
                logits = outputs.logits
                probabilities = torch.softmax(logits, dim=1)[0]
            
            # Get prediction
            predicted_class = torch.argmax(probabilities).item()
            confidence = probabilities[predicted_class].item()
            
            # Map to labels (0=AI, 1=Human) - matches training data
            labels = ["AI-Generated", "Human-Written"]
            prediction = labels[predicted_class]
            
            # Prepare results
            result = {
                "prediction": prediction,
                "confidence": float(confidence),
                "probabilities": {
                    "AI-Generated": float(probabilities[0]),
                    "Human-Written": float(probabilities[1])
                },
                "model_used": model_name
            }
            
            logger.info(f"Prediction: {prediction} (confidence: {confidence:.2%})")
            return result
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise
    
    def detect_language(self, code: str) -> str:
        """
        Auto-detect programming language from code
        
        Args:
            code: Source code
            
        Returns:
            Detected language (python, java, cpp, etc.)
        """
        code_lower = code.lower()
        
        # Python indicators
        python_indicators = [
            "def ", "import ", "from ", "class ", "if __name__",
            "print(", "self.", ":\n", "elif ", "lambda "
        ]
        
        # Java indicators  
        java_indicators = [
            "public class", "private ", "protected ", "public static void main",
            "System.out", "new ", "extends ", "implements ", "package "
        ]
        
        # C++ indicators
        cpp_indicators = [
            "#include", "int main(", "std::", "cout", "cin",
            "namespace ", "template<", "public:", "private:"
        ]
        
        # Count matches
        python_score = sum(1 for ind in python_indicators if ind in code_lower)
        java_score = sum(1 for ind in java_indicators if ind in code_lower)
        cpp_score = sum(1 for ind in cpp_indicators if ind in code_lower)
        
        # Determine language
        scores = {
            "python": python_score,
            "java": java_score,
            "cpp": cpp_score
        }
        
        detected = max(scores, key=scores.get)
        
        # Default to python if no clear winner
        if scores[detected] == 0:
            detected = "python"
        
        logger.info(f"Language detected: {detected} (scores: {scores})")
        return detected
    
    def analyze_code(
        self,
        code: str,
        language: Optional[str] = None,
        model: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Complete analysis pipeline
        
        Args:
            code: Source code to analyze
            language: Programming language (auto-detect if None)
            model: Model to use (auto-select if None)
            
        Returns:
            Complete analysis results
        """
        # Detect language if not provided
        if not language or language == "auto":
            language = self.detect_language(code)
        
        # Select model if not provided
        if not model or model == "auto":
            # Use language-specific model if available
            model = language if language in self.get_available_models() else "base"
        
        # Run prediction
        result = self.predict(code, model)
        
        # Add language info
        result["language"] = language
        
        return result
    
    def get_model_info(self) -> Dict[str, any]:
        """Get information about loaded models"""
        info = {
            "loaded": self.loaded,
            "device": str(self.device),
            "available_models": self.get_available_models(),
            "model_paths": self.model_paths
        }
        return info


# Global instance
_ml_service = None


def get_ml_service() -> MLModelService:
    """Get or create ML service instance"""
    global _ml_service
    if _ml_service is None:
        _ml_service = MLModelService()
        # Load models on first access
        try:
            _ml_service.load_models()
        except Exception as e:
            logger.error(f"Failed to load models: {e}")
    return _ml_service
