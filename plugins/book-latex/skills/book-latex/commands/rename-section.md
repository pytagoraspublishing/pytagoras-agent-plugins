# Rename Section

Changes the slug and/or title of an existing section.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `part` | Part containing the chapter | Yes (if ambiguous) |
| `chapter` | Chapter containing the section | Yes |
| `current` | Current section identifier (prefix or slug) | Yes |
| `new_slug` | New URL-friendly name (optional) | No |
| `new_title` | New display title (optional) | No |

At least one of `new_slug` or `new_title` must be provided.

## Workflow

1. **Locate section** - Find section by number or slug
2. **Rename file** - If slug changes
3. **Update section content** - Label and title
4. **Update aggregator** - Update path in chapter file
5. **Update cross-references** - Search project for old label references

## LaTeX Implementation

### 1. Rename File (if slug changes)
```
sec<NN>-<old-slug>.tex -> sec<NN>-<new-slug>.tex
```

### 2. Update Section File Content

Label:
```latex
\label{sec:<chapter>:<old-slug>}
```
to:
```latex
\label{sec:<chapter>:<new-slug>}
```

Title (if changed):
```latex
\section{<Old Title>}
```
to:
```latex
\section{<New Title>}
```

### 3. Update Chapter Aggregator

In `ch<XX>-<chapter-slug>.tex`:
```latex
\subfile{sec<NN>-<old-slug>.tex}
```
to:
```latex
\subfile{sec<NN>-<new-slug>.tex}
```

## Cross-Reference Updates

Search entire project and update:
- `\ref{sec:<chapter>:<old-slug>}` -> `\ref{sec:<chapter>:<new-slug>}`
- `\hyperref[sec:<chapter>:<old-slug>]` -> `\hyperref[sec:<chapter>:<new-slug>]`
