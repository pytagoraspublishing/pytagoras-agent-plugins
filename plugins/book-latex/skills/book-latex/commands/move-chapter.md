# Move Chapter

Moves a chapter from one part to another.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `source_part` | Part containing the chapter | Yes |
| `chapter` | Chapter to move | Yes |
| `target_part` | Destination part | Yes |
| `position` | Position in target (optional, defaults to end) | No |

## Workflow

1. **Locate source chapter** - Find chapter in source part
2. **Determine target number** - Next available or specified position
3. **Handle numbering scheme change** - Roman to arabic or vice versa if crossing part types
4. **Move folder** - To target part with new number
5. **Rename files** - If numbering scheme changes
6. **Update source aggregator** - Remove entry
7. **Update target aggregator** - Add entry
8. **Renumber affected chapters** - In both source and target parts
9. **Compile the whole book**: `book compile` if any compilation error:
   1. Understand and locate the error
   2. Make changes to fix the error
   3. Recompile the book
   4. Repeat until the error is fixed
10. **Check cross-references** - Search the compilation log to see if there are any broken cross-references due to this change

## LaTeX Implementation

### 1. Determine Target Numbering

| Source Part | Target Part | Action |
|-------------|-------------|--------|
| part01 (roman) | part02+ (arabic) | chi -> ch01 |
| part02+ (arabic) | part01 (roman) | ch01 -> chi |
| Same scheme | Same scheme | Keep or renumber |

### 2. Move Folder

```
latex/200-bodymatter/part<SRC>-<src-slug>/ch<OLD>-<chapter-slug>/
-> latex/200-bodymatter/part<TGT>-<tgt-slug>/ch<NEW>-<chapter-slug>/
```

### 3. Rename Files (if numbering scheme changes)

```
ch<OLD>-<chapter-slug>.tex -> ch<NEW>-<chapter-slug>.tex
```

### 4. Update Chapter File

`\documentclass` path stays same (`../../../main.tex`).

### 5. Update Source Part Aggregator

Remove from `part<SRC>.tex`:
```latex
\subfile{ch<OLD>-<chapter-slug>/ch<OLD>-<chapter-slug>.tex}
```

### 6. Update Target Part Aggregator

Add to `part<TGT>.tex`:
```latex
\subfile{ch<NEW>-<chapter-slug>/ch<NEW>-<chapter-slug>.tex}
```

## Renumbering Affected Chapters

### Source Part (after removal)
Renumber all subsequent chapters DOWN to fill the gap:

**Example:** Moving ch02 from [ch01, ch02, ch03, ch04]:
1. ch03 → ch02
2. ch04 → ch03
3. Update aggregator paths

### Target Part (if inserting at position)
Renumber all subsequent chapters UP to make room:

**Example:** Inserting at position 2 in [ch01, ch02, ch03]:
1. ch03 → ch04
2. ch02 → ch03
3. Insert moved chapter as ch02
4. Update aggregator paths

**Renaming Steps (for each chapter):**
1. Rename folder: `ch<OLD>-<slug>/` → `ch<NEW>-<slug>/`
2. Rename main file: `ch<OLD>-<slug>.tex` → `ch<NEW>-<slug>.tex`
3. Update `\subfile{}` path in part aggregator

**Note:** Labels using slugs (`\label{ch:<slug>}`) do NOT need updating.

## Path Reference

Chapter files always use `../../../main.tex` regardless of which part they're in.
