"""
Smart generation with multiple models and keys
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "scripts"))

# Import and modify generator
from generate_ai_code_groq import GroqCodeGenerator

class SmartGenerator(GroqCodeGenerator):
    def __init__(self):
        # Set env key before calling super
        os.environ["GROQ_API_KEY"] = "YOUR_GROQ_API_KEY_HERE"
        super().__init__()
        
        # Multiple API keys (fallback) - 7 keys total!
        self.api_keys = [
            "YOUR_GROQ_API_KEY_HERE",  # Key 1
            "YOUR_GROQ_API_KEY_HERE",  # Key 2
            "YOUR_GROQ_API_KEY_HERE",  # Key 3
            "YOUR_GROQ_API_KEY_HERE",  # Key 4
            "YOUR_GROQ_API_KEY_HERE",  # Key 5
            "YOUR_GROQ_API_KEY_HERE",  # Key 6
            "YOUR_GROQ_API_KEY_HERE",  # Key 7 (old)
        ]
        
        # Multiple models (from smaller to larger)
        self.models = [
            "llama-3.1-8b-instant",      # Fastest, smallest tokens
            "openai/gpt-oss-20b",        # Medium size
            "llama-3.3-70b-versatile",   # Largest, best quality
        ]
        
        self.current_key_index = 0
        self.current_model_index = 0
        
        # Set initial key and model
        self.client.api_key = self.api_keys[0]
        self.model = self.models[0]
        
        print(f"\nUsing Key {self.current_key_index + 1}/{len(self.api_keys)}")
        print(f"Using Model: {self.model}")
    
    def switch_key(self):
        """Switch to next API key"""
        self.current_key_index += 1
        if self.current_key_index >= len(self.api_keys):
            return False  # No more keys
        
        from groq import Groq
        self.client = Groq(api_key=self.api_keys[self.current_key_index])
        print(f"\n>>> Switched to Key {self.current_key_index + 1}/{len(self.api_keys)}")
        return True
    
    def switch_model(self):
        """Switch to next model"""
        self.current_model_index += 1
        if self.current_model_index >= len(self.models):
            return False  # No more models
        
        self.model = self.models[self.current_model_index]
        print(f"\n>>> Switched to Model: {self.model}")
        return True
    
    def generate_code(self, prompt, max_retries=3):
        """Generate with automatic fallback"""
        for attempt in range(max_retries):
            try:
                result = super().generate_code(prompt, max_retries=1)
                if result:
                    return result
                    
            except Exception as e:
                error_str = str(e)
                
                # Check for rate limit
                if "rate_limit_exceeded" in error_str or "429" in error_str:
                    print(f"\n  Rate limit hit on attempt {attempt + 1}")
                    
                    # Try switching model first
                    if self.current_model_index < len(self.models) - 1:
                        if self.switch_model():
                            continue
                    
                    # Then try switching key
                    if self.switch_key():
                        self.current_model_index = 0  # Reset to smallest model
                        self.model = self.models[0]
                        continue
                    
                    print(f"\n  ERROR: All keys and models exhausted!")
                    return None
                
                print(f"  Error: {e}")
        
        return None

def main():
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--num", type=int, default=100)
    parser.add_argument("--start", type=int, default=181)
    args = parser.parse_args()
    
    try:
        print(f"\n{'='*60}")
        print(f"SMART GENERATION - Multi-Key & Multi-Model")
        print(f"{'='*60}")
        print(f"\nGenerating {args.num} samples starting from {args.start}")
        print(f"Available keys: {len(SmartGenerator().api_keys)}")
        print(f"Available models: {len(SmartGenerator().models)}")
        print(f"\n{'='*60}\n")
        
        generator = SmartGenerator()
        success, fail = generator.generate_samples(args.num, args.start)
        
        print(f"\n{'='*60}")
        print(f"SUMMARY")
        print(f"{'='*60}")
        print(f"Success: {success}/{args.num}")
        print(f"Failed: {fail}")
        
        # Count total
        ai_dir = Path("DATASETS/PYTHON/raw/ai")
        total = len(list(ai_dir.glob("*.py"))) if ai_dir.exists() else 0
        print(f"\nTotal AI samples: {total}/2000")
        print(f"Progress: {total/20:.1f}%")
        
        if total >= 2000:
            print("\n SUCCESS! Ready for next step!")
            print("Run: python scripts/prepare_dataset.py")
        else:
            remaining = 2000 - total
            print(f"\nRemaining: {remaining} samples")
            print(f"To continue: python generate_smart.py --num {remaining} --start {total}")
        
        return 0 if success > 0 else 1
        
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
