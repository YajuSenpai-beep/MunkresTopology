// Compare index_entries.json against parsed index.pdf (MinerU output)
const fs = require('fs');
const path = require('path');
const { PROJECT_ROOT, loadJSON, formatSection, heading, pass, fail, warn, info } = require('../utils');

// Aggressive LaTeX-to-plain-text normalization for fuzzy matching
function toPlain(text) {
  let t = text;
  // Remove common LaTeX commands, keeping their content
  t = t.replace(/\\widehat\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}/g, '$1');
  t = t.replace(/\\widetilde\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}/g, '$1');
  t = t.replace(/\\mathbf\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}/g, '$1');
  t = t.replace(/\\mathbb\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}/g, '$1');
  t = t.replace(/\\mathcal\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}/g, '$1');
  t = t.replace(/\\text\w*\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}/g, '$1');
  t = t.replace(/\\pmb\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}/g, '$1');
  t = t.replace(/\\bar\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}/g, '$1');
  t = t.replace(/\\overline\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}/g, '$1');
  t = t.replace(/\\boldsymbol\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}/g, '$1');
  t = t.replace(/\\left\w*/g, '');
  t = t.replace(/\\right\w*/g, '');
  // Remove LaTeX math delimiters
  t = t.replace(/\\\(/g, '').replace(/\\\)/g, '');
  // Remove remaining LaTeX commands (\command or \command{...})
  t = t.replace(/\\[a-zA-Z]+(\s*\{[^}]*\})?/g, '');
  // Remove braces, brackets
  t = t.replace(/[{}]/g, '');
  t = t.replace(/\\lbrack /g, '[').replace(/\\rbrack /g, ']');
  // Collapse whitespace, lowercase for comparison
  t = t.replace(/\s+/g, ' ').trim().toLowerCase();
  // Remove trailing periods, commas
  t = t.replace(/[,.\s]+$/g, '');
  // Normalize diacritics (OCR often strips them)
  t = t.replace(/ö/g, 'o').replace(/ü/g, 'u').replace(/ä/g, 'a');
  t = t.replace(/č/g, 'c').replace(/ř/g, 'r').replace(/š/g, 's');
  // Remove ^ and _ (subscript/superscript markers lost in OCR)
  t = t.replace(/\^/g, '').replace(/_/g, '');
  return t;
}

