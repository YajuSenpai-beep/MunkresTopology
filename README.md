# Munkres Topology 复刻项目

James R. Munkres *Topology* (2nd Edition) 的 LaTeX 复刻。

## 编译

```bash
# Windows
build.bat

# Linux / macOS / WSL
bash build.sh
```

编译流程：`xelatex → makeindex + fix → xelatex ×2`

需要 TeX Live 2025+ 和 Python 3.10+。

## 索引重建

修改条目数据后重建索引：

```bash
cd latex-index-tool

# 逐章插入
python -m latex_index insert --config config/default.yaml --chapter 1 --entries data/ch01_entries.json

# 后处理（idx→index + 大小写 + 排序键）
python _postfix.py

# 编译
cd .. && bash build.sh
```

## 文件结构

```
├── chapters/           # 14 章 + 前言/版权
├── images/             # 插图
├── fonts/              # 字体文件
├── original/           # 原版 PDF
├── report/             # 项目文档与报告
├── latex-index-tool/   # 索引自动插入工具
├── TopologyBook.sty    # 样式文件
├── Topology_by_Munkres.tex  # 主文件
├── Topology_by_Munkres.ist  # makeindex 样式
├── build.bat / build.sh     # 编译脚本
└── README.md
```

## 工具

| 工具 | 用途 |
|------|------|
| `build.bat` / `build.sh` | 一键编译 |
| `latex-index-tool/` | Python 索引自动插入工具 |
| `latex-index-tool/_postfix.py` | tex 后处理：`\idx`→`\index`，大小写，排序键 |
| `latex-index-tool/_fix_ind.py` | .ind 后处理：合并重复，重分配符号，首字母大写 |

## 报告

详见 [report/INDEX.md](report/INDEX.md)
