// Restore all Ch1 manual formatting changes
const fs = require("fs");
const fp = "chapters/Chapter_1_Set_Theory_and_Logic.tex";
let c = fs.readFileSync(fp, "utf8");

// 1. Lemma 7.2 wrapping
c = c.replace(
  "Lemma 7.2. If \\(C\\) is an infinite subset of \\({\\mathbb{Z}}_{ + }\\) , then \\(C\\) is countably infinite.\n\n\\begin{proof}",
  "\\begin{lemma}\nIf \\(C\\) is an infinite subset of \\({\\mathbb{Z}}_{ + }\\) , then \\(C\\) is countably infinite.\n\\end{lemma}\n\n\\begin{proof}"
);

// 2. Axiom of choice bold+noindent (line 2426)
c = c.replace(
  "Axiom of choice. Given a collection",
  "\\noindent \\textbf{Axiom of choice.} Given a collection"
);

// 3. Proof of the lemma + A second proof wrappers
c = c.replace(
  "Proof of the lemma. Given an element",
  "\\begin{proof}[Proof of the lemma.] Given an element"
);
c = c.replace(
  "as desired.\n\nA second proof of Theorem 9.1.",
  "as desired.\n\\end{proof}\n\nA second proof of Theorem 9.1."
);
c = c.replace(
  "A second proof of Theorem 9.1. Using this lemma",
  "\\begin{proof}[A second proof of Theorem 9.1.] Using this lemma"
);
c = c.replace(
  "Injectivity of \\(f\\) follows as before.\n\nHaving emphasized",
  "Injectivity of \\(f\\) follows as before.\n\\end{proof}\n\nHaving emphasized"
);

// 4. Corollary* (line 2674)
c = c.replace(
  "\\section*{Corollary. There exists an uncountable well-ordered set.}",
  "\\begin{ucorollary}\nThere exists an uncountable well-ordered set.\n\\end{ucorollary}"
);

// 5. Math nesting fixes
c = c.replace(
  "For at least one \\(x \\in  A\\) , statement \\(P\\) does not hold.\n\\]",
  "\\text{For at least one } x \\in  A \\text{, statement } P \\text{ does not hold.}\n\\]"
);
c = c.replace(
  "For every \\(x \\in  A\\) , statement \\(Q\\) does not hold.\n\\]",
  "\\text{For every } x \\in  A \\text{, statement } Q \\text{ does not hold.}\n\\]"
);

// 6. Equation merges with (*) tags - first pair
c = c.replace(
  "(*)\n\\[\nh\\left( 1\\right)  = \\text{ smallest element of }C\\text{ , }\n\\]\n\n\\[\nh\\left( i\\right)  = \\text{ smallest element of }\\left\\lbrack  {C - h\\left( {\\{ 1,\\ldots ,i - 1\\} }\\right) }\\right\\rbrack  \\;\\text{ for all }i > 1\\text{ . }\n\\]",
  "\\[\n\\left( *\\right) \\qquad\n\\begin{gathered}\nh\\left( 1\\right)  = \\text{ smallest element of }C\\text{ , } \\\\\nh\\left( i\\right)  = \\text{ smallest element of }\\left\\lbrack  {C - h\\left( {\\{ 1,\\ldots ,i - 1\\} }\\right) }\\right\\rbrack  \\;\\text{ for all }i > 1\\text{ . }\n\\end{gathered}\n\\]"
);

// 7. Second (*) formula pair
c = c.replace(
  "\\[\nh\\left( 1\\right)  = \\text{ smallest element of }C\\text{ , }\n\\]\n\\[\nh\\left( i\\right)  = \\text{ smallest element of }\\left\\lbrack  {C - h\\left( {\\{ 1,\\ldots ,i - 1\\} }\\right) }\\right\\rbrack  \\;\\text{ for }i > 1\\text{ . }\n\\]\n\nWe shall prove",
  "\\[\n\\left( *\\right) \\qquad\n\\begin{gathered}\nh\\left( 1\\right)  = \\text{ smallest element of }C\\text{ , } \\\\\nh\\left( i\\right)  = \\text{ smallest element of }\\left\\lbrack  {C - h\\left( {\\{ 1,\\ldots ,i - 1\\} }\\right) }\\right\\rbrack  \\;\\text{ for }i > 1\\text{ . }\n\\end{gathered}\n\\]\n\nWe shall prove"
);

