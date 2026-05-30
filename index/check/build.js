// Validate LaTeX build artifacts (.idx, .ind, .log)
const fs = require('fs');
const path = require('path');
const { PROJECT_ROOT, formatSection, heading, pass, fail, warn, info } = require('../utils');

function check() {
  const lines = [];
  let passes = 0, failures = 0, warnings = 0;

  lines.push(formatSection('Build Artifact Validation'));

  // ---- .idx file ----
  lines.push(heading('Topology_by_Munkres.idx'));
  const idxPath = path.join(PROJECT_ROOT, 'Topology_by_Munkres.idx');
  if (!fs.existsSync(idxPath)) {
    lines.push(warn('.idx file does not exist (not yet compiled)'));
    warnings++;
  } else {
    const idxContent = fs.readFileSync(idxPath, 'utf8');
    const idxLines = idxContent.split('\n').filter(l => l.trim());
    if (idxLines.length === 0) {
      lines.push(warn('.idx file is empty (0 entries) — index commands not yet added'));
      warnings++;
    } else {
      lines.push(pass(`.idx has ${idxLines.length} entries`));
      passes++;

      // Validate format: each line should be \indexentry{...}{page}
      let formatErrors = 0;
      for (const l of idxLines) {
        if (!/^\\indexentry\{/.test(l.trim())) {
          formatErrors++;
        }
      }
      if (formatErrors === 0) {
        lines.push(pass(`All ${idxLines.length} entries have valid \\indexentry format`));
        passes++;
      } else {
        lines.push(fail(`${formatErrors} entries have invalid format`));
        failures++;
      }
    }
  }

  // ---- .ind file ----
  lines.push(heading('Topology_by_Munkres.ind'));
  const indPath = path.join(PROJECT_ROOT, 'Topology_by_Munkres.ind');
  if (!fs.existsSync(indPath)) {
    lines.push(warn('.ind file does not exist (not yet built with makeindex)'));
    warnings++;
  } else {
    const indContent = fs.readFileSync(indPath, 'utf8');
    const l1Items = (indContent.match(/\\item /g) || []).length;
    const l2Items = (indContent.match(/\\subitem /g) || []).length;
    lines.push(info(`${l1Items} L1 items + ${l2Items} L2 items = ${l1Items + l2Items} total`));

    if (l1Items + l2Items === 0) {
      lines.push(warn('.ind is empty — rebuild with makeindex after adding commands'));
      warnings++;
    } else {
      lines.push(pass('.ind has rendered index entries'));
      passes++;
    }
  }

  // ---- .log file ----
  lines.push(heading('Topology_by_Munkres.log'));
  const logPath = path.join(PROJECT_ROOT, 'Topology_by_Munkres.log');
  if (!fs.existsSync(logPath)) {
    lines.push(warn('.log file does not exist (compile first)'));
    warnings++;
  } else {
    const log = fs.readFileSync(logPath, 'utf8');
    const errors = (log.match(/^!/gm) || []).length;
    const warningsInLog = (log.match(/Warning/g) || []).length;
    const idxWarnings = (log.match(/makeindex|index|MakeIndex/gi) || []).length;

    if (errors === 0) { lines.push(pass('0 LaTeX errors')); passes++; }
    else { lines.push(fail(`${errors} LaTeX errors found`)); failures++; }

    lines.push(info(`${warningsInLog} total warnings (harmless)`));
    if (idxWarnings === 0) lines.push(info('No makeindex-specific messages'));
  }

  return { passes, failures, warnings, lines };
}

if (require.main === module) {
  const r = check();
  console.log(r.lines.join('\n'));
  process.exit(r.failures > 0 ? 1 : 0);
}

module.exports = { check };
