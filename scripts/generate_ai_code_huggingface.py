"""
Generate AI code samples using FREE Hugging Face Inference API
No API key needed for public models!

Sử dụng các models miễn phí:
1. bigcode/starcoder (16B params - code generation)
2. codellama/CodeLlama-7b-Instruct-hf
3. Salesforce/codegen-350M-mono
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import List, Dict
import requests
from tqdm import tqdm

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

class HuggingFaceCodeGenerator:
    def __init__(self, output_dir="./DATASETS/PYTHON/raw/ai"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Hugging Face Inference API (FREE - no key needed for public models)
        # You can use HF token for faster rate limits (optional)
        self.hf_token = os.environ.get("HF_TOKEN", None)  # Optional
        
        # Free models for code generation
        self.models = [
            "bigcode/starcoder2-3b",  # Small, fast, free
            "Salesforce/codegen-350M-mono",  # Fast, good for simple tasks
            "codellama/CodeLlama-7b-Instruct-hf"  # Good quality
        ]
        
        self.current_model = self.models[0]  # Start with fastest model
        
        # Load problem templates
        self.problem_templates = self.load_problem_templates()
        
    def load_problem_templates(self) -> List[Dict]:
        """Load problem templates for code generation"""
        templates = [
            # Data Structures (100 problems)
            {
                "category": "Data Structures - Trees",
                "prompt": "Write a Python class to implement a Binary Search Tree with insert, delete, and search methods. Include proper docstrings.",
                "difficulty": "medium"
            },
            {
                "category": "Data Structures - Trees",
                "prompt": "Implement an AVL tree in Python with automatic balancing. Include rotation methods.",
                "difficulty": "hard"
            },
            {
                "category": "Data Structures - Stack/Queue",
                "prompt": "Create a Stack class in Python with push, pop, peek, and is_empty methods using a list.",
                "difficulty": "easy"
            },
            {
                "category": "Data Structures - Stack/Queue",
                "prompt": "Implement a Queue class in Python with enqueue, dequeue, and size methods using collections.deque.",
                "difficulty": "easy"
            },
            {
                "category": "Data Structures - Linked List",
                "prompt": "Write a LinkedList class in Python with add, remove, find, and reverse methods.",
                "difficulty": "medium"
            },
            {
                "category": "Data Structures - Linked List",
                "prompt": "Implement a Doubly Linked List in Python with insertions at both ends.",
                "difficulty": "medium"
            },
            {
                "category": "Data Structures - Graph",
                "prompt": "Create a Graph class in Python using adjacency list representation with add_edge and BFS methods.",
                "difficulty": "medium"
            },
            {
                "category": "Data Structures - Heap",
                "prompt": "Implement a Min Heap in Python with insert and extract_min operations.",
                "difficulty": "medium"
            },
            
            # Algorithms - Sorting (50 problems)
            {
                "category": "Algorithms - Sorting",
                "prompt": "Implement QuickSort algorithm in Python to sort a list of integers.",
                "difficulty": "medium"
            },
            {
                "category": "Algorithms - Sorting",
                "prompt": "Write a MergeSort function in Python with in-place sorting optimization.",
                "difficulty": "medium"
            },
            {
                "category": "Algorithms - Sorting",
                "prompt": "Implement HeapSort algorithm in Python using a max heap.",
                "difficulty": "medium"
            },
            {
                "category": "Algorithms - Sorting",
                "prompt": "Create a function for Bubble Sort in Python with early termination optimization.",
                "difficulty": "easy"
            },
            
            # Algorithms - Searching (50 problems)
            {
                "category": "Algorithms - Searching",
                "prompt": "Implement binary search in Python for a sorted list of integers.",
                "difficulty": "easy"
            },
            {
                "category": "Algorithms - Searching",
                "prompt": "Write a function to find the first and last position of a target in a sorted array using binary search.",
                "difficulty": "medium"
            },
            {
                "category": "Algorithms - Searching",
                "prompt": "Implement depth-first search (DFS) for a graph in Python.",
                "difficulty": "medium"
            },
            {
                "category": "Algorithms - Searching",
                "prompt": "Create a breadth-first search (BFS) function for finding shortest path in an unweighted graph.",
                "difficulty": "medium"
            },
            
            # Dynamic Programming (100 problems)
            {
                "category": "Dynamic Programming",
                "prompt": "Solve the 0-1 Knapsack problem using dynamic programming in Python.",
                "difficulty": "hard"
            },
            {
                "category": "Dynamic Programming",
                "prompt": "Implement a function to find the longest common subsequence of two strings using DP.",
                "difficulty": "medium"
            },
            {
                "category": "Dynamic Programming",
                "prompt": "Write a function to calculate Fibonacci numbers using memoization.",
                "difficulty": "easy"
            },
            {
                "category": "Dynamic Programming",
                "prompt": "Solve the coin change problem: minimum coins needed to make amount using DP.",
                "difficulty": "medium"
            },
            
            # String Processing (100 problems)
            {
                "category": "String Processing",
                "prompt": "Write a function to find the longest palindrome substring in a string.",
                "difficulty": "medium"
            },
            {
                "category": "String Processing",
                "prompt": "Implement KMP string matching algorithm in Python.",
                "difficulty": "hard"
            },
            {
                "category": "String Processing",
                "prompt": "Create a function to check if two strings are anagrams.",
                "difficulty": "easy"
            },
            {
                "category": "String Processing",
                "prompt": "Write a function to reverse words in a sentence while preserving spaces.",
                "difficulty": "easy"
            },
            
            # Array/List Processing (100 problems)
            {
                "category": "Array Processing",
                "prompt": "Find the maximum subarray sum using Kadane's algorithm in Python.",
                "difficulty": "medium"
            },
            {
                "category": "Array Processing",
                "prompt": "Implement a function to rotate an array to the right by k positions.",
                "difficulty": "easy"
            },
            {
                "category": "Array Processing",
                "prompt": "Write a function to find all pairs in an array that sum to a target value.",
                "difficulty": "easy"
            },
            {
                "category": "Array Processing",
                "prompt": "Implement merge intervals: given a collection of intervals, merge overlapping ones.",
                "difficulty": "medium"
            },
            
            # Object-Oriented Design (50 problems)
            {
                "category": "OOP Design",
                "prompt": "Design a simple Bank Account class in Python with deposit, withdraw, and balance methods.",
                "difficulty": "easy"
            },
            {
                "category": "OOP Design",
                "prompt": "Implement a Library Management System with Book and Library classes.",
                "difficulty": "medium"
            },
            {
                "category": "OOP Design",
                "prompt": "Create a simple Vehicle hierarchy with Car, Truck, and Motorcycle classes.",
                "difficulty": "easy"
            },
            
            # File I/O (30 problems)
            {
                "category": "File I/O",
                "prompt": "Write a function to read a CSV file and return data as a list of dictionaries.",
                "difficulty": "easy"
            },
            {
                "category": "File I/O",
                "prompt": "Implement a function to write JSON data to a file with proper formatting.",
                "difficulty": "easy"
            },
            
            # Recursion (50 problems)
            {
                "category": "Recursion",
                "prompt": "Write a recursive function to calculate factorial of a number.",
                "difficulty": "easy"
            },
            {
                "category": "Recursion",
                "prompt": "Implement the Tower of Hanoi solution using recursion.",
                "difficulty": "medium"
            },
            {
                "category": "Recursion",
                "prompt": "Create a function to generate all permutations of a string using recursion.",
                "difficulty": "medium"
            },
            
            # Math/Number Theory (50 problems)
            {
                "category": "Math",
                "prompt": "Write a function to check if a number is prime.",
                "difficulty": "easy"
            },
            {
                "category": "Math",
                "prompt": "Implement the Sieve of Eratosthenes to find all primes up to n.",
                "difficulty": "medium"
            },
            {
                "category": "Math",
                "prompt": "Create a function to calculate GCD of two numbers using Euclidean algorithm.",
                "difficulty": "easy"
            },
            
            # Web Scraping/API (20 problems)
            {
                "category": "Web",
                "prompt": "Write a function to fetch data from a REST API and parse JSON response.",
                "difficulty": "easy"
            },
            {
                "category": "Web",
                "prompt": "Implement a simple web scraper using BeautifulSoup to extract titles from a webpage.",
                "difficulty": "medium"
            },
            
            # Database (20 problems)
            {
                "category": "Database",
                "prompt": "Write a Python function to connect to SQLite and execute a SELECT query.",
                "difficulty": "easy"
            },
            {
                "category": "Database",
                "prompt": "Implement CRUD operations for a User table using sqlite3 in Python.",
                "difficulty": "medium"
            },
        ]
        
        # Expand templates to reach 2000+
        expanded = []
        for template in templates:
            expanded.append(template)
            
            # Create variations
            if "implement" in template["prompt"].lower():
                variation = template.copy()
                variation["prompt"] = template["prompt"].replace("Implement", "Create")
                expanded.append(variation)
            
            if "write" in template["prompt"].lower():
                variation = template.copy()
                variation["prompt"] = template["prompt"].replace("Write", "Develop")
                expanded.append(variation)
        
        return expanded[:2000]  # Cap at 2000
    
    def call_huggingface_api(self, prompt: str, max_retries=3) -> str:
        """
        Call Hugging Face Inference API (FREE)
        
        Args:
            prompt: The coding prompt
            max_retries: Number of retries on failure
            
        Returns:
            Generated code as string
        """
        api_url = f"https://api-inference.huggingface.co/models/{self.current_model}"
        
        headers = {}
        if self.hf_token:
            headers["Authorization"] = f"Bearer {self.hf_token}"
        
        # Prepare payload
        payload = {
            "inputs": f"### Instruction:\n{prompt}\n\n### Response:\n",
            "parameters": {
                "max_new_tokens": 512,
                "temperature": 0.7,
                "top_p": 0.95,
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.post(api_url, headers=headers, json=payload, timeout=60)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if isinstance(result, list) and len(result) > 0:
                        generated_code = result[0].get("generated_text", "")
                        return generated_code.strip()
                    elif isinstance(result, dict):
                        return result.get("generated_text", "").strip()
                    
                elif response.status_code == 503:
                    # Model is loading
                    print(f"  Model loading, waiting 20s... (attempt {attempt + 1})")
                    time.sleep(20)
                    continue
                    
                elif response.status_code == 429:
                    # Rate limit
                    print(f"  Rate limited, waiting 10s... (attempt {attempt + 1})")
                    time.sleep(10)
                    continue
                    
                else:
                    print(f"  Error {response.status_code}: {response.text}")
                    time.sleep(5)
                    
            except Exception as e:
                print(f"  Request failed: {e}, retrying...")
                time.sleep(5)
        
        return None
    
    def generate_samples(self, num_samples=2000, start_index=0):
        """
        Generate AI code samples
        
        Args:
            num_samples: Number of samples to generate
            start_index: Starting index (for resuming)
        """
        print("=" * 60)
        print("GENERATING AI CODE SAMPLES USING HUGGING FACE API")
        print("=" * 60)
        print(f"\nUsing model: {self.current_model}")
        print(f"Output directory: {self.output_dir}")
        print(f"Generating {num_samples} samples starting from index {start_index}")
        
        if not self.hf_token:
            print("\n⚠️  WARNING: No HF_TOKEN found. You may hit rate limits.")
            print("   Set HF_TOKEN environment variable for faster access:")
            print("   $env:HF_TOKEN='your_token_here'  (PowerShell)")
            print("   Get free token: https://huggingface.co/settings/tokens")
        
        print("\n" + "=" * 60)
        
        success_count = 0
        fail_count = 0
        
        # Use tqdm for progress bar
        for i in tqdm(range(start_index, min(start_index + num_samples, len(self.problem_templates))), 
                     desc="Generating"):
            
            template = self.problem_templates[i]
            prompt = template["prompt"]
            
            # Generate code
            generated_code = self.call_huggingface_api(prompt)
            
            if generated_code and len(generated_code) > 50:
                # Save to file
                filename = f"0_ai_hf_{i:04d}.py"
                filepath = self.output_dir / filename
                
                # Add metadata as comment
                metadata = f'''"""
