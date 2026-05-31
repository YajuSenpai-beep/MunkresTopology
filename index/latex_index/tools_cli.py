r"""统一批处理工具 CLI — 将 tools/ 中的常用脚本整合为 latex-index tools 子命令。

Usage:
    latex-index tools format-env --chapter 2         # 修复环境格式
    latex-index tools convert-exercises --chapter 3  # 转换习题格式
    latex-index tools clean-ex-envs                  # 清理习题内 theorem/proof
    latex-index tools fix-subitems                   # 修复 (a) 父级条目
    latex-index tools wrap-examples                  # 用 centeredblock 包裹 example
    latex-index tools ocr-fix                        # OCR 拼写修复
    latex-index tools scan-issues                   # 扫描已知问题
"""

from __future__ import annotations

import argparse
import glob
import logging
import os
import re
from typing import Any, Dict, List, Match, Optional, Tuple

logger = logging.getLogger("index_tool")


def cmd_format_env(args: argparse.Namespace) -> int:
    """修复环境格式: \begin{env}text -> 三行拆分."""
    envs = [
        "proof",
        "theorem",
        "lemma",
        "corollary",
        "definition",
        "example",
        "proposition",
        "addendum",
        "property",
    ]

    def process(fp: str) -> int:
        with open(fp, "r", encoding="utf-8") as f:
            lines = f.readlines()
        fixes = _format_env_in_lines(lines, envs)
        if fixes > 0:
            with open(fp, "w", encoding="utf-8") as f:
                f.writelines(lines)
            logger.info("%s: %d fixes", os.path.basename(fp), fixes)
        return fixes

    files = _resolve_files(args)
    total = _for_each_file(files, args, process)
    logger.info("Total: %d fixes", total)
    return 0


def _format_env_in_lines(lines: List[str], envs: List[str]) -> int:
    fixes = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("%") or not stripped:
            i += 1
            continue
        indent = line[: len(line) - len(line.lstrip())]
        for env in envs:
            begin_tag = rf"\begin{{{env}}}"
            end_tag = rf"\end{{{env}}}"
            if begin_tag not in stripped:
                continue
            idx = stripped.index(begin_tag) + len(begin_tag)
            rest = stripped[idx:].strip()
            if rest.startswith("["):
                bd = 0
                oe = -1
                for j, ch in enumerate(rest):
                    if ch == "[":
                        bd += 1
                    elif ch == "]" and bd == 1:
                        oe = j
                        break
                    elif ch == "]":
                        bd -= 1
                if oe >= 0:
                    rest = rest[oe + 1 :].strip()
            if not rest:
                i += 1
                continue
            body_indent = indent + "\t"
            if end_tag in stripped:
                # single-line env
                opt_arg = _extract_opt_arg(stripped, begin_tag)
                content_start = stripped.index(begin_tag) + len(begin_tag)
                tmp = stripped[content_start:].strip()
                if tmp.startswith("["):
                    bd = 0
                    oe = -1
                    for j, ch in enumerate(tmp):
                        if ch == "[":
                            bd += 1
                        elif ch == "]" and bd == 1:
                            oe = j
                            break
                        elif ch == "]":
                            bd -= 1
                    if oe >= 0:
                        tmp = tmp[oe + 1 :].strip()
                content = tmp[: tmp.index(end_tag)].strip()
                if opt_arg:
                    lines[i] = indent + begin_tag + opt_arg + "\n"
                else:
                    lines[i] = indent + begin_tag + "\n"
                lines.insert(i + 1, body_indent + content + "\n")
                lines.insert(i + 2, indent + end_tag + "\n")
                fixes += 1
                break
            else:
                opt_arg = _extract_opt_arg(stripped, begin_tag)
                after_begin = stripped[stripped.index(begin_tag) + len(begin_tag) :].strip()
                if after_begin.startswith("["):
                    bd = 0
                    oe = -1
                    for j, ch in enumerate(after_begin):
                        if ch == "[":
                            bd += 1
                        elif ch == "]" and bd == 1:
                            oe = j
                            break
                        elif ch == "]":
                            bd -= 1
                    if oe >= 0:
                        opt_arg = after_begin[: oe + 1]
                        rest = after_begin[oe + 1 :].strip()
                if opt_arg:
                    lines[i] = indent + begin_tag + opt_arg + "\n"
                else:
                    lines[i] = indent + begin_tag + "\n"
                lines.insert(i + 1, body_indent + rest + "\n")
                fixes += 1
                break
        i += 1
    return fixes


def _extract_opt_arg(stripped: str, begin_tag: str) -> str:
    after = stripped[stripped.index(begin_tag) + len(begin_tag) :].strip()
    if not after.startswith("["):
        return ""
    bd = 0
    for j, ch in enumerate(after):
        if ch == "[":
            bd += 1
        elif ch == "]" and bd == 1:
            return after[: j + 1]
        elif ch == "]":
            bd -= 1
    return ""


