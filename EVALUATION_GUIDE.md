# Hướng dẫn Đánh giá Hiệu quả GPTSniffer

## Tổng quan

Tài liệu này hướng dẫn cách nghiên cứu codebase, chạy dự án và đánh giá hiệu quả thực tế của hệ thống GPTSniffer.

## 1. Nghiên cứu Codebase

### Cấu trúc dự án

```
GPTSniffer/
├── GPTSniffer/              # Core implementation
│   ├── gptsniffer.py       # Training script chính
│   └── preprocessing_rules.py
├── DATASETS/                # Datasets cho các nghiên cứu
│   ├── RQ1/                # Research Question 1
│   ├── RQ2/                # Research Question 2
│   └── RQ3/                # Research Question 3
├── webapp/                  # Web application
│   ├── server/
│   │   └── main.py         # FastAPI server
│   └── static/
│       └── index.html      # Web UI
├── tests/                   # Test cases
│   ├── test_evaluation.py  # Evaluation tests
│   ├── test_api.py         # API tests
│   ├── run_all_tests.py    # Test runner
│   └── README.md           # Test documentation
└── README.md               # Tài liệu chính
```

### Các thành phần chính

1. **GPTSniffer Core** (`GPTSniffer/gptsniffer.py`):
   - Sử dụng CodeBERT từ Microsoft làm base model
   - Fine-tune trên dataset mã nguồn
   - Phân loại nhị phân: ChatGPT (0) vs Human (1)

2. **Web API** (`webapp/server/main.py`):
   - FastAPI server
   - Endpoints: `/health`, `/predict`, `/predict-file`
   - Hỗ trợ JSON payload và file upload

3. **Datasets**:
   - Format: `{label}_{filename}.java`
   - `0_` = ChatGPT-generated
   - `1_` = Human-written

## 2. Cài đặt và Chạy Dự án

### Yêu cầu hệ thống

```bash
Python >= 3.7
CUDA (optional, cho GPU acceleration)
```

### Cài đặt dependencies

```bash
pip install torch transformers scikit-learn pandas numpy matplotlib requests fastapi uvicorn
```

Hoặc sử dụng file requirements:
```bash
pip install -r tests/requirements.txt
```

### Chạy Training Script

```bash
# Chạy training với dataset C1
cd DATASETS/RQ1/C1
python gptsniffer.py
```

Script sẽ:
1. Load CodeBERT model
2. Load training data từ `CONF/training_data/`
3. Fine-tune model trong 12 epochs
4. Evaluate trên test data từ `CONF/testing_data/`
5. In confusion matrix và classification report

### Chạy Web API

```bash
# Terminal 1: Khởi động API server
cd webapp/server
python main.py

# Server sẽ chạy tại http://localhost:8000
```

Truy cập giao diện web tại: `http://localhost:8000`

### Sử dụng Model đã huấn luyện

```bash
# Set environment variable
export MODEL_DIR=./results/checkpoint-1000

# Hoặc trong Windows PowerShell
$env:MODEL_DIR=".\results\checkpoint-1000"

# Sau đó chạy API server
python webapp/server/main.py
```

## 3. Đánh giá Hiệu quả

### Test Cases được thiết kế

#### ✅ Test Case 1: Basic Prediction
**Mục tiêu**: Kiểm tra khả năng dự đoán cơ bản

```bash
python tests/test_evaluation.py --test-case 1
```

**Đánh giá**:
- ✓ Mô hình có thể dự đoán được label
- ✓ Confidence score hợp lý (> 0.5)
- ✓ Probabilities được tính đúng

#### ✅ Test Case 2: Dataset Evaluation
**Mục tiêu**: Đánh giá trên tập dữ liệu test thực tế

```bash
python tests/test_evaluation.py --test-case 2 --test-data DATASETS/RQ1/C1/CONF/testing_data
```

**Metrics đánh giá**:
- **Accuracy**: Tỷ lệ dự đoán đúng tổng thể
- **Precision**: Độ chính xác của dự đoán dương tính
- **Recall**: Tỷ lệ phát hiện đúng các trường hợp thực tế
- **F1-Score**: Trung bình điều hòa của Precision và Recall
- **Confusion Matrix**: Ma trận nhầm lẫn
- **Per-class Metrics**: Metrics cho từng lớp riêng biệt

**Tiêu chí đánh giá tốt**:
- Accuracy > 80%
- F1-Score > 0.75 cho cả hai lớp
- Không có bias nghiêm trọng (balanced precision/recall)

#### ✅ Test Case 3: Edge Cases
**Mục tiêu**: Đánh giá khả năng xử lý các trường hợp đặc biệt

```bash
python tests/test_evaluation.py --test-case 3
```

**Các trường hợp test**:
- Code rất ngắn (< 10 tokens)
- Code rất dài (> 512 tokens)
- Code có nhiều comments
- Code trống/whitespace
- Code có ký tự đặc biệt

