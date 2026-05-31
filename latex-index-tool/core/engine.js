/**
 * Generic LaTeX Index Insertion Engine
 * =====================================
 * Config-driven, project-agnostic. Supports any index command format
 * (\\idx{}, \\index{}, makeidx, xindy) via pluggable templates.
 *
 * Usage:
 *   const engine = require('./engine');
 *   const ops = engine.findInsertions(content, entries, config);
 *   const result = engine.applyInsertions(content, ops);
 */

/**
 * Detect if position `pos` is inside math mode.
 * Handles $...$, $$...$$, \(...\), \[...\].
 */
function isInsideMath(content, pos) {
  const before = content.slice(Math.max(0, pos - 500), pos);

  // Count unescaped $ signs before pos
  let dollarCount = 0;
  for (let i = 0; i < before.length; i++) {
    if (before[i] === "\\") { i++; continue; }
    if (before[i] === "$") dollarCount++;
  }
  if (dollarCount % 2 === 1) return true;

  // Check \( ... \) balance
  const openP = (before.match(/\\\(/g) || []).length;
  const closeP = (before.match(/\\\)/g) || []).length;
  if (openP > closeP) return true;

  // Check \[ ... \] balance
  const openB = (before.match(/\\\[/g) || []).length;
  const closeB = (before.match(/\\\]/g) || []).length;
  if (openB > closeB) return true;

  return false;
}

/**
 * Check if position `pos` would be inside a LaTeX command name
 * (e.g., \\includegraphics, \\begin, \\section).
 */
function isInsideCommand(content, pos) {
  const before = content.slice(Math.max(0, pos - 50), pos);
  if (before.endsWith("\\")) return true;
  const cmdMatch = before.match(/\\([a-zA-Z@]+)$/);
  if (cmdMatch) return true;
  if (/\\[a-zA-Z@]+\s*$/.test(before)) return true;
  return false;
}

/**
 * Check if position `pos` is inside unbalanced braces.
 */
function isInsideBraces(content, pos) {
  const before = content.slice(0, pos);
  const openB = (before.match(/(?<!\\)\{/g) || []).length;
  const closeB = (before.match(/(?<!\\)\}/g) || []).length;
  return openB > closeB;
}

/**
 * Guard: should we skip this insertion position?
 */
function shouldSkip(content, pos, allowMath) {
  if (isInsideCommand(content, pos)) return true;
  if (isInsideBraces(content, pos)) return true;
  if (!allowMath && isInsideMath(content, pos)) return true;
  return false;
}

/**
 * Strip LaTeX formatting from a term for plain-text matching.
 */
function stripLatex(term) {
  return term
    .replace(/\\\(/g, "").replace(/\\\)/g, "")
    .replace(/\\[a-zA-Z]+(\{[^}]*\})?/g, "")
    .replace(/[{}]/g, "")
    .trim();
}

/**
 * Find the first valid insertion point for `search` in `content`.
 * Returns position index or -1.
 */
function findTerm(content, search, allowMath) {
  if (search.length < 2) return -1;

  const lowerContent = content.toLowerCase();
  const lowerSearch = search.toLowerCase();
  let idx = 0;

  while (idx < lowerContent.length) {
    idx = lowerContent.indexOf(lowerSearch, idx);
    if (idx === -1) return -1;
    if (!shouldSkip(content, idx, allowMath)) return idx;
    idx += search.length;
  }
  return -1;
}

/**
 * Build index command string from template.
 *
 * Template variables:
 *   ${key}      — index sort key
 *   ${display}  — displayed text in body
 *   ${sort}     — math sort key (for idxmath)
 *   ${parent}   — L2 parent term
 *   ${child}    — L2 child term
 */
function buildCommand(entry, templates) {
  const t = templates[entry.level === 2 ? "l2" : (entry.sort_key ? "l1Math" : "l1")];
  if (!t) return null;
  return t
    .replace(/\$\{key\}/g, entry.term || "")
    .replace(/\$\{display\}/g, entry.display || entry.term || "")
    .replace(/\$\{sort\}/g, entry.sort_key || "")
    .replace(/\$\{parent\}/g, entry.parent || "")
    .replace(/\$\{child\}/g, entry.child || entry.term || "");
}

