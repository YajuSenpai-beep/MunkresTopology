r"""Tests for LaTeX build integration and rollback support."""

import os
import tempfile

from latex_index.latexmk import (
    clean_backups,
    create_backup,
    generate_latexmkrc,
    list_backups,
    rollback_file,
)


class TestGenerateLatexmkrc:
    def test_generates_config(self):
        content = generate_latexmkrc(project_dir="/tmp/test")
        assert "latex-index" in content
        assert "makeindex" in content

    def test_backup_enabled(self):
        content = generate_latexmkrc(backup=True)
        assert "bak" in content or "Backup" in content or "backup" in content

    def test_backup_disabled(self):
        content = generate_latexmkrc(backup=False)
        # Should not have backup section
        assert "cp" not in content or "bak" not in content

    def test_custom_config(self):
        content = generate_latexmkrc(index_config="my_config.yaml")
        assert "my_config.yaml" in content


class TestBackupRollback:
    def test_create_and_list_backup(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tex", delete=False, encoding="utf-8"
        ) as f:
            f.write("original content")
            path = f.name
        try:
            bp = create_backup(path)
            assert os.path.exists(bp)
            assert ".bak." in bp

            backups = list_backups(path)
            assert len(backups) >= 1
        finally:
            os.unlink(path)
            for b in list_backups(path):
                try:
                    os.unlink(b)
                except OSError:
                    pass

    def test_rollback(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tex", delete=False, encoding="utf-8"
        ) as f:
            f.write("version 1")
            path = f.name
        try:
            bp = create_backup(path)
            # Modify the file
            with open(path, "w", encoding="utf-8") as f:
                f.write("version 2 - modified")

            restored = rollback_file(path)
            assert restored is not None
            with open(path, "r", encoding="utf-8") as f:
                assert f.read() == "version 1"
        finally:
            os.unlink(path)
            for b in list_backups(path):
                try:
                    os.unlink(b)
                except OSError:
                    pass

    def test_rollback_no_backup(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tex", delete=False, encoding="utf-8"
        ) as f:
            f.write("content")
            path = f.name
        try:
            result = rollback_file(path)
            assert result is None
        finally:
            os.unlink(path)

    def test_clean_backups(self):
        import time
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tex", delete=False, encoding="utf-8"
        ) as f:
            f.write("v1")
            path = f.name
        try:
            for i in range(8):
                create_backup(path)
                time.sleep(0.01)  # ensure unique timestamps
            backups = list_backups(path)
            assert len(backups) >= 8, f"Expected >=8, got {len(backups)}: {backups}"
            removed = clean_backups(path, keep=3)
            assert removed >= 5
            assert len(list_backups(path)) <= 3
        finally:
            os.unlink(path)
            for b in list_backups(path):
                try:
                    os.unlink(b)
                except OSError:
                    pass
