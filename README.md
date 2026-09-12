# Munkres Topology 复刻项目

James R. Munkres *Topology* (2nd Edition) 的 LaTeX 复刻。产出两个 PDF：

- **`Topology_by_Munkres.pdf`** —— 内文，**596 页**（全书 14 章正文、前言、版权页、参考文献及索引，共 **220 张插图**，全页统一 21×29.7cm）
- **`Cover.pdf`** —— 封面，**单页 45×29.7cm 跨页**（封底 21cm │ 书脊 3cm │ 封面 21cm）

> 封面与内文**分开编译**：合成一个 PDF 时阅读器会按最宽页（45cm）缩放，导致 21cm 的正文页看起来偏左；且印刷时封面本就单独出片。

## 编译

```bash
make          # 完整编译（内文 + 封面；latexmk 自动收敛 + 自动 biber/makeindex）
make cover    # 仅编译封面（Cover.pdf；TikZ overlay 需两趟定坐标）
make index    # 仅重建索引
make quick    # 单次快速编译（语法检查/调试）
make clean    # 清理中间文件
```

- 使用 **XeLaTeX**，需要 TeX Live 2025+；Python 3.10+。
- **`make` = latexmk**（`latexmk -pdf -xelatex --shell-escape`）：自动重复编译到收敛，并自动跑 `biber`/`makeindex`，确保 hyperref `/PageLabels` 分界与书印页码一致。`make quick`/`make bib` 为低遍数，仅调试用。

## 文件结构

```
├── chapters/                   # 14 章正文 + 前言/版权 + cover2.tex（封面/书脊/封底合版）
├── images/                     # 插图（220 张 PNG + ISBN 条码 svg/pdf）
├── fonts/                      # 字体文件（XeTeX）
├── TopologyBook.sty            # 样式文件（内文）
├── Topology_by_Munkres.tex     # 主文件（内文）
├── Cover.tex                   # 封面主文件（独立编译）
├── Topology_by_Munkres.ist     # makeindex 样式
├── Bibliography.bib            # 参考文献（25 条）
└── Makefile                    # 编译脚本
```

> 注：原始扫描 PDF 及 OCR/索引中间产物已 `.gitignore`（`OCR_files/`），存放于本仓库外
> `..\论文素材\3.Munkres原始扫描文本 (Doc2X)\`，不以目录形式出现在仓库内。

## 现状

- 14 章正文 + 前言；**596 页**（内文）+ 封面跨页；220 张 PNG 插图；参考文献 25 条。
- 目录 TOC 已与原书对齐；`/PageLabels` 经 latexmk 收敛，阅读器页码与书印一致。
- 索引已进书（`194` 条 `\idx`，书末含 Index 页）；交叉引用 **527** 处 `\label`。
- 左右边距 1.55cm（对齐原书版心占页宽 85% 的实测比例）。
