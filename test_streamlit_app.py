import pytest
from streamlit_app import process_command


class TestProcessCommand:
    """Tests for the process_command function"""

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

    def test_whoami_command(self):
        """Test whoami command returns user info"""
        result_type, result_content, new_dir = process_command("whoami")
        assert result_type == "text"
        assert result_content == "user@inference"

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

    def test_clear_command(self):
        """Test clear command returns empty string"""
        result_type, result_content, new_dir = process_command("clear")
        assert result_type == "text"
        assert result_content == ""

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

    def test_echo_with_multiple_spaces(self):
        """Test echo preserves multiple spaces and words"""
        result_type, result_content, new_dir = process_command("echo hello  world   test")
        assert result_type == "text"
        assert result_content == "hello  world   test"

    def test_command_returns_tuple(self):
        """Test that process_command returns a tuple of (type, content, new_dir)"""
        result = process_command("help")
        assert isinstance(result, tuple)
        assert len(result) == 3
        assert result[0] in ("text", "streamlit")

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

    def test_help_includes_cat(self):
        """Test that help command includes cat"""
        result_type, result_content, new_dir = process_command("help")
        assert result_type == "text"
        assert "cat" in result_content

    def test_cat_directory_error(self):
        """Test cat with directory input shows helpful error"""
        result_type, result_content, new_dir = process_command("cat blog")
        assert result_type == "text"
        assert "Is a directory" in result_content
        assert "cd blog" in result_content

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

    def test_cd_parent_shows_about_me(self):
        """Test cd .. shows about_me.md in listing"""
        result_type, result_content, new_dir = process_command("cd ..", current_dir="blog")
        assert result_type == "text"
        assert "about.txt" in result_content
        assert "about_me.md" in result_content
        assert "blog/" in result_content
        assert new_dir == "~"
