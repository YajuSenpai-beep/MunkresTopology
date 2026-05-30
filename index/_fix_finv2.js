const fs = require("fs");
const fp = "chapters/Chapter_1_Set_Theory_and_Logic.tex";
let c = fs.readFileSync(fp, "utf8");
const lines = c.split("\n");

// Lines 607-612 (0-indexed: 606-611)
// Replace with merged aligned version
const newLines = [
  "\\[",
  "\\begin{aligned}",
  "{f}^{-1}\\left( {f\\left( \\left\\lbrack  {0,1}\\right\\rbrack  \\right) }\\right)  &= {f}^{-1}\\left( \\left\\lbrack  {2,5}\\right\\rbrack  \\right)  = \\left\\lbrack  {-1,1}\\right\\rbrack  ,\\;\\text{ and } \\\\",
  "f\\left( {{f}^{-1}\\left( \\left\\lbrack  {0,5}\\right\\rbrack  \\right) }\\right)  &= f\\left( \\left\\lbrack  {-1,1}\\right\\rbrack  \\right)  = \\left\\lbrack  {2,5}\\right\\rbrack  .",
  "\\end{aligned}",
  "\\]",
];

// Replace lines 607-612 (1-indexed) = indices 606-611
const before = lines.slice(0, 606);
const after = lines.slice(612);
const result = [...before, ...newLines, ...after].join("\n");

fs.writeFileSync(fp, result);
console.log("Done.");
