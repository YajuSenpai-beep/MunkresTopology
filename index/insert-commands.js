// Insert index commands into chapter .tex files
// Reads per-chapter JSON and wraps first occurrence of each term with \idx{...}
const fs = require('fs');
const path = require('path');
const { PROJECT_ROOT } = require('./utils');

function pad(n) { return n < 10 ? '0' + n : '' + n; }

function findInsertPoint(content, term) {
  // Strip LaTeX math delimiters for searching, keep the raw search term
  let search = term
    .replace(/\\\(/g, '').replace(/\\\)/g, '')
    .replace(/\\[a-zA-Z]+(\{[^}]*\})?/g, '')
    .replace(/[{}]/g, '')
    .trim();

  // For very short terms (math symbols), try exact match
  if (search.length < 2) {
    const raw = term.replace(/\\\(|\\\)/g, '');
    return content.indexOf(raw);
  }

  // Find first significant occurrence (case-insensitive)
  const lowerContent = content.toLowerCase();
  const lowerSearch = search.toLowerCase();

  let idx = 0;
  while (idx < lowerContent.length) {
    idx = lowerContent.indexOf(lowerSearch, idx);
    if (idx === -1) return -1;

    // Check we're not inside a LaTeX command
    const before = content.slice(Math.max(0, idx - 50), idx);
    const after = content.slice(idx, Math.min(content.length, idx + search.length + 10));

    // Skip if inside \begin{theorem}[...], \section{...}, \chapter{...}, \caption{...}
    if (/\\begin\{[^}]*\}\s*$/.test(before) || /^\s*[}\]]/.test(after.slice(search.length))) {
      idx += search.length;
      continue;
    }
    // Skip if right after \ (inside a command)
    if (before.endsWith('\\')) { idx += search.length; continue; }
    // Skip if inside braces
    const openBefore = (before.match(/\{/g) || []).length;
    const closeBefore = (before.match(/\}/g) || []).length;
    if (openBefore > closeBefore) { idx += search.length; continue; }

    return idx;
  }
  return -1;
}

