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


def init_project(
    project_root: Path,
    title: str | None = None,
    subtitle: str | None = None,
    description: str | None = None,
    authors: tuple[str, ...] = (),
    year: str | None = None,
    edition: str | None = None,
    publisher: str | None = None,
    city: str | None = None,
    state: str | None = None,
    zip_code: str | None = None,
    country: str | None = None,
    language: str | None = None,
    book_type: str | None = None,
    theme: str | None = None,
    echo=print,
    success_style=None,
    error_style=None
) -> int:
    """
    Initialize a LaTeX book project.

    Args:
        project_root: Path to the project root
        title: Book title
        subtitle: Book subtitle
        description: Book description
        authors: Tuple of author names
        year: Publication year
        edition: Book edition
        publisher: Publisher name
        city: Publisher city
        state: Publisher state
        zip_code: Publisher zip code
        country: Publisher country
        language: Book language (e.g., english, norsk)
        book_type: Book type
        theme: Book theme
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

    metadata = {
        "title": title,
        "subtitle": subtitle,
        "description": description,
        "authors": authors,
        "year": year,
        "edition": edition,
        "publisher": publisher,
        "city": city,
        "state": state,
        "zip_code": zip_code,
        "country": country,
        "language": language,
        "book_type": book_type,
        "theme": theme,
    }

    from init_latex import scaffold_latex
    scaffold_latex(project_root, metadata, echo)

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
