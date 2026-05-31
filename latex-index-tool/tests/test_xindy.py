r"""Tests for xindy .xdy generation."""

import os
import tempfile

from latex_index.xindy import (
    generate_multilang_xdy,
    generate_xdy,
    list_supported_languages,
    write_xdy,
)


class TestGenerateXdy:
    def test_default_english(self):
        content = generate_xdy()
        assert "english" in content.lower() or "en" in content.lower()
        assert "define-letter-group" in content

    def test_chinese_pinyin(self):
        content = generate_xdy(languages=["chinese-pinyin"])
        assert "pinyin" in content.lower()

    def test_chinese_stroke(self):
        content = generate_xdy(languages=["chinese-stroke"])
        assert "stroke" in content.lower()

    def test_multi_language(self):
        content = generate_xdy(languages=["english", "chinese-pinyin"])
        assert "english" in content.lower()
        assert "pinyin" in content.lower()

    def test_no_math(self):
        content = generate_xdy(include_math=False)
        assert "Symbols" not in content

    def test_custom_rules(self):
        content = generate_xdy(custom_rules="(my-custom-rule)")
        assert "my-custom-rule" in content

    def test_unknown_language_fallback(self):
        content = generate_xdy(languages=["klingon"])
        assert "english" in content.lower()  # fallback

    def test_empty_languages(self):
        content = generate_xdy(languages=[])
        # Should not crash
        assert isinstance(content, str)


class TestMultiLangXdy:
    def test_chapter_lang_map(self):
        content = generate_multilang_xdy({
            1: "english",
            2: "chinese-pinyin",
        })
        assert "english" in content.lower()

    def test_with_base_languages(self):
        content = generate_multilang_xdy(
            {1: "chinese-pinyin"},
            base_languages=["english", "chinese-stroke"],
        )
        assert "english" in content.lower()
        assert "stroke" in content.lower()


class TestListLanguages:
    def test_returns_list(self):
        langs = list_supported_languages()
        assert "english" in langs
        assert "chinese-pinyin" in langs
        assert "chinese-stroke" in langs
        assert "math-symbols" in langs


class TestWriteXdy:
    def test_writes_file(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".xdy", delete=False, encoding="utf-8"
        ) as f:
            path = f.name
        try:
            result = write_xdy(path, languages=["english"])
            assert result == path
            assert os.path.exists(path)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            assert "define-letter-group" in content
        finally:
            os.unlink(path)
