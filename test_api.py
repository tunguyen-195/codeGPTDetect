"""Quick API test without emoji issues"""
import os
import sys

api_key = "YOUR_GROQ_API_KEY_HERE"
os.environ["GROQ_API_KEY"] = api_key

print("=" * 60)
print("TESTING GROQ API")
print("=" * 60)
print(f"\nAPI Key: {api_key[:10]}...{api_key[-4:]}")

try:
    from groq import Groq
    print("Groq library: OK")
except ImportError:
    print("ERROR: pip install groq")
    sys.exit(1)

print("\nTesting API connection...")
try:
    client = Groq(api_key=api_key)
    
    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": "Write a Python function to add two numbers."}],
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        max_tokens=150,
    )
    
    response = completion.choices[0].message.content
    print("\nSUCCESS! API is working!")
    print("\nSample response:")
    print("-" * 60)
    print(response[:200])
    print("-" * 60)
    print("\nReady to generate 2000 samples!")
    
except Exception as e:
    print(f"\nERROR: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
