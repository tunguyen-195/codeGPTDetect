"""
Check available models on Groq
"""
import os

# Try both keys
keys = [
    "YOUR_GROQ_API_KEY_HERE",  # Old
    "YOUR_GROQ_API_KEY_HERE",  # New
]

try:
    from groq import Groq
    
    for i, key in enumerate(keys):
        print(f"\n{'='*60}")
        print(f"Testing Key {i+1}: {key[:10]}...{key[-4:]}")
        print('='*60)
        
        try:
            client = Groq(api_key=key)
            
            # List models
            models = client.models.list()
            
            print("\nAvailable Models:")
            for model in models.data:
                print(f"\n  ID: {model.id}")
                if hasattr(model, 'context_window'):
                    print(f"  Context: {model.context_window} tokens")
                if hasattr(model, 'owned_by'):
                    print(f"  Owner: {model.owned_by}")
            
            # Test with smaller model
            print(f"\n\nTesting generation with llama-3.1-8b-instant (smaller, faster)...")
            completion = client.chat.completions.create(
                messages=[{"role": "user", "content": "Write a Python function to add two numbers"}],
                model="llama-3.1-8b-instant",
                max_tokens=100,
            )
            print(f"SUCCESS! Response: {completion.choices[0].message.content[:100]}...")
            
        except Exception as e:
            print(f"ERROR: {e}")
            
except ImportError:
    print("ERROR: groq not installed")
