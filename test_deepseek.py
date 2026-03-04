"""
Test DeepSeek API connection
"""
import requests
import json

api_key = "sk-2b5e6fb910f04120aa01ffa4871ef3f2"
endpoint = "https://api.deepseek.com/v1/chat/completions"

print("Testing DeepSeek API...")
print(f"API Key: {api_key[:10]}...{api_key[-6:]}")
print(f"Endpoint: {endpoint}\n")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "deepseek-coder",
    "messages": [
        {
            "role": "system",
            "content": "You are an expert Python programmer."
        },
        {
            "role": "user",
            "content": "Write a simple Python function to calculate factorial. Include docstring."
        }
    ],
    "max_tokens": 500,
    "temperature": 0.7
}

try:
    print("Sending request...")
    response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        code = data["choices"][0]["message"]["content"]
        
        print("\nSUCCESS! DeepSeek API is working!")
        print("\nGenerated Code:")
        print("-" * 60)
        print(code[:300])
        print("-" * 60)
        
        # Check usage
        if "usage" in data:
            usage = data["usage"]
            print(f"\nToken Usage:")
            print(f"  Prompt: {usage.get('prompt_tokens', 'N/A')}")
            print(f"  Completion: {usage.get('completion_tokens', 'N/A')}")
            print(f"  Total: {usage.get('total_tokens', 'N/A')}")
        
        print("\n✓ Ready to generate 875 samples!")
        print("Run: python generate_deepseek.py --num 875 --start 1125")
        
    else:
        print(f"\nERROR: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
