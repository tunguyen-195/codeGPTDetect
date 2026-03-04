"""
Generate AI code using Puter.js FREE UNLIMITED API
NO API KEY NEEDED! Works instantly!

Puter.js provides free access to 400+ AI models including:
- OpenAI GPT-4.1
- Claude Sonnet
- Google Gemini
- Mistral
- And more!
"""

import os
import sys
import time
import requests
from pathlib import Path
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent / "scripts"))

class PuterGenerator:
    def __init__(self, output_dir="./DATASETS/PYTHON/raw/ai"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Puter.js API endpoint
        self.endpoint = "https://api.puter.com/drivers/call"
        
        # Available models (all FREE!)
        self.models = [
            "gpt-4o-mini",           # OpenAI - Fast & Free
            "claude-3.5-sonnet",     # Anthropic - Smart
            "gemini-2-flash",        # Google - Fast
            "llama-3.3-70b",         # Meta - Open source
            "mistral-large",         # Mistral - Fast
        ]
        
        self.current_model = 0
        
        # Load problem templates
        self.problem_templates = self.load_templates()
        
        print("\n" + "="*60)
        print("PUTER.JS FREE UNLIMITED AI CODE GENERATOR")
        print("="*60)
        print(f"\nNO API KEY NEEDED!")
        print(f"Models available: {len(self.models)}")
        print(f"Current model: {self.models[self.current_model]}")
        print(f"Output: {self.output_dir}")
        print("="*60 + "\n")
    
    def load_templates(self):
        """Simple template loader"""
        templates = []
        
        problems = [
            "Implement a Binary Search Tree with insert, delete, search",
            "Create a Stack class with push, pop, peek operations",
            "Write a Queue using collections.deque",
            "Implement LinkedList with add, remove, reverse",
            "Create Min Heap with insert and extract_min",
            "Write Graph with DFS and BFS methods",
            "Implement Hash Table with chaining",
            "Create AVL Tree with balancing",
            "Write Trie for autocomplete",
            "Implement Priority Queue using heapq",
            "QuickSort with random pivot",
            "MergeSort with optimization",
            "HeapSort using max heap",
            "Binary search for sorted array",
            "DFS for graph traversal",
            "BFS for shortest path",
            "0-1 Knapsack using DP",
            "Longest common subsequence",
            "Dijkstra's shortest path",
            "Coin change problem using DP",
        ]
        
        # Expand to 2000
        while len(templates) < 2000:
            for p in problems:
                if len(templates) >= 2000:
                    break
                templates.append({
                    "prompt": f"Write a Python function to {p.lower()}. Include docstrings and error handling.",
                    "category": "Programming"
                })
        
        return templates
    
    def generate_code(self, prompt, max_retries=3):
        """Generate code using Puter.js API"""
        
        payload = {
            "interface": "puter-chat-completion",
            "driver": self.models[self.current_model],
            "method": "complete",
            "args": {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert Python programmer. Generate clean code with docstrings."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.endpoint,
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extract content from response
                    if isinstance(data, dict):
                        if "message" in data and "content" in data["message"]:
                            return data["message"]["content"]
                        elif "content" in data:
                            return data["content"]
                        elif "choices" in data and len(data["choices"]) > 0:
                            return data["choices"][0]["message"]["content"]
                    
                    print(f"\n  Unexpected response format: {str(data)[:100]}")
                    
                elif response.status_code == 429:
                    # Switch to next model
                    print(f"\n  Rate limit on {self.models[self.current_model]}, switching model...")
                    self.current_model = (self.current_model + 1) % len(self.models)
                    print(f"  Now using: {self.models[self.current_model]}")
                    time.sleep(2)
                    continue
                
                else:
                    print(f"\n  Error {response.status_code}: {response.text[:100]}")
                    time.sleep(2)
                    
            except Exception as e:
                print(f"\n  Exception: {str(e)[:100]}")
                if attempt < max_retries - 1:
                    time.sleep(2)
        
        return None
    
    def generate_samples(self, num_samples, start_index):
        """Generate AI code samples"""
        print(f"Generating {num_samples} samples starting from {start_index}\n")
        
        success = 0
        fail = 0
        
        for i in tqdm(range(start_index, start_index + num_samples), desc="Generating"):
            if i >= len(self.problem_templates):
                break
            
            template = self.problem_templates[i]
            code = self.generate_code(template["prompt"])
            
            if code and len(code) > 50:
                # Clean markdown
                if "```python" in code:
                    code = code.split("```python")[1].split("```")[0].strip()
                elif "```" in code:
                    code = code.split("```")[1].split("```")[0].strip()
                
                # Save
                filename = f"0_ai_puter_{i:04d}.py"
                filepath = self.output_dir / filename
                
                metadata = f'''"""
AI-Generated Code using Puter.js (FREE)
Model: {self.models[self.current_model]}
Category: {template["category"]}
Prompt: {template["prompt"]}
"""

'''
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(metadata + code)
                
                success += 1
            else:
                fail += 1
                print(f"\n  Failed: {i}")
            
            # Small delay
            time.sleep(0.5)
            
            # Progress
            if (i - start_index + 1) % 50 == 0:
                print(f"\n  Progress: {success} succeeded, {fail} failed")
                print(f"  Current model: {self.models[self.current_model]}")
        
        print(f"\n\n{'='*60}")
        print("GENERATION COMPLETE")
        print('='*60)
        print(f"Successfully generated: {success}/{num_samples}")
        print(f"Failed: {fail}")
        
        # Count total
        total = len(list(self.output_dir.glob("*.py")))
        print(f"\nTotal AI samples: {total}/2000")
        print(f"Progress: {total/20:.1f}%")
        
        if total >= 2000:
            print("\nSUCCESS! Ready for next step!")
            print("Run: python scripts/prepare_dataset.py")
        else:
            remaining = 2000 - total
            print(f"\nRemaining: {remaining} samples")
            print(f"Continue: python generate_puter.py --num {remaining} --start {total}")
        
        return success, fail

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate AI code using Puter.js (FREE)")
    parser.add_argument("--num", type=int, default=875, help="Number of samples")
    parser.add_argument("--start", type=int, default=1125, help="Starting index")
    
    args = parser.parse_args()
    
    print("="*60)
    print("PUTER.JS - FREE UNLIMITED AI API")
    print("="*60)
    print("\nFeatures:")
    print("  - NO API KEY needed")
    print("  - FREE & UNLIMITED")
    print("  - 400+ AI models available")
    print("  - Auto-switching between models")
    print("  - Instant access")
    print("="*60 + "\n")
    
    try:
        generator = PuterGenerator()
        success, fail = generator.generate_samples(args.num, args.start)
        
        print(f"\nCompleted: {success}/{args.num} samples")
        return 0 if success > 0 else 1
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
