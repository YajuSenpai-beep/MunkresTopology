r"""Tests for Aho-Corasick PatternMatcher.

Coverage targets: 85%+ on latex_index/matcher.py (currently 19%).
"""

import pytest
from latex_index.matcher import PatternMatcher


class TestBasicSearch:
    """Basic pattern matching functionality."""

    def test_single_pattern(self):
        matcher = PatternMatcher()
        matcher.add("field", "key_field")
        matcher.finish()
        results = matcher.search("a field in the text")
        assert len(results) == 1
        assert results[0][0] == 2   # position
        assert results[0][1] == "key_field"
        assert results[0][2] == 5   # length

    def test_no_match(self):
        matcher = PatternMatcher()
        matcher.add("missing", "k")
        matcher.finish()
        results = matcher.search("nothing here")
        assert results == []

    def test_empty_text(self):
        matcher = PatternMatcher()
        matcher.add("abc", "k")
        matcher.finish()
        results = matcher.search("")
        assert results == []

    def test_exact_match(self):
        matcher = PatternMatcher()
        matcher.add("exact", "k")
        matcher.finish()
        results = matcher.search("exact")
        assert results == [(0, "k", 5)]


class TestMultiplePatterns:
    """Multiple pattern registration and search."""

    def test_two_patterns(self):
        matcher = PatternMatcher()
        matcher.add("apple", "apple_key")
        matcher.add("orange", "orange_key")
        matcher.finish()
        results = matcher.search("i like apple and orange")
        assert len(results) == 2
        keys = {r[1] for r in results}
        assert keys == {"apple_key", "orange_key"}

    def test_overlapping_classic(self):
        """Classic Aho-Corasick test: he/she/his/hers."""
        matcher = PatternMatcher()
        matcher.add("he", "he")
        matcher.add("she", "she")
        matcher.add("his", "his")
        matcher.add("hers", "hers")
        matcher.finish()
        results = matcher.search("ushers")
        # "ushers" -> she at 1, he at 2, hers at 2
        keys = {(r[0], r[1]) for r in results}
        assert (1, "she") in keys
        assert (2, "he") in keys
        assert (2, "hers") in keys

    def test_substring_patterns(self):
        """Shorter patterns should be found alongside longer ones."""
        matcher = PatternMatcher()
        matcher.add("a", "short")
        matcher.add("ab", "long")
        matcher.finish()
        results = matcher.search("ab")
        keys = {(r[0], r[1]) for r in results}
        assert (0, "short") in keys  # 'a' at start
        assert (0, "long") in keys   # 'ab' at start

    def test_multiple_occurrences(self):
        matcher = PatternMatcher()
        matcher.add("the", "the")
        matcher.finish()
        results = matcher.search("the cat and the dog")
        assert len(results) == 2
        assert results[0][0] == 0
        assert results[1][0] == 12


class TestCaseSensitivity:
    """Case sensitivity modes."""

    def test_case_insensitive_default(self):
        matcher = PatternMatcher()  # default: case_sensitive=False
        matcher.add("Hello", "k")
        matcher.finish()
        results = matcher.search("hello world")
        assert len(results) == 1

    def test_case_insensitive_mixed(self):
        matcher = PatternMatcher(case_sensitive=False)
        matcher.add("UPPER", "k")
        matcher.finish()
        results = matcher.search("upper case")
        assert len(results) == 1

    def test_case_sensitive_match(self):
        matcher = PatternMatcher(case_sensitive=True)
        matcher.add("Hello", "k")
        matcher.finish()
        results = matcher.search("Hello world")
        assert len(results) == 1

    def test_case_sensitive_no_match(self):
        matcher = PatternMatcher(case_sensitive=True)
        matcher.add("Hello", "k")
        matcher.finish()
        results = matcher.search("hello world")
        assert results == []


class TestLifecycle:
    """Object lifecycle and error handling."""

    def test_finish_before_add_raises(self):
        matcher = PatternMatcher()
        matcher.finish()
        with pytest.raises(RuntimeError, match="Cannot add patterns after finish"):
            matcher.add("x", "y")

    def test_search_auto_finishes(self):
        matcher = PatternMatcher()
        matcher.add("auto", "k")
        # search() calls finish() automatically
        results = matcher.search("auto complete")
        assert len(results) == 1

    def test_double_finish_safe(self):
        matcher = PatternMatcher()
        matcher.add("x", "y")
        matcher.finish()
        matcher.finish()  # should be safe
        results = matcher.search("x")
        assert len(results) == 1

    def test_pattern_count(self):
        matcher = PatternMatcher()
        assert matcher.pattern_count == 0
        matcher.add("a", "k1")
        matcher.add("b", "k2")
        matcher.add("c", "k3")
        assert matcher.pattern_count == 3


