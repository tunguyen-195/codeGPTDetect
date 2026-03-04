"""
Clean Dataset - Remove metadata headers that cause data leakage
"""

import os
import re
from pathlib import Path
from tqdm import tqdm

def remove_metadata_header(code: str) -> str:
    """
    Remove metadata headers from code that reveal if it's AI-generated
    
    Patterns to remove:
    - Triple-quoted AI-Generated markers
    - Human-written markers
    - Model/API mentions
    - Any metadata that leaks label information
    """
    
    # Pattern 1: Triple-quoted string at start with AI/Model mentions
    pattern1 = r'^"""\s*(?:AI-Generated|Human-written|Model:|Category:|Difficulty:|Prompt:).*?"""\s*'
    code = re.sub(pattern1, '', code, flags=re.DOTALL | re.MULTILINE)
    
    # Pattern 2: Comments at start mentioning AI/Human
    pattern2 = r'^#.*?(?:AI-Generated|Human-written|Groq|Ollama|Model:).*?\n'
    code = re.sub(pattern2, '', code, flags=re.MULTILINE)
    
    # Pattern 3: Any remaining triple-quoted string at very start (first 500 chars)
    # that contains suspicious keywords
    if code.startswith('"""') or code.startswith("'''"):
        first_part = code[:500]
        if any(keyword in first_part.lower() for keyword in ['ai-generated', 'ai generated', 'groq', 'ollama', 'model:', 'llama', 'gpt', 'human-written']):
            # Find end of docstring
            quote_type = '"""' if code.startswith('"""') else "'''"
            end_pos = code.find(quote_type, 3)
            if end_pos != -1:
                code = code[end_pos + 3:].lstrip()
    
    return code.strip()


def clean_file(filepath: Path) -> bool:
    """Clean a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            original_code = f.read()
        
        cleaned_code = remove_metadata_header(original_code)
        
        # Only write if changed
        if cleaned_code != original_code and len(cleaned_code) > 10:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned_code)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {filepath.name}: {e}")
        return False


def clean_dataset(base_dir: str = "./DATASETS/PYTHON"):
    """Clean all Python files in dataset"""
    
    base_path = Path(base_dir)
    
    directories = [
        base_path / "raw" / "ai",
        base_path / "raw" / "human",
        base_path / "training_data",
        base_path / "testing_data"
    ]
    
    print("="*70)
    print("CLEANING DATASET - REMOVING METADATA HEADERS")
    print("="*70)
    
    total_cleaned = 0
    total_files = 0
    
    for directory in directories:
        if not directory.exists():
            print(f"\nSkipping {directory} (not found)")
            continue
        
        print(f"\nProcessing: {directory}")
        
        files = list(directory.glob("*.py"))
        cleaned_count = 0
        
        for filepath in tqdm(files, desc=f"Cleaning {directory.name}"):
            total_files += 1
            if clean_file(filepath):
                cleaned_count += 1
                total_cleaned += 1
        
        print(f"  Cleaned: {cleaned_count}/{len(files)} files")
    
    print("\n" + "="*70)
    print("CLEANING COMPLETE")
    print("="*70)
    print(f"Total files processed: {total_files}")
    print(f"Total files cleaned: {total_cleaned}")
    print(f"Percentage cleaned: {total_cleaned/total_files*100:.1f}%")
    
    return total_cleaned


def verify_cleaning(base_dir: str = "./DATASETS/PYTHON"):
    """Verify that all metadata has been removed"""
    
    print("\n" + "="*70)
    print("VERIFICATION - CHECKING FOR REMAINING METADATA")
    print("="*70)
    
    base_path = Path(base_dir)
    suspicious_files = []
    
    for directory in [base_path / "training_data", base_path / "testing_data"]:
        if not directory.exists():
            continue
        
        for filepath in directory.glob("*.py"):
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    first_500 = content[:500].lower()
                    
                    # Check for suspicious patterns
                    if any(keyword in first_500 for keyword in [
                        'ai-generated', 'ai generated', 'groq', 'ollama', 
                        'model: llama', 'model: gpt', 'human-written',
                        'category:', 'difficulty:', 'prompt:'
                    ]):
                        suspicious_files.append(filepath)
            except Exception:
                pass
    
    if suspicious_files:
        print(f"\nWARNING: Found {len(suspicious_files)} files with potential metadata:")
        for f in suspicious_files[:10]:  # Show first 10
            print(f"  - {f.name}")
        if len(suspicious_files) > 10:
            print(f"  ... and {len(suspicious_files) - 10} more")
        return False
    else:
        print("\n+ All files clean! No metadata detected.")
        return True


if __name__ == "__main__":
    import sys
    
    print("\n" + "="*70)
    print("DATASET CLEANING TOOL")
    print("="*70)
    print("\nThis script will remove metadata headers that cause data leakage:")
    print("  - AI-Generated markers")
    print("  - Model names (Groq, Ollama, GPT)")
    print("  - Category/Difficulty labels")
    print("  - Prompts used for generation")
    print("\n" + "="*70)
    
    response = input("\nProceed with cleaning? (yes/no): ").strip().lower()
    
    if response not in ['yes', 'y']:
        print("Cancelled.")
        sys.exit(0)
    
    # Clean
    cleaned = clean_dataset()
    
    # Verify
    is_clean = verify_cleaning()
    
    if is_clean and cleaned > 0:
        print("\n" + "="*70)
        print("SUCCESS!")
        print("="*70)
        print("\nDataset is now clean and ready for re-training.")
        print("\nNext steps:")
        print("  1. python train_python_model.py")
        print("  2. Evaluate new model performance")
        print("  3. Compare with previous results")
    elif cleaned == 0:
        print("\nNo files needed cleaning (already clean)")
    else:
        print("\nPlease review suspicious files and re-run")
    
    sys.exit(0 if is_clean else 1)
