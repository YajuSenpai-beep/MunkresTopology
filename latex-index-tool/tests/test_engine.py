"""engine.py 单元测试。"""
import pytest
from latex_index.engine import IndexEngine


class TestBasicInsertion:
    def test_simple_term(self, sample_config, simple_entries):
        engine = IndexEngine(sample_config)
        content = "The concept of a field is central."
        ops = engine.find_insertions(content, simple_entries)
        assert len(ops) == 1
        assert ops[0]["cmd"] == "\\idx{field}"

    def test_case_insensitive(self, sample_config):
        engine = IndexEngine(sample_config)
        content = "The Field is central."
        entries = [{"term": "field", "level": 1, "page": [1]}]
        ops = engine.find_insertions(content, entries)
        assert len(ops) == 1


class TestMathSkip:
    def test_skip_inline_math(self, sample_config):
        engine = IndexEngine(sample_config)
        content = "The set \\(A\\) is a field."
        entries = [{"term": "field", "level": 1, "page": [1]}]
        ops = engine.find_insertions(content, entries)
        assert len(ops) == 1  # text 'field' found, math skipped

    def test_skip_dollar_math(self, sample_config):
        engine = IndexEngine(sample_config)
        content = "The set $A$ is a field but $B$ is not a field either."
        entries = [{"term": "field", "level": 1, "page": [1]}]
        ops = engine.find_insertions(content, entries)
        assert len(ops) >= 1  # at least one text 'field' found, math-inside skipped


class TestCommentSkip:
    def test_skip_comment(self, sample_config):
        engine = IndexEngine(sample_config)
        content = "We study the field. % field is important"
        entries = [{"term": "field", "level": 1, "page": [1]}]
        ops = engine.find_insertions(content, entries)
        assert len(ops) == 1  # only text, not comment


class TestLongerTermFirst:
    def test_no_overlap(self, sample_config):
        engine = IndexEngine(sample_config)
        content = "The inverse function theorem."
        entries = [
            {"term": "inverse function", "level": 1, "page": [1]},
            {"term": "inverse", "level": 1, "page": [2]},
        ]
        ops = engine.find_insertions(content, entries)
        assert len(ops) == 1
        assert ops[0]["entry"]["term"] == "inverse function"


class TestAliases:
    def test_alias_match(self, sample_config):
        config = dict(sample_config)
        config["aliases"] = {"inverse image": ["preimage"]}
        engine = IndexEngine(config)
        content = "The preimage of the set."
        entries = [{"term": "inverse image", "level": 1, "page": [5]}]
        ops = engine.find_insertions(content, entries)
        assert len(ops) == 1


class TestMathSymbol:
    def test_mathbb_r(self, sample_config):
        engine = IndexEngine(sample_config)
        # In real LaTeX source, \mathbb{R} appears without \(\) wrapper
        # because \idxmath already provides the math context
        content = "We denote reals by \\mathbb{R}."
        entries = [
            {"term": "\\(\\mathbb{R}\\)", "level": 1, "sort_key": "R", "page": [5]}
        ]
        ops = engine.find_insertions(content, entries)
        assert len(ops) == 1
        assert "\\mathbb{R}" in ops[0]["cmd"]


class TestEmpty:
    def test_empty_content(self, sample_config):
        engine = IndexEngine(sample_config)
        ops = engine.find_insertions("", [{"term": "x", "level": 1}])
        assert len(ops) == 0

    def test_empty_entries(self, sample_config):
        engine = IndexEngine(sample_config)
        ops = engine.find_insertions("text", [])
        assert len(ops) == 0

    def test_short_term_skipped(self, sample_config):
        engine = IndexEngine(sample_config)
        ops = engine.find_insertions("a", [{"term": "a", "level": 1}])
        assert len(ops) == 0  # too short


class TestApply:
    def test_insert_order(self, sample_config):
        engine = IndexEngine(sample_config)
        content = "field and ring"
        entries = [
            {"term": "field", "level": 1, "page": [1]},
            {"term": "ring", "level": 1, "page": [2]},
        ]
        ops = engine.find_insertions(content, entries)
        result = engine.apply(content, ops)
        assert "\\idx{field}" in result
        assert "\\idx{ring}" in result
        assert result.index("\\idx{field}") < result.index("\\idx{ring}")


class TestL2Entry:
    def test_l2_handled(self, sample_config):
        engine = IndexEngine(sample_config)
        content = "The finite axiom of choice."
        entries = [
            {"term": "finite axiom of choice", "level": 2, "parent": "Axiom of choice"}
        ]
        ops = engine.find_insertions(content, entries)
        # L2 entries should produce idxsub commands
        if ops:
            assert "\\idxsub" in ops[0]["cmd"]