// 8. f/f' equation merge
c = c.replace(
  "\\[\nf\\left( i\\right)  = {f}^{\\prime }\\left( i\\right) \\;\\text{ for }i \\in  \\{ 1,\\ldots ,n - 1\\} ,\n\\]\n\n\\[\nf\\left( n\\right)  = \\text{ smallest element of }\\left\\lbrack  {C - {f}^{\\prime }\\left( {\\{ 1,\\ldots ,n - 1\\} }\\right) }\\right\\rbrack  .\n\\]",
  "\\[\n\\begin{gathered}\nf\\left( i\\right)  = {f}^{\\prime }\\left( i\\right) \\;\\text{ for }i \\in  \\{ 1,\\ldots ,n - 1\\} , \\\\\nf\\left( n\\right)  = \\text{ smallest element of }\\left\\lbrack  {C - {f}^{\\prime }\\left( {\\{ 1,\\ldots ,n - 1\\} }\\right) }\\right\\rbrack  .\n\\end{gathered}\n\\]"
);

// 9. f/g equation merge
c = c.replace(
  "\\[\nf\\left( i\\right)  = \\text{ smallest element of }\\lbrack C - f\\left( {\\{ 1,\\ldots ,i - 1\\} }\\right) \\} ,\n\\]\n\n\\[\ng\\left( i\\right)  = \\text{ smallest element of }\\left\\lbrack  {C - g\\left( {\\{ 1,\\ldots ,i - 1\\} }\\right) }\\right\\rbrack  \\text{ . }\n\\]",
  "\\[\n\\begin{gathered}\nf\\left( i\\right)  = \\text{ smallest element of }\\lbrack C - f\\left( {\\{ 1,\\ldots ,i - 1\\} }\\right) \\} , \\\\\ng\\left( i\\right)  = \\text{ smallest element of }\\left\\lbrack  {C - g\\left( {\\{ 1,\\ldots ,i - 1\\} }\\right) }\\right\\rbrack  \\text{ . }\n\\end{gathered}\n\\]"
);

// 10. h(i)/f_n equation merge
c = c.replace(
  "    \\[\n    h\\left( i\\right)  = {f}_{n}\\left( i\\right) \\;\\text{ for }i \\leq  n,\n    \\]\n\n\\[\n{f}_{n}\\text{ satisfies }\\left( *\\right) \\text{ for all }i\\text{ in its domain. }\n\\]",
  "    \\[\n    \\begin{gathered}\n    h\\left( i\\right)  = {f}_{n}\\left( i\\right) \\;\\text{ for }i \\leq  n, \\\\\n    {f}_{n}\\text{ satisfies }\\left( *\\right) \\text{ for all }i\\text{ in its domain. }\n    \\end{gathered}\n    \\]"
);

// 11. h(1)=a0, h(i)=ρ with (*)
c = c.replace(
  "(*)\n\\[\nh\\left( 1\\right)  = {a}_{0},\n\\]\n\\[\nh\\left( i\\right)  = \\rho \\left( {h|\\{ 1,\\ldots ,i - 1\\} }\\right) \\;\\text{ for }i > 1.\n\\]",
  "\\[\n\\left( *\\right) \\qquad\n\\begin{gathered}\nh\\left( 1\\right)  = {a}_{0}, \\\\\nh\\left( i\\right)  = \\rho \\left( {h|\\{ 1,\\ldots ,i - 1\\} }\\right) \\;\\text{ for }i > 1.\n\\end{gathered}\n\\]"
);

