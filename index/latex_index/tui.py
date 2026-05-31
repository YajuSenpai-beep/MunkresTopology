r"""Rich TUI — 交互式索引选择界面。

需要安装 rich: pip install rich

Usage:
    from latex_index.tui import interactive_select
    selected = interactive_select(ops, content)
"""

from __future__ import annotations

from typing import Any, Dict, List

try:
    from rich.console import Console
    from rich.prompt import Confirm, Prompt
    from rich.table import Table
    HAS_RICH = True
except ImportError:
    HAS_RICH = False


def _basic_select(
    ops: List[Dict[str, Any]], content: str
) -> List[Dict[str, Any]]:
    """回退到基本行内交互模式（不依赖 rich）。"""
    accepted: List[Dict[str, Any]] = []
    for i, op in enumerate(ops):
        pos = op["pos"]
        ctx = content[max(0, pos - 20):pos + 40].replace("\n", " ")
        line_num = content[:pos].count("\n") + 1
        term = op["entry"].get("term", "?")

        print(f"\n[{i + 1}/{len(ops)}] L{line_num}: {term}")
        print(f"  上下文: ...{ctx.strip()}...")
        print(f"  命令: {op['cmd']}")

        while True:
            resp = input("  插入? [y]es/[n]o/[a]ll/[q]uit: ").lower()
            if resp in ("y", "yes", ""):
                accepted.append(op)
                break
            elif resp in ("n", "no"):
                break
            elif resp in ("a", "all"):
                accepted.append(op)
                accepted.extend(ops[i + 1:])
                return accepted
            elif resp in ("q", "quit"):
                return accepted
            else:
                print("  请输入 y/n/a/q")
    return accepted


def interactive_select(
    ops: List[Dict[str, Any]],
    content: str,
    use_rich: bool = True,
) -> List[Dict[str, Any]]:
    """交互式选择要插入的索引。

    如果安装了 rich 且 use_rich=True，提供表格界面；
    否则回退到命令行逐条确认。

    Args:
        ops: 操作列表 (from engine.find_insertions)
        content: 原始 LaTeX 文本（用于显示上下文）
        use_rich: 是否尝试使用 rich TUI

    Returns:
        用户选择的操作列表
    """
    if not ops:
        return []

    if not use_rich or not HAS_RICH:
        return _basic_select(ops, content)

    # Rich TUI: 表格预览 + 批量选择
    console = Console()
    table = Table(title="索引插入预览", show_lines=False)
    table.add_column("#", style="dim", width=4)
    table.add_column("行", style="cyan", width=5)
    table.add_column("词条", style="green")
    table.add_column("命令", style="yellow")
    table.add_column("上下文", style="dim", max_width=60)

    for i, op in enumerate(ops):
        pos = op["pos"]
        ctx = content[max(0, pos - 30):pos + 50].replace("\n", " ")
        line_num = content[:pos].count("\n") + 1
        table.add_row(
            str(i + 1),
            str(line_num),
            op["entry"].get("term", "?")[:40],
            op["cmd"][:50],
            ctx.strip()[:60],
        )

    console.print(table)
    console.print(f"\n共 {len(ops)} 条索引待插入")

    # 选择模式
    choice = Prompt.ask(
        "选择模式",
        choices=["all", "range", "select", "search", "quit"],
        default="all",
    )

    if choice == "quit":
        return []

    if choice == "all":
        if Confirm.ask(f"确认插入全部 {len(ops)} 条?"):
            return list(ops)
        return []

    if choice == "range":
        rng = Prompt.ask("输入范围 (如 1-10, 15-20)")
        try:
            accepted = []
            for part in rng.split(","):
                part = part.strip()
                if "-" in part:
                    a, b = part.split("-", 1)
                    accepted.extend(ops[int(a) - 1:int(b)])
                else:
                    accepted.append(ops[int(part) - 1])
            return accepted
        except (ValueError, IndexError):
            console.print("[red]范围格式无效[/red]")
            return []

    if choice == "select":
        indices = Prompt.ask("输入编号（空格分隔）", default="")
        try:
            idxs = [int(x) - 1 for x in indices.split()]
            return [ops[i] for i in idxs if 0 <= i < len(ops)]
        except ValueError:
            console.print("[red]编号格式无效[/red]")
            return []

    if choice == "search":
        query = Prompt.ask("搜索词条")
        return [op for op in ops if query.lower() in op["entry"].get("term", "").lower()]

    return []
