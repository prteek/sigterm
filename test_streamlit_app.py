import pytest
from streamlit_app import process_command


class TestProcessCommand:
    """Tests for the process_command function"""

    def test_help_command(self):
        """Test help command returns list of available commands"""
        result = process_command("help")
        assert "help" in result
        assert "ls" in result
        assert "echo" in result
        assert "whoami" in result
        assert "clear" in result

    def test_ls_command(self):
        """Test ls command returns file listing"""
        result = process_command("ls")
        assert "file1.txt" in result
        assert "file2.txt" in result
        assert "folder/" in result

    def test_whoami_command(self):
        """Test whoami command returns user info"""
        result = process_command("whoami")
        assert result == "user@terminal-app"

    def test_echo_command_with_text(self):
        """Test echo command echoes back the provided text"""
        result = process_command("echo hello world")
        assert result == "hello world"

    def test_echo_command_empty(self):
        """Test echo command with no text"""
        result = process_command("echo ")
        assert result == ""

    def test_echo_command_with_special_chars(self):
        """Test echo command with special characters"""
        result = process_command("echo hello@123!$#")
        assert result == "hello@123!$#"

    def test_clear_command(self):
        """Test clear command returns empty string"""
        result = process_command("clear")
        assert result == ""

    def test_invalid_command(self):
        """Test that invalid commands return 'command not found' message"""
        result = process_command("invalid")
        assert "command not found" in result
        assert "invalid" in result

    def test_invalid_command_typo(self):
        """Test typo in command returns error"""
        result = process_command("hlep")
        assert "command not found" in result
        assert "hlep" in result

    def test_command_case_sensitive(self):
        """Test that commands are case sensitive"""
        result = process_command("HELP")
        assert "command not found" in result

    def test_echo_with_multiple_words(self):
        """Test echo preserves multiple spaces and words"""
        result = process_command("echo hello  world   test")
        assert result == "hello  world   test"
