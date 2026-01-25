# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
LaTeX book project initialization.

Can be used as:
1. Module: from init_book import init_project
2. Standalone: uv run init_book.py

Example:
    uv run init_book.py
"""

import sys
from pathlib import Path


def init_project(project_root: Path, echo=print, success_style=None, error_style=None) -> int:
    """
    Initialize a LaTeX book project.

    Args:
        project_root: Path to the project root
        echo: Function for normal output
        success_style: Function for success messages
        error_style: Function for error messages

    Returns:
        0 on success, 1 on error
    """
    if success_style is None:
        success_style = echo
    if error_style is None:
        error_style = echo

    echo(f"Initializing LaTeX book project in {project_root}")
    echo("-" * 50)

    from init_latex import scaffold_latex
    scaffold_latex(project_root, echo)

    echo("-" * 50)
    success_style("Book project initialized successfully!")
    return 0


def main():
    """Standalone entry point."""
    project_root = Path.cwd()
    return_code = init_project(project_root)
    sys.exit(return_code)


if __name__ == "__main__":
    main()
