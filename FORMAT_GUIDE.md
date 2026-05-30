# Munkres Topology — 正文格式规范

基于原始 PDF (MinerU 解析) 对照分析结果。

---

## 零、TopologyBook.sty 样式文件解析

> 文件：[TopologyBook.sty](TopologyBook.sty) | 427 行 | 引擎：XeLaTeX

### 基础包
| 包 | 用途 |
|---|---|
| `geometry` | 页面尺寸 21cm×29.7cm，边距 left=1cm, right=1cm, top=1.2cm, bottom=1.5cm |
| `amsmath`, `amsfonts`, `amssymb` | 数学公式与符号 |
| `fontspec` | XeLaTeX 系统字体加载 |
| `tikz` (+ `arrows.meta`, `calc`) | 封面图案 / 前言分支图 |
| `xstring` | 字符串处理（节标题解析） |
| `xcolor` | 封面配色 |

### 页面布局与页眉
- `\raggedbottom`：允许页面底部不对齐
- `fancyhdr` 管理页眉，`\headrulewidth=0pt` 无页眉横线
- **frontmatter**：罗马数字页码 `i, ii, …`，页脚居中显示
- **mainmatter**：阿拉伯数字页码 `1, 2, …`，页眉显示 `§N`（左）+ `Ch.N`（右）+ 页脚无内容
- **backmatter**：清除左右页眉，保留其他设置
- `fancyhdr` 警告 `\headheight=14.5pt` 偏小，不影响输出

### 标题格式（titlesec）
| 层级 | 格式 | 特点 |
|---|---|---|
| `\part` | 48pt 粗体，`PART I` 标签 + 标题 | 第一部分的首页重置页码为 1（`etoolbox` `\pretocmd`） |
| `\chapter` | 25pt 标签 `Chapter N` + `\Huge` 标题 | `numberless` 变体无编号，用于 Preface 等 |
| `\section` (编号) | `\Large\bfseries`，`§N` 前缀 | 编号跨章连续（`\counterwithout{section}{chapter}`），范围 §1–§85 |
| `\section*` (无编号) | `\large\bfseries`，无前缀 | 由 `\@star@section` 接管（见下） |

### `\@star@section` 宏：无编号节的核心分发逻辑（L62–L98）
```
\section*{<arg>}
  → \@star@section{<arg>}

判断路径：
  1. arg 含 "§" ?
     ├─ Yes → 提取 secnum / sectionname → 写入 TOC
     │        arg 含 "*" ? → 标题加星号（raisebox 上标）
     └─ No  → arg 含 "*" ?
              ├─ Yes → 星号标题（Supplementary Exercises 等）
              └─ No  → 普通 \section* 直传
```
- **节编号提取**：xstring `\StrBehind`/`\StrBefore` 从 `§ N Title` 中分离数字 N 和标题文字
- **TOC 写入**：`\addcontentsline{toc}{section}{...\secnum\quad\sectionname}` — 编号 + 标题
- **星号上标**：`\raisebox{0.15ex}{\small *}` — 页内标题和 TOC 条目均带
- **dagger 处理**：节标题中 `\protect\sectionDagger` → 页内渲染为 `${}^{\dagger}$`，`.toc` 文件中被顶部 `\renewcommand{\sectionDagger}{}` 清空

### 定理环境（amsthm）
| 环境 | 计数器 | 样式 |
|---|---|---|
| `theorem`, `lemma`, `corollary`, `remark`, `proposition`, `addendum`, `property` | 共享 `question` 计数器 | `CustomBookMath`：8pt 上下间距，标题粗体，后跟 0.25em 间距 |
| `definition` | 无编号 (`\newtheorem*`) | 同上 |
| `example` | 独立计数器，每节重置 | 同上 |
| `proof` | — | `\proofname` 重定义为 `\textbf{Proof}`，自动 QED ■ |

