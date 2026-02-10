"""Command processing module for the terminal emulator"""

import os
from page_loader import load_page


# Filesystem structure configuration
# .py files are directories (accessible via cd)
py_files = {
    "blog": "blog.py",
}

# .txt and .md files are text files (readable via cat)
txt_files = {
    "about": "about.txt",
}

# Root directory listing
home_contents = "about.txt\nblog/"


# Simple command functions


def cmd_help():
    """Show available commands"""
    help_text = """help              Show available commands
ls                List directory contents
echo              Display text
whoami            Show current user
pwd               Print working directory
clear             Clear screen
cd                Change directory
cat               Display file contents"""
    return ("text", help_text, None)


def cmd_whoami():
    """Show current user"""
    return ("text", "user@sigterm", None)


def cmd_clear():
    """Clear screen"""
    return ("text", "", None)


def cmd_pwd(current_dir):
    """Print working directory"""
    if current_dir == "~":
        pwd_output = "/home"
    else:
        pwd_output = f"/home/{current_dir}"
    return ("text", pwd_output, None)


# Complex command functions


def cmd_ls(target, current_dir):
    """List directory contents with optional target argument"""
    if target is None:
        # ls without arguments - list current directory
        if current_dir == "~":
            return ("text", home_contents, None)
        else:
            # Inside a directory, show parent (..)
            return ("text", "..", None)

    # Check if ls has a target argument
    if target == "..":
        # List parent directory
        if current_dir == "~":
            return ("text", "ls: ..: No such file or directory", None)
        else:
            return ("text", home_contents, None)
    elif target == "~" or target == "." or target == "/home":
        # List root/home directory
        return ("text", home_contents, None)
    else:
        return ("text", f"ls: {target}: No such file or directory", None)


def cmd_cat(target):
    """Display file contents (.txt or .md files)"""
    if target is None:
        # cat without arguments
        return ("text", "cat: missing file argument\nUsage: cat <file>", None)

    # Check if trying to cat a .py file (directory)
    if target in py_files or target.endswith(".py"):
        target_base = target.replace(".py", "") if target.endswith(".py") else target
        if target_base in py_files:
            return ("text", f"cat: {target}: Is a directory\nUse 'cd {target_base}' to explore it", None)

    # Check if target is a .txt or .md file (remove extension if provided)
    if target.endswith(".txt"):
        target_base = target[:-4]
    elif target.endswith(".md"):
        target_base = target[:-3]
    else:
        target_base = target
        # Try to determine file type from txt_files mapping
        if target_base not in txt_files:
            target = f"{target}.txt"

    if target_base in txt_files:
        pages_dir = os.path.join(os.path.dirname(__file__), "pages")
        file_path = os.path.join(pages_dir, txt_files[target_base])
        try:
            with open(file_path, "r") as f:
                content = f.read()
            # Check if file is markdown
            if txt_files[target_base].endswith(".md"):
                return ("markdown", content, None)
            else:
                return ("text", content, None)
        except FileNotFoundError:
            return ("text", f"cat: {target}: No such file or directory", None)
        except Exception as e:
            return ("text", f"cat: Error reading {target}: {str(e)}", None)
    else:
        return ("text", f"cat: {target}: No such file or directory", None)


def cmd_echo(text):
    """Echo text back to user"""
    if text is None:
        return ("text", "", None)
    return ("text", text, None)


def cmd_cd(target, current_dir):
    """Change directory with navigation logic"""
    if target is None:
        # cd without arguments
        return ("text", "cd: missing directory argument\nUsage: cd <directory>", None)

    if target == "..":
        # Navigate back to root/parent
        if current_dir != "~":
            return ("text", home_contents, "~")
        else:
            return ("text", "Already at root directory", None)
    elif target == "~":
        # Navigate to home/root
        if current_dir != "~":
            return ("text", "Navigated to home", "~")
        else:
            return ("text", "Already at home", None)
    elif target:
        # Check if trying to cd into a .txt file
        if target in txt_files or target.endswith(".txt"):
            target_base = target.replace(".txt", "") if target.endswith(".txt") else target
            if target_base in txt_files:
                return ("text", f"cd: {target}: Is a text file\nUse 'cat {target_base}' to view its contents", None)

        # Check if it's a .py file (directory)
        if target in py_files:
            # Load the .py file content
            content_file = py_files[target].replace(".py", "")
            page_result = load_page(content_file)
            if page_result:
                return (page_result[0], page_result[1], target)
        return ("text", f"cd: {target}: No such file or directory", None)
    else:
        return ("text", "cd: missing directory argument", None)


# Command dispatcher


def process_command(cmd, current_dir="~"):
    """Process terminal commands with directory context

    Args:
        cmd: Command string to process
        current_dir: Current directory context (~ for root, or directory name)

    Returns:
        tuple: (result_type, content, new_directory) where new_directory is None if unchanged
    """
    # Parse command and arguments
    parts = cmd.split(maxsplit=1)
    command = parts[0] if parts else ""
    args = parts[1] if len(parts) > 1 else None

    # Route to appropriate command function
    if command == "help":
        return cmd_help()
    elif command == "whoami":
        return cmd_whoami()
    elif command == "clear":
        return cmd_clear()
    elif command == "pwd":
        return cmd_pwd(current_dir)
    elif command == "ls":
        return cmd_ls(args, current_dir)
    elif command == "cat":
        return cmd_cat(args)
    elif command == "echo":
        return cmd_echo(args)
    elif command == "cd":
        return cmd_cd(args, current_dir)
    else:
        return ("text", f"command not found: {cmd}", None)
