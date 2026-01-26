# New Section

Appends a new section at the end of a chapter.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `part` | Part containing the chapter | Yes (if ambiguous) |
| `chapter` | Target chapter | Yes |
| `slug` | URL-friendly name (e.g., "methodology") | Yes |
| `title` | Display title (e.g., "Methodology") | Yes |

## Workflow

1. **Locate chapter** - Find target chapter folder
2. **Find existing sections** - Count sections in chapter
3. **Calculate next number** - Use next available section number (sec01, sec02, etc.)
4. **Create file** - Section file in chapter folder
5. **Update aggregator** - Add entry to chapter file

## LaTeX Implementation

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

Add to `ch<XX>-<chapter-slug>.tex` before `\ifSubfilesClassLoaded`:

```latex
\subfile{sec<NN>-<section-slug>.tex}
```

## Path Reference

| Location | documentclass path | graphicspath |
|----------|-------------------|--------------|
| Section file | `../../../main.tex` | `\subfix{../figures/}` |

## Label Convention

`sec:<chapter-slug>:<section-slug>`

Example: `sec:transport-optimization:methodology`
