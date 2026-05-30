# Munkres Topology 复刻项目日志

**2025.01.28** — B站 BV1BpfHYcCEc 视频评论区，uid1775540330 用户评论 Munkres 拓扑学相关内容

**2025.07.05** — 提出学习拓扑学

**2025.09.17** — 开始学习 LaTeX 语法，未正式复刻教材

**2025.09.19** — 研究快速输入 LaTeX 公式和语法调整

**2025.10.01** — 思考 4 个技术问题：(1) 矢量图复刻方式 (2) TikZ 小型图示还是外部引用 (3) 国外教材出版格式与字体 (4) 目录样式自定义

**2025.10.02** — 制作封面：字体设定 — "Topology" 用 SenatorTall，"Second Edition" 用 rebar-bold-1，"JAMES R. MUNKRES" 用 TrajanPro

**2025.10.25** — 问题太多，暂时搁置

**2025.10.26** — 调研 clayden.lawaxi.net 有机化学教材项目，得到的回复是"教材格式问 GPT"

**2025.11.01** — 改变思路：先编译格式胚子，再逐步调试，最后画图。顺序定为：正文 → 图片 → 排版格式 → 参考文献与索引 → 目录与页码对齐。确定 Grammarly（英文）和火龙果写作（中文）作为校对手段

**2025.11–12** — 经济困难期间，工厂打工（12小时/日，时薪 17 元，试岗 4 天后被辞退，工资次年 1 月才发，还扣了 80 元"高等商业保险"）

**2026.02.02** — 调试页眉页脚；注意到 Bibliography 引用但未完全理解文件工作方式；参考 "From-Calculus-to-Cohomology" 项目反向工程，研究高效文件管理方式；开始思考 AI 工作流模型

**2026.02.05** — 接触微分几何，写笔记手稿，tex 文件搁置

**2026.03.16** — 项目代码调试：研究 elegantbook.cls 模板工作方式，决定先调试导言区代码；统计图片素材 214 张；尝试调试 bib 文件正文引用（失败）；开始思考索引编译问题；分析结论：工作量主要花在 AI 任务监督和 index 代码插入，担心 AI 工作上下文长度受限

**2026.03.20** — 利用 `\printbibliography[heading=none]` 初步编译出不含正文引用命令的参考文献 PDF

**2026.03.27** — 反向工程研究：Inkscape 绘制插图；Custombook.sty 是主导页面格式细节的文件模板，页眉页脚可提前设置

**2026.04.1–30** — 复刻项目搁置，学习 AI 用法并做小型笔记；初步完成拓扑学笔记（无插图）

**2026.05.06** — 统计教材里的 12 条脚注位置（具体见下方脚注校准）

**2026.05.13** — 拓扑学笔记最终稿确定（含 TikZ 插图），并印刷成册

**2026.05.18** — 页眉页脚样式调整成功（页码粗体格式等），设置在 sty 文件里

**2026.05.19** — 测试 index 局部嵌入正文；用 AI 将 index.pdf 结合 OCR 扫描件转换成 JSON 格式（按级别分 L1/L2）

**2026.05.20** — 首次编译成功自定义索引

**2026.05.21** — 反向工程研究目录格式：preface/NoteToReader 用罗马数字页码；Part I/II 特殊格式无页码无引导点；chapter 用阿拉伯数字页码；section 序数全局继承对齐，部分带星号；Supplementary Exercises 用小节样式；参考文献/索引用阿拉伯数字页码；引导点对齐沉底。改变思路：图片最后做，先处理 section 内容，再调试 subsection，逐个章节处理。尝试脚本直接嵌入正文编译索引失败，污染正文，全部用备份恢复

**2026.05.21 凌晨** — 自定义目录格式初步编译成功；参考文献用 AI 搜索和插入 `\cite{}`，sty 文件自定义 bib 编译顺序，剩余 [D]/[G-P]/[H]/[W] 条目用间接引用和 `\nocite{Dugundji1966}` 完整编译；AI 对照初始图片素材生成 Inkscape SVG 骨架

**2026.05.22** — 发现除目录星号标记外，部分正文练习也有编号前星号标记；`\part{}` 设为页面中心；`\chapter*{}` 首段缺 2 格缩进；对照前言和致读者了解星号提示，知悉原出版物用 MacroTeX 排版

