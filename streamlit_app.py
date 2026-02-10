import streamlit as st
import os
import importlib.util
import sys

st.set_page_config(page_title="Inference", layout="wide")

def load_page(page_name):
    """Load page content from pages directory
    Returns: (content_type, content) where content_type is 'text' or 'streamlit'
    """
    pages_dir = os.path.join(os.path.dirname(__file__), "pages")

    # Try .py file first (Streamlit pages)
    py_path = os.path.join(pages_dir, f"{page_name}.py")
    if os.path.exists(py_path):
        try:
            spec = importlib.util.spec_from_file_location(f"page_{page_name}", py_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[f"page_{page_name}"] = module
            spec.loader.exec_module(module)
            if hasattr(module, "render"):
                return ("streamlit", module.render)
        except Exception as e:
            return ("text", f"Error loading page: {str(e)}")

    # Try .txt file (text pages)
    txt_path = os.path.join(pages_dir, f"{page_name}.txt")
    if os.path.exists(txt_path):
        with open(txt_path, "r") as f:
            return ("text", f.read())

    return None

def process_command(cmd, current_dir="~"):
    """Process terminal commands with directory context

    Args:
        cmd: Command string to process
        current_dir: Current directory context (~ for root, or directory name)

    Returns:
        tuple: (result_type, content, new_directory) where new_directory is None if unchanged
    """
    # Define filesystem structure
    # .py files are directories (accessible via cd)
    py_files = {
        "blog": "blog.py",
    }

    # .txt files are text files (readable via cat)
    txt_files = {
        "about": "about.txt",
    }

    help_text = """help              Show available commands
ls                List directory contents
echo              Display text
whoami            Show current user
clear             Clear screen
cd                Change directory
cat               Display file contents"""

    commands = {
        "help": help_text,
        "whoami": "user@inference",
        "clear": "",
    }

    # Dynamic ls based on current directory
    if cmd == "ls":
        if current_dir == "~":
            return ("text", "about.txt\nblog/", None)
        else:
            # Inside a directory, show parent
            return ("text", "..", None)

    if cmd in commands:
        return ("text", commands[cmd], None)
    elif cmd == "cat" or cmd == "cat ":
        # cat without arguments
        return ("text", "cat: missing file argument\nUsage: cat <file>", None)
    elif cmd.startswith("cat "):
        # cat command to display .txt file contents
        target = cmd[4:].strip()

        # Check if trying to cat a .py file (directory)
        if target in py_files or target.endswith(".py"):
            target_base = target.replace(".py", "") if target.endswith(".py") else target
            if target_base in py_files:
                return ("text", f"cat: {target}: Is a directory\nUse 'cd {target_base}' to explore it", None)

        # Check if target is a .txt file (remove extension if provided)
        if target.endswith(".txt"):
            target_base = target[:-4]
        else:
            target_base = target
            target = f"{target}.txt"

        if target_base in txt_files:
            pages_dir = os.path.join(os.path.dirname(__file__), "pages")
            file_path = os.path.join(pages_dir, txt_files[target_base])
            try:
                with open(file_path, "r") as f:
                    content = f.read()
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
                # Show what ls would display at parent level
                parent_ls_output = "about.txt\nblog/"
                return ("text", parent_ls_output, "~")
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

st.markdown("""
<style>
    .main { background-color: #000000; color: #00FF00; }
    input { background-color: #0a0a0a !important; color: #00FF00 !important;
            border: 1px solid #00FF00 !important; font-family: 'Courier New', monospace !important; }
    .stCode { background-color: #0a0a0a !important; border: 1px solid #00FF00 !important; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    [data-testid="stSidebar"] { display: none; }
    .terminal-prompt { color: #00FF00; font-family: 'Courier New', monospace; font-weight: bold; }
    .title-link { color: #00FF00; text-decoration: none; }
    .title-link:hover { text-decoration: underline; }
</style>
<h1><a href="?" target="_self" class="title-link">$ Inference</a></h1>
""", unsafe_allow_html=True)

if "commands" not in st.session_state:
    st.session_state.commands = []
    st.session_state.outputs = []
    st.session_state.current_dir = "~"

# Display only the last command and output
if st.session_state.commands and st.session_state.outputs:
    cmd = st.session_state.commands[-1]
    output_data = st.session_state.outputs[-1]

    st.markdown(f"<span class='terminal-prompt'>$ {cmd}</span>", unsafe_allow_html=True)

    if output_data["type"] == "text":
        st.code(output_data["content"], language="bash")
    elif output_data["type"] == "streamlit":
        with st.container():
            try:
                output_data["content"](st)
            except Exception as e:
                st.error(f"Error rendering page: {str(e)}")

def submit_command():
    if st.session_state.input:
        if st.session_state.input == "clear":
            st.session_state.commands = []
            st.session_state.outputs = []
        else:
            st.session_state.commands.append(st.session_state.input)
            content_type, content, new_dir = process_command(st.session_state.input, st.session_state.current_dir)
            st.session_state.outputs.append({"type": content_type, "content": content})
            # Update directory if changed
            if new_dir is not None:
                st.session_state.current_dir = new_dir
        st.session_state.input = ""

st.text_input("$ ", key="input", placeholder="Type command (e.g. help)...", on_change=submit_command)
