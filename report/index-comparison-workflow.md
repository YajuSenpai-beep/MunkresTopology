# 索引比对工作流程改进报告

## 初始方案（失败）

### 方案 A：全局 L2 文本匹配

对每个 JSON 条目 `(L1, L2)`，在 `.ind` 中全局搜索 L2 文本（不限父条目）。bigram 相似度 ≥ 0.45 即判"存在"。

**问题**：条目挂在错误父节点下也被判为"存在"。

- `Second-countability!of topological group` 匹配到 `Comparability: of cardinalities!of topologies` → 假阴性
- `Subspace topology!compactness` 匹配到 `Compactness!of subspace` → 假阴性
- 用户人工检查后发现大量遗漏，算法的"0 缺失"结论不可信

### 方案 B：子串匹配

`independence` 不在 `independent` 中 → 漏匹。OCR 用词差异（independence/independent, is/is an）导致假阳性。

## 最终方案（可靠）

### 父节点感知比对

1. **解析 JSON** → `{L1_term: [L2_terms]}`，剥离 `(cont.)` 后缀
2. **解析 `.ind`** → `{L1_term: [L2_terms]}`，剥离 `\hyperpage`
3. **逐字母组比对**：
   - 对每个 JSON L1，在所有 `.ind` L1 中找最佳匹配（bigram ≥ 0.5）
   - 若找不到匹配 → L1 缺失（含其所有 L2）
   - 若找到匹配 → 在该 L1 的 L2 列表中逐一检查每个 JSON L2（bigram ≥ 0.45）
   - 若 L2 不在该父节点下 → 真缺失

### 关键参数

| 参数 | 值 | 说明 |
|------|-----|------|
| L1 匹配阈值 | 0.50 | bigram Jaccard |
| L2 匹配阈值 | 0.45 | 需同时在该 L1 下 |
| LOW 标记阈值 | 0.70 | L1 或 L2 相似度低于此值标记为需人工确认 |

### 清理步骤（比对前必须执行）

1. `_dedup_index.py` — 去除相邻重复 `\index{foo}\index{foo}\index{foo}` → 单份
2. 修复 `\\index` 双反斜杠 → `\index`
3. 修复 `}index{` 缺反斜杠 → `}\index{`
4. 修复 `\index` 割裂单词（`pro\index{...}of` → `proof. \index{...}`）
5. `_fix_ind.py` 续行 bug — 收集子条目时需跳过 `\hyperpage` 续行

### 工具链

| 脚本 | 用途 |
|------|------|
| `_dedup_index.py` | 去除相邻重复 `\index` |
| `_compare_index.py` | 父节点感知比对，输出缺失清单 |
| `_postfix.py` | 编译前：`\idx`→`\index`，排序键规范化 |
| `_fix_ind.py` | 编译后：去重、重分配、续行处理 |
| `_makeindex.py` | 包装 makeindex + fix 脚本 |

### 经验教训

1. **永远不要跨父节点匹配 L2**。`Compactness!of subspace` ≠ `Subspace topology!compactness`
2. **OCR 用词差异必须用 bigram/trigram 相似度**，不能用子串或词重叠
3. **编译流水线的每个环节都可能引入污染**：`_postfix.py`、`_fix_ind.py`、makeindex、引擎插入都可能破坏正文
4. **先清理再比对**。正文污染（`\\index`、割裂单词、三重重复）会导致比对结果不可靠
5. **续行处理是常见 bug 源**。`.ind` 中 `\hyperpage` 独占一行会破坏基于邻接的解析逻辑
