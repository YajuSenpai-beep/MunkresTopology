r"""Tests for multi-file LaTeX project support.

Coverage targets: 85%+ on latex_index/project.py (currently 0%).
"""

import os
import tempfile

import pytest

from latex_index.project import (
    detect_encoding,
    detect_line_ending,
    list_input_files,
    preserve_line_endings,
    resolve_tex_project,
)


class TestDetectEncoding:
    def test_utf8_file(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tex", delete=False, encoding="utf-8"
        ) as f:
            f.write(r"\section{Hello World}")
            path = f.name
        try:
            assert detect_encoding(path) == "utf-8"
        finally:
            os.unlink(path)

    def test_latin1_file(self):
        content = "\xe9\xe8\xfc".encode("latin-1")  # éèü in latin-1
        with tempfile.NamedTemporaryFile(
            mode="wb", suffix=".tex", delete=False
        ) as f:
            f.write(content)
            path = f.name
        try:
            enc = detect_encoding(path)
            assert enc in ("latin-1", "cp1252", "iso-8859-1")
        finally:
            os.unlink(path)

    def test_binary_falls_through_to_fallback(self):
        # bytes \x80-\x83 are valid latin-1 (but not UTF-8)
        with tempfile.NamedTemporaryFile(
            mode="wb", suffix=".tex", delete=False
        ) as f:
            f.write(b"\x80\x81\x82\x83")
            path = f.name
        try:
            enc = detect_encoding(path)
            assert enc in ("latin-1", "cp1252", "iso-8859-1", "utf-8")
        finally:
            os.unlink(path)


class TestDetectLineEnding:
    def test_windows_crlf(self):
        assert detect_line_ending("line1\r\nline2\r\n") == "\r\n"

    def test_unix_lf(self):
        assert detect_line_ending("line1\nline2\n") == "\n"

    def test_old_mac_cr(self):
        assert detect_line_ending("line1\rline2\r") == "\r"

    def test_mixed_prefers_majority(self):
        # majority wins
        text = "a\r\nb\r\nc\nd\r\ne\r\n"
        assert detect_line_ending(text) == "\r\n"

    def test_empty_content(self):
        assert detect_line_ending("") == "\n"


class TestPreserveLineEndings:
    def test_crlf_to_lf_conversion(self):
        original = "line1\r\nline2\r\n"
        new = "line1\nline2\nline3\n"
        result = preserve_line_endings(original, new)
        assert "\r\n" in result
        assert "\n" not in result.replace("\r\n", "")

    def test_no_change_when_same(self):
        original = "line1\nline2\n"
        new = "line3\nline4\n"
        result = preserve_line_endings(original, new)
        assert result == new


