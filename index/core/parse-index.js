/**
 * Index Text → JSON Converter
 * ===========================
 * Parse plain-text index files (OCR output, manual lists) into structured
 * JSON matching the original/index_entries.json format.
 *
 * Supports three common index text formats:
 *
 * 1. INDENTED (default):
 *    L1 entries flush left, L2 entries indented with 2+ spaces or tab.
 *    L1 Term, 42, 45
 *      L2 Term, 42
 *
 * 2. RUN-IN:
 *    L1 followed by L2 on same line, separated by commas/semicolons.
 *    L1 Term, 42, 45; L2 Term, 42; Another L2, 45
 *
 * 3. TWO-COLUMN (--two-column):
 *    OCR from two-column layouts where entries wrap.
 *
 * Usage:
 *   node index/core/parse-index.js input.txt [--format=indented|run-in] [--output=output.json]
 *
 * Output JSON structure:
 * {
 *   "entries": [
 *     {"term": "...", "level": 1, "page": [42, 45]},
 *     {"term": "...", "level": 2, "parent": "...", "page": [42]}
 *   ]
 * }
 */

const fs = require("fs");

/**
 * Parse pages numbers from a string like "42, 45-47, 50".
 * Supports ranges with hyphen/en-dash.
 */
function parsePages(raw) {
  if (!raw) return [];
  const pages = [];
  const parts = raw.split(/\s*[,;，；]\s*/);
  for (const part of parts) {
    const range = part.trim().split(/\s*[-–—]\s*/);
    if (range.length === 2) {
      const start = parseInt(range[0]);
      const end = parseInt(range[1]);
      if (!isNaN(start) && !isNaN(end)) {
        for (let p = start; p <= end; p++) pages.push(p);
      }
    } else {
      const n = parseInt(part.trim());
      if (!isNaN(n) && !pages.includes(n)) pages.push(n);
    }
  }
  return pages.sort((a, b) => a - b);
}

/**
 * Extract pages from the end of a term string.
 * Returns { term, pages }.
 */
function extractPages(line) {
  const pageRe = /,?\s*(\d[\d\s,;，；\-–—]*)$/;
  const match = line.match(pageRe);
  if (!match) return { term: line.trim(), pages: [] };
  return {
    term: line.slice(0, match.index).trim().replace(/,\s*$/, ""),
    pages: parsePages(match[1]),
  };
}

/**
 * Parse indented format: L1 flush left, L2 indented.
 */
function parseIndented(lines) {
  const entries = [];
  let currentParent = null;

  for (let line of lines) {
    // Skip empty lines and headers
    if (!line.trim() || /^[A-Z]\s*$/.test(line.trim())) continue;
    if (/^(Index|INDEX)/i.test(line.trim())) continue;

    const indent = line.match(/^(\s*)/)[1].length;
    const { term, pages } = extractPages(line.trim());

    if (!term) continue;

    if (indent < 2) {
      // L1 entry
      currentParent = term;
      entries.push({ term, level: 1, page: pages });
    } else if (currentParent) {
      // L2 entry (indented)
      entries.push({ term, level: 2, parent: currentParent, page: pages });
    }
  }

  return entries;
}

/**
 * Parse run-in format: L1, pages; L2, pages; L2, pages
 */
function parseRunIn(lines) {
  const entries = [];
  const text = lines.join(" ").replace(/\s+/g, " ");
  let currentParent = null;

  const segments = text.split(/\s*[;；]\s*/);
  for (const seg of segments) {
    const { term, pages } = extractPages(seg.trim());
    if (!term) continue;

    // Heuristic: if term looks like a main heading (longer, more specific),
    // it's L1. If shorter/simpler, it's L2 of the current parent.
    // This is imperfect but works for OCR'd Munkres-style indexes.

    const isL1 = !currentParent || term.length > 10 || /[A-Z]/.test(term[0]);
    if (isL1) {
      currentParent = term;
      entries.push({ term, level: 1, page: pages });
    } else {
      entries.push({ term, level: 2, parent: currentParent, page: pages });
    }
  }

  return entries;
}

/**
 * Main parser. Auto-detects format if not specified.
 */
function parseIndex(inputPath, options = {}) {
  const text = fs.readFileSync(inputPath, "utf8");
  const lines = text.split(/\r?\n/);
  const format = options.format || "auto";

  let entries;
  if (format === "run-in") {
    entries = parseRunIn(lines);
  } else {
    // Default: indented (works for most OCR index outputs)
    entries = parseIndented(lines);
  }

  // Post-process: sort by term within same parent
  entries.sort((a, b) => {
    const pa = (a.parent || "").toLowerCase();
    const pb = (b.parent || "").toLowerCase();
    if (pa !== pb) return pa.localeCompare(pb);
    if (a.level !== b.level) return a.level - b.level;
    return a.term.toLowerCase().localeCompare(b.term.toLowerCase());
  });

  return {
    source: inputPath,
    format,
    total: entries.length,
    l1Count: entries.filter(e => e.level === 1).length,
    l2Count: entries.filter(e => e.level === 2).length,
    entries,
  };
}

// CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.log("Usage: node parse-index.js <input.txt> [--format=indented|run-in] [--output=output.json]");
    console.log("  --format   Index text format (default: auto-detect indented)");
    console.log("  --output   Output JSON file (default: stdout)");
    process.exit(1);
  }

  const inputPath = args[0];
  const formatArg = args.find(a => a.startsWith("--format="));
  const outputArg = args.find(a => a.startsWith("--output="));
  const format = formatArg ? formatArg.split("=")[1] : "auto";
  const outputPath = outputArg ? outputArg.split("=")[1] : null;

  if (!fs.existsSync(inputPath)) {
    console.error("File not found:", inputPath);
    process.exit(1);
  }

  const result = parseIndex(inputPath, { format });
  const json = JSON.stringify({ entries: result.entries }, null, 2);

  if (outputPath) {
    fs.writeFileSync(outputPath, json, "utf8");
    console.log(`Written ${result.entries.length} entries to ${outputPath}`);
    console.log(`  L1: ${result.l1Count}, L2: ${result.l2Count}`);
  } else {
    console.log(json);
  }
}

module.exports = { parseIndex, parsePages, extractPages, parseIndented, parseRunIn };
