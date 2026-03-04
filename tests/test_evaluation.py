# -*- coding: utf-8 -*-
"""
Test cases để đánh giá hiệu quả của GPTSniffer
Đánh giá khả năng phát hiện mã nguồn do ChatGPT tạo vs mã do con người viết
"""

import os
import sys
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict
import json
from datetime import datetime

# Thêm đường dẫn để import từ GPTSniffer
sys.path.insert(0, str(Path(__file__).parent.parent))

class GPTSnifferEvaluator:
    """Lớp đánh giá hiệu quả của GPTSniffer"""
    
    def __init__(self, model_path: str = None, device: str = None):
        """
        Khởi tạo evaluator
        
        Args:
            model_path: Đường dẫn đến model đã huấn luyện (optional)
            device: 'cuda' hoặc 'cpu' (optional, tự động phát hiện)
        """
        self.device = torch.device(device if device else ('cuda' if torch.cuda.is_available() else 'cpu'))
        
        # Load tokenizer và model
        if model_path and os.path.exists(model_path):
            print(f"Loading model from: {model_path}")
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
            self.model_source = f"checkpoint:{model_path}"
        else:
            print("Using base CodeBERT model (not fine-tuned)")
            self.tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
            self.model = AutoModelForSequenceClassification.from_pretrained("microsoft/codebert-base")
            self.model_source = "base:microsoft/codebert-base (not fine-tuned)"
        
        self.model.to(self.device)
        self.model.eval()
        self.labels = {0: "ChatGPT", 1: "Human"}
    
    def predict(self, code: str, max_length: int = 512) -> Dict:
        """
        Dự đoán một đoạn code
        
        Args:
            code: Mã nguồn cần dự đoán
            max_length: Độ dài tối đa của sequence
            
        Returns:
            Dict chứa label, confidence, probabilities
        """
        if not code or not code.strip():
            raise ValueError("Empty code input")
        
        inputs = self.tokenizer(
            code,
            padding="max_length",
            truncation=True,
            max_length=max_length,
            return_tensors="pt"
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits.detach().cpu()
            probs = torch.softmax(logits, dim=-1).squeeze(0)
            conf_values = probs.tolist()
            
            if len(conf_values) < 2:
                conf_values = conf_values + [0.0] * (2 - len(conf_values))
            
            best_idx = int(torch.argmax(probs).item()) if probs.numel() > 0 else 0
            label = self.labels.get(best_idx, str(best_idx))
            
            return {
                "label": label,
                "label_idx": best_idx,
                "confidence": float(conf_values[best_idx]) if conf_values else 0.0,
                "probabilities": {
                    self.labels.get(0, "0"): float(conf_values[0]) if len(conf_values) > 0 else 0.0,
                    self.labels.get(1, "1"): float(conf_values[1]) if len(conf_values) > 1 else 0.0,
                }
            }
    
    def evaluate_on_dataset(self, test_data_path: str) -> Dict:
        """
        Đánh giá trên tập dữ liệu test
        
        Args:
            test_data_path: Đường dẫn đến thư mục chứa file test (format: {label}_{filename})
            
        Returns:
            Dict chứa các metrics: accuracy, precision, recall, f1, confusion_matrix
        """
        y_true = []
        y_pred = []
        file_results = []
        
        print(f"Evaluating on dataset: {test_data_path}")
        
        if not os.path.exists(test_data_path):
            raise FileNotFoundError(f"Test data path not found: {test_data_path}")
        
        files = [f for f in os.listdir(test_data_path) if os.path.isfile(os.path.join(test_data_path, f))]
        total_files = len(files)
        
        print(f"Found {total_files} files to evaluate")
        
        for idx, filename in enumerate(files, 1):
            if idx % 50 == 0:
                print(f"Processing {idx}/{total_files} files...")
            
            # Parse label from filename (format: {label}_{filename})
            try:
                true_label_str = filename.split('_')[0]
                true_label = int(true_label_str)
                
                filepath = os.path.join(test_data_path, filename)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    code = f.read()
                
                prediction = self.predict(code)
                pred_label_idx = prediction['label_idx']
                
                # Map: 0 = ChatGPT, 1 = Human
                y_true.append(true_label)
                y_pred.append(pred_label_idx)
                
                file_results.append({
                    "file": filename,
                    "true_label": self.labels.get(true_label, str(true_label)),
                    "predicted_label": prediction['label'],
                    "confidence": prediction['confidence'],
                    "correct": true_label == pred_label_idx
                })
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue
        
        # Calculate metrics
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
        cm = confusion_matrix(y_true, y_pred)
        
        # Per-class metrics
        precision_per_class = precision_score(y_true, y_pred, average=None, zero_division=0)
        recall_per_class = recall_score(y_true, y_pred, average=None, zero_division=0)
        f1_per_class = f1_score(y_true, y_pred, average=None, zero_division=0)
        
        results = {
            "model_source": self.model_source,
            "device": str(self.device),
            "total_files": total_files,
            "accuracy": float(accuracy),
            "precision": float(precision),
            "recall": float(recall),
            "f1_score": float(f1),
            "confusion_matrix": cm.tolist(),
            "per_class_metrics": {
                "ChatGPT (0)": {
                    "precision": float(precision_per_class[0]) if len(precision_per_class) > 0 else 0.0,
                    "recall": float(recall_per_class[0]) if len(recall_per_class) > 0 else 0.0,
                    "f1": float(f1_per_class[0]) if len(f1_per_class) > 0 else 0.0
                },
                "Human (1)": {
                    "precision": float(precision_per_class[1]) if len(precision_per_class) > 1 else 0.0,
                    "recall": float(recall_per_class[1]) if len(recall_per_class) > 1 else 0.0,
                    "f1": float(f1_per_class[1]) if len(f1_per_class) > 1 else 0.0
                }
            },
            "file_results": file_results[:100],  # Giới hạn 100 file đầu tiên để không quá lớn
            "classification_report": classification_report(y_true, y_pred, target_names=['ChatGPT', 'Human'], output_dict=True)
        }
        
        return results
    
    def print_evaluation_report(self, results: Dict):
        """In báo cáo đánh giá ra console"""
        print("\n" + "="*80)
        print("EVALUATION REPORT - GPTSniffer")
        print("="*80)
        print(f"Model Source: {results['model_source']}")
        print(f"Device: {results['device']}")
        print(f"Total Files Evaluated: {results['total_files']}")
        print("\n--- Overall Metrics ---")
        print(f"Accuracy:  {results['accuracy']:.4f} ({results['accuracy']*100:.2f}%)")
        print(f"Precision: {results['precision']:.4f}")
        print(f"Recall:    {results['recall']:.4f}")
        print(f"F1-Score:  {results['f1_score']:.4f}")
        
        print("\n--- Per-Class Metrics ---")
        for class_name, metrics in results['per_class_metrics'].items():
            print(f"\n{class_name}:")
            print(f"  Precision: {metrics['precision']:.4f}")
            print(f"  Recall:    {metrics['recall']:.4f}")
            print(f"  F1-Score:  {metrics['f1']:.4f}")
        
        print("\n--- Confusion Matrix ---")
        cm = np.array(results['confusion_matrix'])
        print(f"                Predicted")
        print(f"              ChatGPT  Human")
        print(f"True ChatGPT    {cm[0,0]:5d}  {cm[0,1]:5d}")
        print(f"      Human     {cm[1,0]:5d}  {cm[1,1]:5d}")
        
        print("\n--- Classification Report ---")
        report = results['classification_report']
        print(f"\n{'Class':<12} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'Support':<12}")
        print("-" * 60)
        for class_name in ['ChatGPT', 'Human']:
            if class_name in report:
                metrics = report[class_name]
                print(f"{class_name:<12} {metrics['precision']:<12.4f} {metrics['recall']:<12.4f} {metrics['f1-score']:<12.4f} {metrics['support']:<12}")
        
        if 'accuracy' in report:
            print(f"\n{'Accuracy':<12} {'':<12} {'':<12} {report['accuracy']:<12.4f} {report.get('macro avg', {}).get('support', 0):<12}")
        
        print("\n" + "="*80)


def test_case_1_basic_prediction():
    """Test Case 1: Đánh giá khả năng dự đoán cơ bản trên một đoạn code mẫu"""
    print("\n" + "="*80)
    print("TEST CASE 1: Basic Prediction on Sample Code")
    print("="*80)
    
    evaluator = GPTSnifferEvaluator()
    
    # Mã mẫu do ChatGPT tạo (dự kiến label = ChatGPT/0)
    chatgpt_code = """
    public class Calculator {
        public int add(int a, int b) {
            return a + b;
        }
        public int subtract(int a, int b) {
            return a - b;
        }
    }
    """
    
    # Mã mẫu do con người viết (dự kiến label = Human/1)
    human_code = """
    // This is a simple implementation
    public class Calc {
        int add(int x, int y) {
            int result = x + y;
            return result;
        }
    }
    """
    
    print("\n--- Testing ChatGPT-generated code ---")
    result1 = evaluator.predict(chatgpt_code)
    print(f"Predicted: {result1['label']}")
    print(f"Confidence: {result1['confidence']:.4f}")
    print(f"Probabilities: ChatGPT={result1['probabilities']['ChatGPT']:.4f}, Human={result1['probabilities']['Human']:.4f}")
    
    print("\n--- Testing Human-written code ---")
    result2 = evaluator.predict(human_code)
    print(f"Predicted: {result2['label']}")
    print(f"Confidence: {result2['confidence']:.4f}")
    print(f"Probabilities: ChatGPT={result2['probabilities']['ChatGPT']:.4f}, Human={result2['probabilities']['Human']:.4f}")
    
    return {
        "chatgpt_prediction": result1,
        "human_prediction": result2
    }


def test_case_2_dataset_evaluation(test_data_path: str):
    """Test Case 2: Đánh giá trên tập dữ liệu test thực tế"""
    print("\n" + "="*80)
    print("TEST CASE 2: Dataset Evaluation")
    print("="*80)
    
    evaluator = GPTSnifferEvaluator()
    results = evaluator.evaluate_on_dataset(test_data_path)
    evaluator.print_evaluation_report(results)
    
    return results


def test_case_3_edge_cases():
    """Test Case 3: Đánh giá với các trường hợp đặc biệt (edge cases)"""
    print("\n" + "="*80)
    print("TEST CASE 3: Edge Cases Evaluation")
    print("="*80)
    
    evaluator = GPTSnifferEvaluator()
    
    edge_cases = [
        {
            "name": "Very short code",
            "code": "int x = 5;"
        },
        {
            "name": "Very long code (>512 tokens)",
            "code": "public class LongClass {\n" + "    private int field1;\n" * 100 + "}"
        },
        {
            "name": "Code with many comments",
            "code": """
            // This is a comment
            /* This is a multi-line comment
               with multiple lines */
            public class Commented {
                // Another comment
                public void method() { } // Inline comment
            }
            """
        },
        {
            "name": "Empty/whitespace only",
            "code": "   \n\n\t  "
        },
        {
            "name": "Code with special characters",
            "code": """
            public class Special {
                String s = "Hello @#$%^&*()";
                void method() { System.out.println("Test"); }
            }
            """
        }
    ]
    
    results = []
    for case in edge_cases:
        try:
            if case["code"].strip():
                result = evaluator.predict(case["code"])
                results.append({
                    "case": case["name"],
                    "result": result,
                    "status": "success"
                })
                print(f"\n{case['name']}:")
                print(f"  Predicted: {result['label']} (confidence: {result['confidence']:.4f})")
            else:
                results.append({
                    "case": case["name"],
                    "result": None,
                    "status": "skipped (empty)"
                })
                print(f"\n{case['name']}: Skipped (empty code)")
        except Exception as e:
            results.append({
                "case": case["name"],
                "result": None,
                "status": f"error: {str(e)}"
            })
            print(f"\n{case['name']}: Error - {e}")
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Đánh giá hiệu quả GPTSniffer")
    parser.add_argument("--test-case", type=int, choices=[1, 2, 3, 0], default=0,
                       help="Test case to run (1: basic, 2: dataset, 3: edge cases, 0: all)")
    parser.add_argument("--test-data", type=str,
                       default="DATASETS/RQ1/C1/CONF/testing_data",
                       help="Path to test dataset")
    parser.add_argument("--model-path", type=str, default=None,
                       help="Path to trained model checkpoint")
    parser.add_argument("--output", type=str, default=None,
                       help="Output JSON file for results")
    
    args = parser.parse_args()
    
    # Run test cases
    all_results = {}
    
    if args.test_case == 0 or args.test_case == 1:
        all_results["test_case_1"] = test_case_1_basic_prediction()
    
    if args.test_case == 0 or args.test_case == 2:
        if os.path.exists(args.test_data):
            all_results["test_case_2"] = test_case_2_dataset_evaluation(args.test_data)
        else:
            print(f"\nWarning: Test data path not found: {args.test_data}")
            print("Skipping Test Case 2")
    
    if args.test_case == 0 or args.test_case == 3:
        all_results["test_case_3"] = test_case_3_edge_cases()
    
    # Save results if output file specified
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to: {args.output}")