/**
 * Find all insertion operations for a set of entries against content.
 *
 * @param {string} content  - LaTeX source text
 * @param {Array}  entries  - [{term, level, sort_key, display, parent, child}, ...]
 * @param {Object} config   - {templates, aliases, mathShortcuts}
 * @returns {Array} operations - [{pos, len, cmd, entry}, ...] sorted by position descending
 */
function findInsertions(content, entries, config) {
  const ops = [];
  const aliases = config.aliases || {};
  const shortcuts = config.mathShortcuts || {};
  const allowMath = config.allowMathInText !== false; // default true

  // Sort entries by stripped term length (desc): longer first avoids substring hits
  const sorted = [...entries].sort((a, b) => {
    return stripLatex(b.term).length - stripLatex(a.term).length;
  });

  for (const entry of sorted) {
    const term = entry.term;
    let insertPos = -1;
    let cmd = null;

    if (entry.level === 1 && entry.sort_key) {
      // Math symbol: search for raw LaTeX in content (not stripped term)
      const rawLatex = term.replace(/\\\(|\\\)/g, "");  // remove math wrappers
      const shortAliases = shortcuts[rawLatex] || [];
      const patterns = [rawLatex, ...shortAliases, rawLatex.replace(/[{}]/g, "")];

      for (const pat of patterns) {
        if (pat.length < 2) continue;
        insertPos = content.indexOf(pat);
        if (insertPos >= 0 && !shouldSkip(content, insertPos, true)) break;
        insertPos = -1;
      }

      if (insertPos >= 0) {
        cmd = buildCommand(entry, config.templates);
      } else {
        // Try text aliases
        const wordAliases = aliases[rawLatex] || [];
        for (const alt of wordAliases) {
          insertPos = findTerm(content, alt, true);
          if (insertPos >= 0) {
            cmd = buildCommand(entry, config.templates);
            break;
          }
        }
      }
    } else if (entry.level === 1) {
      const search = stripLatex(term);
      if (entry.sort_key) continue; // handled above
      if (/[_^@!|"]/.test(search)) continue; // unsafe for plain text matching

      // Try exact match
      insertPos = findTerm(content, search, allowMath);

      // Try aliases
      if (insertPos < 0) {
        const wordAliases = aliases[search] || aliases[term] || [];
        for (const alt of wordAliases) {
          insertPos = findTerm(content, alt, allowMath);
          if (insertPos >= 0) break;
        }
      }

      if (insertPos >= 0) {
        cmd = buildCommand(entry, config.templates);
      }
    } else if (entry.level === 2) {
      // L2 entries: no display, just index
      const search = stripLatex(entry.child || entry.term);
      insertPos = findTerm(content, search, allowMath);
      if (insertPos >= 0) {
        cmd = buildCommand(entry, config.templates);
      }
    }

    if (insertPos >= 0 && cmd) {
      ops.push({ pos: insertPos, len: 0, cmd, entry });
    }
  }

  // Deduplicate overlapping insertions (keep first = longer term)
  const deduped = [];
  ops.sort((a, b) => a.pos - b.pos);
  for (const op of ops) {
    if (deduped.length === 0) { deduped.push(op); continue; }
    const last = deduped[deduped.length - 1];
    const lastEnd = last.pos + Math.max(last.len, stripLatex(last.entry.term).length);
    if (op.pos < lastEnd) continue; // overlap: skip
    deduped.push(op);
  }

  // Sort by position descending for safe insertion
  deduped.sort((a, b) => b.pos - a.pos);
  return deduped;
}

/**
 * Apply insertion operations to content.
 * Returns modified content.
 */
function applyInsertions(content, operations) {
  for (const op of operations) {
    const before = content.slice(0, op.pos);
    const after = content.slice(op.pos + op.len);
    content = before + op.cmd + after;
  }
  return content;
}

module.exports = { findInsertions, applyInsertions, buildCommand, stripLatex, isInsideMath, isInsideCommand, isInsideBraces };
