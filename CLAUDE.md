# c47-manual: documentation for C47 / R47

**First, every session: read `NEXT.md`** (pending work, what waits on the user). Update it in
the same commit when something is done or found. `README.md` explains the repository,
`guide/README.md` the guide's markup.

## Rules

- **Every claim in the guide is checked on the calculator**, preferably by a screen: write the
  key script (`shots/scripts/`), run `shots/shoot.py`, look at the screens, then write the
  text from what they show. The Owner's Manual can be out of date (see NEXT.md).
- Screens are never edited by hand; `shots/png/` is the shooter's output.
- The guide's text is GFDL 1.3+: text taken from C47's own documentation (also GFDL) is
  allowed, and is credited.
- Keep the builds dependency-light: `pip install -r requirements.txt` must be all a reader
  needs to build every format.

## Commands

```bash
pip install -r requirements.txt                 # typst, pandoc (pypandoc_binary), pypdf, pillow
python3 tools/build.py [pdf split html site epub docx]
python3 shots/engine.py [--c47cg PATH]          # the engine; needs c47-cg's PC build deps
python3 shots/shoot.py [--check] [NAME...]
python3 bundle/bundle.py                        # the C47 team's docs in whole PDFs
python3 tools/gen_keyboard.py                   # after moving C47_VERSION
```

In a fresh cloud session the engine's build dependencies come from fxprgm/c47-cg's
`tools/setup_env.py` (its `apt()` and `xlsxio()`; the CG50 toolchain is not needed).
