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

NB: The user should be able to not answer some of the variables.

Create a table under the heading "Book metadata" in SKILL.md (this file) with the following information:

| Key              | Value |
| ---------------- | ----- |
| Book title       |       |
| Book subtitle    |       |
| Book description |       |
| Book authors     |       |
| Book year        |       |
| Book edition     |       |

| Book publisher | |
| Book city | |
| Book state | |
| Book zip | |
| Book country | |
| Book language | |
| Book type | |
| Book theme | |

#### Step 3: Initialize the book

Run the following command to initialize the book with the following arguments (skip the ones the user skipped in step 2):

- --title `<Book title>`
- --subtitle `<Book subtitle>`
- --description `<Book description>`
- --author <Book author(s)>
- --year `<Book year>`
- --edition `<Book edition>`
- --publisher `<Book publisher>`
- --city `<Book city>`
- --state `<Book state>`
- --zip `<Book zip>`
- --country `<Book country>`
- --language `<Book language>`
- --type `<Book type>`
- --theme `<Book theme>`

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

#### Step 6: Quit the workflow

Give the user a message that the book has been initialized and compiled successfully.
Then exit the request and tell the user that they can now start writing the book.

## Book metadata

## Workflow

For the given prompt:

1. Read necessary background files (if not already read)
   1. @docs/book-structure-guide.md to learn about the general bookstructure
   2. @latex/latex-code-style.md to learn about the preferred Latex code style
2. Locate which tex files to change
   1. Locate which chapter the change belongs to, for instance ch02, or by the `<title>` of the chapter.
   2. Locate which section of this chapter the change belongs to, for instance sec04, or by the `<title>` of the section
3. 
4. Make the changes following best practice for latex
5. When DONE

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
| Compile appendix   | `book compile app01` |                                                                    |
| Outline structure  | `book outline`       | generates latex/ tree to outline.md                                |

**Examples:**

```bash
book compile              # Compile main.tex (full book)
book compile ch01         # Compile ch01-ettersporselprognoser.tex
book compile chii         # Compile chii-arbeidsflyt-og-ki.tex
book compile sec01        # Compile first matching sec01-*.tex
```

### Target Notation

Use numeric dot notation for precise targeting when files have duplicate indices across parts/chapters.

**Bodymatter:** `x.x.x` (part.chapter.section)

| Notation   | Meaning                | Example Path                         |
| ---------- | ---------------------- | ------------------------------------ |
| `3`      | Part 3                 | part03-name/part03.tex               |
| `3.5`    | Part 3, Chapter 5      | part03-name/ch05-name/ch05-name.tex  |
| `3.5.13` | Part 3, Ch 5, Sec 13   | part03-name/ch05-name/sec13-name.tex |
| `0.5`    | Chapter 5 (no part)    | ch05-name/ch05-name.tex              |
| `0.5.13` | Ch 5, Sec 13 (no part) | ch05-name/sec13-name.tex             |

**Backmatter (Appendices):** `A.x.x` (appendix.section)

| Notation  | Meaning           | Example Path                             |
| --------- | ----------------- | ---------------------------------------- |
| `A.1`   | Appendix 1        | 300-backmatter/app01-name/app01-name.tex |
| `A.2.5` | Appendix 2, Sec 5 | 300-backmatter/app02-name/sec05-name.tex |

**Examples:**

```bash
book compile 3.5.13    # Part 03, Chapter 05, Section 13
book compile 3.5       # Part 03, Chapter 05
book compile 3         # Part 03
book compile 0.5.13    # Chapter 05, Section 13 (no part structure)
book compile 0.5       # Chapter 05 (no part structure)
book compile A.1       # Appendix 01
book compile A.2.5     # Appendix 02, Section 05
book compile main      # Still works (slug match)
```

Slug-based matching still works: `book compile main`, `book compile ettersporselprognoser`

When ambiguous targets are detected, the CLI will suggest numeric notation alternatives.

### Image Commands

Generate and edit images using AI (requires GEMINI_API_KEY in .env).

Read @.claude\skills\book-latex\docs\images\image-prompts.md to learn about how to make the "prompt":

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

For structural operations, load the corresponding command file from `commands/`:

| Command         | Description                      | File                          |
| --------------- | -------------------------------- | ----------------------------- |
| New Part        | Append a new part at the end     | @/commands/new-part.md        |
| Insert Part     | Insert part at specific position | @/commands/insert-part.md     |
| Rename Part     | Change part slug/title           | @/commands/rename-part.md     |
| Delete Part     | Remove part and contents         | @/commands/delete-part.md     |
| Swap Parts      | Exchange two parts               | @/commands/swap-part.md       |
| New Chapter     | Append chapter to a part         | @/commands/new-chapter.md     |
| Insert Chapter  | Insert chapter at position       | @/commands/insert-chapter.md  |
| Rename Chapter  | Change chapter slug/title        | @/commands/rename-chapter.md  |
| Delete Chapter  | Remove chapter and contents      | @/commands/delete-chapter.md  |
| Move Chapter    | Move chapter between parts       | @/commands/move-chapter.md    |
| Swap Chapters   | Exchange two chapters            | @/commands/swap-chapters.md   |
| New Section     | Append section to a chapter      | @/commands/new-section.md     |
| Insert Section  | Insert section at position       | @/commands/insert-section.md  |
| Rename Section  | Change section slug/title        | @/commands/rename-section.md  |
| Delete Section  | Remove section                   | @/commands/delete-section.md  |
| Move Section    | Move section between chapters    | @/commands/move-section.md    |
| Swap Sections   | Exchange two sections            | @/commands/swap-sections.md   |
| New Appendix    | Append new appendix              | @/commands/new-appendix.md    |
| Insert Appendix | Insert appendix at position      | @/commands/insert-appendix.md |
| Rename Appendix | Change appendix slug/title       | @/commands/rename-appendix.md |
| Delete Appendix | Remove appendix                  | @/commands/delete-appendix.md |

Each command file contains the complete workflow including LaTeX-specific implementation details.

## Missing Arguments Rule

**Always use `AskUserQuestion`** when required information is missing:

- **Part/Chapter/Section/Appendix operations**: Ask for slug and title if not provided
- **Insert operations**: Ask for position if not specified
- **Move operations**: Ask for target location if not provided
