# Delete Chapter

Removes a chapter and all its contents.

## Required Information

| Field       | Description                         | Ask if missing     |
| ----------- | ----------------------------------- | ------------------ |
| `part`    | Part containing the chapter         | Yes (if ambiguous) |
| `chapter` | Chapter identifier (prefix or slug) | Yes                |

## Preconditions

- **Confirm with user** if chapter contains sections or figures

## Workflow

1. **Locate chapter** - Find chapter by number or slug in the target part
2. **Delete folder** - Remove entire chapter folder recursively
3. **Update aggregator** - Remove entry from part aggregator
4. **Renumber subsequent chapters** - Maintain sequential order
5. **Check cross-references** - Search for broken references

## LaTeX Implementation

### Files to Delete

Remove entire folder recursively:

```
latex/200-bodymatter/part<NN>-<partslug>/ch<XX>-<slug>/
```

This includes:

- Chapter file
- All section files
- figures/ folder
- Any other contents

### Part Aggregator Update

In `part<NN>.tex`, remove:

```latex
% Kapittel <N> - <Title>
\subfile{ch<XX>-<slug>/ch<XX>-<slug>.tex}
```

## Renumbering Subsequent Chapters

After deletion, renumber all subsequent chapters to maintain sequential order:

**Example:** Deleting ch02 from [ch01, ch02, ch03, ch04]:

1. ch03 → ch02 (rename folder and files)
2. ch04 → ch03 (rename folder and files)
3. Update aggregator file with new paths

**Renaming Steps (for each chapter, from lowest to highest):**

1. Rename folder: `ch<OLD>-<slug>/` → `ch<NEW>-<slug>/`
2. Rename main file: `ch<OLD>-<slug>.tex` → `ch<NEW>-<slug>.tex`
3. Update `\subfile{}` path in part aggregator

**Note:** Labels using slugs (`\label{ch:<slug>}`) do NOT need updating.

## Post-Deletion Check

Search for broken references:

- `\ref{ch:<slug>}`
- `\ref{sec:<slug>:*}`
- `\hyperref[ch:<slug>]`
