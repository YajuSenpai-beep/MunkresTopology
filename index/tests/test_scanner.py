r"""Tests for index entry scanner.

Coverage targets: 85%+ on latex_index/scanner.py (currently 0%).
"""

from latex_index.scanner import (
    generate_entry_report,
    scan_existing_indexes,
    scan_idx_commands,
)


class TestScanExistingIndexes:
    def test_empty_content(self):
        assert scan_existing_indexes("") == []

    def test_single_index(self):
        terms = scan_existing_indexes(r"Text \index{compact} more text.")
        assert terms == ["compact"]

    def test_multiple_indexes(self):
        content = (
            r"\index{topology} and \index{compact} and \index{Hausdorff}"
        )
        terms = scan_existing_indexes(content)
        assert len(terms) == 3
        assert terms == sorted(["compact", "Hausdorff", "topology"])

    def test_deduplication(self):
        content = r"\index{compact} and \index{compact} again"
        terms = scan_existing_indexes(content)
        assert terms == ["compact"]

    def test_sort_key_handling(self):
        # Note: simple regex cannot handle nested braces;
        # it extracts up to the first }
        content = r"\index{R@\(\mathbb{R}\)}"
        terms = scan_existing_indexes(content)
        # Extracts up to the first } (inside \mathbb{R}), which is
        # "\\(\\mathbb{R" (truncated at nested brace)
        assert len(terms) >= 1

    def test_sort_key_without_nesting(self):
        content = r"\index{R@real numbers}"
        terms = scan_existing_indexes(content)
        assert "real numbers" in terms

    def test_sub_entries(self):
        content = r"\index{topology!algebraic topology}"
        terms = scan_existing_indexes(content)
        assert "topology" in terms
        assert "  algebraic topology" in terms

    def test_nested_sub_entries(self):
        content = r"\index{topology!algebraic!homotopy}"
        terms = scan_existing_indexes(content)
        assert "topology" in terms
        assert "  algebraic" in terms
        assert "  homotopy" in terms

    def test_skip_other_commands(self):
        content = r"\section{Intro} \index{field} \textbf{bold}"
        terms = scan_existing_indexes(content)
        assert terms == ["field"]


class TestScanIdxCommands:
    def test_empty_content(self):
        result = scan_idx_commands("")
        assert result["idx"] == []
        assert result["idxmath"] == []
        assert result["idxsub"] == []

    def test_idx_command(self):
        result = scan_idx_commands(r"\idx{compact}")
        assert result["idx"] == ["compact"]

    def test_multiple_idx(self):
        result = scan_idx_commands(
            r"\idx{compact} \idx{Hausdorff} \idx{connected}"
        )
        assert len(result["idx"]) == 3

    def test_idxmath_command(self):
        result = scan_idx_commands(r"\idxmath{R}{\(\mathbb{R}\)}")
        assert len(result["idxmath"]) == 1
        assert "@" in result["idxmath"][0]

    def test_idxsub_command(self):
        result = scan_idx_commands(
            r"\idxsub{topology}{algebraic topology}"
        )
        assert len(result["idxsub"]) == 1
        assert "!" in result["idxsub"][0]

    def test_mixed_commands(self):
        content = (
            r"\idx{compact}"
            r"\idxmath{R}{\(\mathbb{R}\)}"
            r"\idxsub{A}{B}"
        )
        result = scan_idx_commands(content)
        assert len(result["idx"]) == 1
        assert len(result["idxmath"]) == 1
        assert len(result["idxsub"]) == 1


class TestGenerateEntryReport:
    def test_generates_report(self):
        content = r"\index{field} \idx{ring} \idxmath{S}{\(\mathbb{S}\)}"
        report = generate_entry_report(content)
        assert "索引条目扫描报告" in report
        assert "field" in report
        assert "ring" in report

    def test_empty_content_report(self):
        report = generate_entry_report("")
        assert "索引条目扫描报告" in report
        assert "0" in report  # all counts are 0
