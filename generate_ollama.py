"""
Generate AI code using LOCAL Ollama
100% FREE, UNLIMITED, NO API KEY!

Available models on your system:
- deepseek-coder:33b (BEST for coding - 18GB)
- deepseek-coder:6.7b-instruct (Good, faster)
- qwen2.5:7b (Excellent)
- llama3.1:8b (Fast)
- gpt-oss:20b (OpenAI model)
"""

import os
import sys
import time
import requests
from pathlib import Path
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent / "scripts"))

class OllamaGenerator:
    def __init__(self, output_dir="./DATASETS/PYTHON/raw/ai"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Ollama local endpoint
        self.endpoint = "http://localhost:11434/api/generate"
        
        # Recommended models (best to worst for coding)
        self.models = [
            "deepseek-coder:33b",      # BEST but slow
            "qwen2.5:7b",              # Excellent, faster
            "deepseek-coder:6.7b",     # Good, fast
            "llama3.1:8b",             # Fast
        ]
        
        self.current_model = 1  # Start with qwen2.5:7b (good balance)
        
        # Load templates
        self.problem_templates = self.load_templates()
        
        print("\n" + "="*60)
        print("OLLAMA LOCAL AI CODE GENERATOR")
        print("="*60)
        print(f"\n+ 100% FREE & UNLIMITED")
        print(f"+ NO API KEY NEEDED")
        print(f"+ Runs on YOUR computer")
        print(f"\nModel: {self.models[self.current_model]}")
        print(f"Available models: {len(self.models)}")
        print(f"Output: {self.output_dir}")
        print("="*60 + "\n")
    
    def load_templates(self):
        """Load problem templates"""
        templates = []
        
        base_problems = [
            "Binary Search Tree with insert, delete, search, and in-order traversal",
            "Stack class using list with push, pop, peek, and is_empty methods",
            "Queue using collections.deque with enqueue, dequeue, and size",
            "LinkedList with add, remove, find, and reverse methods",
            "Min Heap with insert and extract_min operations",
            "Graph using adjacency list with DFS and BFS traversal",
            "Hash Table with separate chaining for collision resolution",
            "AVL Tree with automatic balancing and rotation methods",
            "Trie (Prefix Tree) for autocomplete functionality",
            "Priority Queue using heapq",
            "QuickSort algorithm with random pivot selection",
            "MergeSort with in-place optimization",
            "HeapSort using max heap",
            "Binary search in sorted array",
            "Depth-first search for graph traversal",
            "Breadth-first search for shortest path",
            "0-1 Knapsack problem using dynamic programming",
            "Longest common subsequence using DP",
            "Dijkstra's shortest path algorithm",
            "Coin change problem using DP",
            "Longest increasing subsequence",
            "Edit distance (Levenshtein Distance)",
            "Matrix chain multiplication",
            "Rod cutting problem",
            "House robber problem",
            "Longest palindrome substring",
            "KMP pattern matching algorithm",
            "Check if two strings are anagrams",
            "Reverse words in a sentence",
            "All permutations of a string",
        ]
        
        # Expand to 2000
        while len(templates) < 2000:
            for p in base_problems:
                if len(templates) >= 2000:
                    break
                templates.append({
                    "prompt": f"Write a Python class or function to implement: {p}. Include proper docstrings, type hints, and error handling.",
                    "category": "Programming"
                })
        
        return templates
    
    def generate_code(self, prompt, max_retries=2):
        """Generate code using Ollama"""
        
        system_prompt = "You are an expert Python programmer. Generate clean, well-documented code with docstrings and type hints. Focus on correctness and best practices."
        
        full_prompt = f"### System:\n{system_prompt}\n\n### User:\n{prompt}\n\n### Assistant:\n"
        
        payload = {
            "model": self.models[self.current_model],
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 1024,
            }
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.endpoint,
                    json=payload,
                    timeout=120  # Longer timeout for local model
                )
                
                if response.status_code == 200:
                    data = response.json()
                    code = data.get("response", "")
                    return code.strip()
                
                else:
                    print(f"\n  Error {response.status_code}: {response.text[:100]}")
                    if attempt < max_retries - 1:
                        time.sleep(2)
                        
            except requests.exceptions.Timeout:
                print(f"\n  Timeout (attempt {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    time.sleep(1)
                    
            except Exception as e:
                print(f"\n  Exception: {str(e)[:100]}")
                if attempt < max_retries - 1:
                    time.sleep(2)
        
        return None
    
    def generate_samples(self, num_samples, start_index):
        """Generate AI code samples"""
        print(f"Generating {num_samples} samples starting from {start_index}\n")
        print(f"Using: {self.models[self.current_model]}")
        print(f"This will take approximately {num_samples * 5 / 60:.1f} minutes\n")
        
        success = 0
        fail = 0
        
        start_time = time.time()
        
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
                    parts = code.split("```")
                    if len(parts) >= 2:
                        code = parts[1].strip()
                
                # Remove common prefixes
                if code.startswith("python"):
                    code = code[6:].strip()
                
                # Save
                filename = f"0_ai_ollama_{i:04d}.py"
                filepath = self.output_dir / filename
                
                metadata = f'''"""
AI-Generated Code using Ollama (LOCAL)
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
            
            # Progress report every 50
            if (i - start_index + 1) % 50 == 0:
                elapsed = time.time() - start_time
                avg_time = elapsed / (i - start_index + 1)
                remaining = (num_samples - (i - start_index + 1)) * avg_time
                
                print(f"\n  Progress: {success} succeeded, {fail} failed")
                print(f"  Speed: {avg_time:.1f}s per sample")
                print(f"  ETA: {remaining/60:.1f} minutes")
        
        elapsed_total = time.time() - start_time
        
        print(f"\n\n{'='*60}")
        print("GENERATION COMPLETE")
        print('='*60)
        print(f"Successfully generated: {success}/{num_samples}")
        print(f"Failed: {fail}")
        print(f"Time taken: {elapsed_total/60:.1f} minutes")
        print(f"Average: {elapsed_total/max(success,1):.1f}s per sample")
        
        # Count total
        total = len(list(self.output_dir.glob("*.py")))
        print(f"\nTotal AI samples: {total}/2000")
        print(f"Progress: {total/20:.1f}%")
        
        if total >= 2000:
            print("\n+ SUCCESS! All 2000 samples generated!")
            print("\nNext step:")
            print("  python scripts/prepare_dataset.py")
        else:
            remaining = 2000 - total
            print(f"\nRemaining: {remaining} samples")
            print(f"Continue with:")
            print(f"  python generate_ollama.py --num {remaining} --start {total}")
        
        return success, fail

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate AI code using LOCAL Ollama")
    parser.add_argument("--num", type=int, default=827, help="Number of samples to generate")
    parser.add_argument("--start", type=int, default=1173, help="Starting index")
    parser.add_argument("--model", type=str, default="qwen2.5:7b", help="Model to use")
    
    args = parser.parse_args()
    
    print("="*60)
    print("OLLAMA LOCAL CODE GENERATOR")
    print("="*60)
    print("\n+ 100% FREE & UNLIMITED")
    print("+ NO API KEY")
    print("+ NO RATE LIMITS")
    print("+ Runs offline on your computer")
    print("\nAvailable models:")
    print("  - deepseek-coder:33b (best quality, slower)")
    print("  - qwen2.5:7b (excellent, fast) <-- DEFAULT")
    print("  - deepseek-coder:6.7b (good, faster)")
    print("  - llama3.1:8b (fastest)")
    print("="*60 + "\n")
    
    # Check if Ollama is running
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code != 200:
            print("ERROR: Ollama is not running!")
            print("\nStart Ollama first:")
            print("  Windows: Ollama should auto-start")
            print("  Or run: ollama serve")
            return 1
    except Exception as e:
        print("ERROR: Cannot connect to Ollama!")
        print(f"Details: {e}")
        print("\nMake sure Ollama is running:")
        print("  1. Check if Ollama service is started")
        print("  2. Or run: ollama serve")
        return 1
    
    try:
        generator = OllamaGenerator()
        
        # Update model if specified
        if args.model in generator.models:
            generator.current_model = generator.models.index(args.model)
        
        success, fail = generator.generate_samples(args.num, args.start)
        
        print(f"\n+ Completed: {success}/{args.num} samples")
        return 0 if success > 0 else 1
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
