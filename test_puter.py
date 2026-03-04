"""
Test Puter.js FREE API
"""
import requests
import json

print("Testing Puter.js FREE API...")
print("NO API KEY NEEDED!\n")

endpoint = "https://api.puter.com/drivers/call"

payload = {
    "interface": "puter-chat-completion",
    "driver": "gpt-4o-mini",
    "method": "complete",
    "args": {
        "messages": [
            {
                "role": "system",
                "content": "You are a Python expert."
            },
            {
                "role": "user",
                "content": "Write a simple Python function to add two numbers. Include docstring."
            }
        ]
    }
}

try:
    print("Sending request...")
    response = requests.post(endpoint, json=payload, timeout=30)
    
    print(f"Status: {response.status_code}\n")
    
    if response.status_code == 200:
        data = response.json()
        print("SUCCESS! Puter.js API works!")
        print("\nResponse structure:")
        print(json.dumps(data, indent=2)[:500])
        
        print("\n" + "="*60)
        print("READY TO GENERATE 875 SAMPLES!")
        print("="*60)
        print("\nRun: python generate_puter.py --num 875 --start 1125")
        print("\nFeatures:")
        print("  - FREE & UNLIMITED")
        print("  - No API key needed")
        print("  - Multiple models available")
        print("  - Auto-switching on rate limits")
        
    else:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"Exception: {e}")
    import traceback
    traceback.print_exc()
