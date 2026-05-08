"""
Tests for the JD Gap & Contract Extractor.
Run with:  pytest tests/ -v
"""

import json
import pytest
from unittest.mock import MagicMock, patch
from src.analyzer import analyze_jd_gaps, extract_contract_clauses, cross_gap_analysis


# ── Fixtures ───────────────────────────────────────────────────────────────

MINIMAL_JD = "We need a Python developer with 3 years experience."

MINIMAL_CONTRACT = json.dumps({
    "clauses": [
        {
            "type": "Termination",
            "summary": "At-will employment.",
            "risk_level": "Standard",
            "excerpt": "Employment is at-will."
        }
    ],
    "overall_risk": "Low",
    "red_flags": [],
    "missing_standard_clauses": []
})


def make_mock_stream(text: str):
    """Return a mock streaming context manager that yields characters."""
    mock_stream = MagicMock()
    mock_stream.__enter__ = MagicMock(return_value=mock_stream)
    mock_stream.__exit__ = MagicMock(return_value=False)
    mock_stream.text_stream = iter(list(text))
    return mock_stream


# ── JD Gap Analysis ────────────────────────────────────────────────────────

class TestJDGapAnalysis:
    @patch("src.analyzer.client")
    def test_returns_string(self, mock_client):
        mock_client.messages.stream.return_value = make_mock_stream("## Missing Elements\n- Salary not disclosed")
        result = analyze_jd_gaps(MINIMAL_JD)
        assert isinstance(result, str)
        assert len(result) > 0

    @patch("src.analyzer.client")
    def test_calls_claude_api(self, mock_client):
        mock_client.messages.stream.return_value = make_mock_stream("Some analysis")
        analyze_jd_gaps(MINIMAL_JD)
        mock_client.messages.stream.assert_called_once()
        call_kwargs = mock_client.messages.stream.call_args[1]
        assert call_kwargs["model"].startswith("claude")
        assert any(MINIMAL_JD in m["content"] for m in call_kwargs["messages"])


# ── Contract Clause Extraction ─────────────────────────────────────────────

class TestContractExtraction:
    @patch("src.analyzer.client")
    def test_returns_dict(self, mock_client):
        mock_client.messages.stream.return_value = make_mock_stream(MINIMAL_CONTRACT)
        result = extract_contract_clauses("At-will employment contract.")
        assert isinstance(result, dict)

    @patch("src.analyzer.client")
    def test_parses_clauses(self, mock_client):
        mock_client.messages.stream.return_value = make_mock_stream(MINIMAL_CONTRACT)
        result = extract_contract_clauses("At-will employment contract.")
        assert "clauses" in result
        assert len(result["clauses"]) > 0
        assert result["clauses"][0]["type"] == "Termination"

    @patch("src.analyzer.client")
    def test_handles_bad_json(self, mock_client):
        mock_client.messages.stream.return_value = make_mock_stream("NOT JSON AT ALL")
        result = extract_contract_clauses("Contract text")
        assert "parse_error" in result


# ── Cross-Gap Analysis ─────────────────────────────────────────────────────

class TestCrossGapAnalysis:
    @patch("src.analyzer.client")
    def test_returns_string(self, mock_client):
        mock_client.messages.stream.return_value = make_mock_stream("| Discrepancy | JD | Contract |\n|---|---|---|")
        result = cross_gap_analysis(MINIMAL_JD, "Employment contract text.")
        assert isinstance(result, str)

    @patch("src.analyzer.client")
    def test_both_texts_in_prompt(self, mock_client):
        mock_client.messages.stream.return_value = make_mock_stream("Analysis result")
        cross_gap_analysis("JD text here", "Contract text here")
        call_kwargs = mock_client.messages.stream.call_args[1]
        user_content = call_kwargs["messages"][0]["content"]
        assert "JD text here" in user_content
        assert "Contract text here" in user_content
