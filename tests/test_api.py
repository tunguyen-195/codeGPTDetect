# -*- coding: utf-8 -*-
"""
Test cases cho API endpoints của GPTSniffer WebApp
Đánh giá hiệu quả của các API: /health, /predict, /predict-file
"""

import requests
import json
import os
import time
from typing import Dict, List, Optional
from pathlib import Path


class GPTSnifferAPITester:
    """Lớp test cho GPTSniffer API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Khởi tạo API tester
        
        Args:
            base_url: URL base của API server
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.results = []
    
    def test_health_endpoint(self) -> Dict:
        """Test Case 4a: Test /health endpoint"""
        print("\n" + "="*80)
        print("TEST CASE 4a: Health Endpoint")
        print("="*80)
        
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            response.raise_for_status()
            data = response.json()
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(data, indent=2)}")
            
            result = {
                "test": "health_endpoint",
                "status": "success",
                "status_code": response.status_code,
                "response": data,
                "timestamp": time.time()
            }
            
            assert response.status_code == 200, "Expected status code 200"
            assert "status" in data, "Response should contain 'status' field"
            assert data["status"] == "ok", "Status should be 'ok'"
            
            print("✓ Health endpoint test passed")
            return result
            
        except requests.exceptions.ConnectionError:
            error_msg = f"Cannot connect to {self.base_url}. Make sure the server is running."
            print(f"✗ Connection error: {error_msg}")
            return {
                "test": "health_endpoint",
                "status": "error",
                "error": error_msg,
                "timestamp": time.time()
            }
        except Exception as e:
            error_msg = str(e)
            print(f"✗ Error: {error_msg}")
            return {
                "test": "health_endpoint",
                "status": "error",
                "error": error_msg,
                "timestamp": time.time()
            }
    
    def test_predict_endpoint(self, code: str, expected_label: Optional[str] = None) -> Dict:
        """Test Case 4b: Test /predict endpoint với JSON payload"""
        print("\n" + "="*80)
        print("TEST CASE 4b: Predict Endpoint (JSON)")
        print("="*80)
        
        try:
            payload = {"code": code}
            response = self.session.post(
                f"{self.base_url}/predict",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(data, indent=2)}")
            
            result = {
                "test": "predict_endpoint",
                "status": "success",
                "status_code": response.status_code,
                "response": data,
                "expected_label": expected_label,
                "timestamp": time.time()
            }
            
            assert response.status_code == 200, "Expected status code 200"
            assert "label" in data, "Response should contain 'label' field"
            assert "confidence" in data, "Response should contain 'confidence' field"
            assert "probabilities" in data, "Response should contain 'probabilities' field"
            
            if expected_label:
                if data["label"] == expected_label:
                    print(f"✓ Prediction matches expected label: {expected_label}")
                else:
                    print(f"⚠ Prediction does not match expected label. Got: {data['label']}, Expected: {expected_label}")
                    result["status"] = "warning"
            
            print("✓ Predict endpoint test passed")
            return result
            
        except requests.exceptions.ConnectionError:
            error_msg = f"Cannot connect to {self.base_url}. Make sure the server is running."
            print(f"✗ Connection error: {error_msg}")
            return {
                "test": "predict_endpoint",
                "status": "error",
                "error": error_msg,
                "timestamp": time.time()
            }
        except Exception as e:
            error_msg = str(e)
            print(f"✗ Error: {error_msg}")
            return {
                "test": "predict_endpoint",
                "status": "error",
                "error": error_msg,
                "timestamp": time.time()
            }
    
    def test_predict_file_endpoint(self, file_path: str, expected_label: Optional[str] = None) -> Dict:
        """Test Case 4c: Test /predict-file endpoint với file upload"""
        print("\n" + "="*80)
        print("TEST CASE 4c: Predict File Endpoint")
        print("="*80)
        
        try:
            if not os.path.exists(file_path):
                error_msg = f"File not found: {file_path}"
                print(f"✗ {error_msg}")
                return {
                    "test": "predict_file_endpoint",
                    "status": "error",
                    "error": error_msg,
                    "timestamp": time.time()
                }
            
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f, 'text/plain')}
                response = self.session.post(
                    f"{self.base_url}/predict-file",
                    files=files,
                    timeout=30
                )
            
            response.raise_for_status()
            data = response.json()
            
            print(f"Status Code: {response.status_code}")
            print(f"File: {file_path}")
            print(f"Response: {json.dumps(data, indent=2)}")
            
            result = {
                "test": "predict_file_endpoint",
                "status": "success",
                "status_code": response.status_code,
                "file": file_path,
                "response": data,
                "expected_label": expected_label,
                "timestamp": time.time()
            }
            
            assert response.status_code == 200, "Expected status code 200"
            assert "label" in data, "Response should contain 'label' field"
            assert "confidence" in data, "Response should contain 'confidence' field"
            
            if expected_label:
                if data["label"] == expected_label:
                    print(f"✓ Prediction matches expected label: {expected_label}")
                else:
                    print(f"⚠ Prediction does not match expected label. Got: {data['label']}, Expected: {expected_label}")
                    result["status"] = "warning"
            
            print("✓ Predict file endpoint test passed")
            return result
            
        except requests.exceptions.ConnectionError:
            error_msg = f"Cannot connect to {self.base_url}. Make sure the server is running."
            print(f"✗ Connection error: {error_msg}")
            return {
                "test": "predict_file_endpoint",
                "status": "error",
                "error": error_msg,
                "timestamp": time.time()
            }
        except Exception as e:
            error_msg = str(e)
            print(f"✗ Error: {error_msg}")
            return {
                "test": "predict_file_endpoint",
                "status": "error",
                "error": error_msg,
                "timestamp": time.time()
            }
    
    def test_error_handling(self) -> Dict:
        """Test Case 4d: Test error handling"""
        print("\n" + "="*80)
        print("TEST CASE 4d: Error Handling")
        print("="*80)
        
        results = []
        
        # Test empty code
        try:
            response = self.session.post(
                f"{self.base_url}/predict",
                json={"code": ""},
                timeout=10
            )
            print(f"Empty code - Status: {response.status_code}")
            if response.status_code == 400:
                print("✓ Empty code correctly rejected (400)")
                results.append({"test": "empty_code", "status": "success"})
            else:
                print(f"⚠ Unexpected status code: {response.status_code}")
                results.append({"test": "empty_code", "status": "warning", "status_code": response.status_code})
        except Exception as e:
            print(f"✗ Error testing empty code: {e}")
            results.append({"test": "empty_code", "status": "error", "error": str(e)})
        
        # Test missing code field
        try:
            response = self.session.post(
                f"{self.base_url}/predict",
                json={},
                timeout=10
            )
            print(f"Missing code field - Status: {response.status_code}")
            if response.status_code == 400:
                print("✓ Missing code field correctly rejected (400)")
                results.append({"test": "missing_code", "status": "success"})
            else:
                print(f"⚠ Unexpected status code: {response.status_code}")
                results.append({"test": "missing_code", "status": "warning", "status_code": response.status_code})
        except Exception as e:
            print(f"✗ Error testing missing code: {e}")
            results.append({"test": "missing_code", "status": "error", "error": str(e)})
        
        return {
            "test": "error_handling",
            "results": results,
            "timestamp": time.time()
        }
    
    def test_performance(self, code_samples: List[str], num_iterations: int = 10) -> Dict:
        """Test Case 4e: Test performance (latency)"""
        print("\n" + "="*80)
        print("TEST CASE 4e: Performance Test")
        print("="*80)
        
        latencies = []
        
        for i, code in enumerate(code_samples[:5], 1):  # Test với tối đa 5 samples
            print(f"\nTesting sample {i}/{min(5, len(code_samples))}...")
            sample_latencies = []
            
            for iteration in range(num_iterations):
                try:
                    start_time = time.time()
                    response = self.session.post(
                        f"{self.base_url}/predict",
                        json={"code": code},
                        timeout=30
                    )
                    end_time = time.time()
                    latency = (end_time - start_time) * 1000  # Convert to milliseconds
                    sample_latencies.append(latency)
                    
                    if response.status_code != 200:
                        print(f"  Warning: Status code {response.status_code} on iteration {iteration + 1}")
                except Exception as e:
                    print(f"  Error on iteration {iteration + 1}: {e}")
                    continue
            
            if sample_latencies:
                avg_latency = sum(sample_latencies) / len(sample_latencies)
                min_latency = min(sample_latencies)
                max_latency = max(sample_latencies)
                latencies.extend(sample_latencies)
                
                print(f"  Average latency: {avg_latency:.2f}ms")
                print(f"  Min latency: {min_latency:.2f}ms")
                print(f"  Max latency: {max_latency:.2f}ms")
        
        if latencies:
            overall_avg = sum(latencies) / len(latencies)
            overall_min = min(latencies)
            overall_max = max(latencies)
            
            print(f"\n--- Overall Performance ---")
            print(f"Average latency: {overall_avg:.2f}ms")
            print(f"Min latency: {overall_min:.2f}ms")
            print(f"Max latency: {overall_max:.2f}ms")
            print(f"Total requests: {len(latencies)}")
            
            return {
                "test": "performance",
                "status": "success",
                "average_latency_ms": overall_avg,
                "min_latency_ms": overall_min,
                "max_latency_ms": overall_max,
                "total_requests": len(latencies),
                "timestamp": time.time()
            }
        else:
            return {
                "test": "performance",
                "status": "error",
                "error": "No successful requests",
                "timestamp": time.time()
            }


def test_case_4_api_integration(base_url: str = "http://localhost:8000"):
    """Test Case 4: Tổng hợp test API endpoints"""
    print("\n" + "="*80)
    print("TEST CASE 4: API Integration Tests")
    print("="*80)
    
    tester = GPTSnifferAPITester(base_url)
    results = {}
    
    # Test health endpoint
    results["health"] = tester.test_health_endpoint()
    
    # Test predict endpoint với sample codes
    chatgpt_code = """
    public class Calculator {
        public int add(int a, int b) {
            return a + b;
        }
    }
    """
    human_code = """
    // My implementation
    public class Calc {
        int add(int x, int y) {
            return x + y;
        }
    }
    """
    
    results["predict_json"] = tester.test_predict_endpoint(chatgpt_code)
    results["predict_human"] = tester.test_predict_endpoint(human_code)
    
    # Test predict file endpoint (nếu có file mẫu)
    test_data_dir = Path("DATASETS/RQ1/C1/CONF/testing_data")
    if test_data_dir.exists():
        files = list(test_data_dir.glob("*.java"))
        if files:
            # Test với một file ChatGPT (label = 0)
            chatgpt_file = next((f for f in files if f.name.startswith("0_")), None)
            if chatgpt_file:
                results["predict_file_chatgpt"] = tester.test_predict_file_endpoint(
                    str(chatgpt_file),
                    expected_label="ChatGPT"
                )
            
            # Test với một file Human (label = 1)
            human_file = next((f for f in files if f.name.startswith("1_")), None)
            if human_file:
                results["predict_file_human"] = tester.test_predict_file_endpoint(
                    str(human_file),
                    expected_label="Human"
                )
    
    # Test error handling
    results["error_handling"] = tester.test_error_handling()
    
    # Test performance
    code_samples = [chatgpt_code, human_code] * 3  # 6 samples
    results["performance"] = tester.test_performance(code_samples, num_iterations=5)
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test GPTSniffer API")
    parser.add_argument("--url", type=str, default="http://localhost:8000",
                       help="Base URL of the API server")
    parser.add_argument("--output", type=str, default=None,
                       help="Output JSON file for results")
    
    args = parser.parse_args()
    
    results = test_case_4_api_integration(args.url)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to: {args.output}")

