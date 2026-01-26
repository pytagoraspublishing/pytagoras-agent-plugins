# New Appendix

Appends a new appendix at the end of backmatter.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `slug` | URL-friendly name (e.g., "formulas") | Yes |
| `title` | Display title (e.g., "Mathematical Formulas") | Yes |

## Workflow

1. **Find existing appendices** - Count appendices in `latex/300-backmatter/`
2. **Calculate next number** - Use next available appendix number (app01, app02, etc.)
3. **Create files** - Appendix folder and file
4. **Update aggregator** - Add entry to backmatter aggregator

## LaTeX Implementation

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

Add to `latex/300-backmatter/backmatter.tex` after existing appendices:

```latex
\subfile{app<NN>-<slug>/app<NN>-<slug>.tex}
```

## Path Reference

| Location | documentclass path |
|----------|-------------------|
| `300-backmatter/appNN-*/appNN-*.tex` | `../../main.tex` |
