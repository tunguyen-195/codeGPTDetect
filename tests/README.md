# GPTSniffer - Test Cases và Đánh giá Hiệu quả

Tài liệu này mô tả các test cases được thiết kế để đánh giá hiệu quả thực tế của hệ thống GPTSniffer trong việc phát hiện mã nguồn do ChatGPT tạo.

## Tổng quan

GPTSniffer là hệ thống sử dụng CodeBERT để phân loại mã nguồn, xác định xem mã được viết bởi ChatGPT hay con người. Bộ test cases này đánh giá:

1. **Độ chính xác** (Accuracy) - Tỷ lệ dự đoán đúng
2. **Precision** - Tỷ lệ dự đoán đúng trong số các dự đoán dương tính
3. **Recall** - Tỷ lệ phát hiện đúng trong số các trường hợp thực tế
4. **F1-Score** - Trung bình điều hòa của Precision và Recall
5. **Hiệu năng** (Performance) - Thời gian xử lý và độ trễ API
6. **Tính ổn định** - Xử lý các trường hợp đặc biệt (edge cases)

## Test Cases

### Test Case 1: Basic Prediction (Dự đoán cơ bản)

**Mục tiêu**: Đánh giá khả năng dự đoán cơ bản của mô hình trên các đoạn code mẫu.

**Nội dung**:
- Test với mã mẫu do ChatGPT tạo (dự kiến label = "ChatGPT")
- Test với mã mẫu do con người viết (dự kiến label = "Human")
- Kiểm tra confidence scores và probabilities

**Chạy test**:
```bash
python tests/test_evaluation.py --test-case 1
```

**Kết quả mong đợi**:
- Mô hình có thể dự đoán được label
- Confidence score > 0.5 cho dự đoán
- Probabilities cho cả hai lớp được tính toán đúng

---

### Test Case 2: Dataset Evaluation (Đánh giá trên tập dữ liệu)

**Mục tiêu**: Đánh giá hiệu quả trên tập dữ liệu test thực tế với các metrics đầy đủ.

**Nội dung**:
- Đánh giá trên toàn bộ tập dữ liệu test (format: `{label}_{filename}`)
- Tính toán: Accuracy, Precision, Recall, F1-Score
- Confusion Matrix
- Per-class metrics (cho ChatGPT và Human riêng biệt)
- Classification Report chi tiết

**Chạy test**:
```bash
# Sử dụng đường dẫn mặc định
python tests/test_evaluation.py --test-case 2

# Hoặc chỉ định đường dẫn cụ thể
python tests/test_evaluation.py --test-case 2 --test-data DATASETS/RQ1/C1/CONF/testing_data

# Với model đã huấn luyện
python tests/test_evaluation.py --test-case 2 --model-path ./results/checkpoint-1000
```

**Kết quả mong đợi**:
- Accuracy > 0.70 (70%) cho mô hình được huấn luyện tốt
- F1-Score > 0.70 cho cả hai lớp
- Confusion matrix cân đối, không có bias nghiêm trọng về một lớp

**Output mẫu**:
```
EVALUATION REPORT - GPTSniffer
================================================================================
Model Source: checkpoint:./results/checkpoint-1000
Device: cuda
Total Files Evaluated: 295

--- Overall Metrics ---
Accuracy:  0.8542 (85.42%)
Precision: 0.8621
Recall:    0.8542
F1-Score:  0.8581

--- Per-Class Metrics ---
ChatGPT (0):
  Precision: 0.8456
  Recall:    0.8923
  F1-Score:  0.8682

Human (1):
  Precision: 0.8786
  Recall:    0.8161
  F1-Score:  0.8462
```

---

### Test Case 3: Edge Cases (Các trường hợp đặc biệt)

**Mục tiêu**: Đánh giá khả năng xử lý các trường hợp đặc biệt và giới hạn.

**Nội dung**:
- Code rất ngắn (chỉ một dòng)
- Code rất dài (>512 tokens, cần truncation)
- Code có nhiều comments
- Code trống hoặc chỉ có whitespace
- Code có ký tự đặc biệt

**Chạy test**:
```bash
python tests/test_evaluation.py --test-case 3
```

**Kết quả mong đợi**:
- Mô hình không crash với các input đặc biệt
- Xử lý được truncation cho code dài
- Xử lý được empty/whitespace input
- Đưa ra dự đoán hợp lý cho các trường hợp biên

---

### Test Case 4: API Integration Tests (Test tích hợp API)

**Mục tiêu**: Đánh giá hiệu quả của Web API và các endpoints.

