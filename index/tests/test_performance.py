"""性能测试 — 生成 500 页随机 .tex 并测试插入性能。"""
import pytest
import time
import random
import string
from latex_index.engine import IndexEngine


def generate_sample_tex(pages: int = 500, words_per_page: int = 200) -> str:
    """生成指定页数的随机 LaTeX 文档。

    Args:
        pages: 页数
        words_per_page: 每页约多少词

    Returns:
        生成的 .tex 内容
    """
    sections = [
        "Introduction",
        "Basic Concepts",
        "Advanced Theory",
        "Applications",
        "Conclusion",
    ]
    index_terms = [
        "field", "ring", "group", "topology", "manifold",
        "homology", "cohomology", "fibration", "bundle", "sheaf",
        "category", "functor", "morphism", "isomorphism", "kernel",
    ]

    lines = [
        "\\documentclass{article}",
        "\\begin{document}",
    ]

    for p in range(pages):
        section = random.choice(sections)
        lines.append(f"\\section{{{section} - Page {p+1}}}")

        # Generate paragraph
        words = []
        for _ in range(words_per_page):
            if random.random() < 0.1 and index_terms:
                words.append(random.choice(index_terms))
            else:
                length = random.randint(3, 10)
                word = "".join(random.choices(string.ascii_lowercase, k=length))
                words.append(word)

        # Split into sentences
        sentence = []
        for w in words:
            sentence.append(w)
            if len(sentence) >= random.randint(8, 15):
                lines.append(" ".join(sentence) + ".")
                sentence = []
        if sentence:
            lines.append(" ".join(sentence) + ".")

        # Occasional math
        if random.random() < 0.3:
            lines.append(f"The set \\(A_{{{p}}}\\) has property \\(P_{{{p}}}\\).")

    lines.append("\\end{document}")
    return "\n".join(lines)


class TestPerformance:
    def test_generate_10_pages(self):
        """快速测试：生成 10 页并验证格式。"""
        tex = generate_sample_tex(10, 50)
        assert "\\documentclass" in tex
        assert "\\end{document}" in tex
        assert len(tex) > 1000

    def test_generate_500_pages(self):
        """生成 500 页文档。"""
        start = time.time()
        tex = generate_sample_tex(500, 100)
        elapsed = time.time() - start
        size_mb = len(tex) / (1024 * 1024)
        print(f"\n  500 pages: {size_mb:.1f} MB, generated in {elapsed:.1f}s")
        assert len(tex) > 100000
        assert elapsed < 30  # should generate within 30 seconds

    def test_insert_performance(self):
        """测试插入 100 个条目的性能。"""
        tex = generate_sample_tex(100, 100)
        entries = [
            {"term": t, "level": 1, "page": [1]}
            for t in ["field", "ring", "group", "topology"]
        ]

        engine = IndexEngine({
            "templates": {"l1": "\\idx{${key}}"},
        })

        start = time.time()
        ops = engine.find_insertions(tex, entries)
        elapsed = time.time() - start

        print(f"\n  100 pages, 4 terms: found {len(ops)} in {elapsed:.3f}s")
        assert elapsed < 5  # should complete within 5 seconds

    def test_many_terms_performance(self):
        """测试大量条目的性能。"""
        tex = generate_sample_tex(50, 100)
        entries = [
            {"term": f"term_{i}", "level": 1, "page": [1]}
            for i in range(500)
        ]
        # Add some that will match
        entries.extend([
            {"term": "field", "level": 1, "page": [1]},
            {"term": "ring", "level": 1, "page": [1]},
        ])

        engine = IndexEngine({
            "templates": {"l1": "\\idx{${key}}"},
        })

        start = time.time()
        ops = engine.find_insertions(tex, entries)
        elapsed = time.time() - start

        print(f"\n  50 pages, 502 terms: found {len(ops)} in {elapsed:.3f}s")
        assert elapsed < 10  # should complete within 10 seconds
