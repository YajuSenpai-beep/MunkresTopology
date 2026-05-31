r"""xindy 排序规则生成器 — 生成 .xdy 文件，支持拼音/笔画/多语言混合索引。

Usage:
    from latex_index.xindy import generate_xdy
    xdy = generate_xdy(languages=["chinese", "english"])
    with open("index_style.xdy", "w") as f:
        f.write(xdy)
"""

from __future__ import annotations

from typing import Dict, List, Optional

# 预设语言排序规则
_LANGUAGE_RULES: Dict[str, str] = {
    "english": r"""
;; English: A-Z alphabet order
(define-sort-rule-orientations (forward))
(use-alphabet "en")
(define-letter-group "A" :prefixes ("\char65"))
(define-letter-group "B" :prefixes ("\char66"))
(define-letter-group "C" :prefixes ("\char67"))
(define-letter-group "D" :prefixes ("\char68"))
(define-letter-group "E" :prefixes ("\char69"))
(define-letter-group "F" :prefixes ("\char70"))
(define-letter-group "G" :prefixes ("\char71"))
(define-letter-group "H" :prefixes ("\char72"))
(define-letter-group "I" :prefixes ("\char73"))
(define-letter-group "J" :prefixes ("\char74"))
(define-letter-group "K" :prefixes ("\char75"))
(define-letter-group "L" :prefixes ("\char76"))
(define-letter-group "M" :prefixes ("\char77"))
(define-letter-group "N" :prefixes ("\char78"))
(define-letter-group "O" :prefixes ("\char79"))
(define-letter-group "P" :prefixes ("\char80"))
(define-letter-group "Q" :prefixes ("\char81"))
(define-letter-group "R" :prefixes ("\char82"))
(define-letter-group "S" :prefixes ("\char83"))
(define-letter-group "T" :prefixes ("\char84"))
(define-letter-group "U" :prefixes ("\char85"))
(define-letter-group "V" :prefixes ("\char86"))
(define-letter-group "W" :prefixes ("\char87"))
(define-letter-group "X" :prefixes ("\char88"))
(define-letter-group "Y" :prefixes ("\char89"))
(define-letter-group "Z" :prefixes ("\char90"))
""",
    "chinese-pinyin": r"""
;; Chinese: Pinyin order (A-Z based on romanized reading)
(define-sort-rule-orientations (forward))
(define-letter-group "拼音 A" :prefixes ("\char65"))
(define-letter-group "拼音 B" :prefixes ("\char66"))
(define-letter-group "拼音 C" :prefixes ("\char67"))
(define-letter-group "拼音 D" :prefixes ("\char68"))
(define-letter-group "拼音 E" :prefixes ("\char69"))
(define-letter-group "拼音 F" :prefixes ("\char70"))
(define-letter-group "拼音 G" :prefixes ("\char71"))
(define-letter-group "拼音 H" :prefixes ("\char72"))
(define-letter-group "拼音 J" :prefixes ("\char74"))
(define-letter-group "拼音 K" :prefixes ("\char75"))
(define-letter-group "拼音 L" :prefixes ("\char76"))
(define-letter-group "拼音 M" :prefixes ("\char77"))
(define-letter-group "拼音 N" :prefixes ("\char78"))
(define-letter-group "拼音 O" :prefixes ("\char79"))
(define-letter-group "拼音 P" :prefixes ("\char80"))
(define-letter-group "拼音 Q" :prefixes ("\char81"))
(define-letter-group "拼音 R" :prefixes ("\char82"))
(define-letter-group "拼音 S" :prefixes ("\char83"))
(define-letter-group "拼音 T" :prefixes ("\char84"))
(define-letter-group "拼音 W" :prefixes ("\char87"))
(define-letter-group "拼音 X" :prefixes ("\char88"))
(define-letter-group "拼音 Y" :prefixes ("\char89"))
(define-letter-group "拼音 Z" :prefixes ("\char90"))
""",
    "chinese-stroke": r"""
;; Chinese: Stroke-count order
(define-sort-rule-orientations (forward))
(define-sort-rules ("" stroke-count))
(define-letter-group "1 画")
(define-letter-group "2 画")
(define-letter-group "3 画")
(define-letter-group "4 画")
(define-letter-group "5 画")
(define-letter-group "6 画")
(define-letter-group "7 画")
(define-letter-group "8 画")
(define-letter-group "9 画")
(define-letter-group "10 画")
(define-letter-group "11 画")
(define-letter-group "12 画以上")
""",
    "math-symbols": r"""
;; Math symbols: separate letter group
(define-letter-group "Symbols" :prefixes ("\char92"))
""",
    "greek": r"""
;; Greek letters
(define-letter-group "Greek" :prefixes ("\char945" "\char946"))
""",
}


