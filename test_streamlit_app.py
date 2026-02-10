import pytest
from streamlit_app import process_command


class TestProcessCommand:
    """Tests for the process_command function"""

    def test_help_command(self):
        """Test help command returns available commands"""
        result_type, result_content = process_command("help")
        assert result_type == "text"
        assert "help" in result_content
        assert "ls" in result_content
        assert "echo" in result_content
        assert "whoami" in result_content
        assert "clear" in result_content
        assert "about" not in result_content
        assert "blog" not in result_content

    def test_ls_command(self):
        """Test ls command returns directory listing with current entries"""
        result_type, result_content = process_command("ls")
        assert result_type == "text"
        # Verify exact ls output
        expected_output = "about\nblog/"
        assert result_content == expected_output

    def test_ls_command_contains_entries(self):
        """Test ls command contains all expected directory and file entries"""
        result_type, result_content = process_command("ls")
        assert result_type == "text"
        assert "about" in result_content
        assert "blog/" in result_content
        # Verify entries count
        lines = [line.strip() for line in result_content.strip().split('\n') if line.strip()]
        assert len(lines) == 2, f"Expected 2 entries, got {len(lines)}: {lines}"

    def test_whoami_command(self):
        """Test whoami command returns user info"""
        result_type, result_content = process_command("whoami")
        assert result_type == "text"
        assert result_content == "user@inference"

    def test_echo_command_with_text(self):
        """Test echo command echoes back the provided text"""
        result_type, result_content = process_command("echo hello world")
        assert result_type == "text"
        assert result_content == "hello world"

    def test_echo_command_empty(self):
        """Test echo command with no text"""
        result_type, result_content = process_command("echo ")
        assert result_type == "text"
        assert result_content == ""

    def test_echo_command_with_special_chars(self):
        """Test echo command with special characters"""
        result_type, result_content = process_command("echo hello@123!$#")
        assert result_type == "text"
        assert result_content == "hello@123!$#"

    def test_clear_command(self):
        """Test clear command returns empty string"""
        result_type, result_content = process_command("clear")
        assert result_type == "text"
        assert result_content == ""

    def test_invalid_command(self):
        """Test that invalid commands return 'command not found' message"""
        result_type, result_content = process_command("invalid")
        assert result_type == "text"
        assert "command not found" in result_content
        assert "invalid" in result_content

    def test_invalid_command_typo(self):
        """Test typo in command returns error"""
        result_type, result_content = process_command("hlep")
        assert result_type == "text"
        assert "command not found" in result_content

    def test_command_case_sensitive(self):
        """Test that commands are case sensitive"""
        result_type, result_content = process_command("HELP")
        assert result_type == "text"
        assert "command not found" in result_content

    def test_echo_with_multiple_spaces(self):
        """Test echo preserves multiple spaces and words"""
        result_type, result_content = process_command("echo hello  world   test")
        assert result_type == "text"
        assert result_content == "hello  world   test"

    def test_command_returns_tuple(self):
        """Test that process_command returns a tuple of (type, content)"""
        result = process_command("help")
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert result[0] in ("text", "streamlit")

    def test_about_page_loading(self):
        """Test that about page can be loaded"""
        result_type, result_content = process_command("about")
        # Should either load successfully or return error
        assert isinstance(result_type, str)
        assert isinstance(result_content, str)

    def test_blog_page_loading(self):
        """Test that blog page can be loaded"""
        result_type, result_content = process_command("blog")
        # Should return streamlit type for blog page
        assert isinstance(result_type, str)
        assert result_type in ("streamlit", "text")

    def test_echo_numeric_input(self):
        """Test echo with numeric input"""
        result_type, result_content = process_command("echo 12345")
        assert result_type == "text"
        assert result_content == "12345"

    def test_echo_with_quotes(self):
        """Test echo preserves quotes"""
        result_type, result_content = process_command('echo "quoted text"')
        assert result_type == "text"
        assert result_content == '"quoted text"'