**2026.05.28** — `\part{}` 内容居中；修复目录中 OCR 双编号问题；sty 文件修复 book 类默认 section 编号随章节重置；目录中添加 Supplementary Exercises；调试星号标记与目录样式兼容；section 编号设为全书连续（§1–§85）

**2026.05.29** — AI 校对和环境包裹，顺序：theorem → proof → lemma → corollary → definition → example → footnote；调试 dagger 符号不出现在目录；前导页逐页对照原始 PDF（半书名页、版权页、献词页、前言、致读者）；OCR 标点修复：Type A 括号间隔缺空格 48 处、Type B 冒号误读为句号 16 处、Type C 冒号误读为 `\cdot` 11 处

  - 环境包裹最终统计：Proof 281 个，Lemma 87 个，Theorem 222 个，Corollary 43 个，Definition 152 个，Example 179 个。14 章全部平衡。
  - 定理名手动补全：47 个定理已有名称，经 MinerU 逐章对照与原始 PDF 一致；其余 175 个定理在原始 PDF 中亦无名称
  - 脚注校准：12 处全部使用 `\customfootnote{${}^{\dagger}$ ...}` 正确包裹（内容脚注 6 处：Ch1 §2 / Ch4 §30,§32,§33,§35 / Ch10 §63；节脚注 6 处：Ch1 *§11 / Ch2 *§22 / Ch3 *§25 / Ch4 *§35,*§36 / Ch10 *§62）。修复了 `%\customfootno`、`\HRule` 残留和标点缺失（共 10 处）
  - dagger 格式统一为 `${}^{\dagger}$`（不再使用 `\textsuperscript{\dag}` 和 `^{ \dagger }\)`）
  - 14 章标题全部与原始 PDF 一致验证通过
  - 已知无害警告记录：hyperref "Ignoring empty anchor" 12 处、fancyhdr `\headheight` 偏小、overfull `\hbox` 少量
  - 编译状态：624 页，0 错误

**2026.05.30** — 尝试 index 全局插入；发现按章节插入效率高于按 26 字母分类插入（后者每次遍历全文）；自制脚本插入遇到匹配问题和文档污染问题，代价巨大（110 元 token）；脚本识别不完全精准，agent 精准匹配有 token 成本和效率问题。调查知乎上关于教材的勘误表。Anaconda 环境调试：`conda activate basic114514`（开）/ `conda deactivate`（关）

---

## 附录：TopologyBook.sty 技术配置

基于 FORMAT_GUIDE.md 零部分整理。sty 文件约 427 行，XeLaTeX 引擎。

### 基础包

| 包 | 用途 |
|---|---|
| `geometry` | 页面尺寸 21cm×29.7cm，边距 left=1cm, right=1cm, top=1.2cm, bottom=1.5cm |
| `amsmath`, `amsfonts`, `amssymb` | 数学公式与符号 |
| `fontspec` | XeLaTeX 系统字体加载 |
| `tikz` (+ `arrows.meta`, `calc`) | 封面图案、前言分支图 |
| `xstring` | 字符串处理（节标题解析） |
| `xcolor` | 封面配色 |

### 页面布局与页眉

- `\raggedbottom`：允许页面底部不对齐
- `fancyhdr` 管理页眉，`\headrulewidth=0pt` 无页眉横线
- **frontmatter**：罗马数字页码，页脚居中
- **mainmatter**：阿拉伯数字页码，页眉 `§N`（左）+ `Ch.N`（右），页脚无内容
- **backmatter**：清除左右页眉
- 已知无害：`\headheight=14.5pt` 偏小，不影响输出

### 标题格式（titlesec）

| 层级 | 格式 |
|------|------|
| `\part` | 48pt 粗体，`PART I` 标签 + 标题；Part I 首页重置页码为 1 |
| `\chapter` | 25pt 标签 `Chapter N` + `\Huge` 标题；`numberless` 变体用于 Preface 等 |
| `\section` (编号) | `\Large\bfseries`，`§N` 前缀；编号跨章连续（`\counterwithout{section}{chapter}`），§1–§85 |
| `\section*` (无编号) | `\large\bfseries`，无前缀，由 `\@star@section` 接管分发 |

### `\@star@section` 宏（无编号节的核心分发逻辑）

