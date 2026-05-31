"""Fix remaining idx entries with sorting notation in display."""
import glob

TYPE_D = {
    r"\idx{Ball, unit}": r"\idx[unit ball]{Ball, unit}",
    r"\idx{Basis: for a free abelian group}": r"\idx[basis]{Basis: for a free abelian group}",
    r"\idx{Boundary: of a set}": r"\idx[boundary]{Boundary: of a set}",
    r"\idx{Cardinality: comparability}": r"\idx[cardinality]{Cardinality: comparability}",
    r"\idx{Cartesian product: countably infinite}": r"\idx[cartesian product]{Cartesian product: countably infinite}",
    r"\idx{Closure (cont.)}": r"\idx[closure]{Closure (cont.)}",
    r"\idx{Compact Hausdorff space: is Baire space}": r"\idx[compact Hausdorff space]{Compact Hausdorff space: is Baire space}",
    r"\idx{Comparability: of cardinalities}": r"\idx[comparability]{Comparability: of cardinalities}",
    r"\idx{Complete regularity (cont.)}": r"\idx[complete regularity]{Complete regularity (cont.)}",
    r"\idx{Completeness: and Baire condition}": r"\idx[completeness]{Completeness: and Baire condition}",
    r"\idx{Composite: of functions}": r"\idx[composite]{Composite: of functions}",
    r"\idx{Connected sum: of projective planes}": r"\idx[connected sum]{Connected sum: of projective planes}",
    r"\idx{Continuity: of algebraic operations in}": r"\idx[continuity]{Continuity: of algebraic operations in}",
    r"\idx{Continuous image: of a compact space}": r"\idx[continuous image]{Continuous image: of a compact space}",
    r"\idx{Convex set: in an ordered set}": r"\idx[convex set]{Convex set: in an ordered set}",
    r"\idx{Coordinate: of J-tuple}": r"\idx[coordinate]{Coordinate: of J-tuple}",
    r"\idx{Dimension, topological}": r"\idx[topological dimension]{Dimension, topological}",
    r"\idx{Edge: of curved triangle}": r"\idx[edge]{Edge: of curved triangle}",
    r"\idx{Extension condition: for direct sums}": r"\idx[extension condition]{Extension condition: for direct sums}",
    r"\idx{Final point: of oriented line segment}": r"\idx[final point]{Final point: of oriented line segment}",
    r"\idx{First homotopy group (see Fundamental group)}": r"\idx[first homotopy group]{First homotopy group (see Fundamental group)}",
    r"\idx{Intervals in : compactness}": r"\idx[intervals]{Intervals in : compactness}",
    r"\idx{Regular Lindelof space: metrizability}": r"\idx[regular Lindelof space]{Regular Lindelof space: metrizability}",
}

total = 0
for fp in sorted(glob.glob("chapters/Chapter_*.tex")):
    if "backup" in fp or "test" in fp:
        continue
    with open(fp, "r", encoding="utf-8") as f:
        c = f.read()

    fixes = 0
    for old, new in TYPE_D.items():
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
