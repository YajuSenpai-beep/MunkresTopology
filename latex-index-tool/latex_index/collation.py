r"""排序规则支持 — makeindex/xindy/拼音排序。

Usage:
    from latex_index.collation import sort_key_for

    keys = [(sort_key_for("中文", "pinyin"), "中文")]
"""

from __future__ import annotations

import unicodedata
from typing import List, Tuple

try:
    import pypinyin
    HAS_PINYIN = True
except ImportError:
    HAS_PINYIN = False


def _pinyin_sort_key(text: str) -> str:
    """将中文文本转换为拼音排序键。

    要求安装 pypinyin: pip install pypinyin
    未安装时回退到 Unicode 码点排序。
    """
    if not HAS_PINYIN:
        # 回退：使用 Unicode 数值排序
        return "".join(f"{ord(ch):06d}" for ch in text)

    segs: List[Tuple[str, str]] = []
    buf_chinese: List[str] = []
    buf_other: List[str] = []

    def flush_buf() -> None:
        nonlocal buf_chinese, buf_other
        if buf_chinese:
            py_list = pypinyin.lazy_pinyin(
                "".join(buf_chinese), style=pypinyin.Style.TONE, errors="ignore"
            )
            for py in py_list:
                segs.append((py, "zh"))
            buf_chinese = []
        if buf_other:
            segs.append(("".join(buf_other).lower(), "en"))
            buf_other = []

    for ch in text:
        if "一" <= ch <= "鿿" or "㐀" <= ch <= "䶿":
            if buf_other:
                flush_buf()
            buf_chinese.append(ch)
        elif ch.isspace() or unicodedata.category(ch).startswith("P"):
            flush_buf()
            segs.append((ch, "punct"))
        else:
            if buf_chinese:
                flush_buf()
            buf_other.append(ch)
    flush_buf()

    return "".join(seg[0] for seg in segs)


def _stroke_sort_key(text: str) -> str:
    """笔画排序键。回退到 Unicode 码点。"""
    # 笔画排序需要外部数据表，此处使用 Unicode 码点
    return "".join(f"{ord(ch):06d}" for ch in text)


def sort_key_for(text: str, collation: str = "default") -> str:
    """根据指定排序规则生成排序键。

    Args:
        text: 待排序的文本
        collation: 排序规则
            - "default" / "makeindex": 直接返回小写文本
            - "pinyin": 拼音排序（需 pypinyin）
            - "stroke": 笔画排序（回退到码点）
            - "unicode": Unicode 码点排序

    Returns:
        排序键字符串
    """
    if collation in ("default", "makeindex"):
        return text.lower()
    elif collation == "pinyin":
        return _pinyin_sort_key(text)
    elif collation == "stroke":
        return _stroke_sort_key(text)
    elif collation == "unicode":
        return "".join(f"{ord(ch):06d}" for ch in text)
    else:
        return text.lower()
