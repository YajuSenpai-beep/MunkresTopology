const fs = require("fs");
const path = require("path");

const chaptersDir = path.join(__dirname, "..", "..", "chapters");
const files = fs.readdirSync(chaptersDir).filter(f => f.startsWith("Chapter_") && f.endsWith(".tex"));

for (const f of files) {
  const fp = path.join(chaptersDir, f);
  let content = fs.readFileSync(fp, "utf8");

  // Find all \begin{example}...\end{example} pairs that aren't already in centeredblock
  let result = "";
  let i = 0;

  while (i < content.length) {
    // Look for \begin{example}
    const beginIdx = content.indexOf("\\begin{example}", i);

    if (beginIdx < 0) {
      result += content.slice(i);
      break;
    }

    // Check if already wrapped in centeredblock
    const before = content.slice(Math.max(0, beginIdx - 30), beginIdx);
    if (before.includes("\\begin{centeredblock}")) {
      // Already wrapped — copy up to and including this begin
      result += content.slice(i, beginIdx + "\\begin{example}".length);
      i = beginIdx + "\\begin{example}".length;
      continue;
    }

    // Copy everything before this example
    result += content.slice(i, beginIdx);

    // Find matching \end{example}
    const endIdx = content.indexOf("\\end{example}", beginIdx);
    if (endIdx < 0) {
      result += content.slice(beginIdx);
      break;
    }

    const exampleContent = content.slice(beginIdx, endIdx + "\\end{example}".length);

    // Wrap with centeredblock
    result += "\\begin{centeredblock}\n" + exampleContent + "\n\\end{centeredblock}";

    i = endIdx + "\\end{example}".length;
  }

  fs.writeFileSync(fp, result);
  console.log(f.replace("Chapter_", "").replace(".tex", "").replace(/_/g, " ").trim() + ": done");
}
console.log("Done.");
