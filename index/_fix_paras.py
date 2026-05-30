with open("chapters/Chapter_1_Set_Theory_and_Logic.tex", "r", encoding="utf-8") as f:
    c = f.read()

fixes = [
    (r"] \\This same argument", "]\n\nThis same argument"),
    (r"X\) . \\This exercise shows", "X\) .\n\nThis exercise shows"),
    (r"axiom. \\Said differently", "axiom.\n\nSaid differently"),
]

count = 0
for old, new in fixes:
    if old in c:
        c = c.replace(old, new)
        count += 1
    else:
        print("Not found:", old[:50])

with open("chapters/Chapter_1_Set_Theory_and_Logic.tex", "w", encoding="utf-8") as f:
    f.write(c)
print(f"Fixed {count}/{len(fixes)}")
