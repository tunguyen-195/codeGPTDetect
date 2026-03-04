"""
Quick test to verify the fine-tuned model is working
"""
import requests
import json

# Test code snippet
test_code = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Test the function
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
"""

url = "http://localhost:8001/predict"
payload = {"code": test_code}

print("Testing GPTSniffer API...")
print("=" * 60)
print("Code snippet:")
print(test_code)
print("=" * 60)

response = requests.post(url, json=payload)

if response.status_code == 200:
    result = response.json()
    print("\nPrediction Result:")
    print(f"  Label: {result['label']}")
    print(f"  Confidence: {result['confidence']:.4f}")
    print(f"  Model: {result['model_source']}")
    print(f"  Device: {result['device']}")
    print("\nProbabilities:")
    for label, prob in result['probabilities'].items():
        print(f"  {label}: {prob:.4f}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
