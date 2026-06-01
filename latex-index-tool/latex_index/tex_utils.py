"""LaTeX 语义工具 — 数学模式、注释、抄录环境检测，特殊字符转义，括号匹配。

所有函数均为纯函数，无副作用，可直接用于单元测试。
"""

import re
from typing import List, Tuple

# ── 数学模式 ────────────────────────────────────────────

# 匹配所有数学环境开始/结束
_MATH_DELIMITERS = [
    (r"(?<!\\)\$", r"(?<!\\)\$"),       # $...$
    (r"(?<!\\)\$\$", r"(?<!\\)\$\$"),   # $$...$$
    (r"\\\(", r"\\\)"),                 # \(...\)
    (r"\\\[", r"\\\]"),                 # \[...\]
]
_MATH_ENVIRONMENTS = [
    "equation", "equation*", "align", "align*", "gather", "gather*",
    "multline", "multline*", "eqnarray", "eqnarray*",
    "math", "displaymath",
]


def find_math_ranges(content: str) -> List[Tuple[int, int]]:
    """查找所有数学模式区间 [(start, end), ...]。

    覆盖: $...$, $$...$$,  \\(...\\), \\[...\\], 以及 equation/align 等环境。
    """
    ranges: List[Tuple[int, int]] = []

    # 1. 配对分隔符
    for open_pat, close_pat in _MATH_DELIMITERS:
        for m in re.finditer(open_pat, content):
            start = m.end()
            close_m = re.search(close_pat, content[start:])
            if close_m:
                ranges.append((start, start + close_m.start()))

    # 2. \\begin{env}...\\end{env}
    for env in _MATH_ENVIRONMENTS:
        for m in re.finditer(rf"\\begin\{{{env}\}}", content):
            start = m.end()
            end_m = re.search(rf"\\end\{{{env}\}}", content[start:], re.DOTALL)
            if end_m:
                ranges.append((start, start + end_m.start()))

    # Merge overlapping/sorted
    ranges.sort()
    merged: List[Tuple[int, int]] = []
    for r in ranges:
        if merged and r[0] <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], r[1]))
        else:
            merged.append(r)
    return merged


def is_inside_math(content: str, pos: int) -> bool:
    """检查位置 pos 是否在数学模式内。"""
    for start, end in find_math_ranges(content):
        if start <= pos < end:
            return True
    return False


# ── 注释 ────────────────────────────────────────────────

def find_comment_ranges(content: str) -> List[Tuple[int, int]]:
    """查找所有注释区间（从 % 到行末）。"""
    ranges: List[Tuple[int, int]] = []
    for m in re.finditer(r"(?<!\\)%(.*)$", content, re.MULTILINE):
        ranges.append((m.start(), m.end()))
    return ranges


def is_inside_comment(content: str, pos: int) -> bool:
    """检查位置 pos 是否在注释内。"""
    for start, end in find_comment_ranges(content):
        if start <= pos < end:
            return True
    return False


# ── 抄录环境 ────────────────────────────────────────────

_VERBATIM_ENVS = [
    "verbatim", "lstlisting", "minted", "Verbatim",
    "boxedverbatim", "BVerbatim",
]

# 非索引区域环境（图形、表格、代码块）
_NO_INDEX_ENVS = [
    "tikzpicture", "pgfplots", "axis",
    "tabular", "tabularx", "longtable", "array",
]


def find_verbatim_ranges(content: str) -> List[Tuple[int, int]]:
    """查找所有抄录环境区间和 LaTeX3 语法区域。

    包含: verbatim 系列 + ExplSyntaxOn/Off + tikz/pgf/tabular 等。
    """
    ranges: List[Tuple[int, int]] = []

    # 1. 标准抄录环境
    for env in _VERBATIM_ENVS:
        for m in re.finditer(rf"\\begin\{{{env}\}}", content):
            start = m.end()
            end_m = re.search(rf"\\end\{{{env}\}}", content[start:], re.DOTALL)
            if end_m:
                ranges.append((start, start + end_m.start()))

    # 2. LaTeX3 语法区域: \ExplSyntaxOn ... \ExplSyntaxOff
    i = 0
    while True:
        on = content.find(r"\ExplSyntaxOn", i)
        if on < 0:
            break
        off = content.find(r"\ExplSyntaxOff", on)
        if off >= 0:
            ranges.append((on, off + len(r"\ExplSyntaxOff")))
            i = off + 1
        else:
            ranges.append((on, len(content)))  # 到文件末尾
            break

    # 3. 图形/表格环境（内部不插索引）
    for env in _NO_INDEX_ENVS:
        for m in re.finditer(rf"\\begin\{{{env}\}}", content):
            start = m.end()
            end_m = re.search(rf"\\end\{{{env}\}}", content[start:], re.DOTALL)
            if end_m:
                ranges.append((start, start + end_m.start()))

    ranges.sort()
    return ranges


