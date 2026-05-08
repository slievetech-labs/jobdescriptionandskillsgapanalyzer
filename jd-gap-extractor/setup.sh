#!/usr/bin/env bash
# setup.sh — one-shot environment setup
set -e

echo "📦 Creating virtual environment..."
python3 -m venv .venv

echo "⚡ Activating venv and installing dependencies..."
source .venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
pip install pytest -q

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Add your API key:   export ANTHROPIC_API_KEY='sk-ant-...'"
echo "  2. Run the demo:       python src/analyzer.py"
echo "  3. Run tests:          pytest tests/ -v"
echo ""
echo "Or open in VS Code and press F5 to launch with the debugger."
