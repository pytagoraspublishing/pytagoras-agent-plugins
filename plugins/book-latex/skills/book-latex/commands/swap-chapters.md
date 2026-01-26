# Swap Chapters

Exchanges the positions of two chapters.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `part` | Part containing the chapters | Yes (if ambiguous) |
| `chapter1` | First chapter identifier | Yes |
| `chapter2` | Second chapter identifier | Yes |

## Workflow

1. **Locate both chapters** - Find by number or slug
2. **Temporary rename** - Use `.tmp` suffix to avoid conflicts
3. **Swap folders and files** - Exchange numbers
4. **Update labels** - If they include numbers
5. **Update aggregator** - Reorder entries in part aggregator
6. **Compile the whole book**: `book compile` if any compilation error:
   1. Understand and locate the error
   2. Make changes to fix the error
   3. Recompile the book
   4. Repeat until the error is fixed
7. **Check cross-references** - Search the compilation log to see if there are any broken cross-references due to this change

## LaTeX Implementation

### 1. Use Temporary Names to Avoid Conflicts

```
ch02-<slug-a>/ -> ch02-<slug-a>.tmp/
ch05-<slug-b>/ -> ch02-<slug-b>/
ch02-<slug-a>.tmp/ -> ch05-<slug-a>/
```

### 2. Rename Chapter Files

```
ch02-<slug-a>.tex -> ch05-<slug-a>.tex
ch05-<slug-b>.tex -> ch02-<slug-b>.tex
```

### 3. Update Labels (if using numeric labels)

Usually labels use slugs, so no update needed:
```latex
\label{ch:<slug>}  % stays the same
```

### 4. Update Part Aggregator

Reorder `\subfile{}` lines to match new numeric order:

```latex
% Before
\subfile{ch02-<slug-a>/ch02-<slug-a>.tex}
...
\subfile{ch05-<slug-b>/ch05-<slug-b>.tex}

% After
\subfile{ch02-<slug-b>/ch02-<slug-b>.tex}
...
\subfile{ch05-<slug-a>/ch05-<slug-a>.tex}
```

## Important Notes

- The `\documentclass` path stays the same (`../../../main.tex`)
- Section files inside chapters do NOT need updates
- No renumbering of other chapters is required (items exchange positions)
