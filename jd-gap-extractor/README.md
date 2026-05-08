# JD Gap Analyser & Contract Clause Extractor

> **Powered by Claude API (Anthropic) · Python · VS Code · Live Streaming Terminal Output**

A production-ready CLI tool that uses the Claude API with **real-time streaming** to:

1. 📋 **Analyse Job Descriptions** — find missing sections, vague language, bias, and compensation gaps  
2. 📄 **Extract Contract Clauses** — pull every clause, flag risk levels, return structured JSON  
3. 🔍 **Cross-Gap Analysis** — compare a JD against its contract to surface discrepancies  

---

## Quick Start (30 seconds)

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/jd-gap-extractor.git
cd jd-gap-extractor

# 2. Setup (creates venv + installs deps)
bash setup.sh

# 3. Activate venv
source .venv/bin/activate          # macOS/Linux
# .venv\Scripts\activate           # Windows

# 4. Add your API key
export ANTHROPIC_API_KEY="your_api_key_here"

# 5. Run the demo (uses built-in sample data, no files needed)
python src/analyzer.py
```

---

## VS Code — Live Build & Debug

Open the project folder in VS Code:

```bash
code .
```

Then press **F5** (or go to Run → Start Debugging) and pick a launch config:

| Config | What it does |
|---|---|
| `▶ Demo (no args)` | Runs full demo with built-in sample data |
| `▶ Analyse JD only` | Analyses `sample_data/my_jd.txt` |
| `▶ Extract Contract clauses` | Extracts from `sample_data/my_contract.txt` |
| `▶ Full JD + Contract cross-gap` | Runs all 3 analyses end-to-end |

Streaming output appears **live in the integrated terminal** as Claude generates it.

---

## CLI Usage

```bash
# Demo mode (built-in samples)
python src/analyzer.py

# Analyse a JD file
python src/analyzer.py jd path/to/job_description.txt

# Extract clauses from a contract
python src/analyzer.py contract path/to/contract.txt

# Full analysis: JD gaps + contract extraction + cross-gap comparison
python src/analyzer.py both path/to/jd.txt path/to/contract.txt
```

---

## Project Structure

```
jd-gap-extractor/
├── src/
│   └── analyzer.py          # Main app — 3 Claude-powered features
├── sample_data/
│   ├── samples.py           # Built-in demo data
│   ├── my_jd.txt            # ← Replace with your JD
│   └── my_contract.txt      # ← Replace with your contract
├── tests/
│   └── test_analyzer.py     # pytest unit tests (mocked API)
├── .vscode/
│   ├── launch.json          # F5 debug configs
│   ├── settings.json        # Python interpreter + formatting
│   └── extensions.json      # Recommended extensions
├── requirements.txt
├── setup.sh
└── README.md
```

---

## How It Works

```
User Input (JD / Contract text)
        │
        ▼
Claude API (claude-sonnet-4-20250514)
  · Streaming enabled → text flows to terminal in real time
  · System prompts tuned for HR / legal analysis
        │
        ▼
JD Analysis    →  Markdown report (gaps, bias, recommendations)
Contract       →  Structured JSON (clauses, risk levels, red flags)
Cross-Gap      →  Comparison table + action items
```

The app uses **`client.messages.stream()`** from the `anthropic` SDK so every token prints to your terminal the moment Claude generates it — no waiting for the full response.

---

## Running Tests

```bash
pytest tests/ -v
```

Tests mock the Anthropic SDK — no API calls, no cost.

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | ✅ Yes | Your Anthropic API key |

Get a key at: https://console.anthropic.com/

---

## Recommended VS Code Extensions

- **Python** (`ms-python.python`)
- **Debugpy** (`ms-python.debugpy`)
- **Black Formatter** (`ms-python.black-formatter`)
- **Ruff** (`charliermarsh.ruff`)

Install all at once: `Ctrl+Shift+P` → *Extensions: Show Recommended Extensions*

---

## License

MIT