参数含 `§` → 提取 secnum/sectionname 写入 TOC；参数含 `*` → 星号上标（`\raisebox{0.15ex}{\small *}`）；否则 → 普通 `\section*` 直传。节标题中的 `\protect\sectionDagger` 在 `.toc` 中被 `\renewcommand{\sectionDagger}{}` 清空。

### 定理环境（amsthm）

| 环境 | 计数器 | 样式 |
|------|--------|------|
| `theorem`, `lemma`, `corollary`, `remark`, `proposition`, `addendum`, `property` | 共享 `question` 计数器 | CustomBookMath：8pt 上下间距，标题粗体，后跟 0.25em 间距 |
| `definition` | 无编号（`\newtheorem*`） | 同上 |
| `example` | 独立计数器，每节重置 | 同上 |
| `proof` | — | `\proofname` 重定义为 `\textbf{Proof}`，自动 QED ■ |

### 目录格式

- `tocdepth=1`：只显示 chapter 和 section
- chapter 条目：`Chapter N. Title ...... page` + dot leaders，`\large\bfseries`
- part 条目：`PART I TITLE`（无页码），`\Large\bfseries`
- section 条目：缩进 1.5em，`N. Title ...... page` + dot leaders，`\large`
- TOC 顶部空白：`\patchcmd{\tableofcontents}` 硬编码 6.5cm

### 自定义命令

| 命令 | 定义 | 用途 |
|------|------|------|
| `\HRule` | `\rule{0.9\linewidth}{0.2mm}` 居中 | 分隔线（正文中已不使用） |
| `\customfootnote{#1}` | `\let\thefootnote\relax\footnotetext{#1}` | 无编号脚注，始终显示 † |
| `\sectionDagger` | `${}^{\dagger}$` | 节标题 dagger，目录中清空 |
| `\blankpage` | 居中 "This page intentionally left blank." | 双面打印空白页 |

### 数学快捷命令（部分）

| 命令 | 展开 |
|------|------|
| `\RR`, `\NN`, `\CC`, `\QQ`, `\ZZ` | `\mathbb{R}`, `\mathbb{N}`, … |
| `\sseq` | `\subseteq` |
| `\ns` | `\varnothing` |
| `\C{#1}`, `\B{#1}` | `\mathcal{#1}`, `\mathbb{#1}` |
| `\xra` / `\Xra` / `\xxra` | `\xrightarrow` / `\xRightarrow` / `\xLongrightarrow` |

### 参考文献（biblatex + biber）

- 样式：`alphabetic`（作者-年份标签如 `[Mun00]`）
- 排序：`biborder`（按 `sortkey` 字段）
- 书目标题：`\chapter*{Bibliography}` + TOC 条目 + 顶部 6.5cm 空白
- 标签模板：优先 `shorthand`，其次 `labelname` + `year`

### 超链接（hyperref）

- `linkcolor=teal`，`urlcolor=red`，`citecolor=blue`
- `hyperindex=false`
- 书签编号开启

### 索引（makeidx）

- `\idx{#1}` — `\index{#1}\idxfmt{#1}`
  L1 条目，写入 .idx 并在正文渲染为粗斜体
- `\idxmath{#1}{#2}` — `\index{#1@#2}\idxfmt{#2}`
  数学符号条目，#1 排序键，#2 显示形式。显示含脆弱命令时需 `\protect`（如 `\protect\widetilde`）
- `\idxsub{#1}{#2}` — `\index{#1!#2}`
  L2 子条目，仅写入 .idx，不在正文渲染
- `\idxfmt{#1}` — `\textbf{\textsl{#1}}`
  索引条目正文字体（粗斜体）
- `\lettergroup{#1}` — 索引字母标题格式

编译命令：`makeindex -s Topology_by_Munkres.ist Topology_by_Munkres.idx`

### 字体选项

默认系统字体，支持可选参数：`font=times`（Times New Roman）、`font=euler`（Euler 数学字体 + CM 希腊字母）、`font=ncmr`（NewCM）、`font=cmr`（默认 Computer Modern）

### 标题体系

