# Insert Part

Inserts a new part BEFORE the specified position, renumbering subsequent parts.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `position` | Position to insert BEFORE (e.g., "part 2", "part02") | Yes |
| `slug` | URL-friendly name (e.g., "fundamentals") | Yes |
| `title` | Display title (e.g., "Fundamentals") | Yes |

## Workflow

1. **Identify parts to renumber** - All parts from position onwards
2. **Rename in reverse order** - Highest number first to avoid conflicts
3. **Create new part** - At the insertion position
4. **Update aggregator** - Update all paths in bodymatter aggregator

## LaTeX Implementation

### Renumbering Steps

For each part from highest to insertion point (in reverse order):

1. **Rename folder:**
   ```
   part<NN>-<slug>/ -> part<NN+1>-<slug>/
   ```

2. **Rename aggregator file:**
   ```
   part<NN>.tex -> part<NN+1>.tex
   ```

3. **documentclass path stays the same** (`../../main.tex`)

### Files to Create

#### 1. Folder
```
latex/200-bodymatter/part<NN>-<slug>/
```

#### 2. Part Aggregator
`latex/200-bodymatter/part<NN>-<slug>/part<NN>.tex`

```latex
\documentclass[../../main.tex]{subfiles}
\begin{document}

% Add chapters here using \subfile{chXX-name/chXX-name.tex}

\end{document}
```

### Aggregator Update

In `latex/200-bodymatter/bodymatter.tex`:

1. Update all `\subfile{part<NN>-...}` paths for renumbered parts
2. Insert new entry at correct position:
```latex
% ============ DEL <N>: <TITLE UPPERCASE> ============
\part{<Title>}
\setcounter{chapter}{0}
\renewcommand{\thechapter}{\arabic{chapter}}
\subfile{part<NN>-<slug>/part<NN>.tex}
```

## Important Notes

- Rename from highest to lowest to avoid file conflicts
- Chapter files inside parts do NOT need path updates - they reference `../../main.tex` (relative to main, not to part folder name)
