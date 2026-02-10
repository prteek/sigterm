# Terminal App

This is a terminal interface like a web app for a personal portfolio, built using Streamlit.

## Environment

- Python version: 3.13 (managed via pyenv)
- Virtual environment: `terminal_app` (activated with `pyenv activate terminal_app`)

## Project Structure

```
terminal_app/
├── .claude/                          # Claude Code configuration
│   ├── skills/                       # Available skills
│   │   └── refresh/                  # Documentation refresh skill
│   │       └── SKILL.md
│   └── settings.local.json           # Claude Code settings
├── .streamlit/                       # Streamlit configuration
│   └── config.toml                   # Theme and client settings
├── app.py                            # Main Streamlit application
└── CLAUDE.md                         # This file
```

## Architecture

The application is a Streamlit-based terminal emulator for a personal portfolio site.

### Key Files

**app.py** - Main application file
- Defines terminal-style UI with dark theme (#000000 background, #00FF00 green text)
- Implements command processing logic with support for: `help`, `ls`, `echo`, `whoami`
- Maintains command history using Streamlit session state
- Custom CSS styling for terminal appearance

**Streamlit Configuration** (`.streamlit/config.toml`)
- Dark theme with green terminal styling
- Error details enabled for development

## Skills

### refresh (`.claude/skills/refresh/`)
Updates and refreshes CLAUDE.md documentation. This skill audits the project structure, reviews existing documentation, and updates CLAUDE.md with current agent, skill, and configuration information.

**Invocation:**
```
/refresh
```

## Development

To work on this project:

1. Ensure Python 3.13 is installed via pyenv
2. Activate the virtual environment: `pyenv activate terminal_app`
3. Install dependencies if needed: `pip install streamlit`
4. Run the app: `streamlit run app.py`
