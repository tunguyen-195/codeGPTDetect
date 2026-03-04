"""
Comprehensive Model Evaluation
Evaluate Python model on entire test set
"""

import os
import torch
import numpy as np
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import (
    accuracy_score, 
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report
)
from tqdm import tqdm

MODEL_PATH = "./models/python-detector-finetuned"
TEST_DIR = "./DATASETS/PYTHON/testing_data"

print("="*70)
print("COMPREHENSIVE MODEL EVALUATION")
print("="*70)

# Load model
print(f"\nLoading model from: {MODEL_PATH}")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
print(f"Device: {device}")

def predict(code):
    """Predict if code is AI-generated or human-written"""
    inputs = tokenizer(
        code,
        truncation=True,
        max_length=512,
        padding='max_length',
        return_tensors='pt'
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        prediction = torch.argmax(logits, dim=1).item()
    
    return prediction

# Load test data
print(f"\nLoading test data from: {TEST_DIR}")
test_path = Path(TEST_DIR)
test_files = list(test_path.glob("*.py"))

print(f"Found {len(test_files)} test files")

# Evaluate
y_true = []
y_pred = []
errors = []

print("\nEvaluating model on test set...")
for filepath in tqdm(test_files):
    # Get true label from filename (0=AI, 1=Human)
    true_label = 1 if filepath.name.startswith('1_') else 0
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            code = f.read()
        
        pred_label = predict(code)
        
        y_true.append(true_label)
        y_pred.append(pred_label)
        
        # Track errors
        if pred_label != true_label:
            errors.append({
                'file': filepath.name,
                'true': 'Human' if true_label == 1 else 'AI',
                'pred': 'Human' if pred_label == 1 else 'AI'
            })
    
    except Exception as e:
        print(f"\nError processing {filepath.name}: {e}")
        continue

# Calculate metrics
print("\n" + "="*70)
print("EVALUATION RESULTS")
print("="*70)

accuracy = accuracy_score(y_true, y_pred)
precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='binary')

print(f"\nTest Set Size: {len(y_true)} samples")
print(f"  AI-Generated: {sum(1 for y in y_true if y == 0)}")
print(f"  Human-Written: {sum(1 for y in y_true if y == 1)}")

print(f"\nPerformance Metrics:")
print(f"  Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"  Precision: {precision:.4f}")
print(f"  Recall:    {recall:.4f}")
print(f"  F1-Score:  {f1:.4f}")

# Confusion matrix
cm = confusion_matrix(y_true, y_pred)
print(f"\nConfusion Matrix:")
print(f"                 Predicted")
print(f"               AI    Human")
print(f"Actual  AI    {cm[0][0]:4d}   {cm[0][1]:4d}")
print(f"        Human {cm[1][0]:4d}   {cm[1][1]:4d}")

# Classification report
print(f"\nDetailed Classification Report:")
print(classification_report(
    y_true, y_pred, 
    target_names=['AI-Generated', 'Human-Written'],
    digits=4
))

# Show errors
if errors:
    print(f"\n" + "="*70)
    print(f"ERRORS: {len(errors)} misclassifications")
    print("="*70)
    for err in errors[:10]:  # Show first 10
        print(f"  {err['file']}: True={err['true']}, Predicted={err['pred']}")
    if len(errors) > 10:
        print(f"  ... and {len(errors) - 10} more")
else:
    print(f"\n" + "="*70)
    print("PERFECT SCORE - NO ERRORS!")
    print("="*70)

# Save results
results_file = Path(MODEL_PATH) / "detailed_evaluation.txt"
with open(results_file, 'w') as f:
    f.write("COMPREHENSIVE MODEL EVALUATION\n")
    f.write("="*70 + "\n\n")
    f.write(f"Model: {MODEL_PATH}\n")
    f.write(f"Test Set: {TEST_DIR}\n")
    f.write(f"Test Samples: {len(y_true)}\n\n")
    f.write(f"Accuracy:  {accuracy:.4f}\n")
    f.write(f"Precision: {precision:.4f}\n")
    f.write(f"Recall:    {recall:.4f}\n")
    f.write(f"F1-Score:  {f1:.4f}\n\n")
    f.write("Confusion Matrix:\n")
    f.write(f"               AI    Human\n")
    f.write(f"Actual  AI    {cm[0][0]:4d}   {cm[0][1]:4d}\n")
    f.write(f"        Human {cm[1][0]:4d}   {cm[1][1]:4d}\n\n")
    f.write(classification_report(
        y_true, y_pred, 
        target_names=['AI-Generated', 'Human-Written'],
        digits=4
    ))
    
    if errors:
        f.write(f"\n\nMisclassified Files ({len(errors)}):\n")
        f.write("-"*70 + "\n")
        for err in errors:
            f.write(f"{err['file']}: True={err['true']}, Predicted={err['pred']}\n")

print(f"\nDetailed results saved to: {results_file}")

print("\n" + "="*70)
print("EVALUATION COMPLETE")
print("="*70)
