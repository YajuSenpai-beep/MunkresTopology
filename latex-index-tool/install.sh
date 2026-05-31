#!/usr/bin/env bash
# latex-index-tool 一键安装脚本 (Linux / macOS / WSL)
set -euo pipefail

echo "=== latex-index-tool 安装脚本 ==="
echo ""

# 检查 Python 版本
PYTHON=""
for cmd in python3 python; do
    if command -v $cmd &>/dev/null; then
        ver=$($cmd -c "import sys; print(sys.version_info[:2])" 2>/dev/null || echo "(0,0)")
        major=$(echo "$ver" | grep -oP '\d+' | head -1)
        if [ "${major:-0}" -ge 3 ]; then
            PYTHON=$cmd
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo "错误: 未找到 Python 3.10+。请先安装 Python。"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  macOS: brew install python@3.12"
    echo "  Windows: https://www.python.org/downloads/"
    exit 1
fi

echo "检测到 Python: $($PYTHON --version)"

# 安装核心工具
echo ""
echo ">>> 安装 latex-index-tool ..."
$PYTHON -m pip install --upgrade pip -q
$PYTHON -m pip install latex-index-tool -q

# 可选组件
echo ""
echo "可选组件:"
echo "  [1] Rich TUI 界面 (推荐) — pip install latex-index-tool[tui]"
echo "  [2] 中文拼音排序 — pip install latex-index-tool[xindy]"
echo "  [3] 进度条 — pip install latex-index-tool[progress]"
echo "  [4] 全部 — pip install latex-index-tool[all]"
echo ""
read -p "安装可选组件? (1-4, 回车跳过): " choice

case "${choice:-}" in
    1) $PYTHON -m pip install "latex-index-tool[tui]" -q ;;
    2) $PYTHON -m pip install "latex-index-tool[xindy]" -q ;;
    3) $PYTHON -m pip install "latex-index-tool[progress]" -q ;;
    4) $PYTHON -m pip install "latex-index-tool[all]" -q ;;
    *) echo "跳过可选组件" ;;
esac

# 验证
echo ""
echo ">>> 验证安装 ..."
if $PYTHON -m latex_index --help &>/dev/null; then
    echo "安装成功！"
    echo ""
    echo "快速开始:"
    echo "  latex-index insert --chapter 1 --dry-run"
    echo "  latex-index --help"
else
    echo "安装后无法运行，请检查 PATH 或使用: python -m latex_index --help"
fi
