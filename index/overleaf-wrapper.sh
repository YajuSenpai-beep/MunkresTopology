#!/usr/bin/env bash
# Overleaf 兼容包装脚本
# 在 Overleaf 编译前自动运行索引插入
#
# 用法 (在 Overleaf 项目中):
#   1. 将此文件放在项目根目录
#   2. 在 Overleaf 设置中将编译器改为 "latexmk"
#   3. 编辑 .latexmkrc 添加:
#      $pdflatex = "bash overleaf-wrapper.sh xelatex %O %S";
#
# Overleaf 限制:
#   - 文件系统只读 (除输出目录)
#   - 无 pip 安装权限
#   - 需使用项目内的 Python 包

set -euo pipefail

COMPILER="${1:-pdflatex}"
shift || true

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INDEX_DIR="$SCRIPT_DIR/index"

# 检查 Python
PYTHON=""
for cmd in python3 python; do
    if command -v $cmd &>/dev/null; then
        PYTHON=$cmd
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo "[overleaf-wrapper] 跳过索引插入 (无 Python)" >&2
    exec $COMPILER "$@"
fi

# 检查索引工具是否可用
if [ ! -d "$INDEX_DIR/latex_index" ]; then
    echo "[overleaf-wrapper] 跳过索引插入 (未找到 latex_index/)" >&2
    exec $COMPILER "$@"
fi

# 在编译前插入索引 (dry-run 模式 — Overleaf 文件系统只读)
echo "[overleaf-wrapper] 扫描索引条目..."
cd "$INDEX_DIR"
$PYTHON -m latex_index.cli insert \
    --config config/default.yaml \
    --chapter 1 \
    --dry-run 2>&1 || true

# 执行实际编译
echo "[overleaf-wrapper] 开始编译..."
exec $COMPILER "$@"
