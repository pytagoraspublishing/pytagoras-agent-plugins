# Move Section

Moves a section from one chapter to another.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `source_part` | Part containing source chapter | Yes (if ambiguous) |
| `source_chapter` | Chapter containing the section | Yes |
| `section` | Section to move | Yes |
| `target_part` | Part containing target chapter | Yes (if ambiguous) |
| `target_chapter` | Destination chapter | Yes |

## Workflow

1. **Locate source section** - Find section in source chapter
2. **Determine target number** - Next available section number in target chapter
3. **Move file** - To target chapter with new number
4. **Update section content** - Update label to reference new chapter
5. **Update source aggregator** - Remove entry from source chapter
6. **Update target aggregator** - Add entry to target chapter
7. **Renumber affected sections** - In both source and target chapters
8. **Update cross-references** - Search project for old label references
9. **Compile the whole book**: `book compile` if any compilation error:
   1. Understand and locate the error
   2. Make changes to fix the error
   3. Recompile the book
   4. Repeat until the error is fixed
10. **Check cross-references** - Search the compilation log to see if there are any broken cross-references due to this change

## LaTeX Implementation

### 1. Determine Target Section Number

Find next available section number in target chapter.

### 2. Move File

```
latex/.../ch<SRC>-<src-chapter>/sec<OLD>-<slug>.tex
-> latex/.../ch<TGT>-<tgt-chapter>/sec<NEW>-<slug>.tex
```

### 3. Update Section File

Update label:
```latex
\label{sec:<src-chapter>:<slug>}
```
to:
```latex
\label{sec:<tgt-chapter>:<slug>}
```

The `\documentclass` path stays same if depth is same (`../../../main.tex`).

Update `\graphicspath` if moving between chapters:
```latex
\graphicspath{{\subfix{../figures/}}}
```
(stays same - relative to section file)

### 4. Update Source Chapter Aggregator

Remove from `ch<SRC>-<src-chapter>.tex`:
```latex
\subfile{sec<OLD>-<slug>.tex}
```

### 5. Update Target Chapter Aggregator

Add to `ch<TGT>-<tgt-chapter>.tex` before `\ifSubfilesClassLoaded`:
```latex
\subfile{sec<NEW>-<slug>.tex}
```

## Renumbering Affected Sections

### Source Chapter (after removal)
Renumber all subsequent sections DOWN to fill the gap:

**Example:** Moving sec02 from [sec01, sec02, sec03, sec04]:
1. sec03 → sec02
2. sec04 → sec03
3. Update aggregator paths

### Target Chapter (if inserting at position)
Renumber all subsequent sections UP to make room:

**Example:** Inserting at position 2 in [sec01, sec02, sec03]:
1. sec03 → sec04
2. sec02 → sec03
3. Insert moved section as sec02
4. Update aggregator paths

**Renaming Steps (for each section):**
1. Rename file: `sec<OLD>-<slug>.tex` → `sec<NEW>-<slug>.tex`
2. Update `\subfile{}` path in chapter aggregator

**Note:** Labels using slugs (`\label{sec:<chapter>:<slug>}`) do NOT need updating.

## Cross-Reference Updates

Search entire project and update:
- `\ref{sec:<src-chapter>:<slug>}` -> `\ref{sec:<tgt-chapter>:<slug>}`
