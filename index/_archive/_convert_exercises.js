const fs = require("fs");
const fp = "chapters/Chapter_1_Set_Theory_and_Logic.tex";
let c = fs.readFileSync(fp, "utf8");

// Split into lines for processing
const lines = c.split("\n");

// Find all exercise blocks
const blocks = [];
let inBlock = false;
let blockStart = -1;

for (let i = 0; i < lines.length; i++) {
  const L = lines[i];
  const isEx = L.includes("\\section*{Exercises}") || L.includes("\\section*{* Supplementary");
  const isNextSec = L.includes("\\section*{") && !isEx;

  if (isEx) {
    if (inBlock) blocks.push({ start: blockStart, end: i - 1 });
    inBlock = true;
    blockStart = i;
  } else if (isNextSec && inBlock) {
    blocks.push({ start: blockStart, end: i - 1 });
    inBlock = false;
  }
}
if (inBlock) blocks.push({ start: blockStart, end: lines.length - 1 });

console.log("Found " + blocks.length + " exercise blocks");

// Process each block (skip #1 which is already done)
for (let b = 1; b < blocks.length; b++) {
  const start = blocks[b].start;
  const end = blocks[b].end;
  console.log("\nBlock #" + (b + 1) + " lines " + (start + 1) + "-" + (end + 1));

  // Extract lines from after \section*{Exercises} to end of block
  const blockLines = lines.slice(start + 1, end + 1);

  // Parse exercises: numbered items and subparts
  const items = [];
  let currentItem = null;

  for (let i = 0; i < blockLines.length; i++) {
    const L = blockLines[i].trim();
    if (!L) continue;

    // Check if this line starts a new numbered exercise
    const numMatch = L.match(/^(\d+)\.\s/);
    if (numMatch) {
      if (currentItem) items.push(currentItem);
      currentItem = {
        num: parseInt(numMatch[1]),
        text: L.replace(/^\d+\.\s/, ""),
        subparts: [],
      };
      continue;
    }

    // Check if this line is a subpart (a), (b), etc.
    const subMatch = L.match(/^\(([a-z])\)\s/);
    if (subMatch && currentItem) {
      currentItem.subparts.push({
        letter: subMatch[1],
        text: L.replace(/^\([a-z]\)\s/, ""),
      });
      continue;
    }

    // Check if this line continues a subpart (starts with a formula or continuation)
    if (currentItem && currentItem.subparts.length > 0 && !L.match(/^\d+\.\s/) && !L.match(/^\([a-z]\)\s/)) {
      // Append to last subpart
      currentItem.subparts[currentItem.subparts.length - 1].text += " " + L;
      continue;
    }

    // Otherwise, append to current item text
    if (currentItem) {
      currentItem.text += " " + L;
    }
  }
  if (currentItem) items.push(currentItem);

  // Build the new content
  const newLines = [lines[start]]; // \section*{Exercises}

  newLines.push("\\begin{enumerate}[itemsep=0.4em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=\\arabic*., ref=\\arabic*]");

  for (const item of items) {
    if (item.subparts.length > 0) {
      // Item with subparts
      newLines.push("\\item " + item.text);
      newLines.push("  \\begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\\alph*), align=left]");
      for (const sub of item.subparts) {
        newLines.push("  \\item " + sub.text);
      }
      newLines.push("  \\end{enumerate}");
    } else {
      // Simple item
      newLines.push("\\item " + item.text);
    }
  }

  newLines.push("\\end{enumerate}");

  // Replace the block content
  lines.splice(start, end - start + 1, ...newLines);

  // Adjust blocks after this one since line count changed
  const delta = newLines.length - (end - start + 1);
  for (let j = b + 1; j < blocks.length; j++) {
    blocks[j].start += delta;
    blocks[j].end += delta;
  }

  console.log("  " + items.length + " exercises, " + items.reduce((s, it) => s + (it.subparts.length > 0 ? 1 : 0), 0) + " with subparts");
}

fs.writeFileSync(fp, lines.join("\n"));
console.log("\nDone. All exercise blocks converted.");
