"""
Multi-Provider AI Code Generator
Uses multiple FREE AI services:
1. Together.AI - $25 free credits
2. DeepSeek - Free tier available
3. Groq - 7 keys already configured
"""

import os
import sys
import requests
import json
import time
from pathlib import Path
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent / "scripts"))

class MultiProviderGenerator:
    def __init__(self, output_dir="./DATASETS/PYTHON/raw/ai"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load problem templates
        self.problem_templates = self.load_templates()
        
        # Provider configurations
        self.providers = [
            {
                "name": "Together.AI",
                "enabled": False,  # Set to True when you get API key
                "api_key": os.environ.get("TOGETHER_API_KEY", ""),
                "endpoint": "https://api.together.xyz/v1/chat/completions",
                "model": "meta-llama/Llama-3.3-70b-chat-hf",
                "max_tokens": 1024,
            },
            {
                "name": "DeepSeek",
                "enabled": False,  # Set to True when you get API key
                "api_key": os.environ.get("DEEPSEEK_API_KEY", ""),
                "endpoint": "https://api.deepseek.com/v1/chat/completions",
                "model": "deepseek-coder",
                "max_tokens": 1024,
            },
            # Groq already configured in other script
        ]
        
        self.current_provider = 0
        
        print("\n" + "="*60)
        print("MULTI-PROVIDER CODE GENERATOR")
        print("="*60)
        print("\nAvailable Providers:")
        for i, p in enumerate(self.providers):
            status = "✓ Enabled" if p["enabled"] and p["api_key"] else "✗ Disabled (no key)"
            print(f"  {i+1}. {p['name']}: {status}")
        
    def load_templates(self):
        """Load problem templates - same as before"""
        templates = []
        
        # Categories with problem counts
        categories = {
            "Data Structures": 300,
            "Sorting Algorithms": 100,
            "Searching Algorithms": 80,
            "Dynamic Programming": 200,
            "String Processing": 150,
            "Array Processing": 200,
            "Graph Algorithms": 150,
            "Greedy Algorithms": 100,
            "OOP Design": 120,
            "Recursion": 100,
            "Math": 80,
            "Bit Manipulation": 60,
            "File I/O": 50,
            "Web": 40,
        }
        
        # Simple template generation
        for category, count in categories.items():
            for i in range(count):
                templates.append({
                    "category": category,
                    "prompt": f"Write a Python function for {category.lower()} problem #{i+1}. Include docstrings and error handling.",
                    "difficulty": "medium"
                })
        
        return templates[:2000]
    
    def call_together_ai(self, prompt):
        """Call Together.AI API"""
        provider = self.providers[0]
        
        headers = {
            "Authorization": f"Bearer {provider['api_key']}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": provider["model"],
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert Python programmer. Generate clean, well-documented code with docstrings."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": provider["max_tokens"],
            "temperature": 0.7
        }
        
        try:
            response = requests.post(provider["endpoint"], headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                print(f"  Error {response.status_code}: {response.text[:100]}")
                return None
        except Exception as e:
            print(f"  Exception: {e}")
            return None
    
    def call_deepseek(self, prompt):
        """Call DeepSeek API"""
        provider = self.providers[1]
        
        headers = {
            "Authorization": f"Bearer {provider['api_key']}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": provider["model"],
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert Python programmer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": provider["max_tokens"],
            "temperature": 0.7
        }
        
        try:
            response = requests.post(provider["endpoint"], headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                print(f"  Error {response.status_code}: {response.text[:100]}")
                return None
        except Exception as e:
            print(f"  Exception: {e}")
            return None
    
    def generate_code(self, prompt):
        """Generate code using available providers"""
        # Try Together.AI
        if self.providers[0]["enabled"] and self.providers[0]["api_key"]:
            code = self.call_together_ai(prompt)
            if code:
                return code, "Together.AI"
        
        # Try DeepSeek
        if self.providers[1]["enabled"] and self.providers[1]["api_key"]:
            code = self.call_deepseek(prompt)
            if code:
                return code, "DeepSeek"
        
        return None, None
    
    def generate_samples(self, num_samples, start_index):
        """Generate samples"""
        print(f"\nGenerating {num_samples} samples starting from {start_index}\n")
        
        success = 0
        fail = 0
        
        for i in tqdm(range(start_index, start_index + num_samples), desc="Generating"):
            if i >= len(self.problem_templates):
                break
            
            template = self.problem_templates[i]
            code, provider = self.generate_code(template["prompt"])
            
            if code:
                # Clean markdown
                if "```python" in code:
                    code = code.split("```python")[1].split("```")[0].strip()
                elif "```" in code:
                    code = code.split("```")[1].split("```")[0].strip()
                
                # Save
                filename = f"0_ai_multi_{i:04d}.py"
                filepath = self.output_dir / filename
                
                metadata = f'''"""
AI-Generated Code
Provider: {provider}
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
            
            time.sleep(1)  # Rate limiting
        
        print(f"\n\nSuccess: {success}/{num_samples}")
        print(f"Failed: {fail}")
        
        # Count total
        total = len(list(self.output_dir.glob("*.py")))
        print(f"\nTotal AI samples: {total}/2000")
        
        return success, fail

def main():
    print("="*60)
    print("SETUP INSTRUCTIONS")
    print("="*60)
    print("\n1. Together.AI - Free $25 credits:")
    print("   - Visit: https://api.together.xyz/signup")
    print("   - Get API key")
    print("   - Set: $env:TOGETHER_API_KEY='your_key'")
    
    print("\n2. DeepSeek - Free tier:")
    print("   - Visit: https://platform.deepseek.com/")
    print("   - Get API key")
    print("   - Set: $env:DEEPSEEK_API_KEY='your_key'")
    
    print("\n3. Enable providers in code and run")
    print("="*60)
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--num", type=int, default=100)
    parser.add_argument("--start", type=int, default=1125)
    args = parser.parse_args()
    
    generator = MultiProviderGenerator()
    
    # Check if any provider is enabled
    enabled = any(p["enabled"] for p in generator.providers)
    if not enabled:
        print("\nWARNING: No providers enabled!")
        print("Please set API keys and enable providers in the code.")
        return 1
    
    generator.generate_samples(args.num, args.start)
    return 0

if __name__ == "__main__":
    sys.exit(main())