def is_inside_verbatim(content: str, pos: int) -> bool:
    """检查位置 pos 是否在抄录环境内。"""
    for start, end in find_verbatim_ranges(content):
        if start <= pos < end:
            return True
    return False


# ── LaTeX 命令参数 ──────────────────────────────────────

# 标准 LaTeX 命令 — 这些命令的参数区域内不应插入索引
_STANDARD_COMMANDS = re.compile(
    r"\\(?:"
    r"section|chapter|subsection|subsubsection|paragraph|subparagraph|"
    r"label|ref|pageref|eqref|autoref|"
    r"cite|citep|citet|textcite|parencite|footcite|nocite|Cite|"
    r"index|idx|idxmath|idxsub|gls|acr|ac|"
    r"href|url|hyperref|"
    r"textbf|textit|textsl|textsc|texttt|textsf|textrm|textup|"
    r"emph|underline|"
    r"footnote|footnotemark|footnotetext|"
    r"includegraphics|include|input|"
    r"newcommand|renewcommand|providecommand|NewDocumentCommand|"
    r"DeclareMathOperator|operatorname|"
    r"mathbb|mathbf|mathcal|mathfrak|mathscr|mathit|mathrm|"
    r"boldsymbol|pmb|"
    r"pgfkeys|tikzset|foreach|csname|endcsname|"
    r"str_new:N|str_set:Nn|tl_new:N|int_new:N|prop_new:N|"
    r"caption|fbox|mbox|makebox|framebox|parbox|"
    r"scalebox|rotatebox|raisebox|"
    r"begin|end"
    r")(?:\*|@)?$"
)


def is_inside_command_arg(content: str, pos: int) -> bool:
    """检查 pos 是否在 LaTeX 命令的 {} 参数内部。

    覆盖 \\section, \\label, \\ref, \\cite, \\index, \\textbf,
    \\emph, \\footnote 等所有标准 LaTeX 命令的参数区域。
    也处理带可选参数的命令（如 \\cite[p.42]{key}）。
    """
    before = content[:pos]
    depth = 0
    for ch in before:
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
    if depth <= 0:
        return False

    # 找到包围此位置的最内层 { 位置
    brace_pos = before.rfind("{")
    if brace_pos < 0:
        return False
    # 检查 { 前面是否紧跟 \\command 或 \\command[opt]
    pre = before[:brace_pos].rstrip()
    # 移除可能存在的可选参数 [...]（如 \\cite[p.42]{key}）
    pre_no_opt = re.sub(r"\[[^]]*\]$", "", pre).rstrip()
    if _STANDARD_COMMANDS.search(pre_no_opt):
        # 格式化命令（textsl/textbf/textit/emph/underline 等）的内容允许索引
        formatting_cmds = re.compile(
            r"\\(?:text(?:bf|it|sl|sc|tt|sf|rm|up)|emph|underline)(?:\*|@)?$"
        )
        if formatting_cmds.search(pre_no_opt):
            return False
        return True
    return False


# ── 已有 \\index{} 命令 ──────────────────────────────────

