"""Tests for invalid commands and general behavior"""
import pytest
from commands import process_command


class TestInvalidCommands:
    """Tests for invalid command handling"""

    def test_invalid_command(self):
        """Test that invalid commands return 'command not found' message"""
        result_type, result_content, new_dir = process_command("invalid")
        assert result_type == "text"
        assert "command not found" in result_content
        assert "invalid" in result_content

    def test_invalid_command_typo(self):
        """Test typo in command returns error"""
        result_type, result_content, new_dir = process_command("hlep")
        assert result_type == "text"
        assert "command not found" in result_content

    def test_command_case_sensitive(self):
        """Test that commands are case sensitive"""
        result_type, result_content, new_dir = process_command("HELP")
        assert result_type == "text"
        assert "command not found" in result_content

    def test_about_command_not_found(self):
        """Test that about command is not found (use cat instead)"""
        result_type, result_content, new_dir = process_command("about")
        assert result_type == "text"
        assert "command not found" in result_content

    def test_blog_command_not_found(self):
        """Test that blog command is not found (use cd instead)"""
        result_type, result_content, new_dir = process_command("blog")
        assert result_type == "text"
        assert "command not found" in result_content


class TestGeneralBehavior:
    """Tests for general command behavior"""

    def test_command_returns_tuple(self):
        """Test that process_command returns a tuple of (type, content, new_dir)"""
        result = process_command("help")
        assert isinstance(result, tuple)
        assert len(result) == 3
        assert result[0] in ("text", "streamlit")

    def test_cd_text_file_error(self):
        """Test cd with text file input shows helpful error"""
        result_type, result_content, new_dir = process_command("cd about")
        assert result_type == "text"
        assert "Is a text file" in result_content
        assert "cat about" in result_content

    def test_cd_text_file_with_extension_error(self):
        """Test cd with .txt extension shows helpful error"""
        result_type, result_content, new_dir = process_command("cd about.txt")
        assert result_type == "text"
        assert "Is a text file" in result_content
        assert "cat about" in result_content

    def test_cd_parent_shows_about_me(self):
        """Test cd .. shows about_me.md in listing"""
        result_type, result_content, new_dir = process_command("cd ..", current_dir="blog")
        assert result_type == "text"
        assert "about.txt" in result_content
        assert "about_me.md" in result_content
        assert "blog/" in result_content
        assert new_dir == "~"
