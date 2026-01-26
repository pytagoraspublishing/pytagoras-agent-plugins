# Delete Appendix

Removes an appendix and all its contents.

## Required Information

| Field        | Description                          | Ask if missing |
| ------------ | ------------------------------------ | -------------- |
| `appendix` | Appendix identifier (number or slug) | Yes            |

## Preconditions

- **Confirm with user** if appendix has content

## Workflow

1. **Locate appendix** - Find appendix by number or slug
2. **Delete folder** - Remove entire appendix folder recursively
3. **Update aggregator** - Remove entry from backmatter aggregator
4. **Renumber subsequent appendices** - Maintain sequential order
5. **Check cross-references** - Search for broken references

## LaTeX Implementation

### Files to Delete

Remove entire folder recursively:

```
latex/300-backmatter/app<NN>-<slug>/
```

This includes:

- Appendix file
- figures/ folder
- Any other contents

### Backmatter Aggregator Update

In `latex/300-backmatter/backmatter.tex`, remove:

```latex
\subfile{app<NN>-<slug>/app<NN>-<slug>.tex}
```

## Renumbering Subsequent Appendices

After deletion, renumber all subsequent appendices to maintain sequential order:

**Example:** Deleting app02 from [app01, app02, app03, app04]:

1. app03 → app02 (rename folder and files)
2. app04 → app03 (rename folder and files)
3. Update aggregator file with new paths

**Renaming Steps (for each appendix, from lowest to highest):**

1. Rename folder: `app<OLD>-<slug>/` → `app<NEW>-<slug>/`
2. Rename main file: `app<OLD>-<slug>.tex` → `app<NEW>-<slug>.tex`
3. Update `\subfile{}` path in backmatter.tex

**Note:** Labels using slugs (`\label{app:<slug>}`) do NOT need updating.

## Post-Deletion Check

Search for broken references:

- `\ref{app:<slug>}`
- `\hyperref[app:<slug>]`
