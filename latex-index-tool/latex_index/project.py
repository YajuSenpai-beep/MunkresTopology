r"""多文件 LaTeX 项目支持 — 解析 \\input/\\include 指令，按序处理子文件。"""

from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Dict, List, Match, Optional, Set, Tuple

logger = logging.getLogger(__name__)

# 匹配 \input{file} 或 \include{file}（支持文件名周围空格）
# 也匹配 \includeonly{...} 以便解析限制列表
_INPUT_RE = re.compile(
    r"(?<!\\)\\(input|include)\{\s*([^}]+?)\s*\}",
)
_INCLUDEONLY_RE = re.compile(
    r"(?<!\\)\\includeonly\s*\{\s*([^}]+?)\s*\}",
)


def resolve_tex_project(
    main_file: str,
    project_dir: Optional[str] = None,
    encoding: str = "utf-8",
) -> Tuple[str, List[str], Dict[str, int]]:
    r"""解析 LaTeX 项目的文件依赖。

    读取主文件，递归解析所有 \\input{} 和 \\include{} 指令，
    将子文件内容合并到主文件中（按出现顺序替换）。

    Args:
        main_file: 主 .tex 文件路径
        project_dir: 项目根目录（默认取 main_file 的目录）
        encoding: 文件编码

    Returns:
        (merged_content, file_list, line_map)
        - merged_content: 合并后完整内容
        - file_list: 处理过的文件列表（按依赖顺序）
        - line_map: {文件名: 在主文件中的起始行号}
    """
    if project_dir is None:
        project_dir = str(Path(main_file).parent)

    resolved: Set[str] = set()  # 已处理的文件（避免循环引用）
    file_list: List[str] = []
    line_map: Dict[str, int] = {}
    current_line = 1

    # 解析 \includeonly 限制列表
    includeonly: Optional[Set[str]] = None
    with open(main_file, "r", encoding=encoding) as f:
        main_content = f.read()
    m_only = _INCLUDEONLY_RE.search(main_content)
    if m_only:
        names = [n.strip() for n in m_only.group(1).split(",")]
        includeonly = set(names)
        logger.info("检测到 \\includeonly: %s", includeonly)

    def _resolve(path: str, cmd: str = "include") -> str:
        """读取文件并递归解析子文件引用。"""
        nonlocal current_line

        # \\includeonly 检查：仅对 \\include 有效
        if cmd == "include" and includeonly is not None:
            base = os.path.splitext(os.path.basename(path))[0]
            if base not in includeonly:
                logger.debug("\\includeonly 跳过: %s", path)
                return ""

        # 规范化路径
        full_path = _find_file(path, project_dir)
        if not full_path:
            logger.warning("文件未找到: %s", path)
            return ""

        # 避免循环
        real_path = os.path.realpath(full_path)
        if real_path in resolved:
            logger.warning("循环引用，跳过: %s", path)
            return ""
        resolved.add(real_path)
        file_list.append(real_path)
        line_map[os.path.basename(real_path)] = current_line

        try:
            with open(full_path, "r", encoding=encoding) as f:
                content = f.read()
        except UnicodeDecodeError:
            logger.warning("编码 %s 失败，尝试 latin-1: %s", encoding, full_path)
            with open(full_path, "r", encoding="latin-1") as f:
                content = f.read()

        # 替换 \input / \include
        def _replace_input(m: Match[str]) -> str:
            cmd_type = m.group(1)
            sub_path = m.group(2).strip()
            if not sub_path.endswith(".tex"):
                sub_path += ".tex"
            logger.debug("  解析引用: %s -> %s", path, sub_path)
            return _resolve(sub_path, cmd_type)

        result = _INPUT_RE.sub(_replace_input, content)
        current_line += content.count("\n") + 1
        return result

    # 解析主文件（main_content 已在上方读取）
    file_list.append(os.path.realpath(main_file))
    line_map[os.path.basename(main_file)] = 1
    resolved.add(os.path.realpath(main_file))
    current_line = main_content.count("\n") + 2

    def _replace_main(m: Match[str]) -> str:
        cmd_type = m.group(1)
        sub_path = m.group(2).strip()
        if not sub_path.endswith(".tex"):
            sub_path += ".tex"
        return _resolve(sub_path, cmd_type)

    merged = _INPUT_RE.sub(_replace_main, main_content)

    return merged, file_list, line_map


def detect_encoding(filepath: str) -> str:
    """自动检测文件编码。

    尝试 UTF-8，失败则回退到 latin-1。
    """
    encodings = ["utf-8", "latin-1", "cp1252", "iso-8859-1"]
    for enc in encodings:
        try:
            with open(filepath, "r", encoding=enc) as f:
                f.read(1024)  # 读一小块测试
            return enc
        except (UnicodeDecodeError, UnicodeError):
            continue
    return "utf-8"  # 最终回退


def detect_line_ending(content: str) -> str:
    """检测文本的换行符类型。

    Returns:
        "\r\n" (Windows), "\n" (Unix), 或 "\r" (old Mac)
    """
    if not content:
        return "\n"
    crlf = content.count("\r\n")
    lf = content.count("\n") - crlf
    cr = content.count("\r") - crlf
    if crlf >= lf and crlf >= cr:
        return "\r\n"
    if lf >= cr:
        return "\n"
    return "\r"


def preserve_line_endings(original: str, new_content: str) -> str:
    """确保新内容使用与原文件相同的换行符。"""
    original_le = detect_line_ending(original)
    new_le = detect_line_ending(new_content)
    if original_le != new_le:
        new_content = new_content.replace(new_le, original_le)
    return new_content


def _find_file(path: str, project_dir: str) -> Optional[str]:
    """在项目目录中查找文件。

    处理常见路径变体：带/不带 .tex 扩展名、斜杠方向、前后空格。
    """
    path = path.strip().replace("\\", "/")
    # 添加 .tex 扩展名（如果没有）
    if not path.endswith(".tex"):
        path_tex = path + ".tex"
    else:
        path_tex = path

    # 尝试多个路径
    candidates = [
        path_tex,
        path,
        os.path.join(project_dir, path_tex),
        os.path.join(project_dir, path),
    ]

    for candidate in candidates:
        norm = os.path.normpath(candidate)
        if os.path.isfile(norm):
            return norm

    # 最后尝试：检查父目录中的相对路径
    for candidate in [path_tex, path]:
        alt = os.path.join(os.path.dirname(project_dir), candidate)
        norm = os.path.normpath(alt)
        if os.path.isfile(norm):
            return norm

    return None


def list_input_files(main_file: str, project_dir: Optional[str] = None) -> List[str]:
    """列出项目中所有被 \\input/\\include 引用的文件（不合并内容）。"""
    _, file_list, _ = resolve_tex_project(main_file, project_dir)
    return file_list
