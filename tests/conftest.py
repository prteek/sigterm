"""Shared test fixtures and configuration"""
import sys
from pathlib import Path

# Add parent directory to path so we can import commands
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from commands import process_command
