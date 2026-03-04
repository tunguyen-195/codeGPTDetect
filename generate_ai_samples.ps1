# PowerShell script to generate AI code samples using Groq API
# Make sure you have set GROQ_API_KEY environment variable first!

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   AI CODE GENERATION - GROQ API" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if GROQ_API_KEY is set
if (-not $env:GROQ_API_KEY) {
    Write-Host "ERROR: GROQ_API_KEY not set!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please set your API key first:" -ForegroundColor Yellow
    Write-Host '  $env:GROQ_API_KEY = "gsk_your_key_here"' -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Get free API key at: https://console.groq.com/keys" -ForegroundColor Cyan
    exit 1
}

Write-Host "API Key: " -NoNewline
Write-Host "SET (${env:GROQ_API_KEY.Substring(0, 10)}...)" -ForegroundColor Green
Write-Host ""

# Check if venv exists
if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Expected: .venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    exit 1
}

# Activate venv
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1

# Check if groq is installed
Write-Host "Checking groq library..." -ForegroundColor Cyan
$groqInstalled = & python -m pip show groq 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Groq not installed. Installing..." -ForegroundColor Yellow
    & python -m pip install groq
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install groq" -ForegroundColor Red
        exit 1
    }
    Write-Host "Groq installed successfully!" -ForegroundColor Green
} else {
    Write-Host "Groq library: OK" -ForegroundColor Green
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Parse arguments
param(
    [int]$num = 2000,
    [int]$start = 0,
    [switch]$test
)

if ($test) {
    Write-Host "TEST MODE: Generating 10 samples..." -ForegroundColor Yellow
    Write-Host ""
    & python scripts/generate_ai_code_groq.py --num 10 --start 0
} else {
    Write-Host "FULL MODE: Generating $num samples starting from $start" -ForegroundColor Yellow
    Write-Host "Estimated time: $([math]::Round($num * 2.1 / 60, 1)) minutes" -ForegroundColor Cyan
    Write-Host ""
    
    # Ask for confirmation if generating many samples
    if ($num -ge 500 -and $start -eq 0) {
        $confirm = Read-Host "This will take ~$([math]::Round($num * 2.1 / 60, 1)) minutes. Continue? (y/n)"
        if ($confirm -ne 'y') {
            Write-Host "Cancelled." -ForegroundColor Yellow
            exit 0
        }
    }
    
    & python scripts/generate_ai_code_groq.py --num $num --start $start
}

# Check result
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "   GENERATION COMPLETED SUCCESSFULLY!" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host ""
    
    # Count generated files
    $aiFiles = Get-ChildItem "DATASETS\PYTHON\raw\ai" -Filter "*.py" -ErrorAction SilentlyContinue
    $count = if ($aiFiles) { $aiFiles.Count } else { 0 }
    
    Write-Host "Total AI samples generated: $count" -ForegroundColor Cyan
    Write-Host ""
    
    if ($count -ge 2000) {
        Write-Host "READY for next step!" -ForegroundColor Green
        Write-Host "Run: python scripts/prepare_dataset.py" -ForegroundColor Yellow
    } else {
        Write-Host "Progress: $count / 2000" -ForegroundColor Yellow
        if ($count -gt 0) {
            Write-Host "To continue, run: .\generate_ai_samples.ps1 -num $($2000 - $count) -start $count" -ForegroundColor Cyan
        }
    }
} else {
    Write-Host ""
    Write-Host "ERROR: Generation failed!" -ForegroundColor Red
    Write-Host "Check the error messages above." -ForegroundColor Yellow
    exit 1
}