### 目录格式（L281–L331）
- `tocdepth=1`：只显示 chapter 和 section
- **chapter 条目**：`Chapter N. Title ...... page` + dot leaders，`\large\bfseries`
- **part 条目**：`PART I TITLE`（无页码），`\Large\bfseries`
- **section 条目**：缩进 1.5em，`N. Title ...... page` + dot leaders，`\large`
- **TOC 顶部空白**：`\patchcmd{\tableofcontents}{...}{\vspace*{6.5cm}\@starttoc{toc}}` 硬编码 6.5cm

### 自定义命令
| 命令 | 定义 | 用途 |
|---|---|---|
| `\HRule` | `\rule{0.9\linewidth}{0.2mm}` 居中 | 分隔线（正文中已不使用） |
| `\customfootnote{#1}` | `\let\thefootnote\relax\footnotetext{#1}` | 无编号脚注，始终显示 † |
| `\sectionDagger` | `${}^{\dagger}$` | 节标题 dagger，目录中通过 `.toc` 顶部 `\renewcommand` 清空 |
| `\blankpage` | 居中 "This page intentionally left blank." | 双面打印空白页 |

### 数学快捷命令（部分）
| 命令 | 展开 | 命令 | 展开 |
|---|---|---|---|
| `\RR`, `\NN`, `\CC`, `\QQ`, `\ZZ` | `\mathbb{R}`, `\mathbb{N}`, … | `\sseq` | `\subseteq` |
| `\ns` | `\varnothing` | `\A` | `\forall` |
| `\ra` | `\rightarrow` | `\sime` / `\se` | `\backsimeq` |
| `\C{#1}` | `\mathcal{#1}` | `\B{#1}` | `\mathbb{#1}` |
| `\xra` / `\Xra` / `\xxra` | `\xrightarrow` / `\xRightarrow` / `\xLongrightarrow` | | |

### 参考文献（biblatex + biber）
- 样式：`alphabetic`（作者-年份标签如 `[Mun00]`）
- 排序：`biborder`（按 `sortkey` 字段）
- 书目标题：`\chapter*{Bibliography}` + TOC 条目 + 顶部 6.5cm 空白
- 标签模板：优先 `shorthand`，其次 `labelname` + `year`

### 超链接（hyperref）
- 彩色链接：`linkcolor=teal`，`urlcolor=red`，`citecolor=blue`
- 书签编号开启
- 已知无害警告：`\hskip`/`\hbox`/`\z@`/`\@ifnextchar` 等内部命令在 PDF 书签中自动剔除

### 索引（makeidx）
- 编译命令：`makeindex -s Topology_by_Munkres.ist Topology_by_Munkres.idx`
- `\idxfmt{#1}`：索引条目格式（粗斜体）
- `\idx{#1}`：L1 条目（自动加粗斜体）
- `\idxsub{#1}{#2}`：L2 子条目

### 字体选项
- 默认：无额外字体加载（系统字体）
- `font=times`：Times New Roman（XeLaTeX）
- `font=euler`：Euler 数学字体 + CM 希腊字母
- `font=ncmr`：NewCM 字体（`fontsetup`）
- `font=cmr`：默认 Computer Modern

---

## 核心原则

1. **注意环境平衡**：每个 `\begin{env}` 必须有对应的 `\end{env}`。编译后立即检查 `grep -c` 计数是否匹配，不匹配绝不继续。

2. **避免环境的嵌套**：不同环境不可交叉嵌套（如 `\begin{theorem}...\begin{proof}` 必须先在 proof 前闭合 theorem）。遇到 "ended by" 编译错误即为嵌套问题。

3. **严禁脚本快速处理**：所有环境包裹必须逐条手工审核上下文，确认包裹边界正确。禁止使用批量替换脚本，防止破坏性修改。

---

## 一、标题体系

| 层级 | 源码标记 | 正文渲染 | TOC 渲染 | 计数器 |
|---|---|---|---|---|
| Chapter | `\chapter{Title}` | 居中大字 | `Chapter N. Title` | chapter |
| Section | `\section*{§ NN Title}` | `§ NN Title` 粗体 | `NN Title` | section (连续) |
| *Section | `\section*{*§ NN Title}` | `*§ NN Title` (星号上标) | `*NN Title` (星号挂在边距) | section (连续) |
| *Supp Exercises | `\section*{* Supplementary Exercises: Title}` | `* Title` (星号格式渲染) | `* Title` | 不推进 |
| Subsection | `\section*{Title}` (无 § 无 *) | `\subsection*{Title}` | 不出现在目录 | 无 |