class TestEdgeCases:
    """Edge cases and boundary conditions."""

    def test_single_character_pattern(self):
        matcher = PatternMatcher()
        matcher.add("x", "k")
        matcher.finish()
        results = matcher.search("abcxdef")
        assert len(results) == 1
        assert results[0] == (3, "k", 1)

    def test_very_long_pattern(self):
        long = "abcdefghij" * 100
        matcher = PatternMatcher()
        matcher.add(long, "long")
        matcher.finish()
        results = matcher.search("prefix " + long + " suffix")
        assert len(results) == 1
        assert results[0][2] == len(long)

    def test_special_regex_chars_literal(self):
        """Patterns with regex-special chars should be matched literally."""
        matcher = PatternMatcher()
        matcher.add("a.b*c[d]e(f)g", "special")
        matcher.finish()
        results = matcher.search("test a.b*c[d]e(f)g done")
        assert len(results) == 1

    def test_unicode_support(self):
        matcher = PatternMatcher()
        matcher.add("café", "cafe")
        matcher.add("naïve", "naive")
        matcher.finish()
        results = matcher.search("un café naïve")
        assert len(results) == 2

    def test_unicode_case_insensitive(self):
        matcher = PatternMatcher(case_sensitive=False)
        matcher.add("CAFÉ", "k")
        matcher.finish()
        results = matcher.search("café")
        assert len(results) == 1

    def test_overlapping_at_same_position(self):
        matcher = PatternMatcher()
        matcher.add("abc", "k1")
        matcher.add("ab", "k2")
        matcher.finish()
        results = matcher.search("abcde")
        assert len(results) == 2
        assert (0, "k1") in {(r[0], r[1]) for r in results}
        assert (0, "k2") in {(r[0], r[1]) for r in results}

    def test_pattern_at_text_end(self):
        matcher = PatternMatcher()
        matcher.add("end", "k")
        matcher.finish()
        results = matcher.search("the end")
        assert len(results) == 1
        assert results[0][0] == 4

    def test_pattern_at_text_start(self):
        matcher = PatternMatcher()
        matcher.add("start", "k")
        matcher.finish()
        results = matcher.search("start of text")
        assert len(results) == 1
        assert results[0][0] == 0


class TestPerformance:
    """Performance and scale tests."""

    def test_large_pattern_set(self):
        matcher = PatternMatcher()
        for i in range(2000):
            matcher.add(f"term_{i:04d}", f"key_{i}")
        matcher.finish()
        assert matcher.pattern_count == 2000
        results = matcher.search("this contains term_1234 somewhere")
        assert len(results) >= 1
        assert any(r[1] == "key_1234" for r in results)

    def test_many_matches(self):
        matcher = PatternMatcher()
        for i in range(100):
            matcher.add(f"z{i:03d}z", f"k{i}")
        matcher.finish()
        text = " ".join(f"z{i:03d}z" for i in range(100))
        results = matcher.search(text)
        assert len(results) == 100

    def test_substring_matching(self):
        """Aho-Corasick finds ALL occurrences, including inside other words."""
        matcher = PatternMatcher()
        matcher.add("cat", "cat")
        matcher.add("dog", "dog")
        matcher.finish()
        results = matcher.search(
            "category catalog dogma dogmatic cattle dog cat"
        )
        # Substring matching: "cat" found in "category", "catalog", "cattle", "cat"
        key_results = [r[1] for r in results]
        assert key_results.count("cat") == 4  # category, catalog, cattle, cat
        assert key_results.count("dog") == 3  # dogma, dogmatic, dog


class TestDuplicateKeys:
    """Behavior with duplicate keys."""

    def test_duplicate_key_add(self):
        matcher = PatternMatcher()
        matcher.add("xyz", "same_key")
        matcher.add("xyz", "same_key")
        matcher.finish()
        results = matcher.search("xyz")
        # Both registrations produce output, so 2 results for same position
        assert len(results) == 2

    def test_same_pattern_different_keys(self):
        matcher = PatternMatcher()
        matcher.add("dup", "key_a")
        matcher.add("dup", "key_b")
        matcher.finish()
        results = matcher.search("dup")
        assert len(results) == 2
        keys = {r[1] for r in results}
        assert keys == {"key_a", "key_b"}
