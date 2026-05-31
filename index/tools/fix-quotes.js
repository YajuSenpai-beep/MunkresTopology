const fs = require("fs");
const path = require("path");

const chaptersDir = path.join(__dirname, "..", "..", "chapters");
const files = fs.readdirSync(chaptersDir).filter(f => f.startsWith("Chapter_") && f.endsWith(".tex"));

for (const f of files) {
  const fp = path.join(chaptersDir, f);
  let content = fs.readFileSync(fp, "utf8");
  const original = content;

  let result = "";
  let i = 0;

  while (i < content.length) {
    if (content[i] !== "\"") {
      result += content[i];
      i++;
      continue;
    }

    // Check if inside LaTeX braces
    const before = content.slice(Math.max(0, i - 100), i);
    const openB = (before.match(/\{/g) || []).length;
    const closeB = (before.match(/\}/g) || []).length;

    if (openB > closeB) {
      // Inside braces - idx, index, chapter, section args - skip
      result += "\"";
      i++;
      continue;
    }

    // Determine if opening or closing
    const prev = i > 0 ? content[i - 1] : "\n";
    const next = i < content.length - 1 ? content[i + 1] : "\n";

    // Opening: after whitespace, line start, paren, or brace-open
    if (i === 0 || /[\s\n(\{\[]/.test(prev)) {
      result += "``";
    } else {
      result += "''";
    }
    i++;
  }

  if (result !== original) {
    fs.writeFileSync(fp, result);
    console.log(f.replace("Chapter_", "").replace(".tex", "").replace(/_/g, " ").trim() + ": fixed");
  }
}
console.log("Done.");
