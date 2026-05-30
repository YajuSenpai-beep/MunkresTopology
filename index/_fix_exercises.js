const fs = require("fs");
const fp = "chapters/Chapter_1_Set_Theory_and_Logic.tex";
let c = fs.readFileSync(fp, "utf8");

const pairs = [
  // 1. Exercise 1: sum formulas
  [
    "\\[\n\\mathop{\\sum }\\limits_{{k = 1}}^{n}{b}_{k} = {b}_{1}\\;\\text{ for }n = 1,\n\\]\n\n\\[\n\\mathop{\\sum }\\limits_{{k = 1}}^{n}{b}_{k} = \\left( {\\mathop{\\sum }\\limits_{{k = 1}}^{{n - 1}}{b}_{k}}\\right)  + {b}_{n}\\;\\text{ for }n > 1.\n\\]",
    "\\[\n\\begin{aligned}\n\\mathop{\\sum }\\limits_{{k = 1}}^{n}{b}_{k} &= {b}_{1}\\;\\text{ for }n = 1, \\\\\n\\mathop{\\sum }\\limits_{{k = 1}}^{n}{b}_{k} &= \\left( {\\mathop{\\sum }\\limits_{{k = 1}}^{{n - 1}}{b}_{k}}\\right)  + {b}_{n}\\;\\text{ for }n > 1.\n\\end{aligned}\n\\]",
  ],
  // 2. Exercise 2: product
  [
    "\\[\n\\mathop{\\prod }\\limits_{{k = 1}}^{1}{b}_{k} = {b}_{1}\n\\]\n\n\\[\n\\mathop{\\prod }\\limits_{{k = 1}}^{n}{b}_{k} = \\left( {\\mathop{\\prod }\\limits_{{k = 1}}^{{n - 1}}{b}_{k}}\\right)  \\cdot  {b}_{n}\\;\\text{ for }n > 1.\n\\]",
    "\\[\n\\begin{aligned}\n\\mathop{\\prod }\\limits_{{k = 1}}^{1}{b}_{k} &= {b}_{1} \\\\\n\\mathop{\\prod }\\limits_{{k = 1}}^{n}{b}_{k} &= \\left( {\\mathop{\\prod }\\limits_{{k = 1}}^{{n - 1}}{b}_{k}}\\right)  \\cdot  {b}_{n}\\;\\text{ for }n > 1.\n\\end{aligned}\n\\]",
  ],
  // 3. Exercise 4: Fibonacci
  [
    "\\[\n{\\lambda }_{1} = {\\lambda }_{2} = 1\n\\]\n\n\\[\n{\\lambda }_{n} = {\\lambda }_{n - 1} + {\\lambda }_{n - 2}\\;\\text{ for }n > 2.\n\\]",
    "\\[\n\\begin{aligned}\n{\\lambda }_{1} &= {\\lambda }_{2} = 1 \\\\\n{\\lambda }_{n} &= {\\lambda }_{n - 1} + {\\lambda }_{n - 2}\\;\\text{ for }n > 2.\n\\end{aligned}\n\\]",
  ],
  // 4. Exercise 5
  [
    "\\[\nh\\left( 1\\right)  = 3,\n\\]\n\n\\[\nh\\left( i\\right)  = {\\left\\lbrack  h\\left( i - 1\\right)  + 1\\right\\rbrack  }^{1/2}\\;\\text{ for }i > 1.\n\\]",
    "\\[\n\\begin{aligned}\nh\\left( 1\\right)  &= 3, \\\\\nh\\left( i\\right)  &= {\\left\\lbrack  h\\left( i - 1\\right)  + 1\\right\\rbrack  }^{1/2}\\;\\text{ for }i > 1.\n\\end{aligned}\n\\]",
  ],
  // 5. Exercise 6(a)
  [
    "\\[\nh\\left( 1\\right)  = 3,\n\\]\n\n\\[\nh\\left( i\\right)  = {\\left\\lbrack  h\\left( i - 1\\right)  - 1\\right\\rbrack  }^{1/2}\\;\\text{ for }i > 1.\n\\]",
    "\\[\n\\begin{aligned}\nh\\left( 1\\right)  &= 3, \\\\\nh\\left( i\\right)  &= {\\left\\lbrack  h\\left( i - 1\\right)  - 1\\right\\rbrack  }^{1/2}\\;\\text{ for }i > 1.\n\\end{aligned}\n\\]",
  ],
  // 6. Exercise 6(b)
  [
    "\\[\nh\\left( 1\\right)  = 3,\n\\]\n\n\\[\nh\\left( i\\right)  = \\left\\{  \\begin{array}{ll} {\\left\\lbrack  h\\left( i - 1\\right)  - 1\\right\\rbrack  }^{1/2} & \\text{ if }h\\left( {i - 1}\\right)  > 1 \\\\  5 & \\text{ if }h\\left( {i - 1}\\right)  \\leq  1 \\end{array}\\right\\}  \\;\\text{ for }i > 1.\n\\]",
    "\\[\n\\begin{aligned}\nh\\left( 1\\right)  &= 3, \\\\\nh\\left( i\\right)  &= \\left\\{  \\begin{array}{ll} {\\left\\lbrack  h\\left( i - 1\\right)  - 1\\right\\rbrack  }^{1/2} & \\text{ if }h\\left( {i - 1}\\right)  > 1 \\\\  5 & \\text{ if }h\\left( {i - 1}\\right)  \\leq  1 \\end{array}\\right\\}  \\;\\text{ for }i > 1.\n\\end{aligned}\n\\]",
  ],
];

let count = 0;
for (const [old, nw] of pairs) {
  // Try with \n
  if (c.includes(old)) {
    c = c.replace(old, nw);
    count++;
  } else {
    // Try with \r\n
    const oldCRLF = old.replace(/\n/g, "\r\n");
    if (c.includes(oldCRLF)) {
      const nwCRLF = nw.replace(/\n/g, "\r\n");
      c = c.replace(oldCRLF, nwCRLF);
      count++;
    } else {
      console.log("Not found:", JSON.stringify(old.slice(0, 50)));
    }
  }
}

fs.writeFileSync(fp, c);
console.log("Replaced " + count + "/" + pairs.length + " groups.");