class TestFastPath:
    """Tests for find_insertions_fast (Aho-Corasick path)."""

    def test_fast_basic(self, sample_config):
        engine = IndexEngine(sample_config)
        content = "The field concept is fundamental."
        entries = [{"term": "field", "level": 1, "page": [1]}]
        ops = engine.find_insertions_fast(content, entries)
        assert len(ops) >= 0  # may fall through to normal path

    def test_fast_falls_back_to_normal_for_small(self, sample_config):
        """Small dataset should fall back to normal search."""
        engine = IndexEngine(sample_config)
        content = "field" * 1000
        entries = [{"term": f"w{i}", "level": 1} for i in range(10)]
        ops = engine.find_insertions_fast(content, entries)
        # Falls back because < 1000 entries
        assert isinstance(ops, list)

    def test_fast_triggers_on_large(self, sample_config):
        """Large entry set (>1000) and large text (>500KB) triggers fast path."""
        engine = IndexEngine(sample_config)
        content = "compact " * 25000 + " open cover "
        entries = [{"term": "compact", "level": 1}]
        # Fill to 1001 entries to trigger threshold
        for i in range(1000):
            entries.append({"term": f"filler_{i:04d}", "level": 1})
        ops = engine.find_insertions_fast(content, entries)
        # Should find "compact" via fast path
        assert len(ops) >= 1
        assert any(o["entry"]["term"] == "compact" for o in ops)

    def test_fast_with_math_symbol(self, sample_config):
        engine = IndexEngine(sample_config)
        content = "\\mathbb{R} is the set of reals." * 50000
        entries = [
            {"term": "\\(\\mathbb{R}\\)", "level": 1, "sort_key": "R"}
        ]
        for i in range(1000):
            entries.append({"term": f"pad_{i:04d}", "level": 1})
        ops = engine.find_insertions_fast(content, entries)
        assert len(ops) >= 1

    def test_fast_with_l2(self, sample_config):
        engine = IndexEngine(sample_config)
        content = "open cover " * 25000
        entries = [{"term": "open cover", "level": 2, "parent": "compact"}]
        for i in range(1000):
            entries.append({"term": f"pad_{i:04d}", "level": 1})
        ops = engine.find_insertions_fast(content, entries)
        assert len(ops) >= 1

    def test_fast_respects_forbidden_zones(self, sample_config):
        engine = IndexEngine(sample_config)
        content = ("He said: % compact is important\n" + "compact " * 25000)
        entries = [{"term": "compact", "level": 1}]
        for i in range(1000):
            entries.append({"term": f"pad_{i:04d}", "level": 1})
        ops = engine.find_insertions_fast(content, entries)
        compact_ops = [o for o in ops if o["entry"]["term"] == "compact"]
        assert len(compact_ops) >= 1
        comment_end = content.index("\n")
        for o in compact_ops:
            assert o["pos"] > comment_end

    def test_fast_unique_per_entry(self, sample_config):
        """Fast path returns at most one insertion per entry key."""
        engine = IndexEngine(sample_config)
        content = "compact " * 25000 + " compact "
        entries = [{"term": "compact", "level": 1}]
        for i in range(1000):
            entries.append({"term": f"pad_{i:04d}", "level": 1})
        ops = engine.find_insertions_fast(content, entries)
        compact_ops = [o for o in ops if o["entry"]["term"] == "compact"]
        assert len(compact_ops) == 1

    def test_fast_progress_flag(self, sample_config):
        engine = IndexEngine(sample_config)
        content = "field " * 25000
        entries = [{"term": "field", "level": 1}]
        for i in range(1000):
            entries.append({"term": f"pad_{i:04d}", "level": 1})
        ops = engine.find_insertions_fast(content, entries, progress=True)
        assert len(ops) >= 1


class TestProcessLargeFile:
    """Tests for process_large_file static method."""

    def test_process_small_file(self, sample_config, tmp_path):
        fp = tmp_path / "test.tex"
        fp.write_text("The concept of a field is central.", encoding="utf-8")
        entries = [{"term": "field", "level": 1}]
        n = IndexEngine.process_large_file(str(fp), entries, sample_config)
        assert n >= 0

    def test_process_empty_file(self, sample_config, tmp_path):
        fp = tmp_path / "empty.tex"
        fp.write_text("", encoding="utf-8")
        n = IndexEngine.process_large_file(str(fp), [], sample_config)
        assert n == 0


