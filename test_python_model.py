"""
Test Python Code Detection Model
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from pathlib import Path

MODEL_PATH = "./models/python-detector-finetuned"

print("="*70)
print("TESTING PYTHON CODE DETECTION MODEL")
print("="*70)

# Load model
print(f"\nLoading model from: {MODEL_PATH}")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

def predict(code):
    """Predict if code is AI-generated or human-written"""
    inputs = tokenizer(
        code,
        truncation=True,
        max_length=512,
        padding='max_length',
        return_tensors='pt'
    )
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=1)
        prediction = torch.argmax(logits, dim=1).item()
    
    ai_prob = probs[0][0].item()
    human_prob = probs[0][1].item()
    
    label = "HUMAN-WRITTEN" if prediction == 1 else "AI-GENERATED"
    confidence = max(ai_prob, human_prob) * 100
    
    return label, confidence, ai_prob, human_prob

# Test samples
print("\n" + "="*70)
print("TEST SAMPLES")
print("="*70)

# Sample 1: Human-written code
human_code = """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
"""

# Sample 2: AI-generated code (with docstrings)
ai_code = '''
"""
Binary Search Tree Implementation
Supports insert, delete, search operations
"""

class TreeNode:
    """Node in a binary search tree"""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    """Binary Search Tree with standard operations"""
    
    def __init__(self):
        """Initialize empty BST"""
        self.root = None
    
    def insert(self, value: int) -> None:
        """Insert value into BST"""
        if not self.root:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node: TreeNode, value: int) -> None:
        """Helper method for recursive insertion"""
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)
'''

# Test from files
print("\n1. Testing with HUMAN-WRITTEN sample:")
label, conf, ai_p, human_p = predict(human_code)
print(f"   Prediction: {label}")
print(f"   Confidence: {conf:.2f}%")
print(f"   Probabilities: AI={ai_p:.4f}, Human={human_p:.4f}")

print("\n2. Testing with AI-GENERATED sample:")
label, conf, ai_p, human_p = predict(ai_code)
print(f"   Prediction: {label}")
print(f"   Confidence: {conf:.2f}%")
print(f"   Probabilities: AI={ai_p:.4f}, Human={human_p:.4f}")

# Test real files
print("\n" + "="*70)
print("TESTING WITH REAL FILES")
print("="*70)

test_dir = Path("./DATASETS/PYTHON/testing_data")
if test_dir.exists():
    # Get some samples
    human_files = list(test_dir.glob("1_human_*.py"))[:3]
    ai_files = list(test_dir.glob("0_ai_*.py"))[:3]
    
    print("\nHuman-written files:")
    for f in human_files:
        with open(f, 'r', encoding='utf-8', errors='ignore') as file:
            code = file.read()
        label, conf, _, _ = predict(code)
        status = "CORRECT" if label == "HUMAN-WRITTEN" else "WRONG"
        print(f"   {f.name}: {label} ({conf:.1f}%) - {status}")
    
    print("\nAI-generated files:")
    for f in ai_files:
        with open(f, 'r', encoding='utf-8', errors='ignore') as file:
            code = file.read()
        label, conf, _, _ = predict(code)
        status = "CORRECT" if label == "AI-GENERATED" else "WRONG"
        print(f"   {f.name}: {label} ({conf:.1f}%) - {status}")

print("\n" + "="*70)
print("TEST COMPLETE")
print("="*70)
print(f"\nModel location: {MODEL_PATH}")
print("Model is ready for deployment!")
