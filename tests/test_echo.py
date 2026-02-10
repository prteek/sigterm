"""Tests for the echo command"""
import pytest
from commands import process_command


class TestEchoCommand:
    """Tests for echo command"""

    def test_echo_command_with_text(self):
        """Test echo command echoes back the provided text"""
        result_type, result_content, new_dir = process_command("echo hello world")
        assert result_type == "text"
        assert result_content == "hello world"

    def test_echo_command_empty(self):
        """Test echo command with no text"""
        result_type, result_content, new_dir = process_command("echo ")
        assert result_type == "text"
        assert result_content == ""

    def test_echo_command_with_special_chars(self):
        """Test echo command with special characters"""
        result_type, result_content, new_dir = process_command("echo hello@123!$#")
        assert result_type == "text"
        assert result_content == "hello@123!$#"

    def test_echo_with_multiple_spaces(self):
        """Test echo preserves multiple spaces and words"""
        result_type, result_content, new_dir = process_command("echo hello  world   test")
        assert result_type == "text"
        assert result_content == "hello  world   test"

    def test_echo_numeric_input(self):
        """Test echo with numeric input"""
        result_type, result_content, new_dir = process_command("echo 12345")
        assert result_type == "text"
        assert result_content == "12345"

    def test_echo_with_quotes(self):
        """Test echo preserves quotes"""
        result_type, result_content, new_dir = process_command('echo "quoted text"')
        assert result_type == "text"
        assert result_content == '"quoted text"'
