r"""Tests for configuration management.

Coverage targets: 85%+ on latex_index/config.py (currently 0%).
"""

import json
import os
import tempfile

import pytest

from latex_index.config import DEFAULT_CONFIG, load_config


class TestDefaultConfig:
    def test_load_default_config(self):
        config = load_config(None)
        assert config["templates"]["l1"] == r"\index{${key}}"
        assert config["file_pattern"] == "Chapter_${num}_*.tex"
        assert config["log_level"] == "INFO"

    def test_default_has_required_keys(self):
        config = load_config(None)
        for key in ["version", "templates", "file_pattern", "aliases",
                     "math_shortcuts", "skip_patterns", "chapter_source_dir",
                     "index_processor", "log_level", "log_file"]:
            assert key in config

    def test_default_is_independent_copy(self):
        c1 = load_config(None)
        c2 = load_config(None)
        c1["log_level"] = "DEBUG"
        assert c2["log_level"] == "INFO"  # not affected


class TestLoadYaml:
    def test_load_yaml_config(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as f:
            f.write("log_level: DEBUG\n")
            f.write("templates:\n")
            f.write("  l1: \\mycmd{${key}}\n")
            path = f.name
        try:
            config = load_config(path)
            assert config["log_level"] == "DEBUG"
            assert config["templates"]["l1"] == r"\mycmd{${key}}"
        finally:
            os.unlink(path)

    def test_load_yaml_partial_override(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as f:
            f.write("log_level: ERROR\n")
            path = f.name
        try:
            config = load_config(path)
            # Overridden
            assert config["log_level"] == "ERROR"
            # Preserved from default
            assert config["templates"]["l1"] == r"\index{${key}}"
        finally:
            os.unlink(path)

    def test_load_yaml_aliases_merge(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as f:
            f.write("aliases:\n")
            f.write("  compact: [\"compactness\"]\n")
            path = f.name
        try:
            config = load_config(path)
            assert "compact" in config["aliases"]
        finally:
            os.unlink(path)


class TestLoadJson:
    def test_load_json_config(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump({"log_level": "WARNING", "templates": {"l1": r"\idx{${key}}"}}, f)
            path = f.name
        try:
            config = load_config(path)
            assert config["log_level"] == "WARNING"
            assert config["templates"]["l1"] == r"\idx{${key}}"
        finally:
            os.unlink(path)


class TestJsonConfig:
    def test_json_deep_merge_with_new_key(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump({
                "log_level": "ERROR",
                "new_option": "custom_value",
            }, f)
            path = f.name
        try:
            config = load_config(path)
            assert config["log_level"] == "ERROR"
            assert config["new_option"] == "custom_value"
            # Default template should be preserved
            assert config["templates"]["l1"] == r"\index{${key}}"
        finally:
            os.unlink(path)

    def test_json_without_templates_keeps_defaults(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump({"log_level": "DEBUG"}, f)
            path = f.name
        try:
            config = load_config(path)
            assert config["log_level"] == "DEBUG"
            assert config["templates"]["l1"] == r"\index{${key}}"
        finally:
            os.unlink(path)


class TestErrorHandling:
    def test_missing_file_fallback(self):
        config = load_config("/nonexistent/path/config.yaml")
        assert config == DEFAULT_CONFIG  # falls back to default

    def test_empty_yaml_file(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as f:
            f.write("")
            path = f.name
        try:
            config = load_config(path)
            # Should not crash, returns defaults
            assert config["templates"]["l1"] == r"\index{${key}}"
        finally:
            os.unlink(path)

    def test_invalid_yaml_syntax(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as f:
            f.write("{{{invalid: [[[yaml\n")
            path = f.name
        try:
            config = load_config(path)
            # Should not crash, returns defaults
            assert "templates" in config
        finally:
            os.unlink(path)


class TestDeepMerge:
    def test_nested_dict_merge(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as f:
            f.write("templates:\n")
            f.write("  l1: \\mycmd{${key}}\n")
            f.write("  custom: \\test{}\n")
            path = f.name
        try:
            config = load_config(path)
            # Overridden existing key
            assert config["templates"]["l1"] == r"\mycmd{${key}}"
            # Added new key
            assert config["templates"]["custom"] == r"\test{}"
            # Preserved other keys
            assert config["templates"]["l2"] == r"\index{${parent}!${child}}"
        finally:
            os.unlink(path)
