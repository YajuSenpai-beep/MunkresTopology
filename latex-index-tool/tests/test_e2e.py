r"""End-to-end integration tests — full CLI pipeline with mock project.

These tests create a complete LaTeX project directory structure and
exercise CLI paths that cannot be reached by unit tests alone.
"""

import json
import os
import subprocess
import sys
import tempfile

import pytest


@pytest.fixture(scope="module")
def mock_project():
    """Create a complete mock LaTeX project with multiple chapters."""
    tmpdir = tempfile.mkdtemp(prefix="latex_index_e2e_")
    project = {"root": tmpdir}

    # chapters/
    chapters_dir = os.path.join(tmpdir, "chapters")
    os.makedirs(chapters_dir)

    # Chapter 1: with exercises and examples
    ch1 = os.path.join(chapters_dir, "Chapter_1_Introduction.tex")
    with open(ch1, "w", encoding="utf-8") as f:
        f.write(r"\section{Topology}" + "\n")
        f.write(r"The concept of a field is central to modern mathematics." + "\n")
        f.write(r"A field is a set with two operations, called addition and multiplication." + "\n")
        f.write(r"\begin{theorem}Every field is a ring.\end{theorem}" + "\n")
        f.write(r"\begin{example}The real numbers form a field.\end{example}" + "\n")
        f.write(r"\section*{Exercises}" + "\n")
        f.write(r"1. Prove that every field is an integral domain." + "\n")
        f.write(r"2. Show that the integers modulo p form a field." + "\n")
        f.write(r"3. (a) Define a topology on the set of all fields." + "\n")
        f.write(r"   (b) Show it is Hausdorff." + "\n")
        f.write(r"\section*{Advanced Topics}" + "\n")
        f.write(r"The notion of a field can be generalized." + "\n")
    project["ch1"] = ch1

    # Chapter 2
    ch2 = os.path.join(chapters_dir, "Chapter_2_Basics.tex")
    with open(ch2, "w", encoding="utf-8") as f:
        f.write(r"\section{Compact Spaces}" + "\n")
        f.write(r"A topological space is compact if every open cover has a finite subcover." + "\n")
        f.write(r"The real line is not compact." + "\n")
        f.write(r"\begin{lemma}[Key Lemma]Every closed subset of a compact space is compact.\end{lemma}" + "\n")
    project["ch2"] = ch2

    # Main file
    main = os.path.join(tmpdir, "main.tex")
    with open(main, "w", encoding="utf-8") as f:
        f.write(r"\documentclass{article}" + "\n")
        f.write(r"\begin{document}" + "\n")
        f.write(r"\input{chapters/Chapter_1_Introduction}" + "\n")
        f.write(r"\include{chapters/Chapter_2_Basics}" + "\n")
        f.write(r"\end{document}" + "\n")
    project["main"] = main

    # Config
    config_dir = os.path.join(tmpdir, "index", "config")
    os.makedirs(config_dir)
    cfg = os.path.join(config_dir, "default.yaml")
    with open(cfg, "w", encoding="utf-8") as f:
        f.write("version: 1\n")
        f.write("index_processor: makeindex\n")
        f.write("templates:\n")
        f.write("  l1: \\idx{${key}}\n")
        f.write("  l1Math: \\idxmath{${sort}}{${display}}\n")
        f.write("  l2: \\idxsub{${parent}}{${child}}\n")
        f.write("file_pattern: Chapter_${num}_*.tex\n")
        f.write("chapter_source_dir: " + chapters_dir.replace("\\", "/") + "\n")
        f.write("aliases:\n")
        f.write("  field: [algebraic structure]\n")
        f.write("math_shortcuts: {}\n")
        f.write("skip_patterns: []\n")
        f.write("log_level: INFO\n")
        f.write("log_file: e2e_test.log\n")
    project["config"] = cfg

    # Entries JSON
    data_dir = os.path.join(tmpdir, "index", "data")
    os.makedirs(data_dir)
    entries_file = os.path.join(data_dir, "ch01_entries.json")
    entries = [
        {"term": "field", "level": 1, "page": [1]},
        {"term": "compact space", "level": 1, "page": [5]},
        {"term": "finite subcover", "level": 2, "parent": "compact space", "page": [5]},
        {"term": "Hausdorff", "level": 1, "page": [8]},
    ]
    with open(entries_file, "w", encoding="utf-8") as f:
        json.dump(entries, f)
    project["entries"] = entries_file

    # Candidates file
    cand_file = os.path.join(data_dir, "candidates.txt")
    with open(cand_file, "w", encoding="utf-8") as f:
        f.write("field\ncompact\nHausdorff\nalgebra\n")
    project["candidates"] = cand_file

    # Index text (simulated OCR output)
    idx_file = os.path.join(data_dir, "raw_index.txt")
    with open(idx_file, "w", encoding="utf-8") as f:
        f.write("field, 1\n")
        f.write("  finite field, 3\n")
        f.write("compact space, 5\n")
        f.write("  open cover, 5\n")
        f.write("  finite subcover, 5\n")
    project["idx_text"] = idx_file

    yield project

    # Cleanup
    import shutil
    shutil.rmtree(tmpdir, ignore_errors=True)