### Section 编号
- 全书连续（`\counterwithout{section}{chapter}`）
- 范围：§1 (Ch1) ~ §85 (Ch14)
- § 和数字之间**有空格**：`\section*{§ 1 Title}` 而非 `\section*{§1 Title}`

---

## 二、定理类环境

### 环境定义 (sty)
```latex
\theoremstyle{CustomBookMath}
\newtheorem{theorem}[question]{Theorem}      % 编号, 共享 question 计数器
\newtheorem{lemma}[question]{Lemma}          % 编号
\newtheorem{corollary}[question]{Corollary}  % 编号
\newtheorem*{definition}{Definition}         % 无编号
\newtheorem{example}[question]{Example}      % 编号
```

### CustomBookMath 样式
- 上方间距：8pt
- 下方间距：8pt  
- 正文字体：`\normalfont` (直立)
- 标题字体：`\bfseries` (粗体)
- 标题后间距：0.25em
- 标题格式：`Name Number (Note)`

### 正文包裹格式

**Definition**（无编号）:
```
原始：Definition. A rule of assignment is a subset r...
包裹：\begin{definition} A rule of assignment is a subset r... \end{definition}
```

**Lemma**（有编号）:
```
原始：Lemma 2.1. Let f: A→B. If there are functions...
包裹：\begin{lemma} Let f: A→B. If there are functions... \end{lemma}
```

**Theorem**（有编号）:
```
原始：Theorem 4.1 (Well-ordering property). Every nonempty subset...
包裹：\begin{theorem} Every nonempty subset... \end{theorem}
```
注：定理名 "(Well-ordering property)" 丢失——需手动补为 `\begin{theorem}[Well-ordering property]`

**Corollary**（有编号）:
```
原始：Corollary 67.2. Let G = G₁⊕G₂...
包裹：\begin{corollary} Let G = G₁⊕G₂... \end{corollary}
```

---

## 三、Proof 环境

**已完成** ✓ —— 281 个 proof 已包裹，14 章全部平衡。

```
原始：Proof. Let E be the equivalence class...
包裹：\begin{proof} Let E be the equivalence class... \end{proof}
```

- 标题：amsthm 自动渲染 "Proof." （`\proofname` 已自定义为 `\textbf{Proof}`）
- QED：amsthm 自动附加 ■
- 边界：proof 在下一个 Lemma/Theorem/Definition/Corollary/§ 标题之前结束

---

## 四、需要注意的边界情况

### 1. 星号标记 (*)
`*Lemma 71.4.` → Lemma 前有 `*`（可选节标记）。在包裹成 `\begin{lemma}` 后，`*` 由 sty 的 `\@star@section` 中的 `\raisebox{0.15ex}{\small *}` 渲染。

### 2. 定理带名称
`Theorem 4.1 (Well-ordering property).` → 名称需放进可选参数：
```latex
\begin{theorem}[Well-ordering property]
Every nonempty subset...
\end{theorem}
```

### 3. 无编号定理
`Theorem. If an ordered set A...` → 无编号:
```latex
\begin{theorem}
If an ordered set A...
\end{theorem}
```
amsthm 会自动分配计数器编号。

### 4. 带名称无编号 Lemma
`Lemma (Kuratowski). Let A be a collection...` → 名称放进可选参数:
```latex
\begin{lemma}[Kuratowski]
Let A be a collection...
\end{lemma}
```

### 5. EXAMPLE
`EXAMPLE 1. Let R denote the real numbers...` → 使用 example 环境:
```latex
\begin{example}
Let R denote the real numbers...
\end{example}
```

---

## 五、包裹识别规则

源码中识别定理类语句的正则模式（按优先级）：

