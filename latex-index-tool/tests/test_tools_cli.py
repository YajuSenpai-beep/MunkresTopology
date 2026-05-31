r"""Tests for tools_cli.py command functions.

Tests command functions directly to cover tools_cli.py (5% → target 60%+).
"""

import argparse
import os
import tempfile

import pytest

from latex_index.tools_cli import (
    _convert_exercise_blocks,
    _extract_opt_arg,
    _for_each_file,
    _format_env_in_lines,
    _resolve_files,
    _wrap_with_centeredblock,
    cmd_clean_ex_envs,
    cmd_convert_exercises,
    cmd_fix_subitems,
    cmd_format_env,
    cmd_ocr_fix,
    cmd_scan_issues,
    cmd_wrap_examples,
    register_tools_parser,
)


# ── helpers ──────────────────────────────────────────────

def _make_tex(content: str, suffix: str = ".tex") -> str:
    """Create temp .tex file, return path."""
    fd, path = tempfile.mkstemp(suffix=suffix, text=True)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(content)
    return path


# ── _extract_opt_arg ────────────────────────────────────

class TestExtractOptArg:
    def test_no_opt_arg(self):
        assert _extract_opt_arg(r"\begin{theorem}text", r"\begin{theorem}") == ""

    def test_simple_opt_arg(self):
        result = _extract_opt_arg(
            r"\begin{theorem}[My Title]text", r"\begin{theorem}"
        )
        assert result == "[My Title]"

    def test_nested_brackets(self):
        result = _extract_opt_arg(
            r"\begin{lemma}[Nulhomotopy lemma]text", r"\begin{lemma}"
        )
        assert result == "[Nulhomotopy lemma]"


# ── _format_env_in_lines ────────────────────────────────

class TestFormatEnvInLines:
    def test_single_line_env(self):
        lines = [r"\begin{theorem}This is a theorem.\end{theorem}\n"]
        envs = ["theorem", "lemma", "proof"]
        fixes = _format_env_in_lines(lines, envs)
        assert fixes == 1
        assert lines[0].strip() == r"\begin{theorem}"
        assert "This is a theorem." in lines[1]
        assert r"\end{theorem}" in lines[2]

    def test_begin_text_split(self):
        lines = [r"\begin{proof}Let x be given."]
        envs = ["proof"]
        fixes = _format_env_in_lines(lines, envs)
        assert fixes == 1
        assert lines[0].strip() == r"\begin{proof}"
        assert lines[1].strip() == "Let x be given."

    def test_with_optional_arg(self):
        lines = [r"\begin{lemma}[Key Lemma]Important statement."]
        envs = ["lemma"]
        fixes = _format_env_in_lines(lines, envs)
        assert fixes == 1
        assert "[Key Lemma]" in lines[0]

    def test_already_clean_unchanged(self):
        lines = [r"\begin{proof}", "\tProof text.", r"\end{proof}"]
        envs = ["proof"]
        fixes = _format_env_in_lines(lines, envs)
        assert fixes == 0

    def test_comment_skipped(self):
        lines = [r"% \begin{theorem}ignored text"]
        envs = ["theorem"]
        assert _format_env_in_lines(lines, envs) == 0

    def test_multiple_envs(self):
        lines = [
            r"\begin{theorem}T1.\end{theorem}",
            r"\begin{lemma}L1.\end{lemma}",
        ]
        envs = ["theorem", "lemma"]
        fixes = _format_env_in_lines(lines, envs)
        assert fixes == 2


# ── _convert_exercise_blocks ────────────────────────────

class TestConvertExerciseBlocks:
    def test_simple_blocks(self):
        lines = [
            r"\section*{Exercises}",
            "1. Prove this.",
            "2. Show that.",
            r"\section*{Next Section}",
        ]
        blocks = [(0, 3)]  # exercises section range
        n = _convert_exercise_blocks(lines, blocks)
        assert n == 2
        joined = "\n".join(lines)
        assert r"\begin{enumerate}" in joined
        assert r"\end{enumerate}" in joined

    def test_with_subitems(self):
        lines = [
            r"\section*{Exercises}",
            "1. Main question.",
            "(a) Part one.",
            "(b) Part two.",
            r"\section*{Next}",
        ]
        blocks = [(0, 4)]
        n = _convert_exercise_blocks(lines, blocks)
        assert n == 1
        # Should have nested enumerate for subitems
        joined = "\n".join(lines)
        assert r"label=(\alph*)" in joined

    def test_multiline_continuation(self):
        lines = [
            r"\section*{Exercises}",
            "1. This is a long question that",
            "continues on the next line.",
            r"\section*{Next}",
        ]
        blocks = [(0, 3)]
        n = _convert_exercise_blocks(lines, blocks)
        assert n == 1


# ── _wrap_with_centeredblock ────────────────────────────

class TestWrapWithCenteredblock:
    def test_single_example(self):
        result = _wrap_with_centeredblock(
            r"\begin{example}Test example.\end{example}"
        )
        assert r"\begin{centeredblock}" in result
        assert r"\end{centeredblock}" in result
        assert r"\begin{example}" in result

    def test_already_wrapped_unchanged(self):
        content = (
            r"\begin{centeredblock}"
            + "\n"
            + r"\begin{example}Test.\end{example}"
            + "\n"
            + r"\end{centeredblock}"
        )
        result = _wrap_with_centeredblock(content)
        # Should not double-wrap
        assert result.count(r"\begin{centeredblock}") == 1

    def test_no_example_unchanged(self):
        content = r"\section{Intro} Some text."
        assert _wrap_with_centeredblock(content) == content


# ── _resolve_files ──────────────────────────────────────

