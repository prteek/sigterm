# Terminal App

A terminal interface for a personal portfolio, built with Streamlit. Implements a functional command-line emulator with dark green retro styling and command history.

## Setup

- **Python version:** 3.13 (via pyenv)
- **Virtual env:** `pyenv activate terminal_app`
- **Install:** `pip install streamlit`
- **Run:** `streamlit run app.py`

## Project Structure

- **app.py** - Main Streamlit application (terminal emulator)
- **.streamlit/config.toml** - Theme configuration (dark green terminal style)
- **.gitignore** - Python cache and build files excluded

## App Features

**Terminal Emulator** (app.py):
- Dark green retro theme (#000000 background, #00FF00 text)
- Monospace font styling with custom CSS
- Command processing: `help`, `ls`, `echo`, `whoami`
- `echo` command: echoes user input
- Command history stored in session state
- Input callback (`on_change`) for command submission
- Hidden Streamlit UI elements (menu, footer)

**Theme Configuration** (.streamlit/config.toml):
- Primary/text color: #00FF00 (green)
- Background: #000000 (black)
- Secondary background: #0a0a0a (dark gray)
- Font: monospace
- Error details: enabled

## Skills

- **refresh** - Audits project structure and updates CLAUDE.md (`/refresh`)

## Git

- **Commits** - Never include `Co-Authored-By` trailers in commit messages
