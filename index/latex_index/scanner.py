"""索引自动发现 — 扫描 .tex 文件中已有的 \\index{} 命令，汇总词条。"""

from __future__ import annotations

import re
from typing import Dict, List, Set

_INDEX_RE = re.compile(r"\\index\{([^}]*)\}")


def scan_existing_indexes(content: str) -> List[str]:
    """扫描 LaTeX 内容中所有已有的 \\index{...} 条目。

    Args:
        content: LaTeX 源文本

    Returns:
        去重排序后的词条列表
    """
    terms: Set[str] = set()
    for m in _INDEX_RE.finditer(content):
        term = m.group(1)
        # 提取排序键前的部分（如果有 @）
        if "@" in term:
            term = term.split("@", 1)[1]
        # 处理子条目 (!)
        parts = term.split("!")
        terms.add(parts[0].strip())  # 父条目
        for part in parts[1:]:
            terms.add(f"  {part.strip()}")  # 子条目（缩进标记）

    return sorted(terms)


def scan_idx_commands(content: str) -> Dict[str, List[str]]:
    """扫描 \\idx{} 和 \\idxmath{} 等自定义索引命令。

    Args:
        content: LaTeX 源文本

    Returns:
        {"idx": [terms], "idxmath": [terms], "idxsub": [(parent, child)]}
    """
    result: Dict[str, List[str]] = {
        "idx": [],
        "idxmath": [],
        "idxsub": [],
    }

    for m in re.finditer(r"\\idx\{([^}]*)\}", content):
        result["idx"].append(m.group(1))

    for m in re.finditer(r"\\idxmath\{([^}]*)\}\{([^}]*)\}", content):
        result["idxmath"].append(f"{m.group(1)} @ {m.group(2)}")

    for m in re.finditer(r"\\idxsub\{([^}]*)\}\{([^}]*)\}", content):
        result["idxsub"].append(f"{m.group(1)} ! {m.group(2)}")

    return result


def generate_entry_report(content: str) -> str:
    """生成索引条目报告。

    Args:
        content: LaTeX 源文本

    Returns:
        格式化的报告字符串
    """
    existing = scan_existing_indexes(content)
    custom = scan_idx_commands(content)

    lines = [
        "=" * 50,
        "索引条目扫描报告",
        "=" * 50,
        "",
        f"\\index{{}} 条目: {len(existing)}",
        f"\\idx{{}} 条目: {len(custom['idx'])}",
        f"\\idxmath{{}}{{}} 条目: {len(custom['idxmath'])}",
        f"\\idxsub{{}}{{}} 条目: {len(custom['idxsub'])}",
        "",
    ]

    if existing:
        lines.append("--- \\index{} ---")
        for t in existing[:30]:
            lines.append(f"  {t}")
        if len(existing) > 30:
            lines.append(f"  ... 还有 {len(existing)-30} 条")

    if custom["idx"]:
        lines.append("--- \\idx{} ---")
        for t in custom["idx"][:20]:
            lines.append(f"  {t}")

    return "\n".join(lines)
