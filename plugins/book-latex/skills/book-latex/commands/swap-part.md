# Swap Parts

Exchanges the positions of two parts.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `part1` | First part identifier | Yes |
| `part2` | Second part identifier | Yes |

## Workflow

1. **Locate both parts** - Find by number or slug
2. **Temporary rename** - Use `.tmp` suffix to avoid conflicts
3. **Swap folders and files** - Exchange numbers
4. **Update aggregator** - Reorder entries in bodymatter.tex
5. **Compile the whole book**: `book compile` if any compilation error:
   1. Understand and locate the error
   2. Make changes to fix the error
   3. Recompile the book
   4. Repeat until the error is fixed
6. **Check cross-references** - Search the compilation log to see if there are any broken cross-references due to this change

## LaTeX Implementation

### 1. Use Temporary Names to Avoid Conflicts

```
part02-<slug-a>/ -> part02-<slug-a>.tmp/
part05-<slug-b>/ -> part02-<slug-b>/
part02-<slug-a>.tmp/ -> part05-<slug-a>/
```

### 2. Rename Part Aggregator Files

```
part02.tex -> part05.tex
part05.tex -> part02.tex
```

### 3. Update bodymatter.tex

Reorder `\subfile{}` lines and `\part{}` declarations to match new numeric order:

```latex
% Before
\part{Title A}
\subfile{part02-<slug-a>/part02.tex}
...
\part{Title B}
\subfile{part05-<slug-b>/part05.tex}

% After
\part{Title B}
\subfile{part02-<slug-b>/part02.tex}
...
\part{Title A}
\subfile{part05-<slug-a>/part05.tex}
```

## Important Notes

- The `\documentclass` path stays the same (`../../main.tex` for parts)
- Chapter files inside parts do NOT need updates
- No renumbering of other parts is required (items exchange positions)
