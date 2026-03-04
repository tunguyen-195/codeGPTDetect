"""
Prepare dataset: Split raw data into training and testing sets

This script:
1. Validates raw data (human + AI samples)
2. Removes invalid/empty files
3. Splits into train/test (80/20)
4. Generates dataset statistics
"""

import os
import sys
from pathlib import Path
import shutil
import random
from typing import List, Tuple
import ast

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

class DatasetPreparer:
    def __init__(self, language="python"):
        self.language = language.upper()
        self.base_dir = Path(f"./DATASETS/{self.language}")
        
        self.raw_dir = self.base_dir / "raw"
        self.human_dir = self.raw_dir / "human"
        self.ai_dir = self.raw_dir / "ai"
        
        self.train_dir = self.base_dir / "training_data"
        self.test_dir = self.base_dir / "testing_data"
        
        # File extension
        self.ext = ".py" if language == "python" else ".cpp"
        
    def validate_python_file(self, filepath: Path) -> bool:
        """
        Validate Python file
        
        Checks:
        - File is not empty
        - File contains valid Python syntax
        - File has reasonable length (20-10000 lines)
        
        Returns:
            True if valid, False otherwise
        """
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Check empty
            if len(content.strip()) < 50:
                return False
            
            # Check line count
            lines = content.split('\n')
            if len(lines) < 5 or len(lines) > 10000:
                return False
            
            # Check valid Python syntax
            try:
                ast.parse(content)
            except SyntaxError:
                # Some syntax errors are OK (e.g., incomplete code)
                # But check if it at least has some Python keywords
                python_keywords = ['def ', 'class ', 'import ', 'if ', 'for ', 'while ']
                if not any(keyword in content for keyword in python_keywords):
                    return False
            
            return True
            
        except Exception as e:
            print(f"  WARNING: Error validating {filepath.name}: {e}")
            return False
    
    def validate_cpp_file(self, filepath: Path) -> bool:
        """
        Validate C++ file
        
        Basic checks:
        - File not empty
        - Contains C++ indicators
        - Reasonable length
        """
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if len(content.strip()) < 50:
                return False
            
            lines = content.split('\n')
            if len(lines) < 5 or len(lines) > 10000:
                return False
            
            # Check for C++ indicators
            cpp_indicators = ['#include', 'int main', 'std::', 'namespace', 'class ']
            if not any(indicator in content for indicator in cpp_indicators):
                return False
            
            return True
            
        except Exception:
            return False
    
    def validate_dataset(self) -> Tuple[List[Path], List[Path]]:
        """
        Validate all raw data files
        
        Returns:
            (valid_human_files, valid_ai_files)
        """
        print("=" * 60)
        print("VALIDATING DATASET")
        print("=" * 60)
        
        # Get validator
        validator = self.validate_python_file if self.language == "PYTHON" else self.validate_cpp_file
        
        # Validate human files
        print(f"\nValidating human-written code in {self.human_dir}...")
        human_files = list(self.human_dir.glob(f"*{self.ext}"))
        valid_human = [f for f in human_files if validator(f)]
        
        print(f"  Total: {len(human_files)}")
        print(f"  Valid: {len(valid_human)}")
        print(f"  Invalid: {len(human_files) - len(valid_human)}")
        
        # Validate AI files
        print(f"\nValidating AI-generated code in {self.ai_dir}...")
        ai_files = list(self.ai_dir.glob(f"*{self.ext}"))
        valid_ai = [f for f in ai_files if validator(f)]
        
        print(f"  Total: {len(ai_files)}")
        print(f"  Valid: {len(valid_ai)}")
        print(f"  Invalid: {len(ai_files) - len(valid_ai)}")
        
        return valid_human, valid_ai
    
    def split_dataset(self, human_files: List[Path], ai_files: List[Path], 
                     train_ratio=0.8, random_seed=42) -> None:
        """
        Split files into train/test sets
        
        Args:
            human_files: List of human file paths
            ai_files: List of AI file paths
            train_ratio: Ratio of training data (default 0.8)
            random_seed: Random seed for reproducibility
        """
        print("\n" + "=" * 60)
        print("SPLITTING DATASET")
        print("=" * 60)
        
        # Set random seed
        random.seed(random_seed)
        
        # Shuffle
        random.shuffle(human_files)
        random.shuffle(ai_files)
        
        # Calculate split points
        human_split = int(len(human_files) * train_ratio)
        ai_split = int(len(ai_files) * train_ratio)
        
        # Split
        human_train = human_files[:human_split]
        human_test = human_files[human_split:]
        
        ai_train = ai_files[:ai_split]
        ai_test = ai_files[ai_split:]
        
        print(f"\nTrain/Test Split: {train_ratio:.0%}/{(1-train_ratio):.0%}")
        print(f"\nHuman-written:")
        print(f"  Train: {len(human_train)}")
        print(f"  Test:  {len(human_test)}")
        print(f"\nAI-generated:")
        print(f"  Train: {len(ai_train)}")
        print(f"  Test:  {len(ai_test)}")
        print(f"\nTotal:")
        print(f"  Train: {len(human_train) + len(ai_train)}")
        print(f"  Test:  {len(human_test) + len(ai_test)}")
        
        # Create directories
        self.train_dir.mkdir(parents=True, exist_ok=True)
        self.test_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy files to train
        print(f"\nCopying training files to {self.train_dir}...")
        for f in human_train:
            shutil.copy2(f, self.train_dir / f.name)
        for f in ai_train:
            shutil.copy2(f, self.train_dir / f.name)
        
        # Copy files to test
        print(f"Copying test files to {self.test_dir}...")
        for f in human_test:
            shutil.copy2(f, self.test_dir / f.name)
        for f in ai_test:
            shutil.copy2(f, self.test_dir / f.name)
        
        print("\n+ Dataset split complete!")
    
    def generate_statistics(self) -> None:
        """Generate dataset statistics"""
        print("\n" + "=" * 60)
        print("DATASET STATISTICS")
        print("=" * 60)
        
        # Count files
        train_files = list(self.train_dir.glob(f"*{self.ext}"))
        test_files = list(self.test_dir.glob(f"*{self.ext}"))
        
        train_ai = len([f for f in train_files if f.name.startswith('0_')])
        train_human = len([f for f in train_files if f.name.startswith('1_')])
        
        test_ai = len([f for f in test_files if f.name.startswith('0_')])
        test_human = len([f for f in test_files if f.name.startswith('1_')])
        
        print(f"\nLanguage: {self.language}")
        print(f"\nTraining Set:")
        print(f"   - AI-generated:  {train_ai:4d} samples")
        print(f"   - Human-written: {train_human:4d} samples")
        print(f"   - Total:         {len(train_files):4d} samples")
        
        print(f"\nTest Set:")
        print(f"   - AI-generated:  {test_ai:4d} samples")
        print(f"   - Human-written: {test_human:4d} samples")
        print(f"   - Total:         {len(test_files):4d} samples")
        
        print(f"\nGrand Total:     {len(train_files) + len(test_files):4d} samples")
        
        # Class balance
        train_balance = train_human / (train_human + train_ai) if train_ai + train_human > 0 else 0
        test_balance = test_human / (test_human + test_ai) if test_ai + test_human > 0 else 0
        
        print(f"\nClass Balance:")
        print(f"   - Training: {train_balance:.1%} human / {1-train_balance:.1%} AI")
        print(f"   - Test:     {test_balance:.1%} human / {1-test_balance:.1%} AI")
        
        # Sample file sizes
        if train_files:
            train_sizes = [f.stat().st_size for f in train_files[:100]]
            avg_size = sum(train_sizes) / len(train_sizes)
            print(f"\nAverage file size: {avg_size/1024:.1f} KB")
        
        # Check for issues
        print(f"\nData Quality Checks:")
        
        issues = []
        if train_ai == 0 or train_human == 0:
            issues.append("WARNING: Training set has missing class!")
        if test_ai == 0 or test_human == 0:
            issues.append("WARNING: Test set has missing class!")
        if abs(train_balance - 0.5) > 0.2:
            issues.append("WARNING: Training set is imbalanced (>70/30 split)")
        if len(test_files) < 100:
            issues.append("WARNING: Test set is too small (<100 samples)")
        
        if issues:
            for issue in issues:
                print(f"   {issue}")
        else:
            print(f"   + All checks passed!")
        
        print("\n" + "=" * 60)
    
    def prepare(self, train_ratio=0.8) -> None:
        """
        Main preparation pipeline
        
        Args:
            train_ratio: Ratio of training data
        """
        print("\n" + "=" * 60)
        print(f"PREPARING {self.language} DATASET")
        print("=" * 60)
        
        # Step 1: Validate
        valid_human, valid_ai = self.validate_dataset()
        
        if len(valid_human) == 0:
            print("\n❌ ERROR: No valid human samples found!")
            print(f"   Check directory: {self.human_dir}")
            return
        
        if len(valid_ai) == 0:
            print("\n❌ ERROR: No valid AI samples found!")
            print(f"   Check directory: {self.ai_dir}")
            print("\n💡 Run generation script first:")
            print("   python scripts/generate_ai_code_groq.py --num 2000")
            return
        
        # Step 2: Split
        self.split_dataset(valid_human, valid_ai, train_ratio)
        
        # Step 3: Statistics
        self.generate_statistics()
        
        print("\n+ Dataset preparation complete!")
        print(f"\nTraining data: {self.train_dir}")
        print(f"Test data:     {self.test_dir}")
        print("\nNext step: Train the model")
        print("   python train_python_model.py")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Prepare dataset for training")
    parser.add_argument("--language", type=str, default="python", 
                       choices=["python", "cpp"],
                       help="Programming language (python or cpp)")
    parser.add_argument("--train-ratio", type=float, default=0.8,
                       help="Training set ratio (default: 0.8)")
    
    args = parser.parse_args()
    
    preparer = DatasetPreparer(args.language)
    preparer.prepare(args.train_ratio)

if __name__ == "__main__":
    main()
