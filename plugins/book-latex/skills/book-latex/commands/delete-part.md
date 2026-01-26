# Delete Part

Removes a part and all its contents.

## Required Information

| Field    | Description                      | Ask if missing |
| -------- | -------------------------------- | -------------- |
| `part` | Part identifier (number or slug) | Yes            |

## Preconditions

- **Confirm with user** if part contains chapters

## Workflow

1. **Locate part** - Find part by number or slug
2. **Delete folder** - Remove entire part folder recursively
3. **Update aggregator** - Remove entry from bodymatter aggregator
4. **Renumber subsequent parts** - Maintain sequential order
5. **Compile the whole book**: `book compile` if any compilation error:
   1. Understand and locate the error
   2. Make changes to fix the error
   3. Recompile the book
   4. Repeat until the error is fixed
6. **Check cross-references** - Search the compilation log to see if there are any broken cross-references due to this change

## LaTeX Implementation

### Files to Delete

Remove entire folder recursively:

```
latex/200-bodymatter/part<NN>-<slug>/
```

### Aggregator Update

In `latex/200-bodymatter/bodymatter.tex`, remove:

```latex
% ============ DEL <N>: <TITLE UPPERCASE> ============
\part{<Title>}
\setcounter{chapter}{0}
\renewcommand{\thechapter}{\arabic{chapter}}
\subfile{part<NN>-<slug>/part<NN>.tex}
```

## Renumbering Subsequent Parts

After deletion, renumber all subsequent parts to maintain sequential order:

**Example:** Deleting part02 from [part01, part02, part03, part04]:

1. part03 → part02 (rename folder and files)
2. part04 → part03 (rename folder and files)
3. Update aggregator file with new paths

**Renaming Steps (for each part, from lowest to highest):**

1. Rename folder: `part<OLD>-<slug>/` → `part<NEW>-<slug>/`
2. Rename aggregator file: `part<OLD>.tex` → `part<NEW>.tex`
3. Update `\subfile{}` path in bodymatter.tex

**Note:** Chapter files inside parts do NOT need path updates - they reference `../../main.tex` (relative to main, not to part folder name).
