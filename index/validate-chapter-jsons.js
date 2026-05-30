// Validate chapters/ch*_entries.json structural integrity
const fs = require('fs');
const path = require('path');
const { PROJECT_ROOT, loadJSON, formatSection, heading, pass, fail, warn, info, summaryLine } = require('./utils');

function check() {
  const lines = [];
  let passes = 0, failures = 0, warnings = 0;

  lines.push(formatSection('Chapter JSON Validation'));

  const indexDir = path.join(PROJECT_ROOT, 'index');
  const existingFiles = fs.readdirSync(indexDir).filter(f => /^ch\d+_entries\.json$/.test(f));

  // Load master for parent resolution of L2 entries
  const master = loadJSON('original/index_entries.json');
  const masterL1 = new Set();
  if (master.data && Array.isArray(master.data.entries)) {
    master.data.entries.filter(e => e.level === 1).forEach(e => masterL1.add(e.term));
  }

  let foundCount = 0, validCount = 0;

  for (let ch = 1; ch <= 14; ch++) {
    const filename = `ch${ch < 10 ? '0' + ch : ch}_entries.json`;
    const filePath = path.join(indexDir, filename);
    const exists = fs.existsSync(filePath);
    const chLabel = `Chapter ${ch}`.padEnd(12);

    if (!exists) {
      if (ch >= 1 && ch <= 9) {
        lines.push(warn(`${chLabel} MISSING    (no ch${ch}_entries.json)`));
        warnings++;
      } else {
        lines.push(fail(`${chLabel} MISSING    (expected ch${ch}_entries.json)`));
        failures++;
      }
      continue;
    }

    foundCount++;
    const { data, error } = loadJSON(`index/${filename}`);
    if (error) {
      lines.push(fail(`${chLabel} ${error}`));
      failures++;
      continue;
    }

    // Check format: bare array
    if (!Array.isArray(data)) {
      lines.push(fail(`${chLabel} format: expected bare array [...], got object`));
      failures++;
      continue;
    }

    let chL1 = 0, chL2 = 0, chSortKey = 0;
    let fieldOk = true, dupOk = true, parentOk = true;
    const seen = new Set();
    const chL1Terms = new Set();

    for (const e of data) {
      if (e.level === 1) { chL1++; chL1Terms.add(e.term); }
      else if (e.level === 2) chL2++;

      if (!e.level || (e.level !== 1 && e.level !== 2)) { fieldOk = false; continue; }
      if (typeof e.term !== 'string' || !e.term) { fieldOk = false; continue; }
      if (!Array.isArray(e.page)) { fieldOk = false; continue; }
      if (e.level === 1 && 'parent' in e) { fieldOk = false; continue; }
      if (e.level === 2 && (typeof e.parent !== 'string' || !e.parent)) { fieldOk = false; continue; }
      if (e.level === 1 && 'sort_key' in e) chSortKey++;

      const key = (e.parent || '') + '::' + e.term;
      if (seen.has(key)) { dupOk = false; }
      seen.add(key);
    }

    // Parent resolution: check against both this chapter's L1 and master L1
    let allParentsOk = true;
    for (const e of data) {
      if (e.level === 2 && typeof e.parent === 'string') {
        if (!chL1Terms.has(e.parent) && !masterL1.has(e.parent)) {
          allParentsOk = false;
        }
      }
    }

    const stats = `${data.length} entries: ${chL1} L1 + ${chL2} L2, ${chSortKey} sort_key`;
    if (fieldOk && dupOk && allParentsOk) {
      lines.push(pass(`Chapter ${ch}  `.padEnd(13) + stats));
      passes++; validCount++;
    } else {
      const issues = [];
      if (!fieldOk) issues.push('field errors');
      if (!dupOk) issues.push('duplicates');
      if (!allParentsOk) issues.push('unresolvable parents');
      lines.push(fail(`Chapter ${ch}  `.padEnd(13) + stats + '  [' + issues.join(', ') + ']'));
      failures++;
    }
  }

  lines.push(heading(`Summary: ${foundCount}/14 chapters have JSONs, ${validCount} valid, ${failures} failed`));
  if (foundCount < 14 && foundCount > 0) {
    lines.push(warn(`${14 - foundCount} chapters (1-9) have no chapter-level index JSON`));
  }

  return { passes, failures, warnings, lines };
}

if (require.main === module) {
  const r = check();
  console.log(r.lines.join('\n'));
  process.exit(r.failures > 0 ? 1 : 0);
}

module.exports = { check };
