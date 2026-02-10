"""Tests for the whoami command"""
import pytest
from commands import process_command


class TestWhoamiCommand:
    """Tests for whoami command"""

    def test_whoami_command(self):
        """Test whoami command returns user info"""
        result_type, result_content, new_dir = process_command("whoami")
        assert result_type == "text"
        assert result_content == "user@sigterm"
