with open("chapters/Chapter_1_Set_Theory_and_Logic.tex", "r", encoding="utf-8") as f:
    c = f.read()

old = r"""\item Show that if \(n > 1\) there is bijective correspondence of \[ {A}_{1} \times  \cdots  \times  {A}_{n}\;\text{ with }\;\left( {{A}_{1} \times  \cdots  \times  {A}_{n - 1}}\right)  \times  {A}_{n}. \]
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Given the indexed family"""

new = r"""\item
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Show that if \(n > 1\) there is bijective correspondence of \[ {A}_{1} \times  \cdots  \times  {A}_{n}\;\text{ with }\;\left( {{A}_{1} \times  \cdots  \times  {A}_{n - 1}}\right)  \times  {A}_{n}. \]
  \item Given the indexed family"""

if old in c:
    c = c.replace(old, new)
    with open("chapters/Chapter_1_Set_Theory_and_Logic.tex", "w", encoding="utf-8") as f:
        f.write(c)
    print("Fixed!")
else:
    # Debug
    idx = c.find(r"Show that if \(n > 1\)")
    if idx >= 0:
        snippet = c[idx-10:idx+len(old)+10]
        print("Expected:", repr(old[:60]))
        print("Found:   ", repr(snippet[:80]))
    else:
        print("Not found at all")
