
#!/usr/bin/env bash

set -e

echo "========================================"
echo "Updating InsiderTradingV2"
echo "========================================"

# Navigate to the repository directory.
cd "$(dirname "$0")"

# Pull latest changes from GitHub.
echo ""
echo "[1/7] Pulling latest changes..."

git pull --ff-only origin main

# Activate virtual environment.
echo ""
echo "[2/7] Activating virtual environment..."

source .venv/Scripts/Activate.ps1

# Install dependencies.
echo ""
echo "[3/7] Installing dependencies..."

python -m pip install -e ".[dev]"

# Check dependencies.
echo ""
echo "[4/7] Checking dependencies..."

python -m pip check

# Format code.
echo ""
echo "[5/7] Formatting code..."

ruff format .

# Run linting.
echo ""
echo "[6/7] Running Ruff and mypy..."

ruff check .
mypy src

# Run tests.
echo ""
echo "[7/7] Running tests..."

pytest

echo ""
echo "========================================"
echo "Update and validation completed!"
echo "========================================"
