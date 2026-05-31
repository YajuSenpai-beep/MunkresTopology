"""tex_utils.py 单元测试。"""
import pytest
from latex_index.tex_utils import (
    find_verbatim_ranges,
    is_inside_math,
    is_inside_comment,
    is_inside_verbatim,
    is_inside_command_arg,
    brace_match,
    escape_index_term,
    strip_latex,
)
from latex_index.parser import parse_pages, extract_pages


class TestMathDetection:
    def test_inline_math(self):
        assert is_inside_math("\\(x^2\\) is positive", 2) is True
        assert is_inside_math("\\(x^2\\) is positive", 10) is False

    def test_display_math(self):
        assert is_inside_math("\\[x^2\\] is positive", 3) is True
        assert is_inside_math("\\[x^2\\] is positive", 12) is False

    def test_dollar_math(self):
        assert is_inside_math("$x^2$ is positive", 2) is True
        assert is_inside_math("$x^2$ is positive", 8) is False

    def test_equation_env(self):
        # \begin{equation}\n = 17 chars, position 20 is inside x^2 body
        content = r"\begin{equation}" + "\n" + r"x^2" + "\n" + r"\end{equation}" + "\n is positive"
        assert is_inside_math(content, 20) is True
        assert is_inside_math(content, 50) is False

    def test_outside_math(self):
        assert is_inside_math("plain text without math", 5) is False


class TestCommentDetection:
    def test_inside_comment(self):
        assert is_inside_comment("text % comment here", 10) is True

    def test_outside_comment(self):
        assert is_inside_comment("text before % comment", 3) is False

    def test_escaped_percent(self):
        # \% is not a comment
        assert is_inside_comment("100\\% complete", 5) is False


class TestVerbatimDetection:
    def test_verbatim_env(self):
        # \begin{verbatim}\n = 18 chars, position 22 is inside body
        content = r"\begin{verbatim}" + "\ncode here\n" + r"\end{verbatim}" + "\n text"
        assert is_inside_verbatim(content, 22) is True
        assert is_inside_verbatim(content, 45) is False

    def test_lstlisting_env(self):
        content = "\\begin{lstlisting}\ncode\n\\end{lstlisting}"
        assert is_inside_verbatim(content, 20) is True


class TestCommandArg:
    def test_inside_section(self):
        content = "\\section{Introduction}"
        assert is_inside_command_arg(content, 12) is True

    def test_outside_section(self):
        content = "\\section{Intro} text"
        assert is_inside_command_arg(content, 18) is False

    def test_nested_braces(self):
        content = "\\textbf{\\emph{text}} extra"
        assert is_inside_command_arg(content, 13) is True


class TestBraceMatch:
    def test_simple(self):
        assert brace_match("{hello} world", 0) == 6

    def test_nested(self):
        # {a{b}c} — outer { at 0 matches } at 6
        assert brace_match("{a{b}c}", 0) == 6

    def test_escaped(self):
        assert brace_match("{a\\{b}", 0) == 5

    def test_not_brace(self):
        assert brace_match("hello", 0) == -1

    def test_unbalanced(self):
        assert brace_match("{hello", 0) == -1


class TestEscapeIndex:
    def test_bang(self):
        assert escape_index_term("A!B") == 'A"!B'

    def test_at(self):
        assert escape_index_term("A@B") == 'A"@B'

    def test_pipe(self):
        assert escape_index_term("A|B") == 'A"|B'

    def test_quote(self):
        assert escape_index_term('A"B') == 'A""B'

    def test_preserve_latex(self):
        assert escape_index_term("\\mathbb{R}") == "\\mathbb{R}"

    def test_no_special(self):
        assert escape_index_term("simple term") == "simple term"


class TestStripLatex:
    def test_math_wrapper(self):
        assert strip_latex("\\(\\mathbb{R}\\)") == "\\mathbb{R}"

    def test_textbf(self):
        assert strip_latex("\\textbf{bold}") == "\\textbf{bold}"

    def test_plain(self):
        assert strip_latex("plain text") == "plain text"


class TestParsePages:
    def test_single(self):
        assert parse_pages("42") == [42]

    def test_range(self):
        assert parse_pages("45-47") == [45, 46, 47]

    def test_mixed(self):
        assert parse_pages("42, 45-47, 50") == [42, 45, 46, 47, 50]

    def test_empty(self):
        assert parse_pages("") == []


class TestExtractPages:
    def test_with_pages(self):
        term, pages = extract_pages("Axiom of choice, 42, 45-47")
        assert term == "Axiom of choice"
        assert pages == [42, 45, 46, 47]

    def test_without_pages(self):
        term, pages = extract_pages("Axiom of choice")
        assert term == "Axiom of choice"
        assert pages == []


class TestTikzAndLatex3Envs:
    """Tests for tikzpicture, pgfplots, ExplSyntaxOn/Off regions."""

    def test_tikzpicture_skipped(self):
        content = (
            r"\begin{tikzpicture} field \end{tikzpicture} field"
        )
        ranges = find_verbatim_ranges(content)
        # The first "field" is inside tikzpicture, second is outside
        assert len(ranges) >= 1

    def test_pgfplots_skipped(self):
        content = r"\begin{axis} data \end{axis}"
        ranges = find_verbatim_ranges(content)
        assert len(ranges) >= 1

    def test_explsyntax_region(self):
        content = r"\ExplSyntaxOn code here \ExplSyntaxOff text"
        ranges = find_verbatim_ranges(content)
        assert len(ranges) >= 1

    def test_explsyntax_no_off(self):
        content = r"\ExplSyntaxOn code to end"
        ranges = find_verbatim_ranges(content)
        assert len(ranges) >= 1  # extends to EOF

    def test_tabular_skipped(self):
        content = r"\begin{tabular}{c} field \end{tabular}"
        ranges = find_verbatim_ranges(content)
        assert len(ranges) >= 1