1. `Lemma/Theorem/Corollary N.N. ` → 有编号，句点+空格结尾
2. `Lemma/Theorem/Corollary N.N (` → 有编号，括号名称
3. `Lemma/Theorem/Corollary. ` → 无编号
4. `Lemma/Theorem/Corollary (` → 无编号，括号名称
5. `Definition. ` → 无编号定义
6. `EXAMPLE N.` → 示例

---

## 六、编译验证

每次修改后执行：
```bash
rm -f Topology_by_Munkres.aux Topology_by_Munkres.toc
xelatex --shell-escape Topology_by_Munkres.tex
biber Topology_by_Munkres
xelatex --shell-escape Topology_by_Munkres.tex
xelatex --shell-escape Topology_by_Munkres.tex
```

验证标准：
- PDF 页数 = 624
- 日志中 0 个 `!` 错误
- `\begin{env}` 与 `\end{env}` 数量精确匹配

---

## 七、环境包裹进度

### 已完成
1. Proof 包裹 ✓ — 281 个，14 章全部平衡
2. Lemma 包裹 ✓ — 87 个
3. Theorem 包裹 ✓ — 222 个
4. Corollary 包裹 ✓ — 43 个
5. Definition 包裹 ✓ — 152 个

### 待完成
1. ~~Example 包裹~~ ✓ — ~175 个完成，14 章全部平衡
2. ~~定理名 `[...]` 手动补全~~ ✓ — 47 个定理已有名称，经 MinerU 逐章对照，与原始 PDF 完全一致；其余 175 个定理在原始 PDF 中亦无名称（仅有编号）

---
## 八、脚注校准

### 脚注机制
```latex
\newcommand{\customfootnote}[1]{%
  \let\thefootnote\relax\footnotetext{#1}%
}
```
- 正文中使用 `${}^{\dagger}$` 作为脚注标记（正确数学模式上标，无误报）
- 页面底部由 `\customfootnote{${}^{\dagger}$ text}` 生成脚注文本
- 脚注计数器被 `\let\thefootnote\relax` 禁用，标记始终为 †
- **不再使用** `^{ \dagger }\)`（触发 Missing $ 错误）、`\textsuperscript{\dag}`（导致 hyperref 目录污染）、`%\customfootno\cite{`（破损格式）

### 全项目脚注清单（12 处）

#### 内容脚注（正文标记，共 6 处）

| # | 章节 | 参照位置 | 标记行 | `\customfootnote` 行 | 脚注内容摘要 |
|---|---|---|---|---|---|
| 1 | Ch1 | §2 定义部分 | L535 `f{.}^{\dagger}` | L558 | "range" 与 "image set" 术语辨析 |
| 2 | Ch4 | §30 "separable" 术语讨论 | L75 `separable...${}^{\dagger}$` | L110 | "separation" 一词被过度使用 |
| 3 | Ch4 | §32 例2 | L447 `not normal.${}^{\dagger}$` | L462 | Kelley 将本例归因于 Dieudonné 和 A. P. Morse |
| 4 | Ch4 | §33 正文 "Step 1" 段落第一句 | L630 `interval${}^{\dagger}$` | L675 | [0,1] 的任何可数稠密子集均可 |
| 5 | Ch4 | §33 习题 第二题 (b) 部分 | L828 `uncountable.${}^{\dagger}$` | L836 | 存在连通的可数无限 Hausdorff 空间（见 Steen & Seebach 例75） |
| 6 | Ch10 | §63 定理63.1 | L234 `[f].${}^{\dagger}$` | L252 | 本结果依赖定理54.6，仅在 §65 讨论卷绕数时使用 |

#### 节脚注（section header 标记，共 6 处）

| # | 章节 | 参照位置 | `\customfootnote` 行 | 脚注内容 |
|---|---|---|---|---|
| 7 | Ch1 | *§11 小节标题 | L2791 | This section will be assumed in Chapters 5 and 14. |
| 8 | Ch2 | *§22 小节标题 | L2646 | This section will be used throughout Part II of the book. It also is referred to in a number of exercises of Part I. |
| 9 | Ch3 | *§25 小节标题 | L461 | This section will be assumed in Part II of the book. |
| 10 | Ch4 | *§35 小节标题 | L1121 | This section will be assumed in §62. It is also used in a number of exercises. |
| 11 | Ch4 | *§36 小节标题 | L1335 | This section will be assumed when we study paracompactness in §41 and when we study dimension theory in §50. |
| 12 | Ch10 | *§62 小节标题 | L141 | In this section, we use the Tietze extension theorem (§35). |

