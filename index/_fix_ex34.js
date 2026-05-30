const fs = require("fs");
const fp = "chapters/Chapter_1_Set_Theory_and_Logic.tex";
let c = fs.readFileSync(fp, "utf8").replace(/\r\n/g, "\n");

// Exercise 3 fix
const old3 = [
  "\\item (a) Show that if \\(\\mathcal{A}\\) is a collection of inductive sets, then the intersection of the elements of \\(\\mathcal{A}\\) is an inductive set.",
  "  \\begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\\alph*), align=left]",
  "  \\item Prove the basic properties (l) and (2) of \\({\\mathbb{Z}}_{ + }\\) .",
  "  \\end{enumerate}",
].join("\n");

const nw3 = [
  "\\item",
  "  \\begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\\alph*), align=left]",
  "  \\item Show that if \\(\\mathcal{A}\\) is a collection of inductive sets, then the intersection of the elements of \\(\\mathcal{A}\\) is an inductive set.",
  "  \\item Prove the basic properties (1) and (2) of \\({\\mathbb{Z}}_{ + }\\) .",
  "  \\end{enumerate}",
].join("\n");

// Exercise 4 fix
const old4 = [
  "\\item (a) Prove by induction that given \\(n \\in  {\\mathbb{Z}}_{ + }\\) , every nonempty subset of \\{ 1,\\ldots ,n\\rbrack\\) has a largest element.",
  "  \\begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\\alph*), align=left]",
  "  \\item Explain why you cannot conclude from (a) that every nonempty subset of \\({\\mathbb{Z}}_{ + }\\) has a largest element.",
  "  \\end{enumerate}",
].join("\n");

const nw4 = [
  "\\item",
  "  \\begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\\alph*), align=left]",
  "  \\item Prove by induction that given \\(n \\in  {\\mathbb{Z}}_{ + }\\) , every nonempty subset of \\{ 1,\\ldots ,n\\} has a largest element.",
  "  \\item Explain why you cannot conclude from (a) that every nonempty subset of \\({\\mathbb{Z}}_{ + }\\) has a largest element.",
  "  \\end{enumerate}",
].join("\n");

let count = 0;
if (c.includes(old3)) { c = c.replace(old3, nw3); count++; console.log("Ex 3 fixed."); }
else { console.log("Ex 3 not found"); }

if (c.includes(old4)) { c = c.replace(old4, nw4); count++; console.log("Ex 4 fixed."); }
else {
  // Debug: find the exact text
  const idx = c.indexOf("\\item (a) Prove by induction");
  if (idx >= 0) {
    const snippet = c.slice(idx, idx + old4.length);
    console.log("Expected:", JSON.stringify(old4));
    console.log("Found:   ", JSON.stringify(snippet));
  }
}

fs.writeFileSync(fp, c.replace(/\n/g, "\r\n"));
console.log(count + " fixes applied.");
