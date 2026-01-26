# New Chapter

Appends a new chapter at the end of a part.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `part` | Target part (e.g., "part02", "part 2") | Yes |
| `slug` | URL-friendly name (e.g., "transport-optimization") | Yes |
| `title` | Display title (e.g., "Transport Optimization") | Yes |

## Workflow

1. **Locate part** - Find target part folder
2. **Find existing chapters** - Count chapters in part
3. **Determine numbering scheme** - Part01 uses roman (chi, chii), Part02+ uses arabic (ch01, ch02)
4. **Calculate next number** - Use next available chapter number
5. **Create files** - Chapter folder, chapter file, figures folder
6. **Update aggregator** - Add entry to part aggregator
7. **Compile the whole book**: `book compile` if any compilation error:
   1. Understand and locate the error
   2. Make changes to fix the error
   3. Recompile the book
   4. Repeat until the error is fixed
8. **Check cross-references** - Search the compilation log to see if there are any broken cross-references due to this change

## LaTeX Implementation

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

Add to `part<NN>.tex`:

```latex
% Kapittel <N> - <Title>
\subfile{ch<XX>-<chapter-slug>/ch<XX>-<chapter-slug>.tex}
```

## Numbering Schemes

| Part | Prefix | Examples |
|------|--------|----------|
| part01 | `ch<roman>` | chi, chii, chiii, chiv, chv |
| part02+ | `ch<NN>` | ch01, ch02, ch10, ch11 |

## Path Reference

| Location | documentclass path |
|----------|-------------------|
| Chapter file | `../../../main.tex` |
