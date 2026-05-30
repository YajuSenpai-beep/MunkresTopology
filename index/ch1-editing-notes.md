# 第一章正文修订经验总结

基于 2026.05.29–05.31 对话记录整理。

## 一、公式排版

### 1.1 多行公式合并

OCR 产生的独立 `\[...\]` 公式对，按语义合并为 `aligned`（等号对齐）或 `gathered`（居中），后期全部统一为 `aligned`。

**等号对齐**：
```latex
% 前：两个独立 \[...\]
\[ f(x) = g(x) \]
\[ f(a_0) = n+1 \]
% 后：aligned 等号对齐
\[ \begin{aligned}
f(x) &= g(x), \\
f(a_0) &= n+1
\end{aligned} \]
```

**带 (*) 标记的公式对**：`(*)` 提至公式左侧，用 `\qquad` 与公式分隔。
```latex
\[ \left( *\right) \qquad \begin{aligned}
h(1) &= \text{smallest element of } C, \\
h(i) &= \text{smallest element of } [C - h(\{1,\ldots,i-1\})]
\end{aligned} \]
```

**无等号的左对齐**：用 `&` 在行首。
```latex
\[ \begin{aligned}
&\text{If } x > y \text{ and } z < 0, \text{ then } x\cdot z < y\cdot z. \\
&-1 < 0 \text{ and } 0 < 1.
\end{aligned} \]
```

**冒号对齐**（函数定义）：
```latex
\[ \begin{aligned}
f &: \mathbb{R} \to \mathbb{R} &&\text{defined by } f(x) = x^2, \\
g &: \overline{\mathbb{R}}_+ \to \mathbb{R} &&\text{defined by } g(x) = x^2.
\end{aligned} \]
```

### 1.2 全部使用 `aligned`

`gathered` 环境后来全部改为 `aligned`，确保公式左对齐/等号对齐一致。第一章共有 17+ 个 `aligned` 环境，0 个 `gathered`。

### 1.3 (*) 标记标准化

所有 (*) 标记统一使用 `\(\left( *\right)\)`（行内）或 `\[\left( *\right)\]`（展示）。排查并修复了 5 处纯文本 `(*)`。

## 二、定理类环境

### 2.1 环境包裹原则

OCR 中以下模式需要包裹：
- `Lemma N.N. statement` → `\begin{lemma} statement \end{lemma}`
- `Theorem. statement` → `\begin{theorem} statement \end{theorem}`
- `Proof. text` → `\begin{proof} text \end{proof}`
- `Definition. text` → `\begin{definition} text \end{definition}`
- `Corollary. text` → `\begin{corollary} text \end{corollary}`（有编号）
- `Corollary. text`（无编号）→ `\begin{ucorollary} text \end{ucorollary}`

**带名称的定理**：名称放入可选参数。
```latex
\begin{theorem}[Well-ordering theorem] ... \end{theorem}
\begin{lemma}[Kuratowski] ... \end{lemma}
```

### 2.2 环境平衡检查

使用脚本追踪 `\begin{...}` 与 `\end{...}` 配对。发现定理 7.1 的 `\end{theorem}` 错位（应在 `\begin{proof}` 之前，实际在 150 行之后），导致大段文字被斜体吞没。

**关键教训**：环境未闭合会导致后续所有文本使用该环境的字体样式（如 theorem 的 `\itshape`），是排版异常的常见原因。

### 2.3 习题中的环境

习题内部不应有 `\begin{theorem}` / `\begin{lemma}` / `\begin{proof}` 等环境。共清理 6 处，改为纯文本标记（如 `\textbf{Theorem.}` 或 `\textbf{Lemma (Kuratowski).}`）。

## 三、centeredblock 包裹

### 3.1 哪些需要包裹

- 所有 `\begin{example}...\end{example}`（30 个）
- 引文块（如 Miss Smith / Mr. Jones 语录）
- 独立的讨论段落（如 DeMorgan 口诀、空族并交讨论、有序对定义、理发师悖论）
- 注意：习题部分不需要 centeredblock

### 3.2 包裹脚本

`wrap-examples.js`：检测未被 `centeredblock` 包裹的 `\begin{example}` 并添加包裹。注意在 bash 中执行 JS 时 `\\begin{example}` 的转义问题——`\b` 在 JS 字符串中被解释为退格符，应使用 `String.raw` 或将脚本写入文件。

## 四、引号

### 四类引号问题

| 类型 | 模式 | 示例 | 数量 |
|------|------|------|------|
| D | `,''` 误为 `, `` ` | `saying,''If` → `saying, ``If` | 5 |
| E | 中间闭引号误为开引号 | ` ``X `` means` → ` ``X '' means` | 13 |
| F | Unicode 智能引号 | `"If` (U+201C) → ` ``If` | 1 |
| 直引号 | section/脚注中 `"..."` | `"or"` → ` ``or'' ` | 3 |

