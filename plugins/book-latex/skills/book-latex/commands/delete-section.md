# Delete Section

Removes a section file.

## Required Information

| Field       | Description                         | Ask if missing     |
| ----------- | ----------------------------------- | ------------------ |
| `part`    | Part containing the chapter         | Yes (if ambiguous) |
| `chapter` | Chapter containing the section      | Yes                |
| `section` | Section identifier (prefix or slug) | Yes                |

## Workflow

1. **Locate section** - Find section by number or slug
2. **Delete file** - Remove section file
3. **Update aggregator** - Remove entry from chapter file
4. **Renumber subsequent sections** - Maintain sequential order
5. **Compile the whole book**: `book compile` if any compilation error:
   1. Undestand and locate the error
   2. make changes to fix the error
   3. Recompile the book
   4. Repeat untill the error is fixed
6. **Check cross-references** - search the compilation log to see if there are any broken cross-references due to this change

## LaTeX Implementation

### Files to Delete

```
latex/200-bodymatter/part<NN>-<partslug>/ch<XX>-<chapter-slug>/sec<NN>-<slug>.tex
```

### Chapter Aggregator Update

In `ch<XX>-<chapter-slug>.tex`, remove:

```latex
\subfile{sec<NN>-<slug>.tex}
```

## Renumbering Subsequent Sections

After deletion, renumber all subsequent sections to maintain sequential order:

**Example:** Deleting sec02 from [sec01, sec02, sec03, sec04]:

1. sec03 → sec02 (rename file)
2. sec04 → sec03 (rename file)
3. Update aggregator file with new paths

**Renaming Steps (for each section, from lowest to highest):**

1. Rename file: `sec<OLD>-<slug>.tex` → `sec<NEW>-<slug>.tex`
2. Update `\subfile{}` path in chapter aggregator

**Note:** Labels using slugs (`\label{sec:<chapter>:<slug>}`) do NOT need updating.

## Post-Deletion Check

Search for broken references:

- `\ref{sec:<chapter>:<slug>}`
- `\hyperref[sec:<chapter>:<slug>]`