**Nội dung**:
- **4a. Health Endpoint**: Test `/health` endpoint
- **4b. Predict Endpoint**: Test `/predict` với JSON payload
- **4c. Predict File Endpoint**: Test `/predict-file` với file upload
- **4d. Error Handling**: Test xử lý lỗi (empty code, missing fields)
- **4e. Performance**: Test độ trễ và thời gian phản hồi

**Yêu cầu**: API server phải đang chạy

**Chạy test**:
```bash
# Khởi động API server trước (trong terminal khác)
cd webapp/server
python main.py

# Sau đó chạy test (trong terminal khác)
python tests/test_api.py --url http://localhost:8000
```

**Kết quả mong đợi**:
- Tất cả endpoints trả về status code 200 (trừ error handling)
- Response format đúng cấu trúc
- Average latency < 1000ms cho mỗi request
- Error handling trả về status code 400 cho input không hợp lệ

---

## Chạy tất cả test cases

Sử dụng script tổng hợp để chạy tất cả test cases:

```bash
# Chạy tất cả test cases
python tests/run_all_tests.py

# Chỉ chạy một số test cases cụ thể
python tests/run_all_tests.py --test-cases 1 2 3

# Chạy với model đã huấn luyện
python tests/run_all_tests.py --model-path ./results/checkpoint-1000

# Bỏ qua API tests (khi server chưa chạy)
python tests/run_all_tests.py --skip-api

# Chỉ định đường dẫn test data
python tests/run_all_tests.py --test-data DATASETS/RQ1/C2/CONF/testing_data
```

## Cấu trúc dữ liệu test

Dữ liệu test có format như sau:
```
CONF/
├── training_data/
│   ├── 0_filename1.java  # ChatGPT-generated (label = 0)
│   ├── 1_filename2.java  # Human-written (label = 1)
│   └── ...
└── testing_data/
    ├── 0_filename1.java
    ├── 1_filename2.java
    └── ...
```

**Lưu ý**:
- File name bắt đầu với `0_` = Mã do ChatGPT tạo
- File name bắt đầu với `1_` = Mã do con người viết

## Kết quả đánh giá

Kết quả được lưu trong `tests/results/evaluation_results_TIMESTAMP.json` với cấu trúc:

```json
{
  "timestamp": "2025-01-11T10:30:00",
  "config": {
    "test_cases": [1, 2, 3, 4],
    "test_data_path": "DATASETS/RQ1/C1/CONF/testing_data",
    "model_path": null,
    "api_url": "http://localhost:8000"
  },
  "test_case_1": {
    "chatgpt_prediction": {...},
    "human_prediction": {...}
  },
  "test_case_2": {
    "accuracy": 0.8542,
    "f1_score": 0.8581,
    "confusion_matrix": [[...], [...]],
    ...
  },
  "test_case_3": [...],
  "test_case_4": {...}
}
```

## Đánh giá hiệu quả thực tế

### Tiêu chí đánh giá tốt:

1. **Accuracy > 80%**: Mô hình có độ chính xác cao
2. **F1-Score > 0.75**: Cân bằng giữa precision và recall
3. **Per-class F1 > 0.70**: Không có bias nghiêm trọng về một lớp
4. **API latency < 1000ms**: Phản hồi nhanh trong môi trường production
5. **Xử lý edge cases tốt**: Không crash với input đặc biệt

### Các vấn đề cần lưu ý:

- **Overfitting**: Nếu accuracy trên training data cao nhưng test data thấp
- **Class imbalance**: Nếu một lớp được dự đoán tốt hơn lớp kia nhiều
- **False positives/negatives**: Tỷ lệ dự đoán sai cao cho một lớp có thể gây vấn đề trong thực tế

## Troubleshooting

### Lỗi: "Cannot connect to API server"
- Đảm bảo API server đang chạy: `cd webapp/server && python main.py`
- Kiểm tra URL trong `--api-url`

### Lỗi: "Test data path not found"
- Kiểm tra đường dẫn đến thư mục test data
- Đảm bảo format file đúng: `{label}_{filename}.java`

### Lỗi: "CUDA out of memory"
- Sử dụng CPU: Thêm `device='cpu'` trong code
- Giảm batch size trong training script

### Lỗi: Import errors
- Cài đặt dependencies: `pip install torch transformers scikit-learn requests`
- Kiểm tra Python version >= 3.7

## Tài liệu tham khảo

- [GPTSniffer Paper](https://www.sciencedirect.com/science/article/pii/S0164121224001043)
- [CodeBERT Documentation](https://github.com/microsoft/CodeBERT)
- [Transformers Library](https://huggingface.co/docs/transformers)

## Liên hệ

Nếu có vấn đề hoặc câu hỏi, vui lòng liên hệ:
- phuong.nguyen@univaq.it
- juri.dirocco@univaq.it

