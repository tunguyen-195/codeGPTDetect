"""
Script to download and prepare Python dataset from CodeSearchNet
"""

import os
import sys
from pathlib import Path
from datasets import load_dataset
from tqdm import tqdm
import random

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

class PythonDatasetDownloader:
    def __init__(self, output_dir="./DATASETS/PYTHON"):
        self.output_dir = Path(output_dir)
        self.raw_dir = self.output_dir / "raw"
        self.human_dir = self.raw_dir / "human"
        self.ai_dir = self.raw_dir / "ai"
        
        # Create directories
        self.human_dir.mkdir(parents=True, exist_ok=True)
        self.ai_dir.mkdir(parents=True, exist_ok=True)
        
    def download_codesearchnet(self, num_samples=2000):
        """
        Download Python code from CodeSearchNet dataset
        
        Args:
            num_samples: Number of samples to download
        """
        print("=" * 60)
        print("DOWNLOADING CODESEARCHNET PYTHON DATASET")
        print("=" * 60)
        
        try:
            print("\nLoading dataset from HuggingFace...")
            print("This may take a few minutes on first run...")
            
            # Load dataset (using parquet version - no script needed)
            print("Using parquet version from claudios/code_search_net...")
            ds = load_dataset(
                "claudios/code_search_net", 
                "python",
                split="train"
            )
            
            print(f"✓ Dataset loaded: {len(ds)} total samples")
            
            # Shuffle and sample
            print(f"\nSampling {num_samples} random examples...")
            ds_shuffled = ds.shuffle(seed=42)
            samples = ds_shuffled.select(range(min(num_samples, len(ds))))
            
            # Save samples
            print(f"\nSaving samples to {self.human_dir}...")
            
            saved_count = 0
            skipped_count = 0
            
            for idx, sample in enumerate(tqdm(samples)):
                try:
                    # Extract code
                    code = sample.get('func_code_string', '')
                    
                    # Skip if empty or too short
                    if not code or len(code.strip()) < 50:
                        skipped_count += 1
                        continue
                    
                    # Clean code (remove leading/trailing whitespace)
                    code = code.strip()
                    
                    # Create filename with label 1 (human-written)
                    filename = f"1_human_{saved_count:04d}.py"
                    filepath = self.human_dir / filename
                    
                    # Save
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(code)
                    
                    saved_count += 1
                    
                except Exception as e:
                    print(f"\nError processing sample {idx}: {e}")
                    skipped_count += 1
                    continue
            
            print(f"\n✓ Successfully saved {saved_count} samples")
            print(f"⚠ Skipped {skipped_count} samples (empty or error)")
            
            return saved_count
            
        except Exception as e:
            print(f"\n✗ Error downloading dataset: {e}")
            print("\nTroubleshooting:")
            print("1. Check internet connection")
            print("2. Install datasets: pip install datasets")
            print("3. Try: huggingface-cli login (if authentication needed)")
            return 0
    
    def download_humaneval(self):
        """Download OpenAI HumanEval dataset (for testing)"""
        print("\n" + "=" * 60)
        print("DOWNLOADING OPENAI HUMANEVAL DATASET")
        print("=" * 60)
        
        try:
            import urllib.request
            import json
            
            url = "https://github.com/openai/human-eval/raw/master/data/HumanEval.jsonl.gz"
            
            print(f"\nDownloading from: {url}")
            
            # Download
            import gzip
            temp_file = self.raw_dir / "humaneval.jsonl.gz"
            urllib.request.urlretrieve(url, temp_file)
            
            # Extract
            print("Extracting...")
            with gzip.open(temp_file, 'rt') as f:
                data = [json.loads(line) for line in f]
            
            print(f"✓ Downloaded {len(data)} problems")
            
            # Save
            humaneval_dir = self.raw_dir / "humaneval"
            humaneval_dir.mkdir(exist_ok=True)
            
            for idx, problem in enumerate(data):
                code = problem.get('canonical_solution', '')
                if code:
                    filename = f"1_humaneval_{idx:03d}.py"
                    filepath = humaneval_dir / filename
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(code)
            
            # Cleanup
            temp_file.unlink()
            
            print(f"✓ Saved to {humaneval_dir}")
            
            return len(data)
            
        except Exception as e:
            print(f"✗ Error downloading HumanEval: {e}")
            print("This is optional, you can continue without it.")
            return 0
    
    def generate_statistics(self):
        """Generate dataset statistics"""
        print("\n" + "=" * 60)
        print("DATASET STATISTICS")
        print("=" * 60)
        
        # Count files
        human_files = list(self.human_dir.glob("*.py"))
        ai_files = list(self.ai_dir.glob("*.py"))
        
        print(f"\nHuman-written samples: {len(human_files)}")
        print(f"AI-generated samples: {len(ai_files)}")
        print(f"Total samples: {len(human_files) + len(ai_files)}")
        
        # Analyze code lengths
        if human_files:
            lengths = []
            for f in human_files[:100]:  # Sample 100
                with open(f, 'r', encoding='utf-8') as file:
                    lengths.append(len(file.read()))
            
            avg_length = sum(lengths) / len(lengths)
            print(f"\nAverage code length: {avg_length:.0f} characters")
            print(f"Min: {min(lengths)}, Max: {max(lengths)}")
        
        # Next steps
        print("\n" + "=" * 60)
        print("NEXT STEPS")
        print("=" * 60)
        print("\n1. Generate AI samples using ChatGPT:")
        print("   - Run: python scripts/generate_ai_samples.py")
        print("   - Or manually create ~2000 AI samples")
        print(f"   - Save to: {self.ai_dir}")
        print("\n2. Split train/test:")
        print("   - Run: python scripts/split_dataset.py")
        print("\n3. Train model:")
        print("   - Run: python train_python_model.py")

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║    PYTHON DATASET DOWNLOADER FOR T07GPTcodeDetect        ║
║                                                            ║
║    This script downloads human-written Python code        ║
║    from CodeSearchNet dataset for training.               ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    downloader = PythonDatasetDownloader()
    
    # Download CodeSearchNet
    count = downloader.download_codesearchnet(num_samples=2000)
    
    if count > 0:
        print("\n✓ Download successful!")
        
        # Optionally download HumanEval
        try_humaneval = input("\nDownload HumanEval dataset too? (y/n): ").lower()
        if try_humaneval == 'y':
            downloader.download_humaneval()
    else:
        print("\n✗ Download failed. Please check errors above.")
        return
    
    # Show statistics
    downloader.generate_statistics()
    
    print("\n" + "=" * 60)
    print("✓ DATASET DOWNLOAD COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
