# -*- coding: utf-8 -*-
"""
Script tổng hợp chạy tất cả test cases đánh giá hiệu quả GPTSniffer
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Thêm đường dẫn để import
sys.path.insert(0, str(Path(__file__).parent))

from test_evaluation import (
    test_case_1_basic_prediction,
    test_case_2_dataset_evaluation,
    test_case_3_edge_cases,
    GPTSnifferEvaluator
)
from test_api import test_case_4_api_integration


def create_results_directory():
    """Tạo thư mục lưu kết quả"""
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    return results_dir


def print_summary(all_results: dict):
    """In tóm tắt kết quả"""
    print("\n" + "="*80)
    print("SUMMARY - TỔNG KẾT ĐÁNH GIÁ")
    print("="*80)
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    skipped_tests = 0
    
    for test_name, result in all_results.items():
        if isinstance(result, dict):
            status = result.get("status", "unknown")
            if status == "success":
                passed_tests += 1
                total_tests += 1
            elif status == "error":
                failed_tests += 1
                total_tests += 1
            elif status == "skipped":
                skipped_tests += 1
        elif isinstance(result, list):
            # Đếm các test trong list
            for item in result:
                if isinstance(item, dict):
                    item_status = item.get("status", "unknown")
                    total_tests += 1
                    if item_status == "success":
                        passed_tests += 1
                    elif item_status == "error":
                        failed_tests += 1
        else:
            # Test có thể trả về kết quả khác (như dataset evaluation)
            total_tests += 1
            if result:
                passed_tests += 1
    
    print(f"\nTổng số test: {total_tests}")
    print(f"  ✓ Passed: {passed_tests}")
    print(f"  ✗ Failed: {failed_tests}")
    print(f"  ⊘ Skipped: {skipped_tests}")
    
    # In chi tiết từng test case
    print("\n--- Chi tiết từng Test Case ---")
    
    if "test_case_1" in all_results:
        print("\nTest Case 1: Basic Prediction")
        print("  Status: ✓ Completed")
        tc1 = all_results["test_case_1"]
        if "chatgpt_prediction" in tc1:
            print(f"  ChatGPT prediction: {tc1['chatgpt_prediction'].get('label', 'N/A')}")
        if "human_prediction" in tc1:
            print(f"  Human prediction: {tc1['human_prediction'].get('label', 'N/A')}")
    
    if "test_case_2" in all_results:
        print("\nTest Case 2: Dataset Evaluation")
        tc2 = all_results["test_case_2"]
        if isinstance(tc2, dict) and "accuracy" in tc2:
            print(f"  Status: ✓ Completed")
            print(f"  Accuracy: {tc2['accuracy']:.4f} ({tc2['accuracy']*100:.2f}%)")
            print(f"  F1-Score: {tc2['f1_score']:.4f}")
            print(f"  Total files: {tc2['total_files']}")
        else:
            print("  Status: ⊘ Skipped (no test data)")
    
    if "test_case_3" in all_results:
        print("\nTest Case 3: Edge Cases")
        print("  Status: ✓ Completed")
        tc3 = all_results["test_case_3"]
        success_count = sum(1 for item in tc3 if item.get("status") == "success")
        print(f"  Edge cases tested: {len(tc3)}")
        print(f"  Successful: {success_count}")
    
    if "test_case_4" in all_results:
        print("\nTest Case 4: API Integration Tests")
        tc4 = all_results["test_case_4"]
        if isinstance(tc4, dict):
            api_tests = [k for k in tc4.keys() if isinstance(tc4[k], dict)]
            success_count = sum(1 for k in api_tests if tc4[k].get("status") == "success")
            print(f"  API endpoints tested: {len(api_tests)}")
            print(f"  Successful: {success_count}")
    
    print("\n" + "="*80)


def main():
    parser = argparse.ArgumentParser(
        description="Chạy tất cả test cases đánh giá hiệu quả GPTSniffer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
  # Chạy tất cả test cases
  python run_all_tests.py
  
  # Chỉ chạy test case 1 và 2
  python run_all_tests.py --test-cases 1 2
  
  # Chạy với model đã huấn luyện
  python run_all_tests.py --model-path ./results/checkpoint-1000
  
  # Chạy test API với server khác
  python run_all_tests.py --api-url http://localhost:8000
        """
    )
    
    parser.add_argument("--test-cases", type=int, nargs="+", default=[1, 2, 3, 4],
                       choices=[1, 2, 3, 4],
                       help="Test cases to run (default: all)")
    parser.add_argument("--test-data", type=str,
                       default="DATASETS/RQ1/C1/CONF/testing_data",
                       help="Path to test dataset")
    parser.add_argument("--model-path", type=str, default=None,
                       help="Path to trained model checkpoint")
    parser.add_argument("--api-url", type=str, default="http://localhost:8000",
                       help="Base URL of the API server")
    parser.add_argument("--output", type=str, default=None,
                       help="Output JSON file for results (default: results/timestamp.json)")
    parser.add_argument("--skip-api", action="store_true",
                       help="Skip API tests (useful when server is not running)")
    
    args = parser.parse_args()
    
    # Tạo thư mục results
    results_dir = create_results_directory()
    
    # Tên file output mặc định
    if args.output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = results_dir / f"evaluation_results_{timestamp}.json"
    
    print("="*80)
    print("GPTSniffer - Comprehensive Evaluation Test Suite")
    print("="*80)
    print(f"Test cases to run: {args.test_cases}")
    print(f"Test data path: {args.test_data}")
    print(f"Model path: {args.model_path if args.model_path else 'Using base CodeBERT'}")
    if 4 in args.test_cases and not args.skip_api:
        print(f"API URL: {args.api_url}")
    print(f"Output file: {args.output}")
    print("="*80)
    
    all_results = {
        "timestamp": datetime.now().isoformat(),
        "config": {
            "test_cases": args.test_cases,
            "test_data_path": args.test_data,
            "model_path": args.model_path,
            "api_url": args.api_url if 4 in args.test_cases else None
        }
    }
    
    # Chạy các test cases
    try:
        if 1 in args.test_cases:
            print("\n>>> Running Test Case 1: Basic Prediction...")
            all_results["test_case_1"] = test_case_1_basic_prediction()
        
        if 2 in args.test_cases:
            print("\n>>> Running Test Case 2: Dataset Evaluation...")
            if os.path.exists(args.test_data):
                evaluator = GPTSnifferEvaluator(model_path=args.model_path)
                results = evaluator.evaluate_on_dataset(args.test_data)
                evaluator.print_evaluation_report(results)
                all_results["test_case_2"] = results
            else:
                print(f"Warning: Test data path not found: {args.test_data}")
                print("Skipping Test Case 2")
                all_results["test_case_2"] = {
                    "status": "skipped",
                    "reason": f"Test data path not found: {args.test_data}"
                }
        
        if 3 in args.test_cases:
            print("\n>>> Running Test Case 3: Edge Cases...")
            all_results["test_case_3"] = test_case_3_edge_cases()
        
        if 4 in args.test_cases and not args.skip_api:
            print("\n>>> Running Test Case 4: API Integration Tests...")
            all_results["test_case_4"] = test_case_4_api_integration(args.api_url)
        elif 4 in args.test_cases and args.skip_api:
            print("\n>>> Skipping Test Case 4: API Tests (--skip-api flag set)")
            all_results["test_case_4"] = {
                "status": "skipped",
                "reason": "Skipped by --skip-api flag"
            }
    
    except KeyboardInterrupt:
        print("\n\nTest execution interrupted by user")
        all_results["status"] = "interrupted"
    except Exception as e:
        print(f"\n\nError during test execution: {e}")
        import traceback
        traceback.print_exc()
        all_results["status"] = "error"
        all_results["error"] = str(e)
    
    # In tóm tắt
    print_summary(all_results)
    
    # Lưu kết quả
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Results saved to: {args.output}")
    except Exception as e:
        print(f"\n✗ Error saving results: {e}")
    
    # Exit code
    if all_results.get("status") == "error":
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

