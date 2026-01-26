# New Part

Appends a new part at the end of bodymatter.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `slug` | URL-friendly name (e.g., "advanced-topics") | Yes |
| `title` | Display title (e.g., "Advanced Topics") | Yes |

## Workflow

1. **Find existing parts** - Count parts in `latex/200-bodymatter/`
2. **Calculate next number** - Use next available part number (01, 02, etc.)
3. **Create files** - Part folder and aggregator file
4. **Update aggregator** - Add entry to bodymatter aggregator

## LaTeX Implementation

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

Add to `latex/200-bodymatter/bodymatter.tex` at the end:

```latex
% ============ DEL <N>: <TITLE UPPERCASE> ============
\part{<Title>}
\setcounter{chapter}{0}
\renewcommand{\thechapter}{\arabic{chapter}}
\subfile{part<NN>-<slug>/part<NN>.tex}
```

## Path Reference

| Location | documentclass path |
|----------|-------------------|
| `200-bodymatter/partNN-*/partNN.tex` | `../../main.tex` |
