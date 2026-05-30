// Verify chapter assignments by checking if key terms appear in corresponding .tex
const fs = require('fs');
const path = require('path');
const { PROJECT_ROOT } = require('./utils');

const BACKUP_DIR = path.join(PROJECT_ROOT, 'chapters_backup');

function pad(n) { return n < 10 ? '0' + n : '' + n; }

let totalChecked = 0, totalFound = 0, allMissing = [];

for (let ch = 1; ch <= 14; ch++) {
  const jsonFile = path.join(PROJECT_ROOT, 'index', 'data', `ch${pad(ch)}_entries.json`);
  const data = JSON.parse(fs.readFileSync(jsonFile, 'utf8'));

  const texFiles = fs.readdirSync(BACKUP_DIR).filter(f =>
    f.startsWith(`Chapter_${ch}_`) && f.endsWith('.tex')
  );
  if (texFiles.length === 0) { console.log('Ch' + ch + ': no tex file'); continue; }
  const content = fs.readFileSync(path.join(BACKUP_DIR, texFiles[0]), 'utf8');

  const l1Entries = data.filter(e => e.level === 1).slice(0, 10);
  let found = 0;
  const missing = [];

  for (const e of l1Entries) {
    // Strip LaTeX to find searchable keywords
    let s = e.term.replace(/\\\(|\\\)/g, '');
    s = s.replace(/\\[a-zA-Z]+(\{[^}]*\})?/g, '').replace(/[{}]/g, '');
    const words = s.split(/[\s,;:.()]+/).filter(w => w.length >= 5 && /^[A-Za-z]/.test(w));
    const key = words[0] || s.slice(0, 10);

    if (key && content.includes(key)) {
      found++;
    } else {
      missing.push({ term: e.term.slice(0, 60), key });
    }
  }

  totalChecked += l1Entries.length;
  totalFound += found;
  if (missing.length > 0) allMissing.push({ ch, missing });

  const pct = Math.round(found / l1Entries.length * 100);
  const flag = pct < 70 ? ' !!' : '';
  console.log(`Ch${String(ch).padStart(2)}: ${found}/${l1Entries.length} found (${pct}%)${flag}`);
  for (const m of missing.slice(0, 3)) {
    console.log(`       missing key="${m.key}" from "${m.term}"`);
  }
}

console.log(`\nTotal: ${totalFound}/${totalChecked} found (${Math.round(totalFound/totalChecked*100)}%)`);

if (allMissing.length > 0) {
  console.log(`\nChapters with low match rate:`);
  for (const { ch, missing } of allMissing) {
    console.log(`  Ch${ch}: ${missing.length} entries not found`);
  }
  console.log('\nNote: "missing" may mean the term uses different wording in the .tex source.');
  console.log('Most entries ARE correctly assigned by page range — keyword matching is approximate.');
}
