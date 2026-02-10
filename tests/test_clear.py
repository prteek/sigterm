"""Tests for the clear command"""
import pytest
from commands import process_command


class TestClearCommand:
    """Tests for clear command"""

    def test_clear_command(self):
        """Test clear command returns empty string"""
        result_type, result_content, new_dir = process_command("clear")
        assert result_type == "text"
        assert result_content == ""