| 层级 | 源码标记 | 正文渲染 | TOC 渲染 | 计数器 |
|------|---------|---------|---------|--------|
| Chapter | `\chapter{Title}` | 居中大字 | `Chapter N. Title` | chapter |
| Section | `\section*{§ NN Title}` | `§ NN Title` 粗体 | `NN Title` | section，全书连续 |
| *Section | `\section*{*§ NN Title}` | `*§ NN Title` 星号上标 | `*NN Title` 星号挂边距 | section，全书连续 |
| *Supp Exercises | `\section*{* Supplementary Exercises: Title}` | `* Title` 星号渲染 | `* Title` | 不推进 |
| Subsection | `\section*{Title}`（无 § 无 *） | 正文字体 | 不出现 | 无 |

- Section 编号全书连续（`\counterwithout{section}{chapter}`），范围 §1–§85
- § 和数字之间有空格：`\section*{§ 1 Title}` 而非 `\section*{§1 Title}`

### 定理类环境包裹格式

环境定义见 sty 的 CustomBookMath 样式（8pt 上下间距，粗体标题，0.25em 标题后间距）。

**Definition**（无编号）：
```
原始：Definition. A rule of assignment is a subset r...
包裹：\begin{definition} A rule of assignment is a subset r... \end{definition}
```

**Lemma**（编号，共享 question 计数器）：
```
原始：Lemma 2.1. Let f: A→B. If there are functions...
包裹：\begin{lemma} Let f: A→B. If there are functions... \end{lemma}
```

**Theorem**（编号，共享 question 计数器，带名称时放可选参数）：
```
原始：Theorem 4.1 (Well-ordering property). Every nonempty subset...
包裹：\begin{theorem}[Well-ordering property] Every nonempty subset... \end{theorem}
```

**Corollary**（编号，共享 question 计数器）：
```
原始：Corollary 67.2. Let G = G₁⊕G₂...
包裹：\begin{corollary} Let G = G₁⊕G₂... \end{corollary}
```

**Example**（独立计数器，每节重置）：
```
原始：EXAMPLE 1. Let R denote the real numbers...
包裹：\begin{example} Let R denote the real numbers... \end{example}
```

**Proof**（无计数器，自动 QED ■）：
```
原始：Proof. Let E be the equivalence class...
包裹：\begin{proof} Let E be the equivalence class... \end{proof}
```

#### 边界情况

- `*Lemma 71.4.` → Lemma 前有 `*`（可选节标记），包裹后由 sty 的 `\@star@section` 渲染星号
- `Theorem.`（无编号）→ 包裹后 amsthm 自动分配计数器编号
- `Lemma (Kuratowski).`（无编号带名称）→ 名称放进可选参数：`\begin{lemma}[Kuratowski]`
- `EXAMPLE N.` → 使用 example 环境，不保留编号前缀

### 包裹识别规则

OCR 源码中识别定理类语句的正则模式（按优先级）：

1. `Lemma/Theorem/Corollary N.N. ` → 有编号，句点+空格结尾
2. `Lemma/Theorem/Corollary N.N (` → 有编号，括号名称
3. `Lemma/Theorem/Corollary. ` → 无编号
4. `Lemma/Theorem/Corollary (` → 无编号，括号名称
5. `Definition. ` → 无编号定义
6. `EXAMPLE N.` → 示例

### 编译验证

```bash
rm -f Topology_by_Munkres.aux Topology_by_Munkres.toc
xelatex --shell-escape Topology_by_Munkres.tex
biber Topology_by_Munkres
xelatex --shell-escape Topology_by_Munkres.tex
xelatex --shell-escape Topology_by_Munkres.tex
```

验证标准：PDF 页数 = 624（无索引导入时）/ 634（含索引）、日志 0 个 `!` 错误、`\begin{env}` 与 `\end{env}` 数量精确匹配

### 脚注校准

脚注使用 `\customfootnote{${}^{\dagger}$ text}` 机制，`\let\thefootnote\relax` 禁用计数器，标记始终为 †。共 12 处。

**内容脚注（6 处）**：正文中以 `${}^{\dagger}$` 标记，页面底部由 `\customfootnote` 生成。

| # | 章节 | 位置 | 摘要 |
|---|------|------|------|
| 1 | Ch1 §2 | L558 | "range" 与 "image set" 术语辨析 |
| 2 | Ch4 §30 | L110 | "separation" 一词被过度使用 |
| 3 | Ch4 §32 | L462 | Kelley 将本例归因于 Dieudonné 和 A. P. Morse |
| 4 | Ch4 §33 | L675 | [0,1] 的任何可数稠密子集均可 |
| 5 | Ch4 §33 习题 | L836 | 存在连通的可数无限 Hausdorff 空间 |
| 6 | Ch10 §63 | L252 | 本结果依赖定理 54.6，仅在 §65 讨论卷绕数时使用 |

