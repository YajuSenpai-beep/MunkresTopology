// Validate original/index_entries.json structural integrity
const { loadJSON, formatSection, heading, pass, fail, warn, info } = require('./utils');

function check() {
  const lines = [];
  let passes = 0, failures = 0, warnings = 0;

  lines.push(formatSection('Master JSON Validation'));
  lines.push('  File: original/index_entries.json');

  const { data, error } = loadJSON('original/index_entries.json');
  if (error) {
    lines.push(fail('Valid JSON', error));
    failures++;
    return { passes, failures, warnings, lines };
  }
  lines.push(pass('Valid JSON', 'parsed successfully'));
  passes++;

  // Check wrapper
  if (!data || !Array.isArray(data.entries)) {
    lines.push(fail('Wrapper format', 'missing "entries" array'));
    failures++;
    return { passes, failures, warnings, lines };
  }
  lines.push(pass('Wrapper format', '{"entries": [...]}'));
  passes++;

  const entries = data.entries;
  let l1 = 0, l2 = 0, sortKeyCount = 0, emptyPages = 0;

  // Field validation
  const l1Terms = new Set();
  const seen = new Set();
  let fieldErrors = 0;
  let mathErrors = 0;
  let parentErrors = 0;
  let dupErrors = 0;

  for (const e of entries) {
    if (e.level === 1) { l1++; l1Terms.add(e.term); }
    else if (e.level === 2) l2++;
    else {
      if (fieldErrors === 0) lines.push(fail('Entry level', `invalid level "${e.level}" at "${e.term?.slice(0,40)}"`));
      fieldErrors++;
      continue;
    }

    if (typeof e.term !== 'string' || e.term.length === 0) {
      if (fieldErrors < 5) lines.push(fail('Entry term', `empty or non-string term`));
      fieldErrors++;
      continue;
    }

    if (!Array.isArray(e.page)) {
      if (fieldErrors < 5) lines.push(fail('Entry page', `page not an array for "${e.term.slice(0,40)}"`));
      fieldErrors++;
      continue;
    }

    if (e.page.length === 0) emptyPages++;

    if (e.level === 1 && 'parent' in e) {
      lines.push(fail('L1 has parent', `"${e.term.slice(0,40)}" is L1 but has parent field`));
      fieldErrors++;
    }

    if (e.level === 2) {
      if (typeof e.parent !== 'string' || e.parent.length === 0) {
        lines.push(fail('L2 missing parent', `"${e.term.slice(0,40)}" is L2 without parent`));
        fieldErrors++;
      }
    }

    if ('sort_key' in e) {
      if (typeof e.sort_key !== 'string' || e.sort_key.length === 0) {
        lines.push(fail('sort_key', `empty sort_key for "${e.term.slice(0,40)}"`));
        fieldErrors++;
      }
      if (e.level === 1) sortKeyCount++;
    }

    // Math mode balancing
    const openCount = (e.term.match(/\\\(/g) || []).length;
    const closeCount = (e.term.match(/\\\)/g) || []).length;
    if (openCount !== closeCount && mathErrors < 5) {
      lines.push(fail('Math mode', `unbalanced \\(...\\) in "${e.term.slice(0,50)}"`));
      mathErrors++;
    }

    // Duplicate check
    const key = (e.parent || '') + '::' + e.term;
    if (seen.has(key) && dupErrors < 5) {
      lines.push(fail('Duplicate', `"${e.term.slice(0,40)}" (${e.parent ? 'L2 parent=' + e.parent : 'L1'})`));
      dupErrors++;
    }
    seen.add(key);
  }

  if (fieldErrors === 0) { lines.push(pass('All entries have valid fields')); passes++; }
  else { lines.push(fail('Field validation', `${fieldErrors} error(s)`)); failures++; }

  if (mathErrors === 0) { lines.push(pass('Math mode balanced', '\\(...\\) ')); passes++; }
  else { lines.push(fail('Math mode', `${mathErrors} unbalanced entries`)); failures++; }

  if (dupErrors === 0) { lines.push(pass('No duplicate entries')); passes++; }
  else { lines.push(fail('Duplicates', `${dupErrors} duplicate(s)`)); failures++; }

  // L2 parent resolution (check after all entries parsed)
  let orphanCount = 0;
  for (const e of entries) {
    if (e.level === 2 && typeof e.parent === 'string' && !l1Terms.has(e.parent)) {
      if (orphanCount < 5) lines.push(fail('Orphan L2', `"${e.term.slice(0,40)}" parent "${e.parent.slice(0,40)}" not found in L1`));
      orphanCount++;
    }
  }
  if (orphanCount === 0) { lines.push(pass('All L2 parents resolve to L1 terms')); passes++; }
  else { lines.push(fail('Orphans', `${orphanCount} L2 entries with unresolvable parent`)); failures++; }

  lines.push(heading(`Total: ${entries.length} entries (${l1} L1 + ${l2} L2)`));
  lines.push(info('sort_key', `${sortKeyCount} entries have sort_key`));
  lines.push(info('empty pages', `${emptyPages} entries have empty pages (cross-references)`));

  return { passes, failures, warnings, lines };
}

if (require.main === module) {
  const r = check();
  console.log(r.lines.join('\n'));
  process.exit(r.failures > 0 ? 1 : 0);
}

module.exports = { check };
