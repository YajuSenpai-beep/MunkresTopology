r"""Fix problematic \idx entries: split plurals and descriptive sorting text."""
import glob

# Type A: split plurals: \idx{field}s -> \idx[fields]{field}
TYPE_A = {
    r"\idx{field}s": r"\idx[fields]{field}",
    r"\idx{relation}s": r"\idx[relations]{relation}",
    r"\idx{injective function}s": r"\idx[injective functions]{injective function}",
    r"\idx{surjective function}s": r"\idx[surjective functions]{surjective function}",
    r"\idx{bijective function}s": r"\idx[bijective functions]{bijective function}",
    r"\idx{equivalence relation}s": r"\idx[equivalence relations]{equivalence relation}",
    r"\idx{order relation}s": r"\idx[order relations]{order relation}",
    r"\idx{rational number}s": r"\idx[rational numbers]{rational number}",
    r"\idx{Finite Set}s": r"\idx[Finite Sets]{Finite Set}",
    r"\idx{infinite set}s": r"\idx[infinite sets]{infinite set}",
    r"\idx{countable set}s": r"\idx[countable sets]{countable set}",
    r"\idx{uncountable set}s": r"\idx[uncountable sets]{uncountable set}",
    r"\idx{algebraic number}s": r"\idx[algebraic numbers]{algebraic number}",
    r"\idx{transcendental number}s": r"\idx[transcendental numbers]{transcendental number}",
    r"\idx{continuous function}s": r"\idx[continuous functions]{continuous function}",
    r"\idx{closed set}s": r"\idx[closed sets]{closed set}",
    r"\idx{limit point}s": r"\idx[limit points]{limit point}",
    r"\idx{connected space}s": r"\idx[connected spaces]{connected space}",
    r"\idx{component}s": r"\idx[components]{component}",
    r"\idx{connected component}s": r"\idx[connected components]{connected component}",
    r"\idx{path component}s": r"\idx[path components]{path component}",
    r"\idx{metric space}s": r"\idx[metric spaces]{metric space}",
    r"\idx{complete metric space}s": r"\idx[complete metric spaces]{complete metric space}",
    r"\idx{product space}s": r"\idx[product spaces]{product space}",
    r"\idx{locally finite collection}s": r"\idx[locally finite collections]{locally finite collection}",
    r"\idx{paracompact space}s": r"\idx[paracompact spaces]{paracompact space}",
    r"\idx{covering}s": r"\idx[coverings]{covering}",
    r"\idx{direct sum}s": r"\idx[direct sums]{direct sum}",
    r"\idx{free abelian group}s": r"\idx[free abelian groups]{free abelian group}",
    r"\idx{maximum principle}s": r"\idx[maximum principles]{maximum principle}",
    r"\idx{convergent sequence}s": r"\idx[convergent sequences]{convergent sequence}",
    r"\idx{bounded function}s": r"\idx[bounded functions]{bounded function}",
    r"\idx{closed ray}s": r"\idx[closed rays]{closed ray}",
    r"\idx{open ray}s": r"\idx[open rays]{open ray}",
    r"\idx{half-open interval}s": r"\idx[half-open intervals]{half-open interval}",
    r"\idx{closed map}s": r"\idx[closed maps]{closed map}",
    r"\idx{coordinate function}s": r"\idx[coordinate functions]{coordinate function}",
    r"\idx{nowhere-differentiable function}s": r"\idx[nowhere-differentiable functions]{nowhere-differentiable function}",
    r"\idx{quasicomponent}s": r"\idx[quasicomponents]{quasicomponent}",
    r"\idx{right coset}s": r"\idx[right cosets]{right coset}",
    r"\idx{projection map}p": r"\idx[projection mapping]{projection map}",
    r"\idx{path-homotopy class}e": r"\idx[path-homotopy classes]{path-homotopy class}",
    r"\idx{compactly generated space}s": r"\idx[compactly generated spaces]{compactly generated space}",
    r"\idx{Deformation Retract}s": r"\idx[Deformation Retracts]{Deformation Retract}",
    r"\idx{Covering Space}s": r"\idx[Covering Spaces]{Covering Space}",
    r"\idx{Direct Sum}s": r"\idx[Direct Sums]{Direct Sum}",
}