**总计**：22 处引号修复。

### 关键教训

- OCR 系统性地将 `''`（闭引号）误读为 ` `` `（开引号），特征信号是第二个 ` `` ` 后紧跟 `means` / `can` / `is` / `and` 等接续词。
- Unicode 智能引号 `"` (U+201C) 和 `"` (U+201D) 需替换为 LaTeX ` `` ` 和 `''`。
- section 标题中的引号同样需要 LaTeX 格式。

## 五、OCR 文本错误

### 5.1 拼写错误（8 处）

| 原文 | 正确 |
|------|------|
| `ongin` | `origin` |
| `\operatorname{simplyby}` | `simply by` |
| `posiave` | `positive` |
| `Structly` | `Strictly` |
| `to proved` | `to prove` |
| `ngorously` | `rigorously` |
| `conduction` | `condition` |
| `Schernatically` | `Schematically` |

### 5.2 冒号 OCR（12 处）

两类：`.` → `:`（7 处）和 `\cdot` → `:`（5 处）。常见于函数定义 `f.A → B` 应为 `f : A → B`。

### 5.3 括号不匹配（7 处）

| 问题 | 示例 |
|------|------|
| `\rbrack` 误代 `\}` | `\{1,\ldots,n\rbrack` → `\{1,\ldots,n\}` |
| Hint 后 `}` 应为 `]` | `[Hint. ...\}` → `[Hint: ...]` |
| `\lbrack ... \}` 混用 | 统一使用 `\left\lbrack ... \right\rbrack` |

### 5.4 数学字体（9 处）

- `\mathbf{Z}` → `\mathbb{Z}`（3 处）
- `\mathbf{A}` / `\mathbf{C}` → `A` / `C`（普通斜体）
- `\varepsilon` → `\mathcal{E}`（集族应该用花体，2 处）
- `{Z}_{+}` → `{\mathbb{Z}}_{+}`（`\mathbb` 丢失）
- `\mathcal{C}` → `C`（个别处的错误花体）

### 5.5 缺失句号（~22 处）

典型模式：`word Next` → `word. Next`。使用 `[a-z] [A-Z]` 模式可批量检测。

### 5.6 其他（~15 处）

- `{C}^{7}` → `C\)?`（上标 7 误为问号）
- `{B}_{t}` / `{A}_{t}` → `{B}_{i}` / `{A}_{i}`（下标 `t` 误为 `i`）
- `Figure 11 1` → `Figure 11.1`
- `{a}^{l}` → `{a}^{i}`（`l` 误为 `i`，2 处）
- 逗号拼接 → 分号/句号

**合计约 72 处 OCR 错误**。详细清单见 [ch1-ocr-errors.md](ch1-ocr-errors.md)。

## 六、习题排版

### 6.1 方案选择

使用 `enumitem` 宏包的 `enumerate` 环境，放弃早期的纯文本编号。在 `TopologyBook.sty` 中添加：
```latex
\RequirePackage[shortlabels]{enumitem}
```

### 6.2 标准模板

**外层（习题编号）**：
```latex
\begin{enumerate}[itemsep=0.4em, parsep=0pt, topsep=0pt, partopsep=0pt,
                  leftmargin=*, label=\arabic*., ref=\arabic*]
```

**子题（字母编号）**：
```latex
\begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt,
                  leftmargin=*, label=(\alph*), align=left]
```

**孙题（罗马数字编号）**：
```latex
\begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt,
                  leftmargin=*, label=(\roman*), align=left]
```

### 6.3 子题分段

使用 `resume` 在子 enumerate 间保持编号连续（用于有分隔文字的习题）：

```latex
\item ...
  \begin{enumerate}[label=(\alph*), align=left]
  \item (a)--(d)
  \end{enumerate}
  Show that \(f\) preserves inclusions and unions only:
  \begin{enumerate}[label=(\alph*), align=left, resume]
  \item (e)--(h)
  \end{enumerate}
```

**注意**：`resume` 使用默认 series，与其他 `resume` 会串扰。跨节使用时换用 `start=N` 更安全。

### 6.4 习题内子标题

习题分组标题（如 "Equivalence Relations" / "Order Relations"）应放在 enumerate 之外，使用 `\noindent\textbf{...}`：

```latex
\end{enumerate}

\noindent\textbf{Order Relations}

\begin{enumerate}[..., resume]
```

### 6.5 常见问题

