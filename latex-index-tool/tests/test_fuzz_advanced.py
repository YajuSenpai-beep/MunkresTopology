r"""Advanced fuzz tests — corrupted UTF-8, recursive YAML, huge inputs.

Complements test_fuzz.py with more extreme edge cases.
"""

import json
import os
import tempfile

import pytest

from latex_index.config import load_config
from latex_index.engine import IndexEngine
from latex_index.matcher import PatternMatcher
from latex_index.tex_utils import escape_index_term


class TestCorruptedUtf8:
    """Inject invalid UTF-8 byte sequences."""

    def test_invalid_utf8_in_content(self):
        engine = IndexEngine(
            {"templates": {"l1": r"\index{${key}}"}, "aliases": {}, "math_shortcuts": {}}
        )
        # Invalid UTF-8 bytes: 0xFF, 0xFE, isolated continuation bytes
        content = "hello" + bytes([0xFF, 0xFE, 0x80]).decode("latin-1") + "world"
        ops = engine.find_insertions(content, [{"term": "hello", "level": 1}])
        assert isinstance(ops, list)

    def test_bom_stripped(self):
        content = "﻿\\section{Intro}"  # BOM
        engine = IndexEngine(
            {"templates": {"l1": r"\index{${key}}"}, "aliases": {}, "math_shortcuts": {}}
        )
        ops = engine.find_insertions(content, [{"term": "Intro", "level": 1}])
        assert isinstance(ops, list)

    def test_null_bytes_in_pattern(self):
        matcher = PatternMatcher()
        # Null bytes in pattern
        pat = "hel\x00lo"
        matcher.add(pat, "null_key")
        matcher.finish()
        results = matcher.search("testing hel\x00lo world")
        assert isinstance(results, list)


class TestHugeInputs:
    """Test with extremely large inputs."""

    def test_50000_entries(self):
        engine = IndexEngine(
            {"templates": {"l1": r"\index{${key}}"}, "aliases": {}, "math_shortcuts": {}}
        )
        entries = [{"term": f"word_{i:05d}", "level": 1} for i in range(50000)]
        content = " ".join(f"word_{i:05d}" for i in range(0, 50000, 100))
        ops = engine.find_insertions(content, entries)
        assert isinstance(ops, list)

    def test_100k_chars_escape(self):
        term = "x" * 100000
        result = escape_index_term(term)
        assert len(result) >= len(term)

    def test_1000_matcher_patterns(self):
        matcher = PatternMatcher()
        for i in range(1000):
            matcher.add(f"pat_{i:04d}_unique", f"key_{i}")
        matcher.finish()
        text = " ".join(f"pat_{i:04d}_unique" for i in range(1000))
        results = matcher.search(text)
        assert len(results) == 1000


class TestRecursiveYaml:
    """Test deeply nested and recursive YAML configs."""

    def test_deeply_nested_config(self):
        """Config with deep nesting (JSON)."""
        config_data: dict = {"log_level": "DEBUG"}
        current = config_data
        for i in range(50):
            current["nested"] = {"level": i}
            current = current["nested"]
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump(config_data, f)
            path = f.name
        try:
            config = load_config(path)
            assert config["log_level"] == "DEBUG"
        finally:
            os.unlink(path)

    def test_large_yaml_with_aliases(self):
        config_data = {
            "log_level": "INFO",
            "aliases": {f"term_{i}": [f"alias_{i}_{j}" for j in range(100)] for i in range(100)},
        }
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump(config_data, f)
            path = f.name
        try:
            config = load_config(path)
            assert len(config["aliases"]) == 100
        finally:
            os.unlink(path)

    def test_config_with_empty_values(self):
        config_data = {"log_level": "", "templates": {"l1": ""}, "aliases": {}}
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump(config_data, f)
            path = f.name
        try:
            config = load_config(path)
            assert config["log_level"] == ""
        finally:
            os.unlink(path)


class TestSpecialCharacters:
    """Inject special and control characters."""

    def test_vertical_tab_in_content(self):
        content = "hello\x0bworld"
        engine = IndexEngine(
            {"templates": {"l1": r"\index{${key}}"}, "aliases": {}, "math_shortcuts": {}}
        )
        ops = engine.find_insertions(content, [{"term": "hello", "level": 1}])
        assert isinstance(ops, list)

    def test_form_feed_in_content(self):
        content = "hello\x0cworld"
        engine = IndexEngine(
            {"templates": {"l1": r"\index{${key}}"}, "aliases": {}, "math_shortcuts": {}}
        )
        ops = engine.find_insertions(content, [{"term": "hello", "level": 1}])
        assert isinstance(ops, list)

    def test_all_control_chars(self):
        engine = IndexEngine(
            {"templates": {"l1": r"\index{${key}}"}, "aliases": {}, "math_shortcuts": {}}
        )
        content = "".join(chr(i) for i in range(32)) + "target"
        ops = engine.find_insertions(content, [{"term": "target", "level": 1}])
        assert isinstance(ops, list)
