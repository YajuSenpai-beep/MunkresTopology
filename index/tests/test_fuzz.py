r"""Fuzz tests — verify robustness against malformed/random inputs.

Tests that the engine and utilities never crash, regardless of input quality.
"""

import random
import string

import pytest

from latex_index.engine import IndexEngine
from latex_index.matcher import PatternMatcher
from latex_index.parser import parse_index_file, parse_indented, parse_run_in
from latex_index.tex_utils import (
    brace_match,
    escape_index_term,
    find_comment_ranges,
    find_math_ranges,
    find_verbatim_ranges,
    is_inside_command_arg,
    is_inside_comment,
    is_inside_index,
    is_inside_math,
    is_inside_verbatim,
    strip_latex,
)


def _random_string(length: int, chars: str = string.printable) -> str:
    return "".join(random.choice(chars) for _ in range(length))


class TestEngineFuzz:
    """Fuzz the engine with random inputs."""

    @pytest.mark.parametrize("seed", range(20))
    def test_random_content_no_crash(self, seed):
        random.seed(seed)
        config = {
            "templates": {
                "l1": r"\index{${key}}",
                "l2": r"\index{${parent}!${child}}",
            },
            "aliases": {},
            "math_shortcuts": {},
        }
        engine = IndexEngine(config)
        content = _random_string(random.randint(0, 5000))
        entries = [
            {"term": _random_string(random.randint(1, 30)), "level": 1}
            for _ in range(random.randint(0, 50))
        ]
        # Must not raise
        ops = engine.find_insertions(content, entries)
        assert isinstance(ops, list)
        # Apply should be idempotent-safe
        result = engine.apply(content, ops)
        assert isinstance(result, str)

    @pytest.mark.parametrize("seed", range(10))
    def test_random_latex_like_content(self, seed):
        random.seed(seed)
        config = {
            "templates": {"l1": r"\index{${key}}"},
            "aliases": {},
            "math_shortcuts": {},
        }
        engine = IndexEngine(config)
        # Mix of LaTeX commands and text
        parts = []
        for _ in range(100):
            kind = random.choice(["text", "math", "cmd", "comment", "verb"])
            if kind == "text":
                parts.append(_random_string(random.randint(1, 80)))
            elif kind == "math":
                parts.append(f"${_random_string(random.randint(1, 20))}$")
            elif kind == "cmd":
                parts.append(
                    f"\\{_random_string(random.randint(3, 10))}"
                    f"{{{_random_string(random.randint(1, 30))}}}"
                )
            elif kind == "comment":
                parts.append(f"% {_random_string(random.randint(1, 40))}")
            elif kind == "verb":
                parts.append(
                    "\\begin{verbatim}\n"
                    + _random_string(random.randint(1, 100))
                    + "\n\\end{verbatim}"
                )
        content = "\n".join(parts)
        entries = [
            {"term": _random_string(random.randint(2, 20)), "level": 1}
            for _ in range(20)
        ]
        engine.find_insertions(content, entries)  # must not crash
        engine.find_insertions_fast(content, entries)  # must not crash

    def test_empty_everything(self):
        engine = IndexEngine({"templates": {}, "aliases": {}, "math_shortcuts": {}})
        ops = engine.find_insertions("", [])
        assert ops == []

    def test_null_bytes_in_content(self):
        engine = IndexEngine(
            {"templates": {"l1": r"\index{${key}}"}, "aliases": {}, "math_shortcuts": {}}
        )
        content = "hello\x00world\x00test"
        entries = [{"term": "hello", "level": 1}]
        ops = engine.find_insertions(content, entries)
        assert isinstance(ops, list)

    def test_very_deep_nesting(self):
        """Engine should handle deeply nested braces without stack overflow."""
        engine = IndexEngine(
            {"templates": {"l1": r"\index{${key}}"}, "aliases": {}, "math_shortcuts": {}}
        )
        deep = "{" * 500 + "word" + "}" * 500
        entries = [{"term": "word", "level": 1}]
        ops = engine.find_insertions(deep, entries)
        assert isinstance(ops, list)


class TestMatcherFuzz:
    """Fuzz the pattern matcher."""

    @pytest.mark.parametrize("seed", range(15))
    def test_random_patterns(self, seed):
        random.seed(seed)
        matcher = PatternMatcher()
        for _ in range(random.randint(1, 100)):
            pat = _random_string(random.randint(1, 20))
            matcher.add(pat, f"key_{_}")
        matcher.finish()
        text = _random_string(random.randint(0, 1000))
        results = matcher.search(text)
        assert isinstance(results, list)
        for r in results:
            assert len(r) == 3


class TestTexUtilsFuzz:
    """Fuzz LaTeX utility functions."""

    @pytest.mark.parametrize("seed", range(10))
    def test_random_latex_string(self, seed):
        random.seed(seed)
        content = _random_string(random.randint(0, 2000))
        # All functions must return without exception
        find_math_ranges(content)
        find_comment_ranges(content)
        find_verbatim_ranges(content)
        for pos in [0, len(content) // 2, max(0, len(content) - 1)]:
            is_inside_math(content, pos)
            is_inside_comment(content, pos)
            is_inside_verbatim(content, pos)
            is_inside_command_arg(content, pos)
            is_inside_index(content, pos)

    def test_escape_special_chars(self):
        """Escape should handle arbitrary strings."""
        tests = [
            "a!b@c|d\"e",           # all special chars
            "!" * 100,               # many bangs
            "@" * 100,               # many ats
            "\x00\x01\x02",          # control chars
            "a" * 10000,             # very long
            "",                       # empty
            "normal text with spaces",
        ]
        for t in tests:
            result = escape_index_term(t)
            assert isinstance(result, str)

    def test_strip_latex_robust(self):
        tests = [
            r"\(\mathbb{R}\)", r"\[x^2\]", r"\textbf{bold}",
            "", "plain", r"$$math$$", r"$inline$",
            r"\begin{equation}x\end{equation}",
        ]
        for t in tests:
            result = strip_latex(t)
            assert isinstance(result, str)

    def test_bracket_match_robust(self):
        # Valid cases
        assert brace_match("{hello}", 0) == 6
        # Edge cases
        assert brace_match("", 0) == -1
        assert brace_match("abc", 0) == -1  # no brace at start
        assert brace_match("x{", 0) == -1
        # Unbalanced
        assert brace_match("{unclosed", 0) == -1


class TestParserFuzz:
    """Fuzz the index parser."""

    @pytest.mark.parametrize("seed", range(10))
    def test_random_lines(self, seed):
        random.seed(seed)
        lines = [
            _random_string(random.randint(0, 80))
            for _ in range(random.randint(0, 100))
        ]
        result = parse_indented(lines)
        assert isinstance(result, list)

    def test_run_in_random(self):
        lines = [", ".join(
            f"{random.choice(string.ascii_letters)}: {random.randint(1,100)}"
            for _ in range(50)
        )]
        result = parse_run_in(lines)
        assert isinstance(result, list)
