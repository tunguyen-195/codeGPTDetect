"""
Quick API Test
Test the multi-language API with various scenarios
"""

import requests
import json

API_URL = "http://localhost:8000"

print("="*70)
print("TESTING GPTSNIFFER MULTI-LANGUAGE API")
print("="*70)

# Test 1: Health check
print("\n1. Health Check")
print("-"*70)
try:
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Service: {data['service']}")
    print(f"Version: {data['version']}")
    print(f"Supported: {', '.join(data['supported_languages']).upper()}")
    print(f"Models: {', '.join(data['available_models']).upper()}")
except Exception as e:
    print(f"ERROR: {e}")

# Test 2: Get available models
print("\n2. Available Models")
print("-"*70)
try:
    response = requests.get(f"{API_URL}/models")
    models = response.json()
    print(f"Status: {response.status_code}")
    print(f"Models available: {json.dumps(models, indent=2)}")
except Exception as e:
    print(f"ERROR: {e}")

# Test 3: Predict with Python code (auto-detect)
print("\n3. Python Code - Auto Language Detection")
print("-"*70)
python_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = [fibonacci(i) for i in range(10)]
print(result)
"""
try:
    response = requests.post(
        f"{API_URL}/predict",
        json={"code": python_code}
    )
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Language: {result.get('language', 'N/A')}")
    print(f"Auto-detected: {result.get('auto_detected', 'N/A')}")
    print(f"Model used: {result.get('model_used', 'N/A')}")
    print(f"Prediction: {result.get('label', 'N/A')}")
    print(f"Confidence: {result.get('confidence', 0)*100:.2f}%")
except Exception as e:
    print(f"ERROR: {e}")

# Test 4: Predict with Java code (explicit language)
print("\n4. Java Code - Explicit Language")
print("-"*70)
java_code = """
public class BubbleSort {
    public static void bubbleSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n-1; i++) {
            for (int j = 0; j < n-i-1; j++) {
                if (arr[j] > arr[j+1]) {
                    int temp = arr[j];
                    arr[j] = arr[j+1];
                    arr[j+1] = temp;
                }
            }
        }
    }
}
"""
try:
    response = requests.post(
        f"{API_URL}/predict",
        json={"code": java_code, "language": "java"}
    )
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Language: {result.get('language', 'N/A')}")
    print(f"Model used: {result.get('model_used', 'N/A')}")
    print(f"Prediction: {result.get('label', 'N/A')}")
    print(f"Confidence: {result.get('confidence', 0)*100:.2f}%")
except Exception as e:
    print(f"ERROR: {e}")

# Test 5: Predict with specific model (Python model)
print("\n5. Code with Explicit Model Selection (Python Model)")
print("-"*70)
try:
    response = requests.post(
        f"{API_URL}/predict",
        json={"code": python_code, "model": "python"}
    )
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Model used: {result.get('model_used', 'N/A')}")
    print(f"Model description: {result.get('model_description', 'N/A')}")
    print(f"Prediction: {result.get('label', 'N/A')}")
    print(f"Confidence: {result.get('confidence', 0)*100:.2f}%")
except Exception as e:
    print(f"ERROR: {e}")

# Test 6: AI-generated style code
print("\n6. AI-Generated Style Code (Detailed Comments)")
print("-"*70)
ai_style_code = '''
"""
Binary Search Tree Implementation
This module provides a complete implementation of a Binary Search Tree
with insert, search, and delete operations.
"""

class TreeNode:
    """
    Represents a node in the binary search tree.
    
    Attributes:
        value (int): The value stored in the node
        left (TreeNode): Reference to left child
        right (TreeNode): Reference to right child
    """
    def __init__(self, value: int) -> None:
        """Initialize a new tree node with given value."""
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    """
    A Binary Search Tree implementation with standard operations.
    """
    def __init__(self) -> None:
        """Initialize an empty BST."""
        self.root = None
    
    def insert(self, value: int) -> None:
        """
        Insert a value into the BST.
        
        Args:
            value: The integer value to insert
        """
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)
'''
try:
    response = requests.post(
        f"{API_URL}/predict",
        json={"code": ai_style_code, "model": "python"}
    )
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Prediction: {result.get('label', 'N/A')}")
    print(f"Confidence: {result.get('confidence', 0)*100:.2f}%")
    print(f"AI Probability: {result.get('probabilities', {}).get('AI-Generated', 0)*100:.2f}%")
    print(f"Human Probability: {result.get('probabilities', {}).get('Human-Written', 0)*100:.2f}%")
except Exception as e:
    print(f"ERROR: {e}")

print("\n" + "="*70)
print("API TESTING COMPLETE")
print("="*70)
print("\nServer is running at: http://localhost:8000")
print("API Documentation: http://localhost:8000/docs")
print("Web UI: http://localhost:8000/ui")
