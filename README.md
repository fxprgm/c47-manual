# C47 / R47 documentation in one place

Documentation for the [C47](https://47calc.com) calculator firmware, which runs on the
SwissMicros R47 and, as the C47, on the DM42 and DM42n.

There are two parts:

1. **The C47 team's own documentation, gathered into whole PDFs.** The Owner's Manual and
   every application note come as many separate files. Here they are in one file, with
   bookmarks for every document and chapter, rebuilt weekly:
   - [Everything in one PDF](https://github.com/fxprgm/c47-manual/releases/download/bundle/C47-R47-Manual-and-Notes.pdf)
     (the Owner's Manual and all application notes)
   - [The Owner's Manual](https://github.com/fxprgm/c47-manual/releases/download/bundle/C47-R47-Owners-Manual.pdf)
   - [All application notes](https://github.com/fxprgm/c47-manual/releases/download/bundle/C47-R47-Application-Notes.pdf)

2. **The C47 / R47 User's Guide** (in progress). A step-by-step guide in the manner of the
   best calculator manuals: short procedures, each step with the screen it gives. The
   screens are real. Each one is made by running the C47 firmware with the keystrokes the
   text describes, so when C47 changes, the screens that changed are found automatically.
   Available as a PDF (whole or by chapter), a single web page, a small website, an EPUB
   and a DOCX: [the newest build](https://github.com/fxprgm/c47-manual/releases/tag/guide).

The User's Guide complements the Owner's Manual: the Guide teaches, the Manual is the
reference.

## Building it yourself

Python 3.11 or newer, then:

```bash
pip install -r requirements.txt
```

```bash
python3 tools/build.py
```

That builds every format into `dist/`. `python3 tools/build.py pdf` builds only the PDF; the
formats are `pdf split html site epub docx`. Pandoc and Typst come with the pip packages, the
fonts are in `fonts/`, and the screenshots are committed in `shots/png/`. Nothing else is
needed.

To gather the C47 team's documentation (part 1) yourself:

```bash
python3 bundle/bundle.py
```

## Writing for the guide

The chapters are Markdown files in `guide/`, in the order `guide/book.toml` gives. The few
additions to Markdown (keys, screens, step-by-step procedures, notes) are in
[guide/README.md](guide/README.md).

Each screen is made by a short key script in `shots/scripts/`:

```
key g x⇄y          # press g, then x⇄y
shot menu-stk      # the screen now -> shots/png/menu-stk.png
```

Making screens needs the *engine*: C47 built for a PC, headless, from
[fxprgm/c47-cg](https://github.com/fxprgm/c47-cg)'s test build. On Debian or Ubuntu with
c47-cg's build dependencies (its `tools/setup_env.py` installs them):

```bash
python3 shots/engine.py
```

```bash
python3 shots/shoot.py
```

`shoot.py` rewrites only the screens whose pixels changed, so `git status` lists exactly
the screens a script edit, or a new C47, changed. `C47_VERSION` pins the C47 that the
screens show. The `screens` workflow checks the committed screens against it.

## Layout

| Path | What |
|---|---|
| `guide/` | the User's Guide: chapters, `book.toml`, the keyboard data, the PDF and web styles |
| `shots/` | the screen scripts, the screens they make, the engine and the shooter |
| `tools/` | `build.py` (every format), `c47.lua` (the Pandoc filter), `gen_keyboard.py` |
| `bundle/` | gathers the Owner's Manual and the application notes into whole PDFs |
| `fonts/` | C47's own fonts (keys, softkey labels) and Source Sans 3 (text) |

## Licences

The guide's text, and the bundles of the C47 team's documentation, are under the
[GNU Free Documentation License 1.3](LICENSE) or any later version, with no Invariant
Sections, no Front-Cover Texts and no Back-Cover Texts: the licence of C47's own
documentation, so text can move between the two. The screens are the output of the C47
firmware (GPL-3.0). The C47 fonts in `fonts/` come from the C47 repository (GPL-3.0), and
Source Sans 3 is under the SIL Open Font License 1.1 (`fonts/SourceSans3-LICENSE.md`). The
build scripts are under the MIT licence.
