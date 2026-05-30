"""Fix remaining exercise formatting issues in Chapter 1."""
import re

with open("chapters/Chapter_1_Set_Theory_and_Logic.tex", "r", encoding="utf-8") as f:
    c = f.read()

fixes_applied = 0

# --- Fix 1: §5 Ex3(c) {A}_{t} -> {A}_{i} ---
old = r"{A}_{t} is nonempty"
new = r"{A}_{i} is nonempty"
if old in c:
    c = c.replace(old, new)
    fixes_applied += 1
    print("1. §5 Ex3(c): {A}_{t} -> {A}_{i}")

# --- Fix 2: §6 Ex1: (a) into sub-enumerate, f.\{ -> f : \{ ---
# First fix the colon
old = r"f.\{ 1,\ldots ,8\}"
new = r"f : \{ 1,\ldots ,8\}"
if old in c:
    c = c.replace(old, new)
    fixes_applied += 1
    print("2. §6 Ex1: f. -> f :")

# --- Fix 3: §6 Ex1: Move (a) content into sub-enumerate ---
old = r"""\item (a) Make a list of all the injective maps \[ f : \{ 1,2,3\}  \rightarrow  \{ 1,2,3,4\} . \] Show that none is bijective. (This constitutes a direct proof that a set \(A\) of cardinality three does not have cardinality four.)
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item How many injective maps"""
new = r"""\item
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Make a list of all the injective maps \[ f : \{ 1,2,3\}  \rightarrow  \{ 1,2,3,4\} . \] Show that none is bijective. (This constitutes a direct proof that a set \(A\) of cardinality three does not have cardinality four.)
  \item How many injective maps"""
if old in c:
    c = c.replace(old, new)
    fixes_applied += 1
    print("3. §6 Ex1: (a) into sub-enumerate")

# --- Fix 4: §6 Ex6: (a) into sub-enumerate ---
old = r"""\item (a) Let \(A = \{ 1,\ldots ,n\}\) . Show there is a bijection of \(\mathcal{P}\left( A\right)\) with the cartesian product \({X}^{n}\) , where \(X\) is the two-element set \(X = \{ 0,1\}\) .
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Show that if \(A\) is finite, then \(\mathcal{P}\left( A\right)\) is finite."""
new = r"""\item
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Let \(A = \{ 1,\ldots ,n\}\) . Show there is a bijection of \(\mathcal{P}\left( A\right)\) with the cartesian product \({X}^{n}\) , where \(X\) is the two-element set \(X = \{ 0,1\}\) .
  \item Show that if \(A\) is finite, then \(\mathcal{P}\left( A\right)\) is finite."""
if old in c:
    c = c.replace(old, new)
    fixes_applied += 1
    print("4. §6 Ex6: (a) into sub-enumerate")

# --- Fix 5: §7 Ex4: (a) into sub-enumerate ---
old = r"""\item (a) A real number \(x\) is said to be algebraic (over the rationals) if it satisfies some polynomial equation of positive degree \[ {x}^{n} + {a}_{n - 1}{x}^{n - 1} + \cdots  + {a}_{1}x + {a}_{0} = 0 \] with rational coefficients \({a}_{i}\) . Assuming that each polynomial equation has only finitely many roots, show that the set of \idx{algebraic number}s is countable.
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item A real number is said to be transcendental if it is not algebraic. Assuming the reals are uncountable, show that the \idx{transcendental number}s are uncountable."""
new = r"""\item
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item A real number \(x\) is said to be algebraic (over the rationals) if it satisfies some polynomial equation of positive degree \[ {x}^{n} + {a}_{n - 1}{x}^{n - 1} + \cdots  + {a}_{1}x + {a}_{0} = 0 \] with rational coefficients \({a}_{i}\) . Assuming that each polynomial equation has only finitely many roots, show that the set of \idx{algebraic number}s is countable.
  \item A real number is said to be transcendental if it is not algebraic. Assuming the reals are uncountable, show that the \idx{transcendental number}s are uncountable."""
if old in c:
    c = c.replace(old, new)
    fixes_applied += 1
    print("5. §7 Ex4: (a) into sub-enumerate")

