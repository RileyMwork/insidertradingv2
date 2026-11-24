
#!/usr/bin/env bash

# Ensure this script is executable.
chmod +x "$0"

set -Eeuo pipefail

# Navigate to the repository directory.
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "========================================"
echo "Updating InsiderTradingV2"
echo "========================================"

# ----------------------------------------
# 1. Check required commands
# ----------------------------------------

echo ""
echo "[1/8] Checking system requirements..."

for command in git python3; do
    if ! command -v "$command" >/dev/null 2>&1; then
        echo "ERROR: $command is not installed."
        exit 1
    fi
done

# ----------------------------------------
# 2. Check Git working tree
# ----------------------------------------

echo ""
echo "[2/8] Checking Git status..."

if ! git diff --quiet -- . ':(exclude)data/insider_trading_v2.db' ||
   ! git diff --cached --quiet -- . ':(exclude)data/insider_trading_v2.db' ||
   [ -n "$(git ls-files --others --exclude-standard)" ]; then
    echo "ERROR: You have local changes or untracked files."
    git status --short
    exit 1
fi

# ----------------------------------------
# 3. Pull latest changes
# ----------------------------------------

echo ""
echo "[3/8] Pulling latest changes from GitHub..."

git fetch origin
git pull --ff-only origin main

# ----------------------------------------
# 4. Check Python version
# ----------------------------------------

echo ""
echo "[4/8] Checking Python version..."

PYTHON_VERSION="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"

if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 13) else 1)'; then
    echo "ERROR: Python 3.13 or newer is required."
    echo "Detected Python version: $PYTHON_VERSION"
    exit 1
fi

echo "Python $PYTHON_VERSION detected."

# ----------------------------------------
# 5. Create and activate virtual environment
# ----------------------------------------

echo ""
echo "[5/8] Setting up virtual environment..."

if [ ! -f ".venv/bin/activate" ]; then
    echo "Virtual environment not found. Creating one..."

    python3 -m venv .venv
fi

source .venv/bin/activate

# ----------------------------------------
# 6. Install dependencies
# ----------------------------------------

echo ""
echo "[6/8] Installing dependencies..."

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

python -m pip check

# ----------------------------------------
# 7. Format and validate code
# ----------------------------------------

echo ""
echo "[7/8] Formatting and checking code..."

ruff format .
ruff check .
mypy src

# ----------------------------------------
# 8. Run tests
# ----------------------------------------

echo ""
echo "[8/8] Running tests..."

pytest

# ----------------------------------------
# Finished
# ----------------------------------------

echo "========================================"
echo "Update and validation completed!"
echo "========================================"
