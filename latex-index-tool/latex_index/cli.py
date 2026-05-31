"""命令行入口 — LaTeX 索引插入工具。

Usage:
    python -m index.py.cli insert --config config/default.yaml --chapter 1
    python -m index.py.cli insert --chapter 1 --dry-run
    python -m index.py.cli parse index.txt --output entries.json
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import tempfile
from typing import Any, Dict, List

from .config import load_config
from .engine import IndexEngine
from .latexmk import (
    clean_backups,
    create_backup,
    generate_latexmkrc,
    list_backups,
    rollback_file,
)
from .parser import parse_index_file
from .project import (
    preserve_line_endings,
    resolve_tex_project,
)
from .reporter import generate_report
from .scanner import generate_entry_report
from .tools_cli import register_tools_parser
from .tui import HAS_RICH, interactive_select
from .xindy import generate_xdy, list_supported_languages

logger = logging.getLogger("index_tool")


def setup_logging(level: str = "INFO", log_file: str = "index_tool.log") -> None:
    """配置日志：控制台 + 文件。"""
    root = logging.getLogger("index_tool")
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    root.handlers.clear()

    fmt = logging.Formatter(
        "[%(asctime)s] %(levelname)-7s %(message)s", datefmt="%H:%M:%S"
    )

    # 控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    root.addHandler(ch)

    # 文件（带轮转：最多 5 个文件，每个 10MB）
    try:
        from logging.handlers import RotatingFileHandler
        fh: logging.Handler = RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=5,
            encoding="utf-8",
        )
    except ImportError:
        fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    root.addHandler(fh)


def _lock_file(f: Any) -> None:
    """获取文件独占锁（跨平台）。"""
    if sys.platform == "win32":
        import msvcrt
        msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)
    else:
        import fcntl
        fcntl.flock(f, fcntl.LOCK_EX)


def _validate_path(path: str, base_dir: str = ".") -> str:
    """验证路径安全性，防止路径遍历攻击。

    仅在配置了非默认 base_dir 时生效。
    如果路径不安全，抛出 ValueError。
    """
    if base_dir == "." or os.path.isabs(path):
        return path  # 绝对路径或默认 CWD，信任用户
    real_base = os.path.realpath(base_dir)
    real_path = os.path.realpath(os.path.join(real_base, path))
    common = os.path.commonpath([real_base, real_path])
    if common != real_base:
        raise ValueError(f"路径遍历拒绝: {path} (解析后: {real_path})")
    return real_path


def atomic_write(path: str, content: str) -> None:
    """原子写入：临时文件 + 文件锁 + 原子替换。自动清理旧备份。"""
    dirname = os.path.dirname(path) or "."
    fd, tmp = tempfile.mkstemp(dir=dirname, suffix=".tex")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            _lock_file(f)
            f.write(content)
        os.replace(tmp, path)
    except Exception:
        os.unlink(tmp)
        raise

    # 清理旧备份（保留 5 个）
    try:
        from .latexmk import clean_backups
        clean_backups(path, keep=5)
    except Exception:
        pass


def cmd_insert(args: argparse.Namespace) -> int:
    """插入索引命令。"""
    config = load_config(args.config)
    setup_logging(
        config.get("log_level", "INFO"),
        config.get("log_file", "index_tool.log"),
    )

    # 加载条目
    entry_file = args.entries
    if not entry_file:
        ch = str(args.chapter).zfill(2)
        entry_file = f"index/data/ch{ch}_entries.json"

    if not os.path.exists(entry_file):
        logger.error("条目文件不存在: %s", entry_file)
        return 1

    try:
        with open(entry_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        entries: List[Dict[str, Any]] = data if isinstance(data, list) else data.get("entries", [])
    except Exception as e:
        logger.error("条目文件读取失败: %s", e)
        return 1

    if args.l1_only:
        entries = [e for e in entries if e.get("level") == 1]

    logger.info("已加载 %d 个条目", len(entries))

    # 确定 tex 内容来源
    content: str = ""
    tex_path: str = ""
    sub_files: List[str] = []

    if args.main:
        # 多文件项目模式
        logger.info("多文件模式，主文件: %s", args.main)
        content, sub_files, line_map = resolve_tex_project(args.main)
        tex_path = args.main
        logger.info("解析完成: %d 个子文件", len(sub_files))
    else:
        # 单文件模式
        source_dir = config.get("chapter_source_dir", "chapters")
        pattern = config.get("file_pattern", "Chapter_${num}_*.tex")
        prefix = pattern.replace("${num}", str(args.chapter)).replace("_*.tex", "_")

        tex_files = [
            f for f in os.listdir(source_dir)
            if f.startswith(prefix) and f.endswith(".tex")
        ]
        if not tex_files:
            logger.error("在 %s 中未找到匹配 %s 的文件", source_dir, prefix)
            return 1

        tex_path = os.path.join(source_dir, tex_files[0])
        try:
            with open(tex_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            logger.error("文件读取失败: %s", e)
            return 1

    logger.info("[%s] 处理中: %d 字符", os.path.basename(tex_path), len(content))

    # 查找插入位置
    engine = IndexEngine(config)

    # 自动选择快速模式（大词条集 + 大文本）
    use_fast = args.fast or (len(entries) > 1000 and len(content) > 500_000)
    show_progress = getattr(args, "progress", False)
    if use_fast:
        ops = engine.find_insertions_fast(content, entries, progress=show_progress)
    else:
        ops = engine.find_insertions(content, entries, progress=show_progress)

    if args.dry_run or args.interactive:
        n_total = len(ops)
        logger.info("[%s] 将插入 %d 条索引（共 %d 条）",
                    "DRY-RUN" if args.dry_run else "INTERACTIVE", n_total, len(entries))

        if args.dry_run:
            for i, op in enumerate(ops):
                pos = op["pos"]
                ctx = content[max(0, pos - 20):pos + 40].replace("\n", " ")
                line_num = content[:pos].count("\n") + 1
                term = op["entry"].get("term", "?")
                logger.info("  [%d/%d] L%d: %s", i + 1, n_total, line_num, term)
                logger.info("    上下文: ...%s...", ctx.strip())
                logger.info("    命令: %s", op["cmd"])
            return 0

        # 交互确认（优先使用 Rich TUI）
        use_tui = getattr(args, "tui", False) or HAS_RICH
        if use_tui and HAS_RICH:
            logger.info("使用 Rich TUI 交互界面")
        accepted: List[Dict[str, Any]] = interactive_select(
            ops, content, use_rich=use_tui,
        )
        if not accepted:
            logger.info("未选择任何插入")
            return 0
        ops = accepted

    # 应用修改
    new_content = engine.apply(content, ops)

    if new_content != content:
        # 自动备份（若启用）
        if getattr(args, "backup", False):
            try:
                bp = create_backup(tex_path)
                logger.info("已备份: %s", bp)
            except Exception as e:
                logger.warning("备份失败: %s", e)
        # 保留原文件换行风格
        new_content = preserve_line_endings(content, new_content)
        atomic_write(tex_path, new_content)
        logger.info("已写入 %d 条索引到 %s", len(ops), tex_path)
    else:
        logger.info("未找到任何可插入位置")

    return 0


def cmd_scan(args: argparse.Namespace) -> int:
    """扫描 .tex 文件中的已有索引条目。"""
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        logger.error("文件不存在: %s", args.input)
        return 1
    except Exception as e:
        logger.error("文件读取失败: %s", e)
        return 1

    report = generate_entry_report(content)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report + "\n")
        logger.info("报告已写入: %s", args.output)
    else:
        print(report)

    return 0


def cmd_parse(args: argparse.Namespace) -> int:
    """解析索引文本文件。"""
    try:
        result = parse_index_file(args.input, args.format or "indented")
    except FileNotFoundError:
        logger.error("文件不存在: %s", args.input)
        return 1
    except Exception as e:
        logger.error("解析失败: %s", e)
        return 1

    json_str = json.dumps({"entries": result["entries"]}, indent=2, ensure_ascii=False)

    if args.output:
        atomic_write(args.output, json_str + "\n")
        logger.info(
            "已写入 %d 条 (L1:%d L2:%d) → %s",
            result["total"],
            result["l1_count"],
            result["l2_count"],
            args.output,
        )
    else:
        print(json_str)

    return 0


def cmd_report(args: argparse.Namespace) -> int:
    """生成索引分析报告."""
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        logger.error("文件不存在: %s", args.input)
        return 1
    except Exception as e:
        logger.error("文件读取失败: %s", e)
        return 1

    entries = None
    if args.entries:
        try:
            with open(args.entries, "r", encoding="utf-8") as f:
                data = json.load(f)
            entries = data if isinstance(data, list) else data.get("entries", [])
        except Exception as e:
            logger.warning("条目文件读取失败: %s", e)

    candidates = None
    if args.candidates:
        try:
            with open(args.candidates, "r", encoding="utf-8") as f:
                candidates = [line.strip() for line in f if line.strip()]
        except Exception as e:
            logger.warning("候选词条文件读取失败: %s", e)

    report = generate_report(content, entries=entries, candidates=candidates)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report + "\n")
        logger.info("报告已写入: %s", args.output)
    else:
        print(report)

    return 0


def cmd_setup(args: argparse.Namespace) -> int:
    """生成 latexmk 集成配置."""
    content = generate_latexmkrc(
        project_dir=args.project_dir,
        backup=not args.no_backup,
    )
    output_path = os.path.join(args.project_dir, ".latexmkrc")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content + "\n")
        logger.info("已生成: %s", output_path)
        if not args.no_backup:
            logger.info("自动备份已启用（编译前备份到 .tex.bak.*）")
        return 0
    except OSError as e:
        logger.error("写入失败: %s", e)
        return 1


def cmd_rollback(args: argparse.Namespace) -> int:
    """恢复文件备份."""
    if args.list:
        backups = list_backups(args.input)
        if backups:
            print(f"备份列表 ({len(backups)} 个):")
            for b in backups:
                print(f"  {b}")
        else:
            print("无备份文件")
        return 0

    if args.clean is not None:
        n = clean_backups(args.input, keep=args.clean)
        logger.info("已清理 %d 个旧备份", n)
        return 0

    restored = rollback_file(args.input)
    if restored:
        logger.info("已从 %s 恢复", restored)
        return 0
    else:
        logger.warning("未找到备份文件: %s", args.input)
        return 1


def backup_current(args: argparse.Namespace) -> str:
    """创建当前文件的备份。用作其他命令的前置步骤。"""
    return create_backup(args.input)


def cmd_xindy(args: argparse.Namespace) -> int:
    """生成 xindy 排序规则文件。"""
    if args.list_langs:
        langs = list_supported_languages()
        print("支持的语言代码:")
        for lang in langs:
            print(f"  {lang}")
        return 0

    content = generate_xdy(languages=args.languages)
    try:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content + "\n")
        logger.info("已生成 xindy 样式文件: %s (语言: %s)", args.output, args.languages)
        return 0
    except OSError as e:
        logger.error("写入失败: %s", e)
        return 1


def main() -> None:
    parser = argparse.ArgumentParser(
        description="LaTeX 索引插入工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", help="子命令")

    # insert 子命令
    p_ins = sub.add_parser("insert", help="插入索引命令到 tex 文件")
    p_ins.add_argument("--config", help="配置文件路径 (YAML/JSON)")
    p_ins.add_argument("--chapter", type=int, default=1, help="章节编号")
    p_ins.add_argument("--entries", help="条目 JSON 文件路径")
    p_ins.add_argument("--dry-run", action="store_true", help="仅显示，不修改文件")
    p_ins.add_argument("--l1-only", action="store_true", help="仅处理 L1 条目")
    p_ins.add_argument("--main", help="多文件项目主文件，自动解析 \\input/\\include")
    p_ins.add_argument(
        "--fast", action="store_true",
        help="使用 Aho-Corasick 自动机（大词条集自动启用）",
    )
    p_ins.add_argument(
        "--interactive", "-i", action="store_true",
        help="交互模式：逐条确认每个插入",
    )
    p_ins.add_argument(
        "--progress", action="store_true",
        help="显示进度条（需要安装 tqdm）",
    )
    p_ins.add_argument(
        "--tui", action="store_true",
        help="强制使用 Rich TUI 交互界面（需安装 rich）",
    )
    p_ins.add_argument(
        "--backup", action="store_true",
        help="修改前自动备份原文件",
    )
    p_ins.set_defaults(func=cmd_insert)

    # parse 子命令
    p_par = sub.add_parser("parse", help="解析索引文本文件为 JSON")
    p_par.add_argument("input", help="索引文本文件路径")
    p_par.add_argument("--format", choices=["indented", "run-in"], default="indented")
    p_par.add_argument("--output", "-o", help="输出 JSON 文件路径")
    p_par.set_defaults(func=cmd_parse)

    # scan 子命令
    p_scn = sub.add_parser("scan", help="扫描 .tex 文件中已有的 \\index/\\idx 条目")
    p_scn.add_argument("input", help=".tex 文件路径")
    p_scn.add_argument("--output", "-o", help="输出报告文件路径")
    p_scn.set_defaults(func=cmd_scan)

    # report 子命令
    p_rep = sub.add_parser("report", help="生成索引分析报告（覆盖率/缺失/重复）")
    p_rep.add_argument("input", help=".tex 文件路径")
    p_rep.add_argument("--entries", help="条目 JSON 文件（用于覆盖率分析）")
    p_rep.add_argument("--candidates", help="候选词条文件（每行一个，用于缺失检测）")
    p_rep.add_argument("--output", "-o", help="输出报告文件路径")
    p_rep.set_defaults(func=cmd_report)

    # setup 子命令
    p_setup = sub.add_parser("setup", help="生成 latexmk 集成配置")
    p_setup.add_argument("--project-dir", default=".", help="项目目录")
    p_setup.add_argument("--no-backup", action="store_true", help="禁用自动备份")
    p_setup.set_defaults(func=cmd_setup)

    # rollback 子命令
    p_rb = sub.add_parser("rollback", help="恢复文件备份")
    p_rb.add_argument("input", help=".tex 文件路径")
    p_rb.add_argument("--list", action="store_true", help="列出所有备份")
    p_rb.add_argument("--clean", type=int, metavar="KEEP", help="清理旧备份，保留最近 N 个")
    p_rb.set_defaults(func=cmd_rollback)

    # xindy 子命令
    p_xdy = sub.add_parser("xindy", help="生成 xindy 排序规则文件 (.xdy)")
    p_xdy.add_argument("--languages", nargs="+", default=["english"],
                       help="语言代码，如: english chinese-pinyin chinese-stroke")
    p_xdy.add_argument("--output", "-o", default="index_style.xdy",
                       help="输出 .xdy 文件路径")
    p_xdy.add_argument("--list-langs", action="store_true",
                       help="列出支持的语言代码")
    p_xdy.set_defaults(func=cmd_xindy)

    # tools 子命令（注册批处理工具集）
    register_tools_parser(sub)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
