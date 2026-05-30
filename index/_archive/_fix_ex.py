import re

with open("chapters/Chapter_1_Set_Theory_and_Logic.tex", "r", encoding="utf-8") as f:
    content = f.read()

# Fix exercise 4 corrupted lines
# Lines 1132-1136 (1-indexed) need to be replaced
lines = content.split("\n")

# Remove corrupted lines 1132-1136 (0-indexed: 1131-1135)
new_lines = [
    "\\item",
    "  \\begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\\alph*), align=left]",
    "  \\item Prove by induction that given \\(n \\in  {\\mathbb{Z}}_{ + }\\) , every nonempty subset of \\{ 1,\\ldots ,n\\} has a largest element.",
    "  \\item Explain why you cannot conclude from (a) that every nonempty subset of \\({\\mathbb{Z}}_{ + }\\) has a largest element.",
    "  \\end{enumerate}",
]

lines[1131:1136] = new_lines

with open("chapters/Chapter_1_Set_Theory_and_Logic.tex", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Exercise 4 fixed.")
