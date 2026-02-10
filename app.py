import streamlit as st

st.set_page_config(page_title="Terminal", layout="wide")

def process_command(cmd):
    commands = {
        "help": "Available: help, ls, echo, whoami",
        "ls": "file1.txt\nfile2.txt\nfolder/",
        "whoami": "user@terminal-app",
    }
    if cmd in commands:
        return commands[cmd]
    elif cmd.startswith("echo "):
        return cmd[5:]
    return f"command not found: {cmd}"

st.markdown("""
<style>
    .main { background-color: #000000; color: #00FF00; }
    input { background-color: #0a0a0a !important; color: #00FF00 !important;
            border: 1px solid #00FF00 !important; font-family: 'Courier New', monospace !important; }
    .stCode { background-color: #0a0a0a !important; border: 1px solid #00FF00 !important; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .terminal-prompt { color: #00FF00; font-family: 'Courier New', monospace; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("$ Terminal")

if "commands" not in st.session_state:
    st.session_state.commands = []
    st.session_state.output = []

for cmd, out in zip(st.session_state.commands, st.session_state.output):
    st.markdown(f"<span class='terminal-prompt'>$ {cmd}</span>", unsafe_allow_html=True)
    st.code(out, language="bash")

user_input = st.text_input("$ ", key="input", placeholder="Type command...")
if user_input:
    st.session_state.commands.append(user_input)
    st.session_state.output.append(process_command(user_input))
    st.session_state.input = ""
    st.rerun()