| 问题 | 现象 | 修复 |
|------|------|------|
| `(a)` 在父级 item 中 | 子 enumerate 只有 `(b)` 一个 item | 删除父级 `(a)`，改为 `\item` 空壳，内容放入子 enumerate |
| OCR 残留编号 | `4. Text` 而非 `\item Text` | 替换为 `\item Text` |
| 习题连行 | Ex3 和 Ex4 在同一行 | 分行 |
| 孙题合并 | `(i) (ii) (iii)` 挤在一个 item | 拆分为嵌套 enumerate |

### 6.6 转换脚本风险

`_convert_exercises.js` 批量转换了 12 个习题块，但存在以下局限：
- 分隔文字（如 "Show that \(f\) preserves..."）被误并入子题
- 部分习题的 `(a)` 未正确提取
- 需手动逐块检查修正

**教训**：自动转换后必须人工验证每个习题块。

## 七、实数的公理排版

8 条公理分三组（Algebraic / Mixed / Order），使用 enumerate + `resume` 编号连续 1–8：

```latex
\noindent\textbf{Algebraic Properties}
\begin{enumerate}[nosep, leftmargin=*, label=(\arabic*)]
\item ...  % (1)-(5)
\end{enumerate}

\noindent\textbf{A Mixed Algebraic and Order Property}
\begin{enumerate}[nosep, leftmargin=*, label=(\arabic*), resume]
\item ...  % (6)
\end{enumerate}

\noindent\textbf{Order Properties}
\begin{enumerate}[nosep, leftmargin=*, label=(\arabic*), resume]
\item ...  % (7)-(8)
\end{enumerate}
```

加乘配对公式用 `aligned[t]` 左对齐、顶部对齐编号。

## 八、Proof QED 位置验证

通过比对 `Chapter_1_backup.tex`（OCR 原文）和当前 tex 的所有 proof 结束位置，确认 28 个 proof 的 QED 标记全部在正确位置。有两个 proof 从原始裸文本手动包裹（"Proof of the lemma" 和 "A second proof"），其余 26 个与 OCR 原文一致。

## 九、样式调整

### 9.1 章节字体

`TopologyBook.sty` 中 chapter 标题从 `\Huge`（≈25pt）调大为 `\fontsize{30}{36}`，"Chapter N" 标签调为 `\fontsize{28}{34}`。

### 9.2 取消首段缩进

`\titlespacing{name=\section,numberless}` 缺少 `*` → 改为 `\titlespacing*{...}`。`*` 变体自动添加 `\@afterindentfalse`。

### 9.3 enumitem 包

在 sty 文件中添加 `\RequirePackage[shortlabels]{enumitem}`，提供 `enumerate` 的 `label`、`resume`、`align` 等选项。

## 十、工作流经验

### 10.1 工具选择

| 任务 | 推荐方式 | 原因 |
|------|---------|------|
| 单处精确修改 | `Edit` 工具 | 直接、可审查 |
| 批量相同模式替换 | Python 脚本文件 | 避免 bash 转义地狱 |
| 跨文件批量修改 | Node.js 脚本文件 | 快速、可控 |
| 模式检测/审计 | Explore Agent | 全局搜索能力强 |
| 纯文本替换 | Python raw string | `\b` `\(` 等不会转义 |

### 10.2 转义问题

- **Bash `node -e`**：双重转义噩梦。`\\` → bash → `\` → Node → `\`（或 `\b` → 退格符）。绝不用于包含 `\` 的文本。
- **Python 脚本文件**：使用 raw string `r"..."` 避免 `\b` `\(` 等被解释。
- **sed 中的 `\{`**：在基本正则中是量词标记，需使用 perl 替代。

### 10.3 文件修改争用

IDE linter 频繁在 Read 和 Edit 之间修改文件，导致 Edit 报错 "File has been modified since read"。应对策略：
- 使用 Bash 工具直接操作文件（sed/perl/python）
- 减小 Edit 的 old_string 长度，提高命中率
- 先 Read 再立即 Edit

### 10.4 索引命令与文本

`\idx{}` 命令嵌入单词中间会导致单词断裂（如 `inter\idx{Section}section`）。应放在完整单词之后。

## 十一、编译状态

第一章全流程修订后：
- **编译错误**：0
- **PDF 页数**：约 618 页
- **环境平衡**：全部 `\begin{...}` / `\end{...}` 匹配
- **习题块**：12 个，104 题，全部使用 enumerate 格式
- **aligned 环境**：17+ 个，gathered：0
- **centeredblock 环境**：36 个
- **引号修复**：22 处
- **OCR 错误修复**：约 72 处

---

> **对其他 13 章的参考价值**：所有 OCR 错误类型（拼写、冒号、括号、字体、句号、引号）在其他章节中同样存在。equation 合并、定理环境包裹、习题 enumerate 转换等流程可复用。建议逐章审计，先跑自动检测脚本再人工修正。
