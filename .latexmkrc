# latexmk 配置文件 — Munkres Topology
# VSCode + LaTeX Workshop: Ctrl+Alt+B 一键编译

$pdf_mode = 5;
$xelatex = "xelatex -interaction=nonstopmode %O %S";

# makeindex 通过 Python 包装脚本：makeindex + _fix_ind.py + _fix_bn.py
# latexmk 自动把 -o output.ind input.idx 追加到命令后面
$makeindex = 'python latex-index-tool/_makeindex.py';

$clean_ext = "aux bbl blg log out ilg ind idx synctex.gz fls fdb_latexmk";
