// Wrap all unwrapped \begin{example}...\end{example} in Chapter 1 with centeredblock
const fs = require("fs");
const fp = "chapters/Chapter_1_Set_Theory_and_Logic.tex";
let c = fs.readFileSync(fp, "utf8");

let r = "";
let i = 0;
let count = 0;

while (i < c.length) {
  const bi = c.indexOf("\\begin{example}", i);
  if (bi < 0) { r += c.slice(i); break; }

  const before = c.slice(Math.max(0, bi - 30), bi);
  if (before.includes("\\begin{centeredblock}")) {
    r += c.slice(i, bi + "\\begin{example}".length);
    i = bi + "\\begin{example}".length;
    continue;
  }

  r += c.slice(i, bi);
  const ei = c.indexOf("\\end{example}", bi);
  if (ei < 0) { r += c.slice(bi); break; }

  const ex = c.slice(bi, ei + "\\end{example}".length);
  r += "\\begin{centeredblock}\n" + ex + "\n\\end{centeredblock}";
  i = ei + "\\end{example}".length;
  count++;
}

fs.writeFileSync(fp, r);
console.log("Wrapped " + count + " examples in Chapter 1.");