def _run(*args: str, cwd: str = "") -> subprocess.CompletedProcess:
    """Run latex-index CLI command via main() with captured output."""
    import io
    import latex_index.cli as cli_mod
    old_argv = sys.argv
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    try:
        sys.argv = ["latex-index"] + list(args)
        captured_out = io.StringIO()
        captured_err = io.StringIO()
        sys.stdout = captured_out
        sys.stderr = captured_err
        old_cwd = os.getcwd()
        index_dir = os.path.dirname(os.path.dirname(__file__))
        os.chdir(cwd or index_dir)
        exit_code = 0
        try:
            cli_mod.main()
        except SystemExit as e:
            exit_code = e.code or 0
        return subprocess.CompletedProcess(
            args, exit_code,
            stdout=captured_out.getvalue(),
            stderr=captured_err.getvalue(),
        )
    finally:
        sys.argv = old_argv
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        os.chdir(old_cwd)


class TestE2EInsert:
    """End-to-end insert command tests."""

    def test_insert_chapter_mode(self, mock_project):
        """Insert via --chapter using real chapter files."""
        index_dir = os.path.join(mock_project["root"], "index")
        r = _run(
            "insert",
            "--config", mock_project["config"],
            "--chapter", "1",
            "--entries", mock_project["entries"],
            "--dry-run",
        )
        assert r.returncode == 0

    def test_insert_with_progress(self, mock_project):
        r = _run(
            "insert",
            "--config", mock_project["config"],
            "--chapter", "1",
            "--entries", mock_project["entries"],
            "--dry-run",
            "--progress",
        )
        assert r.returncode == 0

    def test_insert_main_mode(self, mock_project):
        """Insert via --main (multi-file project)."""
        r = _run(
            "insert",
            "--config", mock_project["config"],
            "--main", mock_project["main"],
            "--entries", mock_project["entries"],
            "--dry-run",
        )
        assert r.returncode == 0

    def test_insert_l1_only(self, mock_project):
        r = _run(
            "insert",
            "--config", mock_project["config"],
            "--chapter", "1",
            "--entries", mock_project["entries"],
            "--dry-run",
            "--l1-only",
        )
        assert r.returncode == 0

    def test_insert_fast_mode(self, mock_project):
        r = _run(
            "insert",
            "--config", mock_project["config"],
            "--chapter", "1",
            "--entries", mock_project["entries"],
            "--dry-run",
            "--fast",
        )
        assert r.returncode == 0

    def test_insert_help(self):
        r = _run("insert", "--help")
        assert r.returncode == 0
        assert "usage" in r.stdout.lower() or "参数" in r.stdout


