"""
Prepare model checkpoint for serving by adding tokenizer files
"""
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Configuration
CHECKPOINT_DIR = "./results/checkpoint-228"
OUTPUT_DIR = "./models/gptsniffer-finetuned"

print(f"Loading model from {CHECKPOINT_DIR}...")
model = AutoModelForSequenceClassification.from_pretrained(CHECKPOINT_DIR)

print("Loading CodeBERT tokenizer...")
tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")

print(f"Saving complete model with tokenizer to {OUTPUT_DIR}...")
os.makedirs(OUTPUT_DIR, exist_ok=True)
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print("Done! Model is ready for serving.")
print(f"\nTo use with webapp:")
print(f"  set MODEL_DIR={OUTPUT_DIR}")
print(f"  or use environment variable:")
print(f"    $env:MODEL_DIR=\"{OUTPUT_DIR}\"")
