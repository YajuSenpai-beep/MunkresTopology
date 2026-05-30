const fs = require("fs");
const fp = "chapters/Chapter_1_Set_Theory_and_Logic.tex";
let c = fs.readFileSync(fp, "utf8");

// Build old and new with actual line endings from file
const lines = c.split("\n");
// Line endings: check if CRLF
const hasCR = lines.length > 1 && lines[0].endsWith("\r");
const LE = hasCR ? "\r\n" : "\n";
console.log("Line endings:", hasCR ? "CRLF" : "LF");

const old = [
  "\\[",
  "{f}^{-1}\\left( {f\\left( \\left\\lbrack  {0,1}\\right\\rbrack  \\right) }\\right)  = {f}^{-1}\\left( \\left\\lbrack  {2,5}\\right\\rbrack  \\right)  = \\left\\lbrack  {-1,1}\\right\\rbrack  ,\\;\\text{ and }",
  "\\]",
  "\\[",
  "f\\left( {{f}^{-1}\\left( \\left\\lbrack  {0,5}\\right\\rbrack  \\right) }\\right)  = f\\left( \\left\\lbrack  {-1,1}\\right\\rbrack  \\right)  = \\left\\lbrack  {2,5}\\right\\rbrack  .",
  "\\]",
].join(LE);

const nw = [
  "\\[",
  "\\begin{aligned}",
  "{f}^{-1}\\left( {f\\left( \\left\\lbrack  {0,1}\\right\\rbrack  \\right) }\\right)  &= {f}^{-1}\\left( \\left\\lbrack  {2,5}\\right\\rbrack  \\right)  = \\left\\lbrack  {-1,1}\\right\\rbrack  ,\\;\\text{ and } \\\\",
  "f\\left( {{f}^{-1}\\left( \\left\\lbrack  {0,5}\\right\\rbrack  \\right) }\\right)  &= f\\left( \\left\\lbrack  {-1,1}\\right\\rbrack  \\right)  = \\left\\lbrack  {2,5}\\right\\rbrack  .",
  "\\end{aligned}",
  "\\]",
].join(LE);

if (c.includes(old)) {
  c = c.replace(old, nw);
  fs.writeFileSync(fp, c);
  console.log("Done.");
} else {
  console.log("Not found. Debugging...");
  // Try without \r
  const oldLF = old.replace(/\r\n/g, "\n");
  if (c.includes(oldLF)) {
    console.log("Found with LF only");
    c = c.replace(oldLF, nw.replace(/\r\n/g, "\n"));
    fs.writeFileSync(fp, c);
    console.log("Done (LF).");
  } else {
    console.log("Still not found. Searching for partial...");
    const idx = c.indexOf("{f}^{-1}\\left( {f\\left( \\left\\lbrack  {0,1}\\right\\rbrack");
    console.log("Index:", idx);
    if (idx >= 0) {
      console.log("Context:", JSON.stringify(c.slice(idx-5, idx+80)));
    }
  }
}