# --- Fix 6: §7 Ex9: (a) into sub-enumerate ---
old = r"""\item (a) The formula \[ \left( *\right) \qquad \begin{aligned} h\left( 1\right)  &= 1, \\ h\left( 2\right)  &= 2\text{ , } \\ h\left( n\right)  &= {\left\lbrack  h\left( n + 1\right) \right\rbrack  }^{2} - {\left\lbrack  h\left( n - 1\right) \right\rbrack  }^{2}\;\text{ for }n \geq  2 \end{aligned} \] is not one to which the principle of recursive definition applies. Show that nevertheless there does exist a function \(h : {\mathbb{Z}}_{ + } \rightarrow  \mathbb{R}\) satisfying this formula. [Hint: Reformulate \(\left( *\right)\) so that the principle will apply and require \(h\) to be positive.]
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Show that the formula \(\left( *\right)\) of part (a) does not determine \(h\) uniquely."""
new = r"""\item
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item The formula \[ \left( *\right) \qquad \begin{aligned} h\left( 1\right)  &= 1, \\ h\left( 2\right)  &= 2\text{ , } \\ h\left( n\right)  &= {\left\lbrack  h\left( n + 1\right) \right\rbrack  }^{2} - {\left\lbrack  h\left( n - 1\right) \right\rbrack  }^{2}\;\text{ for }n \geq  2 \end{aligned} \] is not one to which the principle of recursive definition applies. Show that nevertheless there does exist a function \(h : {\mathbb{Z}}_{ + } \rightarrow  \mathbb{R}\) satisfying this formula. [Hint: Reformulate \(\left( *\right)\) so that the principle will apply and require \(h\) to be positive.]
  \item Show that the formula \(\left( *\right)\) of part (a) does not determine \(h\) uniquely."""
if old in c:
    c = c.replace(old, new)
    fixes_applied += 1
    print("6. §7 Ex9: (a) into sub-enumerate")

# --- Fix 7: §8 Ex3/4 line break ---
old = r"""special cases of Exercise 2. 4. The \idx{Fibonacci numbers}"""
new = r"""special cases of Exercise 2.

4. The \idx{Fibonacci numbers}"""
if old in c:
    c = c.replace(old, new)
    fixes_applied += 1
    print("7. §8 Ex3/4: line break")

# --- Fix 8: §8 Ex6: (a) into sub-enumerate ---
old = r"""\item (a) Show that there is no function \(h : {\mathbb{Z}}_{ + } \rightarrow  {\mathbb{R}}_{ + }\) satisfying the formula \[ \begin{aligned} h\left( 1\right)  &= 3, \\ h\left( i\right)  &= {\left\lbrack  h\left( i - 1\right)  - 1\right\rbrack  }^{1/2}\;\text{ for }i > 1. \end{aligned} \] Explain why this example does not violate the principle of recursive definition.
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Consider the recursion formula"""
new = r"""\item
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Show that there is no function \(h : {\mathbb{Z}}_{ + } \rightarrow  {\mathbb{R}}_{ + }\) satisfying the formula \[ \begin{aligned} h\left( 1\right)  &= 3, \\ h\left( i\right)  &= {\left\lbrack  h\left( i - 1\right)  - 1\right\rbrack  }^{1/2}\;\text{ for }i > 1. \end{aligned} \] Explain why this example does not violate the principle of recursive definition.
  \item Consider the recursion formula"""
if old in c:
    c = c.replace(old, new)
    fixes_applied += 1
    print("8. §8 Ex6: (a) into sub-enumerate")

# --- Fix 9: §9 Ex5: (a) into sub-enumerate ---
old = r"""\item (a) Use the choice axiom to show that if \(f : A \rightarrow  B\) is surjective, then \(f\) has a right inverse \(h \cdot  B \rightarrow  A\) .
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Show that if \(f : A \rightarrow  B\) is injective and \(A\) is not empty, then \(f\) has a left inverse. Is the axiom of choice needed?"""
new = r"""\item
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Use the choice axiom to show that if \(f : A \rightarrow  B\) is surjective, then \(f\) has a right inverse \(h \cdot  B \rightarrow  A\) .
  \item Show that if \(f : A \rightarrow  B\) is injective and \(A\) is not empty, then \(f\) has a left inverse. Is the axiom of choice needed?"""
