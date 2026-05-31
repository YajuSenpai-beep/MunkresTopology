"""集成测试 — 使用代表性的 .tex 样本验证端到端流程。"""
import pytest
from latex_index.engine import IndexEngine
from latex_index.parser import parse_indented

# ── 样本1：常规文档 ──
SAMPLE_PLAIN = r"""
\documentclass{article}
\begin{document}
\section{Introduction}
The concept of a field is central to algebra.
A ring is another algebraic structure.
The field of complex numbers is denoted by $\mathbb{C}$.
\end{document}
"""

# ── 样本2：含数学模式 ──
SAMPLE_MATH = r"""
The set \(\mathbb{R}\) of real numbers has the field property.
In $A \subset B$, the set $A$ is a subset.
The equation \(x^2 + y^2 = 1\) defines a circle.
But outside math, the word field should be indexed.
"""

# ── 样本3：含注释 ──
SAMPLE_COMMENT = r"""
We study the field of topology. % field is also used in algebra
The concept of a ring % not to be confused with jewelry
is fundamental.
"""

# ── 样本4：含抄录环境 ──
SAMPLE_VERBATIM = r"""
The following code defines a field:
\begin{verbatim}
class Field:
    def __init__(self):
        self.field = True
\end{verbatim}
After the verbatim block, the mathematical field concept continues.
"""

# ── 样本5：含自定义命令 ──
SAMPLE_CUSTOM = r"""
\newcommand{\R}{\mathbb{R}}
We study the field of \R.
\section{The Field Concept}
In this section, the term field appears in the title.
"""


class TestIntegration:
    def test_plain_document(self):
        engine = IndexEngine({
            "templates": {"l1": "\\idx{${key}}"},
            "aliases": {},
            "math_shortcuts": {},
        })
        entries = [
            {"term": "field", "level": 1, "page": [1]},
            {"term": "ring", "level": 1, "page": [1]},
        ]
        ops = engine.find_insertions(SAMPLE_PLAIN, entries)
        result = engine.apply(SAMPLE_PLAIN, ops)
        assert "\\idx{field}" in result
        assert "\\idx{ring}" in result

    def test_math_preserved(self):
        engine = IndexEngine({
            "templates": {"l1": "\\idx{${key}}"},
        })
        entries = [{"term": "field", "level": 1, "page": [1]}]
        ops = engine.find_insertions(SAMPLE_MATH, entries)
        result = engine.apply(SAMPLE_MATH, ops)
        # "field" in $\mathbb{C}$ should NOT be indexed
        # "field" in text "word field should" SHOULD be indexed
        assert result.count("\\idx{field}") == 1

    def test_comment_skipped(self):
        engine = IndexEngine({
            "templates": {"l1": "\\idx{${key}}"},
        })
        entries = [
            {"term": "field", "level": 1, "page": [1]},
            {"term": "ring", "level": 1, "page": [1]},
        ]
        ops = engine.find_insertions(SAMPLE_COMMENT, entries)
        result = engine.apply(SAMPLE_COMMENT, ops)
        # "field" in comment should NOT be indexed
        # "ring" in comment should NOT be indexed
        assert result.count("\\idx{field}") == 1  # text occurrence
        assert result.count("\\idx{ring}") == 1   # text occurrence

    def test_verbatim_preserved(self):
        engine = IndexEngine({
            "templates": {"l1": "\\idx{${key}}"},
        })
        entries = [{"term": "field", "level": 1, "page": [1]}]
        ops = engine.find_insertions(SAMPLE_VERBATIM, entries)
        result = engine.apply(SAMPLE_VERBATIM, ops)
        # "field" inside verbatim should NOT be indexed
        # "field" after verbatim block SHOULD be indexed
        assert result.count("\\idx{field}") == 1

    def test_section_title_handled(self):
        engine = IndexEngine({
            "templates": {"l1": "\\idx{${key}}"},
        })
        entries = [{"term": "field", "level": 1, "page": [1]}]
        ops = engine.find_insertions(SAMPLE_CUSTOM, entries)
        assert len(ops) >= 1  # at least text occurrence found


class TestParserIntegration:
    def test_parse_and_insert(self):
        """解析索引文本 → 生成 JSON → 直接用于插入。"""
        lines = [
            "Field, 1, 5",
            "  vector field, 5",
            "Ring, 10",
        ]
        entries = parse_indented(lines)
        assert len(entries) == 3
        assert entries[0]["level"] == 1
        assert entries[1]["parent"] == "Field"

        engine = IndexEngine({
            "templates": {"l1": "\\idx{${key}}", "l2": "\\idxsub{${parent}}{${child}}"},
        })
        content = "The field concept includes vector field theory. Ring theory is separate."
        ops = engine.find_insertions(content, entries)
        assert len(ops) >= 2
