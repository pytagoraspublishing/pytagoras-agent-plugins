# Insert Appendix

Inserts a new appendix BEFORE the specified position, renumbering subsequent appendices.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `position` | Position to insert BEFORE (e.g., "appendix 2", "app02") | Yes |
| `slug` | URL-friendly name | Yes |
| `title` | Display title | Yes |

## Workflow

1. **Identify appendices to renumber** - All appendices from position onwards
2. **Rename in reverse order** - Highest number first to avoid conflicts
3. **Create new appendix** - At the insertion position
4. **Update aggregator** - Update all paths in backmatter aggregator

## LaTeX Implementation

### Renumbering Steps

For each appendix from highest to insertion point (in reverse order):

1. **Rename folder:**
   ```
   app<NN>-<slug>/ -> app<NN+1>-<slug>/
   ```

2. **Rename appendix file:**
   ```
   app<NN>-<slug>.tex -> app<NN+1>-<slug>.tex
   ```

3. **documentclass path stays the same** (`../../main.tex`)

### Files to Create

#### 1. Appendix Folder
```
latex/300-backmatter/app<NN>-<slug>/
```

#### 2. Appendix File
`app<NN>-<slug>/app<NN>-<slug>.tex`

```latex
\documentclass[../../main.tex]{subfiles}
\graphicspath{{\subfix{./figures/}}}
\begin{document}

\chapter{<Appendix Title>}
\label{app:<slug>}

% Appendix content

\end{document}
```

#### 3. Figures Folder (optional)
```
latex/300-backmatter/app<NN>-<slug>/figures/
```

### Backmatter Aggregator Update

In `latex/300-backmatter/backmatter.tex`:

1. Update all `\subfile{app<NN>-...}` paths for renumbered appendices
2. Insert new entry at correct position

### Example

Before:
```latex
\subfile{app01-formulas/app01-formulas.tex}
\subfile{app02-glossary/app02-glossary.tex}
```

Insert appendix 2 -> after renumbering:
```latex
\subfile{app01-formulas/app01-formulas.tex}
\subfile{app02-tables/app02-tables.tex}           % NEW
\subfile{app03-glossary/app03-glossary.tex}       % was app02
```

## Important Notes

- Rename from highest to lowest to avoid file conflicts
