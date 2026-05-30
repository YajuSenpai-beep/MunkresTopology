with open("chapters/Chapter_1_Set_Theory_and_Logic.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the exact line range for exercise 2 of §11
# Look for the three lines that need changing
target_old = r"  \item \(a \preccurlyeq  a\) for all \(a \in  A\) . (ii) \(a \preccurlyeq  b\) and \(b \preccurlyeq  a \Rightarrow  a = b\) . (iii) \(a \preccurlyeq  b\) and \(b \preccurlyeq  c \Rightarrow  a \preccurlyeq  c\) ."

for i, line in enumerate(lines):
    if target_old in line:
        indent = line[:len(line) - len(line.lstrip())]
        subindent = indent + "  "

        # Replace this line with three separate sub-items in a sub-sub-enumerate
        replacement = [
            subindent + "\\begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\\roman*), align=left]\n",
            subindent + "\\item \\(a \\preccurlyeq  a\\) for all \\(a \\in  A\\) .\n",
            subindent + "\\item \\(a \\preccurlyeq  b\\) and \\(b \\preccurlyeq  a \\Rightarrow  a = b\\) .\n",
            subindent + "\\item \\(a \\preccurlyeq  b\\) and \\(b \\preccurlyeq  c \\Rightarrow  a \\preccurlyeq  c\\) .\n",
            subindent + "\\end{enumerate}\n",
        ]

        lines[i:i+1] = replacement
        print(f"Fixed at line {i+1}")
        break

with open("chapters/Chapter_1_Set_Theory_and_Logic.tex", "w", encoding="utf-8") as f:
    f.writelines(lines)
print("Done")
