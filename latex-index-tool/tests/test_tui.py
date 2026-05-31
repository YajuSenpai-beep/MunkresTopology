r"""Tests for Rich TUI module.

Covers latex_index/tui.py.
"""

import sys
from unittest.mock import MagicMock, patch

from latex_index.tui import _basic_select, HAS_RICH, interactive_select


class TestBasicSelect:
    def test_all_accepted(self, monkeypatch):
        ops = [
            {"pos": 0, "cmd": r"\index{field}", "entry": {"term": "field"}},
            {"pos": 10, "cmd": r"\index{ring}", "entry": {"term": "ring"}},
        ]
        monkeypatch.setattr("builtins.input", lambda _: "a")
        result = _basic_select(ops, "field and ring")
        assert len(result) == 2

    def test_quit_immediately(self, monkeypatch):
        ops = [{"pos": 0, "cmd": r"\index{field}", "entry": {"term": "field"}}]
        monkeypatch.setattr("builtins.input", lambda _: "q")
        result = _basic_select(ops, "field")
        assert result == []

    def test_accept_one(self, monkeypatch):
        ops = [
            {"pos": 0, "cmd": r"\index{a}", "entry": {"term": "a"}},
            {"pos": 5, "cmd": r"\index{b}", "entry": {"term": "b"}},
        ]
        responses = iter(["y", "n"])
        monkeypatch.setattr("builtins.input", lambda _: next(responses))
        result = _basic_select(ops, "a and b")
        assert len(result) == 1

    def test_empty_ops(self):
        assert _basic_select([], "") == []

    def test_all_single_op(self, monkeypatch):
        ops = [{"pos": 0, "cmd": r"\idx{x}", "entry": {"term": "x"}}]
        monkeypatch.setattr("builtins.input", lambda _: "a")
        result = _basic_select(ops, "x")
        assert len(result) == 1


class TestInteractiveSelect:
    def test_empty_ops(self):
        assert interactive_select([], "") == []

    def test_basic_fallback(self, monkeypatch):
        ops = [{"pos": 0, "cmd": r"\index{test}", "entry": {"term": "test"}}]
        monkeypatch.setattr("builtins.input", lambda _: "y")
        result = interactive_select(ops, "test", use_rich=False)
        assert len(result) == 1

    def test_has_rich_flag(self):
        assert isinstance(HAS_RICH, bool)


