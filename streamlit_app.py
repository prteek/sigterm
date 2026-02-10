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

def process_command(cmd):
    commands = {
        "help": "Available: help, ls, echo, whoami, about, blog, clear",
        "ls": "about/\nblog/\ncontact.txt",
        "whoami": "user@inference",
        "clear": "",
    }

    if cmd in commands:
        return ("text", commands[cmd])
    elif cmd.startswith("echo "):
        return ("text", cmd[5:])
    else:
        # Try to load as a page
        page_result = load_page(cmd)
        if page_result:
            return page_result
        return ("text", f"command not found: {cmd}")

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
<h1><a href="?" class="title-link">$ Inference</a></h1>
""", unsafe_allow_html=True)

if "commands" not in st.session_state:
    st.session_state.commands = []
    st.session_state.outputs = []

for cmd, output_data in zip(st.session_state.commands, st.session_state.outputs):
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
            content_type, content = process_command(st.session_state.input)
            st.session_state.outputs.append({"type": content_type, "content": content})
        st.session_state.input = ""

st.text_input("$ ", key="input", placeholder="Type command...", on_change=submit_command)
