"""Aho-Corasick 多模式匹配器 — 单次扫描同时匹配所有词条。

复杂度 O(n + m) 其中 n=文本长度, m=所有词条长度之和。
相比逐条搜索 O(n*k)，在大词条集上有数量级提升。

Usage:
    matcher = PatternMatcher()
    matcher.add("field", "field")
    matcher.add("inverse function", "inverse_function")
    matcher.finish()
    for pos, key in matcher.search(content):
        print(f"Found {key} at {pos}")
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple


class _TrieNode:
    __slots__ = ("children", "fail", "output")

    def __init__(self) -> None:
        self.children: Dict[str, _TrieNode] = {}
        self.fail: Optional[_TrieNode] = None
        self.output: List[str] = []  # keys that end at this node


class PatternMatcher:
    """Aho-Corasick 自动机。

    使用方法：
    1. add() 逐个添加模式
    2. finish() 构建失败链接
    3. search() 扫描文本
    """

    def __init__(self, case_sensitive: bool = False) -> None:
        self._root = _TrieNode()
        self._case_sensitive = case_sensitive
        self._built = False
        self._patterns: Dict[str, str] = {}  # key -> original pattern

    def add(self, pattern: str, key: str) -> None:
        """添加一个搜索模式。

        Args:
            pattern: 搜索的文本模式
            key: 匹配时返回的标识符
        """
        if self._built:
            raise RuntimeError("Cannot add patterns after finish()")
        text = pattern if self._case_sensitive else pattern.lower()
        self._patterns[key] = pattern

        node = self._root
        for ch in text:
            if ch not in node.children:
                node.children[ch] = _TrieNode()
            node = node.children[ch]
        node.output.append(key)

    def finish(self) -> None:
        """构建失败链接（BFS）。调用后方可 search()。"""
        from collections import deque

        queue: deque[_TrieNode] = deque()

        # 第一层节点的 fail 指向 root
        for child in self._root.children.values():
            child.fail = self._root
            queue.append(child)

        # BFS 构建
        while queue:
            current = queue.popleft()
            for ch, child in current.children.items():
                queue.append(child)
                # 沿 fail 链查找
                f = current.fail
                while f is not None and ch not in f.children:
                    f = f.fail
                child.fail = f.children[ch] if f else self._root
                # 合并输出
                if child.fail:
                    child.output.extend(child.fail.output)

        self._built = True

    def search(self, text: str) -> List[Tuple[int, str, int]]:
        """在文本中搜索所有模式。

        Args:
            text: 待搜索文本

        Returns:
            [(位置, 键, 长度), ...] 按位置升序排列
        """
        if not self._built:
            self.finish()

        results: List[Tuple[int, str, int]] = []
        search_text = text if self._case_sensitive else text.lower()
        node: Optional[_TrieNode] = self._root

        for i, ch in enumerate(search_text):
            while node is not None and ch not in node.children:
                node = node.fail
            if node is None:
                node = self._root
                continue
            node = node.children[ch]
            for key in node.output:
                pat_len = len(self._patterns[key])
                start = i - pat_len + 1
                results.append((start, key, pat_len))

        results.sort()
        return results

    @property
    def pattern_count(self) -> int:
        return len(self._patterns)