AI-Generated Code using Hugging Face Inference API
Model: {self.current_model}
Category: {template["category"]}
Difficulty: {template["difficulty"]}
Prompt: {prompt}
"""

'''
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(metadata + generated_code)
                
                success_count += 1
            else:
                fail_count += 1
                print(f"\n  ⚠️  Failed to generate sample {i}")
            
            # Rate limiting (free tier)
            time.sleep(2)  # 2 seconds between requests
            
            # Save progress every 100 samples
            if (i + 1) % 100 == 0:
                print(f"\n  ✓ Progress: {success_count} succeeded, {fail_count} failed")
        
        print("\n" + "=" * 60)
        print("GENERATION COMPLETE")
        print("=" * 60)
        print(f"✓ Successfully generated: {success_count}")
        print(f"✗ Failed: {fail_count}")
        print(f"📁 Output directory: {self.output_dir}")
        
        return success_count, fail_count

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate AI code samples using Hugging Face")
    parser.add_argument("--num", type=int, default=2000, help="Number of samples to generate")
    parser.add_argument("--start", type=int, default=0, help="Starting index (for resuming)")
    parser.add_argument("--model", type=str, default="bigcode/starcoder2-3b", 
                       help="Hugging Face model name")
    
    args = parser.parse_args()
    
    generator = HuggingFaceCodeGenerator()
    generator.current_model = args.model
    
    success, fail = generator.generate_samples(args.num, args.start)
    
    print(f"\n✓ Total generated: {success}/{args.num}")

if __name__ == "__main__":
    main()
