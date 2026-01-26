# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Core compilation logic for LaTeX books.

Can be used as:
1. Module: from compile_latex import find_tex_file, run_compile
2. Standalone: uv run compile_latex.py [filename]

Examples:
    uv run compile_latex.py              # Compiles main.tex
    uv run compile_latex.py ch01         # Compiles ch01-*.tex (prefix match)
    uv run compile_latex.py ch01-name    # Compiles specific chapter
    uv run compile_latex.py 3.5.13       # Compiles part03/ch05/sec13 (numeric notation)
    uv run compile_latex.py A.1          # Compiles app01 in backmatter (appendix)
"""

import re
import subprocess
import sys
from pathlib import Path


class AmbiguousTargetError(Exception):
    """Raised when multiple files match a simple target."""

    def __init__(self, target: str, matches: list[Path], latex_dir: Path):
        self.target = target
        self.matches = matches
        self.latex_dir = latex_dir

        # Generate numeric suggestions from paths
        self.suggestions = []
        for m in matches:
            suggestion = path_to_numeric_index(m, latex_dir)
            if suggestion:
                self.suggestions.append((suggestion, m))

        super().__init__(f"Ambiguous target '{target}'")


def parse_numeric_target(target: str) -> tuple[str, int, int, int] | None:
    """Parse numeric dot notation into (area, part/appendix, chapter, section).

    Supports:
    - Bodymatter: "3.5.13" -> ("body", 3, 5, 13)
    - Appendix: "A.2.5" -> ("back", 2, 5, 0)  # appendix 2, section 5

    Returns None if not a numeric target.
    Returns (area, num1, num2, num3) where:
    - area: "body" for bodymatter, "back" for backmatter/appendix
    - For body: (part, chapter, section)
    - For back: (appendix, section, 0)
    """
    # Check for appendix notation: A.x or A.x.x
    if target.upper().startswith('A.'):
        rest = target[2:]  # Remove "A."
        if not re.match(r'^\d+(\.\d+)?$', rest):
            return None
        nums = [int(x) for x in rest.split('.')]
        while len(nums) < 2:
            nums.append(0)
        return ("back", nums[0], nums[1], 0)

    # Check if it matches numeric pattern: digits separated by dots
    if not re.match(r'^\d+(\.\d+){0,2}$', target):
        return None

    parts = [int(x) for x in target.split('.')]

    # Pad with zeros to always have 3 elements
    while len(parts) < 3:
        parts.append(0)

    return ("body", parts[0], parts[1], parts[2])  # (area, part, chapter, section)


def find_by_numeric_index(latex_dir: Path, area: str, num1: int, num2: int, num3: int) -> Path | None:
    """Find tex file by numeric indices.

    Args:
        latex_dir: Path to the latex directory
        area: "body" for bodymatter, "back" for backmatter/appendix
        num1: Part number (body) or Appendix number (back). 0 means no part.
        num2: Chapter number (body) or Section number (back). 0 means target is part/appendix.
        num3: Section number (body only). 0 means target is chapter.
    """
    if area == "back":
        return find_appendix_file(latex_dir, num1, num2)
    else:
        return find_bodymatter_file(latex_dir, num1, num2, num3)


def find_appendix_file(latex_dir: Path, appendix: int, section: int) -> Path | None:
    """Find appendix or section within appendix."""
    backmatter = latex_dir / "300-backmatter"

    if not backmatter.exists():
        return None

    # Find appendix directory
    app_pattern = f"app{appendix:02d}-*"
    app_dirs = list(backmatter.glob(app_pattern))
    if not app_dirs:
        return None
    app_dir = app_dirs[0]

    if section == 0:
        # Target is the appendix itself - find aggregator
        app_name = app_dir.name
        app_file = app_dir / f"{app_name}.tex"
        return app_file if app_file.exists() else None

    # Find section file within appendix
    sec_pattern = f"sec{section:02d}-*.tex"
    sec_files = list(app_dir.glob(sec_pattern))
    if not sec_files:
        return None

    return sec_files[0]


def find_bodymatter_file(latex_dir: Path, part: int, chapter: int, section: int) -> Path | None:
    """Find tex file in bodymatter by numeric indices."""
    bodymatter = latex_dir / "200-bodymatter"

    if not bodymatter.exists():
        return None

    if part == 0:
        # No part structure - search directly in bodymatter
        search_base = bodymatter
    else:
        # Find part directory
        part_pattern = f"part{part:02d}-*"
        part_dirs = list(bodymatter.glob(part_pattern))
        if not part_dirs:
            return None
        search_base = part_dirs[0]

        if chapter == 0:
            # Target is a part - find part aggregator
            part_file = search_base / f"part{part:02d}.tex"
            return part_file if part_file.exists() else None

    # Find chapter directory
    ch_pattern = f"ch{chapter:02d}-*"
    ch_dirs = list(search_base.glob(ch_pattern))
    if not ch_dirs:
        # Try roman numerals for intro chapters
        roman_map = {1: 'i', 2: 'ii', 3: 'iii', 4: 'iv', 5: 'v', 6: 'vi', 7: 'vii', 8: 'viii', 9: 'ix', 10: 'x'}
        if chapter in roman_map:
            ch_pattern = f"ch{roman_map[chapter]}-*"
            ch_dirs = list(search_base.glob(ch_pattern))
    if not ch_dirs:
        return None
    ch_dir = ch_dirs[0]

    if section == 0:
        # Target is a chapter - find chapter aggregator
        ch_name = ch_dir.name
        ch_file = ch_dir / f"{ch_name}.tex"
        return ch_file if ch_file.exists() else None

    # Find section file
    sec_pattern = f"sec{section:02d}-*.tex"
    sec_files = list(ch_dir.glob(sec_pattern))
    if not sec_files:
        return None

    return sec_files[0]


def path_to_numeric_index(path: Path, latex_dir: Path) -> str | None:
    """Convert a file path to numeric dot notation."""
    try:
        rel = path.relative_to(latex_dir)
    except ValueError:
        return None

    parts = rel.parts

    # Check if in backmatter (appendix)
    if "300-backmatter" in parts:
        app_num = 0
        sec_num = 0
        for p in parts:
            if p.startswith("app"):
                match = re.match(r'app(\d+)', p)
                if match:
                    app_num = int(match.group(1))
            elif p.startswith("sec"):
                match = re.match(r'sec(\d+)', p)
                if match:
                    sec_num = int(match.group(1))
        if sec_num:
            return f"A.{app_num}.{sec_num}"
        elif app_num:
            return f"A.{app_num}"
        return None

    # Bodymatter
    part_num = 0
    ch_num = 0
    sec_num = 0

    for p in parts:
        if p.startswith("part"):
            match = re.match(r'part(\d+)', p)
            if match:
                part_num = int(match.group(1))
        elif p.startswith("ch"):
            match = re.match(r'ch(\d+)', p)
            if match:
                ch_num = int(match.group(1))
            else:
                # Roman numeral
                roman_map = {'i': 1, 'ii': 2, 'iii': 3, 'iv': 4, 'v': 5, 'vi': 6, 'vii': 7, 'viii': 8, 'ix': 9, 'x': 10}
                match = re.match(r'ch([ivx]+)', p)
                if match:
                    ch_num = roman_map.get(match.group(1), 0)
        elif p.startswith("sec"):
            match = re.match(r'sec(\d+)', p)
            if match:
                sec_num = int(match.group(1))

    # Build notation, omitting trailing zeros
    if sec_num:
        return f"{part_num}.{ch_num}.{sec_num}"
    elif ch_num:
        return f"{part_num}.{ch_num}"
    elif part_num:
        return str(part_num)
    return None


def find_tex_file(latex_dir: Path, name: str) -> Path | None:
    """Find a .tex file by name, slug, or numeric index.

    Supports:
    - Numeric index: "3.5.13" (part 3, chapter 5, section 13)
    - Appendix: "A.1" or "A.2.5" (appendix in backmatter)
    - Simple names: "main", "ch01", "sec02"
    - Slug matching: "ettersporselprognoser"

    Raises:
        AmbiguousTargetError: If multiple files match and no numeric index is provided
    """
    # Exclude localsettings.tex as it's not a standalone file
    if name == "localsettings":
        return None

    # Try numeric notation first
    numeric = parse_numeric_target(name)
    if numeric:
        area, num1, num2, num3 = numeric
        result = find_by_numeric_index(latex_dir, area, num1, num2, num3)
        if result:
            return result
        # Fall through to slug matching if numeric fails

    # Existing logic: exact match, then prefix match
    matches = list(latex_dir.rglob(f"{name}.tex"))
    if not matches:
        matches = list(latex_dir.rglob(f"{name}-*.tex"))

    if len(matches) == 0:
        return None
    elif len(matches) == 1:
        return matches[0]
    else:
        # Multiple matches - raise error with suggestions
        raise AmbiguousTargetError(name, matches, latex_dir)


def run_compile(tex_file: Path, latex_dir: Path, bib: bool = False, echo=print, success_style=None, error_style=None) -> int:
    """
    Compile a LaTeX file using pdflatex.

    Args:
        tex_file: Path to the .tex file
        latex_dir: Path to the latex directory
        bib: If True, run biber for bibliography processing
        echo: Function for normal output (print or click.echo)
        success_style: Function for success messages (optional, e.g., click.secho with fg="green")
        error_style: Function for error messages (optional, e.g., click.secho with fg="red")
    """
    # Default styled output to regular echo if not provided
    if success_style is None:
        success_style = echo
    if error_style is None:
        error_style = echo

    build_dir = latex_dir / "build"
    build_dir.mkdir(exist_ok=True)

    # Calculate relative path from latex_dir to tex_file (for display)
    rel_path = tex_file.relative_to(latex_dir)

    # For subfiles to work, we must compile from the file's directory
    # so that relative paths like ../../../main.tex resolve correctly
    file_dir = tex_file.parent
    file_name = tex_file.name

    echo(f"Compiling: {rel_path}")
    echo(f"Working directory: {file_dir.relative_to(latex_dir) if file_dir != latex_dir else '.'}")
    echo(f"Output directory: {build_dir}")
    echo("-" * 50)

    # Run pdflatex from the file's directory with absolute output path
    cmd = [
        "pdflatex",
        "-interaction=nonstopmode",
        f"-output-directory={build_dir}",
        file_name
    ]

    result = subprocess.run(
        cmd,
        cwd=file_dir,
        capture_output=False
    )

    # Run biber for bibliography if requested
    if bib and result.returncode == 0:
        aux_name = tex_file.stem
        biber_cmd = ["biber", f"--output-directory={build_dir}", aux_name]
        echo("-" * 50)
        echo("Running biber for bibliography...")
        biber_result = subprocess.run(biber_cmd, cwd=file_dir, capture_output=False)

        if biber_result.returncode == 0:
            # Run pdflatex two more times to resolve references
            for i in range(2):
                echo("-" * 50)
                echo(f"Running pdflatex (pass {i + 2})...")
                result = subprocess.run(cmd, cwd=file_dir, capture_output=False)
                if result.returncode != 0:
                    break
        else:
            result = biber_result

    if result.returncode == 0:
        pdf_name = tex_file.stem + ".pdf"
        echo("-" * 50)
        success_style(f"Success! Output: {build_dir / pdf_name}")
    else:
        echo("-" * 50)
        error_style(f"Compilation failed with return code {result.returncode}")

    return result.returncode


def main():
    """Standalone entry point."""
    cwd = Path.cwd()
    latex_dir = cwd / "latex"

    if not latex_dir.exists():
        print(f"Error: latex directory not found at {latex_dir}")
        print("Make sure you run this command from the project root.")
        sys.exit(1)

    # Get filename from arguments (default: main)
    name = sys.argv[1] if len(sys.argv) > 1 else "main"

    # Check for excluded file
    if name == "localsettings":
        print("Error: localsettings.tex is not a standalone file and cannot be compiled.")
        sys.exit(1)

    # Find the tex file
    try:
        tex_file = find_tex_file(latex_dir, name)
    except AmbiguousTargetError as e:
        print(f"Error: '{e.target}' matches multiple files:")
        for i, match in enumerate(e.matches, 1):
            rel_path = match.relative_to(latex_dir)
            print(f"  {i}. {rel_path}")
        if e.suggestions:
            print()
            print("Use numeric notation to specify which one:")
            for suggestion, path in e.suggestions:
                rel_path = path.relative_to(latex_dir)
                print(f"  uv run compile_latex.py {suggestion}  # {rel_path}")
        sys.exit(1)

    if tex_file is None:
        print(f"Error: Could not find {name}.tex in {latex_dir}")
        sys.exit(1)

    # Compile
    return_code = run_compile(tex_file, latex_dir)
    sys.exit(return_code)


if __name__ == "__main__":
    main()
