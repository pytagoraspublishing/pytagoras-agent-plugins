# Rename Chapter

Changes the slug and/or title of an existing chapter.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `part` | Part containing the chapter | Yes (if ambiguous) |
| `current` | Current chapter identifier (prefix or slug) | Yes |
| `new_slug` | New URL-friendly name (optional) | No |
| `new_title` | New display title (optional) | No |

At least one of `new_slug` or `new_title` must be provided.

## Workflow

1. **Locate chapter** - Find chapter by number or slug
2. **Rename folder and file** - If slug changes
3. **Update chapter content** - Label and title
4. **Update aggregator** - Update path in part aggregator
5. **Update cross-references** - Search project for old label references
6. **Compile the whole book**: `book compile` if any compilation error:
   1. Understand and locate the error
   2. Make changes to fix the error
   3. Recompile the book
   4. Repeat until the error is fixed
7. **Check cross-references** - Search the compilation log to see if there are any broken cross-references due to this change

## LaTeX Implementation

### 1. Rename Folder (if slug changes)
```
ch<XX>-<old-slug>/ -> ch<XX>-<new-slug>/
```

### 2. Rename Chapter File
```
ch<XX>-<old-slug>.tex -> ch<XX>-<new-slug>.tex
```

### 3. Update Chapter File Content

Label:
```latex
\label{ch:<old-slug>}
```
to:
```latex
\label{ch:<new-slug>}
```

Title (if changed):
```latex
\chapter{<Old Title>}
```
to:
```latex
\chapter{<New Title>}
```

### 4. Update Part Aggregator

In `part<NN>.tex`:
```latex
\subfile{ch<XX>-<old-slug>/ch<XX>-<old-slug>.tex}
```
to:
```latex
\subfile{ch<XX>-<new-slug>/ch<XX>-<new-slug>.tex}
```

## Cross-Reference Updates

Search entire project and update:
- `\ref{ch:<old-slug>}` -> `\ref{ch:<new-slug>}`
- `\hyperref[ch:<old-slug>]` -> `\hyperref[ch:<new-slug>]`

## Files NOT Needing Updates

- Section files (they use relative `\subfile{}` without folder path)
