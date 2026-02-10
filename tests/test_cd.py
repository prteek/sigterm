"""Tests for the cd command"""
import pytest
from commands import process_command


class TestCdCommand:
    """Tests for cd (change directory) command"""

    def test_cd_home_command(self):
        """Test cd ~ navigates to home from subdirectory"""
        result_type, result_content, new_dir = process_command("cd ~", current_dir="blog")
        assert result_type == "text"
        assert "Navigated to home" in result_content
        assert new_dir == "~"

    def test_cd_home_already_at_home(self):
        """Test cd ~ when already at home"""
        result_type, result_content, new_dir = process_command("cd ~")
        assert result_type == "text"
        assert "Already at home" in result_content
        assert new_dir is None

    def test_cd_parent_at_root(self):
        """Test cd .. at root directory"""
        result_type, result_content, new_dir = process_command("cd ..")
        assert result_type == "text"
        assert "Already" in result_content or "root" in result_content
        assert new_dir is None

    def test_cd_parent_from_subdirectory(self):
        """Test cd .. navigates back from subdirectory and shows ls output"""
        result_type, result_content, new_dir = process_command("cd ..", current_dir="blog")
        assert result_type == "text"
        # Should show parent directory contents (same as ls at parent level)
        assert "about.txt" in result_content
        assert "blog/" in result_content
        assert new_dir == "~"

    def test_cd_blog_command(self):
        """Test cd blog loads the blog page"""
        result_type, result_content, new_dir = process_command("cd blog")
        # Blog page can be loaded (returns text or streamlit)
        assert isinstance(result_type, str)
        assert result_type in ("streamlit", "text")

    def test_cd_about_command(self):
        """Test cd about loads the about page"""
        result_type, result_content, new_dir = process_command("cd about")
        # Should load about.txt which returns text type
        assert result_type == "text"

    def test_cd_invalid_target(self):
        """Test cd with invalid target returns error"""
        result_type, result_content, new_dir = process_command("cd nonexistent")
        assert result_type == "text"
        assert "No such file or directory" in result_content

    def test_cd_no_argument(self):
        """Test cd without argument returns helpful error"""
        result_type, result_content, new_dir = process_command("cd ")
        assert result_type == "text"
        assert "missing directory argument" in result_content
        assert "Usage:" in result_content

    def test_cd_no_space(self):
        """Test cd without space or argument returns helpful error"""
        result_type, result_content, new_dir = process_command("cd")
        assert result_type == "text"
        assert "missing directory argument" in result_content

    def test_cd_with_whitespace(self):
        """Test cd command handles whitespace correctly"""
        result_type, result_content, new_dir = process_command("cd   blog   ")
        # Should still load blog despite extra whitespace
        assert isinstance(result_type, str)
        assert result_type in ("streamlit", "text")
