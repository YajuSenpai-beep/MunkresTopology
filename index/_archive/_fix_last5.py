with open("chapters/Chapter_1_Set_Theory_and_Logic.tex", "r", encoding="utf-8") as f:
    c = f.read()

fixes = [
    # §3 Ex9
    (
        r"""\item (a) Show that the map \(f : \left( {-1,1}\right)  \rightarrow  \mathbb{R}\) of Example 9 is order preserving.
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Show that the equation""",
        r"""\item
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Show that the map \(f : \left( {-1,1}\right)  \rightarrow  \mathbb{R}\) of Example 9 is order preserving.
  \item Show that the equation"""
    ),
    # §4 Ex? (greatest lower bound)
    (
        r"""\item (a) Show that \(\mathbb{R}\) has the greatest lower bound property.
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Show that every nonempty""",
        r"""\item
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Show that \(\mathbb{R}\) has the greatest lower bound property.
  \item Show that every nonempty"""
    ),
    # §4 Ex? (bounded above)
    (
        r"""\item (a) Show that every nonempty subset of \(\mathbb{Z}\) that is bounded above has a largest element.
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item If \(x \notin  {\mathbb{Z}}_{ + }\)""",
        r"""\item
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Show that every nonempty subset of \(\mathbb{Z}\) that is bounded above has a largest element.
  \item If \(x \notin  {\mathbb{Z}}_{ + }\)"""
    ),
    # §11 Ex2
    (
        r"""\item (a) Let \(\prec\) be a strict partial order on the set \(A\) . Define a relation on \(A\) by letting \(a \preccurlyeq  b\) if either \(a \prec  b\) or \(a = b\) . Show that this relation has the following properties, which are called the partial order axioms:
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Let \(P\) be a relation on \(A\)""",
        r"""\item
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Let \(\prec\) be a strict partial order on the set \(A\) . Define a relation on \(A\) by letting \(a \preccurlyeq  b\) if either \(a \prec  b\) or \(a = b\) . Show that this relation has the following properties, which are called the partial order axioms:
  \item Let \(P\) be a relation on \(A\)"""
    ),
    # Supplementary Ex2
    (
        r"""\item (a) Let \(J\) and \(E\) be well-ordered sets, let \(h : J \rightarrow  E\) . Show the following two statements are equivalent:
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Show that""",
        r"""\item
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Let \(J\) and \(E\) be well-ordered sets, let \(h : J \rightarrow  E\) . Show the following two statements are equivalent:
  \item Show that"""
    ),
]

count = 0
for old, new in fixes:
    if old in c:
        c = c.replace(old, new)
        count += 1
    else:
        print("NOT FOUND:", old[:60])

with open("chapters/Chapter_1_Set_Theory_and_Logic.tex", "w", encoding="utf-8") as f:
    f.write(c)
print(f"Fixed {count}/{len(fixes)}")
