# Book Structure Guide

This document describes the folder and file naming conventions for creating structured books. The structure is **format-agnostic** - it works with any markup language (.tex, .md, .html, etc.).

---

## Overview

```
type/
├── main.tex                          # Root file - includes all parts
├── localsettings.tex                 # Global settings/styles
├── 100-frontmatter/                 # Front matter section
├── 200-bodymatter/                  # Main content
│   ├── part01-name/                 # Part 1
│   │   └── chXX-name/               # Chapters (roman numerals for intro)
│   │       └── secXX-name.tex        # Sections
│   └── part02-name/                 # Part 2
│       └── chXX-name/               # Chapters (arabic numerals)
├── 300-backmatter/                  # Back matter section
└── bib/                             # Bibliography/references
```

---

**type** could be any language in which the book is written:

* latex - which means xx=tex
* markdown - which means xx=md
* html - which means xx =html
* etc

## Naming Conventions

### Numeric Prefixes

All folders and files use **3-digit numeric prefixes** for sorting:

| Prefix Range | Purpose                    |
| ------------ | -------------------------- |
| `100-199`  | Front matter               |
| `200-299`  | Body matter (main content) |
| `300-399`  | Back matter                |

Within ranges, use **10-unit increments** to allow insertions:

- `100`, `110`, `120`, `130`... (not 101, 102, 103)

### Slug Format

After the numeric prefix, use **lowercase descriptive names**:

- Words separated by hyphens: `ch01-ettersporselprognoser`
- No special characters (ø → o, æ → ae, å → a)
- Keep reasonably short (max ~30 chars)

---

## Hierarchy Levels

### Level 1: Root

```
main.tex                    # Root document
localsettings.tex           # Global configuration
```

### Level 2: Major Sections (Frontmatter, Bodymatter, Backmatter)

```
100-frontmatter/
├── frontmatter.tex         # Aggregator - includes all frontmatter files
├── 100-frontpage.tex       # Title page
├── 110-preface.tex         # Preface
├── 120-about.tex           # About this book
├── 130-acknowledgements.tex
└── 140-toc.tex             # Table of contents
```

```
200-bodymatter/
├── bodymatter.tex          # Aggregator - includes all parts
├── part01-innledning/     # Part 1: Introduction
└── part02-omrader/        # Part 2: Topics
```

```
300-backmatter/
├── backmatter.tex          # Aggregator
├── 100-bibliography.tex    # References list
├── 110-index.tex           # Index
├── app01-name/            # Appendix A
└── app02-name/            # Appendix B
```

### Level 3: Parts

Parts are numbered folders within bodymatter:

```
200-bodymatter/
├── part01-innledning/     # Part 1
│   └── part01.tex          # Part aggregator
└── part02-omrader/        # Part 2
    └── part02.tex          # Part aggregator
```

### Level 4: Chapters

Chapters use prefixes that match their numbering scheme:

**Part 1 (Introduction) - Roman numerals:**

```
part01-innledning/
├── chi-begreper/                           # Chapter I
│   └── chi-begreper.tex
├── chii-arbeidsflyt-og-ki/                 # Chapter II
│   └── chii-arbeidsflyt-og-ki.tex
└── chiii-prosjektgjennomforing-med-ki/     # Chapter III
    └── chiii-prosjektgjennomforing-med-ki.tex
```

**Part 2 (Main content) - Arabic numerals:**

```
part02-omrader/
├── ch01-ettersporselprognoser/     # Chapter 1
│   └── ch01-ettersporselprognoser.tex
├── ch02-lagerstyring/              # Chapter 2
│   └── ch02-lagerstyring.tex
└── ch03-produksjonsplanlegging/    # Chapter 3
    └── ch03-produksjonsplanlegging.tex
```

### Level 5: Sections

Sections are files within chapter folders:

```
ch01-ettersporselprognoser/
├── ch01-ettersporselprognoser.tex      # Chapter file (aggregator)
├── sec01-omrade.tex                    # Section 1.1
├── sec02-problemstilling.tex           # Section 1.2
├── sec03-modell.tex                    # Section 1.3
├── sec04-prosess.tex                   # Section 1.4
├── sec05-metode.tex                    # Section 1.5
├── sec06-eksempel-kampanjestyring.tex  # Section 1.6
├── sec07-eksempel-lagerstyring-ml.tex  # Section 1.7
└── sec08-anbefalt-fordypning.tex       # Section 1.8
```

### Level 6: Supporting Folders

Each chapter can have supporting folders:

```
ch01-ettersporselprognoser/
├── ch01-ettersporselprognoser.tex
├── sec01-omrade.tex
├── figures/          # Images for this chapter
├── docs/             # Source documents, notes
└── references/       # Chapter-specific references
```

---

## Complete Example