**节脚注（6 处）**：节标题以 `\protect\sectionDagger` 标记，紧随 `\customfootnote`。

| # | 章节 | 位置 | 摘要 |
|---|------|------|------|
| 7 | Ch1 *§11 | L2791 | This section will be assumed in Chapters 5 and 14. |
| 8 | Ch2 *§22 | L2646 | This section will be used throughout Part II. |
| 9 | Ch3 *§25 | L461 | This section will be assumed in Part II. |
| 10 | Ch4 *§35 | L1121 | This section will be assumed in §62. |
| 11 | Ch4 *§36 | L1335 | This section will be assumed in §41 and §50. |
| 12 | Ch10 *§62 | L141 | In this section, we use the Tietze extension theorem. |

**修复记录**：`%\customfootno\cite{` → `\customfootnote{...}`（Ch1 两处）、`\HRule` 包裹移除（Ch10 两处）、Unicode † → `${}^{\dagger}$`（Ch10）。标点补全共 10 处（句号、缩写点）。

### 标点符号 OCR 校准

| 类型 | 模式 | 修复 | 示例 |
|------|------|------|------|
| A：括号间隔缺空格 | `intervals(a, b)in` | **48 处**（Ch1–Ch4, Ch6–Ch7） | → `intervals (a, b) in` |
| B：冒号误读为句号 | `f.A → B` | **16 处**（Ch1–Ch5, Ch7, Ch9, Ch13） | → `f : A → B` |
| C：冒号误读为 `\cdot` | `f \cdot X → Y` | **11 处**（Ch1–Ch7） | → `f : X → Y` |
| D：已确认正常 | 逗号、分号、句号间距、双引号 | — | 无需修复 |

> 注意：`A \cdot B`（群运算）为正确用法，Type C 修复中未改动。

### Ch1 引号 OCR 校准（2026.05.31）

引号问题是 OCR 转换中的系统性错误，分三类：

#### 类型 D：`,''` → `, ``（逗号 + 闭引号误读为开引号）