// 12. 3-equation chain aligned
c = c.replace(
  "\\[\nh\\left( i\\right)  = \\rho \\left( {h|\\{ 1,\\ldots ,i - 1\\} }\\right)\n\\]\n\n\\[\n= \\text{ smallest element of }\\left\\lbrack  {C - \\left( {\\text{ image set of }h \\mid  \\{ 1,\\ldots ,i - 1\\} }\\right) }\\right\\rbrack\n\\]\n\n\\[\n= \\text{ smallest element of }\\left\\lbrack  {C - h\\left( {\\{ 1\\ldots ,i - 1\\} }\\right) }\\right\\rbrack  \\text{ , }\n\\]",
  "\\[\n\\begin{aligned}\nh\\left( i\\right)  &= \\rho \\left( {h|\\{ 1,\\ldots ,i - 1\\} }\\right) \\\\\n&= \\text{ smallest element of }\\left\\lbrack  {C - \\left( {\\text{ image set of }h \\mid  \\{ 1,\\ldots ,i - 1\\} }\\right) }\\right\\rbrack \\\\\n&= \\text{ smallest element of }\\left\\lbrack  {C - h\\left( {\\{ 1\\ldots ,i - 1\\} }\\right) }\\right\\rbrack  \\text{ , }\n\\end{aligned}\n\\]"
);

// 13. g equations aligned
c = c.replace(
  "    \\[\n    g\\left( {a}_{n}\\right)  = {a}_{n + 1}\\;\\text{ for }{a}_{n} \\in  B.\n    \\]\n    \\[\n    g\\left( x\\right)  = x\\;\\text{ for }x \\in  A - B.\n    \\]",
  "    \\[\n    \\begin{aligned}\n    g\\left( {a}_{n}\\right)  &= {a}_{n + 1}\\;\\text{ for }{a}_{n} \\in  B, \\\\\n    g\\left( x\\right)  &= x\\;\\text{ for }x \\in  A - B.\n    \\end{aligned}\n    \\]"
);

// 14. f(1)=a1, f(i)=arbitrary with (*)
c = c.replace(
  "(*)\n\\[\nf\\left( 1\\right)  = {a}_{1},\n\\]\n\n\\[\nf\\left( i\\right)  = \\text{ an arbitrary element of }\\left\\lbrack  {A - f\\left( {\\{ 1,\\ldots ,i - 1\\} }\\right) }\\right\\rbrack  \\;\\text{ for }i > 1\\text{ . }\n\\]",
  "\\[\n\\left( *\\right) \\qquad\n\\begin{aligned}\nf\\left( 1\\right)  &= {a}_{1}, \\\\\nf\\left( i\\right)  &= \\text{ an arbitrary element of }\\left\\lbrack  {A - f\\left( {\\{ 1,\\ldots ,i - 1\\} }\\right) }\\right\\rbrack  \\;\\text{ for }i > 1\\text{ . }\n\\end{aligned}\n\\]"
);

// 15. h(1)/h(i) third occurrence aligned
c = c.replace(
  "\\[\nh\\left( 1\\right)  = \\text{ smallest element of }C\\text{ , }\n\\]\n\n\\[\nh\\left( i\\right)  = \\text{ smallest element of }\\left\\lbrack  {C - h\\left( {\\{ 1,\\ldots ,i - 1\\} }\\right) }\\right\\rbrack  \\;\\text{ for }i > 1\\text{ . }\n\\]\nThis formula does define",
  "\\[\n\\begin{aligned}\nh\\left( 1\\right)  &= \\text{ smallest element of }C\\text{ , } \\\\\nh\\left( i\\right)  &= \\text{ smallest element of }\\left\\lbrack  {C - h\\left( {\\{ 1,\\ldots ,i - 1\\} }\\right) }\\right\\rbrack  \\;\\text{ for }i > 1\\text{ . }\n\\end{aligned}\n\\]\nThis formula does define"
);

