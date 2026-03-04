# Start GPTSniffer Web Server with Fine-tuned Model

$env:MODEL_DIR="E:\Freelance\Research\D11_8_2025_GPTCodeDetetect\GPTSniffer\models\gptsniffer-finetuned"

Write-Host "Starting GPTSniffer Web Server..."
Write-Host "Model: $env:MODEL_DIR"
Write-Host "Server will be available at: http://localhost:8000"
Write-Host ""

Set-Location "E:\Freelance\Research\D11_8_2025_GPTCodeDetetect\GPTSniffer\webapp\server"
& "E:\Freelance\Research\D11_8_2025_GPTCodeDetetect\GPTSniffer\.venv\Scripts\uvicorn.exe" main:app --host 0.0.0.0 --port 8000
