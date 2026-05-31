"""回归测试 — 每次修复 bug 后添加用例，防止再次出错。"""
import pytest
from latex_index.engine import IndexEngine
from latex_index.tex_utils import (
    is_inside_math,
    is_inside_command_arg,
    is_inside_index,
    escape_index_term,
    brace_match,
    strip_latex,
)


class TestBugDoubleMathDelimiter:
    """Bug: \\(\\left( *\\right)\\) 被错误识别为两个数学块。"""

    def test_nested_paren_in_math(self):
        content = "\\(n\\left( {f,a}\\right)\\) is the winding number"
        assert is_inside_math(content, 5) is True


class TestBugBraceMatchEdge:
    """Bug: brace_match 对空内容返回错误值。"""

    def test_empty_brace(self):
        assert brace_match("{}", 0) == 1

    def test_deeply_nested(self):
        assert brace_match("{a{b{c}d}e}", 0) == 10


class TestBugStripLatexKeepsMath:
    """Bug: strip_latex 曾删除 \\mathbb 等数学命令。"""

    def test_mathbb_preserved(self):
        assert "\\mathbb" in strip_latex("\\(\\mathbb{R}\\)")

    def test_mathcal_preserved(self):
        assert "\\mathcal" in strip_latex("\\(\\mathcal{P}(A)\\)")


class TestBugIndexInsideIndex:
    """Bug: \index{} 内部被二次插入。"""

    def test_skip_existing_index(self):
        content = "See \\index{field} for details."
        # Position of 'f' in 'field' inside \index{field}
        pos = content.index("field")
        assert is_inside_index(content, pos) is True

    def test_outside_index_ok(self):
        content = "\\index{field} and field again."
        pos = content.rindex("field")  # second occurrence
        assert is_inside_index(content, pos) is False


class TestBugEscapeSpecialChars:
    """Bug: makeindex 特殊字符未转义导致索引编译失败。"""

    def test_bang_escaped(self):
        assert escape_index_term("A!B") == 'A"!B'

    def test_multiple_special(self):
        result = escape_index_term("A!B@C|D")
        assert '"!' in result
        assert '"@' in result
        assert '"|' in result

    def test_non_special_untouched(self):
        assert escape_index_term("simple term") == "simple term"


class TestBugSearchInsideCommandArg:
    """Bug: 搜索引擎在 \\section{...} 内插入索引。"""

    def test_section_arg_skipped(self):
        content = "\\section{The Field Concept}"
        pos = content.index("Field")
        assert is_inside_command_arg(content, pos) is True
