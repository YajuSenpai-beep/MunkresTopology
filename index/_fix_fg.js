const fs = require("fs");
const fp = "chapters/Chapter_1_Set_Theory_and_Logic.tex";
let c = fs.readFileSync(fp, "utf8");
const lines = c.split("\n");
const hasCR = lines[0].endsWith("\r");
const LE = hasCR ? "\r\n" : "\n";

const old = [
  "\\[",
  "f : A \\rightarrow  \\{ 1,\\ldots ,n\\}",
  "\\]",
  "",
  "\\[",
  "g : A \\rightarrow  \\{ 1,\\ldots ,m\\} \\text{ . }",
  "\\]",
].join(LE);

const nw = [
  "\\[",
  "\\begin{aligned}",
  "f &: A \\rightarrow  \\{ 1,\\ldots ,n\\} \\\\",
  "g &: A \\rightarrow  \\{ 1,\\ldots ,m\\} \\text{ . }",
  "\\end{aligned}",
  "\\]",
].join(LE);

if (c.includes(old)) {
  c = c.replace(old, nw);
  fs.writeFileSync(fp, c);
  console.log("Done.");
} else {
  console.log("Not found.");
}