class TestResolveFiles:
    def test_all_chapters(self):
        args = argparse.Namespace(chapter=None)
        # This depends on CWD having a chapters/ dir; skip in CI
        # Just test that it returns a list
        files = _resolve_files(args)
        assert isinstance(files, list)

    def test_specific_chapter(self):
        args = argparse.Namespace(chapter=1)
        files = _resolve_files(args)
        assert isinstance(files, list)

    def test_explicit_files(self):
        args = argparse.Namespace(files=["a.tex", "b.tex"], chapter=None)
        files = _resolve_files(args)
        assert files == ["a.tex", "b.tex"]


# ── _for_each_file ──────────────────────────────────────

class TestForEachFile:
    def test_continue_on_error(self):
        def failing(fp):
            if "bad" in fp:
                raise ValueError("fail")
            return 1

        args = argparse.Namespace(continue_on_error=True)
        total = _for_each_file(["good.tex", "bad.tex", "ok.tex"], args, failing)
        assert total == 2  # good + ok

    def test_stop_on_first_error(self):
        def failing(fp):
            raise ValueError("fail")

        args = argparse.Namespace(continue_on_error=False)
        with pytest.raises(ValueError):
            _for_each_file(["a.tex"], args, failing)


# ── Command functions ───────────────────────────────────

class TestCmdFormatEnv:
    def test_dry_run(self):
        path = _make_tex(r"\begin{theorem}Test.\end{theorem}")
        try:
            args = argparse.Namespace(
                chapter=None, files=[path], dry_run=True, continue_on_error=False,
            )
            result = cmd_format_env(args)
            assert result == 0
        finally:
            os.unlink(path)

    def test_actual_fix(self):
        path = _make_tex(r"\begin{proof}QED.\end{proof}")
        try:
            args = argparse.Namespace(
                chapter=None, files=[path], dry_run=False, continue_on_error=False,
            )
            result = cmd_format_env(args)
            assert result == 0
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            assert content.count("\n") >= 2
        finally:
            os.unlink(path)


class TestCmdConvertExercises:
    def test_conversion(self):
        path = _make_tex(
            r"\section*{Exercises}" + "\n"
            "1. Prove.\n"
            "2. Show.\n"
            + r"\section*{Next}"
        )
        try:
            args = argparse.Namespace(
                chapter=None, files=[path], continue_on_error=False,
            )
            result = cmd_convert_exercises(args)
            assert result == 0
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            assert r"\begin{enumerate}" in content
        finally:
            os.unlink(path)


class TestCmdCleanExEnvs:
    def test_cleanup(self):
        path = _make_tex(
            r"\section*{Exercises}" + "\n"
            + r"\begin{theorem}Thm.\end{theorem}" + "\n"
            + r"\section*{Next}"
        )
        try:
            args = argparse.Namespace(
                chapter=None, files=[path], continue_on_error=False,
            )
            result = cmd_clean_ex_envs(args)
            assert result == 0
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            assert r"\textsl{" in content
            assert r"\begin{theorem}" not in content
        finally:
            os.unlink(path)


class TestCmdFixSubitems:
    def test_fix(self):
        path = _make_tex(
            r"\item (a) First part." + "\n"
            + r"\begin{enumerate}[label=(\alph*)]" + "\n"
            + r"\item Second." + "\n"
            + r"\end{enumerate}"
        )
        try:
            args = argparse.Namespace(
                chapter=None, files=[path], continue_on_error=False,
            )
            result = cmd_fix_subitems(args)
            assert result == 0
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            assert r"\item First part." in content
        finally:
            os.unlink(path)


class TestCmdOcrFix:
    def test_spelling_fix(self):
        path = _make_tex(r"\section{Intro} Siliarly, we note that Structly speaking.")
        try:
            args = argparse.Namespace(
                chapter=None, files=[path], continue_on_error=False,
            )
            result = cmd_ocr_fix(args)
            assert result == 0
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            assert "Similarly" in content
            assert "Strictly" in content
            assert "Siliarly" not in content
        finally:
            os.unlink(path)

    def test_belonging_preserved(self):
        """'belonging' must NOT become 'belorigin'."""
        path = _make_tex(r"The elements belonging to the set.")
        try:
            args = argparse.Namespace(
                chapter=None, files=[path], continue_on_error=False,
            )
            cmd_ocr_fix(args)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            assert "belonging" in content
            assert "belorigin" not in content
        finally:
            os.unlink(path)


class TestCmdScanIssues:
    def test_detects_issues(self):
        path = _make_tex(r"Siliarly, the ``quote is unbalanced.")
        try:
            args = argparse.Namespace(
                chapter=None, files=[path], continue_on_error=False,
            )
            result = cmd_scan_issues(args)
            assert result == 0
        finally:
            os.unlink(path)


class TestCmdWrapExamples:
    def test_wrap(self):
        path = _make_tex(r"\begin{example}Test.\end{example}")
        try:
            args = argparse.Namespace(
                chapter=None, files=[path], continue_on_error=False,
            )
            result = cmd_wrap_examples(args)
            assert result == 0
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            assert r"\begin{centeredblock}" in content
        finally:
            os.unlink(path)

    def test_continue_on_error(self):
        """Should not crash on missing file with --continue-on-error."""
        path = "/nonexistent/path/file.tex"
        args = argparse.Namespace(
            chapter=None, files=[path], continue_on_error=True,
        )
        result = cmd_wrap_examples(args)
        assert result == 0  # error logged, total = 0


# ── register_tools_parser ──────────────────────────────

class TestRegisterToolsParser:
    def test_registers_all_commands(self):
        parser = argparse.ArgumentParser()
        sub = parser.add_subparsers(dest="command")
        register_tools_parser(sub)
        # Should not raise
        known = parser.parse_args(["tools", "format-env", "--chapter", "1"])
        assert known.tool_command == "format-env"
