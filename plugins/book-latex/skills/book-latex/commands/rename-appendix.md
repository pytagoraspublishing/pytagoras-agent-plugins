# Rename Appendix

Changes the slug and/or title of an existing appendix.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `current` | Current appendix identifier (number or slug) | Yes |
| `new_slug` | New URL-friendly name (optional) | No |
| `new_title` | New display title (optional) | No |

At least one of `new_slug` or `new_title` must be provided.

## Workflow

1. **Locate appendix** - Find appendix by number or slug
2. **Rename folder and file** - If slug changes
3. **Update appendix content** - Label and title
4. **Update aggregator** - Update path in backmatter aggregator
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
app<NN>-<old-slug>/ -> app<NN>-<new-slug>/
```

### 2. Rename Appendix File
```
app<NN>-<old-slug>.tex -> app<NN>-<new-slug>.tex
```

### 3. Update Appendix File Content

Label:
```latex
\label{app:<old-slug>}
```
to:
```latex
\label{app:<new-slug>}
```

Title (if changed):
```latex
\chapter{<Old Title>}
```
to:
```latex
\chapter{<New Title>}
```

### 4. Update Backmatter Aggregator

In `backmatter.tex`:
```latex
\subfile{app<NN>-<old-slug>/app<NN>-<old-slug>.tex}
```
to:
```latex
\subfile{app<NN>-<new-slug>/app<NN>-<new-slug>.tex}
```

## Cross-Reference Updates

Search entire project and update:
- `\ref{app:<old-slug>}` -> `\ref{app:<new-slug>}`
- `\hyperref[app:<old-slug>]` -> `\hyperref[app:<new-slug>]`
