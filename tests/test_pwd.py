"""Tests for the pwd command"""
import pytest
from commands import process_command


class TestPwdCommand:
    """Tests for pwd (print working directory) command"""

    def test_pwd_command_at_root(self):
        """Test pwd command shows /home at root"""
        result_type, result_content, new_dir = process_command("pwd")
        assert result_type == "text"
        assert result_content == "/home"

    def test_pwd_command_in_subdirectory(self):
        """Test pwd command shows /home/<directory> in subdirectory"""
        result_type, result_content, new_dir = process_command("pwd", current_dir="blog")
        assert result_type == "text"
        assert result_content == "/home/blog"
