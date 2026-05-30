const fs = require("fs");
const fp = "chapters/Chapter_1_Set_Theory_and_Logic.tex";
let c = fs.readFileSync(fp, "utf8");

const old = `\\[
{f}^{-1}\\left( {f\\left( \\left\\lbrack  {0,1}\\right\\rbrack  \\right) }\\right)  = {f}^{-1}\\left( \\left\\lbrack  {2,5}\\right\\rbrack  \\right)  = \\left\\lbrack  {-1,1}\\right\\rbrack  ,\\;\\text{ and }
\\]

\\[
f\\left( {{f}^{-1}\\left( \\left\\lbrack  {0,5}\\right\\rbrack  \\right) }\\right)  = f\\left( \\left\\lbrack  {-1,1}\\right\\rbrack  \\right)  = \\left\\lbrack  {2,5}\\right\\rbrack  .
\\]`;

const nw = `\\[
\\begin{aligned}
{f}^{-1}\\left( {f\\left( \\left\\lbrack  {0,1}\\right\\rbrack  \\right) }\\right)  &= {f}^{-1}\\left( \\left\\lbrack  {2,5}\\right\\rbrack  \\right)  = \\left\\lbrack  {-1,1}\\right\\rbrack  ,\\;\\text{ and } \\\\
f\\left( {{f}^{-1}\\left( \\left\\lbrack  {0,5}\\right\\rbrack  \\right) }\\right)  &= f\\left( \\left\\lbrack  {-1,1}\\right\\rbrack  \\right)  = \\left\\lbrack  {2,5}\\right\\rbrack  .
\\end{aligned}
\\]`;

if (c.includes(old)) {
  c = c.replace(old, nw);
  fs.writeFileSync(fp, c);
  console.log("Done.");
} else {
  console.log("OLD TEXT NOT FOUND. Searching for partial match...");
  const idx = c.indexOf("{f}^{-1}\\left( {f\\left(");
  if (idx >= 0) {
    console.log("Found at", idx);
    console.log("Context:", JSON.stringify(c.slice(idx, idx+100)));
  } else {
    console.log("Not found at all.");
  }
}
