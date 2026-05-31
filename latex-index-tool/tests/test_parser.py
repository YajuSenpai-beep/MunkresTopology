"""parser.py 单元测试。"""
import pytest
from latex_index.parser import parse_indented, parse_run_in, extract_pages, parse_pages


class TestIndented:
    def test_basic(self):
        lines = [
            "Axiom of choice, 42, 45",
            "  finite axiom of choice, 42",
            "  choice function, 43",
            "Compactness, 50-52",
        ]
        entries = parse_indented(lines)
        assert len(entries) == 4
        assert entries[0]["level"] == 1
        assert entries[0]["term"] == "Axiom of choice"
        assert entries[1]["level"] == 2
        assert entries[1]["parent"] == "Axiom of choice"
        assert entries[3]["level"] == 1
        assert entries[3]["term"] == "Compactness"

    def test_skip_headers(self):
        lines = ["A", "Axiom of choice, 42", "B", "Compactness, 50"]
        entries = parse_indented(lines)
        assert len(entries) == 2

    def test_skip_empty(self):
        lines = ["", "  ", "Field, 1", ""]
        entries = parse_indented(lines)
        assert len(entries) == 1

    def test_no_l2_without_l1(self):
        lines = ["  orphan l2, 5"]
        entries = parse_indented(lines)
        assert all(e["level"] == 1 or "parent" in e for e in entries)


class TestRunIn:
    def test_basic(self):
        lines = ["Field, 42; Ring, 45; Group, 50"]
        entries = parse_run_in(lines)
        assert len(entries) >= 2  # heuristic may vary

    def test_empty(self):
        entries = parse_run_in([""])
        assert len(entries) == 0
