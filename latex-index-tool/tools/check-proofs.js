const fs = require("fs");
const backup = fs.readFileSync("chapters/Chapter_1_backup.tex", "utf8").replace(/\r\n/g, "\n");
const current = fs.readFileSync("chapters/Chapter_1_Set_Theory_and_Logic.tex", "utf8").replace(/\r\n/g, "\n");

function getBeforeEndProofs(text) {
  const results = [];
  const regex = /\\end\{proof\}/g;
  let match;
  while ((match = regex.exec(text)) !== null) {
    const start = Math.max(0, match.index - 80);
    const before = text.slice(start, match.index)
      .replace(/[\r\n]+/g, " ")
      .replace(/\s+/g, " ")
      .trim();
    results.push(before.slice(-60));
  }
  return results;
}

function getProofStarts(text) {
  const results = [];
  const regex = /\\begin\{proof\}/g;
  let match;
  while ((match = regex.exec(text)) !== null) {
    const after = text.slice(match.index + 13, match.index + 100)
      .replace(/[\r\n]+/g, " ")
      .replace(/\s+/g, " ")
      .trim();
    results.push(after.slice(0, 60));
  }
  return results;
}

const bBefore = getBeforeEndProofs(backup);
const cBefore = getBeforeEndProofs(current);
const bStarts = getProofStarts(backup);
const cStarts = getProofStarts(current);

console.log("=== PROOF MATCHING ===");
console.log("Backup: " + bStarts.length + " proofs, Current: " + cStarts.length + " proofs\n");

// For each current proof, find matching backup proof by start text
const usedBackup = new Set();

for (let ci = 0; ci < cStarts.length; ci++) {
  const cs = cStarts[ci].replace(/\s+/g, " ").trim();
  const csKey = cs.slice(0, 25).toLowerCase();

  let bestMatch = -1;
  let bestScore = 0;
  for (let bi = 0; bi < bStarts.length; bi++) {
    if (usedBackup.has(bi)) continue;
    const bs = bStarts[bi].replace(/\s+/g, " ").trim().toLowerCase();
    const bsKey = bs.slice(0, 25);
    // Count matching initial chars
    let score = 0;
    for (let j = 0; j < Math.min(csKey.length, bsKey.length); j++) {
      if (csKey[j] === bsKey[j]) score++;
    }
    if (score > bestScore) { bestScore = score; bestMatch = bi; }
  }

  const bar = bestScore >= 15 ? "MATCH" : (bestScore >= 8 ? "WEAK" : "MISMATCH");
  console.log(bar + "  Current #" + (ci + 1) + " -> Backup #" + (bestMatch >= 0 ? bestMatch + 1 : "?") + "  (score:" + bestScore + ")");
  console.log("  Start: " + cs.slice(0, 60));
  console.log("  End:   " + cBefore[ci].slice(-50));

  if (bar === "MISMATCH" || bar === "WEAK") {
    console.log("  *** CHECK THIS PROOF ***");
  }

  if (bestMatch >= 0) usedBackup.add(bestMatch);
  console.log("");
}

// Check for backup proofs not matched
console.log("=== UNMATCHED BACKUP PROOFS ===");
for (let bi = 0; bi < bStarts.length; bi++) {
  if (!usedBackup.has(bi)) {
    console.log("Backup #" + (bi + 1) + ": " + bStarts[bi]);
  }
}
