# Munkres Topology 复刻项目

James R. Munkres *Topology* (2nd Edition) 的 LaTeX 复刻，编译后 **609 页**，含全书 14 章正文、前言、版权页、参考文献及索引，共 **220 张插图**。

## 编译

```bash
make          # 完整编译（latexmk 自动收敛 + 自动 biber/makeindex）
make index    # 仅重建索引
make quick    # 单次快速编译（语法检查/调试）
make clean    # 清理中间文件
```

- 使用 **XeLaTeX**，需要 TeX Live 2025+；Python 3.10+。
- **`make` = latexmk**（`latexmk -pdf -xelatex --shell-escape`）：自动重复编译到收敛，并自动跑 `biber`/`makeindex`，确保 hyperref `/PageLabels` 分界与书印页码一致。`make quick`/`make bib` 为低遍数，仅调试用。

## 文件结构

```
├── chapters/                   # 14 章正文 + 前言/版权
├── images/                     # 插图（220 张 PNG）
├── fonts/                      # 字体文件（XeTeX）
├── OCR_files/                  # 原始扫描 pdf 及 OCR/索引中间产物
├── TopologyBook.sty            # 样式文件
├── Topology_by_Munkres.tex     # 主文件
├── Topology_by_Munkres.ist     # makeindex 样式
├── Bibliography.bib            # 参考文献（25 条）
└── Makefile                    # 编译脚本
```

## 现状

- 14 章正文 + 前言；609 页；220 张 PNG 插图；参考文献 25 条。
- 目录 TOC 已与原书对齐；`/PageLabels` 经 latexmk 收敛，阅读器页码与书印一致。
