# Insert Section

Inserts a new section BEFORE the specified position, renumbering subsequent sections.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `part` | Part containing the chapter | Yes (if ambiguous) |
| `chapter` | Chapter containing the sections | Yes |
| `position` | Position to insert BEFORE (e.g., "section 3", "sec03") | Yes |
| `slug` | URL-friendly name | Yes |
| `title` | Display title | Yes |

## Workflow

1. **Locate chapter and section position** - Validate position exists
2. **Identify sections to renumber** - All sections from position onwards
3. **Rename in reverse order** - Highest number first to avoid conflicts
4. **Create new section** - At the insertion position
5. **Update aggregator** - Update all paths in chapter file

## LaTeX Implementation

### Renumbering Steps

For each section from highest to insertion point (in reverse order):

1. **Rename file:**
   ```
   sec<NN>-<slug>.tex -> sec<NN+1>-<slug>.tex
   ```

2. **Labels using slugs do NOT need updates:**
   ```latex
   \label{sec:<chapter>:<slug>}  % stays the same
   ```

### Files to Create

#### Section File
`ch<XX>-<chapter-slug>/sec<NN>-<section-slug>.tex`

```latex
\documentclass[../../../main.tex]{subfiles}
\graphicspath{{\subfix{../figures/}}}
\begin{document}

\section{<Section Title>}
\label{sec:<chapter-slug>:<section-slug>}

% Section content

\end{document}
```

### Chapter Aggregator Update

In `ch<XX>-<chapter-slug>.tex`:

1. Update all `\subfile{sec<NN>-...}` paths for renumbered sections
2. Insert new entry at correct position (before `\ifSubfilesClassLoaded`)

### Example

Before:
```latex
\subfile{sec01-intro.tex}
\subfile{sec02-methods.tex}
\subfile{sec03-results.tex}
```

Insert section 2 -> after renumbering:
```latex
\subfile{sec01-intro.tex}
\subfile{sec02-background.tex}      % NEW
\subfile{sec03-methods.tex}         % was sec02
\subfile{sec04-results.tex}         % was sec03
```

## Important Notes

- Rename from highest to lowest to avoid file conflicts
- Labels using slugs (not numbers) do NOT need updating