def generate_xdy(
    languages: Optional[List[str]] = None,
    custom_rules: Optional[str] = None,
    include_math: bool = True,
) -> str:
    """生成 xindy 索引样式文件 (.xdy)。

    Args:
        languages: 语言列表，如 ["english", "chinese-pinyin"]
        custom_rules: 自定义规则文本（追加到末尾）
        include_math: 是否包含数学符号分组

    Returns:
        .xdy 文件内容
    """
    if languages is None:
        languages = ["english"]

    parts = [
        ";; Auto-generated xindy style file by latex-index-tool",
        ";; Do not edit manually — use latex-index xindy --help for options",
        "",
        ";; ── 合并规则 ──",
        "(define-location-class \"arabic-page-numbers\" (\"arabic-numbers\"))",
        "(define-location-class-order (\"arabic-page-numbers\"))",
        "",
        "(define-attributes ((\"default\")))",
        "",
        ";; ── 标记规则 ──",
        "(markup-range :open \"\\markup-index-range-open{%s-%s}\" :close \"\")",
        "(markup-locref :class \"arabic-page-numbers\" :open \"\\hyperpage{\" :close \"}\")",
        "(markup-indexentry :open \"\\item \\markup-indexentry{%s}\" :close \"\")",
        "",
    ]

    if include_math:
        parts.append(";; ── 数学符号 ──")
        parts.append(_LANGUAGE_RULES["math-symbols"])
        parts.append("")

    for lang in languages:
        if lang in _LANGUAGE_RULES:
            parts.append(f";; ── {lang} ──")
            parts.append(_LANGUAGE_RULES[lang])
            parts.append("")
        else:
            parts.append(f";; Unknown language: {lang}, using english fallback")
            parts.append(_LANGUAGE_RULES["english"])
            parts.append("")

    parts.append(";; ── 通用配置 ──")
    parts.append("(markup-letter-group :open-head \"~n  \\textbf{\" :close-head \"}  ~n\")")
    parts.append("(markup-crossref-list :class \"see\" :open \"\\emph{see} \" :close \"\")")

    if custom_rules:
        parts.append("")
        parts.append(";; ── 自定义规则 ──")
        parts.append(custom_rules)

    return "\n".join(parts)


def generate_multilang_xdy(
    chapter_lang_map: Dict[int, str],
    base_languages: Optional[List[str]] = None,
) -> str:
    """为多语言项目生成 xindy 配置。

    支持章节级别的语言标记：
        chapter_lang_map = {
            1: "english",
            2: "english",
            3: "chinese-pinyin",
        }

    Args:
        chapter_lang_map: {章节编号: 语言代码}
        base_languages: 基础语言列表

    Returns:
        .xdy 内容
    """
    if base_languages is None:
        base_languages = ["english"]
    # Collect unique languages
    unique_langs = list(dict.fromkeys(base_languages + list(chapter_lang_map.values())))
    return generate_xdy(languages=unique_langs)


def list_supported_languages() -> List[str]:
    """返回支持的语言代码列表。"""
    return sorted(_LANGUAGE_RULES.keys())


def write_xdy(
    output_path: str,
    languages: Optional[List[str]] = None,
    custom_rules: Optional[str] = None,
) -> str:
    """生成并写入 .xdy 文件。

    Returns:
        生成的文件路径
    """
    content = generate_xdy(languages=languages, custom_rules=custom_rules)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content + "\n")
    return output_path
