#!/bin/bash

echo "========================================"
echo "GPTSniffer v3.0 - Quick Start"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
echo ""

# Check if dependencies are installed
echo "Checking dependencies..."
if ! python -c "import fastapi" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt --quiet
    echo "Dependencies installed successfully!"
    echo ""
fi

# Check if database exists
if [ ! -f "gptsniffer.db" ]; then
    echo "Database not found. Running initialization..."
    python scripts/init_db.py
    echo ""
fi

# Start server
echo "========================================"
echo "Starting GPTSniffer v3.0..."
echo "========================================"
echo ""
echo "Web UI:   http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python -m app.main
