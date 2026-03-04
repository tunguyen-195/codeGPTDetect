"""
Generate AI code samples using FREE Groq API
Groq is MUCH FASTER than Hugging Face and has free tier!

Get free API key at: https://console.groq.com/keys
Free tier: 30 requests/minute, 14,400 requests/day

Models available:
- llama-3.3-70b-versatile (BEST for code)
- llama-3.1-70b-versatile
- mixtral-8x7b-32768
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import List, Dict
from tqdm import tqdm

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("⚠️  Groq library not installed. Run: pip install groq")

class GroqCodeGenerator:
    def __init__(self, output_dir="./DATASETS/PYTHON/raw/ai"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Check for API key
        self.api_key = os.environ.get("GROQ_API_KEY", None)
        
        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY not found!\n"
                "1. Get free API key: https://console.groq.com/keys\n"
                "2. Set environment variable:\n"
                "   PowerShell: $env:GROQ_API_KEY='your_key_here'\n"
                "   Linux/Mac: export GROQ_API_KEY='your_key_here'"
            )
        
        if not GROQ_AVAILABLE:
            raise ImportError("Groq library not installed. Run: pip install groq")
        
        # Initialize client
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"  # Best for code
        
        # Load problem templates
        self.problem_templates = self.load_problem_templates()
        
    def load_problem_templates(self) -> List[Dict]:
        """Load comprehensive problem templates"""
        templates = []
        
        # 1. Data Structures (300 problems)
        data_structures = [
            # Trees
            ("Binary Search Tree with insert, delete, search, and in-order traversal", "medium"),
            ("AVL Tree with automatic balancing and rotation methods", "hard"),
            ("Red-Black Tree implementation with insertion and rebalancing", "hard"),
            ("B-Tree for disk-based storage with insertion and search", "hard"),
            ("Trie (Prefix Tree) for autocomplete functionality", "medium"),
            ("Segment Tree for range queries", "hard"),
            
            # Linked Lists
            ("Singly Linked List with add, remove, find, and reverse", "easy"),
            ("Doubly Linked List with bidirectional traversal", "medium"),
            ("Circular Linked List implementation", "medium"),
            ("Skip List for efficient search operations", "hard"),
            
            # Stacks and Queues
            ("Stack using list with push, pop, peek operations", "easy"),
            ("Queue using collections.deque with enqueue, dequeue", "easy"),
            ("Priority Queue using heapq", "medium"),
            ("Circular Queue with fixed size", "medium"),
            ("Deque (Double-ended Queue) implementation", "easy"),
            
            # Heaps
            ("Min Heap with insert and extract_min operations", "medium"),
            ("Max Heap with heapify operation", "medium"),
            ("Binary Heap with both min and max operations", "medium"),
            
            # Graphs
            ("Graph using adjacency list with DFS and BFS", "medium"),
            ("Graph using adjacency matrix", "medium"),
            ("Directed Graph with cycle detection", "hard"),
            ("Weighted Graph with edge weights", "medium"),
            
            # Hash Tables
            ("Hash Table with separate chaining for collision resolution", "medium"),
            ("Hash Map with open addressing", "hard"),
            ("LRU Cache using OrderedDict", "hard"),
        ]
        
        for desc, difficulty in data_structures:
            templates.append({
                "category": "Data Structures",
                "prompt": f"Write a Python class to implement {desc}. Include docstrings and type hints.",
                "difficulty": difficulty
            })
        
        # 2. Sorting Algorithms (100 problems)
        sorting_algorithms = [
            ("QuickSort with random pivot selection", "medium"),
            ("MergeSort with in-place optimization", "medium"),
            ("HeapSort using max heap", "medium"),
            ("Bubble Sort with early termination", "easy"),
            ("Selection Sort", "easy"),
            ("Insertion Sort with binary search optimization", "medium"),
            ("Counting Sort for integer arrays", "medium"),
            ("Radix Sort for large numbers", "hard"),
            ("Bucket Sort for uniformly distributed data", "medium"),
            ("Shell Sort with custom gap sequence", "hard"),
        ]
        
        for desc, difficulty in sorting_algorithms:
            templates.append({
                "category": "Sorting",
                "prompt": f"Implement {desc} in Python. Handle edge cases and include time complexity analysis in docstring.",
                "difficulty": difficulty
            })
        
        # 3. Searching Algorithms (80 problems)
        searching_algorithms = [
            ("Binary Search for sorted array", "easy"),
            ("Linear Search with sentinel", "easy"),
            ("Interpolation Search for uniformly distributed data", "medium"),
            ("Exponential Search for unbounded arrays", "medium"),
            ("Jump Search for sorted arrays", "medium"),
            ("Ternary Search for unimodal functions", "hard"),
            ("Depth-First Search (DFS) for graphs", "medium"),
            ("Breadth-First Search (BFS) for shortest path", "medium"),
            ("A* Search algorithm for pathfinding", "hard"),
            ("Dijkstra's algorithm for weighted graphs", "hard"),
        ]
        
        for desc, difficulty in searching_algorithms:
            templates.append({
                "category": "Searching",
                "prompt": f"Implement {desc} in Python with clear documentation.",
                "difficulty": difficulty
            })
        
        # 4. Dynamic Programming (200 problems)
        dp_problems = [
            ("0-1 Knapsack problem", "hard"),
            ("Unbounded Knapsack problem", "hard"),
            ("Longest Common Subsequence (LCS)", "medium"),
            ("Longest Increasing Subsequence (LIS)", "medium"),
            ("Edit Distance (Levenshtein Distance)", "hard"),
            ("Coin Change - minimum coins", "medium"),
            ("Coin Change - number of ways", "medium"),
            ("Matrix Chain Multiplication", "hard"),
            ("Rod Cutting problem", "medium"),
            ("Fibonacci with memoization", "easy"),
            ("Climbing Stairs problem", "easy"),
            ("House Robber problem", "medium"),
            ("Maximum Subarray Sum (Kadane)", "medium"),
            ("Palindrome Partitioning", "hard"),
            ("Word Break problem", "medium"),
        ]
        
        for problem, difficulty in dp_problems:
            templates.append({
                "category": "Dynamic Programming",
                "prompt": f"Solve {problem} using dynamic programming in Python with time and space complexity analysis.",
                "difficulty": difficulty
            })
        
        # 5. String Algorithms (150 problems)
        string_problems = [
            ("longest palindrome substring", "medium"),
            ("all permutations of a string", "medium"),
            ("KMP pattern matching algorithm", "hard"),
            ("Rabin-Karp string search", "hard"),
            ("Z-algorithm for pattern matching", "hard"),
            ("Manacher's algorithm for longest palindrome", "hard"),
            ("check if two strings are anagrams", "easy"),
            ("reverse words in a sentence", "easy"),
            ("longest common prefix", "easy"),
            ("string compression (aabbbcc -> a2b3c2)", "medium"),
            ("all substrings of a string", "easy"),
            ("valid parentheses checker", "easy"),
            ("longest substring without repeating characters", "medium"),
        ]
        
        for problem, difficulty in string_problems:
            templates.append({
                "category": "String Processing",
                "prompt": f"Write a Python function to find/implement {problem}. Include edge case handling.",
                "difficulty": difficulty
            })
        
        # 6. Array/List Problems (200 problems)
        array_problems = [
            ("maximum subarray sum (Kadane's algorithm)", "medium"),
            ("rotate array to the right by k positions", "easy"),
            ("find all pairs that sum to target", "easy"),
            ("merge overlapping intervals", "medium"),
            ("find missing number in array 1 to n", "easy"),
            ("find duplicate number in array", "easy"),
            ("two sum problem using hash map", "easy"),
            ("three sum problem", "medium"),
            ("four sum problem", "hard"),
            ("product of array except self", "medium"),
            ("trapping rain water", "hard"),
            ("container with most water", "medium"),
            ("sliding window maximum", "hard"),
            ("find median of two sorted arrays", "hard"),
        ]
        
        for problem, difficulty in array_problems:
            templates.append({
                "category": "Array Processing",
                "prompt": f"Implement a function to {problem} in Python with optimal time complexity.",
                "difficulty": difficulty
            })
        
        # 7. Graph Algorithms (150 problems)
        graph_algorithms = [
            ("Dijkstra's shortest path", "hard"),
            ("Bellman-Ford algorithm", "hard"),
            ("Floyd-Warshall all-pairs shortest path", "hard"),
            ("Kruskal's Minimum Spanning Tree", "hard"),
            ("Prim's Minimum Spanning Tree", "hard"),
            ("Topological Sort using DFS", "medium"),
            ("cycle detection in directed graph", "medium"),
            ("cycle detection in undirected graph", "medium"),
            ("strongly connected components (Kosaraju)", "hard"),
            ("articulation points in graph", "hard"),
            ("bridges in graph", "hard"),
        ]
        
        for algo, difficulty in graph_algorithms:
            templates.append({
                "category": "Graph Algorithms",
                "prompt": f"Implement {algo} in Python with clear explanation.",
                "difficulty": difficulty
            })
        
        # 8. Greedy Algorithms (100 problems)
        greedy_problems = [
            ("Activity Selection problem", "medium"),
            ("Fractional Knapsack", "medium"),
            ("Huffman Coding", "hard"),
            ("Job Sequencing problem", "hard"),
            ("minimum number of platforms required", "medium"),
        ]
        
        for problem, difficulty in greedy_problems:
            templates.append({
                "category": "Greedy Algorithms",
                "prompt": f"Solve {problem} using greedy approach in Python.",
                "difficulty": difficulty
            })
        
        # 9. Object-Oriented Design (120 problems)
        oop_designs = [
            ("Bank Account class with deposit, withdraw, balance", "easy"),
            ("Library Management System with Book, Member, Library classes", "medium"),
            ("Vehicle hierarchy (Car, Truck, Motorcycle)", "easy"),
            ("E-commerce Shopping Cart system", "medium"),
            ("Employee Management System with inheritance", "medium"),
            ("Design a Parking Lot system", "hard"),
            ("Design a Elevator system", "hard"),
            ("LRU Cache implementation", "hard"),
        ]
        
        for design, difficulty in oop_designs:
            templates.append({
                "category": "OOP Design",
                "prompt": f"Design and implement {design} in Python using OOP principles.",
                "difficulty": difficulty
            })
        
        # 10. Recursion (100 problems)
        recursion_problems = [
            ("factorial using recursion", "easy"),
            ("Fibonacci using recursion with memoization", "easy"),
            ("Tower of Hanoi", "medium"),
            ("generate all permutations of string", "medium"),
            ("generate all subsets (power set)", "medium"),
            ("N-Queens problem", "hard"),
            ("Sudoku Solver", "hard"),
        ]
        
        for problem, difficulty in recursion_problems:
            templates.append({
                "category": "Recursion",
                "prompt": f"Write a recursive function to solve {problem} in Python.",
                "difficulty": difficulty
            })
        
        # 11. Math/Number Theory (80 problems)
        math_problems = [
            ("check if a number is prime", "easy"),
            ("Sieve of Eratosthenes for primes up to n", "medium"),
            ("GCD using Euclidean algorithm", "easy"),
            ("LCM of two numbers", "easy"),
            ("power function (x^n) in O(log n)", "medium"),
            ("modular exponentiation", "hard"),
        ]
        
        for problem, difficulty in math_problems:
            templates.append({
                "category": "Math",
                "prompt": f"Implement a function to {problem} in Python.",
                "difficulty": difficulty
            })
        
        # 12. Bit Manipulation (60 problems)
        bit_problems = [
            ("count set bits in integer", "easy"),
            ("check if number is power of 2", "easy"),
            ("find single non-duplicate in array", "medium"),
            ("reverse bits of integer", "medium"),
        ]
        
        for problem, difficulty in bit_problems:
            templates.append({
                "category": "Bit Manipulation",
                "prompt": f"Write a function to {problem} using bit manipulation in Python.",
                "difficulty": difficulty
            })
        
        # 13. File I/O (50 problems)
        file_io_tasks = [
            ("read CSV file and return as list of dictionaries", "easy"),
            ("write data to JSON file with formatting", "easy"),
            ("read large file line by line efficiently", "medium"),
            ("parse and validate XML file", "medium"),
        ]
        
        for task, difficulty in file_io_tasks:
            templates.append({
                "category": "File I/O",
                "prompt": f"Implement a function to {task} in Python.",
                "difficulty": difficulty
            })
        
        # 14. Web/API (40 problems)
        web_tasks = [
            ("fetch data from REST API and parse JSON", "easy"),
            ("web scraper using BeautifulSoup", "medium"),
            ("rate-limited API client", "medium"),
        ]
        
        for task, difficulty in web_tasks:
            templates.append({
                "category": "Web",
                "prompt": f"Write a Python function to {task}.",
                "difficulty": difficulty
            })
        
        # Expand to reach 2000
        while len(templates) < 2000:
            templates.extend(templates[:min(100, 2000 - len(templates))])
        
        return templates[:2000]
    
    def generate_code(self, prompt: str, max_retries=3) -> str:
        """
        Generate code using Groq API
        
        Args:
            prompt: Coding task description
            max_retries: Retry attempts on failure
            
        Returns:
            Generated Python code
        """
        system_message = """You are an expert Python programmer. Generate clean, well-documented Python code.
