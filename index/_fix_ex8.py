with open("chapters/Chapter_1_Set_Theory_and_Logic.tex", "r", encoding="utf-8") as f:
    c = f.read()

old = r"greater cardinality than \({A}_{n}\) . *8. Show"
new = r"greater cardinality than \({A}_{n}\) ." + "\n\n" + r"\item *8. Show"

if old in c:
    c = c.replace(old, new)
    with open("chapters/Chapter_1_Set_Theory_and_Logic.tex", "w", encoding="utf-8") as f:
        f.write(c)
    print("Fixed!")
else:
    print("Not found; searching...")
    idx = c.find("greater cardinality than")
    if idx >= 0:
        print("Found:", repr(c[idx:idx+80]))
