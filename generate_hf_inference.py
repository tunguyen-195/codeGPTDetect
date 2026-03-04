"""
Generate AI code using HuggingFace Inference API (FREE)
No API key needed for public models!
"""

import os
import sys
import time
import requests
from pathlib import Path
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent / "scripts"))

class HuggingFaceGenerator:
    def __init__(self, output_dir="./DATASETS/PYTHON/raw/ai"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # HuggingFace models (FREE, no key needed for public models)
        self.models = [
            "bigcode/starcoder2-15b",
            "Salesforce/codegen-350M-mono",
            "codellama/CodeLlama-7b-hf",
            "mistralai/Mistral-7B-Instruct-v0.3",
            "meta-llama/Llama-3.2-3B-Instruct",
        ]
        
        self.current_model = 0
        
        # Optional HF token for better rate limits
        self.hf_token = os.environ.get("HF_TOKEN", None)
        
        # Load templates
        self.problem_templates = self.load_templates()
        
        print("\n" + "="*60)
        print("HUGGINGFACE INFERENCE API (FREE)")
        print("="*60)
        print(f"\nModels: {len(self.models)}")
        print(f"Current: {self.models[self.current_model]}")
        print(f"HF Token: {'Yes' if self.hf_token else 'No (rate limited)'}")
        print(f"Output: {self.output_dir}")
        print("="*60 + "\n")
    
    def load_templates(self):
        """Load templates"""
        templates = []
        problems = [
            "binary search tree implementation",
            "stack with push pop operations",
            "queue using deque",
            "linked list with reverse",
            "min heap implementation",
            "graph DFS BFS",
            "hash table with chaining",
            "quicksort algorithm",
            "mergesort algorithm",
            "binary search",
        ]
        
        while len(templates) < 2000:
            for p in problems:
                if len(templates) >= 2000:
                    break
                templates.append({
                    "prompt": f"Write Python code for {p}. Include docstrings.",
                    "category": "Code"
                })
        
        return templates
    
    def generate_code(self, prompt, max_retries=3):
        """Generate code using HF Inference API"""
        
        model = self.models[self.current_model]
        api_url = f"https://api-inference.huggingface.co/models/{model}"
        
        headers = {}
        if self.hf_token:
            headers["Authorization"] = f"Bearer {self.hf_token}"
        
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
                response = requests.post(
                    api_url,
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if isinstance(result, list) and len(result) > 0:
                        return result[0].get("generated_text", "")
                    elif isinstance(result, dict):
                        return result.get("generated_text", "")
                
                elif response.status_code == 503:
                    print(f"\n  Model loading (attempt {attempt + 1}/3)...")
                    time.sleep(20)
                    continue
                
                elif response.status_code == 429:
                    print(f"\n  Rate limit, switching model...")
                    self.current_model = (self.current_model + 1) % len(self.models)
                    print(f"  Now using: {self.models[self.current_model]}")
                    time.sleep(5)
                    continue
                
                else:
                    print(f"\n  Error {response.status_code}")
                    time.sleep(5)
                    
            except Exception as e:
                print(f"\n  Exception: {str(e)[:50]}")
                time.sleep(5)
        
        return None
    
    def generate_samples(self, num_samples, start_index):
        """Generate samples"""
        print(f"Generating {num_samples} samples from {start_index}\n")
        
        success = 0
        fail = 0
        
        for i in tqdm(range(start_index, start_index + num_samples), desc="Generating"):
            if i >= len(self.problem_templates):
                break
            
            template = self.problem_templates[i]
            code = self.generate_code(template["prompt"])
            
            if code and len(code) > 50:
                # Clean
                if "```python" in code:
                    code = code.split("```python")[1].split("```")[0].strip()
                elif "```" in code:
                    code = code.split("```")[1].split("```")[0].strip()
                
                # Save
                filename = f"0_ai_hf_{i:04d}.py"
                filepath = self.output_dir / filename
                
                metadata = f'''"""
AI-Generated via HuggingFace (FREE)
Model: {self.models[self.current_model]}
Prompt: {template["prompt"]}
"""

'''
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(metadata + code)
                
                success += 1
            else:
                fail += 1
            
            time.sleep(2)  # Rate limiting
            
            if (i - start_index + 1) % 25 == 0:
                print(f"\n  Progress: {success}/{i - start_index + 1}")
        
        print(f"\n\n{'='*60}")
        print(f"Success: {success}/{num_samples}")
        print(f"Failed: {fail}")
        
        total = len(list(self.output_dir.glob("*.py")))
        print(f"\nTotal: {total}/2000")
        
        return success, fail

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--num", type=int, default=100)
    parser.add_argument("--start", type=int, default=1125)
    args = parser.parse_args()
    
    print("HuggingFace Inference API (FREE)\n")
    print("TIP: Set HF_TOKEN for better rate limits:")
    print("  Get token: https://huggingface.co/settings/tokens")
    print("  Set: $env:HF_TOKEN='your_token'\n")
    
    generator = HuggingFaceGenerator()
    success, fail = generator.generate_samples(args.num, args.start)
    
    return 0 if success > 0 else 1

if __name__ == "__main__":
    sys.exit(main())
