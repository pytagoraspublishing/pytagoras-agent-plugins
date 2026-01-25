---
name: book
description: Manage book projects - create/edit parts, chapters, sections. Use when user wants to add, rename, delete, or reorganize book structure elements. Triggers on "new chapter", "add section", "rename part", "delete appendix", "move chapter".
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, AskUserQuestion
---
# Book Latex Skill

## Purpose

Write structured book projects with parts, chapters, sections, and appendices with the Latex typewriting langauge.

## Initialize Project

If you are reading this section, it means that the book yes YET NOT initiated and you need to run the initialization workflow:

### Workflow

#### Step 1: Install the book CLI

##### Prerequisites

Check if the user has uv installed, if not, install it:

Install [uv](https://docs.astral.sh/uv/) (Python package manager):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

##### Installation command

Run the following command to install the book CLI:

```bash
uv tool install .claude/skills/book-latex/cli/windows/
```

make sure the installation is successful by running the following command:
```bash
book --help
```

if the command is not found, try running the following command:
```bash
uv tool install .claude/skills/book-latex/cli/windows/
```

#### Step 2: Initialize the book

Ask the user for the follwing information with the AskUserQuestion tool:
- Book title
- Book subtitle
- Book description
- Book authors
- Book year
- Book edition
- Book publisher
- Book city
- Book state
- Book zip
- Book country
- Book language
- Book type
- Book theme

Create a table under the heading "Book metadata" with the following information:
| Key | Value |
| --- | --- |
| Book title | |
| Book subtitle | |
| Book description | |
| Book authors | |
| Book year | |
| Book edition | |

| Book publisher | |
| Book city | |
| Book state | |
| Book zip | |
| Book country | |
| Book language | |
| Book type | |
| Book theme | |

#### Step 3: Initialize the book

Run the following command to initialize the book with the following arguments:
- --title <Book title>
- --subtitle <Book subtitle>
- --description <Book description>
- --author <Book author(s)>
- --year <Book year>
- --edition <Book edition>
- --publisher <Book publisher>
- --city <Book city>
- --state <Book state>
- --zip <Book zip>
- --country <Book country>
- --language <Book language>
- --type <Book type>
- --theme <Book theme>

```bash
book init --title <Book title> --subtitle <Book subtitle> --description <Book description> --author <Book authors> --year <Book year> --edition <Book edition> --publisher <Book publisher> --city <Book city> --state <Book state> --zip <Book zip> --country <Book country> --language <Book language> --type <Book type> --theme <Book theme>
```

#### Step 4: Compile the book

Run the following command to compile the book:
```bash
book compile --bib
```

#### Step 5: Remove the `Initialize project` section from the SKILL.md file

Remove the `Initialize project` section from the SKILL.md file (this file and this section).





## Book metadata



## Workflow

1. Read the user prompt with this



## CLI Commands

There are TWO types of commands the user can call for these commands:

1. book CLI commands - the book CLI is a python click application that is already installed and ready to use
2. structure commands - strucutral commands where you change the outline of the book and where you execute a workflow instead of running a CLI command

### Compile Commands

All commands must be run from the **project root directory**.

| Task               | CLI                    | Description                                                        |
| ------------------ | ---------------------- | ------------------------------------------------------------------ |
| Compile full book  | `book compile`       | compiles the entire book, that is, compiles main.tex               |
| Compile chapter 1  | `book compile ch01`  | compiles the chapter ch01, that is, compiles the ch01.tex file     |
| Compile chapter ii | `book compile chii`  | in general, chapter can be indexed differently, with patterns chXX |
| Compile section 01 | `book compile sec01` | compiles the chapter sec01, that is, compiles the sec01.tex file   |
| Compile appendix   | `book compile sec01` |                                                                    |

**Examples:**

```bash
book compile              # Compile main.tex (full book)
book compile ch01         # Compile ch01-ettersporselprognoser.tex
book compile chii         # Compile chii-arbeidsflyt-og-ki.tex
book compile sec01        # Compile first matching sec01-*.tex
```

### Image Commands

Generate and edit images using AI (requires GEMINI_API_KEY in .env):

| Task           | CLI (after install)                            | Standalone (no install)                                           |
| -------------- | ---------------------------------------------- | ----------------------------------------------------------------- |
| Generate image | `book image new --path "path.png" "prompt"`  | generates a new image according to prompt, and saves it to --path |
| Edit image     | `book image edit --path "path.png" "prompt"` | edits an existing image at --path and overwrites it               |

**Examples:**

```bash
book image new --path "figures/flowchart.png" "A process diagram showing order fulfillment"
book image new -p "charts/sales.png" -r 4K "Bar chart comparing Q1-Q4 sales"
book image edit --path "figures/logo.png" "Change background to blue"
```

**Resolution options:** 1K (default), 2K, 4K

**Note:** `edit` overwrites the original image file.

## Structure Commands

For structural operations, load the command file from `commands/`:

| Operation          | Command File                                                                                                                       |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Part**     | `new-part.md`, `insert-part.md`, `rename-part.md`, `delete-part.md`                                                        |
| **Chapter**  | `new-chapter.md`, `insert-chapter.md`, `rename-chapter.md`, `delete-chapter.md`, `move-chapter.md`, `swap-chapters.md` |
| **Section**  | `new-section.md`, `insert-section.md`, `rename-section.md`, `delete-section.md`, `move-section.md`, `swap-sections.md` |
| **Appendix** | `new-appendix.md`, `insert-appendix.md`, `rename-appendix.md`, `delete-appendix.md`                                        |

Each command file specifies:

1. Required information to gather
2. Type-agnostic workflow steps
3. Reference to type-specific implementation in `commands/<type>/`

## Missing Arguments Rule

**Always use `AskUserQuestion`** when required information is missing:

- **Part/Chapter/Section/Appendix operations**: Ask for slug and title if not provided
- **Insert operations**: Ask for position if not specified
- **Move operations**: Ask for target location if not provided

## Reference Documents

- `templates/structure.md` - Folder/file naming conventions
- `filetypes/<type>.md` - Type-specific templates and patterns
- `docs/` - Additional reference documentation
