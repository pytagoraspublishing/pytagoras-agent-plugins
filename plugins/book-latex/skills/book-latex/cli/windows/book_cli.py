"""
Book CLI - Command line tool for managing LaTeX book projects.

Usage:
    book init               # Initialize a new book project
    book compile [FILENAME] # Compile a LaTeX file
    book compile --bib      # Compile with bibliography (biber)
    book image new          # Generate a new image
    book image edit         # Edit an existing image

Examples:
    book init               # Create a new LaTeX book project
    book compile            # Compiles main.tex
    book compile ch01       # Compiles ch01-*.tex (prefix match)
    book compile --bib      # Compiles main.tex with bibliography
    book image new --path "figures/diagram.png" "A flowchart..."
    book image edit --path "figures/chart.png" "Add a legend"
"""

import sys
from functools import partial
from pathlib import Path

import click

from compile_latex import find_tex_file, run_compile, AmbiguousTargetError
from init_book import init_project
from image_gen import generate_image, edit_image


@click.group()
def cli():
    """Book CLI - Tools for managing LaTeX book projects."""
    pass


@cli.command()
@click.argument("filename", default="main")
@click.option("--bib", "-b", is_flag=True, help="Also compile bibliography with biber")
def compile(filename: str, bib: bool):
    """Compile a LaTeX file from the book.

    FILENAME is the name of the .tex file without extension (default: main).

    Supports:
    - Prefix matching: 'ch01' will find 'ch01-ettersporselprognoser.tex'
    - Numeric notation: '3.5.13' for part 3, chapter 5, section 13
    - Appendix notation: 'A.1' for appendix 1, 'A.2.5' for appendix 2 section 5

    Examples:

        book compile              # Compiles main.tex

        book compile ch01         # Compiles ch01-*.tex

        book compile 3.5          # Compiles part03/ch05

        book compile A.1          # Compiles app01 in backmatter

        book compile --bib        # Compiles main.tex with bibliography

        book compile main --bib   # Same as above
    """
    # Find latex directory relative to current working directory
    cwd = Path.cwd()
    latex_dir = cwd / "latex"

    if not latex_dir.exists():
        click.secho(f"Error: latex directory not found at {latex_dir}", fg="red")
        click.echo("Make sure you run this command from the project root.")
        sys.exit(1)

    # Check for excluded file
    if filename == "localsettings":
        click.secho("Error: localsettings.tex is not a standalone file and cannot be compiled.", fg="red")
        sys.exit(1)

    # Find the tex file
    try:
        tex_file = find_tex_file(latex_dir, filename)
    except AmbiguousTargetError as e:
        click.secho(f"Error: '{e.target}' matches multiple files:", fg="red")
        for i, match in enumerate(e.matches, 1):
            rel_path = match.relative_to(latex_dir)
            click.echo(f"  {i}. {rel_path}")
        if e.suggestions:
            click.echo()
            click.secho("Use numeric notation to specify which one:", fg="yellow")
            for suggestion, path in e.suggestions:
                rel_path = path.relative_to(latex_dir)
                click.echo(f"  book compile {suggestion}  # {rel_path}")
        sys.exit(1)

    if tex_file is None:
        click.secho(f"Error: Could not find {filename}.tex in {latex_dir}", fg="red")
        sys.exit(1)

    # Compile with click-styled output
    return_code = run_compile(
        tex_file,
        latex_dir,
        bib=bib,
        echo=click.echo,
        success_style=partial(click.secho, fg="green"),
        error_style=partial(click.secho, fg="red")
    )
    sys.exit(return_code)


@cli.command()
@click.option("--title", help="Book title")
@click.option("--subtitle", help="Book subtitle")
@click.option("--description", help="Book description")
@click.option("--authors", multiple=True, help="Book authors (can be specified multiple times)")
@click.option("--year", help="Publication year")
@click.option("--edition", help="Book edition")
@click.option("--publisher", help="Publisher name")
@click.option("--city", help="Publisher city")
@click.option("--state", help="Publisher state")
@click.option("--zip", "zip_code", help="Publisher zip code")
@click.option("--country", help="Publisher country")
@click.option("--language", help="Book language (e.g., english, norsk)")
@click.option("--type", "book_type", help="Book type")
@click.option("--theme", help="Book theme")
def init(title, subtitle, description, authors, year, edition, publisher, city, state, zip_code, country, language, book_type, theme):
    """Initialize a new LaTeX book project.

    Creates:
      - config.yaml with project settings
      - latex/ folder with book template

    All options are optional. When provided, they pre-fill the corresponding
    placeholders in the generated files.

    Examples:

        book init              # Create LaTeX book project with placeholders

        book init --title "My Book" --authors "John Doe"

        book init --authors "John Doe" --authors "Jane Smith" --year 2024
    """
    cwd = Path.cwd()

    return_code = init_project(
        cwd,
        title=title,
        subtitle=subtitle,
        description=description,
        authors=authors,
        year=year,
        edition=edition,
        publisher=publisher,
        city=city,
        state=state,
        zip_code=zip_code,
        country=country,
        language=language,
        book_type=book_type,
        theme=theme,
        echo=click.echo,
        success_style=partial(click.secho, fg="green"),
        error_style=partial(click.secho, fg="red")
    )
    sys.exit(return_code)


@cli.group()
def image():
    """Image generation and editing commands.

    Generate new images or edit existing ones using AI (Gemini API).
    Requires GEMINI_API_KEY in .env file.
    """
    pass


@image.command()
@click.option("--path", "-p", required=True, help="Output path for the image (e.g., figures/flowchart.png)")
@click.option("--resolution", "-r", type=click.Choice(["1K", "2K", "4K"]), default="1K", help="Image resolution")
@click.argument("prompt")
def new(path: str, resolution: str, prompt: str):
    """Generate a new image from a text prompt.

    PROMPT is the text description of the image to generate.

    Examples:

        book image new --path "figures/flowchart.png" "A process flowchart"

        book image new -p "diagrams/network.png" -r 4K "Network topology diagram"
    """
    return_code = generate_image(
        prompt=prompt,
        output_path=Path(path),
        resolution=resolution,
        echo=click.echo,
        error_style=partial(click.secho, fg="red")
    )
    sys.exit(return_code)


@image.command()
@click.option("--path", "-p", required=True, help="Path to image to edit (will be overwritten)")
@click.option("--resolution", "-r", type=click.Choice(["1K", "2K", "4K"]), default=None, help="Output resolution (auto-detected if not specified)")
@click.argument("prompt")
def edit(path: str, resolution: str | None, prompt: str):
    """Edit an existing image with a text prompt.

    PROMPT is the text instructions for editing the image.
    The edited image overwrites the original file.

    Examples:

        book image edit --path "figures/chart.png" "Add a legend in the corner"

        book image edit -p "logo.png" -r 2K "Change the color scheme to blue"
    """
    return_code = edit_image(
        prompt=prompt,
        image_path=Path(path),
        resolution=resolution,
        echo=click.echo,
        error_style=partial(click.secho, fg="red")
    )
    sys.exit(return_code)


if __name__ == "__main__":
    cli()
