# 🤖 HƯỚNG DẪN GENERATE AI CODE SAMPLES

## 📊 MỤC TIÊU
Generate **2000 AI Python code samples** để training model phát hiện AI-generated code

---

## 🎯 PHƯƠNG ÁN KHUYÊN DÙNG: GROQ API (NHANH + MIỄN PHÍ)

### ✅ Ưu điểm:
- ⚡ **CỰC NHANH**: ~2 samples/giây (100x nhanh hơn Hugging Face)
- 🆓 **MIỄN PHÍ**: 30 requests/phút = 1800 requests/giờ
- 🎯 **CHẤT LƯỢNG CAO**: Sử dụng Llama 3.3 70B
- ✅ **ỔN ĐỊNH**: Không bị timeout như HuggingFace

### 📝 HƯỚNG DẪN SỬ DỤNG GROQ:

#### Bước 1: Lấy API Key (MIỄN PHÍ)
1. Truy cập: https://console.groq.com/keys
2. Đăng ký tài khoản miễn phí (Google/GitHub)
3. Tạo API key mới
4. Copy key

#### Bước 2: Cài đặt thư viện
```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install Groq
pip install groq
```

#### Bước 3: Set API Key
```powershell
# PowerShell
$env:GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"

# Hoặc Linux/Mac
export GROQ_API_KEY="gsk_your_key_here"
```

#### Bước 4: Generate samples
```powershell
# Generate 2000 samples (mất ~35 phút)
python scripts/generate_ai_code_groq.py --num 2000

# Hoặc generate từng phần (100 samples = ~3.5 phút)
python scripts/generate_ai_code_groq.py --num 100 --start 0
python scripts/generate_ai_code_groq.py --num 100 --start 100
python scripts/generate_ai_code_groq.py --num 100 --start 200
# ... tiếp tục
```

#### ⏱️ Thời gian ước tính:
- 100 samples: ~3.5 phút
- 500 samples: ~17 phút
- 1000 samples: ~35 phút
- **2000 samples: ~70 phút (1.2 giờ)**

---

## 🐌 PHƯƠNG ÁN DỰ PHÒNG: HUGGING FACE INFERENCE (CHẬM)

### ⚠️ Nhược điểm:
- 🐢 CHẬM: ~30-60 giây/sample
- ⏳ TIMEOUT nhiều
- 🔄 Cần retry nhiều lần
- 📉 Chất lượng không ổn định

### 📝 Chỉ dùng khi:
- Không lấy được Groq API key
- Hoặc đã hết quota Groq (khó xảy ra)

### Hướng dẫn:
```powershell
# KHÔNG CẦN API KEY (nhưng có thì tốt hơn)
# Get token (optional): https://huggingface.co/settings/tokens

# Set token (optional)
$env:HF_TOKEN = "hf_your_token_here"

# Generate (RẤT CHẬM - 2000 samples = ~30-60 giờ)
python scripts/generate_ai_code_huggingface.py --num 2000
```

---

## 📊 KIỂM TRA TIẾN ĐỘ

### Xem số lượng files đã generate:
```powershell
# Count files
(Get-ChildItem DATASETS/PYTHON/raw/ai -File).Count

# List recent files
Get-ChildItem DATASETS/PYTHON/raw/ai -File | Select-Object -Last 10
```

### Xem nội dung file mẫu:
```powershell
# View first generated file
Get-Content DATASETS/PYTHON/raw/ai/0_ai_groq_0000.py
```

---

## 🎯 SAU KHI GENERATE XONG

### Bước tiếp theo:
1. ✅ Verify số lượng: Phải có **2000 files** trong `DATASETS/PYTHON/raw/ai/`
2. ✅ Check chất lượng: Xem ngẫu nhiên vài files
3. ✅ Run script split train/test:
   ```powershell
   python scripts/prepare_dataset.py
   ```

---

## 🆘 TROUBLESHOOTING

### Lỗi: "GROQ_API_KEY not found"
**Giải pháp:**
```powershell
# Kiểm tra key đã set chưa
echo $env:GROQ_API_KEY

# Nếu null, set lại
$env:GROQ_API_KEY = "gsk_your_key_here"
```

### Lỗi: "Rate limit exceeded"
**Giải pháp:**
- Đợi 1 phút rồi tiếp tục
- Hoặc dùng `--start` để resume từ vị trí bị dừng

### Lỗi: "groq module not found"
**Giải pháp:**
```powershell
.\.venv\Scripts\Activate.ps1
pip install groq
```

### Generation bị gián đoạn
**Giải pháp:**
```powershell
# Kiểm tra số files đã có
$count = (Get-ChildItem DATASETS/PYTHON/raw/ai -File).Count
echo "Generated: $count files"

# Resume từ vị trí đó
python scripts/generate_ai_code_groq.py --num 2000 --start $count
```

---

## 📈 TỐI ƯU HOÁ

### Parallel Generation (Advanced)
Nếu muốn nhanh hơn, chạy nhiều processes song song:

```powershell
# Terminal 1
python scripts/generate_ai_code_groq.py --num 500 --start 0

# Terminal 2
python scripts/generate_ai_code_groq.py --num 500 --start 500

# Terminal 3
python scripts/generate_ai_code_groq.py --num 500 --start 1000

# Terminal 4
python scripts/generate_ai_code_groq.py --num 500 --start 1500
```

⚠️ **Lưu ý**: Mỗi terminal cần set `GROQ_API_KEY` riêng!

---

## ✅ CHECKLIST

- [ ] Lấy Groq API key miễn phí
- [ ] Install groq library
- [ ] Set GROQ_API_KEY environment variable
- [ ] Run generation script
- [ ] Verify có đủ 2000 files
- [ ] Check quality của vài files ngẫu nhiên
- [ ] Tiếp tục bước tiếp theo: Split train/test

---

## 🚀 QUICK START (TL;DR)

```powershell
# 1. Get key: https://console.groq.com/keys
# 2. Install & set key
.\.venv\Scripts\Activate.ps1
pip install groq
$env:GROQ_API_KEY = "gsk_your_key_here"

# 3. Generate (70 phút)
python scripts/generate_ai_code_groq.py --num 2000

# 4. Verify
(Get-ChildItem DATASETS/PYTHON/raw/ai -File).Count  # Should be 2000
```

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề, kiểm tra:
1. API key đã đúng chưa
2. Internet connection ổn định
3. Virtual environment đã activate
4. Thư viện đã cài đặt đầy đủ

Good luck! 🎉
