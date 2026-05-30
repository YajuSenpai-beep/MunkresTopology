const fs = require("fs");
const path = require("path");

const dir = "chapters";
const files = fs.readdirSync(dir).filter(f => f.endsWith(".tex") && f.startsWith("Chapter"));

// Count all \index entries per chapter
let total = 0;
for (const f of files) {
    const content = fs.readFileSync(path.join(dir, f), "utf8");
    const matches = content.match(/\\index\{[^}]*\}/g) || [];
    console.log(f.replace(".tex","") + ": " + matches.length);
    total += matches.length;
}
console.log("Total \\index commands: " + total);

// Check idx file
const idx = fs.readFileSync("Topology_by_Munkres.idx", "utf8");
const idxLines = idx.split("\n").filter(l => l.trim());
console.log("\nIDX entries: " + idxLines.length);

// Check ind file
const ind = fs.readFileSync("Topology_by_Munkres.ind", "utf8");
const items = (ind.match(/\\item /g) || []).length;
const subitems = (ind.match(/\\subitem /g) || []).length;
console.log("IND: " + items + " L1 + " + subitems + " L2 = " + (items+subitems) + " total");

// Check errors
const log = fs.readFileSync("Topology_by_Munkres.log", "utf8");
const errors = (log.match(/^!/gm) || []).length;
const warnings = (log.match(/Warning/g) || []).length;
console.log("\nErrors: " + errors + ", Warnings: " + warnings);

// JSON comparison
const json = JSON.parse(fs.readFileSync("original/index_entries.json", "utf8"));
const jsonL1 = json.entries.filter(e => e.level === 1).length;
const jsonL2 = json.entries.filter(e => e.level === 2).length;
console.log("JSON target: " + jsonL1 + " L1 + " + jsonL2 + " L2 = " + json.entries.length + " total");
console.log("L1 coverage: " + items + "/" + jsonL1 + " = " + (items/jsonL1*100).toFixed(1) + "%");
console.log("L2 coverage: " + subitems + "/" + jsonL2 + " = " + (subitems/jsonL2*100).toFixed(1) + "%");
console.log("Overall: " + (items+subitems) + "/" + json.entries.length + " = " + ((items+subitems)/json.entries.length*100).toFixed(1) + "%");