Include:
- Proper docstrings
- Type hints where appropriate
- Error handling
- Comments explaining complex logic
- Example usage if applicable

Generate ONLY the Python code, no explanations before or after."""

        for attempt in range(max_retries):
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": system_message
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model=self.model,
                    temperature=0.7,
                    max_tokens=2048,
                    top_p=0.9,
                )
                
                generated_code = chat_completion.choices[0].message.content
                return generated_code.strip()
                
            except Exception as e:
                print(f"  Error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                else:
                    return None
        
        return None
    
    def generate_samples(self, num_samples=2000, start_index=0):
        """
        Generate AI code samples
        
        Args:
            num_samples: Number of samples to generate
            start_index: Starting index (for resuming)
        """
        print("=" * 60)
        print("GENERATING AI CODE SAMPLES USING GROQ API")
        print("=" * 60)
        print(f"\nModel: {self.model}")
        print(f"Output: {self.output_dir}")
        print(f"Generating {num_samples} samples from index {start_index}")
        print("\nGroq is FAST - expect ~2 samples/second")
        print("=" * 60)
        
        success_count = 0
        fail_count = 0
        
        for i in tqdm(range(start_index, min(start_index + num_samples, len(self.problem_templates))),
                     desc="Generating"):
            
            template = self.problem_templates[i]
            prompt = template["prompt"]
            
            # Generate code
            generated_code = self.generate_code(prompt)
            
            if generated_code and len(generated_code) > 50:
                # Clean up markdown code blocks if present
                if "```python" in generated_code:
                    generated_code = generated_code.split("```python")[1].split("```")[0].strip()
                elif "```" in generated_code:
                    generated_code = generated_code.split("```")[1].split("```")[0].strip()
                
                # Save to file
                filename = f"0_ai_groq_{i:04d}.py"
                filepath = self.output_dir / filename
                
                # Add metadata
                metadata = f'''"""
AI-Generated Code using Groq API
Model: {self.model}
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
                print(f"\n  WARNING: Failed to generate sample {i}")
            
            # Rate limiting: 30 requests/minute = 1 every 2 seconds
            time.sleep(2.1)
            
            # Progress update
            if (i + 1) % 100 == 0:
                print(f"\n  Progress: {success_count} succeeded, {fail_count} failed")
        
        print("\n" + "=" * 60)
        print("GENERATION COMPLETE")
        print("=" * 60)
        print(f"Successfully generated: {success_count}")
        print(f"Failed: {fail_count}")
        print(f"Output: {self.output_dir}")
        
        return success_count, fail_count

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate AI code using Groq API")
    parser.add_argument("--num", type=int, default=2000, help="Number of samples")
    parser.add_argument("--start", type=int, default=0, help="Starting index")
    
    args = parser.parse_args()
    
    try:
        generator = GroqCodeGenerator()
        success, fail = generator.generate_samples(args.num, args.start)
        print(f"\nTotal: {success}/{args.num}")
    except ValueError as e:
        print(f"\nError: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
