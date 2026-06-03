# Ch1 修复记录 — 2026.06.03

从 aef86b3 恢复后，对 Chapter_1_Set_Theory_and_Logic.tex 的全部修复。

## 背景

14 个章节从 `git commit aef86b3`（Ch.1 23th）恢复，该版本已包含 `\index{}` 命令、LaTeX 引号、centeredblock 包裹、习题 enumerate 格式化。但存在两类问题：

1. **OCR 标点遗留**：`aef86b3` 中尚未修复的拼写/字体/括号错误
2. **`\index{}` 替换正文关键词**：索引转换过程中，`\index{KEY}` 命令替换了正文中的关键词，导致 PDF 渲染时这些词消失（LaTeX 的 `\index{}` 不产生可见文本）

## 一、OCR 标点修复（7 处）

| # | 行号 | 问题类型 | 原文 | 修复 |
|---|------|------|------|------|
| 1 | 422 | 数学字体 | `\mathbf{C} \times \mathbf{D}` | `C \times D` |
| 2 | 951 | 括号不匹配 | `1\rbrack` | `1\}` |
| 3 | 1043 | 缺空格 | `that1is` | `that 1 is` |
| 4 | 1049 | 数学字体 + 罗马数字 | `(2) ... {Z}_{+}` | `(II) ... {\mathbb{Z}}_{+}` |
| 5 | 1054 | 缺空格 | `between1and` | `between 1 and` |
| 6 | 1656 | 冒号 OCR | `g \circ f.{\mathbb{Z}}_{+}` | `g \circ f : {\mathbb{Z}}_{+}` |
| 7 | 1838 | 冒号 OCR | `f.\{1,\ldots,n\}` | `f : \{1,\ldots,n\}` |

（第 8 处 `f.\{1,\ldots,m\}` 于 L1927 同批修复）

## 二、`\index{}` 正文关键词还原（~33 处）

**问题根因**：`\idx` → `\index` 转换过程中，`\index{KEY}` 命令替换了原本的可见关键词，而非伴随它。LaTeX 中 `\index{...}` 仅向索引写入条目，不产生任何可见输出。

**修复模式**：`\index{KEY}PUNCT` → `\index{KEY}visible_keywordPUNCT`

### 已还原的关键词清单

| 行号 | `\index` 键 | 补回的可见文本 |
|------|-------------|---------------|
| 6 | `index set@Index set` | `index set` |
| 46 | `Integers` | `integers` |
| 80 | `Empty set` | `empty set` |
| 126 | `Vacuously true` | `vacuously true` |
| 131 | `Contrapositive` | `contrapositive` |
| 131 | `Converse` | `converse` |
| 215 | `Difference of two sets` | `difference of two sets` |
| 255 | `demorgan's laws@DeMorgan's laws` | `DeMorgan's laws` |
| 310 | `Ordered pair` | `ordered pair` |
| 536 | `One-to-one correspondence` | `one-to-one correspondence` |
| 571 | `Counterimage` | `counterimage` |
| 571 | `Inverse image` | `inverse image` |
| 648 | `Equivalence relation` | `equivalence relations` |
| 648 | `Order relation` | `order relations` |
| 762 | `Simple order` | `simple order` |
| 762 | `Linear order` | `linear order` |
| 864 | `Positive integers` | `positive integers` |
| 882 | `Supremum` | `supremum` |
| 884 | `Greatest lower bound` | `greatest lower bound` |
| 884 | `Infimum` | `infimum` |
| 1028 | `Ordered field` | `ordered field` |
| 1030 | `Linear continuum` | `linear continuum` |
| 1049 | `principle of induction@Principle of induction` | `Principle of induction` |
| 1050 | `Rational number` | `rational numbers` |
| 1149 | `Inductive definition` | `inductive definition` |
| 1185 | `Index set` | `index set` |
| 1185 | `Family of sets` | `family of sets` |
| 1250 | `Infinite sequence` | `infinite sequence` |
| 1267 | `Euclidean space` | `euclidean space` |
| 1305 | `finite set@Finite Set` | `Finite sets` |
| 1305 | `Infinite set` | `infinite sets` |
| 1305 | `Countable set` | `countable sets` |
| 1305 | `Uncountable set` | `uncountable sets` |
| 1762 | `Eventually zero` | `eventually zero` |
| 1771 | `schroeder-bernstein theorem@Schroeder-Bernstein theorem` | `Schroeder-Bernstein theorem` |
| 1966 | `Axiom of choice` | `axiom of choice` |
| 2145 | `Continuum hypothesis` | `continuum hypothesis` |
| 2322 | `Transfinite induction` | `transfinite induction` |
| 2325 | `Disjoint sets` | `disjoint sets` |
| 2348 | `Maximum principle` | `maximum principle` |
| 2407 | `zorn's lemma@Zorn's Lemma` | `Zorn's lemma` |
| 2440 | `hausdorff maximum principle@Hausdorff maximum principle` | `Hausdorff maximum principle` |

## 三、定理名/环境名隐藏修复（2 处）

| 行号 | 原文 | 修复 |
|------|------|------|
| 1074 | `\begin{theorem}[\index{strong induction principle@Strong induction principle}]` | `\begin{theorem}[\index{strong induction principle@Strong induction principle}Strong induction principle]` |
| 2049 | `\begin{lemma}[Existence of a \index{Choice function}]` | `\begin{lemma}[Existence of a \index{Choice function}choice function]` |

## 四、损坏命令修复（1 处）

| 行号 | 原文 | 问题 | 修复 |
|------|------|------|------|
| 6 | `\\index{index set@Index set}.` | `\\` 被解释为 LaTeX 换行 + 字面量 `index{...}` | `\index{index set@Index set}index set.` |

## 修复统计

| 类别 | 数量 |
|------|------|
| OCR 标点 | 8 |
| `\index{}` 吞词还原 | ~33 |
| 定理名隐藏 | 2 |
| 损坏命令 | 1 |
| **合计** | **~44** |

## 编译结果

xelatex ×3 通过，0 错误，597 页 PDF。
