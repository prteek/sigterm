import streamlit as st
from commands import process_command

st.set_page_config(page_title="Sigterm", layout="wide")

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
<h1><a href="?" target="_self" class="title-link">$ Sigterm</a></h1>
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
    elif output_data["type"] == "markdown":
        st.markdown(output_data["content"])
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
