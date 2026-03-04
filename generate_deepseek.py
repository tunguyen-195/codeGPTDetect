"""
Generate AI code using DeepSeek API
DeepSeek is specialized for coding and very affordable!
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent / "scripts"))

class DeepSeekGenerator:
    def __init__(self, output_dir="./DATASETS/PYTHON/raw/ai"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # DeepSeek API configuration
        self.api_key = "sk-2b5e6fb910f04120aa01ffa4871ef3f2"
        self.endpoint = "https://api.deepseek.com/v1/chat/completions"
        self.model = "deepseek-coder"  # Specialized for code
        
        # Load problem templates
        self.problem_templates = self.load_templates()
        
        print("\n" + "="*60)
        print("DEEPSEEK AI CODE GENERATOR")
        print("="*60)
        print(f"\nModel: {self.model}")
        print(f"API: DeepSeek (specialized for coding)")
        print(f"Output: {self.output_dir}")
        print("="*60 + "\n")
    
    def load_templates(self):
        """Load coding problem templates"""
        templates = []
        
        # Problem categories
        problems = [
            # Data Structures (300)
            *[f"Implement a Binary Search Tree in Python with insert, delete, search methods" for _ in range(20)],
            *[f"Create a Stack class in Python using list with push, pop, peek operations" for _ in range(15)],
            *[f"Write a Queue implementation in Python using collections.deque" for _ in range(15)],
            *[f"Implement a LinkedList class with add, remove, reverse methods" for _ in range(20)],
            *[f"Create a Min Heap in Python with insert and extract_min operations" for _ in range(15)],
            *[f"Implement a Graph using adjacency list with DFS and BFS methods" for _ in range(20)],
            *[f"Write a Hash Table with separate chaining for collision resolution" for _ in range(15)],
            *[f"Create an AVL Tree with automatic balancing and rotation" for _ in range(15)],
            *[f"Implement a Trie (Prefix Tree) for autocomplete functionality" for _ in range(15)],
            *[f"Write a Priority Queue using heapq in Python" for _ in range(15)],
            
            # Algorithms (500)
            *[f"Implement QuickSort algorithm in Python with random pivot" for _ in range(20)],
            *[f"Write MergeSort with in-place optimization" for _ in range(20)],
            *[f"Create HeapSort using max heap implementation" for _ in range(15)],
            *[f"Implement binary search for sorted array" for _ in range(15)],
            *[f"Write depth-first search (DFS) for graph traversal" for _ in range(15)],
            *[f"Implement breadth-first search (BFS) for shortest path" for _ in range(15)],
            *[f"Solve 0-1 Knapsack problem using dynamic programming" for _ in range(25)],
            *[f"Find longest common subsequence (LCS) using DP" for _ in range(20)],
            *[f"Implement Dijkstra's shortest path algorithm" for _ in range(20)],
            *[f"Write solution for coin change problem using DP" for _ in range(20)],
            *[f"Find longest increasing subsequence using DP" for _ in range(15)],
            *[f"Solve edit distance (Levenshtein) problem" for _ in range(15)],
            *[f"Implement matrix chain multiplication using DP" for _ in range(15)],
            *[f"Write rod cutting problem solution" for _ in range(15)],
            *[f"Solve house robber problem using DP" for _ in range(15)],
            
            # String Problems (200)
            *[f"Find longest palindrome substring in a string" for _ in range(20)],
            *[f"Implement KMP pattern matching algorithm" for _ in range(15)],
            *[f"Check if two strings are anagrams" for _ in range(10)],
            *[f"Reverse words in a sentence preserving spaces" for _ in range(10)],
            *[f"Find all permutations of a string" for _ in range(15)],
            *[f"Implement string compression (aabbbcc -> a2b3c2)" for _ in range(10)],
            *[f"Find longest substring without repeating characters" for _ in range(15)],
            *[f"Check valid parentheses in string" for _ in range(10)],
            *[f"Find longest common prefix in array of strings" for _ in range(10)],
            *[f"Implement Rabin-Karp string search" for _ in range(15)],
            
            # Array Problems (200)
            *[f"Find maximum subarray sum using Kadane's algorithm" for _ in range(15)],
            *[f"Rotate array to the right by k positions" for _ in range(10)],
            *[f"Find all pairs in array that sum to target" for _ in range(10)],
            *[f"Merge overlapping intervals" for _ in range(15)],
            *[f"Find missing number in array 1 to n" for _ in range(10)],
            *[f"Solve two sum problem using hash map" for _ in range(10)],
            *[f"Find three sum combinations" for _ in range(15)],
            *[f"Calculate product of array except self" for _ in range(10)],
            *[f"Solve trapping rain water problem" for _ in range(15)],
            *[f"Find container with most water" for _ in range(10)],
            
            # OOP Design (150)
            *[f"Design a Bank Account class with deposit, withdraw, balance" for _ in range(15)],
            *[f"Implement a Library Management System" for _ in range(15)],
            *[f"Create a Vehicle hierarchy (Car, Truck, Motorcycle)" for _ in range(10)],
            *[f"Design a Shopping Cart system" for _ in range(15)],
            *[f"Implement an Employee Management System" for _ in range(15)],
            *[f"Design a Parking Lot system" for _ in range(15)],
            *[f"Create an LRU Cache implementation" for _ in range(15)],
            *[f"Design an Elevator system" for _ in range(10)],
            
            # Other categories (450)
            *[f"Write recursive function for factorial" for _ in range(10)],
            *[f"Implement Fibonacci with memoization" for _ in range(10)],
            *[f"Solve Tower of Hanoi problem" for _ in range(10)],
            *[f"Generate all subsets (power set)" for _ in range(10)],
            *[f"Solve N-Queens problem" for _ in range(15)],
            *[f"Check if number is prime" for _ in range(10)],
            *[f"Implement Sieve of Eratosthenes" for _ in range(10)],
            *[f"Calculate GCD using Euclidean algorithm" for _ in range(10)],
            *[f"Implement power function in O(log n)" for _ in range(10)],
            *[f"Count set bits in integer" for _ in range(10)],
            *[f"Check if number is power of 2" for _ in range(10)],
            *[f"Read CSV file and return as list of dicts" for _ in range(10)],
            *[f"Write JSON data to file with formatting" for _ in range(10)],
            *[f"Fetch data from REST API and parse JSON" for _ in range(10)],
            *[f"Implement web scraper using BeautifulSoup" for _ in range(10)],
        ]
        
        # Convert to template format
        for i, problem in enumerate(problems[:2000]):
            templates.append({
                "category": "Programming",
                "prompt": f"{problem}. Include proper docstrings, type hints, and error handling.",
                "difficulty": "medium"
            })
        
        return templates
    
    def generate_code(self, prompt, max_retries=3):
        """Generate code using DeepSeek API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert Python programmer. Generate clean, well-documented code with docstrings and type hints. Include error handling where appropriate."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 2048,
            "temperature": 0.7,
            "stream": False
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.endpoint,
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    data = response.json()
                    code = data["choices"][0]["message"]["content"]
                    return code.strip()
                
                elif response.status_code == 429:
                    print(f"\n  Rate limit, waiting... (attempt {attempt + 1})")
                    time.sleep(5)
                    continue
                
                else:
                    print(f"\n  Error {response.status_code}: {response.text[:100]}")
                    time.sleep(2)
                    
            except Exception as e:
                print(f"\n  Exception: {e}")
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
                # Clean markdown code blocks
                if "```python" in code:
                    code = code.split("```python")[1].split("```")[0].strip()
                elif "```" in code:
                    code = code.split("```")[1].split("```")[0].strip()
                
                # Save to file
                filename = f"0_ai_deepseek_{i:04d}.py"
                filepath = self.output_dir / filename
                
                # Add metadata
                metadata = f'''"""
AI-Generated Code using DeepSeek
Model: {self.model}
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
            
            # Rate limiting
            time.sleep(1)
            
            # Progress report
            if (i - start_index + 1) % 50 == 0:
                print(f"\n  Progress: {success} succeeded, {fail} failed")
        
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
            print("\n✓ SUCCESS! All 2000 samples generated!")
            print("Next step: python scripts/prepare_dataset.py")
        else:
            remaining = 2000 - total
            print(f"\nRemaining: {remaining} samples")
            print(f"To continue: python generate_deepseek.py --num {remaining} --start {total}")
        
        return success, fail

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate AI code using DeepSeek")
    parser.add_argument("--num", type=int, default=875, help="Number of samples to generate")
    parser.add_argument("--start", type=int, default=1125, help="Starting index")
    
    args = parser.parse_args()
    
    try:
        generator = DeepSeekGenerator()
        success, fail = generator.generate_samples(args.num, args.start)
        
        print(f"\n✓ Completed: {success}/{args.num} samples")
        return 0 if success > 0 else 1
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
