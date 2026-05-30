// Insert index commands into chapter .tex files
const fs = require('fs');
const path = require('path');
const { PROJECT_ROOT } = require('./utils');

function pad(n) { return n < 10 ? '0' + n : '' + n; }

function isInsideMath(content, pos) {
  const before = content.slice(Math.max(0, pos - 200), pos);
  let dollarCount = 0;
  for (let i = 0; i < before.length; i++) {
    if (before[i] === '\\') { i++; continue; }
    if (before[i] === '$') dollarCount++;
  }
  if (dollarCount % 2 === 1) return true;
  const openParen = (before.match(/\\\(/g) || []).length;
  const closeParen = (before.match(/\\\)/g) || []).length;
  if (openParen > closeParen) return true;
  const openBracket = (before.match(/\\\[/g) || []).length;
  const closeBracket = (before.match(/\\\]/g) || []).length;
  if (openBracket > closeBracket) return true;
  return false;
}

function findInsertPoint(content, term, allowMath) {
  let search = term
    .replace(/\\\(/g, '').replace(/\\\)/g, '')
    .replace(/\\[a-zA-Z]+(\{[^}]*\})?/g, '')
    .replace(/[{}]/g, '')
    .trim();

  if (search.length < 2) {
    const raw = term.replace(/\\\(|\\\)/g, '');
    return content.indexOf(raw);
  }

  const lowerContent = content.toLowerCase();
  const lowerSearch = search.toLowerCase();
  let idx = 0;
  while (idx < lowerContent.length) {
    idx = lowerContent.indexOf(lowerSearch, idx);
    if (idx === -1) return -1;

    const before = content.slice(Math.max(0, idx - 50), idx);
    if (before.endsWith('\\')) { idx += search.length; continue; }
    // Skip if inside a LaTeX command name (e.g., \includegraphics)
    const cmdMatch = before.match(/\\([a-zA-Z@]+)$/);
    if (cmdMatch) { idx += search.length; continue; }
    // Skip if right after a LaTeX command name with no braces yet
    if (/\\[a-zA-Z@]+\s*$/.test(before)) { idx += search.length; continue; }
    const openBefore = (before.match(/\{/g) || []).length;
    const closeBefore = (before.match(/\}/g) || []).length;
    if (openBefore > closeBefore) { idx += search.length; continue; }
    if (!allowMath && isInsideMath(content, idx)) { idx += search.length; continue; }
    return idx;
  }
  return -1;
}