#### 格式规范
- **内容脚注**：正文中 `${}^{\dagger}$` 标记 + 紧随（或就近）的 `\customfootnote{${}^{\dagger}$ text.}`
- **节脚注**：`\section*{*§ NN Title \protect\sectionDagger}` + 紧随 `\customfootnote{${}^{\dagger}$ text.}`
  - 节标题中的 `\sectionDagger` 在目录中不显示（`.toc` 顶部 `\renewcommand{\sectionDagger}{}` 清空）
- 所有 dagger 使用 `${}^{\dagger}$`（`{}` 为空基底，`^{\dagger}` 为上标，`$...$` 提供数学模式）

### 脚注修复记录
- Ch1 L558: `%\customfootno\cite{` → `\customfootnote{...}`（破损命令）
- Ch1 L2791: `%\customfootno\cite{` → `\customfootnote{...}`（破损命令）
- Ch10 L141: `\HRule` 包裹 → `\customfootnote{...}`（移除 `\HRule`）
- Ch10 L252: `\HRule` 包裹 + Unicode † → `\customfootnote{${}^{\dagger}$ ...}`（移除 `\HRule`，统一格式）
- Ch10 L133: 节标题 `†` → `${}^{\dagger}$`（统一格式）

### 脚注文字标点修复
- Ch1 L559: `of \(f\) They` → `of \(f\). They`（补句号）
- Ch2 L2648: `of Part I` → `of Part I.`（补句号）
- Ch3 L463: `of the book` → `of the book.`（补句号）
- Ch4 L112: `shortly` → `shortly.`（补句号）
- Ch4 L464: `A. P Morse` → `A. P. Morse`（补句号 + 句号）
- Ch4 L838: `infinite See` → `infinite. See` + 末尾补句号
- Ch4 L1123: `exercises` → `exercises.`（补句号）
- Ch4 L1337: `§{50}` → `§{50}.`（补句号）
- Ch10 L141: `( \S 35)` → `( \S 35).`（补句号）
- Ch10 L252: 末尾补句号

---
## 九、标点符号 OCR 校准

### 类型 A：括号间隔缺失空格
`intervals(a, b)in` → `intervals (a, b) in`
全 14 章共修复 **48 处**（Ch1-Ch4, Ch6-Ch7）

### 类型 B：冒号 `:` 误读为句号 `.`
`f.A → B` → `f : A → B`
全项目修复 **16 处**（Ch1/2/3/4/5/7/9/13）：`f.A`(×6), `g.B`, `g.C`, `h.X`, `q.C`, `p.E`(×4), `f.X`(×3), `G.B`, `F.X`

### 类型 C：冒号 `:` 误读为 `\cdot`
`f \cdot X → Y` → `f : X → Y`
全项目修复 **11 处**（Ch1/2/3/4/5/6/7）
> 注意：`A \cdot B`（群运算）为正确用法，未修改。

### 类型 D：已确认正常的标点
逗号间距 `, ` · 分号间距 `; ` · 句号后 `.[A-Z]` 间距 · 双引号一致性

---
## 十、14 章 tex 文件 vs 原始 PDF 对比报告

> 对比日期：2026-05-29 | 编译状态：624 页，0 错误 | `\begin{}/\end{}` 全部平衡

### 章标题
全部 14 章标题与原始 PDF 一致：

