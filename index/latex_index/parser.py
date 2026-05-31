"""索引文本 → JSON 转换器。

支持缩进格式（L1 顶格，L2 缩进）和 run-in 格式。
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple


def parse_pages(raw: str) -> List[int]:
    """解析页码字符串。

    Examples:
        "42, 45-47, 50" -> [42, 45, 46, 47, 50]
        "10-12, 15" -> [10, 11, 12, 15]
    """
    if not raw:
        return []
    pages: List[int] = []
    for part in re.split(r"\s*[,;，；]\s*", raw.strip()):
        rng = re.split(r"\s*[-–—]\s*", part.strip())
        if len(rng) == 2:
            a, b = int(rng[0]), int(rng[1])
            pages.extend(range(a, b + 1))
        else:
            try:
                n = int(part.strip())
                if n not in pages:
                    pages.append(n)
            except ValueError:
                pass
    return sorted(pages)


def extract_pages(line: str) -> Tuple[str, List[int]]:
    """从行末提取页码。

    Returns:
        (term, pages) — 词条名称和页码列表
    """
    m = re.search(r",?\s*(\d[\d\s,;，；\-–—]*)$", line)
    if not m:
        return line.strip(), []
    term = line[: m.start()].strip().rstrip(",")
    pages = parse_pages(m.group(1))
    return term, pages


def parse_indented(lines: List[str]) -> List[Dict[str, Any]]:
    """解析缩进格式的索引文本。

    L1: 顶格（缩进 < 2）
    L2: 缩进 ≥ 2
    """
    entries: List[Dict[str, Any]] = []
    current_parent: Optional[str] = None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        # 跳过字母标题
        if re.match(r"^[A-Z]\s*$", stripped):
            continue
        if re.match(r"^(Index|INDEX)", stripped, re.IGNORECASE):
            continue

        indent = len(line) - len(line.lstrip())
        term, pages = extract_pages(stripped)
        if not term:
            continue

        if indent < 2:
            current_parent = term
            entries.append({"term": term, "level": 1, "page": pages})
        elif current_parent:
            entries.append({
                "term": term,
                "level": 2,
                "parent": current_parent,
                "page": pages,
            })

    return entries


def parse_run_in(lines: List[str]) -> List[Dict[str, Any]]:
    """解析 run-in 格式的索引文本。"""
    entries: List[Dict[str, Any]] = []
    text = " ".join(lines).replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    current_parent: Optional[str] = None

    for seg in re.split(r"\s*[;；]\s*", text):
        term, pages = extract_pages(seg.strip())
        if not term:
            continue
        is_l1 = not current_parent or len(term) > 15 or term[0].isupper()
        if is_l1:
            current_parent = term
            entries.append({"term": term, "level": 1, "page": pages})
        elif current_parent:
            entries.append({
                "term": term,
                "level": 2,
                "parent": current_parent,
                "page": pages,
            })

    return entries


def parse_index_file(path: str, fmt: str = "indented") -> Dict[str, Any]:
    """解析索引文本文件，返回结构化 JSON。"""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if fmt == "run-in":
        entries = parse_run_in(lines)
    else:
        entries = parse_indented(lines)

    entries.sort(key=lambda e: (
        (e.get("parent") or "").lower(),
        e["level"],
        e["term"].lower(),
    ))

    return {
        "source": path,
        "format": fmt,
        "total": len(entries),
        "l1_count": sum(1 for e in entries if e["level"] == 1),
        "l2_count": sum(1 for e in entries if e["level"] == 2),
        "entries": entries,
    }
