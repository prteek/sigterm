"""Tests for the cat command"""
import pytest
from commands import process_command


class TestCatCommand:
    """Tests for cat (display file) command"""

    def test_cat_about_txt(self):
        """Test cat about.txt displays file contents"""
        result_type, result_content, new_dir = process_command("cat about.txt")
        assert result_type == "text"
        assert "Prateek" in result_content or "ABOUT" in result_content
        assert new_dir is None

    def test_cat_nonexistent_file(self):
        """Test cat with nonexistent file returns error"""
        result_type, result_content, new_dir = process_command("cat nonexistent.txt")
        assert result_type == "text"
        assert "No such file or directory" in result_content
        assert new_dir is None

    def test_cat_no_argument(self):
        """Test cat without argument returns helpful error"""
        result_type, result_content, new_dir = process_command("cat ")
        assert result_type == "text"
        assert "missing file argument" in result_content
        assert "Usage:" in result_content
        assert new_dir is None

    def test_cat_no_space(self):
        """Test cat without space or argument returns helpful error"""
        result_type, result_content, new_dir = process_command("cat")
        assert result_type == "text"
        assert "missing file argument" in result_content
        assert new_dir is None

    def test_cat_directory_error(self):
        """Test cat with directory input shows helpful error"""
        result_type, result_content, new_dir = process_command("cat blog")
        assert result_type == "text"
        assert "Is a directory" in result_content
        assert "cd blog" in result_content

    def test_cat_about_me_md(self):
        """Test cat about_me.md renders as markdown"""
        result_type, result_content, new_dir = process_command("cat about_me.md")
        assert result_type == "markdown"
        assert "About Me" in result_content
        assert "Prateek" in result_content
        assert new_dir is None

    def test_cat_about_me_without_extension(self):
        """Test cat about_me renders as markdown without extension"""
        result_type, result_content, new_dir = process_command("cat about_me")
        assert result_type == "markdown"
        assert "About Me" in result_content
        assert new_dir is None
