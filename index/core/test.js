/**
 * Test Suite — engine.js + parse-index.js
 * Run: node index/core/test.js
 */
const engine = require("./engine");
const { parseIndented, parseRunIn, parsePages, extractPages } = require("./parse-index");

let passed = 0;
let failed = 0;

function assert(condition, label) {
  if (condition) { passed++; }
  else { console.error("  FAIL:", label); failed++; }
}

// ============================================================
// engine.js tests
// ============================================================
console.log("\n=== engine.js ===\n");

const config = {
  templates: {
    l1: "\\idx{${key}}",
    l1Math: "\\idxmath{${sort}}{${display}}",
    l2: "\\idxsub{${parent}}{${child}}",
  },
  aliases: { "inverse image": ["preimage"] },
  mathShortcuts: {},
};

// 1. Basic insertion
(function () {
  console.log("1. Basic insertion");
  const content = "The concept of a field is central to algebra.";
  const entries = [{ term: "field", level: 1, page: [1] }];
  const ops = engine.findInsertions(content, entries, config);
  assert(ops.length === 1, "found field");
  assert(ops[0].cmd === "\\idx{field}", "correct cmd");
  assert(ops[0].pos === content.indexOf("field"), "correct position");
})();

// 2. Math mode skip
(function () {
  console.log("2. Math mode skip");
  const content = "The set \\(A\\) is a field of study.";
  const entries = [{ term: "field", level: 1, page: [1] }];
  const ops = engine.findInsertions(content, entries, config);
  // "field" appears in text (second occurrence), not inside math
  assert(ops.length === 1, "skipped math-mode 'field', found text 'field'");
})();

// 3. Longer term priority
(function () {
  console.log("3. Longer term priority (no overlap)");
  const content = "The inverse function theorem is important.";
  const entries = [
    { term: "inverse function", level: 1, page: [20] },
    { term: "inverse", level: 1, page: [15] },
  ];
  const ops = engine.findInsertions(content, entries, config);
  // "inverse function" found, "inverse" should NOT overlap
  assert(ops.length === 1, "only longer term inserted");
  assert(ops[0].entry.term === "inverse function", "correct term");
})();

// 4. Alias resolution
(function () {
  console.log("4. Alias resolution");
  const content = "The preimage of a set under a function.";
  const entries = [{ term: "inverse image", level: 1, page: [5] }];
  const configWithAlias = {
    ...config,
    aliases: { "inverse image": ["preimage"] },
  };
  const ops = engine.findInsertions(content, entries, configWithAlias);
  assert(ops.length === 1, "found via alias");
  assert(ops[0].entry.term === "inverse image", "correct term mapped");
})();

// 5. Math symbol insertion
(function () {
  console.log("5. Math symbol insertion");
  const content = "We denote real numbers by \\mathbb{R}.";
  const entries = [
    { term: "\\(\\mathbb{R}\\)", level: 1, sort_key: "R", page: [5] },
  ];
  const ops = engine.findInsertions(content, entries, config);
  assert(ops.length === 1, "found math symbol");
  assert(ops[0].cmd.includes("\\idxmath"), "uses idxmath command");
})();

// 6. Inside command skip
(function () {
  console.log("6. Inside command skip");
  const content = "\\includegraphics{field.jpg} shows a field.";
  const entries = [{ term: "field", level: 1, page: [1] }];
  const ops = engine.findInsertions(content, entries, config);
  // "field" inside \\includegraphics should be skipped
  // "field" in text should be found
  assert(ops.length === 1, "skipped command arg, found text occurrence");
})();

// 7. Inside braces skip
(function () {
  console.log("7. Inside braces skip");
  const content = "The set {field, ring, group} is finite. But field theory is vast.";
  const entries = [{ term: "field", level: 1, page: [1] }];
  const ops = engine.findInsertions(content, entries, config);
  // "field" inside {...} should be skipped
  assert(ops.length === 1, "skipped braced occurrence, found text");
})();

// 8. L2 entry handling
(function () {
  console.log("8. L2 entry handling");
  const content = "The finite axiom of choice is important.";
  const entries = [
    { term: "finite axiom of choice", level: 2, parent: "Axiom of choice", page: [42] },
  ];
  const ops = engine.findInsertions(content, entries, config);
  assert(ops.length >= 0, "L2 entries handled without crash");
})();

// 9. Empty content
(function () {
  console.log("9. Empty content");
  const content = "";
  const entries = [{ term: "field", level: 1, page: [1] }];
  const ops = engine.findInsertions(content, entries, config);
  assert(ops.length === 0, "empty content produces no insertions");
})();

// 10. Empty entries
(function () {
  console.log("10. Empty entries");
  const content = "Some text.";
  const ops = engine.findInsertions(content, [], config);
  assert(ops.length === 0, "empty entries produces no insertions");
})();

// ============================================================
// parse-index.js tests
// ============================================================
console.log("\n=== parse-index.js ===\n");

// 11. Page range expansion
(function () {
  console.log("11. Page range expansion");
  const pages = parsePages("42, 45-47, 50");
  assert(pages.length === 5, "5 pages total");
  assert(pages[0] === 42, "first is 42");
  assert(pages[4] === 50, "last is 50");
})();

// 12. Extract pages from term
(function () {
  console.log("12. Extract pages from term");
  const { term, pages } = extractPages("Axiom of choice, 42, 45-47");
  assert(term === "Axiom of choice", "term extracted");
  assert(pages.length === 4, "4 pages");
})();

// 13. Indented format
(function () {
  console.log("13. Indented format");
  const lines = [
    "Axiom of choice, 42, 45",
    "  finite axiom of choice, 42",
    "  choice function, 43",
    "Compactness, 50-52",
  ];
  const entries = parseIndented(lines);
  assert(entries.length === 4, "4 entries");
  assert(entries[0].level === 1 && entries[0].term === "Axiom of choice", "L1 detected");
  assert(entries[1].level === 2 && entries[1].parent === "Axiom of choice", "L2 linked to parent");
  assert(entries[3].level === 1 && entries[3].term === "Compactness", "second L1 detected");
})();

// 14. Alphabet headers skipped
(function () {
  console.log("14. Alphabet headers skipped");
  const lines = ["A", "Axiom of choice, 42", "B", "Compactness, 50"];
  const entries = parseIndented(lines);
  assert(entries.length === 2, "headers skipped");
})();

// 15. buildCommand
(function () {
  console.log("15. buildCommand");
  const cmd = engine.buildCommand(
    { term: "field", level: 1 },
    config.templates
  );
  assert(cmd === "\\idx{field}", "L1 command built");
  const cmd2 = engine.buildCommand(
    { term: "\\(\\mathbb{R}\\)", level: 1, sort_key: "R" },
    config.templates
  );
  assert(cmd2 === "\\idxmath{R}{\\(\\mathbb{R}\\)}", "L1Math command built");
})();

// ============================================================
console.log(`\n${"=".repeat(40)}`);
console.log(`Passed: ${passed}  Failed: ${failed}`);
console.log(`${"=".repeat(40)}\n`);
process.exit(failed > 0 ? 1 : 0);
