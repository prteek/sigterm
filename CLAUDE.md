# Terminal App

A terminal interface for a personal portfolio, built with Streamlit.

## Setup

- Python 3.13 (via pyenv)
- Virtual env: `pyenv activate terminal_app`
- Install: `pip install streamlit`
- Run: `streamlit run app.py`

## App

**app.py** - Terminal emulator with:
- Dark green terminal theme (#000000 bg, #00FF00 text)
- Commands: `help`, `ls`, `echo`, `whoami`
- Command history via session state

**Config** - `.streamlit/config.toml` sets theme and error details

## Skills

- **refresh** - Updates CLAUDE.md documentation (`/refresh`)

## Git

- **Commits** - Never include `Co-Authored-By` trailers in commit messages
