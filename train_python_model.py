"""
Train Python Code Detection Model using CodeBERT

Dataset: 3286 training samples (1565 human + 1721 AI)
Model: microsoft/codebert-base
Task: Binary classification (Human vs AI-generated code)
"""

import os
import sys
import torch
import numpy as np
from pathlib import Path
from datetime import datetime
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback
)
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

class CodeDataset(torch.utils.data.Dataset):
    """Dataset for code classification"""
    
    def __init__(self, data_dir, tokenizer, max_length=512):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.samples = []
        self.labels = []
        
        print(f"Loading data from: {data_dir}")
        
        # Load all files
        data_path = Path(data_dir)
        files = list(data_path.glob("*.py"))
        
        print(f"Found {len(files)} files")
        
        for filepath in files:
            # Get label from filename (0=AI, 1=Human)
            label = 1 if filepath.name.startswith('1_') else 0
            
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    code = f.read()
                
                self.samples.append(code)
                self.labels.append(label)
                
            except Exception as e:
                print(f"Error loading {filepath.name}: {e}")
        
        print(f"Loaded {len(self.samples)} samples")
        
        # Count labels
        ai_count = sum(1 for l in self.labels if l == 0)
        human_count = sum(1 for l in self.labels if l == 1)
        print(f"  AI: {ai_count}, Human: {human_count}")
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        code = self.samples[idx]
        label = self.labels[idx]
        
        # Tokenize
        encoding = self.tokenizer(
            code,
            truncation=True,
            max_length=self.max_length,
            padding='max_length',
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].squeeze(),
            'attention_mask': encoding['attention_mask'].squeeze(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

def compute_metrics(pred):
    """Compute evaluation metrics"""
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average='binary'
    )
    acc = accuracy_score(labels, preds)
    
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

def plot_confusion_matrix(y_true, y_pred, output_dir):
    """Plot and save confusion matrix"""
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        cm, 
        annot=True, 
        fmt='d', 
        cmap='Blues',
        xticklabels=['AI-Generated', 'Human-Written'],
        yticklabels=['AI-Generated', 'Human-Written']
    )
    plt.title('Confusion Matrix - Python Code Detection')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    
    save_path = Path(output_dir) / 'confusion_matrix.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\nConfusion matrix saved to: {save_path}")
    plt.close()

def main():
    print("="*70)
    print("TRAINING PYTHON CODE DETECTION MODEL")
    print("="*70)
    
    # Configuration
    MODEL_NAME = "microsoft/codebert-base"
    TRAIN_DIR = "./DATASETS/PYTHON/training_data"
    TEST_DIR = "./DATASETS/PYTHON/testing_data"
    OUTPUT_DIR = "./models/python-detector-v1"
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    OUTPUT_DIR = f"./models/python-detector-{timestamp}"
    
    # Check CUDA
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\nDevice: {device}")
    if device == "cuda":
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    
    # Load tokenizer and model
    print(f"\nLoading model: {MODEL_NAME}")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=2
    )
    
    # Prepare datasets
    print("\n" + "="*70)
    print("LOADING DATASETS")
    print("="*70)
    
    train_dataset = CodeDataset(TRAIN_DIR, tokenizer)
    test_dataset = CodeDataset(TEST_DIR, tokenizer)
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=12,
        per_device_train_batch_size=8 if device == "cpu" else 16,
        per_device_eval_batch_size=16 if device == "cpu" else 32,
        learning_rate=5e-5,
        weight_decay=0.01,
        warmup_steps=500,
        logging_dir=f'{OUTPUT_DIR}/logs',
        logging_steps=50,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True,
        save_total_limit=2,
        fp16=torch.cuda.is_available(),
        report_to="none",
        dataloader_num_workers=0,  # Avoid multiprocessing issues on Windows
    )
    
    print("\n" + "="*70)
    print("TRAINING CONFIGURATION")
    print("="*70)
    print(f"Epochs: {training_args.num_train_epochs}")
    print(f"Batch size (train): {training_args.per_device_train_batch_size}")
    print(f"Batch size (eval): {training_args.per_device_eval_batch_size}")
    print(f"Learning rate: {training_args.learning_rate}")
    print(f"Weight decay: {training_args.weight_decay}")
    print(f"FP16: {training_args.fp16}")
    print(f"Output: {OUTPUT_DIR}")
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
    )
    
    # Train
    print("\n" + "="*70)
    print("STARTING TRAINING")
    print("="*70)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        train_result = trainer.train()
        
        print("\n" + "="*70)
        print("TRAINING COMPLETE")
        print("="*70)
        print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Training time: {train_result.metrics['train_runtime']/60:.1f} minutes")
        print(f"Samples/second: {train_result.metrics['train_samples_per_second']:.2f}")
        
    except Exception as e:
        print(f"\nTraining error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Evaluate on test set
    print("\n" + "="*70)
    print("EVALUATING ON TEST SET")
    print("="*70)
    
    try:
        eval_results = trainer.evaluate()
        
        print("\nTest Set Results:")
        print(f"  Accuracy:  {eval_results['eval_accuracy']:.4f}")
        print(f"  Precision: {eval_results['eval_precision']:.4f}")
        print(f"  Recall:    {eval_results['eval_recall']:.4f}")
        print(f"  F1-Score:  {eval_results['eval_f1']:.4f}")
        
        # Get predictions for confusion matrix
        predictions = trainer.predict(test_dataset)
        y_pred = predictions.predictions.argmax(-1)
        y_true = predictions.label_ids
        
        plot_confusion_matrix(y_true, y_pred, OUTPUT_DIR)
        
    except Exception as e:
        print(f"\nEvaluation error: {e}")
        import traceback
        traceback.print_exc()
    
    # Save final model
    print(f"\n" + "="*70)
    print("SAVING MODEL")
    print("="*70)
    
    try:
        trainer.save_model(OUTPUT_DIR)
        tokenizer.save_pretrained(OUTPUT_DIR)
        
        # Save metrics
        metrics_path = Path(OUTPUT_DIR) / 'metrics.txt'
        with open(metrics_path, 'w') as f:
            f.write("PYTHON CODE DETECTION MODEL - EVALUATION METRICS\n")
            f.write("="*50 + "\n\n")
            f.write(f"Model: {MODEL_NAME}\n")
            f.write(f"Training samples: {len(train_dataset)}\n")
            f.write(f"Test samples: {len(test_dataset)}\n\n")
            f.write("Test Set Performance:\n")
            f.write(f"  Accuracy:  {eval_results['eval_accuracy']:.4f}\n")
            f.write(f"  Precision: {eval_results['eval_precision']:.4f}\n")
            f.write(f"  Recall:    {eval_results['eval_recall']:.4f}\n")
            f.write(f"  F1-Score:  {eval_results['eval_f1']:.4f}\n")
        
        print(f"Model saved to: {OUTPUT_DIR}")
        print(f"Metrics saved to: {metrics_path}")
        
        print("\n" + "="*70)
        print("SUCCESS! TRAINING COMPLETE")
        print("="*70)
        print(f"\nModel location: {OUTPUT_DIR}")
        print("\nNext steps:")
        print("  1. Check confusion_matrix.png")
        print("  2. Review metrics.txt")
        print("  3. Test model with test_prediction.py")
        
        return 0
        
    except Exception as e:
        print(f"\nSaving error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