class TestE2EParse:
    """End-to-end parse command tests."""

    def test_parse_to_json(self, mock_project):
        out = os.path.join(mock_project["root"], "parsed.json")
        r = _run("parse", mock_project["idx_text"], "-o", out)
        assert r.returncode == 0
        assert os.path.exists(out)
        with open(out, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert len(data["entries"]) >= 3

    def test_parse_run_in_format(self, mock_project):
        out = os.path.join(mock_project["root"], "runin.json")
        r = _run("parse", mock_project["idx_text"], "--format", "run-in", "-o", out)
        assert r.returncode == 0

    def test_parse_stdout(self, mock_project):
        r = _run("parse", mock_project["idx_text"])
        assert r.returncode == 0
        assert "entries" in r.stdout

    def test_parse_missing_file(self):
        r = _run("parse", "/nonexistent/file.txt")
        assert r.returncode == 1


class TestE2EScan:
    """End-to-end scan command tests."""

    def test_scan_chapter(self, mock_project):
        r = _run("scan", mock_project["ch1"])
        assert r.returncode == 0

    def test_scan_to_file(self, mock_project):
        out = os.path.join(mock_project["root"], "scan_report.txt")
        r = _run("scan", mock_project["ch1"], "-o", out)
        assert r.returncode == 0
        assert os.path.exists(out)


class TestE2EReport:
    """End-to-end report command tests."""

    def test_report_basic(self, mock_project):
        r = _run("report", mock_project["ch1"])
        assert r.returncode == 0

    def test_report_with_entries(self, mock_project):
        r = _run(
            "report", mock_project["ch1"],
            "--entries", mock_project["entries"],
        )
        assert r.returncode == 0

    def test_report_with_candidates(self, mock_project):
        r = _run(
            "report", mock_project["ch1"],
            "--candidates", mock_project["candidates"],
        )
        assert r.returncode == 0

    def test_report_to_file(self, mock_project):
        out = os.path.join(mock_project["root"], "index_report.txt")
        r = _run(
            "report", mock_project["ch1"],
            "--entries", mock_project["entries"],
            "-o", out,
        )
        assert r.returncode == 0
        assert os.path.exists(out)


class TestE2ETools:
    """End-to-end tools subcommand tests."""

    def test_format_env(self, mock_project):
        r = _run(
            "tools", "format-env",
            "--files", mock_project["ch1"],
        )
        assert r.returncode == 0

    def test_convert_exercises(self, mock_project):
        r = _run(
            "tools", "convert-exercises",
            "--files", mock_project["ch1"],
        )
        assert r.returncode == 0

    def test_clean_ex_envs(self, mock_project):
        r = _run(
            "tools", "clean-ex-envs",
            "--files", mock_project["ch1"],
        )
        assert r.returncode == 0

    def test_fix_subitems(self, mock_project):
        r = _run(
            "tools", "fix-subitems",
            "--files", mock_project["ch1"],
        )
        assert r.returncode == 0

    def test_ocr_fix(self, mock_project):
        # Create a file with known OCR errors
        fp = os.path.join(mock_project["root"], "ocr_test.tex")
        with open(fp, "w", encoding="utf-8") as f:
            f.write(r"Siliarly, Structly speaking.")
        r = _run("tools", "ocr-fix", "--files", fp)
        assert r.returncode == 0
        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()
        assert "Similarly" in content

    def test_scan_issues(self, mock_project):
        r = _run("tools", "scan-issues", "--files", mock_project["ch1"])
        assert r.returncode == 0

    def test_wrap_examples(self, mock_project):
        r = _run("tools", "wrap-examples", "--files", mock_project["ch1"])
        assert r.returncode == 0

    def test_continue_on_error(self, mock_project):
        r = _run(
            "tools", "wrap-examples",
            "--files", mock_project["ch1"], "/nonexistent/file.tex",
            "--continue-on-error",
        )
        assert r.returncode == 0


class TestE2ESetup:
    """End-to-end setup and xindy commands."""

    def test_setup(self, mock_project):
        r = _run("setup", "--project-dir", mock_project["root"])
        assert r.returncode == 0
        assert os.path.exists(os.path.join(mock_project["root"], ".latexmkrc"))

    def test_setup_no_backup(self, mock_project):
        r = _run("setup", "--project-dir", mock_project["root"], "--no-backup")
        assert r.returncode == 0

    def test_xindy_list_langs(self):
        r = _run("xindy", "--list-langs")
        assert r.returncode == 0
        assert "english" in r.stdout.lower()

    def test_xindy_generate(self, mock_project):
        out = os.path.join(mock_project["root"], "style.xdy")
        r = _run(
            "xindy",
            "--languages", "english", "chinese-pinyin",
            "-o", out,
        )
        assert r.returncode == 0
        assert os.path.exists(out)


class TestE2EPipeline:
    """Full pipeline: parse → insert → report."""

    def test_full_workflow(self, mock_project):
        """Complete workflow from raw index text to final report."""
        # Step 1: Parse OCR text
        parsed = os.path.join(mock_project["root"], "entries.json")
        r = _run("parse", mock_project["idx_text"], "-o", parsed)
        assert r.returncode == 0

        # Step 2: Dry-run insert
        r = _run(
            "insert",
            "--config", mock_project["config"],
            "--chapter", "1",
            "--entries", parsed,
            "--dry-run",
        )
        assert r.returncode == 0

        # Step 3: Generate report
        r = _run(
            "report", mock_project["ch1"],
            "--entries", parsed,
            "--candidates", mock_project["candidates"],
        )
        assert r.returncode == 0
        assert "覆盖率" in r.stdout or "命中" in r.stdout or "coverage" in r.stdout.lower()

    def test_multi_chapter_workflow(self, mock_project):
        """Process multiple chapters."""
        for ch_num in [1, 2]:
            r = _run(
                "insert",
                "--config", mock_project["config"],
                "--chapter", str(ch_num),
                "--entries", mock_project["entries"],
                "--dry-run",
            )
            assert r.returncode == 0