function insertForChapter(chNum, sourceDir, dryRun, l1Only) {
  const jsonFile = path.join(PROJECT_ROOT, 'index', 'data', `ch${pad(chNum)}_entries.json`);
  let data = JSON.parse(fs.readFileSync(jsonFile, 'utf8'));
  if (l1Only) data = data.filter(e => e.level === 1);
  data = data.filter(e => {
    const t = e.term;
    if (t.includes('(cont.)')) return false;
    if (/\(see\s/.test(t)) return false;
    if (/\(see also\s/.test(t)) return false;
    if (e.page.length === 0) return false;
    return true;
  });

  const texFiles = fs.readdirSync(sourceDir).filter(f =>
    f.startsWith(`Chapter_${chNum}_`) && f.endsWith('.tex')
  );
  if (texFiles.length === 0) return { error: 'no tex file for chapter ' + chNum };

  const texPath = path.join(sourceDir, texFiles[0]);
  let content = fs.readFileSync(texPath, 'utf8');
  const report = { file: texFiles[0], total: data.length, inserted: 0, skipped: 0, notFound: [] };

  // Phase 1: find all insertion points on original content
  const operations = [];

  for (const e of data) {
    let insertPos = -1, replaceLen = 0, cmd = '';

    if (e.level === 1 && e.sort_key) {
      const rawLatex = e.term.replace(/\\\(|\\\)/g, '');
      const latexOnly = rawLatex.split(/\s*[\(\[]/)[0].trim();
      const styShortcuts = {
        '\\mathbb{R}': ['\\R', '\\RR'], '\\mathbb{N}': ['\\N', '\\NN'],
        '\\mathbb{Z}': ['\\Z', '\\ZZ'], '\\mathbb{Q}': ['\\Q', '\\QQ'],
        '\\mathbb{C}': ['\\C', '\\CC'],
      };
      const aliases = styShortcuts[latexOnly] || [];
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
      if (insertPos < 0) {
        const wordMap = {
          'Inf A': 'infimum', 'Sup A': 'supremum',
          'Int A': 'interior of', 'Bd A': 'boundary of', 'Cl A': 'closure of',
        };
        const plain = latexOnly.replace(/\\[a-zA-Z]+(\{[^}]*\})?/g, '').replace(/[{}]/g, '').trim();
        const alt = wordMap[plain];
        if (alt) {
          insertPos = findInsertPoint(content, alt);
          if (insertPos >= 0) { cmd = `\\idxmath{${e.sort_key}}{${e.term}}`; replaceLen = 0; }
        }
      }
    } else if (e.level === 1) {
      // CRITICAL: entries with sort_key must NOT use plain \idx

      const searchTerm = e.term.replace(/\\\(|\\\)/g, '').replace(/\\[a-zA-Z]+(\{[^}]*\})?/g, '').replace(/[{}]/g, '').trim();

      if (e.sort_key) continue;
      if (/[_^@!|"]/.test(searchTerm)) continue;
      const l1Aliases = {
        'Counterimage': ['counterimage', 'preimage', 'inverse image'],
        'Inf A': ['infimum'], 'Sup A': ['supremum'],
        'Bd A': ['boundary of'], 'Int A': ['interior of'],
        'First-countability': ['first-countable', 'first countable', 'first axiom'],
        'Second-countability': ['second-countable', 'second countable', 'second axiom'],
        'Hilbert cube': ['hilbert cube'],
        'Bicompactness': ['bicompact', 'bicompactness'],
        'Perfect map': ['perfect map'],
        'Cofinal': ['cofinal'],
        'Curve': ['simple closed curve', 'peano curve'],
        'Directed set': ['directed set'],
        'Line with two origins': ['two origins', 'line with two origins'],
        'Net': ['a net ', 'convergent net'],
        'Subnet': ['subnet'],
        'Stone-Čech compactification': ['stone-\\v{C}ech', 'stone-čech', 'stone-Cech', 'cech compactification'],
        'Functor': ['functor'],
        'Normalizer': ['normalizer', 'normaliser'],
        'Cone': ['mapping cone', 'cone over', 'cone'],
        'CW complex': ['cw complex', 'cw-complex'],
        'Clockwise loop': ['clockwise', 'clock-wise'],
        'Star-convex set': ['star-convex', 'star convex'],
        'Zermelo': ['zermelo'],
        'Tower': ['tower'],
        '2-cell': ['2-cell', 'two-cell', 'adjoining a 2-cell'],
        '2-manifold': ['2-manifold', 'two-manifold'],
        '2-manifold with boundary': ['surface with boundary', '2-manifold with boundary'],
        'Ball, unit': ['unit ball'],
        'm -fold projective plane': ['m-fold projective plane', 'projective plane'],
        'n -fold torus': ['n-fold torus'],
        'T_i axioms': ['separation axioms', 't_i axioms'],
      };

      let pos = findInsertPoint(content, searchTerm);
      if (pos < 0 && l1Aliases[searchTerm]) {
        for (const alias of l1Aliases[searchTerm]) {
          pos = findInsertPoint(content, alias);
          if (pos >= 0) break;
        }
      }
      if (pos < 0 && searchTerm.length > 5) {
        const keywords = searchTerm.split(/[\s,;:.()]+/).filter(w => w.length >= 5);
        for (const kw of keywords) {
          pos = findInsertPoint(content, kw);
          if (pos >= 0) { cmd = `\\idx{${searchTerm}}`; insertPos = pos; replaceLen = 0; break; }
        }
      }
      if (cmd === '' && pos >= 0) {
        const atPos = content.slice(pos, pos + searchTerm.length);
        if (atPos.toLowerCase() === searchTerm.toLowerCase()) {
          cmd = `\\idx{${atPos}}`;
          insertPos = pos;
          replaceLen = searchTerm.length;
        } else {
          cmd = `\\idx{${searchTerm}}`;
          insertPos = pos;
          replaceLen = 0;
        }
      }
    } else if (e.level === 2) {
      cmd = `\\idxsub{${e.parent}}{${e.term}}`;
      const termClean = e.term.replace(/\\\(|\\\)/g, '').replace(/\\[a-zA-Z]+(\{[^}]*\})?/g, '').replace(/[{}]/g, '').trim();
      const parentClean = e.parent.replace(/\\\(|\\\)/g, '').replace(/\\[a-zA-Z]+(\{[^}]*\})?/g, '').replace(/[{}]/g, '').trim();
      let pIdx = -1, searchFrom = 0;
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
        let tIdx = lcVicinity.indexOf(lcTerm);
        if (tIdx < 0 && lcTerm.length > 5) {
          const keywords = lcTerm.split(/\s+/).filter(w => w.length >= 4);
          for (const kw of keywords) { const ki = lcVicinity.indexOf(kw); if (ki >= 0) { tIdx = ki; break; } }
        }
        if (tIdx >= 0 && tIdx < 3000) {
          insertPos = pIdx + tIdx; replaceLen = 0;
        } else {
          const paraSep = content.includes('\r\n') ? '\r\n\r\n' : '\n\n';
          const paraEnd = content.indexOf(paraSep, pIdx);
          if (paraEnd >= 0 && paraEnd - pIdx < 3000) {
            const nearEnd = content.slice(Math.max(0, paraEnd - 100), paraEnd + 20);
            if (!/\\idx\{|\\idxsub\{|\\idxmath\{/.test(nearEnd)) {
              insertPos = paraEnd; replaceLen = 0;
            }
          }
        }
      } else {
        const lcTerm = termClean.toLowerCase();
        const cIdx = lcContent.indexOf(lcTerm);
        if (cIdx >= 0) { insertPos = cIdx; replaceLen = 0; }
        else if (lcTerm.length > 5) {
          const keywords = lcTerm.split(/\s+/).filter(w => w.length >= 4);
          for (const kw of keywords) { const ki = lcContent.indexOf(kw); if (ki >= 0) { insertPos = ki; replaceLen = 0; break; } }
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

  // Phase 2: remove overlaps and apply from end to start
  operations.sort((a, b) => b.pos - a.pos);
  const deduped = [], clustered = [];
  for (const op of operations) {
    let overlaps = false;
    for (const d of deduped) {
      const opEnd = op.pos + Math.max(op.replaceLen, 1);
      const dEnd = d.pos + Math.max(d.replaceLen, 1);
      if (op.pos < dEnd && opEnd > d.pos) { overlaps = true; break; }
    }
    if (overlaps) clustered.push(op);
    else deduped.push(op);
  }
  report.inserted = deduped.length;
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

if (require.main === module) {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  const l1Only = args.includes('--l1-only');
  const targetDir = args.includes('--chapters') ? 'chapters' : 'chapters_backup';
  const chNum = parseInt(args.find(a => /^\d+$/.test(a)) || '5');
  console.log(`\nInserting ${l1Only ? 'L1 ' : ''}index commands into Chapter ${chNum} (${dryRun ? 'DRY RUN' : 'LIVE'}, target: ${targetDir}/)...\n`);
  const report = insertForChapter(chNum, path.join(PROJECT_ROOT, targetDir), dryRun, l1Only);
  if (report.error) { console.log('ERROR: ' + report.error); }
  else {
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