Based on "Kvantitative metoder i logistikk":


```text
📁 latex/
├─📁 100-frontmatter/
│ ├─📄 100-frontpage.tex
│ ├─📄 110-preface.tex
│ ├─📄 120-about.tex
│ ├─📄 130-acknowledgements.tex
│ ├─📄 140-toc.tex
│ └─📄 frontmatter.tex
├─📁 200-bodymatter/
│ ├─📄 bodymatter.tex
│ ├─📁 part01-innledning/
│ │ ├─📁 chi-begreper/
│ │ │ ├─📄 chi-begreper.tex
│ │ │ ├─📁 docs/
│ │ │ │ ├─📄 5-concepts.md
│ │ │ │ └─📄 Screenshot 2026-01-09 155907.png
│ │ │ ├─📁 figures/
│ │ │ │ ├─📄 kapittelstruktur.png
│ │ │ │ ├─📄 kapittelstruktur_new.png
│ │ │ │ ├─📄 kompendiet_tilnaerming.png
│ │ │ │ └─📄 prosess_fem_steg.png
│ │ │ ├─📄 sec01-omrade.tex
│ │ │ ├─📄 sec02-problemstilling.tex
│ │ │ ├─📄 sec03-modell.tex
│ │ │ ├─📄 sec04-prosess.tex
│ │ │ └─📄 sec05-metoder.tex
│ │ ├─📁 chii-arbeidsflyt-og-ki/
│ │ │ ├─📄 chii-arbeidsflyt-og-ki.tex
│ │ │ ├─📁 figures/
│ │ │ │ └─📄 kompendiet_tilnaerming.png
│ │ │ ├─📄 sec01-arbeidsflyt.tex
│ │ │ └─📄 sec02-ki.tex
│ │ ├─📁 chiii-prosjektgjennomforing-med-ki/
│ │ │ ├─📄 chiii-prosjektgjennomforing-med-ki.tex
│ │ │ ├─📁 figures/
│ │ │ │ └─📄 fire_faser.png
│ │ │ ├─📄 sec01-rolleavklaring.tex
│ │ │ └─📄 sec02-fire-faser.tex
│ │ └─📄 part01.tex
│ └─📁 part02-omrader/
│   ├─📁 ch01-ettersporselprognoser/
│   │ ├─📁 build/
│   │ │ ├─📄 sec01-omrade.aux
│   │ │ ├─📄 sec01-omrade.bcf
│   │ │ ├─📄 sec01-omrade.idx
│   │ │ ├─📄 sec01-omrade.log
│   │ │ ├─📄 sec01-omrade.out
│   │ │ ├─📄 sec01-omrade.pdf
│   │ │ ├─📄 sec01-omrade.run.xml
│   │ │ └─📄 sec01-omrade.synctex.gz
│   │ ├─📄 ch01-ettersporselprognoser.tex
│   │ ├─📁 docs/
│   │ │ └─📄 ch01.md
│   │ ├─📁 figures/
│   │ │ ├─📄 arima_hero.png
│   │ │ ├─📄 arima_method.png
│   │ │ ├─📄 arima_model.png
│   │ │ ├─📄 arima_pdq_definition.png
│   │ │ ├─📄 arima_problem.png
│   │ │ ├─📄 ettersporselprognoser_intro.png
│   │ │ ├─📄 gb_decision_tree.png
│   │ │ ├─📄 gb_ensemble_concept.png
│   │ │ ├─📄 gb_hero.png
│   │ │ ├─📄 gb_level_vs_leaf.png
│   │ │ ├─📄 gb_method.png
│   │ │ ├─📄 gb_model.png
│   │ │ ├─📄 gb_problem.png
│   │ │ ├─📄 gb_shap_summary.png
│   │ │ └─📄 gb_time_series_cv.png
│   │ ├─📄 sec01-omrade.tex
│   │ ├─📄 sec02-problemstilling.tex
│   │ ├─📄 sec03-trend-og-sesong.tex
│   │ ├─📄 sec04-eksterne-faktorer.tex
│   │ ├─📄 sec05-mange-variabler.tex
│   │ ├─📄 sec06-intermitterende.tex
│   │ ├─📄 sec07-komplekse-sekvenser.tex
│   │ └─📄 sec08-fordypning.tex
│   ├─📁 ch02-lagerstyring/
│   │ ├─📄 ch02-lagerstyring.tex
│   │ ├─📄 sec01-kvantitative-utfordringer.tex
│   │ ├─📄 sec02-metoder-lagerstyring.tex
│   │ ├─📄 sec03-lagerstyring-eksempel-metode-1.tex
│   │ ├─📄 sec04-lagerstyring-eksempel-metode-2.tex
│   │ ├─📄 sec05-lagerstyring-eksempel-metode-3.tex
│   │ ├─📄 sec06-lagerstyring-eksempel-metode-4.tex
│   │ └─📄 sec07-lagerstyring-eksempel-metode-5.tex
│   ├─📁 ch03-produksjonsplanlegging/
│   │ ├─📄 ch03-produksjonsplanlegging.tex
│   │ ├─📄 sec01-kvantitative-utfordringer.tex
│   │ ├─📄 sec02-metoder-produksjonsplanlegging.tex
│   │ ├─📄 sec03-produksjonsplanlegging-eksempel-metode-1.tex
│   │ ├─📄 sec04-produksjonsplanlegging-eksempel-metode-2.tex
│   │ ├─📄 sec05-produksjonsplanlegging-eksempel-metode-3.tex
│   │ ├─📄 sec06-produksjonsplanlegging-eksempel-metode-4.tex
│   │ └─📄 sec07-produksjonsplanlegging-eksempel-metode-5.tex
│   ├─📁 ch04-nettverksdesign/
│   │ ├─📄 ch04-nettverksdesign.tex
│   │ ├─📄 sec01-kvantitative-utfordringer.tex
│   │ ├─📄 sec02-metoder-nettverksdesign.tex
│   │ ├─📄 sec03-nettverksdesign-eksempel-metode-1.tex
│   │ ├─📄 sec04-nettverksdesign-eksempel-metode-2.tex
│   │ ├─📄 sec05-nettverksdesign-eksempel-metode-3.tex
│   │ ├─📄 sec06-nettverksdesign-eksempel-metode-4.tex
│   │ └─📄 sec07-nettverksdesign-eksempel-metode-5.tex
│   ├─📁 ch05-forsyningskjedeanalyse/
│   │ ├─📄 ch05-forsyningskjedeanalyse.tex
│   │ ├─📄 sec01-kvantitative-utfordringer.tex
│   │ ├─📄 sec02-metoder-forsyningskjedeanalyse.tex
│   │ ├─📄 sec03-forsyningskjede-eksempel-metode-1.tex
│   │ ├─📄 sec04-forsyningskjede-eksempel-metode-2.tex
│   │ ├─📄 sec05-forsyningskjede-eksempel-metode-3.tex
│   │ ├─📄 sec06-forsyningskjede-eksempel-metode-4.tex
│   │ └─📄 sec07-forsyningskjede-eksempel-metode-5.tex
│   ├─📁 ch06-ko-teori/
│   │ ├─📄 ch06-ko-teori.tex
│   │ ├─📄 sec01-kvantitative-utfordringer.tex
│   │ ├─📄 sec02-metoder-ko-teori.tex
│   │ ├─📄 sec03-ko-teori-eksempel-metode-1.tex
│   │ ├─📄 sec04-ko-teori-eksempel-metode-2.tex
│   │ ├─📄 sec05-ko-teori-eksempel-metode-3.tex
│   │ ├─📄 sec06-ko-teori-eksempel-metode-4.tex
│   │ └─📄 sec07-ko-teori-eksempel-metode-5.tex
│   ├─📁 ch07-lagerdrift/
│   │ ├─📄 ch07-lagerdrift.tex
│   │ ├─📄 sec01-kvantitative-utfordringer.tex
│   │ ├─📄 sec02-metoder-lagerdrift.tex
│   │ ├─📄 sec03-lagerdrift-eksempel-metode-1.tex
│   │ ├─📄 sec04-lagerdrift-eksempel-metode-2.tex
│   │ ├─📄 sec05-lagerdrift-eksempel-metode-3.tex
│   │ ├─📄 sec06-lagerdrift-eksempel-metode-4.tex
│   │ └─📄 sec07-lagerdrift-eksempel-metode-5.tex
│   ├─📁 ch08-barekraftig-logistikk/
│   │ ├─📄 ch08-barekraftig-logistikk.tex
│   │ ├─📄 sec01-kvantitative-utfordringer.tex
│   │ ├─📄 sec02-metoder-barekraftig-logistikk.tex
│   │ ├─📄 sec03-barekraftig-logistikk-eksempel-metode-1.tex
│   │ ├─📄 sec04-barekraftig-logistikk-eksempel-metode-2.tex
│   │ ├─📄 sec05-barekraftig-logistikk-eksempel-metode-3.tex
│   │ ├─📄 sec06-barekraftig-logistikk-eksempel-metode-4.tex
│   │ └─📄 sec07-barekraftig-logistikk-eksempel-metode-5.tex
│   ├─📁 ch09-returlogistikk/
│   │ ├─📄 ch09-returlogistikk.tex
│   │ ├─📄 sec01-kvantitative-utfordringer.tex
│   │ ├─📄 sec02-metoder-returlogistikk.tex
│   │ ├─📄 sec03-returlogistikk-eksempel-metode-1.tex
│   │ ├─📄 sec04-returlogistikk-eksempel-metode-2.tex
│   │ ├─📄 sec05-returlogistikk-eksempel-metode-3.tex
│   │ ├─📄 sec06-returlogistikk-eksempel-metode-4.tex
│   │ └─📄 sec07-returlogistikk-eksempel-metode-5.tex
│   ├─📁 ch10-innkjopsoptimalisering/
│   │ ├─📄 ch10-innkjopsoptimalisering.tex
│   │ ├─📄 sec01-kvantitative-utfordringer.tex
│   │ ├─📄 sec02-metoder-innkjopsoptimalisering.tex
│   │ ├─📄 sec03-innkjopsoptimalisering-eksempel-metode-1.tex
│   │ ├─📄 sec04-innkjopsoptimalisering-eksempel-metode-2.tex
│   │ ├─📄 sec05-innkjopsoptimalisering-eksempel-metode-3.tex
│   │ ├─📄 sec06-innkjopsoptimalisering-eksempel-metode-4.tex
│   │ └─📄 sec07-innkjopsoptimalisering-eksempel-metode-5.tex
│   ├─📁 ch11-risikostyring/
│   │ ├─📄 ch11-risikostyring.tex
│   │ ├─📄 sec01-kvantitative-utfordringer.tex
│   │ ├─📄 sec02-metoder-risikostyring.tex
│   │ ├─📄 sec03-risikostyring-eksempel-metode-1.tex
│   │ ├─📄 sec04-risikostyring-eksempel-metode-2.tex
│   │ ├─📄 sec05-risikostyring-eksempel-metode-3.tex
│   │ ├─📄 sec06-risikostyring-eksempel-metode-4.tex
│   │ └─📄 sec07-risikostyring-eksempel-metode-5.tex
│   └─📄 part02.tex
├─📁 300-backmatter/
│ ├─📄 100-bibliography.tex
│ ├─📄 110-index.tex
│ ├─📁 app01-sjekklister/
│ │ ├─📄 app01-sjekklister.tex
│ │ ├─📄 sec01-a-niva.tex
│ │ ├─📄 sec02-problemstilling.tex
│ │ ├─📄 sec03-teori-metode-analyse.tex
│ │ ├─📄 sec04-analyse-resultat.tex
│ │ └─📄 sec05-figurer-tabeller.tex
│ ├─📁 app02-types/
│ │ ├─📄 app02-types.tex
│ │ ├─📄 sec01-kvalitativ.tex
│ │ ├─📄 sec02-kvantitativ.tex
│ │ ├─📄 sec03-mixed-methods.tex
│ │ ├─📄 sec04-case-studie.tex
│ │ ├─📄 sec05-drofting.tex
│ │ ├─📄 sec06-analytisk.tex
│ │ ├─📄 sec07-modellering.tex
│ │ └─📄 sec08-teorianalyse.tex
│ └─📄 backmatter.tex
├─📁 bib/
│ └─📄 references.bib
├─📄 localsettings.tex
└─📄 main.tex
```

