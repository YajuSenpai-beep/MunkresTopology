"""Fix idxmath entries with sorting text in display argument."""
import glob

FIXES = {
    r'\idxmath{R}{\(\mathbb{R}\) (reals)}': r'\idxmath{R}{\(\mathbb{R}\)}',
    r'\idxmath{S}{\({S}_{\alpha }\) (section of well-ordered set)}': r'\idxmath{S}{\({S}_{\alpha }\)}',
    r'\idxmath{n}{\(n\left( {f,a}\right)\) (see Winding number)}': r'\idxmath{n}{\(n\left( {f,a}\right)\)}',
    r'\idxmath{rho}{\(\rho\) (see also sup metric)}': r'\idxmath{rho}{\(\rho\)}',
    r'\idxmath{A}{\(\bar{A}\) (closure)}': r'\idxmath{A}{\(\bar{A}\)}',
    r'\idxmath{e}{\({e}_{x}\) (constant path)}': r'\idxmath{e}{\({e}_{x}\)}',
    r'\idxmath{H}{\({H}_{1}\left( X\right)\) (see First homology group)}': r'\idxmath{H}{\({H}_{1}\left( X\right)\)}',
    r'\idxmath{I}{\({I}_{o}^{2}\) (see Ordered square)}': r'\idxmath{I}{\({I}_{o}^{2}\)}',
    r'\idxmath{pi}{\({\pi }_{1}\left( {X,{x}_{0}}\right)\) (see also Fundamental group)}': r'\idxmath{pi}{\({\pi }_{1}\left( {X,{x}_{0}}\right)\)}',
}

total = 0
for fp in sorted(glob.glob("chapters/Chapter_*.tex")):
    if "backup" in fp or "test" in fp:
        continue
    with open(fp, "r", encoding="utf-8") as f:
        c = f.read()

    fixes = 0
    for old, new in FIXES.items():
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