class TestRichTUI:
    """Test the Rich TUI paths by mocking Rich classes."""

    def test_all_mode(self, monkeypatch):
        """Rich TUI: 'all' mode confirms all."""
        ops = [
            {"pos": 0, "cmd": r"\index{a}", "entry": {"term": "a"}},
            {"pos": 5, "cmd": r"\index{b}", "entry": {"term": "b"}},
        ]
        # Only test if rich is installed
        if not HAS_RICH:
            import pytest
            pytest.skip("rich not installed")

        mock_table = MagicMock()
        mock_console = MagicMock()

        with patch("latex_index.tui.Console", return_value=mock_console):
            with patch("latex_index.tui.Table", return_value=mock_table):
                with patch("latex_index.tui.Prompt") as mock_prompt:
                    with patch("latex_index.tui.Confirm") as mock_confirm:
                        mock_prompt.ask.return_value = "all"
                        mock_confirm.ask.return_value = True
                        result = interactive_select(ops, "a b", use_rich=True)
                        assert len(result) == 2

    def test_quit_mode(self):
        """Rich TUI: 'quit' returns empty."""
        ops = [{"pos": 0, "cmd": r"\index{x}", "entry": {"term": "x"}}]
        if not HAS_RICH:
            import pytest
            pytest.skip("rich not installed")

        mock_console = MagicMock()
        with patch("latex_index.tui.Console", return_value=mock_console):
            with patch("latex_index.tui.Table", return_value=MagicMock()):
                with patch("latex_index.tui.Prompt") as mock_prompt:
                    mock_prompt.ask.return_value = "quit"
                    result = interactive_select(ops, "x", use_rich=True)
                    assert result == []

    def test_range_mode(self):
        """Rich TUI: 'range' mode selects by range."""
        ops = [
            {"pos": i * 10, "cmd": f"\\index{{t{i}}}", "entry": {"term": f"t{i}"}}
            for i in range(10)
        ]
        if not HAS_RICH:
            import pytest
            pytest.skip("rich not installed")

        mock_console = MagicMock()
        with patch("latex_index.tui.Console", return_value=mock_console):
            with patch("latex_index.tui.Table", return_value=MagicMock()):
                with patch("latex_index.tui.Prompt") as mock_prompt:
                    mock_prompt.ask.side_effect = ["range", "1-3"]
                    with patch("latex_index.tui.Confirm") as mock_confirm:
                        result = interactive_select(ops, "x" * 100, use_rich=True)
                        assert len(result) == 3

    def test_select_mode(self):
        """Rich TUI: 'select' mode selects by index."""
        ops = [
            {"pos": i * 10, "cmd": f"\\index{{t{i}}}", "entry": {"term": f"t{i}"}}
            for i in range(10)
        ]
        if not HAS_RICH:
            import pytest
            pytest.skip("rich not installed")

        mock_console = MagicMock()
        with patch("latex_index.tui.Console", return_value=mock_console):
            with patch("latex_index.tui.Table", return_value=MagicMock()):
                with patch("latex_index.tui.Prompt") as mock_prompt:
                    mock_prompt.ask.side_effect = ["select", "1 3 5"]
                    result = interactive_select(ops, "x" * 100, use_rich=True)
                    assert len(result) == 3

    def test_search_mode(self):
        """Rich TUI: 'search' mode filters by term."""
        ops = [
            {"pos": 0, "cmd": r"\index{compact}", "entry": {"term": "compact"}},
            {"pos": 10, "cmd": r"\index{connected}", "entry": {"term": "connected"}},
            {"pos": 20, "cmd": r"\index{compactness}", "entry": {"term": "compactness"}},
        ]
        if not HAS_RICH:
            import pytest
            pytest.skip("rich not installed")

        mock_console = MagicMock()
        with patch("latex_index.tui.Console", return_value=mock_console):
            with patch("latex_index.tui.Table", return_value=MagicMock()):
                with patch("latex_index.tui.Prompt") as mock_prompt:
                    mock_prompt.ask.side_effect = ["search", "compact"]
                    result = interactive_select(ops, "x", use_rich=True)
                    assert len(result) == 2

    def test_invalid_range(self):
        """Rich TUI: invalid range input returns empty."""
        ops = [{"pos": 0, "cmd": r"\index{x}", "entry": {"term": "x"}}]
        if not HAS_RICH:
            import pytest
            pytest.skip("rich not installed")

        mock_console = MagicMock()
        with patch("latex_index.tui.Console", return_value=mock_console):
            with patch("latex_index.tui.Table", return_value=MagicMock()):
                with patch("latex_index.tui.Prompt") as mock_prompt:
                    mock_prompt.ask.side_effect = ["range", "abc"]
                    result = interactive_select(ops, "x", use_rich=True)
                    assert result == []

    def test_invalid_select(self):
        """Rich TUI: invalid select input returns empty."""
        ops = [{"pos": 0, "cmd": r"\index{x}", "entry": {"term": "x"}}]
        if not HAS_RICH:
            import pytest
            pytest.skip("rich not installed")

        mock_console = MagicMock()
        with patch("latex_index.tui.Console", return_value=mock_console):
            with patch("latex_index.tui.Table", return_value=MagicMock()):
                with patch("latex_index.tui.Prompt") as mock_prompt:
                    mock_prompt.ask.side_effect = ["select", ""]
                    result = interactive_select(ops, "x", use_rich=True)
                    assert result == []

    def test_all_declined(self):
        """Rich TUI: 'all' mode but user declines confirmation."""
        ops = [{"pos": 0, "cmd": r"\index{x}", "entry": {"term": "x"}}]
        if not HAS_RICH:
            import pytest
            pytest.skip("rich not installed")

        mock_console = MagicMock()
        with patch("latex_index.tui.Console", return_value=mock_console):
            with patch("latex_index.tui.Table", return_value=MagicMock()):
                with patch("latex_index.tui.Prompt") as mock_prompt:
                    mock_prompt.ask.return_value = "all"
                    with patch("latex_index.tui.Confirm") as mock_confirm:
                        mock_confirm.ask.return_value = False
                        result = interactive_select(ops, "x", use_rich=True)
                        assert result == []
