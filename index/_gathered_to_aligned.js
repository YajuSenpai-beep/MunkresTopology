// Convert all \begin{gathered}...\end{gathered} to \begin{aligned}...\end{aligned}
// and add & before = on each line
const fs = require("fs");
const fp = "chapters/Chapter_1_Set_Theory_and_Logic.tex";
let c = fs.readFileSync(fp, "utf8");

// Replace gathered with aligned
c = c.replace(/\\begin\{gathered\}/g, "\\begin{aligned}");
c = c.replace(/\\end\{gathered\}/g, "\\end{aligned}");

// Now add & before = inside aligned blocks
let result = "";
let i = 0;
while (i < c.length) {
  const start = c.indexOf("\\begin{aligned}", i);
  if (start < 0) { result += c.slice(i); break; }

  const end = c.indexOf("\\end{aligned}", start);
  if (end < 0) { result += c.slice(i); break; }

  result += c.slice(i, start + "\\begin{aligned}".length);

  let interior = c.slice(start + "\\begin{aligned}".length, end);

  let lines = interior.split("\\\\");
  lines = lines.map(line => {
    if (line.includes("=") && !line.includes("&")) {
      // brace-aware = detection
      let depth = 0;
      let eqPos = -1;
      for (let j = 0; j < line.length; j++) {
        if (line[j] === "{" && (j === 0 || line[j-1] !== "\\")) depth++;
        else if (line[j] === "}" && (j === 0 || line[j-1] !== "\\")) depth--;
        else if (line[j] === "=" && depth === 0) { eqPos = j; break; }
      }
      if (eqPos >= 0) {
        line = line.slice(0, eqPos) + "&" + line.slice(eqPos);
      }
    }
    return line;
  });
  interior = lines.join("\\\\");

  result += interior;
  result += "\\end{aligned}";
  i = end + "\\end{aligned}".length;
}

fs.writeFileSync(fp, result);
console.log("Done: all gathered -> aligned with & before =");
