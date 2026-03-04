# -*- coding: utf-8 -*-
"""GPTSniffer Training Script"""

import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from torch.utils.data import DataLoader, Dataset
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from os.path import join
import itertools
import time

# Set environment variables for CPU threading
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"

# Configuration
DATA_PATH = './DATASETS/RQ1/C1/CONF'
train_data_path = join(DATA_PATH, 'training_data')
test_data_path = join(DATA_PATH, 'testing_data')
OUTPUT_DIR = './results'
MODEL_CHECKPOINT_DIR = join(OUTPUT_DIR, 'final_model')

# Set device to GPU if available, otherwise use CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# Define the tokenizer and the model
print("Loading CodeBERT tokenizer and model...")
tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModelForSequenceClassification.from_pretrained("microsoft/codebert-base", num_labels=2)
model.to(device)

# Define the dataset
class CodeDataset(Dataset):
    def __init__(self, directory):
        self.samples = []
        print(f"Loading data from {directory}...")
        for filename in os.listdir(directory):
            try:
                label = int(filename.split('_')[0])
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    code = f.read()
                    self.samples.append((code, label))
            except Exception as e:
                print(f"Error loading {filename}: {e}")
        print(f"Loaded {len(self.samples)} samples")
    
    def __len__(self):
        return len(self.samples)

    def __getitem__(self, index):
        code, label = self.samples[index]
        inputs = tokenizer.encode_plus(
            code, 
            padding='max_length', 
            max_length=512, 
            truncation=True
        )
        input_ids = inputs['input_ids']
        attention_mask = inputs['attention_mask']
        return {
            'input_ids': torch.tensor(input_ids, dtype=torch.long), 
            'attention_mask': torch.tensor(attention_mask, dtype=torch.long), 
            'labels': torch.tensor(label, dtype=torch.long)
        }

# Define the training dataset and dataloader
print("\n=== Loading Training Data ===")
train_dataset = CodeDataset(train_data_path)
train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# Define the testing dataset and dataloader
print("\n=== Loading Testing Data ===")
test_dataset = CodeDataset(test_data_path)
test_dataloader = DataLoader(test_dataset, batch_size=32, shuffle=False)

# Define the training arguments and the trainer
print("\n=== Setting Up Training ===")
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=12,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=32,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    optim='adamw_torch',
    learning_rate=5e-5,
    save_total_limit=2,
    save_strategy='epoch',
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset
)

# Train the model
print("\n=== Starting Training ===")
print("This will take approximately 30-60 minutes on GPU or 4-8 hours on CPU...")
trainer.train()

# Save the final model
print(f"\n=== Saving Final Model to {MODEL_CHECKPOINT_DIR} ===")
trainer.save_model(MODEL_CHECKPOINT_DIR)
tokenizer.save_pretrained(MODEL_CHECKPOINT_DIR)

# Test the model
print("\n=== Evaluating Model ===")
model.eval()
y_true = []
y_pred = []

start = time.time()
with torch.no_grad():
    for batch in test_dataloader:
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)
        outputs = model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=1)
        y_true += labels.tolist()
        y_pred += predictions.tolist()

end = time.time()
print(f'Inference time: {end - start:.2f} seconds')

# Plot confusion matrix
def plot_confusion_matrix(cm, classes, normalize=True, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.figure(figsize=(10,10))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    if normalize:
        cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        cm_normalized = np.around(cm_normalized, decimals=2)
        cm_normalized[np.isnan(cm_normalized)] = 0.0
        print("Normalized confusion matrix")
        display_cm = cm_normalized
    else:
        print('Confusion matrix, without normalization')
        display_cm = cm
    
    thresh = display_cm.max() / 2.
    for i, j in itertools.product(range(display_cm.shape[0]), range(display_cm.shape[1])):
        plt.text(j, i, display_cm[i, j],
                 horizontalalignment="center",
                 color="white" if display_cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.savefig('confusion_matrix.png')
    print("Confusion matrix saved to confusion_matrix.png")

# Print results
target_names = ['ChatGPT', 'Human']

print('\n=== Confusion Matrix ===')
cm = confusion_matrix(y_true, y_pred)
print(cm)
plot_confusion_matrix(cm, target_names, title='Confusion Matrix')

print('\n=== Classification Report ===')
print(classification_report(y_true, y_pred, target_names=target_names))

accuracy = accuracy_score(y_true, y_pred)
print(f'\n=== Final Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%) ===')

print(f"\n=== Training Complete! ===")
print(f"Model saved to: {MODEL_CHECKPOINT_DIR}")
print(f"To use this model with the webapp, set environment variable:")
print(f"  MODEL_DIR={MODEL_CHECKPOINT_DIR}")
