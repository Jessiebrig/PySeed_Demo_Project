#!/usr/bin/env python3
"""
Project Entry Point

This allows the project package to be run as a module:
python -m project

This script handles virtual environment setup automatically.
"""

import sys
from pathlib import Path

# ==========================================================================
# PROJECT CONSTANTS (Safe from user config.py modifications)
# ==========================================================================

# Core paths
if getattr(sys, 'frozen', False):
    # Running as executable - use executable's directory
    PROJECT_ROOT = Path(sys.executable).parent
    PROJECT_DIR = PROJECT_ROOT
else:
    # Running as script - use normal path resolution
    PROJECT_ROOT = Path(__file__).parent.parent.resolve()
    PROJECT_DIR = Path(__file__).parent

def _get_project_name():
    """Get project name from folder."""
    if getattr(sys, 'frozen', False):
        # Running as executable - use parent directory name (the actual project root)
        return PROJECT_ROOT.parent.name
    else:
        # Running as script - use project root name
        return PROJECT_ROOT.name

def _get_version():
    """Get version from appmanager config."""
    if getattr(sys, 'frozen', False):
        # Running as executable - use parent directory to find version file
        version_file = PROJECT_ROOT.parent / "requirements" / "version.txt"
        if version_file.exists():
            return version_file.read_text().strip()
        return "1.0.0"  # Fallback
    else:
        # Running as script
        try:
            sys.path.insert(0, str(PROJECT_ROOT))
            from appmanager import config as app_config
            return app_config.VERSION
        except ImportError:
            return "1.0.0"  # Fallback

PROJECT_NAME = _get_project_name()
VERSION = _get_version()



# Import environment manager for bootstrap
from appmanager.environment import VenvManager

def main():
    """Main entry point for the application."""
    # Check if running as executable (PyInstaller sets sys.frozen)
    if getattr(sys, 'frozen', False):
        # Running as executable - skip venv setup
        from project.core import MainApplication
        app = MainApplication()
        app.run()
    else:
        # Running as script - ensure virtual environment is active
        venv_manager = VenvManager()
        venv_manager.ensure_active()
        
        # Import and run project after venv is active
        from project.core import MainApplication
        app = MainApplication()
        app.run()


if __name__ == "__main__":
    main()