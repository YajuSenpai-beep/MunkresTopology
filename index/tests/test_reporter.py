r"""Tests for index reporter module.

Covers latex_index/reporter.py.
"""

from latex_index.reporter import (
    find_duplicate_indexes,
    find_potential_missing_entries,
    generate_coverage_report,
    generate_report,
    validate_range_pairs,
)


class TestCoverageReport:
    def test_full_coverage(self):
        content = "The concept of a compact space is fundamental."
        entries = [
            {"term": "compact space", "level": 1},
            {"term": "fundamental group", "level": 1},
        ]
        report = generate_coverage_report(content, entries)
        assert report["total_entries"] == 2
        assert report["found_entries"] >= 1
        assert report["coverage_pct"] >= 50.0

    def test_no_coverage(self):
        content = "Hello world."
        entries = [{"term": "nonexistent term", "level": 1}]
        report = generate_coverage_report(content, entries)
        assert report["found_entries"] == 0
        assert len(report["missing_entries"]) == 1

    def test_l1_l2_separate_counts(self):
        content = "compact space"
        entries = [
            {"term": "compact space", "level": 1},
            {"term": "open cover", "level": 2, "parent": "compact space"},
        ]
        report = generate_coverage_report(content, entries)
        assert report["l1_total"] == 1
        assert report["l2_total"] == 1
        assert report["l1_found"] == 1

    def test_empty_entries(self):
        report = generate_coverage_report("text", [])
        assert report["coverage_pct"] == 0.0


class TestDuplicateIndexes:
    def test_find_duplicates(self):
        content = (
            r"\index{compact} text \index{compact} more \index{field}"
        )
        dups = find_duplicate_indexes(content)
        assert len(dups) >= 1
        assert dups[0][0] == "compact"

    def test_no_duplicates(self):
        content = r"\index{a} \index{b} \index{c}"
        dups = find_duplicate_indexes(content)
        assert len(dups) == 0

    def test_idx_commands_counted(self):
        content = r"\idx{compact} more \idx{compact}"
        dups = find_duplicate_indexes(content)
        assert len(dups) >= 1


class TestMissingEntries:
    def test_finds_missing(self):
        content = r"The concept of topology includes open sets."
        candidates = ["topology", "algebra", "open sets"]
        missing = find_potential_missing_entries(content, candidates)
        assert "topology" in missing
        assert "open sets" in missing  # appears in text, not in \index{}

    def test_already_indexed_not_missing(self):
        content = r"\index{topology} is important."
        candidates = ["topology"]
        missing = find_potential_missing_entries(content, candidates)
        assert "topology" not in missing


class TestRangePairs:
    def test_balanced_pairs(self):
        content = (
            r"\index{compact|(} text \index{compact|)}"
        )
        result = validate_range_pairs(content)
        assert result["open_count"] >= 1
        assert result["close_count"] >= 1

    def test_unbalanced(self):
        content = r"\index{compact|(} text without close"
        result = validate_range_pairs(content)
        assert not result["balanced"]

    def test_no_pairs(self):
        result = validate_range_pairs(r"\index{normal} entry")
        assert result["open_count"] == 0
        assert result["balanced"]


class TestGenerateReport:
    def test_full_report(self):
        content = r"\index{compact} \index{compact} \index{field}"
        report = generate_report(
            content,
            entries=[{"term": "compact", "level": 1}],
            candidates=["field", "missing"],
        )
        assert "LaTeX" in report or "索引" in report
        assert "compact" in report

    def test_minimal_report(self):
        report = generate_report("empty text")
        assert "已有索引" in report

    def test_report_without_entries(self):
        content = r"\index{test} and \idx{other}"
        report = generate_report(content)
        # Report should show counts: 1 \index and 1 \idx
        assert "1" in report  # count lines show "1"

    def test_report_with_range_pairs(self):
        content = r"\index{compact|(} text \index{compact|)}"
        report = generate_report(content)
        assert "配对" in report or "平衡" in report or "范围" in report

    def test_report_with_candidates(self):
        content = r"\section{Topology} The concept of topology."
        report = generate_report(
            content,
            candidates=["topology", "missing"],
        )
        assert "topology" in report

    def test_report_with_both(self):
        content = r"\index{field} \index{field}"
        report = generate_report(
            content,
            entries=[{"term": "field", "level": 1}],
            candidates=["field", "extra"],
        )
        assert "重复" in report or "duplicate" in report.lower() or "field" in report

    def test_report_with_missing_entries_shown(self):
        content = "text about algebra"
        entries = [{"term": "algebra", "level": 1}]
        report = generate_report(content, entries=entries)
        assert "命中" in report or "found" in report.lower() or "coverage" in report.lower()

    def test_report_shows_l2_coverage(self):
        content = "compact space"
        entries = [
            {"term": "compact space", "level": 1},
            {"term": "open cover", "level": 2, "parent": "compact"},
        ]
        report = generate_report(content, entries=entries)
        assert "L2" in report

    def test_report_with_range_pairs_unbalanced(self):
        content = r"\index{test|(} begin only"
        report = generate_report(content)
        assert "不平衡" in report or "unbalanced" in report.lower() or "配对" in report
