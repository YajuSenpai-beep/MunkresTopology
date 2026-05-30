// Scan .tex chapter files for \idx, \idxsub, \idxmath commands
const fs = require('fs');
const path = require('path');
const { PROJECT_ROOT, extractCommands, formatSection, heading, pass, warn, fail } = require('../utils');

function check() {
  const lines = [];
  let passes = 0, failures = 0, warnings = 0;

  lines.push(formatSection('Index Command Scan'));

  const chaptersDir = path.join(PROJECT_ROOT, 'chapters');
  const titleMap = {
    'Chapter_1': 'Set Theory and Logic',
    'Chapter_2': 'Topological Spaces and Continuous Functions',
    'Chapter_3': 'Connectedness and Compactness',
    'Chapter_4': 'Countability and Separation Axioms',
    'Chapter_5': 'The Tychonoff Theorem',
    'Chapter_6': 'Metrization Theorems and Paracompactness',
    'Chapter_7': 'Complete Metric Spaces and Function Spaces',
    'Chapter_8': 'Baire Spaces and Dimension Theory',
    'Chapter_9': 'The Fundamental Group',
    'Chapter_10': 'Separation Theorems in the Plane',
    'Chapter_11': 'The Seifert-van Kampen Theorem',
    'Chapter_12': 'Classification of Surfaces',
    'Chapter_13': 'Classification of Covering Spaces',
    'Chapter_14': 'Applications to Group Theory',
  };

  let totalIdx = 0, totalIdxsub = 0, totalIdxmath = 0;

  for (let ch = 1; ch <= 14; ch++) {
    const chNum = ch < 10 ? '0' + ch : ch;
    const chapterKey = `Chapter_${ch < 10 ? ch : chNum}`;
    // Try both naming patterns
    let filename = null;
    const files = fs.readdirSync(chaptersDir);
    for (const f of files) {
      if (f.startsWith(`Chapter_${ch}_`) || (ch < 10 && f.startsWith(`Chapter_${ch}_`))) {
        filename = f;
        break;
      }
    }
    if (!filename) {
      lines.push(fail(`Chapter ${ch}: file not found`));
      failures++;
      continue;
    }

    const content = fs.readFileSync(path.join(chaptersDir, filename), 'utf8');
    const cmds = extractCommands(content);

    const shortTitle = titleMap[chapterKey] || '';
    const label = `Chapter ${String(ch).padStart(2)}`.padEnd(12) + shortTitle;

    const count = cmds.idx.length + cmds.idxsub.length + cmds.idxmath.length;
    if (count === 0) {
      lines.push(warn(label.padEnd(65) + `0 idx, 0 idxsub, 0 idxmath`));
      warnings++;
    } else {
      lines.push(pass(label.padEnd(65) + `${cmds.idx.length} idx, ${cmds.idxsub.length} idxsub, ${cmds.idxmath.length} idxmath`));
      passes++;
    }

    totalIdx += cmds.idx.length;
    totalIdxsub += cmds.idxsub.length;
    totalIdxmath += cmds.idxmath.length;
  }

  const grandTotal = totalIdx + totalIdxsub + totalIdxmath;
  lines.push('  ' + '-'.repeat(70));
  lines.push(heading(`Total: ${totalIdx} idx + ${totalIdxsub} idxsub + ${totalIdxmath} idxmath = ${grandTotal} commands`));
  lines.push(warn(`Expected target (master JSON): 1418 entries (685 L1 + 733 L2)`));
  lines.push(warn(`Implementation progress: ${grandTotal}/1418 (${(grandTotal/1418*100).toFixed(1)}%)`));

  return { passes, failures, warnings, lines };
}

if (require.main === module) {
  const r = check();
  console.log(r.lines.join('\n'));
  process.exit(0); // zero commands is WARN, not failure
}

module.exports = { check };
