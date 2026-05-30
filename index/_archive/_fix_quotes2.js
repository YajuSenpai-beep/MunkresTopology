const fs = require("fs");
const fp = "chapters/Chapter_1_Set_Theory_and_Logic.tex";
let c = fs.readFileSync(fp, "utf8");

// Category A: `,''X` → `, ``X` (comma + closing → comma + opening)
const catA = [
  ["sentence,''Every", "sentence, ``Every"],
  ["formally,''For every", "formally, ``For every"],
  ["the form,''If \\\\(P\\\\)", "the form, ``If \\\\(P\\\\)"],
  ["as saying,''If \\\\(x \\\\in", "as saying, ``If \\\\(x \\\\in"],
  ["by saying,''Let \\\\(A\\\\)", "by saying, ``Let \\\\(A\\\\)"],
];

// Category B: ` `` X `` Y` → ` `` X '' Y` where Y is a continuation word
// Pattern: `` after \\) followed by continuation text
const catB = [
  // L57
  ['\\\\(Q\\\\) `` means', '\\\\(Q\\\\) \'\' means'],
  // L66
  ['\\\\(Q\\\\) `` always means', '\\\\(Q\\\\) \'\' always means'],
  // L117: (called the hypothesis
  ['0\\\\) `` (called the hypothesis', '0\\\\) \'\' (called the hypothesis'],
  // L117: (called the conclusion
  ['0\\\\) `` (called the conclusion', '0\\\\) \'\' (called the conclusion'],
  // L158: stands for
  ['\\\\(Q\\\\) `` stands for', '\\\\(Q\\\\) \'\' stands for'],
  // L160: can fail
  ['Q\\\\) `` can fail', 'Q\\\\) \'\' can fail'],
  // L160: not Q is true
  ['\\\\(Q\\\\) `` is true', '\\\\(Q\\\\) \'\' is true'],
  // L160: not P is false
  ['\\\\(P\\\\) `` is false', '\\\\(P\\\\) \'\' is false'],
  // L160: not P as a proof
  ['\\\\(P\\\\) `` as a proof', '\\\\(P\\\\) \'\' as a proof'],
  // L478: is no longer
  ['1\\\\) `` is no longer', '1\\\\) \'\' is no longer'],
  // L696: and
  ['\\\\(y\\\\) `` and', '\\\\(y\\\\) \'\' and'],
  // L696: mean
  ['\\\\(y\\\\) `` mean', '\\\\(y\\\\) \'\' mean'],
  // L820: ; and
  ['\\\\(y\\\\) ``; and', '\\\\(y\\\\) \'\'; and'],
];

// Category C: Smart quote to LaTeX
const catC = [
  ['“If \\\\(x < 0\\\\)', "``If \\\\(x < 0\\\\)"],
];

let count = 0;
for (const [old, nw] of [...catA, ...catB, ...catC]) {
  if (c.includes(old)) {
    c = c.replace(old, nw);
    count++;
  } else {
    // Try without the double-backslash for inline math
    const old2 = old.replace(/\\\\\\\\/g, "\\\\");
    if (c.includes(old2)) {
      c = c.replace(old2, nw.replace(/\\\\\\\\/g, "\\\\"));
      count++;
    } else {
      console.log("NOT FOUND:", JSON.stringify(old).slice(0, 60));
    }
  }
}

fs.writeFileSync(fp, c);
console.log("Fixed " + count + " quote issues.");
