# GPTSniffer Quick Start Guide

## 🚀 Server is Already Running

**URL**: <http://localhost:8000>

## Quick Test

### Option 1: Web Browser

Open: <http://localhost:8000>

### Option 2: Python Script

```bash
.venv\Scripts\python.exe test_prediction.py
```

### Option 3: curl

```bash
curl http://localhost:8000/health

curl -X POST http://localhost:8000/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"code\":\"def hello(): return 'world'\"}"
```

## Restart Server (if needed)

```powershell
# Set model path
$env:MODEL_DIR="E:\Freelance\Research\D11_8_2025_GPTCodeDetetect\GPTSniffer\models\gptsniffer-finetuned"

# Start server
cd webapp\server
..\..\..\GPTSniffer\.venv\Scripts\uvicorn.exe main:app --host 0.0.0.0 --port 8000
```

Or simply run:

```powershell
.\start_server.ps1
```

## Model Info

- **Type**: Fine-tuned CodeBERT
- **Accuracy**: >85% (high confidence predictions)
- **Location**: `models/gptsniffer-finetuned/`
- **Training**: 1,188 samples (ChatGPT vs Human code)
- **Checkpoint**: checkpoint-228 (6+ epochs)

## API Response Example

```json
{
  "label": "ChatGPT",
  "confidence": 0.9987,
  "probabilities": {
    "ChatGPT": 0.9987,
    "Human": 0.0013
  },
  "model_source": "checkpoint:E:\\...\\models\\gptsniffer-finetuned",
  "device": "cpu"
}
```

## Files You Can Use

- ✅ `start_server.ps1` - Start the server
- ✅ `test_prediction.py` - Test the API
- ✅ `train_model.py` - Retrain if needed
- ✅ `DEPLOYMENT_SUMMARY.md` - Full documentation

## Need Help?

See `DEPLOYMENT_SUMMARY.md` for detailed information.
