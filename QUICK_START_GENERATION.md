# 🚀 QUICK START: GENERATE AI CODE SAMPLES

## ⚡ CÁCH NHANH NHẤT (Dùng PowerShell Script)

### 1. Mở PowerShell trong thư mục project
```powershell
cd E:\Freelance\Research\D11_8_2025_GPTCodeDetetect\GPTSniffer
```

### 2. Set API Key (nếu chưa set)
```powershell
$env:GROQ_API_KEY = "gsk_your_key_here"
```
### 3. Chạy script

#### Test trước (10 samples, 20 giây):
```powershell
.\generate_ai_samples.ps1 -test
```

#### Generate full (2000 samples, 70 phút):
```powershell
.\generate_ai_samples.ps1
```

#### Generate từng phần (ví dụ 500 samples):
```powershell
.\generate_ai_samples.ps1 -num 500 -start 0
```

---

## 📝 HOẶC CHẠY TRỰC TIẾP (Manual)

### 1. Activate virtual environment
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Ensure groq is installed
```powershell
pip install groq
```

### 3. Set API key (nếu chưa)
```powershell
$env:GROQ_API_KEY = "gsk_your_key_here"
```

### 4. Run generation
```powershell
# Test với 10 samples
python scripts/generate_ai_code_groq.py --num 10 --start 0

# Full 2000 samples
python scripts/generate_ai_code_groq.py --num 2000 --start 0
```

---

## 🔍 KIỂM TRA TIẾN ĐỘ

### Đếm số files đã generate:
```powershell
(Get-ChildItem DATASETS\PYTHON\raw\ai -File).Count
```

### Xem file mẫu:
```powershell
Get-Content DATASETS\PYTHON\raw\ai\0_ai_groq_0000.py
```

### Xem 10 files gần nhất:
```powershell
Get-ChildItem DATASETS\PYTHON\raw\ai -File | Sort-Object LastWriteTime -Descending | Select-Object -First 10
```

---

## ⏸️ NẾU BỊ GIÁN ĐOẠN

### Kiểm tra đã generate bao nhiêu:
```powershell
$count = (Get-ChildItem DATASETS\PYTHON\raw\ai -File).Count
Write-Host "Generated: $count / 2000"
```

### Resume từ vị trí đó:
```powershell
$count = (Get-ChildItem DATASETS\PYTHON\raw\ai -File).Count
.\generate_ai_samples.ps1 -num (2000 - $count) -start $count
```

---

## 🚀 TĂNG TỐC (Advanced)

### Chạy parallel với 4 terminals:

**Terminal 1:**
```powershell
cd E:\Freelance\Research\D11_8_2025_GPTCodeDetetect\GPTSniffer
$env:GROQ_API_KEY = "your_key"
.\generate_ai_samples.ps1 -num 500 -start 0
```

**Terminal 2:**
```powershell
cd E:\Freelance\Research\D11_8_2025_GPTCodeDetetect\GPTSniffer
$env:GROQ_API_KEY = "your_key"
.\generate_ai_samples.ps1 -num 500 -start 500
```

**Terminal 3:**
```powershell
cd E:\Freelance\Research\D11_8_2025_GPTCodeDetetect\GPTSniffer
$env:GROQ_API_KEY = "your_key"
.\generate_ai_samples.ps1 -num 500 -start 1000
```

**Terminal 4:**
```powershell
cd E:\Freelance\Research\D11_8_2025_GPTCodeDetetect\GPTSniffer
$env:GROQ_API_KEY = "your_key"
.\generate_ai_samples.ps1 -num 500 -start 1500
```

**Thời gian:** Từ 70 phút → 20 phút! ⚡

---

## ✅ SAU KHI HOÀN THÀNH

### Verify có đủ 2000 files:
```powershell
$count = (Get-ChildItem DATASETS\PYTHON\raw\ai -File).Count
if ($count -ge 2000) {
    Write-Host "SUCCESS: $count files generated!" -ForegroundColor Green
    Write-Host "Next step: python scripts/prepare_dataset.py" -ForegroundColor Cyan
} else {
    Write-Host "WARNING: Only $count files generated" -ForegroundColor Yellow
}
```

### Chạy bước tiếp theo:
```powershell
python scripts/prepare_dataset.py
```

---

## 🆘 TROUBLESHOOTING

### Lỗi: "GROQ_API_KEY not found"
```powershell
# Check current value
echo $env:GROQ_API_KEY

# Set again
$env:GROQ_API_KEY = "gsk_your_key_here"
```

### Lỗi: "cannot be loaded because running scripts is disabled"
```powershell
# Run PowerShell as Administrator, then:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Lỗi: "Rate limit exceeded"
**Giải pháp:** Đợi 1 phút, sau đó resume với `--start` parameter

### Generation chậm bất thường
**Kiểm tra:** Internet connection, Groq API status

---

## 📊 EXPECTED OUTPUT

Sau khi hoàn thành, bạn sẽ có:
- `DATASETS/PYTHON/raw/ai/` chứa 2000 files
- Mỗi file có format: `0_ai_groq_XXXX.py`
- Mỗi file chứa Python code với metadata

**Example file structure:**
```python
"""
AI-Generated Code using Groq API
Model: llama-3.3-70b-versatile
Category: Data Structures
Difficulty: medium
Prompt: Write a Python class to implement a Binary Search Tree...
"""

class BinarySearchTree:
    def __init__(self):
        ...
```

---

## 🎯 TL;DR (Cách nhanh nhất)

```powershell
cd E:\Freelance\Research\D11_8_2025_GPTCodeDetetect\GPTSniffer
$env:GROQ_API_KEY = "your_key"
.\generate_ai_samples.ps1 -test  # Test first (20s)
.\generate_ai_samples.ps1        # Then run full (70min)
```

Good luck! 🚀
