import streamlit as st

st.set_page_config(page_title="Terminal", layout="wide")

def process_command(cmd):
    """Your command logic"""
    commands = {
        "help": "Available: help, ls, echo, whoami",
        "ls": "file1.txt\nfile2.txt\nfolder/",
        "whoami": "user@terminal-app",
    }

    if cmd in commands:
        return commands[cmd]
    elif cmd.startswith("echo "):
        return cmd.replace("echo ", "")
    else:
        return f"command not found: {cmd}"

# Custom CSS for terminal look
st.markdown("""
<style>
    /* Dark terminal background */
    .main {
        background-color: #000000;
        color: #00FF00;
    }

    /* Terminal-style text input */
    input {
        background-color: #0a0a0a !important;
        color: #00FF00 !important;
        border: 1px solid #00FF00 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 14px !important;
    }

    /* Code blocks styled as terminal output */
    .stCode {
        background-color: #0a0a0a !important;
        border: 1px solid #00FF00 !important;
    }

    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Terminal prompt styling */
    .terminal-prompt {
        color: #00FF00;
        font-family: 'Courier New', monospace;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("$ Terminal")

if "commands" not in st.session_state:
    st.session_state.commands = []
    st.session_state.output = []

# Display command history
for cmd, out in zip(st.session_state.commands, st.session_state.output):
    st.markdown(f"<span class='terminal-prompt'>$ {cmd}</span>", unsafe_allow_html=True)
    st.code(out, language="bash")

# Command input
user_input = st.text_input("$ ", key="input", placeholder="Type command...")

if user_input:
    st.session_state.commands.append(user_input)
    result = process_command(user_input)
    st.session_state.output.append(result)
    st.session_state.input = ""
    st.rerun()
