# Munkres Topology 复刻项目

James R. Munkres *Topology* (2nd Edition) 的 LaTeX 复刻，编译后 **607 页**，含全书 14 章正文、前言、版权页及索引。

## 编译

```bash
make          # 完整编译（xelatex → biber → makeindex → xelatex ×2）
make index    # 仅重建索引
make quick    # 单次快速编译（语法检查）
make clean    # 清理中间文件
```

需要 TeX Live 2025+（XeLaTeX）和 Python 3.10+。

## 文件结构

```
├── chapters/                   # 14 章正文 + 前言/版权
├── images/                     # 插图（214 张 PNG）
├── ocr/                        # OCR 提取源文件（校对参考）
├── fonts/                      # 字体文件（XeTeX）
├── TopologyBook.sty            # 样式文件
├── Topology_by_Munkres.tex     # 主文件
├── Topology_by_Munkres.ist     # makeindex 样式
├── Biblography.bib             # 参考文献
└── Makefile                    # 编译脚本
```

## 插图

使用统一命令 `\munkresfig`（定义于 `TopologyBook.sty`）：

```latex
\munkresfig[width]{filename}[Figure label]
% 宽度默认 0.8\textwidth，标签可省略
```

