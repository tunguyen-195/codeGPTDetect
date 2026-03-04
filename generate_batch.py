"""
Batch generation with embedded API key
"""
import os
import sys
from pathlib import Path

# Set API key
os.environ["GROQ_API_KEY"] = "YOUR_GROQ_API_KEY_HERE"

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

# Import and run generator
from generate_ai_code_groq import GroqCodeGenerator

def main():
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--num", type=int, default=50)
    parser.add_argument("--start", type=int, default=0)
    args = parser.parse_args()
    
    try:
        print(f"\nGenerating {args.num} samples starting from {args.start}...\n")
        generator = GroqCodeGenerator()
        success, fail = generator.generate_samples(args.num, args.start)
        
        print(f"\nSuccess: {success}/{args.num}")
        print(f"Failed: {fail}")
        
        # Count total
        ai_dir = Path("DATASETS/PYTHON/raw/ai")
        total = len(list(ai_dir.glob("*.py"))) if ai_dir.exists() else 0
        print(f"\nTotal AI samples: {total}/2000")
        
        if total >= 2000:
            print("\nREADY! Run: python scripts/prepare_dataset.py")
        
        return 0 if success > 0 else 1
        
    except Exception as e:
        print(f"\nError: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
