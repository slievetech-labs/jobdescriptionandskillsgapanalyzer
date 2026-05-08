"""
Job Description Gap & Contract Extractor
Uses Claude API to analyze JDs and contracts, extract clauses, and find gaps.
"""

import anthropic
import json
import sys
from pathlib import Path
from typing import Optional


client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env


# ─────────────────────────────────────────────
# STREAMING HELPER
# ─────────────────────────────────────────────

def stream_claude(system: str, user: str, label: str = "") -> str:
    """Call Claude with streaming and print output live to terminal."""
    if label:
        print(f"\n{'─'*60}")
        print(f"  {label}")
        print(f"{'─'*60}")

    full_text = ""
    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=system,
        messages=[{"role": "user", "content": user}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full_text += text

    print()  # newline after streaming ends
    return full_text


# ─────────────────────────────────────────────
# FEATURE 1 — JD GAP ANALYSIS
# ─────────────────────────────────────────────

JD_GAP_SYSTEM = """You are an expert HR analyst and talent acquisition specialist.
Analyse the provided Job Description and identify:
1. MISSING ELEMENTS — critical JD sections that are absent or incomplete
2. VAGUE LANGUAGE — requirements that are unclear or unmeasurable
3. BIAS FLAGS — language that may discourage diverse candidates
4. SALARY/COMPENSATION — whether it is disclosed and competitive signals
5. RECOMMENDATIONS — concrete suggestions to strengthen the JD

Format your response with clear section headers using markdown."""


def analyze_jd_gaps(jd_text: str) -> str:
    return stream_claude(
        system=JD_GAP_SYSTEM,
        user=f"Analyse this Job Description for gaps and improvements:\n\n{jd_text}",
        label="📋  JD GAP ANALYSIS  (streaming live)",
    )


# ─────────────────────────────────────────────
# FEATURE 2 — CONTRACT CLAUSE EXTRACTION
# ─────────────────────────────────────────────

CONTRACT_SYSTEM = """You are a senior legal analyst specialising in employment contracts.
Extract and summarise ALL key clauses from the provided contract. For each clause:
- State the clause TYPE (e.g. Non-Compete, IP Assignment, Termination, etc.)
- Provide a plain-English SUMMARY (1-2 sentences)
- Flag any RISK LEVEL: 🟢 Standard | 🟡 Review | 🔴 High Risk
- Quote the exact contract LANGUAGE that triggered the flag

Return results as structured JSON with this schema:
{
  "clauses": [
    {
      "type": "string",
      "summary": "string",
      "risk_level": "Standard|Review|High Risk",
      "excerpt": "string"
    }
  ],
  "overall_risk": "Low|Medium|High",
  "red_flags": ["string"],
  "missing_standard_clauses": ["string"]
}
Return ONLY valid JSON, no markdown fences."""


def extract_contract_clauses(contract_text: str) -> dict:
    print(f"\n{'─'*60}")
    print("  📄  CONTRACT CLAUSE EXTRACTION  (streaming live)")
    print(f"{'─'*60}")

    full_text = ""
    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=CONTRACT_SYSTEM,
        messages=[{"role": "user", "content": f"Extract all clauses from this contract:\n\n{contract_text}"}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full_text += text

    print()

    try:
        return json.loads(full_text)
    except json.JSONDecodeError:
        return {"raw_output": full_text, "parse_error": "Could not parse JSON"}


# ─────────────────────────────────────────────
# FEATURE 3 — JD vs CONTRACT CROSS-GAP
# ─────────────────────────────────────────────

CROSS_GAP_SYSTEM = """You are an employment law and HR specialist.
You will receive a Job Description and an Employment Contract side-by-side.
Identify DISCREPANCIES and GAPS between the two documents:
- Responsibilities mentioned in JD but absent from contract
- Compensation/benefits promised in JD vs what's in the contract
- Role scope differences
- Any misleading or contradictory language

Format as a clear comparison table in markdown, then list action items."""


def cross_gap_analysis(jd_text: str, contract_text: str) -> str:
    return stream_claude(
        system=CROSS_GAP_SYSTEM,
        user=f"JOB DESCRIPTION:\n{jd_text}\n\n---\n\nEMPLOYMENT CONTRACT:\n{contract_text}",
        label="🔍  JD vs CONTRACT CROSS-GAP ANALYSIS  (streaming live)",
    )


# ─────────────────────────────────────────────
# CLI ENTRYPOINT
# ─────────────────────────────────────────────

def load_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def print_banner():
    print("""
╔══════════════════════════════════════════════════════════╗
║   JD Gap Analyser & Contract Extractor — Powered by Claude ║
╚══════════════════════════════════════════════════════════╝
""")


def main():
    print_banner()

    # ── Demo mode: use built-in samples if no args given ──
    if len(sys.argv) == 1:
        print("No files provided — running DEMO with sample data.\n")
        print("Usage:")
        print("  python src/analyzer.py jd <jd_file.txt>")
        print("  python src/analyzer.py contract <contract_file.txt>")
        print("  python src/analyzer.py both <jd_file.txt> <contract_file.txt>\n")

        from sample_data.samples import SAMPLE_JD, SAMPLE_CONTRACT
        print("Running full demo (JD → Contract → Cross-Gap)…")

        analyze_jd_gaps(SAMPLE_JD)
        result = extract_contract_clauses(SAMPLE_CONTRACT)

        print(f"\n{'─'*60}")
        print("  📊  PARSED CLAUSE SUMMARY")
        print(f"{'─'*60}")
        if "clauses" in result:
            for c in result["clauses"]:
                risk_icon = {"Standard": "🟢", "Review": "🟡", "High Risk": "🔴"}.get(c["risk_level"], "⚪")
                print(f"{risk_icon}  [{c['type']}]  {c['summary']}")
            print(f"\nOverall Risk: {result.get('overall_risk', 'N/A')}")
            if result.get("red_flags"):
                print(f"Red Flags: {', '.join(result['red_flags'])}")
        else:
            print(result.get("raw_output", "No output"))

        cross_gap_analysis(SAMPLE_JD, SAMPLE_CONTRACT)
        return

    mode = sys.argv[1].lower()

    if mode == "jd" and len(sys.argv) >= 3:
        jd = load_file(sys.argv[2])
        analyze_jd_gaps(jd)

    elif mode == "contract" and len(sys.argv) >= 3:
        contract = load_file(sys.argv[2])
        result = extract_contract_clauses(contract)
        print("\n\n📊 Parsed Summary:\n")
        print(json.dumps(result, indent=2))

    elif mode == "both" and len(sys.argv) >= 4:
        jd = load_file(sys.argv[2])
        contract = load_file(sys.argv[3])
        analyze_jd_gaps(jd)
        extract_contract_clauses(contract)
        cross_gap_analysis(jd, contract)

    else:
        print("❌ Invalid arguments.")
        print("Usage:")
        print("  python src/analyzer.py jd <jd_file.txt>")
        print("  python src/analyzer.py contract <contract_file.txt>")
        print("  python src/analyzer.py both <jd_file.txt> <contract_file.txt>")
        sys.exit(1)


if __name__ == "__main__":
    main()
