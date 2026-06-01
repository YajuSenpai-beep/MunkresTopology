"""通用 LaTeX 索引插入引擎。

配置驱动，项目无关。核心逻辑：
1. 接收 LaTeX 文本 + 索引条目 + 配置
2. 查找所有可插入位置（避免数学模式/注释/抄录/命令参数）
3. 去重（长词优先，避免重叠）
4. 输出操作列表（从尾到头排序，安全插入）

Usage:
    from index.py.engine import IndexEngine
    engine = IndexEngine(config)
    ops = engine.find_insertions(content, entries)
    result = engine.apply(content, ops)
"""

from __future__ import annotations

import logging
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

try:
    from tqdm import tqdm as _tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False

from .matcher import PatternMatcher
from .tex_utils import (
    escape_index_term,
    find_comment_ranges,
    find_math_ranges,
    find_verbatim_ranges,
    is_inside_command_arg,
    is_inside_index,
    strip_latex,
)

logger = logging.getLogger(__name__)

# ── 类型定义 ────────────────────────────────────────────

Entry = Dict[str, Any]             # {"term": ..., "level": 1|2, ...}
Operation = Dict[str, Any]         # {"pos": int, "cmd": str, "entry": Entry}


class IndexEngine:
    """通用索引插入引擎。

    Args:
        config: 配置字典，必须包含 templates 字段。
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.templates: Dict[str, str] = config.get("templates", {})
        self.aliases: Dict[str, List[str]] = config.get("aliases", {})
        self.math_shortcuts: Dict[str, List[str]] = config.get("math_shortcuts", {})
        self.skip_patterns: List[str] = config.get("skip_patterns", [])
        self.index_processor: str = config.get("index_processor", "makeindex")

    # ── 核心 API ────────────────────────────────────────

    def find_insertions(
        self, content: str, entries: List[Entry],
        progress: bool = False,
    ) -> List[Operation]:
        """查找所有可插入位置。

        Args:
            content: LaTeX 源文本
            entries: 索引条目列表
            progress: 是否显示进度条（需要安装 tqdm）

        Returns:
            操作列表，按位置降序排列（从尾到头）
        """
        # 预计算禁区
        no_go: List[Tuple[int, int]] = []
        no_go.extend(find_math_ranges(content))
        no_go.extend(find_comment_ranges(content))
        no_go.extend(find_verbatim_ranges(content))
        no_go.sort()

        def _is_forbidden(pos: int) -> bool:
            for s, e in no_go:
                if s <= pos < e:
                    return True
            return False

        ops: List[Operation] = []

        # 按纯文本长度降序排列（长词优先，避免子串冲突）
        sorted_entries = sorted(
            entries,
            key=lambda e: len(strip_latex(e.get("term", ""))),
            reverse=True,
        )

        entry_iter = sorted_entries
        if progress and HAS_TQDM:
            entry_iter = _tqdm(sorted_entries, desc="Finding insertions", unit="entry")
        elif progress:
            logger.warning("tqdm 未安装，使用 pip install tqdm 安装后可见进度条")

        for entry in entry_iter:
            term = entry.get("term", "")
            if not term:
                continue

            insert_pos = -1
            cmd: Optional[str] = None

            if entry.get("level") == 1 and entry.get("sort_key"):
                # ── 数学符号 ──
                raw_latex = strip_latex(term)  # \( and \) removed, \mathbb{R} stays
                patterns = [raw_latex]
                patterns.extend(self.math_shortcuts.get(raw_latex, []))
                patterns.append(raw_latex.replace("{", "").replace("}", ""))

                for pat in patterns:
                    if len(pat) < 2:
                        continue
                    idx = self._find_text(content, pat, _is_forbidden)
                    if idx >= 0:
                        insert_pos = idx
                        break

                if insert_pos >= 0:
                    cmd = self._build_cmd(entry)
                else:
                    # 尝试文本别名
                    for alt in self.aliases.get(raw_latex, []):
                        idx = self._find_text(content, alt, _is_forbidden)
                        if idx >= 0:
                            insert_pos = idx
                            cmd = self._build_cmd(entry)
                            break

            elif entry.get("level") == 1:
                # ── 普通 L1 条目 ──
                search = strip_latex(term)
                if len(search) < 2:
                    continue
                if any(c in search for c in "_^@!|\""):
                    continue

                insert_pos = self._find_text(content, search, _is_forbidden)

                # 尝试别名
                if insert_pos < 0:
                    for alt in self.aliases.get(term, []) + self.aliases.get(search, []):
                        insert_pos = self._find_text(content, alt, _is_forbidden)
                        if insert_pos >= 0:
                            break

                if insert_pos >= 0:
                    cmd = self._build_cmd(entry)

            elif entry.get("level") == 2:
                # ── L2 条目 ──
                child: str = entry.get("child") or entry.get("term") or ""
                search = strip_latex(child)
                if len(search) >= 2:
                    insert_pos = self._find_text(content, search, _is_forbidden)
                    if insert_pos >= 0:
                        cmd = self._build_cmd(entry)

            if insert_pos >= 0 and cmd:
                ops.append({"pos": insert_pos, "cmd": cmd, "entry": entry})

        # 去重：按位置排序，移除重叠（保留长词）
        ops.sort(key=lambda o: o["pos"])
        deduped: List[Operation] = []
        for op in ops:
            if not deduped:
                deduped.append(op)
                continue
            last = deduped[-1]
            last_end = last["pos"] + max(
                len(strip_latex(last["entry"].get("term", ""))), 2
            )
            if op["pos"] < last_end:
                continue  # 重叠，跳过
            deduped.append(op)

        # 从尾到头排序（安全插入）
        deduped.sort(key=lambda o: o["pos"], reverse=True)
        return deduped

    def find_insertions_fast(
        self, content: str, entries: List[Entry],
        progress: bool = False,
    ) -> List[Operation]:
        """快速搜索：使用 Aho-Corasick 自动机单次扫描全文本。

        适用于词条 > 1000 且文本 > 500KB 的大规模索引。
        """
        if len(entries) < 1000 or len(content) < 500_000:
            return self.find_insertions(content, entries, progress=progress)

        logger.info("快速模式：Aho-Corasick 自动机 (%d 词条)", len(entries))

        # 预计算禁区
        no_go = (
            find_math_ranges(content)
            + find_comment_ranges(content)
            + find_verbatim_ranges(content)
        )
        no_go.sort()

        def _is_forbidden(pos: int) -> bool:
            for s, e in no_go:
                if s <= pos < e:
                    return True
            return False

        # 构建自动机
        matcher = PatternMatcher()
        entry_map: Dict[str, List[Entry]] = {}
        sorted_entries = sorted(
            entries, key=lambda e: len(strip_latex(e.get("term", ""))), reverse=True
        )

        for entry in sorted_entries:
            term = entry.get("term", "")
            if not term:
                continue
            search_text = strip_latex(term)
            if len(search_text) < 2:
                continue
            if entry.get("sort_key"):
                # Math: use strip_latex to remove \( \) wrappers
                raw = strip_latex(term)
                matcher.add(raw, f"MATH:{term}")
                entry_map[f"MATH:{term}"] = [entry]
            elif entry.get("level") == 2:
                child: str = entry.get("child") or term
                st = strip_latex(child)
                if len(st) >= 2:
                    key = f"L2:{st}"
                    matcher.add(st, key)
                    if key not in entry_map:
                        entry_map[key] = []
                    entry_map[key].append(entry)
            else:
                key = f"L1:{search_text}"
                if key not in entry_map:
                    matcher.add(search_text, key)
                    entry_map[key] = [entry]
                else:
                    entry_map[key].append(entry)

        matcher.finish()

        # 单次扫描：每个条目只取首次出现
        ops: List[Operation] = []
        seen_keys: Set[str] = set()

        for pos, key, length in matcher.search(content):
            if key in seen_keys:
                continue  # 每个条目只取第一次出现
            if _is_forbidden(pos):
                continue
            if is_inside_command_arg(content, pos):
                continue
            if is_inside_index(content, pos):
                continue

            for entry in entry_map.get(key, []):
                cmd = self._build_cmd(entry)
                if cmd:
                    ops.append({"pos": pos, "cmd": cmd, "entry": entry})
                    seen_keys.add(key)
                    break

        # 去重+排序
        ops.sort(key=lambda o: o["pos"])
        deduped: List[Operation] = []
        for op in ops:
            if not deduped:
                deduped.append(op)
                continue
            last = deduped[-1]
            last_end = last["pos"] + max(
                len(strip_latex(last["entry"].get("term", ""))), 2
            )
            if op["pos"] < last_end:
                continue
            deduped.append(op)

        deduped.sort(key=lambda o: o["pos"], reverse=True)
        logger.info("快速模式完成：%d 次插入", len(deduped))
        return deduped

    def apply(self, content: str, operations: List[Operation]) -> str:
        """将操作列表应用到文本，返回修改后的文本。

        从尾到头插入，保证前面的位置不变。
        超大文件自动使用缓冲写入。
        """
        if len(content) > 10 * 1024 * 1024:  # > 10MB
            logger.info("大文件模式：使用缓冲写入")
        for op in operations:
            pos = op["pos"]
            cmd = op["cmd"]
            content = content[:pos] + cmd + content[pos:]
        return content

    @staticmethod
    def process_large_file(
        path: str,
        entries: List[Entry],
        config: Dict[str, Any],
        chunk_size: int = 1024 * 1024,  # 1MB chunks
    ) -> int:
        """流式处理超大文件，避免内存溢出。

        Args:
            path: .tex 文件路径
            entries: 索引条目列表
            config: 配置字典
            chunk_size: 每块大小（字节）

        Returns:
            插入的索引命令数量
        """
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # 对于超大文件，限制 entries 数量
        if len(content) > 50 * 1024 * 1024:  # > 50MB
            logger.warning(
                "文件超过 50MB (%d 字节)，仅处理前 10000 个条目",
                len(content),
            )
            entries = entries[:10000]

        engine = IndexEngine(config)
        ops = engine.find_insertions(content, entries)

        if ops:
            new_content = engine.apply(content, ops)
            # 原子写入
            import os
            import tempfile

            dirname = os.path.dirname(path) or "."
            fd, tmp = tempfile.mkstemp(dir=dirname, suffix=".tex")
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    f.write(new_content)
                os.replace(tmp, path)
            except Exception:
                os.unlink(tmp)
                raise

        return len(ops)

    # ── 内部方法 ─────────────────────────────────────────

    def _find_text(
        self,
        content: str,
        search: str,
        is_forbidden: Callable[[int], bool],
    ) -> int:
        """在 content 中查找 search 的纯文本出现位置（跳过禁区）。"""
        if len(search) < 2:
            return -1
        lower_content = content.lower()
        lower_search = search.lower()
        idx = 0
        while idx < len(lower_content):
            idx = lower_content.find(lower_search, idx)
            if idx < 0:
                return -1
            if (
                not is_forbidden(idx)
                and not is_inside_command_arg(content, idx)
                and not is_inside_index(content, idx)
            ):
                return idx
            idx += len(search)
        return -1

    @staticmethod
    def _sanitize_display(text: str) -> str:
        r"""清理 display/sort 参数中的 fragile 命令。

        makeindex 无法处理 \left, \right 和 \(...\)（后者被展开为底层原语）。
        \left/\right 直接移除；\(/\) 替换为 $ 保持数学模式。
        """
        for frag in (chr(92)+"left", chr(92)+"right", chr(92)+"lbrack", chr(92)+"rbrack"):
            text = text.replace(frag, "")
        text = text.replace(chr(92)+"(", "$").replace(chr(92)+")", "$")
        return text

    def _build_cmd(self, entry: Entry) -> str:
        """根据模板构建索引命令字符串。"""
        t = self.templates.get(
            "l2" if entry.get("level") == 2
            else ("l1Math" if entry.get("sort_key") else "l1"),
            self.templates.get("l1", "\\index{${key}}"),
        )
        key_sanitized = self._sanitize_display(
            escape_index_term(entry.get("term") or "", self.index_processor)
        )
        key_cap = key_sanitized[:1].upper() + key_sanitized[1:] if key_sanitized else key_sanitized
        return (
            t.replace("${key_lower}", key_sanitized.lower())
            .replace("${key_cap}", key_cap)
            .replace("${key}", key_sanitized)
            .replace("${display}", self._sanitize_display(
                entry.get("display") or entry.get("term") or ""
            ))
            .replace("${sort}", self._sanitize_display(
                entry.get("sort_key") or ""
            ))
            .replace("${parent}", entry.get("parent") or "")
            .replace("${child}", entry.get("child") or entry.get("term") or "")
        )
