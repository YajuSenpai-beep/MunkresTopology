// Compare index commands found in .tex source against master JSON target
const fs = require('fs');
const path = require('path');
const { PROJECT_ROOT, loadJSON, extractCommands, normalizeTerm, formatSection, heading, pass, fail, warn, info } = require('./utils');

function check() {
  const lines = [];
  let passes = 0, failures = 0, warnings = 0;

  lines.push(formatSection('Coverage Analysis'));

  const master = loadJSON('original/index_entries.json');
  if (master.error) {
    lines.push(fail('Cannot load master JSON', master.error));
    failures++;
    return { passes, failures, warnings, lines };
  }

  // Collect all index commands from all chapter .tex files
  const chaptersDir = path.join(PROJECT_ROOT, 'chapters');
  const files = fs.readdirSync(chaptersDir).filter(f => f.startsWith('Chapter_') && f.endsWith('.tex'));

  const sourceL1 = new Set();
  const sourceL2 = new Set();
  const sourceMath = new Map(); // display -> sort

  for (const f of files) {
    const content = fs.readFileSync(path.join(chaptersDir, f), 'utf8');
    const cmds = extractCommands(content);
    for (const term of cmds.idx) sourceL1.add(term);
    for (const m of cmds.idxmath) sourceMath.set(m.display, m.sort);
    for (const s of cmds.idxsub) sourceL2.add(s.parent + '::' + s.term);
  }

  const sourceTotal = sourceL1.size + sourceL2.size + sourceMath.size;
  lines.push(info(`Source commands found: ${sourceL1.size} idx + ${sourceL2.size} idxsub + ${sourceMath.size} idxmath = ${sourceTotal}`));
  lines.push(info(`Master target: ${master.data.entries.length} entries (685 L1 + 733 L2)`));

  // Match master entries against source
  let matched = 0, missing = 0, extra = 0;
  const missingL1 = [];
  const mathCheckIssues = [];

  for (const e of master.data.entries) {
    let found = false;
    if (e.level === 1) {
      if (sourceL1.has(e.term)) found = true;
      else if (sourceMath.has(e.term)) found = true; // \idxmath display matches term
    } else {
      found = sourceL2.has(e.parent + '::' + e.term);
    }

    if (found) matched++;
    else {
      missing++;
      if (e.level === 1 && missingL1.length < 15) missingL1.push(e);
    }
  }

  // Math mode audit: entries with sort_key should use \idxmath
  let mathMisuse = 0;
  for (const e of master.data.entries) {
    if (e.sort_key && e.level === 1) {
      if (sourceL1.has(e.term)) {
        // Found via \idx instead of \idxmath - potential issue
        mathCheckIssues.push(`"${e.term.slice(0,50)}" has sort_key="${e.sort_key}" but found via \\idx (should use \\idxmath)`);
        mathMisuse++;
      }
    }
  }

  // Coverage percentage
  const pct = master.data.entries.length > 0 ? (matched / master.data.entries.length * 100) : 0;

  if (matched === 0 && missing === master.data.entries.length) {
    lines.push(warn('The index has NOT been implemented yet. 100% of entries are pending.'));
    warnings++;
  } else if (pct < 50) {
    lines.push(warn(`Coverage: ${matched}/${master.data.entries.length} (${pct.toFixed(1)}%)`));
    warnings++;
  } else {
    lines.push(pass(`Coverage: ${matched}/${master.data.entries.length} (${pct.toFixed(1)}%)`));
    passes++;
  }

  if (missingL1.length > 0) {
    lines.push(heading('Sample Missing L1 Entries'));
    for (const e of missingL1) {
      const cmd = e.sort_key ? `\\idxmath{${e.sort_key}}{${e.term}}` : `\\idx{${e.term}}`;
      lines.push(`  [p.${e.page.join(',')}] ${cmd}`);
    }
  }

  if (mathCheckIssues.length > 0) {
    lines.push(heading(`Math Sort-Key Audit (${mathMisuse} issues)`));
    for (const issue of mathCheckIssues.slice(0, 5)) {
      lines.push(warn(issue));
    }
    warnings += mathCheckIssues.length;
  }

  return { passes, failures, warnings, lines };
}

if (require.main === module) {
  const r = check();
  console.log(r.lines.join('\n'));
  process.exit(r.failures > 0 ? 1 : 0);
}

module.exports = { check };