# Type B: descriptive sorting text -> separate display
TYPE_B = {
    r"\idx{Section: of the positive integers}": r"\idx[section]{Section: of the positive integers}",
    r"\idx{Choice axiom (see Axiom of choice)}": r"\idx[choice axiom]{Choice axiom (see Axiom of choice)}",
    r"\idx{Recursive definition, principle}": r"\idx[principle of recursive definition]{Recursive definition, principle}",
    r"\idx{Operation, binary}": r"\idx[binary operation]{Operation, binary}",
    r"\idx{Quantifiers, logical}": r"\idx[logical quantifiers]{Quantifiers, logical}",
    r"\idx{Standard topology: on}": r"\idx[standard topology]{Standard topology: on}",
    r"\idx{Interior point: of an arc}": r"\idx[interior point]{Interior point: of an arc}",
    r"\idx{Lifting lemma: general}": r"\idx[general lifting lemma]{Lifting lemma: general}",
    r"\idx{Imbedding theorem: for a compact manifold}": r"\idx[imbedding theorem]{Imbedding theorem: for a compact manifold}",
    r"\idx{Subgroup: of free abelian group}": r"\idx[subgroup]{Subgroup: of free abelian group}",
    r"\idx{Logical equivalence}": r"\idx[logical identity]{Logical equivalence}",
    r"\idx{Barber of Seville paradox}": r"\idx[barber of Seville]{Barber of Seville paradox}",
    r"\idx{Product: of continuous maps}": r"\idx[product]{Product: of continuous maps}",
    r"\idx{Topologist's sine curve (cont.): connectedness}": r"\idx[topologist's sine curve]{Topologist's sine curve (cont.): connectedness}",
    r"\idx{Uniform metric (see also Uniform topology)}": r"\idx[uniform metric]{Uniform metric (see also Uniform topology)}",
    r"\idx{Second-countable space (see also Second-countability)}": r"\idx[second-countable space]{Second-countable space (see also Second-countability)}",
    r"\idx{Regular space (see also Regularity)}": r"\idx[regular space]{Regular space (see also Regularity)}",
    r"\idx{Quotient space (see also Quotient topology)}": r"\idx[quotient space]{Quotient space (see also Quotient topology)}",
    r"\idx{Separable (see also Countable dense subset)}": r"\idx[separable]{Separable (see also Countable dense subset)}",
    r"\idx{Square metric (see also )}": r"\idx[square metric]{Square metric (see also )}",
    r"\idx{Derivative: of }": r"\idx[derivative]{Derivative: of }",
    r"\idx{Initial point: of an oriented line segment}": r"\idx[initial point]{Initial point: of an oriented line segment}",
    r"\idx{Vertex: of a curved triangle}": r"\idx[vertex]{Vertex: of a curved triangle}",
    r"\idx{Restriction: of a covering map}": r"\idx[restriction]{Restriction: of a covering map}",
    r"\idx{Slice: in covering space}": r"\idx[slice]{Slice: in covering space}",
    r"\idx{Regular Lindelof space: metrizability}": r"\idx[regular Lindelof space]{Regular Lindelof space: metrizability}",
    r"\idx{Pointwise convergence topology (see also Point-open topology)}": r"\idx[pointwise convergence topology]{Pointwise convergence topology (see also Point-open topology)}",
    r"\idx{Positive linear map: of intervals in}": r"\idx[positive linear map]{Positive linear map: of intervals in}",
    r"\idx{Metrizability: of compact Hausdorff space}": r"\idx[metrizability]{Metrizability: of compact Hausdorff space}",
    r"\idx{Maximum value theorem: of calculus}": r"\idx[maximum value theorem]{Maximum value theorem: of calculus}",
    r"\idx{Locally compact Hausdorff space: Baire condition}": r"\idx[locally compact Hausdorff space]{Locally compact Hausdorff space: Baire condition}",
    r"\idx{Generated: by elements}": r"\idx[generated]{Generated: by elements}",
    r"\idx{Classification: of covering spaces}": r"\idx[classification]{Classification: of covering spaces}",
    r"\idx{Free homotopy of loops}": r"\idx[free homotopy]{Free homotopy of loops}",
    r"\idx{First-countable space (see First-countability)}": r"\idx[first-countable space]{First-countable space (see First-countability)}",
    r"\idx{Closed topologist's sine curve}": r"\idx[closed topologist's sine curve]{Closed topologist's sine curve}",
    r"\idx{Finiteness: of cartesian products}": r"\idx[finiteness]{Finiteness: of cartesian products}",
    r"\idx{Distributive laws for  and}": r"\idx[distributive laws]{Distributive laws for  and}",
    r"\idx{Convergence of sequences: with }": r"\idx[convergence of sequences]{Convergence of sequences: with }",
    r"\idx{Topological completeness (see also Complete metric space)}": r"\idx[topological completeness]{Topological completeness (see also Complete metric space)}",
}

# Type C: OCR errors
TYPE_C = {
    r"\idx{Infinite senes}": r"\idx[infinite-dimensional euclidean space]{infinite series}",
}

ALL = {**TYPE_A, **TYPE_B, **TYPE_C}

total = 0
for fp in sorted(glob.glob("chapters/Chapter_*.tex")):
    if "backup" in fp or "test" in fp:
        continue
    with open(fp, "r", encoding="utf-8") as f:
        c = f.read()

    fixes = 0
    for old, new in ALL.items():
        if old in c:
            c = c.replace(old, new)
            fixes += 1

    if fixes > 0:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(c)
        name = fp.replace("chapters/Chapter_", "").replace(".tex", "").replace("_", " ")
        print(f"{name}: {fixes} fixes")
        total += fixes

print(f"\nTotal: {total} fixes")
