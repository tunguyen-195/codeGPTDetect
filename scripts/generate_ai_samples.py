"""
Script to generate AI code samples using ChatGPT API or manual prompts
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict
import time

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

class AICodeGenerator:
    def __init__(self, output_dir="./DATASETS/PYTHON/raw/ai"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load problem templates
        self.problem_templates = self.load_problem_templates()
        
    def load_problem_templates(self) -> List[Dict]:
        """Load problem templates for code generation"""
        templates = [
            # Data Structures
            {
                "category": "Data Structures",
                "prompt": "Write a Python class to implement a Binary Search Tree with insert, delete, and search methods. Include proper docstrings and error handling."
            },
            {
                "category": "Data Structures",
                "prompt": "Implement a Stack data structure in Python with push, pop, peek, and is_empty methods. Use a list as the underlying storage."
            },
            {
                "category": "Data Structures",
                "prompt": "Create a Queue class in Python with enqueue, dequeue, and size methods. Implement it using collections.deque."
            },
            {
                "category": "Data Structures",
                "prompt": "Write a LinkedList class in Python with methods to add, remove, and find nodes. Include a method to reverse the list."
            },
            
            # Algorithms - Sorting
            {
                "category": "Sorting",
                "prompt": "Implement the QuickSort algorithm in Python. The function should sort a list of integers in ascending order."
            },
            {
                "category": "Sorting",
                "prompt": "Write a Python function to implement Merge Sort. Include detailed comments explaining the divide-and-conquer approach."
            },
            {
                "category": "Sorting",
                "prompt": "Implement Bubble Sort in Python with an optimization to stop early if the list is already sorted."
            },
            
            # Algorithms - Searching
            {
                "category": "Searching",
                "prompt": "Write a Python function to perform binary search on a sorted list. Return the index if found, -1 otherwise."
            },
            {
                "category": "Searching",
                "prompt": "Implement a function to find all occurrences of a substring in a string using the KMP algorithm in Python."
            },
            
            # Dynamic Programming
            {
                "category": "Dynamic Programming",
                "prompt": "Write a Python function to solve the 0-1 Knapsack problem using dynamic programming. Include docstrings."
            },
            {
                "category": "Dynamic Programming",
                "prompt": "Implement a function to calculate the nth Fibonacci number using memoization in Python."
            },
            {
                "category": "Dynamic Programming",
                "prompt": "Write a Python function to find the Longest Common Subsequence of two strings using dynamic programming."
            },
            
            # String Manipulation
            {
                "category": "String",
                "prompt": "Write a Python function to check if a string is a palindrome. Consider both case-insensitive and case-sensitive versions."
            },
            {
                "category": "String",
                "prompt": "Implement a function in Python to find all anagrams of a word in a list of words."
            },
            {
                "category": "String",
                "prompt": "Write a Python function to reverse words in a sentence while maintaining the word order."
            },
            
            # Array/List Problems
            {
                "category": "Array",
                "prompt": "Write a Python function to find the maximum sum of a contiguous subarray (Kadane's Algorithm)."
            },
            {
                "category": "Array",
                "prompt": "Implement a function to rotate an array to the right by k steps in Python."
            },
            {
                "category": "Array",
                "prompt": "Write a Python function to find the two numbers in an array that sum up to a given target."
            },
            
            # Graph Algorithms
            {
                "category": "Graph",
                "prompt": "Implement Depth-First Search (DFS) for a graph in Python. Use an adjacency list representation."
            },
            {
                "category": "Graph",
                "prompt": "Write a Python function to implement Breadth-First Search (BFS) on a graph."
            },
            {
                "category": "Graph",
                "prompt": "Implement Dijkstra's shortest path algorithm in Python for a weighted graph."
            },
            
            # OOP Concepts
            {
                "category": "OOP",
                "prompt": "Create a Python class hierarchy for a simple banking system with Account, SavingsAccount, and CheckingAccount classes."
            },
            {
                "category": "OOP",
                "prompt": "Implement a Python class for a Student with properties for name, grades, and methods to calculate GPA."
            },
            
            # File Handling
            {
                "category": "File I/O",
                "prompt": "Write a Python function to read a CSV file and return its contents as a list of dictionaries."
            },
            {
                "category": "File I/O",
                "prompt": "Implement a function in Python to write data to a JSON file with proper error handling."
            },
            
            # Recursion
            {
                "category": "Recursion",
                "prompt": "Write a recursive Python function to generate all permutations of a string."
            },
            {
                "category": "Recursion",
                "prompt": "Implement a recursive function in Python to solve the Tower of Hanoi problem."
            },
            
            # More advanced topics
            {
                "category": "Advanced",
                "prompt": "Implement a LRU (Least Recently Used) Cache in Python using OrderedDict."
            },
            {
                "category": "Advanced",
                "prompt": "Write a Python decorator to measure the execution time of a function."
            },
            {
                "category": "Advanced",
                "prompt": "Implement a simple thread-safe Queue in Python using threading.Lock."
            }
        ]
        
        return templates
    
    def generate_manual_instructions(self):
        """Generate instructions for manual code generation"""
        print("\n" + "=" * 60)
        print("MANUAL CODE GENERATION INSTRUCTIONS")
        print("=" * 60)
        
        print("\nYou need to generate ~2000 AI code samples using ChatGPT.")
        print("\nRECOMMENDED APPROACH:")
        print("\n1. Use ChatGPT web interface or API")
        print("2. Use the problem templates below")
        print("3. For each problem:")
        print("   - Copy the prompt")
        print("   - Paste into ChatGPT")
        print("   - Save response as 0_chatgpt_XXXX.py")
        print(f"   - Save to: {self.output_dir}")
        
        print("\n" + "=" * 60)
        print("PROBLEM TEMPLATES")
        print("=" * 60)
        
        # Group by category
        by_category = {}
        for template in self.problem_templates:
            cat = template['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(template['prompt'])
        
        for category, prompts in by_category.items():
            print(f"\n{category} ({len(prompts)} problems):")
            print("-" * 50)
            for i, prompt in enumerate(prompts, 1):
                print(f"{i}. {prompt}")
        
        # Save to file for easy reference
        template_file = self.output_dir.parent / "ai_generation_prompts.txt"
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("ChatGPT PROMPTS FOR AI CODE GENERATION\n")
            f.write("=" * 60 + "\n\n")
            
            for category, prompts in by_category.items():
                f.write(f"\n{'='*60}\n")
                f.write(f"{category}\n")
                f.write(f"{'='*60}\n\n")
                for i, prompt in enumerate(prompts, 1):
                    f.write(f"{i}. {prompt}\n\n")
        
        print(f"\n✓ Prompts saved to: {template_file}")
        
        # Additional variations
        print("\n" + "=" * 60)
        print("GENERATING VARIATIONS")
        print("=" * 60)
        print("\nTo reach 2000 samples, create variations:")
        print("- Different problem parameters")
        print("- Different implementation styles")
        print("- With/without comments")
        print("- Different complexity levels")
        
        print("\nEXAMPLE VARIATIONS:")
        print("1. 'Implement bubble sort for integers'")
        print("2. 'Implement bubble sort for strings'")
        print("3. 'Implement bubble sort with early termination'")
        print("4. 'Implement bubble sort in descending order'")
    
    def generate_using_api(self, api_key: str = None):
        """Generate code using ChatGPT API (if available)"""
        if not api_key:
            print("\n⚠ No API key provided. Use manual generation instead.")
            return False
        
        try:
            import openai
            openai.api_key = api_key
            
            print("\n" + "=" * 60)
            print("GENERATING CODE USING CHATGPT API")
            print("=" * 60)
            
            generated_count = 0
            
            for idx, template in enumerate(self.problem_templates):
                try:
                    print(f"\nGenerating {idx+1}/{len(self.problem_templates)}: {template['category']}")
                    
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a Python programming expert. Generate complete, working Python code."},
                            {"role": "user", "content": template['prompt']}
                        ],
                        temperature=0.7,
                        max_tokens=1000
                    )
                    
                    code = response.choices[0].message.content
                    
                    # Extract code from markdown if present
                    if "```python" in code:
                        code = code.split("```python")[1].split("```")[0].strip()
                    elif "```" in code:
                        code = code.split("```")[1].split("```")[0].strip()
                    
                    # Save
                    filename = f"0_chatgpt_{generated_count:04d}.py"
                    filepath = self.output_dir / filename
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(code)
                    
                    generated_count += 1
                    
                    # Rate limiting
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Error: {e}")
                    continue
            
            print(f"\n✓ Generated {generated_count} samples")
            return True
            
        except ImportError:
            print("\n✗ OpenAI library not installed. Run: pip install openai")
            return False
        except Exception as e:
            print(f"\n✗ Error: {e}")
            return False
    
    def check_existing_samples(self):
        """Check how many AI samples exist"""
        ai_files = list(self.output_dir.glob("0_*.py"))
        return len(ai_files)
    
    def validate_samples(self):
        """Validate AI samples can be parsed"""
        print("\n" + "=" * 60)
        print("VALIDATING AI SAMPLES")
        print("=" * 60)
        
        ai_files = list(self.output_dir.glob("0_*.py"))
        
        if not ai_files:
            print("\n⚠ No AI samples found.")
            return
        
        print(f"\nFound {len(ai_files)} AI samples")
        print("Validating syntax...")
        
        valid_count = 0
        invalid_files = []
        
        for filepath in ai_files:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                # Try to compile (check syntax)
                compile(code, str(filepath), 'exec')
                valid_count += 1
                
            except SyntaxError as e:
                invalid_files.append((filepath.name, str(e)))
        
        print(f"\n✓ Valid: {valid_count}/{len(ai_files)}")
        
        if invalid_files:
            print(f"\n⚠ Invalid files ({len(invalid_files)}):")
            for name, error in invalid_files[:10]:  # Show first 10
                print(f"  - {name}: {error}")

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║    AI CODE SAMPLE GENERATOR FOR T07GPTcodeDetect         ║
║                                                            ║
║    Generate AI code samples using ChatGPT                 ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    generator = AICodeGenerator()
    
    # Check existing samples
    existing_count = generator.check_existing_samples()
    print(f"\nExisting AI samples: {existing_count}")
    
    if existing_count >= 2000:
        print("✓ You already have enough samples!")
        proceed = input("Validate existing samples? (y/n): ").lower()
        if proceed == 'y':
            generator.validate_samples()
        return
    
    print(f"\nTarget: 2000 samples")
    print(f"Remaining: {2000 - existing_count}")
    
    # Choose method
    print("\n" + "=" * 60)
    print("GENERATION METHOD")
    print("=" * 60)
    print("\n1. Manual generation (recommended)")
    print("2. Use ChatGPT API (requires API key)")
    
    choice = input("\nChoose method (1/2): ").strip()
    
    if choice == '2':
        api_key = input("Enter OpenAI API key: ").strip()
        if api_key:
            generator.generate_using_api(api_key)
        else:
            print("No API key provided. Showing manual instructions.")
            generator.generate_manual_instructions()
    else:
        generator.generate_manual_instructions()
    
    # Validate
    validate = input("\nValidate existing samples? (y/n): ").lower()
    if validate == 'y':
        generator.validate_samples()

if __name__ == "__main__":
    main()
