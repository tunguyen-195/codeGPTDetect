# Automatic AI Code Generation Script
# This script will automatically test and generate 2000 AI code samples

param(
    [string]$ApiKey = "YOUR_GROQ_API_KEY_HERE"
)

$ErrorActionPreference = "Stop"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   AUTOMATIC AI CODE GENERATION" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Set API key
$env:GROQ_API_KEY = $ApiKey
Write-Host "[1/5] API Key set: $($ApiKey.Substring(0,10))..." -ForegroundColor Green

# Navigate to project directory
Set-Location "E:\Freelance\Research\D11_8_2025_GPTCodeDetetect\GPTSniffer"
Write-Host "[2/5] Working directory: $(Get-Location)" -ForegroundColor Green

# Activate virtual environment
Write-Host "[3/5] Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Install groq if needed
Write-Host "[4/5] Checking dependencies..." -ForegroundColor Yellow
$groqCheck = & python -m pip show groq 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Installing groq..." -ForegroundColor Yellow
    & python -m pip install groq -q
    Write-Host "  Groq installed!" -ForegroundColor Green
} else {
    Write-Host "  Groq already installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   STEP 1: TESTING API CONNECTION (10 samples)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Test with 10 samples
Write-Host "Testing with 10 samples (~20 seconds)..." -ForegroundColor Yellow
& python scripts/generate_ai_code_groq.py --num 10 --start 0

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Test generation failed!" -ForegroundColor Red
    Write-Host "Please check the error messages above." -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Test PASSED! API is working correctly." -ForegroundColor Green
Write-Host ""

# Ask for confirmation
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   STEP 2: FULL GENERATION (2000 samples)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This will generate 1990 more samples (~70 minutes total)" -ForegroundColor Yellow
Write-Host ""

$confirmation = Read-Host "Continue with full generation? (y/n)"

if ($confirmation -ne 'y') {
    Write-Host "Cancelled by user." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Starting full generation..." -ForegroundColor Green
Write-Host "Progress will be saved. You can stop and resume anytime." -ForegroundColor Cyan
Write-Host ""

# Generate remaining 1990 samples
& python scripts/generate_ai_code_groq.py --num 1990 --start 10

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Generation failed!" -ForegroundColor Red
    
    # Check how many files were generated
    $count = (Get-ChildItem "DATASETS\PYTHON\raw\ai" -Filter "*.py" -ErrorAction SilentlyContinue).Count
    Write-Host "Files generated so far: $count" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To resume, run:" -ForegroundColor Cyan
    Write-Host "  python scripts/generate_ai_code_groq.py --num $(2000 - $count) --start $count" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "   GENERATION COMPLETED!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

# Verify file count
$aiFiles = Get-ChildItem "DATASETS\PYTHON\raw\ai" -Filter "*.py" -ErrorAction SilentlyContinue
$count = if ($aiFiles) { $aiFiles.Count } else { 0 }

Write-Host "Total AI samples: $count" -ForegroundColor Cyan
Write-Host ""

if ($count -ge 2000) {
    Write-Host "SUCCESS! All 2000 samples generated!" -ForegroundColor Green
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "   NEXT STEP: PREPARE DATASET" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Run the following command to split train/test:" -ForegroundColor Yellow
    Write-Host "  python scripts/prepare_dataset.py" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "WARNING: Expected 2000 samples, got $count" -ForegroundColor Yellow
    Write-Host "To generate remaining samples:" -ForegroundColor Cyan
    Write-Host "  python scripts/generate_ai_code_groq.py --num $(2000 - $count) --start $count" -ForegroundColor Yellow
}