**Đánh giá**:
- ✓ Không crash với input đặc biệt
- ✓ Xử lý truncation tốt
- ✓ Đưa ra dự đoán hợp lý

#### ✅ Test Case 4: API Integration
**Mục tiêu**: Đánh giá hiệu quả Web API

```bash
# Đảm bảo API server đang chạy
python tests/test_api.py --url http://localhost:8000
```

**Các test**:
- Health endpoint
- Predict endpoint (JSON)
- Predict file endpoint
- Error handling
- Performance (latency)

**Đánh giá**:
- ✓ Tất cả endpoints hoạt động
- ✓ Response format đúng
- ✓ Average latency < 1000ms
- ✓ Error handling đúng

### Chạy tất cả Test Cases

```bash
python tests/run_all_tests.py
```

Script sẽ:
1. Chạy tất cả test cases
2. In báo cáo chi tiết
3. Lưu kết quả vào `tests/results/evaluation_results_TIMESTAMP.json`

### Phân tích Kết quả

#### Kết quả tốt:
```
Accuracy:  0.8542 (85.42%)
F1-Score:  0.8581

ChatGPT (0):
  Precision: 0.8456
  Recall:    0.8923
  F1-Score:  0.8682

Human (1):
  Precision: 0.8786
  Recall:    0.8161
  F1-Score:  0.8462
```

#### Các vấn đề cần chú ý:

1. **Low Accuracy (< 70%)**:
   - Model chưa được fine-tune đủ
   - Dataset không phù hợp
   - Cần điều chỉnh hyperparameters

2. **Class Imbalance**:
   - Một lớp được dự đoán tốt hơn lớp kia nhiều
   - Cần balance dataset hoặc điều chỉnh loss function

3. **High False Positives/Negatives**:
   - Tỷ lệ dự đoán sai cao
   - Ảnh hưởng đến tính thực tế của hệ thống

## 4. Đánh giá Hiệu quả Thực tế

### Tiêu chí Đánh giá

| Metric | Mục tiêu | Ý nghĩa |
|--------|----------|---------|
| Accuracy | > 80% | Độ chính xác tổng thể cao |
| F1-Score | > 0.75 | Cân bằng giữa precision và recall |
| Per-class F1 | > 0.70 | Không có bias nghiêm trọng |
| API Latency | < 1000ms | Phản hồi nhanh trong production |
| Edge Cases | Pass all | Xử lý tốt các trường hợp đặc biệt |

### Báo cáo Đánh giá

Sau khi chạy tests, báo cáo sẽ bao gồm:

1. **Overall Metrics**: Accuracy, Precision, Recall, F1-Score
2. **Per-Class Metrics**: Metrics cho ChatGPT và Human riêng biệt
3. **Confusion Matrix**: Ma trận nhầm lẫn chi tiết
4. **Performance Metrics**: Latency, throughput
5. **Edge Case Results**: Kết quả xử lý các trường hợp đặc biệt

### So sánh với Baseline

Theo nghiên cứu gốc, GPTSniffer:
- Outperforms GPTZero
- Outperforms OpenAI Text Classifier
- Accuracy trên nhiều configurations đạt > 80%

## 5. Troubleshooting

### Lỗi thường gặp

**Lỗi: "CUDA out of memory"**
```bash
# Sử dụng CPU thay vì GPU
device = torch.device('cpu')
```

**Lỗi: "Cannot connect to API server"**
```bash
# Kiểm tra server đang chạy
cd webapp/server
python main.py
```

**Lỗi: "Model checkpoint not found"**
```bash
# Sử dụng base CodeBERT (không fine-tuned)
# Hoặc train model trước
python DATASETS/RQ1/C1/gptsniffer.py
```

**Lỗi: "Test data path not found"**
```bash
# Kiểm tra đường dẫn
# Đảm bảo format file đúng: {label}_{filename}.java
```

## 6. Kết luận

Hệ thống GPTSniffer được thiết kế để phát hiện mã nguồn do ChatGPT tạo với độ chính xác cao. Bộ test cases này cung cấp:

- ✅ Đánh giá toàn diện về hiệu quả
- ✅ Metrics chi tiết và báo cáo
- ✅ Test các trường hợp thực tế và edge cases
- ✅ Đánh giá API performance

Để có kết quả tốt nhất, nên:
1. Fine-tune model trên dataset phù hợp
2. Sử dụng model checkpoint đã được train
3. Chạy đầy đủ test cases để đánh giá toàn diện

## Tài liệu tham khảo

- [GPTSniffer Paper](https://www.sciencedirect.com/science/article/pii/S0164121224001043)
- [CodeBERT](https://github.com/microsoft/CodeBERT)
- [Transformers Documentation](https://huggingface.co/docs/transformers)

