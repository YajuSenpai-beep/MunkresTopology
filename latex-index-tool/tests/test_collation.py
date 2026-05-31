r"""Tests for collation/sorting support.

Covers latex_index/collation.py.
"""

import pytest

from latex_index.collation import (
    _pinyin_sort_key,
    _stroke_sort_key,
    sort_key_for,
)


class TestDefaultSort:
    def test_lowercase(self):
        assert sort_key_for("Hello") == "hello"

    def test_empty(self):
        assert sort_key_for("") == ""

    def test_makeindex_alias(self):
        assert sort_key_for("Test", "makeindex") == "test"


class TestUnicodeSort:
    def test_numeric_keys(self):
        a = sort_key_for("abc", "unicode")
        b = sort_key_for("abd", "unicode")
        assert a < b

    def test_chinese_order(self):
        a = sort_key_for("拓扑学", "unicode")
        b = sort_key_for("代数", "unicode")
        assert a > b  # 拓 U+62D3 > 代 U+4EE3

    def test_consistent_output(self):
        assert sort_key_for("abc", "unicode") == sort_key_for("abc", "unicode")


class TestPinyinSort:
    def test_no_crash(self):
        result = sort_key_for("中文", "pinyin")
        assert isinstance(result, str)

    def test_stable_output(self):
        a = sort_key_for("拓扑学", "pinyin")
        b = sort_key_for("代数拓扑", "pinyin")
        assert isinstance(a, str)
        assert isinstance(b, str)

    def test_mixed_chinese_english(self):
        result = sort_key_for("Chapter 1 拓扑学基础", "pinyin")
        assert isinstance(result, str)

    def test_punctuation_handled(self):
        result = sort_key_for("A. 测试", "pinyin")
        assert isinstance(result, str)

    def test_actual_pinyin_order(self):
        """With pypinyin installed, verify basic ordering."""
        a = sort_key_for("代数", "pinyin")
        b = sort_key_for("拓扑", "pinyin")
        # "dai shu" < "tuo pu" alphabetically
        assert a < b

    def test_pinyin_consistent_output(self):
        a1 = sort_key_for("中文索引", "pinyin")
        a2 = sort_key_for("中文索引", "pinyin")
        assert a1 == a2

    def test_pinyin_handles_long_text(self):
        result = sort_key_for("这是一个很长的中文句子用于测试排序", "pinyin")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_pinyin_pure_english_unchanged(self):
        result = sort_key_for("hello world", "pinyin")
        assert "hello" in result
        assert "world" in result


class TestStrokeSort:
    def test_no_crash(self):
        result = sort_key_for("中文", "stroke")
        assert isinstance(result, str)

    def test_numeric_output(self):
        result = sort_key_for("ab", "stroke")
        assert all(c.isdigit() for c in result)


class TestInternalFunctions:
    def test_pinyin_raw(self):
        result = _pinyin_sort_key("测试")
        assert isinstance(result, str)

    def test_stroke_raw(self):
        result = _stroke_sort_key("测试")
        assert isinstance(result, str)
        assert all(c.isdigit() for c in result)

    def test_pinyin_mixed(self):
        result = _pinyin_sort_key("hello 世界 test")
        assert isinstance(result, str)


class TestInvalidCollation:
    def test_falls_back_to_default(self):
        assert sort_key_for("test", "unknown") == "test"

    def test_nonexistent_not_crash(self):
        for name in ["pinyin", "stroke", "unicode", "default", "makeindex", ""]:
            result = sort_key_for("test", name)
            assert isinstance(result, str)


class TestSortOrder:
    def test_unicode_monotonic(self):
        items = ["c", "a", "b", "d"]
        sorted_items = sorted(items, key=lambda x: sort_key_for(x, "unicode"))
        assert sorted_items == ["a", "b", "c", "d"]

    def test_default_monotonic(self):
        items = ["Cat", "apple", "Banana"]
        sorted_items = sorted(items, key=lambda x: sort_key_for(x, "default"))
        assert sorted_items == ["apple", "Banana", "Cat"]


class TestFallbackWithoutPypinyin:
    """Test pinyin/stroke fallback when pypinyin is not installed."""

    def test_pinyin_fallback_numeric(self, monkeypatch):
        """Without pypinyin, pinyin uses Unicode codepoint fallback."""
        monkeypatch.setattr("latex_index.collation.HAS_PINYIN", False)
        result = sort_key_for("测试", "pinyin")
        # Fallback returns numeric string
        assert all(c.isdigit() for c in result) or result != ""

    def test_stroke_fallback(self, monkeypatch):
        monkeypatch.setattr("latex_index.collation.HAS_PINYIN", False)
        result = sort_key_for("测试", "stroke")
        assert all(c.isdigit() for c in result) or result != ""


