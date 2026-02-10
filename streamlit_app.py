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
    # Define directory structure
    directories = {
        "blog": {"type": "directory", "content": "blog.py"},
    }

    commands = {
        "help": "Available: help, ls, echo, whoami, clear, cd, cat",
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
    elif cmd.startswith("cat "):
        # cat command to display file contents
        target = cmd[4:].strip()
        if target == "about.txt":
            pages_dir = os.path.join(os.path.dirname(__file__), "pages")
            about_path = os.path.join(pages_dir, "about.txt")
            try:
                with open(about_path, "r") as f:
                    content = f.read()
                return ("text", content, None)
            except FileNotFoundError:
                return ("text", f"cat: {target}: No such file or directory", None)
            except Exception as e:
                return ("text", f"cat: Error reading {target}: {str(e)}", None)
        else:
            return ("text", f"cat: {target}: No such file or directory", None)
    elif cmd.startswith("echo "):
        return ("text", cmd[5:], None)
    elif cmd.startswith("cd "):
        # cd command to navigate into pages or directories
        target = cmd[3:].strip()
        if target == "..":
            # Navigate back to root
            if current_dir != "~":
                return ("text", f"Navigated back from {current_dir}", "~")
            else:
                return ("text", "Already at root directory", None)
        elif target == "~":
            # Navigate to home/root
            if current_dir != "~":
                return ("text", "Navigated to home", "~")
            else:
                return ("text", "Already at home", None)
        elif target:
            # Check if it's a directory
            if target in directories:
                # Load the directory's content file
                content_file = directories[target]["content"].replace(".py", "")
                page_result = load_page(content_file)
                if page_result:
                    return (page_result[0], page_result[1], target)
            # Try to load as a page
            page_result = load_page(target)
            if page_result:
                return (page_result[0], page_result[1], target)
            return ("text", f"cd: {target}: No such file or directory", None)
        else:
            return ("text", "cd: missing directory argument", None)
    else:
        # Try to load as a page
        page_result = load_page(cmd)
        if page_result:
            return page_result + (None,)
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
