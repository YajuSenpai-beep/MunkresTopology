# 字母组索引修复报告

## 已完成字母组：A, B, J, K, U, V, W, X, Z

---

## A 组（前一会话）
| 条目 | 操作 |
|------|------|
| Cone | 新增（Ch13 §82 习题） |
| Tower | 新增（Ch1 Well-Ordering 习题） |
| Axiom of choice L2s | 手动补全 |
| Absolute retract!vs. universal extension property | 新增 L2 |

## B 组
| 条目 | 操作 |
|------|------|
| Bd A | 新增 L1（Ch2 习题） |
| β(X) (see Stone-Čech) | 新增 L1（Ch5 定义处） |
| Basis!for a topology | 新增 L2（Ch2 定义处） |
| Boundary!of a surface with boundary | 新增 L2（Ch12） |
| Box topology!vs. product/uniform/fine topology | 新增 3 个 L2 |
| Baire space!fine topology on C(X,Y) | 新增 L2（Ch8） |
| Base point!effect on h\_\*/π₁ | 新增 2 个 L2（Ch9） |
| Bⁿ!compactness/fundamental group/path connectedness | 补全 3 个 L2（sort key 问题，通过 `_fix_bn.py` 修正） |
| B^n/B(x,ε) 重复条目 | `_fix_ind.py` 归一化数学模式去重 |

## J 组
| 条目 | 操作 |
|------|------|
| J-tuple | 新增 L1（Ch1 m-tuple 定义处） |

## K 组
| 条目 | 操作 |
|------|------|
| k-fold covering | 新增 L1（Ch9 §53 习题） |
| k-plane | 新增 L1（Ch8 §50 定义处） |
| K-topology (see also R\_K) | 新增 L1（Ch2 定义处） |

## U 组
| 条目 | 操作 |
|------|------|
| Uncountability | 重构：L1 名称从 "Uncountability: of P(Z+)" 改为 "Uncountability:"，of P(Z+) 降为 L2 |
| Uncountability!of R 重复 | 修复 `.tex` 源文件中 `\left/\right` 导致的 L1 重复 |
| Uncountability!of transcendental numbers | 新增 L2（Ch1 习题） |
| Uncountable well-ordered set | 新增 L1（Ch1 推论） |
| Uniform topology L1 + vs. box topology | 新增 L1 + L2（Ch2） |
| Uniform topology!vs. compact convergence topology | 新增 L2（Ch7） |
| Uniform convergence!Weierstrass M-test | 新增 L2（Ch2 习题） |
| Uniform limit theorem!converse fails | 新增 L2（Ch2 习题） |
| Uniform metric!completeness | 新增 L2（Ch7） |
| Uniform metric!vs. sup metric | 新增 L2（Ch7） |
| Urysohn lemma!strong form | 新增 L2（Ch4 §33 习题5） |
| Unit ball/circle/sphere (see also) | 新增 3 个交叉引用 L1 |
| Universal covering space!existence | 新增 L2（Ch13 Theorem 82.1） |
| Utilities graph!nonembeddability | 新增 L2（Ch10） |
| U(A,ε) 错位子条目 → Uncountability | `_fix_misc.py` 错位修正 |

## V 组
| 条目 | 操作 |
|------|------|
| Vertex!of a curved triangle | 从独立 L1 转为 L2（Ch12） |
| Vertex!of a linear graph | 新增 L2（Ch14 习题） |
| Vertex!of a polygonal region | 新增 L2（Ch12） |

## W 组
| 条目 | 操作 |
|------|------|
| Wedge of circles | 新增 L1（修复嵌套 `\index` bug） |
| Wedge of circles!existence/fundamental group | 新增 2 个 L2（Ch11） |
| Well-ordered set!compact subspaces | 新增 L2（Ch3） |
| Well-ordered set!dictionary order | 新增 L2（Ch1） |
| Well-ordered set!finite | 新增 L2（Ch1） |
| Well-ordered set!normality | 新增 L2（Ch4） |
| Well-ordered set!subsets well-ordered | 新增 L2（Ch1） |
| Well-ordering theorem!and axiom of choice | 新增 L2（Ch1） |
| Well-ordering theorem!and maximum principle | 新增 L2（Ch1 习题） |
| Well-ordering theorem!applied | 新增 L2（Ch5 Tychonoff） |
| Winding number!as an integral | 新增 L2（Ch10） |
| Word!reduced | 新增 L2（Ch11） |

## Z 组
| 条目 | 操作 |
|------|------|
| Z（整数符号） | 新增 L1（Ch1） |
| Z⁺（正整数符号） | 新增 L1（Ch1） |
| Z⁺!not finite | 新增 L2（从 Z 下移） |
| Z⁺!well-ordered | 新增 L2（Ch1） |
| Zorn's lemma!vs. maximum principle | 新增 L2（Ch1） |
| Zorn's lemma!applied | 新增 L2（Ch5, Ch14） |

---

## 编译管线改进

| 工具 | 作用 |
|------|------|
| `_fix_ind.py` | 合并 (cont.) 条目、去重 L1（归一化数学模式分隔符）、前缀合并、L2 去重、符号条目重分配 |
| `_fix_bn.py` | 修正 makeindex 对 Bⁿ sort key 的排序错误 |
| `_fix_misc.py` | 通用错位修正（U(A,ε)→Uncountability 等）+ L1 合并 + L2 去重 |
| `_makeindex.py` | Python 包装脚本，串联 makeindex + 三个 fix 脚本（替代 `&&` 链） |
| `.latexmkrc` | 统一用 `python latex-index-tool/_makeindex.py` 作为 `$makeindex` |

## 通用修复

- 修复引擎把 `\index` 插入 `\begin{...}` 中间导致的 `\beg` 断裂（Ch3 三处）
- 修复 `\widehat{\alpha}` 缺少数学模式导致的编译错误
- 修复 `_fix_ind.py` 中数学模式分隔符 `$`/`\(`/`\)` 去重归一化
- 修复 sort key `^` 字符导致的 makeindex 排序错位

## 统计

- 条目数：600（从初始约 624 提升，重复合并后净增约 30+ 条目）
- `.ind` 行数：975
- makeindex：0 rejected，0 warnings
- 编译错误：0
