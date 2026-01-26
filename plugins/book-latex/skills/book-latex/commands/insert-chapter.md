# Insert Chapter

Inserts a new chapter BEFORE the specified position, renumbering subsequent chapters.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `part` | Target part | Yes |
| `position` | Position to insert BEFORE (e.g., "chapter 2", "ch02", "chii") | Yes |
| `slug` | URL-friendly name | Yes |
| `title` | Display title | Yes |

## Workflow

1. **Locate part and chapter position** - Validate position exists
2. **Identify chapters to renumber** - All chapters from position onwards
3. **Rename in reverse order** - Highest number first to avoid conflicts
4. **Create new chapter** - At the insertion position
5. **Update aggregator** - Update all paths in part aggregator
6. **Compile the whole book**: `book compile` if any compilation error:
   1. Understand and locate the error
   2. Make changes to fix the error
   3. Recompile the book
   4. Repeat until the error is fixed
7. **Check cross-references** - Search the compilation log to see if there are any broken cross-references due to this change

## LaTeX Implementation

### Renumbering Steps

For each chapter from highest to insertion point (in reverse order):

1. **Rename folder:**
   ```
   ch<XX>-<slug>/ -> ch<XX+1>-<slug>/
   ```

2. **Rename chapter file:**
   ```
   ch<XX>-<slug>.tex -> ch<XX+1>-<slug>.tex
   ```

3. **Labels using slugs do NOT need updates:**
   ```latex
   \label{ch:<slug>}  % stays the same
   ```

4. **Section files do NOT need path updates** (same relative depth)

### Files to Create

#### 1. Chapter Folder
```
latex/200-bodymatter/part<NN>-<partslug>/ch<XX>-<chapter-slug>/
```

#### 2. Figures Folder
```
latex/200-bodymatter/part<NN>-<partslug>/ch<XX>-<chapter-slug>/figures/
```

#### 3. Chapter Aggregator
`ch<XX>-<chapter-slug>/ch<XX>-<chapter-slug>.tex`

```latex
\documentclass[../../../main.tex]{subfiles}
\graphicspath{{\subfix{./figures/}}}
\begin{document}

\chapter{<Chapter Title>}
\label{ch:<chapter-slug>}

% Chapter introduction

% Add sections here using \subfile{secNN-name.tex}

\ifSubfilesClassLoaded{%
  \printbibliography
}{}

\end{document}
```

### Part Aggregator Update

In `part<NN>.tex`:

1. Update all `\subfile{ch<XX>-...}` paths for renumbered chapters
2. Insert new entry at correct position:
```latex
% Kapittel <N> - <Title>
\subfile{ch<XX>-<chapter-slug>/ch<XX>-<chapter-slug>.tex}
```

## Important Notes

- Rename from highest to lowest to avoid file conflicts
- Labels using slugs (not numbers) do NOT need updating
- Cross-references using numeric labels may need updating

## Cross-Reference Check

If any labels use numeric prefixes, search and update:
- `\ref{ch:XX}` references
- `\hyperref[ch:XX]` references
