@echo off
REM ========================================
REM  Munkres Topology 编译脚本 (Windows)
REM  用法: build.bat
REM ========================================

echo [1/4] xelatex (pass 1)...
xelatex -interaction=nonstopmode Topology_by_Munkres.tex > nul 2>&1

echo [2/4] makeindex + fix...
makeindex -s Topology_by_Munkres.ist Topology_by_Munkres.idx > nul 2>&1
python latex-index-tool\_fix_ind.py

echo [3/4] xelatex (pass 2)...
xelatex -interaction=nonstopmode Topology_by_Munkres.tex > nul 2>&1

echo [4/4] xelatex (pass 3)...
xelatex -interaction=nonstopmode Topology_by_Munkres.tex > nul 2>&1

echo.
echo ========================================
echo Build complete: Topology_by_Munkres.pdf
echo ========================================
