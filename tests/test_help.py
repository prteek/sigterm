"""Tests for the help command"""
import pytest
from commands import process_command


class TestHelpCommand:
    """Tests for help command"""

    def test_help_command(self):
        """Test help command returns available commands with descriptions"""
        result_type, result_content, new_dir = process_command("help")
        assert result_type == "text"
        # Check for commands
        assert "help" in result_content
        assert "ls" in result_content
        assert "echo" in result_content
        assert "whoami" in result_content
        assert "pwd" in result_content
        assert "clear" in result_content
        assert "cd" in result_content
        assert "cat" in result_content
        # Check for descriptions
        assert "Show available commands" in result_content
        assert "List directory contents" in result_content
        assert "Display text" in result_content
        assert "Show current user" in result_content
        assert "Print working directory" in result_content
        assert "Clear screen" in result_content
        assert "Change directory" in result_content
        assert "Display file contents" in result_content
        assert new_dir is None

    def test_help_includes_cat(self):
        """Test that help command includes cat"""
        result_type, result_content, new_dir = process_command("help")
        assert result_type == "text"
        assert "cat" in result_content
