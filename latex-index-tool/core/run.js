/**
 * Munkres Topology — index insertion runner.
 * Thin wrapper: loads config + data, calls engine.
 *
 * Usage: node index/core/run.js [--dry-run] [--l1-only] [chapter-number]
 */
const fs = require("fs");
const path = require("path");
const engine = require("./engine");

const PROJECT_ROOT = path.join(__dirname, "..", "..");
const CONFIG_PATH = path.join(__dirname, "..", "config", "default.json");

function pad(n) { return n < 10 ? "0" + n : "" + n; }

function run(chNum, options = {}) {
  const config = JSON.parse(fs.readFileSync(CONFIG_PATH, "utf8"));
  const { dryRun = false, l1Only = false } = options;

  // Load entries
  const entryPath = path.join(PROJECT_ROOT, config.entryFile.replace("${num}", pad(chNum)));
  let entries = JSON.parse(fs.readFileSync(entryPath, "utf8"));
  if (!Array.isArray(entries)) entries = entries.entries || [];

  // Filter
  if (l1Only) entries = entries.filter(e => e.level === 1);
  entries = entries.filter(e => {
    if (!e.term) return false;
    const skipPatterns = config.skipPatterns || [];
    for (const p of skipPatterns) {
      if (e.term.includes(p)) return true; // keep these
    }
    if (e.page && e.page.length === 0) return false;
    return true;
  });

  // Find tex file
  const sourceDir = path.join(PROJECT_ROOT, config.chapterSourceDir || "chapters");
  const pattern = config.filePattern.replace("${num}", chNum);
  const files = fs.readdirSync(sourceDir).filter(f =>
    f.startsWith(pattern.replace("_*.tex", "_")) && f.endsWith(".tex")
  );

  if (files.length === 0) {
    return { error: `No tex file for chapter ${chNum} in ${sourceDir}` };
  }

  const texPath = path.join(sourceDir, files[0]);
  let content = fs.readFileSync(texPath, "utf8");
  const original = content;

  // Find insertions
  const ops = engine.findInsertions(content, entries, config);

  if (dryRun) {
    const report = {
      file: files[0],
      total: entries.length,
      found: ops.length,
      notFound: [],
    };
    const foundTerms = new Set(ops.map(o => o.entry.term));
    for (const e of entries) {
      if (!foundTerms.has(e.term)) report.notFound.push(e.term);
    }
    return report;
  }

  // Apply
  content = engine.applyInsertions(content, ops);

  if (content !== original) {
    fs.writeFileSync(texPath, content, "utf8");
  }

  return {
    file: files[0],
    total: entries.length,
    inserted: ops.length,
  };
}

// CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  const dryRun = args.includes("--dry-run");
  const l1Only = args.includes("--l1-only");
  const chNum = args.find(a => /^\d+$/.test(a)) || "1";

  const result = run(parseInt(chNum), { dryRun, l1Only });
  if (result.error) {
    console.error("ERROR:", result.error);
    process.exit(1);
  }
  console.log(JSON.stringify(result, null, 2));
}

module.exports = { run };