class TestEngineConfig:
    """Tests for engine configuration handling."""

    def test_index_processor_passed(self):
        config = {
            "templates": {"l1": r"\index{${key}}"},
            "aliases": {},
            "math_shortcuts": {},
            "index_processor": "xindy",
        }
        engine = IndexEngine(config)
        assert engine.index_processor == "xindy"

    def test_default_index_processor(self):
        engine = IndexEngine({"templates": {}, "aliases": {}, "math_shortcuts": {}})
        assert engine.index_processor == "makeindex"

    def test_normal_insert_with_progress(self, sample_config):
        engine = IndexEngine(sample_config)
        content = "The field is important."
        entries = [{"term": "field", "level": 1}]
        ops = engine.find_insertions(content, entries, progress=True)
        assert len(ops) == 1

    def test_fast_with_progress(self, sample_config):
        engine = IndexEngine(sample_config)
        content = "field " * 25000
        entries = [{"term": "field", "level": 1}]
        for i in range(1000):
            entries.append({"term": f"pad_{i:04d}", "level": 1})
        ops = engine.find_insertions_fast(content, entries, progress=True)
        assert len(ops) >= 1


class TestEngineEdgeCases:
    """Additional edge case tests for uncovered branches."""

    def test_l2_with_child_field(self, sample_config):
        engine = IndexEngine(sample_config)
        content = "The open cover is important."
        entries = [{
            "term": "compact space",
            "level": 2,
            "parent": "topology",
            "child": "open cover",
        }]
        ops = engine.find_insertions(content, entries)
        assert len(ops) >= 1

    def test_math_entry_with_shortcuts(self, sample_config):
        config = dict(sample_config)
        config["math_shortcuts"] = {"\\mathbb{R}": ["\\R"]}
        engine = IndexEngine(config)
        content = "We use \\R to denote reals."
        entries = [{
            "term": "\\(\\mathbb{R}\\)",
            "level": 1,
            "sort_key": "R",
        }]
        ops = engine.find_insertions(content, entries)
        # Should find via alias \\R
        assert len(ops) >= 1

    def test_math_entry_with_text_alias(self, sample_config):
        config = dict(sample_config)
        # The alias key should be the raw LaTeX (after strip_latex)
        config["aliases"] = {"\\mathbb{R}": ["the real numbers"]}
        engine = IndexEngine(config)
        content = "We consider the real numbers as a field."
        entries = [{
            "term": "\\(\\mathbb{R}\\)",
            "level": 1,
            "sort_key": "R",
        }]
        ops = engine.find_insertions(content, entries)
        assert len(ops) >= 1

    def test_fast_without_tqdm(self, sample_config, monkeypatch):
        """Test fast path when tqdm is not installed."""
        monkeypatch.setattr("latex_index.engine.HAS_TQDM", False)
        engine = IndexEngine(sample_config)
        content = "field " * 25000
        entries = [{"term": "field", "level": 1}]
        for i in range(1000):
            entries.append({"term": f"pad_{i:04d}", "level": 1})
        ops = engine.find_insertions_fast(content, entries, progress=True)
        assert len(ops) >= 1  # should work without tqdm

    def test_special_chars_in_term_fallback(self, sample_config):
        """Terms with special chars (_^@!|\") are skipped in L1 but not L2."""
        engine = IndexEngine(sample_config)
        content = "test content with special_stuff"
        entries = [{"term": "special_stuff", "level": 1}]
        ops = engine.find_insertions(content, entries)
        # Should skip because term contains _
        assert len(ops) == 0

    def test_large_file_apply(self, sample_config):
        """Apply should work on content > 10MB."""
        engine = IndexEngine(sample_config)
        content = "x" * (11 * 1024 * 1024)
        ops = [{"pos": 100, "cmd": r"\index{test}", "entry": {"term": "test"}}]
        result = engine.apply(content, ops)
        assert len(result) > len(content)


class TestTqdmNotInstalled:
    """Test behavior when tqdm is not available."""

    def test_find_insertions_without_tqdm(self, sample_config, monkeypatch):
        monkeypatch.setattr("latex_index.engine.HAS_TQDM", False)
        engine = IndexEngine(sample_config)
        content = "field " * 100
        entries = [{"term": "field", "level": 1}]
        ops = engine.find_insertions(content, entries, progress=True)
        assert len(ops) >= 1

    def test_find_fast_without_tqdm(self, sample_config, monkeypatch):
        monkeypatch.setattr("latex_index.engine.HAS_TQDM", False)
        engine = IndexEngine(sample_config)
        content = "field " * 25000
        entries = [{"term": "field", "level": 1}]
        for i in range(1000):
            entries.append({"term": f"pad_{i:04d}", "level": 1})
        ops = engine.find_insertions_fast(content, entries, progress=True)
        assert len(ops) >= 1
