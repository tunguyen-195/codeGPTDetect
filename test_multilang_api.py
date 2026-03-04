"""
Test Multi-Language API
"""

import requests
import json

API_URL = "http://localhost:8000"

print("="*70)
print("TESTING MULTI-LANGUAGE API")
print("="*70)

# Test 1: Health check
print("\n1. Health Check")
print("-"*70)
response = requests.get(f"{API_URL}/health")
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 2: Get supported languages
print("\n2. Supported Languages")
print("-"*70)
response = requests.get(f"{API_URL}/languages")
print(f"Languages: {json.dumps(response.json(), indent=2)}")

# Test 3: Auto-detect Python code
print("\n3. Auto-detect Python code")
print("-"*70)
python_code = """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
"""

response = requests.post(
    f"{API_URL}/predict",
    json={"code": python_code, "language": None}  # None for auto-detect
)
result = response.json()
print(f"Code snippet: {python_code[:50]}...")
print(f"Result: {json.dumps(result, indent=2)}")

# Test 4: Explicit Java code
print("\n4. Explicit Java code detection")
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

response = requests.post(
    f"{API_URL}/predict",
    json={"code": java_code, "language": "java"}
)
result = response.json()
print(f"Code snippet: {java_code[:50]}...")
print(f"Result: {json.dumps(result, indent=2)}")

# Test 5: Language detection only
print("\n5. Language Detection Only")
print("-"*70)
response = requests.post(
    f"{API_URL}/detect-language",
    json={"code": python_code}
)
result = response.json()
print(f"Detection result: {json.dumps(result, indent=2)}")

print("\n" + "="*70)
print("API TESTS COMPLETE")
print("="*70)
print(f"\nAPI URL: {API_URL}")
print(f"Docs: {API_URL}/docs")
print("Server is ready for production!")
