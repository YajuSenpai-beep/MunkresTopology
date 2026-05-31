r"""Tests for CLI command functions.

Tests command functions directly via argparse.Namespace to cover cli.py (0% → target 60%+).
"""

import argparse
import json
import os
import tempfile

import pytest

from latex_index.cli import (
    atomic_write,
    cmd_insert,
    cmd_parse,
    cmd_scan,
    setup_logging,
)


@pytest.fixture
def tmp_tex():
    """Create a temporary .tex file with content."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".tex", delete=False, encoding="utf-8"
    ) as f:
        f.write(r"\section{Topology}" + "\n")
        f.write("The concept of a field is central to modern mathematics.\n")
        f.write("A field is a set with two operations.\n")
        f.write(r"\section*{Exercises}" + "\n")
        f.write("1. Prove this.\n")
        path = f.name
    yield path
    try:
        os.unlink(path)
    except OSError:
        pass


@pytest.fixture
def tmp_entries():
    """Create a temporary entries JSON file."""
    entries = [
        {"term": "field", "level": 1, "page": [1]},
        {"term": "topology", "level": 1, "page": [5]},
    ]
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as f:
        json.dump(entries, f)
        path = f.name
    yield path
    try:
        os.unlink(path)
    except OSError:
        pass


class TestCmdInsert:
    def test_insert_with_main_file(self, tmp_tex, tmp_entries):
        args = argparse.Namespace(
            config=None,
            chapter=None,
            entries=tmp_entries,
            dry_run=True,
            l1_only=False,
            main=tmp_tex,
            fast=False,
            interactive=False,
            progress=False,
        )
        result = cmd_insert(args)
        assert result == 0

    def test_l1_only_filter(self, tmp_tex, tmp_entries):
        args = argparse.Namespace(
            config=None,
            chapter=None,
            entries=tmp_entries,
            dry_run=True,
            l1_only=True,
            main=tmp_tex,
            fast=False,
            interactive=False,
            progress=False,
        )
        result = cmd_insert(args)
        assert result == 0

    def test_missing_entries_file(self):
        args = argparse.Namespace(
            config=None,
            chapter=None,
            entries="/nonexistent/file.json",
            dry_run=True,
            l1_only=False,
            main=None,
            fast=False,
            interactive=False,
            progress=False,
        )
        result = cmd_insert(args)
        assert result == 1  # error


class TestCmdParse:
    def test_parse_indented_format(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write("Axiom of choice, 42\n  choice function, 43\n")
            path = f.name
        try:
            args = argparse.Namespace(
                input=path, format="indented", output=None, command="parse"
            )
            result = cmd_parse(args)
            assert result == 0
        finally:
            os.unlink(path)

    def test_parse_with_output_file(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write("compact, 1\n")
            path = f.name
        out_path = path + ".out.json"
        try:
            args = argparse.Namespace(
                input=path, format="indented", output=out_path, command="parse"
            )
            result = cmd_parse(args)
            assert result == 0
            assert os.path.exists(out_path)
        finally:
            os.unlink(path)
            try:
                os.unlink(out_path)
            except OSError:
                pass

    def test_parse_missing_file(self):
        args = argparse.Namespace(
            input="/nonexistent/index.txt",
            format="indented",
            output=None,
            command="parse",
        )
        result = cmd_parse(args)
        assert result == 1  # error

    def test_parse_run_in_format(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write("compact, 1; connected, 2; Hausdorff, 3\n")
            path = f.name
        try:
            args = argparse.Namespace(
                input=path, format="run-in", output=None, command="parse"
            )
            result = cmd_parse(args)
            assert result == 0
        finally:
            os.unlink(path)


class TestCmdScan:
    def test_scan_tex_file(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tex", delete=False, encoding="utf-8"
        ) as f:
            f.write(r"\index{compact} and \idx{topology}")
            path = f.name
        try:
            args = argparse.Namespace(input=path, output=None, command="scan")
            result = cmd_scan(args)
            assert result == 0
        finally:
            os.unlink(path)

    def test_scan_with_output(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tex", delete=False, encoding="utf-8"
        ) as f:
            f.write(r"\index{field}")
            path = f.name
        out_path = path + ".report.txt"
        try:
            args = argparse.Namespace(input=path, output=out_path, command="scan")
            result = cmd_scan(args)
            assert result == 0
            assert os.path.exists(out_path)
        finally:
            os.unlink(path)
            try:
                os.unlink(out_path)
            except OSError:
                pass

    def test_scan_missing_file(self):
        args = argparse.Namespace(
            input="/nonexistent/file.tex", output=None, command="scan"
        )
        result = cmd_scan(args)
        assert result == 1


class TestAtomicWrite:
    def test_write_and_read(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.tex")
            atomic_write(path, r"\section{Hello}")
            with open(path, "r", encoding="utf-8") as f:
                assert f.read() == r"\section{Hello}"

    def test_overwrite_existing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.tex")
            with open(path, "w", encoding="utf-8") as f:
                f.write("original")
            atomic_write(path, "updated")
            with open(path, "r", encoding="utf-8") as f:
                assert f.read() == "updated"

    def test_special_characters(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test file.tex")
            atomic_write(path, "café naïve 中文")
            with open(path, "r", encoding="utf-8") as f:
                assert "中文" in f.read()


class TestSetupLogging:
    def test_default_level(self):
        setup_logging("INFO", "test_index.log")
        import logging
        root = logging.getLogger("index_tool")
        assert root.level == logging.INFO
        try:
            os.unlink("test_index.log")
        except OSError:
            pass

    def test_debug_level(self):
        setup_logging("DEBUG", "test_debug.log")
        import logging
        root = logging.getLogger("index_tool")
        assert root.level == logging.DEBUG
        try:
            os.unlink("test_debug.log")
        except OSError:
            pass

    def test_warning_level(self):
        setup_logging("WARNING", "test_warn.log")
        import logging
        root = logging.getLogger("index_tool")
        assert root.level == logging.WARNING
        try:
            os.unlink("test_warn.log")
        except OSError:
            pass


class TestMainEntry:
    """Test main() and module-level entry points."""

    def test_main_no_args_exits(self):
        from latex_index.cli import main
        import sys
        old_argv = sys.argv
        try:
            sys.argv = ["latex-index"]
            with pytest.raises(SystemExit) as exc:
                main()
            assert exc.value.code != 0  # exits with error for no command
        finally:
            sys.argv = old_argv

    def test_main_help_ok(self):
        from latex_index.cli import main
        import sys
        old_argv = sys.argv
        try:
            sys.argv = ["latex-index", "--help"]
            with pytest.raises(SystemExit) as exc:
                main()
            assert exc.value.code == 0
        finally:
            sys.argv = old_argv

    def test_main_subcommand_help(self):
        from latex_index.cli import main
        import sys
        old_argv = sys.argv
        try:
            sys.argv = ["latex-index", "insert", "--help"]
            with pytest.raises(SystemExit) as exc:
                main()
            assert exc.value.code == 0
        finally:
            sys.argv = old_argv

    def test_main_scan_help(self):
        from latex_index.cli import main
        import sys
        old_argv = sys.argv
        try:
            sys.argv = ["latex-index", "scan", "--help"]
            with pytest.raises(SystemExit) as exc:
                main()
            assert exc.value.code == 0
        finally:
            sys.argv = old_argv

    def test_main_parse_help(self):
        from latex_index.cli import main
        import sys
        old_argv = sys.argv
        try:
            sys.argv = ["latex-index", "parse", "--help"]
            with pytest.raises(SystemExit) as exc:
                main()
            assert exc.value.code == 0
        finally:
            sys.argv = old_argv

    def test_main_tools_help(self):
        from latex_index.cli import main
        import sys
        old_argv = sys.argv
        try:
            sys.argv = ["latex-index", "tools", "--help"]
            with pytest.raises(SystemExit) as exc:
                main()
            assert exc.value.code == 0
        finally:
            sys.argv = old_argv


class TestMainModule:
    """Test __main__.py entry point."""

    def test_main_module_file_exists(self):
        """Verify __main__.py exists and is well-formed."""
        import latex_index
        import os
        main_path = os.path.join(
            os.path.dirname(latex_index.__file__), "__main__.py"
        )
        assert os.path.isfile(main_path)
        with open(main_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "from .cli import main" in content
        assert "main()" in content

    @pytest.mark.skip(reason="需要完整安装环境，CI 中跳过")
    def test_cli_module_execution(self):
        """python -m latex_index --help should exit 0."""
        import subprocess
        import sys
        result = subprocess.run(
            [sys.executable, "-m", "latex_index", "--help"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0


class TestSetupAndRollback:
    """Tests for latex-index setup and rollback commands."""

    def test_setup_generates_file(self, tmp_path):
        import latex_index.cli as cli_mod
        args = argparse.Namespace(project_dir=str(tmp_path), no_backup=False)
        result = cli_mod.cmd_setup(args)
        assert result == 0
        assert (tmp_path / ".latexmkrc").exists()

    def test_setup_no_backup(self, tmp_path):
        import latex_index.cli as cli_mod
        args = argparse.Namespace(project_dir=str(tmp_path), no_backup=True)
        result = cli_mod.cmd_setup(args)
        assert result == 0

    def test_rollback_list(self, tmp_path):
        import latex_index.cli as cli_mod
        test_file = tmp_path / "test.tex"
        test_file.write_text("content", encoding="utf-8")
        args = argparse.Namespace(
            input=str(test_file), list=True, clean=None,
        )
        result = cli_mod.cmd_rollback(args)
        assert result == 0

    def test_rollback_no_backup(self, tmp_path):
        import latex_index.cli as cli_mod
        test_file = tmp_path / "nonexistent.tex"
        test_file.write_text("x", encoding="utf-8")
        args = argparse.Namespace(
            input=str(test_file), list=False, clean=None,
        )
        result = cli_mod.cmd_rollback(args)
        assert result == 1  # no backup found

    def test_rollback_clean(self, tmp_path):
        import latex_index.cli as cli_mod
        test_file = tmp_path / "cleanme.tex"
        test_file.write_text("v1", encoding="utf-8")
        args = argparse.Namespace(
            input=str(test_file), list=False, clean=1,
        )
        result = cli_mod.cmd_rollback(args)
        assert result == 0


class TestCmdXindy:
    """Tests for latex-index xindy command."""

    def test_xindy_default(self, tmp_path):
        import latex_index.cli as cli_mod
        out = tmp_path / "test.xdy"
        args = argparse.Namespace(
            languages=["english"], output=str(out), list_langs=False,
        )
        result = cli_mod.cmd_xindy(args)
        assert result == 0
        assert out.exists()

    def test_xindy_multi_language(self, tmp_path):
        import latex_index.cli as cli_mod
        out = tmp_path / "multi.xdy"
        args = argparse.Namespace(
            languages=["english", "chinese-pinyin"],
            output=str(out), list_langs=False,
        )
        result = cli_mod.cmd_xindy(args)
        assert result == 0

    def test_xindy_list_languages(self):
        import latex_index.cli as cli_mod
        args = argparse.Namespace(
            languages=["english"], output="test.xdy", list_langs=True,
        )
        result = cli_mod.cmd_xindy(args)
        assert result == 0


class TestCmdReport:
    """Tests for latex-index report command."""

    def test_report_basic(self, tmp_path):
        import latex_index.cli as cli_mod
        tex = tmp_path / "test.tex"
        tex.write_text(r"\index{compact} and \index{field}", encoding="utf-8")
        args = argparse.Namespace(
            input=str(tex), entries=None, candidates=None, output=None,
        )
        result = cli_mod.cmd_report(args)
        assert result == 0

    def test_report_with_entries_file(self, tmp_path):
        import latex_index.cli as cli_mod
        tex = tmp_path / "test.tex"
        tex.write_text(r"\index{compact}", encoding="utf-8")
        entries_file = tmp_path / "entries.json"
        entries_file.write_text(
            '[{"term": "compact", "level": 1}]', encoding="utf-8",
        )
        args = argparse.Namespace(
            input=str(tex), entries=str(entries_file),
            candidates=None, output=None,
        )
        result = cli_mod.cmd_report(args)
        assert result == 0

    def test_report_with_candidates_file(self, tmp_path):
        import latex_index.cli as cli_mod
        tex = tmp_path / "test.tex"
        tex.write_text(r"\index{field}", encoding="utf-8")
        cand = tmp_path / "candidates.txt"
        cand.write_text("field\nalgebra\n", encoding="utf-8")
        args = argparse.Namespace(
            input=str(tex), entries=None,
            candidates=str(cand), output=None,
        )
        result = cli_mod.cmd_report(args)
        assert result == 0

    def test_report_to_file(self, tmp_path):
        import latex_index.cli as cli_mod
        tex = tmp_path / "test.tex"
        tex.write_text(r"\index{test}", encoding="utf-8")
        out = tmp_path / "report.txt"
        args = argparse.Namespace(
            input=str(tex), entries=None, candidates=None,
            output=str(out),
        )
        result = cli_mod.cmd_report(args)
        assert result == 0
        assert out.exists()

    def test_report_missing_input(self):
        import latex_index.cli as cli_mod
        args = argparse.Namespace(
            input="/nonexistent/file.tex", entries=None,
            candidates=None, output=None,
        )
        result = cli_mod.cmd_report(args)
        assert result == 1
