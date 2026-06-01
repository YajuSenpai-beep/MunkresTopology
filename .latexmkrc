# latexmk 配置文件 — Munkres Topology
# VSCode + LaTeX Workshop: Ctrl+Alt+B 一键编译

$pdf_mode = 5;
$xelatex = "xelatex -interaction=nonstopmode %O %S";

# makeindex 使用自定义 .ist，然后在 .ind 上运行修复
$makeindex = 'makeindex -s Topology_by_Munkres.ist %O -o %D %S && python latex-index-tool/_fix_ind.py';

$clean_ext = "aux bbl blg log out ilg ind idx synctex.gz fls fdb_latexmk";
