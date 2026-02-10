# Sigterm

A terminal interface for a personal portfolio, built with Streamlit. Implements a functional command-line emulator with dark green retro styling, command history, and dynamic page loading system.

## Setup

- **Python version:** 3.13 (via pyenv)
- **Virtual env:** `pyenv activate sigterm`
- **Install:** `pip install -r requirements.txt`
- **Run:** `streamlit run streamlit_app.py`
- **Tests:** `pytest`

## Project Structure

- **streamlit_app.py** - Main Streamlit application (terminal emulator UI and session management)
- **commands.py** - Command processing module (all command implementations and dispatcher)
- **page_loader.py** - Dynamic page loader utility (loads .py, .txt, and .md pages)
- **pages/** - Dynamic page content directory
  - **blog.py** - Dynamic blog fetcher page (loads posts from Regression Room)
  - **about.txt** - Text about page
- **tests/** - Unit test directory (organized by command)
  - **conftest.py** - Shared test configuration and fixtures
  - **test_help.py** - Help command tests
  - **test_ls.py** - Ls command tests
  - **test_pwd.py** - Pwd command tests
  - **test_whoami.py** - Whoami command tests
  - **test_echo.py** - Echo command tests
  - **test_clear.py** - Clear command tests
  - **test_cd.py** - Cd command tests
  - **test_cat.py** - Cat command tests
  - **test_invalid.py** - Invalid command and general behavior tests
- **pytest.ini** - Pytest configuration
- **.streamlit/config.toml** - Theme configuration (dark green terminal style)
- **requirements.txt** - Python dependencies (streamlit, pytest, beautifulsoup4, requests)
- **.gitignore** - Python cache and build files excluded

## App Features

**Terminal Emulator** (streamlit_app.py):
- Dark green retro theme (#000000 background, #00FF00 text)
- Monospace font styling with custom CSS
- Session state management for command history and directory context
- Input callback (`on_change`) for command submission
- Output rendering (text, markdown, or Streamlit components)
- Hidden Streamlit UI elements (menu, footer)

**Command Processing** (commands.py):
- Modular command functions (help, whoami, clear, pwd, ls, cat, echo, cd)
- Directory context awareness for navigation
- Filesystem structure configuration (py_files, txt_files, home_contents)
- Consistent return format: (content_type, content, new_directory)

**Dynamic Page Loading** (page_loader.py):
- Loads .py files as Streamlit pages with `render(st)` function
- Loads .txt and .md files as text content
- Returns (content_type, content) for streamlit_app.py integration

**Supported Commands:**
- `help` - Show available commands
- `ls [target]` - List directory contents (supports `.`, `..`, `~`, `/home`)
- `cd <directory>` - Navigate directories (supports `.`, `..`, `~`, and subdirectories like `blog`)
- `cat <file>` - Display file contents (supports `.txt` and `.md` files with markdown rendering)
- `pwd` - Print working directory
- `echo [text]` - Display text
- `whoami` - Show current user (`user@sigterm`)
- `clear` - Clear command history

**Dynamic Pages:**
- Pages are loaded on-demand via `page_loader.py`
- `.py` files define Streamlit pages with a `render(st)` function
- `.txt` and `.md` files are displayed as text content (markdown rendered for .md)
- Blog page (`cd blog`) fetches posts from external website
- Filesystem mapping in `commands.py`: py_files dict for directories, txt_files dict for text content

**Theme Configuration** (.streamlit/config.toml):
- Primary/text color: #00FF00 (green)
- Background: #000000 (black)
- Secondary background: #0a0a0a (dark gray)
- Font: monospace
- Error details: enabled

**Testing:**
- Unit tests organized in `tests/` directory by command
- 43 tests cover all commands and directory navigation
- Run with `pytest` (configured via pytest.ini)
- Each test file contains a single command class with related tests

## Skills

- **refresh** - Audits project structure and updates CLAUDE.md (`/refresh`)

## Git

- **Commits** - Never include `Co-Authored-By: ` trailer in commit messages