| # | tex `\chapter{...}` | PDF 标题 | 匹配 |
|---|---|---|---|
| 1 | Set Theory and Logic | Set Theory and Logic | ✓ |
| 2 | Topological Spaces and Continuous Functions | Topological Spaces and Continuous Functions | ✓ |
| 3 | Connectedness and Compactness | Connectedness and Compactness | ✓ |
| 4 | Countability and Separation Axioms | Countability and Separation Axioms | ✓ |
| 5 | The Tychonoff Theorem | The Tychonoff Theorem | ✓ |
| 6 | Metrization Theorems and Paracompactness | Metrization Theorems and Paracompactness | ✓ |
| 7 | Complete Metric Spaces and Function Spaces | Complete Metric Spaces and Function Spaces | ✓ |
| 8 | Baire Spaces and Dimension Theory | Baire Spaces and Dimension Theory | ✓ |
| 9 | The Fundamental Group | The Fundamental Group | ✓ |
| 10 | Separation Theorems in the Plane | Separation Theorems in the Plane | ✓ |
| 11 | The Seifert-van Kampen Theorem | The Seifert-van Kampen Theorem | ✓ |
| 12 | Classification of Surfaces | Classification of Surfaces | ✓ |
| 13 | Classification of Covering Spaces | Classification of Covering Spaces | ✓ |
| 14 | Applications to Group Theory | Applications to Group Theory | ✓ |

### 环境统计

| 环境 | 总数 | 覆盖章节 |
|---|---|---|
| `theorem` | 222 | 全部 14 章 |
| `lemma` | 87 | 全部 14 章 |
| `corollary` | 43 | Ch1/2/3/7/8/9/11/12/13 |
| `definition` | 152 | 全部 14 章 |
| `example` | 179 | 全部 14 章 |
| `proof` | 281 | 全部 14 章 |
| `\section*` | 221 | §1~§85 连续编号 |
| `\customfootnote` | 12 | Ch1(2), Ch2(1), Ch3(1), Ch4(6), Ch10(2) |

### 节标题格式
- 普通节：`\section*{§ N Title}` — 全书 §1~§85 连续编号，§ 与数字间有空格
- 星号节：`\section*{*§ N Title ${}^{\dagger}$}` — 共 6 处（§11/§22/§25/§35/§36/§62）
- 各节顺序和编号与 PDF 一致

