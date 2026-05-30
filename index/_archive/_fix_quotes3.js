const fs = require("fs");
const fp = "chapters/Chapter_1_Set_Theory_and_Logic.tex";
let c = fs.readFileSync(fp, "utf8");

const S = String.raw;

const fixes = [
  // Category A: ,'' → , ``
  [S`sentence,''Every`, S`sentence, ``Every`],
  [S`formally,''For every`, S`formally, ``For every`],
  [S`the form,''If \(P\)`, S`the form, ``If \(P\)`],
  [S`as saying,''If \(x \in`, S`as saying, ``If \(x \in`],
  [S`by saying,''Let \(A\)`, S`by saying, ``Let \(A\)`],

  // Category B: `` X `` Y → `` X '' Y
  [S`\(Q\) `` means`, S`\(Q\) '' means`],
  [S`\(Q\) `` always means`, S`\(Q\) '' always means`],
  [S`0\) `` (called the hypothesis`, S`0\) '' (called the hypothesis`],
  [S`0\) `` (called the conclusion`, S`0\) '' (called the conclusion`],
  [S`\(Q\) `` stands for`, S`\(Q\) '' stands for`],
  [S`Q\) `` can fail`, S`Q\) '' can fail`],
  [S`\(Q\) `` is true`, S`\(Q\) '' is true`],
  [S`\(P\) `` is false`, S`\(P\) '' is false`],
  [S`\(P\) `` as a proof`, S`\(P\) '' as a proof`],
  [S`1\) `` is no longer`, S`1\) '' is no longer`],
  [S`\(y\) `` and`, S`\(y\) '' and`],
  [S`\(y\) `` mean`, S`\(y\) '' mean`],
  [S`\(y\) ``; and`, S`\(y\) '' ; and`],

  // Category C: Unicode smart quote → LaTeX
  [S`"If \(x < 0\)`, S```If \(x < 0\)`],
];

let count = 0;
for (const [old, nw] of fixes) {
  if (c.includes(old)) {
    c = c.replace(old, nw);
    count++;
  } else {
    console.log("NOT FOUND:", JSON.stringify(old).slice(0, 50));
  }
}

fs.writeFileSync(fp, c);
console.log("Fixed " + count + "/" + fixes.length + " quote issues.");
