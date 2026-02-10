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
    "about_me": "about_me.md",
}

# Root directory listing
home_contents = "about.txt\nabout_me.md\nblog/"


def process_command(cmd, current_dir="~"):
    """Process terminal commands with directory context

    Args:
        cmd: Command string to process
        current_dir: Current directory context (~ for root, or directory name)

    Returns:
        tuple: (result_type, content, new_directory) where new_directory is None if unchanged
    """
    help_text = """help              Show available commands
ls                List directory contents
echo              Display text
whoami            Show current user
pwd               Print working directory
clear             Clear screen
cd                Change directory
cat               Display file contents"""

    # Generate pwd output based on current directory
    if current_dir == "~":
        pwd_output = "/home"
    else:
        pwd_output = f"/home/{current_dir}"

    commands = {
        "help": help_text,
        "whoami": "user@inference",
        "clear": "",
        "pwd": pwd_output,
    }

    # Dynamic ls based on current directory
    if cmd == "ls" or cmd.startswith("ls "):
        # Check if ls has a target argument
        if cmd.startswith("ls "):
            target = cmd[3:].strip()
            if target == "..":
                # List parent directory
                if current_dir == "~":
                    return ("text", f"ls: ..: No such file or directory", None)
                else:
                    return ("text", home_contents, None)
            elif target == "~" or target == "." or target == "/home":
                # List root/home directory
                return ("text", home_contents, None)
            else:
                return ("text", f"ls: {target}: No such file or directory", None)
        else:
            # ls without arguments - list current directory
            if current_dir == "~":
                return ("text", home_contents, None)
            else:
                # Inside a directory, show parent (..)
                return ("text", "..", None)

    if cmd in commands:
        return ("text", commands[cmd], None)
    elif cmd == "cat" or cmd == "cat ":
        # cat without arguments
        return ("text", "cat: missing file argument\nUsage: cat <file>", None)
    elif cmd.startswith("cat "):
        # cat command to display .txt or .md file contents
        target = cmd[4:].strip()

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
    elif cmd == "echo" or cmd == "echo ":
        # echo without arguments
        return ("text", "", None)
    elif cmd.startswith("echo "):
        return ("text", cmd[5:], None)
    elif cmd == "cd" or cmd == "cd ":
        # cd without arguments
        return ("text", "cd: missing directory argument\nUsage: cd <directory>", None)
    elif cmd.startswith("cd "):
        # cd command to navigate into pages or directories
        target = cmd[3:].strip()
        if target == "..":
            # Navigate back to root/parent
            if current_dir != "~":
                # Show what ls would display at parent level (/home)
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
    else:
        return ("text", f"command not found: {cmd}", None)