// 16. f(1)=c(A), f(i)=c(...) with (*)
c = c.replace(
  "(*)\n\\[\nf\\left( 1\\right)  = c\\left( A\\right)\n\\]\n\n\\[\nf\\left( i\\right)  = c\\left( {A - f\\left( {\\{ 1,\\ldots ,i - 1\\} }\\right) }\\right) \\;\\text{ for }i > 1.\n\\]",
  "\\[\n\\left( *\\right) \\qquad\n\\begin{aligned}\nf\\left( 1\\right)  &= c\\left( A\\right) \\\\\nf\\left( i\\right)  &= c\\left( {A - f\\left( {\\{ 1,\\ldots ,i - 1\\} }\\right) }\\right) \\;\\text{ for }i > 1.\n\\end{aligned}\n\\]"
);

// 17. f/f' x≠b aligned
c = c.replace(
  "    \\[\n    f\\left( x\\right)  = {f}^{\\prime }\\left( x\\right) \\;\\text{ for }x \\neq  b,\n    \\]\n    \\[\n    f\\left( b\\right)  = n\\text{ . }\n    \\]",
  "    \\[\n    \\begin{aligned}\n    f\\left( x\\right)  &= {f}^{\\prime }\\left( x\\right) \\;\\text{ for }x \\neq  b, \\\\\n    f\\left( b\\right)  &= n\\text{ . }\n    \\end{aligned}\n    \\]"
);

// 18. 4-set Z alignment
c = c.replace(
  "\\[\n{\\mathbb{Z}}_{ + }\\text{ , }\n\\]\n\n\\[\n\\{ 1,\\ldots ,n\\}  \\times  {\\mathbb{Z}}_{ + },\n\\]\n\n\\[\n{\\mathbb{Z}}_{ + } \\times  {\\mathbb{Z}}_{ + }\n\\]\n\n\\[\n{\\mathbb{Z}}_{ + } \\times  \\left( {{\\mathbb{Z}}_{ + } \\times  {\\mathbb{Z}}_{ + }}\\right)\n\\]",
  "\\[\n\\begin{aligned}\n&{\\mathbb{Z}}_{ + }\\text{ , } \\\\\n&\\{ 1,\\ldots ,n\\}  \\times  {\\mathbb{Z}}_{ + }, \\\\\n&{\\mathbb{Z}}_{ + } \\times  {\\mathbb{Z}}_{ + } \\\\\n&{\\mathbb{Z}}_{ + } \\times  \\left( {{\\mathbb{Z}}_{ + } \\times  {\\mathbb{Z}}_{ + }}\\right)\n\\end{aligned}\n\\]"
);

// 19. a^1/a^n three pairs in the example
c = c.replace(
  "\\[\n{a}^{1} = a\n\\]\n\n\\[\n{a}^{n} = {a}^{n - 1} \\cdot  a\n\\]\n\nWe wish to apply Theorem 8.4",
  "\\[\n\\begin{aligned}\n{a}^{1} &= a \\\\\n{a}^{n} &= {a}^{n - 1} \\cdot  a\n\\end{aligned}\n\\]\n\nWe wish to apply Theorem 8.4"
);

c = c.replace(
  "\\[\nh\\left( 1\\right)  = {a}_{0},\n\\]\n\n\\[\nh\\left( i\\right)  = \\rho \\left( {h|\\{ 1,\\ldots ,i - 1\\} }\\right) \\;\\text{ for }i > 1.\n\\]\n\nThis means that",
  "\\[\n\\begin{aligned}\nh\\left( 1\\right)  &= {a}_{0}, \\\\\nh\\left( i\\right)  &= \\rho \\left( {h|\\{ 1,\\ldots ,i - 1\\} }\\right) \\;\\text{ for }i > 1.\n\\end{aligned}\n\\]\n\nThis means that"
);

c = c.replace(
  "\\[\n{a}^{1} = a,\n\\]\n\n\\[\n{a}^{l} = {a}^{l - 1} \\cdot  a\n\\]\n\nas desired.",
  "\\[\n\\begin{aligned}\n{a}^{1} &= a, \\\\\n{a}^{l} &= {a}^{l - 1} \\cdot  a\n\\end{aligned}\n\\]\n\nas desired."
);

fs.writeFileSync(fp, c);
console.log("Ch1 restored.");
