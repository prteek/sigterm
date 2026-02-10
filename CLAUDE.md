# Inference Terminal

A terminal interface for a personal portfolio, built with Streamlit. Implements a functional command-line emulator with dark green retro styling, command history, and dynamic page loading system.

## Setup

- **Python version:** 3.13 (via pyenv)
- **Virtual env:** `pyenv activate terminal_app`
- **Install:** `pip install streamlit beautifulsoup4 requests`
- **Run:** `streamlit run streamlit_app.py`

## Project Structure

- **streamlit_app.py** - Main Streamlit application (terminal emulator with command processing)
- **pages/** - Dynamic page content directory
  - **blog.py** - Dynamic blog fetcher (loads posts from Regression Room)
  - **about.txt** - Text about page
  - **about_me.md** - Markdown about page
- **.streamlit/config.toml** - Theme configuration (dark green terminal style)
- **test_streamlit_app.py** - Unit tests for command processing
- **.gitignore** - Python cache and build files excluded

## App Features

**Terminal Emulator** (streamlit_app.py):
- Dark green retro theme (#000000 background, #00FF00 text)
- Monospace font styling with custom CSS
- Functional filesystem simulator with `/home` directory structure
- Command processing with directory context awareness
- Command history stored in session state
- Input callback (`on_change`) for command submission
- Hidden Streamlit UI elements (menu, footer)

**Supported Commands:**
- `help` - Show available commands
- `ls [target]` - List directory contents (supports `.`, `..`, `~`, `/home`)
- `cd <directory>` - Navigate directories (supports `.`, `..`, `~`, and subdirectories like `blog`)
- `cat <file>` - Display file contents (supports `.txt` and `.md` files with markdown rendering)
- `pwd` - Print working directory
- `echo [text]` - Display text
- `whoami` - Show current user (`user@inference`)
- `clear` - Clear command history

**Dynamic Pages:**
- Pages are loaded from the `pages/` directory
- `.py` files define Streamlit pages with a `render(st)` function
- `.txt` and `.md` files are displayed as text content
- Blog page (`cd blog`) fetches posts from external website

**Theme Configuration** (.streamlit/config.toml):
- Primary/text color: #00FF00 (green)
- Background: #000000 (black)
- Secondary background: #0a0a0a (dark gray)
- Font: monospace
- Error details: enabled

**Testing:**
- Unit tests in `test_streamlit_app.py`
- Tests cover all commands and directory navigation
- Run with `pytest test_streamlit_app.py`

## Skills

- **refresh** - Audits project structure and updates CLAUDE.md (`/refresh`)

## Git

- **Commits** - Never include `Co-Authored-By` trailers in commit messages