---

## Naming Pattern Summary

| Element                 | Pattern           | Example                           |
| ----------------------- | ----------------- | --------------------------------- |
| Major section folder    | `NNN-name/`     | `100-frontmatter/`              |
| Frontmatter file        | `NNN-name.tex`   | `120-about.tex`                  |
| Part folder             | `partNN-name/`  | `part01-innledning/`            |
| Chapter folder (roman)  | `chR-name/`     | `chi-begreper/`                 |
| Chapter folder (arabic) | `chNN-name/`    | `ch01-ettersporselprognoser/`   |
| Chapter file            | `chNN-name.tex`  | `ch01-ettersporselprognoser.tex` |
| Section file            | `secNN-name.tex` | `sec01-omrade.tex`               |
| Appendix folder         | `appNN-name/`   | `app01-sjekklister/`            |
| Aggregator file         | `name.tex`       | `bodymatter.tex`                 |

---

## Key Principles

1. **Folder = File**: The main file inside a folder has the same name as the folder

   - `ch01-ettersporselprognoser/ch01-ettersporselprognoser.tex`
2. **Aggregators**: Each container folder has an aggregator file that includes its children

   - `frontmatter.tex` includes all frontmatter files
   - `part01.tex` includes all chapters in Part 1
   - `ch01-ettersporselprognoser.tex` includes all sections
3. **Numeric sorting**: Prefixes ensure correct display order in file browsers
4. **Self-contained chapters**: Each chapter folder contains everything it needs:

   - Main chapter file
   - Section files
   - figures/ folder
   - docs/ folder (optional)
5. **Consistent depth**: All content follows the same hierarchy depth:

   - main → bodymatter → part → chapter → section
