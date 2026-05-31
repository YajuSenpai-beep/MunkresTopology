"""Scan Ch2-Ch14 for all known OCR error patterns from Ch1 experience."""
import re, os, glob

chapters_dir = "chapters"
backup_dir = "original/chapters_backup"
files = sorted(glob.glob(f"{chapters_dir}/Chapter_*[2-9]*.tex")) + \
        sorted(glob.glob(f"{chapters_dir}/Chapter_1[0-4]*.tex"))

results = {}

for fp in files:
    name = os.path.basename(fp).replace("Chapter_", "").replace(".tex", "").replace("_", " ")
    with open(fp, "r", encoding="utf-8") as f:
        c = f.read()
    lines = c.split("\n")

    issues = {
        "spelling": [], "colon_period": [], "colon_cdot": [],
        "bracket_mismatch": [], "math_font": [], "missing_period": [],
        "straight_quotes": [], "unbalanced_quotes": [],
        "rbrack": [], "star_marker": [], "exercise_merged": [],
        "centeredblock_missing": [], "long_lines": [],
    }

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("%"):
            continue

        # 1. Known misspellings
        for pat, correct in [("ongin", "origin"), ("posiave", "positive"),
                              ("Structly", "Strictly"), ("ngorously", "rigorously"),
                              ("conduction", "condition"), ("Schernatically", "Schematically"),
                              ("simplyby", "simply by"), ("Siliarly", "Similarly")]:
            if pat in line:
                issues["spelling"].append(f"L{i}: '{pat}' -> '{correct}'")

        # 2. Period-for-colon: f.A -> f : A
        m = re.findall(r"\\\(([a-z])\.\s*\\mathbb|\\\(([a-z])\.\s*\{|\\\(([a-z])\.\s*\{\\", line)
        if m:
            issues["colon_period"].append(f"L{i}: {stripped[:80]}")

        # 3. cdot-for-colon in function context
        if "\\cdot" in line and ("function" in stripped.lower()[:30] or
            "surjection" in stripped.lower()[:30] or "injection" in stripped.lower()[:30] or
            "bijection" in stripped.lower()[:30] or "map" in stripped.lower()[:10]):
            issues["colon_cdot"].append(f"L{i}: {stripped[:80]}")

        # 4. Bracket mismatches
        if "\\rbrack" in line and "\\right\\rbrack" not in line and "\\left\\lbrack" not in line:
            issues["rbrack"].append(f"L{i}: {stripped[:80]}")
        if stripped.endswith("\\}") and "[Hint" in stripped:
            issues["bracket_mismatch"].append(f"L{i}: Hint ends with }}: {stripped[:80]}")

        # 5. Math font: \mathbf{Z} etc
        for pat in [r"\{\\mathbf\{Z\}\}", r"\\mathbf\{A\}", r"\\mathbf\{C\}"]:
            if re.search(pat, line):
                issues["math_font"].append(f"L{i}: {pat} in: {stripped[:80]}")

        # 6. Missing period: [a-z] [A-Z] pattern (crude)
        # Skip math mode and commands
        if re.search(r"[a-z]\s+[A-Z][a-z]", stripped[:100]):
            # Check for common OCR patterns
            for pat in ["is empty On", "is empty Not", "disjoint It", "surjective For",
                       "countable Since", "countable Its", "Given ", "set Given",
                       "uncountable Then", "versions Formulated", "however Specifically",
                       "theorem", "integers"]:
                if pat in line:
                    issues["missing_period"].append(f"L{i}: '{pat}': {stripped[:80]}")
                    break

        # 7. Straight double quotes
        m = re.findall(r'"([A-Za-z][^"]*[A-Za-z])"', stripped)
        if m:
            issues["straight_quotes"].append(f"L{i}: {m}")

        # 8. Unbalanced LaTeX quotes
        open_q = stripped.count("``")
        close_q = stripped.count("''")
        if open_q != close_q and (open_q > 0 or close_q > 0):
            # Skip if it's just math double-primes
            mathless = re.sub(r"\$[^$]*\$|\\\([^)]*\\\)|\\\[[^\]]*\\\]", "", stripped)
            if mathless.count("``") != mathless.count("''"):
                issues["unbalanced_quotes"].append(f"L{i}: ({open_q}`` vs {close_q}''): {stripped[:80]}")

        # 9. Raw (*) not in math mode
        if re.search(r"\(\*\)", stripped) and "\\left" not in stripped and "\\(" not in stripped:
            issues["star_marker"].append(f"L{i}: raw (*): {stripped[:80]}")

        # 10. Long lines
        if len(line) > 250:
            issues["long_lines"].append(f"L{i}: {len(line)} chars")

    # 11. Check centeredblock coverage
    example_count = c.count("\\begin{example}")
    cb_count = c.count("\\begin{centeredblock}")
    if example_count > cb_count:
        issues["centeredblock_missing"].append(
            f"{example_count} examples but only {cb_count} centeredblocks (missing ~{example_count - cb_count})")

    # 12. Check exercise formatting
    ex_blocks = c.count("\\section*{Exercises}")
    enumerate_blocks = len(re.findall(r"\\begin\{enumerate\}.*?label=\\arabic", c))
    if ex_blocks > enumerate_blocks:
        issues["exercise_merged"].append(
            f"{ex_blocks} exercise sections but only {enumerate_blocks} with enumerate formatting")

    # Summary
    total = sum(len(v) for v in issues.values())
    results[name] = {"total": total, "issues": issues, "lines": len(lines)}

# Print summary
print("# Ch2-Ch14 OCR Error Scan Report\n")
print("| Chapter | Lines | Total Issues | Spelling | Quotes | Bracket | Font | Period | Colon | Star | Other |")
print("|---------|-------|-------------|----------|--------|---------|------|--------|-------|------|-------|")

for name, data in results.items():
    iss = data["issues"]
    counts = [
        data["lines"],
        data["total"],
        len(iss["spelling"]), len(iss["unbalanced_quotes"]) + len(iss["straight_quotes"]),
        len(iss["rbrack"]) + len(iss["bracket_mismatch"]), len(iss["math_font"]),
        len(iss["missing_period"]), len(iss["colon_period"]) + len(iss["colon_cdot"]),
        len(iss["star_marker"]),
        len(iss["centeredblock_missing"]) + len(iss["exercise_merged"]) + len(iss["long_lines"]),
    ]
    print(f"| {name} | " + " | ".join(str(c) for c in counts) + " |")

print(f"\n## Grand Total Issues: {sum(d['total'] for d in results.values())}")
