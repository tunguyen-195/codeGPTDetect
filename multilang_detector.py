"""
Multi-Language Code Detector
Supports: Java, Python (C++ ready)
"""

import os
import re
import torch
from typing import Dict, Any, Optional
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class MultiLanguageDetector:
    """Unified detector for multiple programming languages"""
    
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.models = {}
        self.tokenizers = {}
        
        # Model paths - 3 options
        self.model_paths = {
            'base': 'microsoft/codebert-base',  # Base model (not fine-tuned)
            'java': 'models/java-detector-finetuned',  # Java fine-tuned
            'python': 'models/python-detector-finetuned',  # Python fine-tuned
            # 'cpp': 'models/cpp-detector-xxx',  # Reserved for future
        }
        
        # Model descriptions
        self.model_descriptions = {
            'base': 'CodeBERT Base (Chưa fine-tune, dùng cho mọi ngôn ngữ)',
            'java': 'Java Detector (Fine-tuned cho Java code)',
            'python': 'Python Detector (Fine-tuned cho Python, 100% accuracy)'
        }
        
        self.labels = {0: "AI-Generated", 1: "Human-Written"}
        
        print("="*70)
        print("MULTI-LANGUAGE CODE DETECTOR")
        print("="*70)
        print(f"Device: {self.device}")
        
        # Load all available models
        self._load_models()
    
    def _load_models(self):
        """Load all available language models"""
        for lang, model_path in self.model_paths.items():
            full_path = Path(model_path)
            
            if not full_path.exists():
                print(f"\nWARNING: {lang.upper()} model not found at {model_path}")
                continue
            
            try:
                print(f"\nLoading {lang.upper()} model...")
                tokenizer = AutoTokenizer.from_pretrained(str(full_path))
                model = AutoModelForSequenceClassification.from_pretrained(str(full_path))
                model.to(self.device)
                model.eval()
                
                self.tokenizers[lang] = tokenizer
                self.models[lang] = model
                
                print(f"  + {lang.upper()} model loaded successfully")
                
            except Exception as e:
                print(f"  X Error loading {lang.upper()} model: {e}")
        
        print(f"\n+ Loaded {len(self.models)} language models")
        print(f"  Supported languages: {', '.join(self.models.keys()).upper()}")
        print("="*70 + "\n")
    
    def detect_language(self, code: str) -> str:
        """
        Auto-detect programming language from code
        Returns: 'java', 'python', 'cpp', or 'unknown'
        """
        code = code.strip()
        
        # Python indicators
        python_patterns = [
            r'\bdef\s+\w+\s*\(',  # def function(
            r'\bclass\s+\w+\s*:',  # class Name:
            r'\bimport\s+\w+',  # import module
            r'\bfrom\s+\w+\s+import',  # from x import y
            r'\bif\s+__name__\s*==\s*["\']__main__["\']',  # if __name__ == "__main__"
            r'^\s*#.*$',  # Python comments
            r'\bprint\s*\(',  # print()
        ]
        
        # Java indicators
        java_patterns = [
            r'\bpublic\s+class\s+\w+',  # public class Name
            r'\bprivate\s+\w+\s+\w+',  # private type var
            r'\bprotected\s+\w+\s+\w+',  # protected
            r'\bstatic\s+void\s+main',  # static void main
            r'\bSystem\.out\.print',  # System.out.print
            r'\bpublic\s+static\s+',  # public static
            r'^\s*//.*$',  # Java comments
            r'\bpackage\s+\w+',  # package declaration
        ]
        
        # C++ indicators
        cpp_patterns = [
            r'#include\s*<\w+>',  # #include <iostream>
            r'\bstd::\w+',  # std::cout
            r'\busing\s+namespace\s+std',  # using namespace std
            r'\bint\s+main\s*\(',  # int main(
            r'\bcout\s*<<',  # cout <<
            r'\bcin\s*>>',  # cin >>
        ]
        
        # Count matches
        python_score = sum(1 for p in python_patterns if re.search(p, code, re.MULTILINE))
        java_score = sum(1 for p in java_patterns if re.search(p, code, re.MULTILINE))
        cpp_score = sum(1 for p in cpp_patterns if re.search(p, code, re.MULTILINE))
        
        # Determine language
        scores = {'python': python_score, 'java': java_score, 'cpp': cpp_score}
        max_lang = max(scores, key=scores.get)
        max_score = scores[max_lang]
        
        if max_score == 0:
            return 'unknown'
        
        return max_lang
    
    @torch.inference_mode()
    def predict(
        self, 
        code: str, 
        language: Optional[str] = None,
        model: Optional[str] = None,  # New: explicit model selection
        max_length: int = 512
    ) -> Dict[str, Any]:
        """
        Predict if code is AI-generated or human-written
        
        Args:
            code: Source code to analyze
            language: Programming language ('java', 'python', or None for auto-detect)
            model: Explicit model selection ('base', 'java', 'python', or None for auto-select)
            max_length: Maximum token length
            
        Returns:
            Dictionary with prediction results
        """
        if not code or not code.strip():
            raise ValueError("Empty code input")
        
        # Auto-detect language if not specified
        if language is None:
            language = self.detect_language(code)
            auto_detected = True
        else:
            language = language.lower()
            auto_detected = False
        
        # Determine which model to use
        if model is not None:
            # Explicit model selection
            model_key = model.lower()
            if model_key not in self.models:
                return {
                    "error": f"Model '{model}' not supported or not loaded",
                    "available_models": list(self.models.keys())
                }
        else:
            # Auto-select model based on language
            if language in self.models:
                model_key = language
            else:
                # Fallback to first available model
                model_key = list(self.models.keys())[0]
        
        # Check if selected model exists
        if model_key not in self.models:
            return {
                "error": f"Model '{model_key}' not loaded",
                "supported_languages": list(self.models.keys()),
                "available_models": list(self.models.keys()),
                "detected_language": language if auto_detected else None
            }
        
        # Get model and tokenizer
        model = self.models[model_key]
        tokenizer = self.tokenizers[model_key]
        
        # Tokenize and predict
        inputs = tokenizer(
            code,
            padding="max_length",
            truncation=True,
            max_length=max_length,
            return_tensors="pt",
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        outputs = model(**inputs)
        logits = outputs.logits.detach().cpu()
        probs = torch.softmax(logits, dim=-1).squeeze(0)
        
        # Get prediction
        ai_prob = float(probs[0])
        human_prob = float(probs[1])
        predicted_class = 0 if ai_prob > human_prob else 1
        label = self.labels[predicted_class]
        confidence = max(ai_prob, human_prob)
        
        return {
            "label": label,
            "confidence": float(confidence),
            "probabilities": {
                "AI-Generated": ai_prob,
                "Human-Written": human_prob
            },
            "language": language.upper() if language else "UNKNOWN",
            "auto_detected": auto_detected,
            "model_used": model_key,
            "model_description": self.model_descriptions.get(model_key, model_key),
            "device": str(self.device)
        }
    
    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        return list(self.models.keys())
    
    def is_language_supported(self, language: str) -> bool:
        """Check if language is supported"""
        return language.lower() in self.models


# Singleton instance
_detector = None

def get_detector() -> MultiLanguageDetector:
    """Get or create detector instance"""
    global _detector
    if _detector is None:
        _detector = MultiLanguageDetector()
    return _detector


if __name__ == "__main__":
    # Test the detector
    detector = get_detector()
    
    print("\nTEST 1: Auto-detect Python code")
    print("-" * 70)
    python_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
    result = detector.predict(python_code)
    print(f"Code: {python_code[:50]}...")
    print(f"Detected Language: {result['language']}")
    print(f"Prediction: {result['label']}")
    print(f"Confidence: {result['confidence']:.2%}")
    
    print("\nTEST 2: Auto-detect Java code")
    print("-" * 70)
    java_code = """
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
"""
    result = detector.predict(java_code)
    print(f"Code: {java_code[:50]}...")
    print(f"Detected Language: {result['language']}")
    print(f"Prediction: {result['label']}")
    print(f"Confidence: {result['confidence']:.2%}")
    
    print("\nTEST 3: Explicit language specification")
    print("-" * 70)
    result = detector.predict(python_code, language='python')
    print(f"Specified Language: PYTHON")
    print(f"Prediction: {result['label']}")
    print(f"Confidence: {result['confidence']:.2%}")
    
    print("\n" + "="*70)
    print(f"Supported Languages: {', '.join(detector.get_supported_languages()).upper()}")
    print("="*70)
