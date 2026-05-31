r"""索引报告生成器 — 覆盖率分析、缺失词条检测、重复索引诊断。

Usage:
    from latex_index.reporter import generate_report
    report = generate_report(content, entries)
    print(report)
"""

from __future__ import annotations

import re
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple

from .scanner import scan_existing_indexes, scan_idx_commands
from .tex_utils import strip_latex


def generate_coverage_report(
    content: str, entries: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """分析索引覆盖率。

    Args:
        content: LaTeX 源文本
        entries: 目标索引条目列表

    Returns:
        {
            "total_entries": 总条目数,
            "found_entries": 在正文中找到的条目数,
            "missing_entries": [未在正文出现的条目],
            "coverage_pct": 覆盖率百分比,
            "l1_found": L1 命中数,
            "l1_total": L1 总数,
            "l2_found": L2 命中数,
            "l2_total": L2 总数,
        }
    """
    lower_content = content.lower()
    found: List[str] = []
    missing: List[str] = []
    l1_total = 0
    l1_found = 0
    l2_total = 0
    l2_found = 0

    for entry in entries:
        term = entry.get("term", "")
        level = entry.get("level", 1)
        if level == 1:
            l1_total += 1
        else:
            l2_total += 1

        search = strip_latex(term).lower()
        if len(search) < 2:
            continue
        if search in lower_content:
            found.append(term)
            if level == 1:
                l1_found += 1
            else:
                l2_found += 1
        else:
            missing.append(term)

    total = len(entries)
    return {
        "total_entries": total,
        "found_entries": len(found),
        "missing_entries": missing,
        "coverage_pct": round(len(found) / total * 100, 1) if total > 0 else 0.0,
        "l1_found": l1_found,
        "l1_total": l1_total,
        "l2_found": l2_found,
        "l2_total": l2_total,
        "found_terms": found,
    }


def find_duplicate_indexes(content: str) -> List[Tuple[str, List[int]]]:
    """查找重复出现的索引条目。

    Returns:
        [(term, [line_numbers]), ...] 按出现次数降序排列
    """
    counter: Counter[str] = Counter()
    for m in re.finditer(r"\\index\{([^}]*)\}", content):
        term = m.group(1)
        if "@" in term:
            term = term.split("@", 1)[1]
        counter[term.strip()] += 1

    # Also scan idx commands
    for cmd_pat in [r"\\idx\{([^}]*)\}", r"\\idx\[([^\]]*)\]"]:
        for m in re.finditer(cmd_pat, content):
            term = m.group(1).strip()
            if term:
                counter[term] += 1

    # Filter to duplicates only, sort by frequency desc
    duplicates = [
        (term, count) for term, count in counter.items() if count > 1
    ]
    duplicates.sort(key=lambda x: -x[1])

    # Get line numbers for each duplicate
    result: List[Tuple[str, List[int]]] = []
    lines = content.split("\n")
    for term, _ in duplicates:
        line_nums = []
        for i, line in enumerate(lines, 1):
            if term in line:
                line_nums.append(i)
        result.append((term, line_nums))
    return result


def validate_range_pairs(content: str) -> Dict[str, Any]:
    """检测 |( 和 |) 范围索引的配对情况。

    Returns:
        {
            "open_count": 开始标记数,
            "close_count": 结束标记数,
            "unclosed": [未闭合的条目],
            "unopened": [未开始的条目],
            "balanced": 是否平衡,
        }
    """
    opens: List[Tuple[str, int]] = []
    closes: List[Tuple[str, int]] = []

    # 查找所有 \index{...|(...} 和 \index{...|)...}
    for m in re.finditer(r"\\index\{([^}]*(?:\{[^}]*\}[^}]*)*)\}\|\(\)", content):
        pass  # |() pattern
    for m in re.finditer(r"\\index\{([^}]*)\}\|\(\)", content):
        pass

    # 简化版：提取 |( 和 |) 模式
    for m in re.finditer(r"\\index\{([^}]*)\|\([^}]*\}", content):
        line = content[: m.start()].count("\n") + 1
        opens.append((m.group(1), line))
    for m in re.finditer(r"\\index\{([^}]*)\|\)[^}]*\}", content):
        line = content[: m.start()].count("\n") + 1
        closes.append((m.group(1), line))

    # 按词条匹配
    open_terms = {t for t, _ in opens}
    close_terms = {t for t, _ in closes}

    return {
        "open_count": len(opens),
        "close_count": len(closes),
        "unclosed": [(t, ln) for t, ln in opens if t not in close_terms],
        "unopened": [(t, ln) for t, ln in closes if t not in open_terms],
        "balanced": len(opens) == len(closes) and open_terms == close_terms,
    }


def find_potential_missing_entries(
    content: str, candidate_list: List[str]
) -> List[str]:
    """在正文中搜索候选词，返回未建立索引的词条。

    Args:
        content: LaTeX 源文本
        candidate_list: 疑似应建立索引的词条列表

    Returns:
        在正文中出现但未建立索引的词条
    """
    existing_terms = set(scan_existing_indexes(content))
    # Also get idx command terms
    idx_data = scan_idx_commands(content)
    for t in idx_data.get("idx", []):
        existing_terms.add(t)
    for t in idx_data.get("idxmath", []):
        existing_terms.add(t.split("@")[-1] if "@" in t else t)

    lower_content = content.lower()
    missing = []
    for candidate in candidate_list:
        if candidate.lower() not in existing_terms:
            if candidate.lower() in lower_content:
                missing.append(candidate)
    return sorted(missing)


def generate_report(
    content: str,
    entries: Optional[List[Dict[str, Any]]] = None,
    candidates: Optional[List[str]] = None,
) -> str:
    """生成完整索引分析报告。

    Args:
        content: LaTeX 源文本
        entries: 目标索引条目（用于覆盖率分析）
        candidates: 候选词条（用于缺失检测）

    Returns:
        格式化的报告字符串
    """
    lines = [
        "=" * 60,
        "LaTeX 索引分析报告",
        "=" * 60,
        "",
    ]

    # 1. 现有索引统计
    existing = scan_existing_indexes(content)
    idx_data = scan_idx_commands(content)
    total_existing = len(existing) + len(idx_data["idx"]) + len(idx_data["idxmath"])
    lines.append("--- 已有索引 ---")
    existing_count = len(existing)
    idx_count = len(idx_data["idx"])
    idxmath_count = len(idx_data["idxmath"])
    idxsub_count = len(idx_data["idxsub"])
    lines.append(f"  \\index{{}} 条目: {existing_count}")
    lines.append(f"  \\idx{{}} 条目: {idx_count}")
    lines.append(f"  \\idxmath{{}}{{}} 条目: {idxmath_count}")
    lines.append(f"  \\idxsub{{}}{{}} 条目: {idxsub_count}")
    lines.append(f"  总计: {total_existing}")
    lines.append("")

    # 2. 覆盖率分析
    if entries:
        cov = generate_coverage_report(content, entries)
        lines.append("--- 覆盖率 ---")
        lines.append(f"  目标条目: {cov['total_entries']}")
        lines.append(f"  命中: {cov['found_entries']} ({cov['coverage_pct']}%)")
        lines.append(f"  未命中: {len(cov['missing_entries'])}")
        lines.append(f"  L1 命中率: {cov['l1_found']}/{cov['l1_total']}")
        lines.append(f"  L2 命中率: {cov['l2_found']}/{cov['l2_total']}")
        if cov["missing_entries"]:
            lines.append("")
            lines.append("  未命中条目 (前 20):")
            for m in cov["missing_entries"][:20]:
                lines.append(f"    - {m}")
        lines.append("")

    # 3. 重复索引
    duplicates = find_duplicate_indexes(content)
    if duplicates:
        lines.append("--- 重复索引 ---")
        lines.append(f"  重复条目数: {len(duplicates)}")
        for term, lns in duplicates[:10]:
            lines.append(f"    [{len(lns)}x] {term} (行: {', '.join(map(str, lns[:5]))})")
        lines.append("")

    # 4. 范围索引配对
    pairs = validate_range_pairs(content)
    if pairs["open_count"] > 0 or pairs["close_count"] > 0:
        lines.append("--- 范围索引配对 (|( ... |)) ---")
        lines.append(f"  开始标记: {pairs['open_count']}")
        lines.append(f"  结束标记: {pairs['close_count']}")
        lines.append(f"  状态: {'✓ 平衡' if pairs['balanced'] else '✗ 不平衡'}")
        if pairs["unclosed"]:
            lines.append("  未闭合:")
            for t, ln in pairs["unclosed"][:10]:
                lines.append(f"    L{ln}: {t}")
        if pairs["unopened"]:
            lines.append("  未开始:")
            for t, ln in pairs["unopened"][:10]:
                lines.append(f"    L{ln}: {t}")
        lines.append("")

    # 5. 潜在缺失
    if candidates:
        missing = find_potential_missing_entries(content, candidates)
        if missing:
            lines.append("--- 潜在缺失（正文出现但未建索引） ---")
            for m in missing[:20]:
                lines.append(f"    - {m}")
            lines.append("")

    return "\n".join(lines)
