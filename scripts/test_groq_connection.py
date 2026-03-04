"""
Quick test script to verify Groq API connection
"""

import os
import sys

print("=" * 60)
print("TESTING GROQ API CONNECTION")
print("=" * 60)

# Check API key
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    print("\nERROR: GROQ_API_KEY not found!")
    print("\nPlease set it first:")
    print('  PowerShell: $env:GROQ_API_KEY = "gsk_your_key_here"')
    print('  Linux/Mac:  export GROQ_API_KEY="gsk_your_key_here"')
    print("\nGet free key at: https://console.groq.com/keys")
    sys.exit(1)

print(f"\nAPI Key: {api_key[:10]}...{api_key[-4:]}")

# Check groq library
try:
    from groq import Groq
    print("Groq library: OK")
except ImportError:
    print("\nERROR: Groq library not installed!")
    print("Run: pip install groq")
    sys.exit(1)

# Test API connection
print("\nTesting API connection...")
try:
    client = Groq(api_key=api_key)
    
    # Make a simple test call
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Write a simple Python function to add two numbers.",
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        max_tokens=200,
    )
    
    response = chat_completion.choices[0].message.content
    
    print("\nSUCCESS! API is working!")
    print("\nSample response:")
    print("-" * 60)
    print(response[:200] + "..." if len(response) > 200 else response)
    print("-" * 60)
    
    print("\nYou can now run the generation script:")
    print("  python scripts/generate_ai_code_groq.py --num 2000")
    print("\nOr use the PowerShell script:")
    print("  .\\generate_ai_samples.ps1")
    
except Exception as e:
    print(f"\nERROR: API test failed!")
    print(f"Details: {e}")
    print("\nPossible issues:")
    print("  1. Invalid API key")
    print("  2. Network connection problem")
    print("  3. Groq API is down")
    print("\nCheck your API key at: https://console.groq.com/keys")
    sys.exit(1)

print("\n" + "=" * 60)