OCR 将 `, ``（逗号 + 左双引号）误读为 `,''`（逗号 + 右双引号），导致引号方向错误。

| # | 行号 | 原文本 | 修复 |
|---|------|--------|------|
| D-1 | 98 | `the sentence,''Every element` | `the sentence, ``Every element` |
| D-2 | 98 | `formally,''For every object` | `formally, ``For every object` |
| D-3 | 117 | `the form,''If \(P\)` | `the form, ``If \(P\)` |
| D-4 | 125 | `as saying,''If \(x \in \varnothing\)` | `as saying, ``If \(x \in \varnothing\)` |
| D-5 | 1746 | `by saying,''Let \(A\) be the set` | `by saying, ``Let \(A\) be the set` |

#### 类型 E：` `` … `` Y` → ` `` … '' Y`（引号中间被 OCR 误认为开引号）

OCR 将公式后接续文本前的闭引号 `''` 误读为开引号 ` `` `。关键特征：第二个 ` `` ` 后跟的不是新引文，而是 `means` / `can` / `is` / `and` 等接续词。

| # | 行号 | 原文本 | 修复 |
|---|------|--------|------|
| E-1 | 57 | ` `` \(P\) or \(Q\) `` means` | ` `` \(P\) or \(Q\) '' means` |
| E-2 | 66 | ` `` \(P\) or \(Q\) `` always means` | ` `` \(P\) or \(Q\) '' always means` |
| E-3 | 117 | ` `` \(x > 0\) `` (called the hypothesis` | ` `` \(x > 0\) '' (called the hypothesis` |
| E-4 | 117 | ` `` \({x}^{3} \neq 0\) `` (called the conclusion` | ` `` \({x}^{3} \neq 0\) '' (called the conclusion` |
| E-5 | 158 | ` ``not \(Q\) `` stands for` | ` ``not \(Q\) '' stands for` |
| E-6 | 160 | ` `` \(P \Rightarrow Q\) `` can fail` | ` `` \(P \Rightarrow Q\) '' can fail` |
| E-7 | 160 | ` ``not \(Q\) `` is true` | ` ``not \(Q\) '' is true` |
| E-8 | 160 | ` ``not \(P\) `` is false` | ` ``not \(P\) '' is false` |
| E-9 | 160 | ` `` not \(Q \Rightarrow\) not \(P\) `` as a proof` | ` `` not \(Q \Rightarrow\) not \(P\) '' as a proof` |
| E-10 | 478 | ` ``Let \(f\) … = {x}^{3} + 1\) `` is no longer` | ` ``Let \(f\) … = {x}^{3} + 1\) '' is no longer` |
| E-11 | 696 | ` `` \(x\) is in the relation \(D\) to \(y\) `` and` | ` `` \(x\) is in the relation \(D\) to \(y\) '' and` |
| E-12 | 696 | ` `` \(x\) is a descendant of \(y\) `` mean` | ` `` \(x\) is a descendant of \(y\) '' mean` |
| E-13 | 820 | ` ``either \(x < y\) or \(x = y\) ``; and` | ` ``either \(x < y\) or \(x = y\) ''; and` |

#### 类型 F：Unicode 智能引号 → LaTeX 引号

OCR 产生 Unicode 左双引号 `"` (U+201C) 而非 LaTeX ` `` `。

| # | 行号 | 原文本 | 修复 |
|---|------|--------|------|
| F-1 | 376 | `"If \(x < 0\)` | ` ``If \(x < 0\)` |

#### 前期已修复（直引号）

| # | 行号 | 原文本 | 修复 | 类型 |
|---|------|--------|------|------|
| — | 49 | `"or"` → ` ``or'' ` | section 标题 | 直引号 |
| — | 70 | `"If ... Then"` → ` ``If ... Then'' ` | section 标题 | 直引号 |
| — | 480 | `"range"` / `"image set''` → ` ``range'' ` / ` ``image set'' ` | 脚注 | 直引号 + 混用 |

#### 统计

| 类型 | 数量 | 说明 |
|------|------|------|
| D：`,''` → `, `` ` | 5 | 闭引号误为开引号 |
| E：` `` X `` Y` → ` `` X '' Y` | 13 | 中间闭引号误为开引号 |
| F：Unicode → LaTeX | 1 | 智能引号 |
| 直引号 | 3 | section/脚注直引号 |

**合计 22 处引号修复**。修复脚本：`index/_fix_quotes2.js`。

> 注意：以上修复针对 Ch1。其他 13 章可能存在同类问题，需后续统一处理。

### 前导页 vs 原始 PDF 对照

| 顺序 | 文件 | 内容 | 匹配 |
|------|------|------|------|
| 1 | `cover.tex` | TikZ 自定义设计（深绿底 + 几何图案），非 Prentice Hall 原版封面 | 刻意重制 |
| 2 | `halftitle.tex` | "Topology / Second Edition"，James R. Munkres / MIT / Prentice Hall | ✓ |
| 3 | `copyright.tex` | CIP 数据（`\ttfamily` 等宽）、编辑团队、版权声明、ISBN | ✓ |
| 4 | `dedication.tex` | "For Barbara" 斜体粗体居中 | ✓ |
| 5 | `\tableofcontents` | General Topology / Algebraic Topology，章节编号+页码 | LaTeX 自动生成 |
| 6 | `preface.tex` | 开篇/Prerequisites/组织说明/分支图(TikZ)/课程大纲/修订说明/致谢 | ✓ |
| 7 | `NoteToReader.tex` | 练习说明、四个核心反例列表 | ✓ |

发现的问题：

| # | 文件 | 问题 | 严重性 |
|---|------|------|--------|
| 1 | `copyright.tex` L24, L27 | 行末残留 `\` 反斜杠 | 低 |
| 2 | `copyright.tex` | `\ttfamily` 使 CIP 数据字体与 PDF 不一致 | 低（风格选择） |
| 3 | `preface.tex` L8 | `\vspace{6.5cm}` 硬编码空白 | 中（排版脆弱） |
| 4 | `preface.tex` L5 | `\large` 全局放大前言字号 | 低（风格选择） |
| 5 | `cover.tex` | 封面为全新设计 | 信息（刻意为之） |
| 6 | `halftitle.tex` | 排版布局与 PDF 有细微差异 | 低（风格选择） |
