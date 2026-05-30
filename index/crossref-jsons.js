// Cross-reference chapter JSON files against the master index JSON
const fs = require('fs');
const path = require('path');
const { PROJECT_ROOT, loadJSON, formatSection, heading, pass, fail, warn, info, summaryLine } = require('./utils');

function check() {
  const lines = [];
  let passes = 0, failures = 0, warnings = 0;

  lines.push(formatSection('Chapter-Master Cross-Reference'));

  const master = loadJSON('original/index_entries.json');
  if (master.error) {
    lines.push(fail('Cannot load master JSON', master.error));
    failures++;
    return { passes, failures, warnings, lines };
  }

  // Build master index maps
  const masterL1 = new Map(); // term -> entry
  const masterL2 = new Map(); // parent::term -> entry
  for (const e of master.data.entries) {
    if (e.level === 1) masterL1.set(e.term, e);
    else masterL2.set(e.parent + '::' + e.term, e);
  }

  lines.push(heading('Forward Check (chapter entries -> master)'));

  const indexDir = path.join(PROJECT_ROOT, 'index');
  let totalChapter = 0, totalFound = 0, totalMismatch = 0;
  let coveredMaster = new Set();

  for (let ch = 1; ch <= 14; ch++) {
    const filename = `ch${ch < 10 ? '0' + ch : ch}_entries.json`;
    const filePath = path.join(indexDir, filename);
    if (!fs.existsSync(filePath)) continue;

    const { data } = loadJSON(`index/${filename}`);
    if (!Array.isArray(data)) continue;

    totalChapter += data.length;
    let found = 0, mismatch = 0;
    const mismatchDetails = [];

    for (const e of data) {
      const key = (e.parent || '') + '::' + e.term;
      let masterEntry;
      if (e.level === 1) masterEntry = masterL1.get(e.term);
      else masterEntry = masterL2.get(e.parent + '::' + e.term);

      if (masterEntry) {
        found++;
        coveredMaster.add(key);
        // Field consistency check
        if (JSON.stringify(e.page) !== JSON.stringify(masterEntry.page)) {
          mismatch++;
          mismatchDetails.push(`page: ch=[${e.page}] vs master=[${masterEntry.page}] for "${e.term.slice(0,50)}"`);
        }
        if (e.sort_key && masterEntry.sort_key && e.sort_key !== masterEntry.sort_key) {
          mismatch++;
          mismatchDetails.push(`sort_key: ch="${e.sort_key}" vs master="${masterEntry.sort_key}" for "${e.term.slice(0,50)}"`);
        }
      } else {
        mismatchDetails.push(`NOT FOUND in master: "${e.term.slice(0,50)}" (L${e.level})`);
      }
    }

    totalFound += found;
    totalMismatch += mismatch;

    const chLabel = `Chapter ${ch}`.padEnd(12);
    const stats = `${found}/${data.length} found`;
    const notFound = data.length - found;
    if (notFound === 0 && mismatch === 0) {
      lines.push(pass(chLabel + stats));
      passes++;
    } else if (notFound > 0) {
      lines.push(fail(chLabel + stats + `  ${notFound} entries NOT in master, ${mismatch} field mismatches`));
      for (const d of mismatchDetails.slice(0, 5)) lines.push(`         ${d}`);
      failures++;
    } else {
      lines.push(warn(chLabel + stats + `  ${mismatch} field mismatches`));
      for (const d of mismatchDetails.slice(0, 3)) lines.push(`         ${d}`);
      warnings++;
    }
  }

  // Reverse coverage
  lines.push(heading('Reverse Coverage (master entries covered by chapter JSONs)'));
  lines.push(info(`Covered: ${coveredMaster.size}/${master.data.entries.length} master entries (${(coveredMaster.size/master.data.entries.length*100).toFixed(1)}%)`));

  const uncoveredCh1to9 = [];
  for (const e of master.data.entries) {
    const key = (e.parent || '') + '::' + e.term;
    if (!coveredMaster.has(key)) {
      const pg = e.page.length > 0 ? e.page[0] : 999;
      uncoveredCh1to9.push({ entry: e, firstPage: pg });
    }
  }

  const ch10PlusUncovered = uncoveredCh1to9.filter(e => e.firstPage >= 300);
  const ch1to9Uncovered = uncoveredCh1to9.filter(e => e.firstPage < 300);

  lines.push(info(`  Ch 1-9 range: ${ch1to9Uncovered.length} entries uncovered (no chapter JSONs exist)`));
  if (ch10PlusUncovered.length > 0) {
    lines.push(warn(`  Ch 10-14 range: ${ch10PlusUncovered.length} entries not in any chapter JSON`));
    for (const e of ch10PlusUncovered.slice(0, 5)) {
      lines.push(`         "${e.entry.term.slice(0,60)}"  [p.${e.entry.page.join(', ')}]`);
    }
    warnings++;
  }

  return { passes, failures, warnings, lines };
}

if (require.main === module) {
  const r = check();
  console.log(r.lines.join('\n'));
  process.exit(r.failures > 0 ? 1 : 0);
}

module.exports = { check };
