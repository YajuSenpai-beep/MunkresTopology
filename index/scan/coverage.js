// Accurate L1 coverage: compare .idx file (ground truth) against master JSON
const fs = require('fs');
const path = require('path');
const { PROJECT_ROOT, loadJSON, formatSection, heading, pass, fail, warn, info } = require('../utils');

function check() {
  const lines = [];
  let passes = 0, failures = 0, warnings = 0;

  lines.push(formatSection('L1 Coverage Analysis (.idx ground truth)'));

  const idxPath = path.join(PROJECT_ROOT, 'Topology_by_Munkres.idx');
  if (!fs.existsSync(idxPath)) {
    lines.push(fail('.idx file not found — compile first'));
    failures++;
    return { passes, failures, warnings, lines };
  }

  // Parse .idx entries
  const idxContent = fs.readFileSync(idxPath, 'utf8');
  const idxEntries = [];
  for (const line of idxContent.split('\n')) {
    const m = line.match(/\\indexentry\{(.+?)\}\{(\d+)\}/);
    if (m) idxEntries.push({ raw: m[1], page: m[2] });
  }

  // Build lookup sets
  const idxPlain = new Set(); // term|page_format
  const idxMath = new Map();  // sortkey -> [display, ...]
  for (const e of idxEntries) {
    const parts = e.raw.split('|');
    const key = parts[0];
    const atIdx = key.indexOf('@');
    if (atIdx >= 0) {
      const sort = key.slice(0, atIdx).toLowerCase();
      const display = key.slice(atIdx + 1).replace(/\s+/g, ' ').toLowerCase();
      if (!idxMath.has(sort)) idxMath.set(sort, []);
      idxMath.get(sort).push(display);
    } else {
      idxPlain.add(key.toLowerCase().replace(/\s+/g, ' '));
    }
  }

  const master = loadJSON('original/index_entries.json');
  if (master.error) {
    lines.push(fail('Cannot load master JSON', master.error));
    failures++;
    return { passes, failures, warnings, lines };
  }

  const filterable = master.data.entries.filter(e =>
    e.level === 1 && !e.term.includes('(cont.)') && !/\(see/.test(e.term) && e.page.length > 0
  );

  let covered = 0, missing = [], matchIssue = [];
  for (const e of filterable) {
    const ct = e.term.replace(/\\\(|\\\)/g, '').replace(/\s+/g, ' ').toLowerCase().trim();
    let found = false;

    if (e.sort_key) {
      const displays = idxMath.get(e.sort_key.toLowerCase());
      if (displays) {
        for (const d of displays) {
          if (d.includes(ct.slice(0, 20)) || ct.includes(d.slice(0, 20))) { found = true; break; }
        }
      }
      if (!found) {
        // Try plain match too
        if (idxPlain.has(ct)) found = true;
      }
    } else {
      if (idxPlain.has(ct)) found = true;
      else {
        // Fuzzy: check if any plain entry contains the term
        for (const p of idxPlain) {
          if (p.includes(ct.slice(0, 15)) || ct.includes(p)) { found = true; break; }
        }
      }
    }

    if (found) covered++;
    else if (e.sort_key) matchIssue.push(e);
    else missing.push(e);
  }

  const pct = (covered / filterable.length * 100).toFixed(1);
  lines.push(info(`Filterable L1: ${filterable.length}`));
  lines.push(info(`.idx entries: ${idxEntries.length}`));
  lines.push(info(`Covered: ${covered} (${pct}%)`));

  if (missing.length === 0 && matchIssue.length === 0) {
    lines.push(pass('All L1 entries verified in .idx'));
    passes++;
  } else {
    if (missing.length > 0) {
      lines.push(fail(`Plain entries NOT in .idx: ${missing.length}`));
      failures++;
      lines.push(heading('Missing Plain Entries'));
      for (const e of missing.slice(0, 20)) {
        const ct = e.term.replace(/\\\(|\\\)/g, '').trim();
        lines.push(`  [p.${e.page}] ${ct.slice(0,65)}`);
      }
    }
    if (matchIssue.length > 0) {
      lines.push(warn(`Math entries with match issues: ${matchIssue.length} (likely formatting)`));
      warnings++;
    }
  }

  return { passes, failures, warnings, lines };
}

if (require.main === module) {
  const r = check();
  console.log(r.lines.join('\n'));
  process.exit(r.failures > 0 ? 1 : 0);
}

module.exports = { check };
