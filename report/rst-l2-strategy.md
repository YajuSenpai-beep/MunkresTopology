# R/S/T 字母组 L2 深度比对策略

## 现状

R/S/T 三个组共约 70+ 个 OCR L2 条目在 `.ind` 中缺失。每个条目需要：
1. 从 OCR 查找 L2 所属的 L1 父条目
2. 在章节 .tex 中定位对应原文
3. 添加 `\index{parent!child}` 命令
4. 编译验证

## 策略（与 Q、U-Z 流程一致）

### 第一步：列出目标
对每个字母组，列出 OCR 中有但 `.ind` 中缺的 L2 条目清单。

### 第二步：批量搜索
对每个缺失 L2，grep 搜索 14 个章节文件中的关键词匹配。

### 第三步：定位添加
找到原文位置后，在合适位置插入 `\index{}` 命令。

### 第四步：编译验证
每轮修改后完整编译验证。

## R 组 L2 目标清单

| 父条目 | 缺失 L2 |
|--------|---------|
| Regularity | of orbit space, and perfect maps, of topological groups, vs. complete regularity, vs. Hausdorff condition, vs. metrizability, vs. normality |
| \(\mathbb{R}\) (reals) | algebraic properties, compact subspaces, connected subspaces, local compactness, K-topology, lower limit topology, metric for, order properties, second-countability, standard topology, uncountability |
| Restriction | (already complete) |
| Retraction | as quotient map |

## S 组 L2 目标清单

| 父条目 | 缺失 L2 |
|--------|---------|
| Second-countability | of compact metric space, of C(I,R), of orbit space, and perfect maps, of products, of R/R^n/R^ω, of R_ℓ, of subspace, of topological group, vs. countable dense subset, vs. Lindelöf condition |
| Seifert-van Kampen theorem | classical version |
| Simply connected | star-convex set |
| Stone-Čech compactification | of S_Ω |
| Separation | by continuous functions |

## T 组 L2 目标清单

| 父条目 | 缺失 L2 |
|--------|---------|
| Topological group | complete regularity, normality, paracompactness, π₁ is abelian, second-countability |
| Tychonoff theorem | for countable products, via well-ordering theorem |
| Topologist's sine curve | connectedness, path components, does not separate S² |
| Torus | covering space of, fundamental group, as quotient space |

## 执行顺序

R → S → T，每个条目按清单顺序批量查找原文位置。
