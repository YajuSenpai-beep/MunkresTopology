"""异常测试 — 损坏文件、二进制、空文件等边界情况。"""
import os
import pytest
import tempfile
from latex_index.engine import IndexEngine
from latex_index.parser import parse_indented


class TestEmpty:
    def test_empty_content(self):
        engine = IndexEngine({"templates": {"l1": "\\idx{${key}}"}})
        ops = engine.find_insertions("", [{"term": "x", "level": 1}])
        assert len(ops) == 0

    def test_empty_entries(self):
        engine = IndexEngine({"templates": {"l1": "\\idx{${key}}"}})
        ops = engine.find_insertions("some text", [])
        assert len(ops) == 0

    def test_empty_parse(self):
        entries = parse_indented([""])
        assert len(entries) == 0


class TestBinaryFile:
    def test_binary_content(self):
        engine = IndexEngine({"templates": {"l1": "\\idx{${key}}"}})
        # 二进制内容不应崩溃
        binary_like = "\x00\x01\x02\x03text\x00field\x01"
        ops = engine.find_insertions(
            binary_like, [{"term": "field", "level": 1}]
        )
        # 引擎应该优雅处理
        assert isinstance(ops, list)


class TestUnbalancedBraces:
    def test_unbalanced_tex(self):
        engine = IndexEngine({"templates": {"l1": "\\idx{${key}}"}})
        content = "\\section{Introduction"  # 缺闭合 }
        entries = [{"term": "field", "level": 1, "page": [1]}]
        # 不应崩溃
        ops = engine.find_insertions(content, entries)
        assert isinstance(ops, list)


class TestHugeEntryList:
    def test_many_entries(self):
        engine = IndexEngine({"templates": {"l1": "\\idx{${key}}"}})
        # 生成大量条目
        entries = [
            {"term": f"term_{i}", "level": 1, "page": [i]}
            for i in range(1000)
        ]
        ops = engine.find_insertions(
            "This text contains none of the generated terms.", entries
        )
        # 都不匹配，但不应崩溃
        assert isinstance(ops, list)
        assert len(ops) == 0

    def test_duplicate_terms(self):
        engine = IndexEngine({"templates": {"l1": "\\idx{${key}}"}})
        entries = [
            {"term": "field", "level": 1, "page": [1]},
            {"term": "field", "level": 1, "page": [2]},  # duplicate
        ]
        ops = engine.find_insertions("the field is important", entries)
        assert len(ops) == 1  # deduplicated


class TestSpecialCharacters:
    def test_unicode_in_content(self):
        engine = IndexEngine({"templates": {"l1": "\\idx{${key}}"}})
        content = "The field of étude is rich."
        entries = [{"term": "field", "level": 1, "page": [1]}]
        ops = engine.find_insertions(content, entries)
        assert len(ops) == 1

    def test_unicode_in_term(self):
        engine = IndexEngine({"templates": {"l1": "\\idx{${key}}"}})
        content = "The Möbius band is fascinating."
        entries = [{"term": "Möbius band", "level": 1, "page": [1]}]
        ops = engine.find_insertions(content, entries)
        assert len(ops) == 1