function insertForChapter(chNum, sourceDir, dryRun, l1Only) {
  const jsonFile = path.join(PROJECT_ROOT, 'index', 'data', `ch${pad(chNum)}_entries.json`);
  let data = JSON.parse(fs.readFileSync(jsonFile, 'utf8'));
  if (l1Only) data = data.filter(e => e.level === 1);
  // Skip organizational entries that don't represent actual text
  data = data.filter(e => {
    const t = e.term;
    if (t.includes('(cont.)')) return false;       // continuation marker
    if (/\(see\s/.test(t)) return false;            // cross-reference
    if (/\(see also\s/.test(t)) return false;        // cross-reference
    if (e.page.length === 0) return false;           // empty page (organizational)
    return true;
  });

  const texFiles = fs.readdirSync(sourceDir).filter(f =>
    f.startsWith(`Chapter_${chNum}_`) && f.endsWith('.tex')
  );
  if (texFiles.length === 0) return { error: 'no tex file for chapter ' + chNum };

  const texPath = path.join(sourceDir, texFiles[0]);
  let content = fs.readFileSync(texPath, 'utf8');

  const report = { file: texFiles[0], total: data.length, inserted: 0, skipped: 0, notFound: [] };

  // Phase 1: find all insertion points (on the ORIGINAL content)
  const operations = [];

  for (const e of data) {
    let insertPos = -1;
    let replaceLen = 0;
    let cmd = '';

    if (e.level === 1 && e.sort_key) {
      // Math symbol: extract just the LaTeX symbol part (before any parenthetical)
      const rawLatex = e.term.replace(/\\\(|\\\)/g, '');
      const latexOnly = rawLatex.split(/\s*[\(\[]/)[0].trim(); // just the symbol, no description
      // Map common .sty shortcuts to their LaTeX equivalents for searching
      const styShortcuts = {
        '\\mathbb{R}': ['\\R', '\\RR'], '\\mathbb{N}': ['\\N', '\\NN'],
        '\\mathbb{Z}': ['\\Z', '\\ZZ'], '\\mathbb{Q}': ['\\Q', '\\QQ'],
        '\\mathbb{C}': ['\\C', '\\CC'],
      };
      const aliases = styShortcuts[latexOnly] || [];

      // Try: latexOnly, sty shortcuts, no-braces
      const patterns = [latexOnly, ...aliases, latexOnly.replace(/[{}]/g, '')];
      for (const pat of patterns) {
        if (pat.length < 2) continue;
        insertPos = content.indexOf(pat);
        if (insertPos >= 0) break;
      }
      if (insertPos >= 0) {
        cmd = `\\idxmath{${e.sort_key}}{${e.term}}`;
        replaceLen = 0;
      }

      // For abbreviated symbols like "Inf A", "Sup A", try full words
      if (insertPos < 0) {
        const wordMap = {
          'Inf A': 'infimum', 'Sup A': 'supremum',
          'Int A': 'interior of', 'Bd A': 'boundary of',
          'Cl A': 'closure of',
        };
        const plain = latexOnly.replace(/\\[a-zA-Z]+(\{[^}]*\})?/g, '').replace(/[{}]/g, '').trim();
        const alt = wordMap[plain];
        if (alt) {
          insertPos = findInsertPoint(content, alt);
          if (insertPos >= 0) { cmd = `\\idxmath{${e.sort_key}}{${e.term}}`; replaceLen = 0; }
        }
      }
    } else if (e.level === 1) {
      const searchTerm = e.term.replace(/\\\(|\\\)/g, '').replace(/\\[a-zA-Z]+(\{[^}]*\})?/g, '').replace(/[{}]/g, '').trim();
      let pos = findInsertPoint(content, searchTerm);

      // If full term not found, try keyword matching
      if (pos < 0 && searchTerm.length > 5) {
        const keywords = searchTerm.split(/[\s,;:.()]+/).filter(w => w.length >= 5);
        for (const kw of keywords) {
          pos = findInsertPoint(content, kw);
          if (pos >= 0) {
            // Use the keyword match position to insert \idx{searchTerm}
            cmd = `\\idx{${searchTerm}}`;
            insertPos = pos;
            replaceLen = 0;
            break;
          }
        }
      }

      if (cmd === '' && pos >= 0) {
        const matched = content.slice(pos, pos + searchTerm.length);
        cmd = `\\idx{${matched}}`;
        insertPos = pos;
        replaceLen = searchTerm.length;
      }
    } else if (e.level === 2) {
      cmd = `\\idxsub{${e.parent}}{${e.term}}`;
      const termClean = e.term.replace(/\\\(|\\\)/g, '').replace(/\\[a-zA-Z]+(\{[^}]*\})?/g, '').replace(/[{}]/g, '').trim();

      // Strategy 1: find parent, then look for child term nearby
      const parentClean = e.parent.replace(/\\\(|\\\)/g, '').replace(/\\[a-zA-Z]+(\{[^}]*\})?/g, '').replace(/[{}]/g, '').trim();
      // Use LAST occurrence of parent (detailed discussion is usually later in chapter)
      let pIdx = -1;
      let searchFrom = 0;
      const lcContent = content.toLowerCase();
      const lcParent = parentClean.toLowerCase();
      while (true) {
        const next = lcContent.indexOf(lcParent, searchFrom);
        if (next < 0) break;
        pIdx = next;
        searchFrom = next + 1;
      }

      if (pIdx >= 0) {
        const vicinity = content.slice(pIdx, Math.min(content.length, pIdx + 6000));
        const lcVicinity = vicinity.toLowerCase();
        const lcTerm = termClean.toLowerCase();

        // Try exact child term match
        let tIdx = lcVicinity.indexOf(lcTerm);
        // If not exact, try matching key words (3+ chars) from child term
        if (tIdx < 0 && lcTerm.length > 5) {
          const keywords = lcTerm.split(/\s+/).filter(w => w.length >= 4);
          for (const kw of keywords) {
            const ki = lcVicinity.indexOf(kw);
            if (ki >= 0) { tIdx = ki; break; }
          }
        }

        if (tIdx >= 0 && tIdx < 3000) {
          insertPos = pIdx + tIdx;
          replaceLen = 0;
        } else {
          // Fallback: paragraph end after parent (with anti-clustering)
          const paraSep = content.includes('\r\n') ? '\r\n\r\n' : '\n\n';
          const paraEnd = content.indexOf(paraSep, pIdx);
          if (paraEnd >= 0 && paraEnd - pIdx < 3000) {
            const nearEnd = content.slice(Math.max(0, paraEnd - 100), paraEnd + 20);
            if (!/\\idx\{|\\idxsub\{|\\idxmath\{/.test(nearEnd)) {
              insertPos = paraEnd;
              replaceLen = 0;
            }
          }
        }
      } else {
        // Strategy 2: parent not found (may be in different chapter)
        // Try to find the child term itself anywhere in the text
        const lcContent = content.toLowerCase();
        const lcTerm = termClean.toLowerCase();
        const cIdx = lcContent.indexOf(lcTerm);
        if (cIdx >= 0) {
          insertPos = cIdx;
          replaceLen = 0;
        } else if (lcTerm.length > 5) {
          // Try keyword matching
          const keywords = lcTerm.split(/\s+/).filter(w => w.length >= 4);
          for (const kw of keywords) {
            const ki = lcContent.indexOf(kw);
            if (ki >= 0) { insertPos = ki; replaceLen = 0; break; }
          }
        }
      }
    }

    if (insertPos >= 0 && cmd) {
      operations.push({ pos: insertPos, replaceLen, cmd });
    } else {
      report.notFound.push({ level: e.level, term: e.term.slice(0, 60), parent: e.parent || '' });
      report.skipped++;
    }
  }

  // Phase 2: deduplicate positions and apply from END to START
  operations.sort((a, b) => b.pos - a.pos);

  // Deduplicate: if multiple ops share same position, only keep first
  const seenPos = new Set();
  const deduped = [];
  const clustered = [];
  for (const op of operations) {
    if (seenPos.has(op.pos)) {
      clustered.push(op);
    } else {
      seenPos.add(op.pos);
      deduped.push(op);
    }
  }
  report.inserted = deduped.length;
  // Move clustered back to notFound
  for (const op of clustered) {
    report.notFound.push({ level: 0, term: '(clustered) ' + op.cmd.slice(0, 60), parent: '' });
    report.skipped++;
  }

  if (!dryRun) {
    for (const op of deduped) {
      if (op.replaceLen > 0) {
        content = content.slice(0, op.pos) + op.cmd + content.slice(op.pos + op.replaceLen);
      } else {
        content = content.slice(0, op.pos) + op.cmd + ' ' + content.slice(op.pos);
      }
    }
    fs.writeFileSync(texPath, content);
  }

  return report;
}

// ---- Main ----
if (require.main === module) {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  const l1Only = args.includes('--l1-only');
  const targetDir = args.includes('--chapters') ? 'chapters' : 'chapters_backup';
  const chNum = parseInt(args.find(a => /^\d+$/.test(a)) || '5');

  console.log(`\nInserting ${l1Only ? 'L1 ' : ''}index commands into Chapter ${chNum} (${dryRun ? 'DRY RUN' : 'LIVE'}, target: ${targetDir}/)...\n`);

  const report = insertForChapter(chNum, path.join(PROJECT_ROOT, targetDir), dryRun, l1Only);

  if (report.error) {
    console.log('ERROR: ' + report.error);
  } else {
    console.log(`File: ${report.file}`);
    console.log(`Total entries: ${report.total}`);
    console.log(`Inserted: ${report.inserted}`);
    console.log(`Skipped (not found): ${report.skipped}`);
    if (report.notFound.length > 0) {
      console.log(`\nNot found:`);
      for (const nf of report.notFound) {
        console.log(`  L${nf.level} "${nf.term}"${nf.parent ? ' under "' + nf.parent + '"' : ''}`);
      }
    }
    if (dryRun) console.log('\n(DRY RUN — no files modified)');
  }
}

module.exports = { insertForChapter, findInsertPoint };