if old in c:
    c = c.replace(old, new)
    fixes_applied += 1
    print("9. §9 Ex5: (a) into sub-enumerate")

# --- Fix 10: §9 Ex8 split from Ex7(d) ---
old = r"""cardinality than \({A}_{n}\) . *8. Show that \(\mathcal{P}\left( {\mathbb{Z}}_{ + }\right)\)"""
new = r"""cardinality than \({A}_{n}\) .

\item *8. Show that \(\mathcal{P}\left( {\mathbb{Z}}_{ + }\right)\)"""
if old in c:
    c = c.replace(old, new)
    fixes_applied += 1
    print("10. §9 Ex8: split from Ex7")

# --- Fix 11: §10 Ex2: (a) into sub-enumerate ---
old = r"""\item (a) Show that in a well-ordered set, every element except the largest (if one exists) has an immediate successor.
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Find a set in which every element has an immediate successor that is not well-ordered."""
new = r"""\item
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Show that in a well-ordered set, every element except the largest (if one exists) has an immediate successor.
  \item Find a set in which every element has an immediate successor that is not well-ordered."""
if old in c:
    c = c.replace(old, new)
    fixes_applied += 1
    print("11. §10 Ex2: (a) into sub-enumerate")

# --- Fix 12: §10 Ex4: (a) into sub-enumerate ---
old = r"""\item (a) Let \({\mathbb{Z}}_{ - }\) denote the set of negative integers in the usual order. Show that a simply ordered set \(A\) fails to be well-ordered if and only if it contains a subset having the same order type as \({\mathbb{Z}}_{ - }\) .
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Show that if \(A\) is simply ordered and every countable subset of \(A\) is well-ordered, then \(A\) is well-ordered."""
new = r"""\item
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Let \({\mathbb{Z}}_{ - }\) denote the set of negative integers in the usual order. Show that a simply ordered set \(A\) fails to be well-ordered if and only if it contains a subset having the same order type as \({\mathbb{Z}}_{ - }\) .
  \item Show that if \(A\) is simply ordered and every countable subset of \(A\) is well-ordered, then \(A\) is well-ordered."""
if old in c:
    c = c.replace(old, new)
    fixes_applied += 1
    print("12. §10 Ex4: (a) into sub-enumerate")

# --- Fix 13: §10 Ex8: (a) into sub-enumerate ---
old = r"""\item (a) Let \({A}_{1}\) and \({A}_{2}\) be \idx{disjoint sets}, well-ordered by \({ < }_{1}\) and \({ < }_{2}\) , respectively. Define an order relation on \({A}_{1} \cup  {A}_{2}\) by letting \(a < b\) either if \(a,b \in  {A}_{1}\) and \(a{ < }_{1}b\) , or if \(a,b \in  {A}_{2}\) and \(a{ < }_{2}b\) , or if \(a \in  {A}_{1}\) and \(b \in  {A}_{2}\) . Show that this is a well-ordering
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Generalize (a) to an arbitrary family of disjoint well-ordered sets, indexed by a well-ordered set."""
new = r"""\item
  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]
  \item Let \({A}_{1}\) and \({A}_{2}\) be \idx{disjoint sets}, well-ordered by \({ < }_{1}\) and \({ < }_{2}\) , respectively. Define an order relation on \({A}_{1} \cup  {A}_{2}\) by letting \(a < b\) either if \(a,b \in  {A}_{1}\) and \(a{ < }_{1}b\) , or if \(a,b \in  {A}_{2}\) and \(a{ < }_{2}b\) , or if \(a \in  {A}_{1}\) and \(b \in  {A}_{2}\) . Show that this is a well-ordering
  \item Generalize (a) to an arbitrary family of disjoint well-ordered sets, indexed by a well-ordered set."""
if old in c:
    c = c.replace(old, new)
    fixes_applied += 1
    print("13. §10 Ex8: (a) into sub-enumerate")

# --- Save ---
with open("chapters/Chapter_1_Set_Theory_and_Logic.tex", "w", encoding="utf-8") as f:
    f.write(c)

print(f"\nTotal fixes applied: {fixes_applied}")
