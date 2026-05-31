# Ch1 格式修改恢复清单

基于对话记录整理。标记状态：⬜ 待修复 / ✅ 已修复。

## sty 改动（已保留，无需再改）

- ✅ Section 字号 `\large` → `\Large`
- ✅ Proof 标题 `\textbf` → `\textsl`
- ✅ Theorem/Lemma/Corollary 正文 `{}` → `\itshape`
- ✅ Example 正文保持 `\normalfont`（ExampleStyle）
- ✅ Theorem/Lemma/Corollary 共享 `theorem` 计数器、按 section 重置
- ✅ `ucorollary` 无编号推论环境
- ✅ 索引页眉 `\MakeUppercase` 移除

## Ch1 正文修改

### 引文块
- [x] L73-75 Miss Smith/Mr. Jones 引文包 `centeredblock`
- [x] L127-129 第二对引文包 `centeredblock`

### 环境包裹
- [ ] L1847 Lemma 7.2 包裹 `\begin{lemma}...\end{lemma}`
- [ ] L2445 "Proof of the lemma." → `\begin{proof}[Proof of the lemma.]...\end{proof}`
- [ ] L2474 "A second proof of Theorem 9.1." → `\begin{proof}[...]...\end{proof}`
- [ ] L2674 `\section*{Corollary...}` → `\begin{ucorollary}...\end{ucorollary}`

### 格式修正
- [ ] L2426 "Axiom of choice." → `\noindent \textbf{Axiom of choice.}`
- [ ] L255 `For at least one \(x \in A\)` 在 `\[...\]` 内 → 改用 `\text{...}`
- [ ] L269 `For every \(x \in A\)` 在 `\[...\]` 内 → 改用 `\text{...}`

### 公式合并 + (*) 标签
- [ ] L1871-1876 h(1)/h(i) 公式对：左侧加 (*)，合并 gathered
- [ ] L2106-2111 h(1)/h(i) 第二对：左侧加 (*)，合并 gathered
- [ ] L2204-2210 h(1)=a0, h(i)=ρ：左侧加 (*)，合并 gathered
- [ ] L2391-2398 f(1)=a1, f(i)=arbitrary：左侧加 (*)，合并 aligned（等号对齐）
- [ ] L2480-2487 f(1)=c(A), f(i)=c(...)：左侧加 (*)，合并 aligned

### 公式合并（无星号）
- [ ] L2136-2142 f(i)=f'(i), f(n)=smallest：合并 gathered
- [ ] L2165-2171 f(i)/g(i) 方程对：合并 gathered
- [ ] L2186-2192 h(i)=f_n(i), f_n satisfies：合并 gathered
- [ ] L2224-2234 三行等号链：合并 aligned（= 对齐）
- [ ] L2364-2368 g(a_n)/g(x) 方程对：合并 aligned
- [ ] L2404-2408 h(1)/h(i) 第三对：合并 aligned
- [ ] L2622-2625 f(x)=f'(x), f(b)=n：合并 aligned
- [ ] L2630-2643 四个 Z+ 集合：合并 aligned 左对齐

### 示例内三组公式（gathered → aligned 等号对齐）
- [ ] a^1/a^n 第一组
- [ ] h(1)/h(i) 第二组
- [ ] a^1/a^l 第三组

### Ch9 等其他章节
- [ ] Ch9 g 方程对齐（等号）