def cmd_convert_exercises(args: argparse.Namespace) -> int:
    r"""将 \section*{Exercises} 后的文本转换为 enumerate 格式."""

    def process(fp: str) -> int:
        with open(fp, "r", encoding="utf-8") as f:
            c = f.read()
        if r"\begin{enumerate}[itemsep=0.4em" in c and "label=\\arabic*" in c:
            logger.info("%s: already converted", os.path.basename(fp))
            return 0
        lines = c.split("\n")
        blocks: List[Tuple[int, int]] = []
        in_block = False
        block_start = 0
        for i, line in enumerate(lines):
            is_ex = r"\section*{Exercises}" in line
            is_next = r"\section*{" in line and "Exercises" not in line
            if is_ex:
                if in_block:
                    blocks.append((block_start, i - 1))
                in_block = True
                block_start = i
            elif is_next and in_block:
                blocks.append((block_start, i - 1))
                in_block = False
        if in_block:
            blocks.append((block_start, len(lines) - 1))
        if not blocks:
            return 0
        total_ex = _convert_exercise_blocks(lines, blocks)
        with open(fp, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        logger.info("%s: %d blocks, %d exercises", os.path.basename(fp), len(blocks), total_ex)
        return total_ex

    files = _resolve_files(args)
    total = _for_each_file(files, args, process)
    logger.info("Total: %d exercises", total)
    return 0


def _convert_exercise_blocks(lines: List[str], blocks: List[Tuple[int, int]]) -> int:
    total_ex = 0
    for b_idx, (start, end) in enumerate(blocks):
        block_lines = lines[start + 1 : end + 1]
        items: List[Dict[str, Any]] = []
        current: Optional[Dict[str, Any]] = None
        for line in block_lines:
            s = line.strip()
            if not s:
                continue
            m = re.match(r"^(\d+)\.\s+(.*)", s)
            if m:
                if current is not None:
                    items.append(current)
                current = {"num": int(m.group(1)), "text": m.group(2), "subs": []}
                continue
            m = re.match(r"^\(([a-z])\)\s+(.*)", s)
            if m and current is not None:
                current["subs"].append((m.group(1), m.group(2)))
                continue
            if current is not None:
                if current["subs"]:
                    letter, text = current["subs"][-1]
                    current["subs"][-1] = (letter, text + " " + s)
                else:
                    current["text"] += " " + s
        if current is not None:
            items.append(current)
        new_lines = [lines[start]]
        new_lines.append(
            r"\begin{enumerate}[itemsep=0.4em, parsep=0pt, topsep=0pt, "
            r"partopsep=0pt, leftmargin=*, label=\arabic*., ref=\arabic*]"
        )
        for item in items:
            if item["subs"]:
                new_lines.append(r"\item " + item["text"])
                new_lines.append(
                    r"  \begin{enumerate}[itemsep=0.2em, parsep=0pt, "
                    r"topsep=0pt, partopsep=0pt, leftmargin=*, "
                    r"label=(\alph*), align=left]"
                )
                for letter, text in item["subs"]:
                    new_lines.append(r"  \item " + text)
                new_lines.append(r"  \end{enumerate}")
            else:
                new_lines.append(r"\item " + item["text"])
        new_lines.append(r"\end{enumerate}")
        old_len = end - start + 1
        lines[start : end + 1] = new_lines
        diff = len(new_lines) - old_len
        for j in range(b_idx + 1, len(blocks)):
            blocks[j] = (blocks[j][0] + diff, blocks[j][1] + diff)
        total_ex += len(items)
    return total_ex


def cmd_clean_ex_envs(args: argparse.Namespace) -> int:
    """习题块内 theorem/proof/lemma -> \\textsl{}."""
    tags = {"theorem": "Theorem.", "proof": "Proof.", "lemma": "Lemma"}

    def process(fp: str) -> int:
        with open(fp, "r", encoding="utf-8") as f:
            c = f.read()
        lines = c.split("\n")
        ex_ranges: List[Tuple[int, int]] = []
        in_ex = False
        ex_start = 0
        for i, line in enumerate(lines):
            if r"\section*{Exercises}" in line:
                if in_ex:
                    ex_ranges.append((ex_start, i - 1))
                in_ex = True
                ex_start = i
            elif r"\section*{" in line and "Exercises" not in line and in_ex:
                ex_ranges.append((ex_start, i - 1))
                in_ex = False
        if in_ex:
            ex_ranges.append((ex_start, len(lines) - 1))
        fixes = 0
        for start, end in ex_ranges:
            block = "\n".join(lines[start:end + 1])
            for env_name, display in tags.items():
                begin_tag = rf"\begin{{{env_name}}}"
                end_tag = rf"\end{{{env_name}}}"

                def _repl_begin(m: Match[str]) -> str:
                    opt = m.group(1) if m.group(1) else ""
                    if opt:
                        return rf"\textsl{{{display} ({opt.strip('[]')}).}}"
                    return rf"\textsl{{{display}}}"

                block = re.sub(
                    re.escape(begin_tag) + r"(\[.*?\])?",
                    _repl_begin, block,
                )
                block = re.sub(re.escape(end_tag), "", block)
            new_block_lines = block.split("\n")
            lines[start:end + 1] = new_block_lines
            fixes += 1
        if fixes > 0:
            with open(fp, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            logger.info("%s: %d blocks cleaned", os.path.basename(fp), fixes)
        return fixes

    files = _resolve_files(args)
    total = _for_each_file(files, args, process)
    logger.info("Total: %d blocks", total)
    return 0


def cmd_fix_subitems(args: argparse.Namespace) -> int:
    """修复 \\item (a) TEXT -> \\item + sub-enumerate."""

    def process(fp: str) -> int:
        with open(fp, "r", encoding="utf-8") as f:
            lines = f.readlines()
        fixes = 0
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.lstrip()
            if not stripped.startswith(r"\item (a) "):
                i += 1
                continue
            if r"\begin{enumerate}" in stripped:
                i += 1
                continue
            indent = line[: len(line) - len(line.lstrip())]
            a_text = stripped[len(r"\item (a) "):]
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j >= len(lines) or not lines[j].lstrip().startswith(r"\begin{enumerate}"):
                i += 1
                continue
            lines[i] = indent + r"\item" + "\n"
            k = j + 1
            while k < len(lines):
                if lines[k].lstrip().startswith(r"\item"):
                    sub_indent = lines[k][: len(lines[k]) - len(lines[k].lstrip())]
                    lines.insert(k, sub_indent + r"\item " + a_text + "\n")
                    fixes += 1
                    break
                k += 1
            i += 1
        if fixes > 0:
            with open(fp, "w", encoding="utf-8") as f:
                f.writelines(lines)
            logger.info("%s: %d fixes", os.path.basename(fp), fixes)
        return fixes

    files = _resolve_files(args)
    total = _for_each_file(files, args, process)
    logger.info("Total: %d fixes", total)
    return 0


def cmd_ocr_fix(args: argparse.Namespace) -> int:
    """OCR 拼写修复."""
    word_boundary_reps = [(r"\bongin\b", "origin")]
    reps = [
        ("posiave", "positive"),
        ("Structly", "Strictly"),
        ("ngorously", "rigorously"),
        ("conduction", "condition"),
        ("Schernatically", "Schematically"),
        ("Siliarly", "Similarly"),
        ("Simularly", "Similarly"),
        ("to proved", "to prove"),
    ]

    def process(fp: str) -> int:
        with open(fp, "r", encoding="utf-8") as f:
            c = f.read()
        fixes = 0
        for pat, repl in word_boundary_reps:
            new_c, n = re.subn(pat, repl, c)
            if n > 0:
                c = new_c
                fixes += n
        for old, new in reps:
            if old in c:
                c = c.replace(old, new)
                fixes += 1
        if fixes > 0:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(c)
            logger.info("%s: %d OCR fixes", os.path.basename(fp), fixes)
        return fixes

    files = _resolve_files(args)
    total = _for_each_file(files, args, process)
    logger.info("Total: %d fixes", total)
    return 0


def cmd_scan_issues(args: argparse.Namespace) -> int:
    """扫描已知问题（OCR 拼写、Unicode 引号、格式问题）."""
    files = _resolve_files(args)
    for fp in files:
        with open(fp, "r", encoding="utf-8") as f:
            c = f.read()
        issues = []
        lines = c.split("\n")
        for i, line in enumerate(lines, 1):
            s = line.strip()
            if not s or s.startswith("%"):
                continue
            for w in [
                "ongin",
                "posiave",
                "Structly",
                "ngorously",
                "conduction",
                "Schernatically",
                "Siliarly",
                "Simularly",
                "to proved",
                "senes",
                "lumit",
            ]:
                if w in s:
                    issues.append(f"L{i}: spelling '{w}'")
            for ch in ["“", "”", "‘", "’"]:
                if ch in s:
                    issues.append(f"L{i}: Unicode smart quote")
            oq = s.count("``")
            cq = s.count("''")
            if oq != cq and (oq > 0 or cq > 0):
                issues.append(f"L{i}: unbalanced quotes ({oq}/{cq})")
        if issues:
            print(f"\n{os.path.basename(fp)}: {len(issues)} issues")
            for iss in issues[:10]:
                print(f"  {iss}")
            if len(issues) > 10:
                print(f"  ... +{len(issues) - 10} more")
        else:
            print(f"{os.path.basename(fp)}: clean")
    return 0


def cmd_wrap_examples(args: argparse.Namespace) -> int:
    """用 \\begin{centeredblock} 包裹所有 example 环境."""

    def process(fp: str) -> int:
        with open(fp, "r", encoding="utf-8") as f:
            c = f.read()
        new_c = _wrap_with_centeredblock(c)
        if new_c != c:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(new_c)
            n = c.count(r"\begin{example}")
            logger.info("%s: %d examples wrapped", os.path.basename(fp), n)
            return n
        return 0

    files = _resolve_files(args)
    total = _for_each_file(files, args, process)
    logger.info("Total: %d examples", total)
    return 0


def _wrap_with_centeredblock(content: str) -> str:
    begin_ex = r"\begin{example}"
    end_ex = r"\end{example}"
    begin_cb = r"\begin{centeredblock}"
    result = []
    i = 0
    while i < len(content):
        idx = content.find(begin_ex, i)
        if idx < 0:
            result.append(content[i:])
            break
        before = content[max(0, idx - 30) : idx]
        if begin_cb in before:
            result.append(content[i : idx + len(begin_ex)])
            i = idx + len(begin_ex)
            continue
        result.append(content[i:idx])
        end_idx = content.find(end_ex, idx)
        if end_idx < 0:
            result.append(content[idx:])
            break
        example_body = content[idx : end_idx + len(end_ex)]
        result.append(begin_cb + "\n" + example_body + "\n" + r"\end{centeredblock}")
        i = end_idx + len(end_ex)
    return "".join(result)


def _resolve_files(args: argparse.Namespace) -> List[str]:
    """根据参数解析要处理的文件列表."""
    if hasattr(args, "files") and args.files:
        files: Any = args.files
        return list(files) if isinstance(files, list) else [str(files)]
    if hasattr(args, "chapter") and args.chapter is not None:
        ch: str = str(args.chapter).zfill(2)
        pattern = f"chapters/Chapter_{ch}_*.tex"
        return sorted(glob.glob(pattern))
    # 所有章节
    return sorted(glob.glob("chapters/Chapter_*.tex"))


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    """为批处理工具子命令添加通用参数."""
    parser.add_argument("--chapter", type=int, help="章节编号（默认所有）")
    parser.add_argument("--files", nargs="+", help="指定文件列表")
    parser.add_argument(
        "--continue-on-error", action="store_true",
        help="遇到错误时继续处理剩余文件",
    )


def _for_each_file(
    files: List[str], args: argparse.Namespace, processor: Any,
) -> int:
    """遍历文件执行 processor(fp)，支持 --continue-on-error."""
    total = 0
    errors: List[Tuple[str, str]] = []
    for fp in files:
        try:
            n = processor(fp)
            total += n
        except Exception as e:
            if getattr(args, "continue_on_error", False):
                logger.error("%s: %s", os.path.basename(fp), e)
                errors.append((fp, str(e)))
            else:
                raise
    if errors:
        logger.warning("%d/%d files had errors", len(errors), len(files))
    return total


def register_tools_parser(subparsers: Any) -> None:
    """注册 tools 子命令及其子命令."""
    p_tools = subparsers.add_parser("tools", help="批处理工具集")
    tools_sub = p_tools.add_subparsers(dest="tool_command", help="工具名称")

    # format-env
    p = tools_sub.add_parser("format-env", help="修复环境格式 begin{env}text -> 三行")
    _add_common_args(p)
    p.add_argument("--dry-run", action="store_true", help="仅显示，不修改")
    p.set_defaults(func=cmd_format_env)

    # convert-exercises
    p = tools_sub.add_parser("convert-exercises", help="转换习题为 enumerate 格式")
    _add_common_args(p)
    p.set_defaults(func=cmd_convert_exercises)

    # clean-ex-envs
    p = tools_sub.add_parser("clean-ex-envs", help="清理习题内 theorem/proof/lemma")
    _add_common_args(p)
    p.set_defaults(func=cmd_clean_ex_envs)

    # fix-subitems
    p = tools_sub.add_parser("fix-subitems", help="修复 (a) 父级条目")
    _add_common_args(p)
    p.set_defaults(func=cmd_fix_subitems)

    # ocr-fix
    p = tools_sub.add_parser("ocr-fix", help="OCR 拼写修复")
    _add_common_args(p)
    p.set_defaults(func=cmd_ocr_fix)

    # scan-issues
    p = tools_sub.add_parser("scan-issues", help="扫描已知问题")
    _add_common_args(p)
    p.set_defaults(func=cmd_scan_issues)

    # wrap-examples
    p = tools_sub.add_parser("wrap-examples", help="用 centeredblock 包裹 example")
    _add_common_args(p)
    p.set_defaults(func=cmd_wrap_examples)