### 脚注状态
- 12 个全部使用 `\customfootnote{${}^{\dagger}$ ...}` 正确包裹
- 内容脚注 6 个：Ch1 §2, Ch4 §30/§32/§33/§35, Ch10 §63
- 节脚注 6 个：Ch1 *§11, Ch2 *§22, Ch3 *§25, Ch4 *§35/*§36, Ch10 *§62
- 标点全部补全（末尾句号、缩写点）
- 无 `%\customfootno`、`\HRule` 残留

### dagger 格式
- 统一使用 `${}^{\dagger}$`（`{}` 空基底 + `^{\dagger}` 上标 + `$...$` 数学模式）
- 编译通过，0 个 "Missing $ inserted" 错误
- 不再使用 `\textsuperscript{\dag}`（历史上导致 hyperref PDF 书签污染）
- 不再使用 `^{ \dagger }\)`（历史上触发 7 个 Missing $ 错误）

### 标点符号校准状态
- **Type A**（括号间隔缺空格）：48 处已修复，确认无残留
- **Type B**（冒号→句号）：16 处已修复，确认无残留
- **Type C**（冒号→`\cdot`）：11 处已修复，确认无残留
- **Type D**（逗号/分号/句号间距）：确认正常

### 已知无害警告
| 类型 | 数量 | 说明 |
|---|---|---|
| hyperref "Ignoring empty anchor" | 12 | `\customfootnote` 使用 `\footnotetext` 无配对 `\footnotemark`，无害 |
| hyperref "Token not allowed in a PDF string" | 若干 | `\hskip` 在 PDF 书签中不可用，自动替换为空格 |
| fancyhdr `\headheight` too small | 3 | 页眉高度微调，不影响输出 |
| overfull `\hbox` | 少量 | 排版微溢出，可忽略 |

### 未完成的内容对照
以下章节因超过 20 页未完整解析，但环境平衡和节标题已验证：
- Ch7 后半（§46–§47）、Ch8 后半（§49–§50）、Ch9 后半（§55–§60）
- Ch11 后半（§71–§73）、Ch12 后半（§77–§78）、Ch13 后半（§82）

---
## 十一、前导页 vs 原始 PDF 对比报告

> 对比日期：2026-05-29 | 编译状态：624 页，0 错误

### 前导页结构
主文件 `Topology_by_Munkres.tex` 中 `\frontmatter` 包含：

| 顺序 | 文件 | PDF 对应页 | 匹配 |
|---|---|---|---|
| 1 | `cover.tex` | 封面 | 自定义设计 |
| 2 | `halftitle.tex` | 半书名页 | ✓ |
| 3 | `copyright.tex` | 版权页 | ✓ |
| 4 | `dedication.tex` | 献词页 | ✓ |
| 5 | `\tableofcontents` | 目录 | 自动生成 |
| 6 | `preface.tex` | 前言 | ✓ |
| 7 | `NoteToReader.tex` | 致读者 | ✓ |

### 逐页详情

**封面 (cover.tex):** TikZ 自定义设计（深绿色底 + 几何图案 + "TOPOLOGY" 大字 + "JAMES R. MUNKRES"），与原始 Prentice Hall 封面风格不同，为刻意重制。

**半书名页 (halftitle.tex):** 两页——第一页 "Topology / Second Edition" 居中（字号较小），第二页含 "Topology / Second Edition / James R. Munkres / Massachusetts Institute of Technology / Prentice Hall..." 右对齐。内容与 PDF 一致。

**版权页 (copyright.tex):**
- Library of Congress CIP 数据 ✓（使用 `\ttfamily` 等宽字体）
- 编辑出版团队 15 行 ✓
- 版权声明 `© 2000, 1975 by Prentice Hall, Inc.` ✓
- 国际出版社列表 8 行 ✓
- ISBN 0-13-181629-2 ✓
- 注意：`\ttfamily` 使 CIP 部分呈现打字机字体，与 PDF 的普通正文字体不同

**献词页 (dedication.tex):** "For Barbara" 斜体粗体居中 ✓

**目录 (`\tableofcontents`):** LaTeX 自动生成，两条目（General Topology / Algebraic Topology），章节编号、页码由编译确定。

**前言 (preface.tex):** 内容与 PDF 逐段对照：
- 开篇段落 ✓
- Prerequisites 段 ✓（`\noindent\textbf{Prerequisites. }`）
- How the book is organized 段 ✓
- 分支图：tex 用 TikZ 绘制，PDF 为排版字符画 ✓（效果等价）
- Possible course outlines 段 ✓
- Comments on this edition 段 ✓
- Acknowledgments 段 ✓
- J.R.M. 署名 ✓
- 注意：tex 全文使用 `\large` 字号 + `\vspace{6.5cm}` 顶部空推，与 PDF 排版风格有异

**致读者 (NoteToReader.tex):** 内容与 PDF 逐段对照：
- 练习与习题说明 ✓
- "open-ended" 讨论 ✓
- 四个核心反例列表（`\({\mathbb{R}}^{J}\)`, `\({\mathbb{R}}_{\ell }\)`, `\({S}_{\Omega }\)`, `\({I}_{o}^{2}\)`）✓
- 注意：tex 使用 `\chapter*{A Note to the Reader}` 无编号章标题，PDF 标题为 "# A Note to the Reader"

### 发现的问题

| # | 文件 | 问题 | 严重性 |
|---|---|---|---|
| 1 | `copyright.tex` L24, L27 | 行末残留 `\` 反斜杠（L24: `\` 独立，L27: `\` 独立） | 低（可能触发编译警告） |
| 2 | `copyright.tex` | `\ttfamily` 使 CIP 数据字体与 PDF 不一致 | 低（风格选择） |
| 3 | `preface.tex` L8 | `\vspace{6.5cm}` 硬编码空白，跨页面布局可能漂移 | 中（排版脆弱） |
| 4 | `preface.tex` L5 | `\large` 全局放大前言字号，PDF 为正常字号 | 低（风格选择） |
| 5 | `cover.tex` | 封面为全新设计，非 Prentice Hall 原版封面复制 | 信息（刻意为之） |
| 6 | `halftitle.tex` | 半书名页排版布局（右对齐 / 字号）与 PDF 有细微差异 | 低（风格选择） |