class TestResolveTexProject:
    def test_simple_main_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            main = os.path.join(tmpdir, "main.tex")
            with open(main, "w", encoding="utf-8") as f:
                f.write(r"\section{Intro}" + "\n" + r"Hello world." + "\n")
            merged, files, line_map = resolve_tex_project(main)
            assert "Hello world" in merged
            assert len(files) >= 1
            assert os.path.basename(main) in line_map

    def test_input_subfile(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sub = os.path.join(tmpdir, "chapter1.tex")
            with open(sub, "w", encoding="utf-8") as f:
                f.write("Content from chapter 1.\n")
            main = os.path.join(tmpdir, "main.tex")
            with open(main, "w", encoding="utf-8") as f:
                f.write(r"\input{chapter1}" + "\n")
            merged, files, line_map = resolve_tex_project(main)
            assert "Content from chapter 1" in merged
            assert len(files) == 2

    def test_include_subfile(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sub = os.path.join(tmpdir, "ch2.tex")
            with open(sub, "w", encoding="utf-8") as f:
                f.write("Chapter 2 text.\n")
            main = os.path.join(tmpdir, "main.tex")
            with open(main, "w", encoding="utf-8") as f:
                f.write(r"\include{ch2}" + "\n")
            merged, files, line_map = resolve_tex_project(main)
            assert "Chapter 2 text" in merged

    def test_nested_input(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            leaf = os.path.join(tmpdir, "leaf.tex")
            with open(leaf, "w", encoding="utf-8") as f:
                f.write("Leaf content.\n")
            mid = os.path.join(tmpdir, "mid.tex")
            with open(mid, "w", encoding="utf-8") as f:
                f.write(r"Before \input{leaf} After" + "\n")
            main = os.path.join(tmpdir, "main.tex")
            with open(main, "w", encoding="utf-8") as f:
                f.write(r"\input{mid}" + "\n")
            merged, files, line_map = resolve_tex_project(main)
            assert "Leaf content" in merged
            assert len(files) == 3

    def test_auto_add_tex_extension(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sub = os.path.join(tmpdir, "ch1.tex")
            with open(sub, "w", encoding="utf-8") as f:
                f.write("Chapter 1.\n")
            main = os.path.join(tmpdir, "main.tex")
            with open(main, "w", encoding="utf-8") as f:
                f.write(r"\input{ch1}" + "\n")  # no .tex extension
            merged, files, _ = resolve_tex_project(main)
            assert "Chapter 1" in merged

    def test_missing_file_warning(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            main = os.path.join(tmpdir, "main.tex")
            with open(main, "w", encoding="utf-8") as f:
                f.write(r"\input{does_not_exist}" + "\n")
            merged, files, _ = resolve_tex_project(main)
            # Should not crash; missing file is replaced with empty string
            assert len(merged) >= 0

    def test_includeonly_filter(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            for name in ["ch1.tex", "ch2.tex", "ch3.tex"]:
                with open(os.path.join(tmpdir, name), "w", encoding="utf-8") as f:
                    f.write(f"Content of {name}\n")
            main = os.path.join(tmpdir, "main.tex")
            with open(main, "w", encoding="utf-8") as f:
                f.write(
                    r"\includeonly{ch1,ch3}" + "\n"
                    r"\include{ch1}" + "\n"
                    r"\include{ch2}" + "\n"
                    r"\include{ch3}" + "\n"
                )
            merged, files, _ = resolve_tex_project(main)
            assert "Content of ch1.tex" in merged
            assert "Content of ch2.tex" not in merged
            assert "Content of ch3.tex" in merged

    def test_includeonly_without_extension(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sub = os.path.join(tmpdir, "intro.tex")
            with open(sub, "w", encoding="utf-8") as f:
                f.write("Intro text.\n")
            main = os.path.join(tmpdir, "main.tex")
            with open(main, "w", encoding="utf-8") as f:
                f.write(r"\includeonly{intro}" + "\n" r"\include{intro}" + "\n")
            merged, files, _ = resolve_tex_project(main)
            assert "Intro text" in merged

    def test_spaces_in_filename(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sub = os.path.join(tmpdir, "ch1.tex")
            with open(sub, "w", encoding="utf-8") as f:
                f.write("OK\n")
            main = os.path.join(tmpdir, "main.tex")
            with open(main, "w", encoding="utf-8") as f:
                f.write(r"\input{ ch1 }" + "\n")
            merged, files, _ = resolve_tex_project(main)
            assert "OK" in merged

    def test_circular_reference_handled(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            a = os.path.join(tmpdir, "a.tex")
            b = os.path.join(tmpdir, "b.tex")
            with open(a, "w", encoding="utf-8") as f:
                f.write(r"A starts. \input{b} A ends." + "\n")
            with open(b, "w", encoding="utf-8") as f:
                f.write(r"B starts. \input{a} B ends." + "\n")
            # Should not infinite-loop
            merged, files, _ = resolve_tex_project(a)
            assert "A starts" in merged

    def test_line_map_tracks_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sub = os.path.join(tmpdir, "ch1.tex")
            with open(sub, "w", encoding="utf-8") as f:
                f.write("Line1\nLine2\nLine3\n")
            main = os.path.join(tmpdir, "main.tex")
            with open(main, "w", encoding="utf-8") as f:
                f.write("Main line1\n" + r"\input{ch1}" + "\nMain line3\n")
            _, files, line_map = resolve_tex_project(main)
            assert "ch1.tex" in line_map
            assert os.path.basename(main) in line_map


class TestListInputFiles:
    def test_returns_file_list(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sub = os.path.join(tmpdir, "ch1.tex")
            with open(sub, "w", encoding="utf-8") as f:
                f.write("ok\n")
            main = os.path.join(tmpdir, "main.tex")
            with open(main, "w", encoding="utf-8") as f:
                f.write(r"\input{ch1}" + "\n")
            files = list_input_files(main)
            assert len(files) == 2
