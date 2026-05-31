const fs = require("fs");
const backup = fs.readFileSync("chapters/Chapter_1_backup.tex", "utf8").replace(/\r\n/g, "\n");
const current = fs.readFileSync("chapters/Chapter_1_Set_Theory_and_Logic.tex", "utf8").replace(/\r\n/g, "\n");

function findExerciseBlocks(text) {
  const lines = text.split("\n");
  const blocks = [];

  let inBlock = false;
  let blockStart = 0;

  for (let i = 0; i < lines.length; i++) {
    const L = lines[i];
    const isExSection = L.includes("\\section*{Exercises}") || L.includes("\\section*{* Supplementary");
    const isNextSection = L.includes("\\section*{") && !isExSection;

    if (isExSection) {
      if (inBlock) blocks.push({ start: blockStart, end: i - 1, line: blockStart + 1 });
      inBlock = true;
      blockStart = i;
    } else if (isNextSection && inBlock) {
      blocks.push({ start: blockStart, end: i - 1, line: blockStart + 1 });
      inBlock = false;
    }
  }
  if (inBlock) blocks.push({ start: blockStart, end: lines.length - 1, line: blockStart + 1 });

  return { blocks, lines };
}

function scanEnvs(content) {
  const envs = [];
  const names = ["theorem", "lemma", "corollary", "proof", "definition", "example", "proposition", "addendum", "property"];
  names.forEach(env => {
    const re = new RegExp("\\\\begin\\{" + env + "\\}", "g");
    const matches = content.match(re);
    if (matches) envs.push({ name: env, count: matches.length });
  });
  return envs;
}

function process(name, text) {
  const { blocks, lines } = findExerciseBlocks(text);
  console.log("=== " + name + " ===");
  console.log("Exercise blocks: " + blocks.length + "\n");

  let grandTotal = 0;
  blocks.forEach((b, idx) => {
    const content = lines.slice(b.start, b.end + 1).join("\n");
    const title = lines[b.start].trim().slice(0, 80);
    const envs = scanEnvs(content);

    let total = envs.reduce((s, e) => s + e.count, 0);
    grandTotal += total;

    if (envs.length > 0) {
      const desc = envs.map(e => e.name + "(" + e.count + ")").join(", ");
      console.log("  #" + (idx + 1) + " L" + (b.start + 1) + " " + title + "  [" + desc + "]");
    } else {
      console.log("  #" + (idx + 1) + " L" + (b.start + 1) + " " + title + "  [none]");
    }
  });

  console.log("\nTotal environments in exercises: " + grandTotal + "\n");
}

process("BACKUP (OCR)", backup);
process("CURRENT", current);
