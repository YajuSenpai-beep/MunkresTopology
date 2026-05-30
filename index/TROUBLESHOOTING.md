# Index 故障排除与经验记录

## XeLaTeX + makeindex: `\idxmath` 中鲁棒命令的展开问题

### 发现日期

2026-05-30

### 现象

编译后 `makeindex` 报告 1 条 rejected：
```
!! Input index error (file = Topology_by_Munkres.idx, line = 207):
   -- Extra `@' at position 15 of first argument.
```

被拒条目：
```
\indexentry{d@\(\setbox \z@ \hbox {\mathsurround \z@ $\textstyle d$}\mathaccent "0365{d}\)|hyperpage}{143}
```

### 根因定位

1. 源文件 `chapters/Chapter_2_Topological_Spaces_and_Continuous_Functions.tex` L1870：
   ```latex
   \idxmath{d}{\(\widetilde{d}\)}
   ```

2. `\idxmath` 定义（`TopologyBook.sty` L423）：
   ```latex
   \newcommand{\idxmath}[2]{\index{#1@#2}\idxfmt{#2}}
   ```
   即写入 `.idx` 的是 `\index{d@\(\widetilde{d}\)}`

3. **`\widetilde` 是 LaTeX 鲁棒命令**（由 `\DeclareRobustCommand` 定义），理论上在 `\write`（`\index` 底层使用的 TeX 原语）中**不应展开**

4. **但在 XeLaTeX 下，`\widetilde` 仍被完全展开**。展开结果包含 `\z@`（一个 TeX 内部寄存器，值为 0pt），其中的 `@` 字符被 `makeindex` 误解析为 sort/display 分隔符，导致拒绝该条目

### 根因分析

`\index` 命令（来自 `makeidx` 宏包）使用 `\write` 将条目写出到 `.idx` 文件。`\write` 在写出前会**完全展开**其参数。鲁棒命令通常通过 `\protect` 机制在 `\write` 中生存，但 XeLaTeX 对 `\widetilde` 的保护实现与 pdfLaTeX 不同，导致意外展开。

**受影响的命令**：任何在 XeLaTeX 下被 `\index{...@...}` 包裹的数学模式命令，尤其是带重音/装饰的符号（`\widetilde`, `\widehat`, `\bar`, `\tilde`, `\hat` 等）。

### 修复方案

**方案 A（已采用）：在源文件中保护**

在 `.tex` 源文件中，对 `\idxmath` 第二个参数中的脆弱命令添加 `\protect`：

```latex
% 修复前
\idxmath{d}{\(\widetilde{d}\)}

% 修复后
\idxmath{d}{\(\protect\widetilde{d}\)}
```

改动文件：`chapters/Chapter_2_Topological_Spaces_and_Continuous_Functions.tex` L1870

**方案 B（.sty 层面，未采用）**：修改 `\idxmath` 定义为 `\protected@write` 版本：

```latex
\makeatletter
\newcommand{\idxmath}[2]{\protected@write\@indexfile{}{\string\indexentry{#1@#2}{\thepage}}\idxfmt{#2}}
\makeatother
```

> 未采用原因：直接操作 `\@indexfile` 绕过了 `\makeindex` 的 `\@sanitize` 处理，可能引入其他兼容性问题。保持 `\idxmath` 定义简单，在调用点按需保护更可控。

**方案 C（未采用）**：在 `.sty` 中使用 `\unexpanded{#2}`：

```latex
\newcommand{\idxmath}[2]{\index{#1@\unexpanded{#2}}\idxfmt{#2}}
```

> 未采用原因：`\unexpanded` 在 `\write` 中同样被丢弃，不能阻止展开。

### 预防措施

今后在 `.tex` 源文件中使用 `\idxmath` 时，如果第二个参数包含带重音的数学命令，应显式添加 `\protect`：

```latex
\idxmath{A}{\(\protect\bar{A}\)}          % OK
\idxmath{alpha}{\(\protect\widehat{\alpha}\)}  % OK
\idxmath{d}{\(\protect\widetilde{d}\)}    % OK
\idxmath{ell}{\({\protect\ell}^{2}\)}     % OK
\idxmath{R}{\(\mathbb{R}\)}              % OK — \mathbb 内部不含 @
```

不带重音的数学命令（`\mathbb`, `\mathcal`, `\mathbf` 等）通常不受影响，因为它们内部不含 `@` 字符。

### 编译验证

```
rm -f Topology_by_Munkres.idx Topology_by_Munkres.ind
xelatex Topology_by_Munkres
makeindex -s Topology_by_Munkres.ist Topology_by_Munkres.idx
xelatex Topology_by_Munkres
xelatex Topology_by_Munkres
```

结果：549 accepted, 0 rejected, 0 errors.

---

## 索引插入脚本开发经验

### 102 错误 → 0 错误的修复历程

| # | 问题 | 原因 | 修复 | 减少错误 |
|---|------|------|------|----------|
| 1 | `\idx` 在数学模式内 | `findInsertPoint` 未检测 `$...$` 环境 | `isInsideMath()` 函数 | -92 |
| 2 | `\idx` 在 LaTeX 命令名内 | `\idx` 插入到 `\includegraphics` 中间 | 检测 `\<cmdname>` 模式 | -8 |
| 3 | TeX 特殊字符在索引参数中 | 无 `sort_key` 的条目含 `_`, `^` 等 | `if (/[_^\\@!|\"]/.test(term)) continue;` | -2 |
| 4 | `\idxmath` 中 `\widetilde` 展开 | XeLaTeX `\write` 展开鲁棒命令 | 源文件中使用 `\protect\widetilde` | -1 |
| 5 | 重叠插入 | 两条命令覆盖同一文本范围 | 去重检测 | -1 |

### 插入脚本的安全守卫

`insert-commands.js` 中的 `findInsertPoint()` 经过以下守卫层：

1. **LaTeX 命令名检测** — 不在 `\<letters>` 中间插入
2. **花括号内检测** — 不在 `{...}` 参数内部插入
3. **数学模式检测** — 不在 `$...$` / `\(...\)` / `\[...\]` 中插入
4. **TeX 特殊字符过滤** — 含 `_^@!|"` 的条目不生成 `\idx`
5. **sort_key 守卫** — 有 `sort_key` 的条目只能用 `\idxmath`，不降级为 `\idx`
6. **重叠去重** — 插入范围重叠时，保留最右（从后向前插入）
