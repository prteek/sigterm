"""Tests for the ls command"""
import pytest
from commands import process_command


class TestLsCommand:
    """Tests for ls (list directory) command"""

    def test_ls_command(self):
        """Test ls command returns directory listing with current entries"""
        result_type, result_content, new_dir = process_command("ls")
        assert result_type == "text"
        # Verify exact ls output
        expected_output = "about.txt\nabout_me.md\nblog/"
        assert result_content == expected_output

    def test_ls_command_contains_entries(self):
        """Test ls command contains all expected directory and file entries"""
        result_type, result_content, new_dir = process_command("ls")
        assert result_type == "text"
        assert "about.txt" in result_content
        assert "about_me.md" in result_content
        assert "blog/" in result_content
        # Verify entries count
        lines = [line.strip() for line in result_content.strip().split('\n') if line.strip()]
        assert len(lines) == 3, f"Expected 3 entries, got {len(lines)}: {lines}"

    def test_ls_parent_directory(self):
        """Test ls .. from subdirectory lists parent"""
        result_type, result_content, new_dir = process_command("ls ..", current_dir="blog")
        assert result_type == "text"
        assert "about.txt" in result_content
        assert "about_me.md" in result_content
        assert "blog/" in result_content

    def test_ls_parent_from_subdirectory(self):
        """Test ls .. from subdirectory lists root"""
        result_type, result_content, new_dir = process_command("ls ..", current_dir="blog")
        assert result_type == "text"
        assert "about.txt" in result_content
        assert "blog/" in result_content

    def test_ls_home_directory(self):
        """Test ls ~ lists root directory"""
        result_type, result_content, new_dir = process_command("ls ~")
        assert result_type == "text"
        assert "about.txt" in result_content
        assert "blog/" in result_content

    def test_ls_current_directory(self):
        """Test ls . lists current directory"""
        result_type, result_content, new_dir = process_command("ls .")
        assert result_type == "text"
        assert "about.txt" in result_content
        assert "blog/" in result_content

    def test_ls_invalid_target(self):
        """Test ls with invalid directory returns error"""
        result_type, result_content, new_dir = process_command("ls nonexistent")
        assert result_type == "text"
        assert "No such file or directory" in result_content