def is_inside_index(content: str, pos: int) -> bool:
    """检查 pos 是否在已有索引命令内部。

    覆盖: \\index{...}, \\idx[display]{key}, \\idx{key},
          \\idxmath{sort}{display}, \\idxsub{parent}{child}
    """
    before = content[:pos]
    cmd_starts = []
    for cmd in ("\\index", "\\idxmath", "\\idxsub", "\\idx"):
        p = before.rfind(cmd)
        if p >= 0:
            cmd_starts.append((p, cmd))
    if not cmd_starts:
        return False
    cmd_start, cmd = max(cmd_starts, key=lambda x: x[0])
    after = content[cmd_start:]
    if cmd == "\\index":
        i = 6
    elif cmd in ("\\idxmath", "\\idxsub"):
        i = len(cmd)
    elif cmd == "\\idx":
        if cmd_start + 5 <= len(content) and content[cmd_start + 4] == "[":
            i = 4
            depth = 1
            for j in range(i + 1, len(after)):
                if after[j] == "[":
                    depth += 1
                elif after[j] == "]":
                    depth -= 1
                    if depth == 0:
                        if i <= pos - cmd_start <= j:
                            return True
                        i = j + 1
                        break
            if depth != 0:
                return False
            if i >= len(after) or after[i] != "{":
                return False
        else:
            i = 4
    else:
        return False
    if cmd in ("\\idxmath", "\\idxsub"):
        groups_to_check = 2
    else:
        groups_to_check = 1
    for _ in range(groups_to_check):
        if i >= len(after) or after[i] != "{":
            if groups_to_check > 1:
                break
            return False
        start_i = i
        depth = 0
        while i < len(after):
            ch = after[i]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            if depth == 0:
                if start_i <= pos - cmd_start <= i:
                    return True
                i += 1
                break
            i += 1
        if depth != 0:
            return False
    return False


# ── 括号匹配 ────────────────────────────────────────────

def brace_match(text: str, start: int) -> int:
    """从 start 位置（应为 '{'）找到匹配的 '}' 位置。

    Args:
        text: 文本内容
        start: 开括号 '{' 的位置

    Returns:
        匹配的 '}' 位置，未找到返回 -1
    """
    if start >= len(text) or text[start] != "{":
        return -1
    depth = 1
    i = start + 1
    while i < len(text) and depth > 0:
        if text[i] == "\\":
            i += 1  # skip escaped char
        elif text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
        i += 1
    return i - 1 if depth == 0 else -1


# ── 特殊字符转义 ────────────────────────────────────────

# makeindex 的特殊字符转义
_MAKEINDEX_SPECIAL = {
    "!": '"!',   # 子条目分隔符
    "@": '"@',   # 排序键分隔符
    "|": '"|',   # 页面格式分隔符
    '"': '""',   # 引号
}

# xindy 的特殊字符转义（不同于 makeindex）
_XINDY_SPECIAL = {
    "@": '"@',   # 排序键分隔符
    "|": '"|',   # 页面格式分隔符
    '"': '""',   # 引号
}


def escape_index_term(term: str, processor: str = "makeindex") -> str:
    """对索引条目中的特殊字符进行转义。

    保留 |see{...} 和 |seealso{...} 中的 | 不转义，
    因为它们是交叉引用操作符。

    Args:
        term: 索引条目文本
        processor: 索引处理器 ("makeindex" 或 "xindy")
    """
    special = _XINDY_SPECIAL if processor == "xindy" else _MAKEINDEX_SPECIAL
    result = []
    i = 0
    while i < len(term):
        ch = term[i]
        if ch == "\\" and i + 1 < len(term):
            result.append(ch)
            i += 1
            if i < len(term):
                result.append(term[i])
        elif ch == "|":
            rest = term[i + 1:] if i + 1 < len(term) else ""
            if rest.startswith("see{") or rest.startswith("seealso{"):
                result.append(ch)
            elif rest.startswith("(") or rest.startswith(")"):
                # |( open range and |) close range — keep literal
                result.append(ch)
            elif processor == "xindy":
                result.append('"|')
            else:
                result.append(_MAKEINDEX_SPECIAL["|"])
        elif ch == "!":
            if processor == "xindy":
                result.append(ch)  # xindy 不需要转义 !
            else:
                result.append(_MAKEINDEX_SPECIAL["!"])
        elif ch in special:
            result.append(special[ch])
        else:
            result.append(ch)
        i += 1
    return "".join(result)


# ── strip LaTeX ─────────────────────────────────────────

def strip_latex(term: str) -> str:
    """去除 LaTeX 数学模式标记，保留命令和括号（用于搜索匹配）。

    Examples:
        \\(\\mathbb{R}\\) -> \\mathbb{R}
        \\textbf{bold}    -> \\textbf{bold}
        plain text        -> plain text
    """
    s = term
    s = re.sub(r"\\\(|\\\)", "", s)    # 去数学模式 ( )
    s = re.sub(r"\\\[|\\\]", "", s)    # 去数学模式 [ ]
    return s.strip()
