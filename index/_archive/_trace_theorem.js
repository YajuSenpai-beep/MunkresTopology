const fs = require("fs");
const c = fs.readFileSync("chapters/Chapter_1_Set_Theory_and_Logic.tex", "utf8");

const BEGIN = String.raw`\begin{theorem}`;
const END = String.raw`\end{theorem}`;

let depth = 0;
let pos = 0;
while (pos < c.length) {
  const begin = c.indexOf(BEGIN, pos);
  const end = c.indexOf(END, pos);
  if (begin < 0 && end < 0) break;
  const nextB = begin >= 0 && (end < 0 || begin < end);
  if (nextB) {
    depth++;
    const line = c.slice(0, begin).split("\n").length;
    console.log("BEGIN line", line, "depth:", depth);
    pos = begin + 1;
  } else {
    const line = c.slice(0, end).split("\n").length;
    console.log("END line", line, "depth:", depth);
    depth--;
    pos = end + 1;
  }
}
console.log("Final depth:", depth);
