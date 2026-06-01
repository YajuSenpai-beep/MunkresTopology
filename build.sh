#!/bin/bash
# ========================================
#  Munkres Topology 编译脚本 (Linux/macOS/WSL)
#  用法: bash build.sh
# ========================================

echo "[1/4] xelatex (pass 1)..."
xelatex -interaction=nonstopmode Topology_by_Munkres.tex > /dev/null 2>&1

echo "[2/4] makeindex + fix..."
makeindex -s Topology_by_Munkres.ist Topology_by_Munkres.idx > /dev/null 2>&1
python latex-index-tool/_fix_ind.py

echo "[3/4] xelatex (pass 2)..."
xelatex -interaction=nonstopmode Topology_by_Munkres.tex > /dev/null 2>&1

echo "[4/4] xelatex (pass 3)..."
xelatex -interaction=nonstopmode Topology_by_Munkres.tex > /dev/null 2>&1

echo ""
echo "========================================"
echo "Build complete: Topology_by_Munkres.pdf"
echo "========================================"
