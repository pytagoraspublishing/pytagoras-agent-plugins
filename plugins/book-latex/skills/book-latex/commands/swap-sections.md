# Swap Sections

Exchanges the positions of two sections within a chapter.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `part` | Part containing the chapter | Yes (if ambiguous) |
| `chapter` | Chapter containing the sections | Yes |
| `section1` | First section identifier | Yes |
| `section2` | Second section identifier | Yes |

## Workflow

1. **Locate both sections** - Find by number or slug
2. **Temporary rename** - Use `.tmp` suffix to avoid conflicts
3. **Swap files** - Exchange numbers
4. **Update labels** - If they include numbers
5. **Update aggregator** - Reorder entries in chapter file

## LaTeX Implementation

### 1. Use Temporary Names to Avoid Conflicts

```
sec02-<slug-a>.tex -> sec02-<slug-a>.tex.tmp
sec05-<slug-b>.tex -> sec02-<slug-b>.tex
sec02-<slug-a>.tex.tmp -> sec05-<slug-a>.tex
```

### 2. Update Labels (if using numeric labels)

Usually labels use slugs, so no update needed:
```latex
\label{sec:<chapter>:<slug>}  % stays the same
```

### 3. Update Chapter Aggregator

Reorder `\subfile{}` lines to match new numeric order:

```latex
% Before
\subfile{sec02-<slug-a>.tex}
...
\subfile{sec05-<slug-b>.tex}

% After
\subfile{sec02-<slug-b>.tex}
...
\subfile{sec05-<slug-a>.tex}
```

## Important Notes

- The `\documentclass` path stays the same (`../../../main.tex`)
- The `\graphicspath` stays the same (`\subfix{../figures/}`)
- No renumbering of other sections is required (items exchange positions)
