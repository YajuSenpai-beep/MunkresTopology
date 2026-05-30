# Ch1 临时修复脚本存档

这是第一章编辑过程中使用的一次性脚本，归档于此供后续 13 章参考。

## 按用途分类

### 公式合并与对齐
- `_gathered_to_aligned.js` — gathered → aligned 环境转换，自动加 `&` 对齐
- `_fix_finv.js` / `_fix_finv2.js` / `_fix_finv3.js` — f^{-1} 公式对的合并
- `_fix_fg.js` — f:A / g:A 公式合并
- `_fix_exercises.js` — Exercises 公式对齐合并（批量 6 组）

### 习题格式
- `_convert_exercises.js` — 11 个习题块自动转换为 enumerate 格式（批量）
- `_fix_ex.py` / `_fix_ex2.py` / `_fix_ex34.js` / `_fix_ex8.py` — 个别习题修复
- `_fix_ex_all.py` — 批量修复 13 个 (a) 入子题
- `_fix_last5.py` — 最后 5 个 (a) 入子题
- `_fix_ex2_11.py` / `_fix_remaining.py` — §11 / 其余习题修复
- `_fix_paras.py` — 习题内延续段落换行修复

### 引号修复
- `_fix_quotes2.js` / `_fix_quotes3.js` — 三类引号 OCR 错误批量修复（22 处）

### 环境/结构检查
- `_check_ex_envs.js` — 扫描习题块内的 theorem/lemma/proof 环境
- `_check_proofs.js` — 比对 backup 和 current 的 proof 结束位置
- `_trace_theorem.js` — 追踪 theorem 环境的 begin/end 嵌套
- `_quick_scan.py` — 快速扫描习题块残留问题

### centeredblock 包裹
- `_wrap_ch1.js` — 将 Ch1 全部 example 用 centeredblock 包裹

## 注意事项

- 这些脚本在第一章语境下编写，用于其他章节时需检查路径和匹配文本
- `_fix_*.py` 使用 Python raw string 避免转义问题
- `_convert_exercises.js` 处理批量转换时存在局限（分隔文字误并入子题等）
- 推荐：先用 `_quick_scan.py` 扫描目标章节，再按需选用修复脚本
