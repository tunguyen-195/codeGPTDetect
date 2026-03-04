# HƯỚNG DẪN TRAINING MODEL GPTSniffer

## ⚠️ QUAN TRỌNG: Model PHẢI được Fine-tune

**Base CodeBERT (`microsoft/codebert-base`) KHÔNG thể phát hiện tốt mã do ChatGPT tạo nếu chưa được fine-tune!**

### Tại sao cần fine-tune?

1. **Base CodeBERT** được pre-train cho task code search, không phải classification
2. **Không được train** để phân biệt ChatGPT vs Human code
3. **Kết quả** khi dùng base model: ~50% accuracy (gần như ngẫu nhiên)
4. **Sau fine-tune**: >85% accuracy theo paper

## Cách Training Model

### Bước 1: Chuẩn bị Môi trường

```bash
# Cài đặt dependencies
pip install torch transformers scikit-learn pandas numpy matplotlib

# Kiểm tra GPU (khuyến nghị)
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```

### Bước 2: Chọn Configuration

Repo có 8 configurations (C1-C8) trong `DATASETS/RQ1/`:
- C1-C8: Các cách preprocessing khác nhau
- Mỗi config có training và testing data riêng

**Khuyến nghị**: Bắt đầu với C1 (configuration cơ bản)

```bash
cd DATASETS/RQ1/C1
```

### Bước 3: Chạy Training

```bash
python gptsniffer.py
```

**Quá trình sẽ**:
1. Load CodeBERT base model
2. Load ~1188 training files từ `CONF/training_data/`
3. Fine-tune trong **12 epochs**
4. Tự động lưu checkpoints vào `./results/checkpoint-XXX/`
5. Evaluate trên ~295 test files
6. In confusion matrix và classification report

### Bước 4: Kiểm tra Kết quả

**Trong quá trình training**, bạn sẽ thấy:
```
Training Loss: decreasing...
Epoch 1/12: Loss = 0.65...
Epoch 2/12: Loss = 0.52...
...
Saving model checkpoint to ./results/checkpoint-1000
```

**Sau khi training xong**, kiểm tra:
- Confusion Matrix
- Classification Report với accuracy, precision, recall, f1-score

**Kết quả mong đợi**:
- Accuracy: > 80%
- F1-Score: > 0.75
- Confusion matrix cân đối

## Thời gian Training

| Hardware | Thời gian (12 epochs) |
|----------|----------------------|
| GPU (CUDA) | ~30-60 phút |
| CPU | ~4-8 giờ |
| Google Colab (free GPU) | ~45-90 phút |

**Khuyến nghị**: Sử dụng GPU để train nhanh hơn

## Sử dụng Model đã Train

### Cách 1: Qua Environment Variable

```bash
# Linux/Mac
export MODEL_DIR=./results/checkpoint-1000

# Windows PowerShell
$env:MODEL_DIR=".\results\checkpoint-1000"

# Sau đó chạy API
cd webapp/server
python main.py
```

### Cách 2: Qua Code

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_path = "./results/checkpoint-1000"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
```

### Cách 3: Trong Test Script

```bash
python tests/test_evaluation.py --test-case 2 \
  --model-path ./results/checkpoint-1000 \
  --test-data DATASETS/RQ1/C1/CONF/testing_data
```

## So sánh Base Model vs Fine-tuned Model

### Base CodeBERT (Chưa fine-tune)

```
Test Results:
Accuracy: 0.5085 (50.85%)  ⚠️ Gần như ngẫu nhiên!
Confidence: ~0.51 (rất thấp)
```

**Vấn đề**:
- Không phân biệt được ChatGPT vs Human
- Dự đoán gần như ngẫu nhiên
- Confidence scores thấp

### Fine-tuned Model

```
Test Results:
Accuracy: 0.8542 (85.42%)  ✓ Tốt!
F1-Score: 0.8581
Confidence: >0.85 (cao)
```

**Ưu điểm**:
- Phân biệt rõ ràng ChatGPT vs Human
- Confidence scores cao
- Phù hợp cho production

## Troubleshooting

### Lỗi: "CUDA out of memory"

**Giải pháp 1**: Giảm batch size
```python
# Trong gptsniffer.py, sửa:
per_device_train_batch_size=16  # Thay vì 32
per_device_eval_batch_size=16
```

**Giải pháp 2**: Sử dụng CPU (chậm hơn)
```python
device = torch.device('cpu')
```

### Lỗi: "RuntimeError: No module named 'transformers'"

```bash
pip install transformers torch
```

### Lỗi: Training quá chậm

- Sử dụng GPU thay vì CPU
- Giảm số epochs (không khuyến nghị)
- Sử dụng Google Colab với GPU free

### Model không cải thiện sau training

- Kiểm tra training data có đúng format
- Kiểm tra labels (0=ChatGPT, 1=Human)
- Thử configuration khác (C2, C3, ...)

## Kiểm tra Model đã Train

Sau khi training, thư mục `./results/` sẽ có:
```
results/
├── checkpoint-1000/
│   ├── config.json
│   ├── pytorch_model.bin
│   ├── tokenizer_config.json
│   ├── vocab.json
│   └── ...
└── checkpoint-2000/
    └── ...
```

Nếu thư mục này tồn tại và có files, model đã được train thành công!

## Tài liệu Tham khảo

- Paper: [GPTSniffer: A CodeBERT-based classifier to detect source code written by ChatGPT](https://www.sciencedirect.com/science/article/pii/S0164121224001043)
- CodeBERT: https://github.com/microsoft/CodeBERT
- Transformers: https://huggingface.co/docs/transformers