// Also strip from PDF text
function toPlainPdf(text) {
  let t = text;
  // Remove markdown heading markers
  t = t.replace(/^##\s*[A-Z]\s*$/gm, '');
  // Remove math $...$ patterns from OCR
  t = t.replace(/\$[^$]*\$/g, (m) => {
    const inner = m.slice(1, -1);
    return toPlain(inner);
  });
  // Remove backslash-escaped chars
  t = t.replace(/\\([{}])/g, '$1');
  // Collapse
  t = t.replace(/\s+/g, ' ').trim().toLowerCase();
  // Diacritics and markers
  t = t.replace(/ö/g, 'o').replace(/ü/g, 'u').replace(/ä/g, 'a');
  t = t.replace(/č/g, 'c').replace(/ř/g, 'r').replace(/š/g, 's');
  t = t.replace(/\^/g, '').replace(/_/g, '');
  return t;
}

// Check if needle is found in haystack with some fuzziness
// Uses trigram overlap >= 70% as "fuzzy match"
function fuzzyIncludes(haystack, needle) {
  if (haystack.includes(needle)) return true;
  if (needle.length < 5) return false;
  // Check if 70% of trigrams from needle appear in haystack
  const tri = new Set();
  for (let i = 0; i <= needle.length - 3; i++) {
    tri.add(needle.slice(i, i + 3));
  }
  if (tri.size === 0) return false;
  let found = 0;
  for (const t of tri) {
    if (haystack.includes(t)) found++;
  }
  return found / tri.size >= 0.7;
}

function buildPdfIndex() {
  const pdfPath = 'C:\\Users\\didhf\\mineru-downloads\\index_1.md';
  return fs.readFileSync(pdfPath, 'utf8');
}

function check() {
  const lines = [];
  let passes = 0, failures = 0, warnings = 0;

  lines.push(formatSection('PDF vs JSON Index Comparison'));
  lines.push(info('Source: original/pdf/index.pdf (via MinerU OCR)'));
  lines.push(info('Matching: aggressive LaTeX stripping + lowercase fuzzy match'));

  const pdfRaw = buildPdfIndex();
  const pdfNorm = toPlainPdf(pdfRaw);
  const master = loadJSON('original/index_entries.json');
  if (master.error) {
    lines.push(fail('Cannot load master JSON', master.error));
    failures++;
    return { passes, failures, warnings, lines };
  }

  const l1Entries = master.data.entries.filter(e => e.level === 1);
  const l2Entries = master.data.entries.filter(e => e.level === 2);

  // ---- L1: JSON -> PDF ----
  lines.push(heading('L1 Coverage: JSON entries -> PDF'));
  const l1Missing = [];

  for (const e of l1Entries) {
    const plain = toPlain(e.term);
    if (plain.length === 0) continue;
    if (fuzzyIncludes(pdfNorm, plain)) continue;
    if (plain.length > 30 && fuzzyIncludes(pdfNorm, plain.slice(0, 30))) continue;
    if (plain.length > 30 && fuzzyIncludes(pdfNorm, plain.slice(-30))) continue;
    l1Missing.push(e);
  }

  const l1Pct = (100 - l1Missing.length / l1Entries.length * 100).toFixed(1);
  if (l1Missing.length === 0) {
    lines.push(pass(`All ${l1Entries.length} L1 entries found in PDF (100%)`));
    passes++;
  } else {
    lines.push(fail(`${l1Entries.length - l1Missing.length}/${l1Entries.length} L1 found (${l1Pct}%), ${l1Missing.length} MISSING`));
    failures++;
  }

  // ---- L2: JSON -> PDF ----
  lines.push(heading('L2 Coverage: JSON entries -> PDF'));
  const l2Missing = [];

  for (const e of l2Entries) {
    const child = toPlain(e.term);
    const parent = toPlain(e.parent);
    if (child.length === 0) continue;
    const pIdx = pdfNorm.indexOf(parent);
    if (pIdx >= 0) {
      const vicinity = pdfNorm.slice(Math.max(0, pIdx - 20), pIdx + 400);
      if (fuzzyIncludes(vicinity, child)) continue;
    }
    if (child.length > 4 && fuzzyIncludes(pdfNorm, child)) continue;
    if (child.length > 20 && fuzzyIncludes(pdfNorm, child.slice(0, 20))) continue;
    l2Missing.push(e);
  }

  const l2Pct = (100 - l2Missing.length / l2Entries.length * 100).toFixed(1);
  if (l2Missing.length === 0) {
    lines.push(pass(`All ${l2Entries.length} L2 entries found in PDF (100%)`));
    passes++;
  } else {
    lines.push(fail(`${l2Entries.length - l2Missing.length}/${l2Entries.length} L2 found (${l2Pct}%), ${l2Missing.length} MISSING`));
    failures++;
  }

  // ---- Detailed missing lists ----
  if (l1Missing.length > 0) {
    lines.push(heading(`L1 Entries in JSON but NOT found in PDF (${l1Missing.length})`));
    for (const e of l1Missing) {
      const plain = toPlain(e.term);
      lines.push(`  ${e.term.slice(0, 65).padEnd(68)} [p.${e.page.join(',')}]   normalized:"${plain.slice(0,50)}"`);
    }
  }

  if (l2Missing.length > 0) {
    const outPath = path.join(PROJECT_ROOT, 'index', 'l2_missing_in_pdf.txt');
    const l2Lines = l2Missing.map(e => {
      const c = toPlain(e.term);
      const p = toPlain(e.parent);
      return `"${e.parent}" -> "${e.term}"  [p.${e.page.join(',')}]   norm:"${p}" -> "${c}"`;
    });
    fs.writeFileSync(outPath, l2Lines.join('\n'));
    lines.push(info(`Full L2 missing list (${l2Missing.length} entries) written to: index/l2_missing_in_pdf.txt`));

    // Show first 20
    lines.push(heading('Sample L2 missing (first 20)'));
    for (const e of l2Missing.slice(0, 20)) {
      lines.push(`  "${e.parent.slice(0,45)}" -> "${e.term.slice(0,50)}"  [p.${e.page.join(',')}]`);
    }
  }

  // ---- Summary ----
  lines.push(heading('Summary'));
  const total = l1Entries.length + l2Entries.length;
  const totalMissing = l1Missing.length + l2Missing.length;
  const totalPct = (100 - totalMissing / total * 100).toFixed(1);
  lines.push(info(`Total coverage: ${total - totalMissing}/${total} (${totalPct}%)`));
  lines.push(info(`  L1: ${l1Entries.length - l1Missing.length}/${l1Entries.length}`));
  lines.push(info(`  L2: ${l2Entries.length - l2Missing.length}/${l2Entries.length}`));

  return { passes, failures, warnings, lines };
}

if (require.main === module) {
  const r = check();
  console.log(r.lines.join('\n'));
  process.exit(r.failures > 0 ? 1 : 0);
}

module.exports = { check };
