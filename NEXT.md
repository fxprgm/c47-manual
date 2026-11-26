# What's next

The running list of pending work. Read it at the start of a session; update it when something
is done or found.

## Waiting on the user

- **A `main` branch.** The repository was empty, so the first branch pushed
  (`claude/hopeful-lovelace-qhl315`) is its default. The workflows publish from `main` only
  (and the weekly bundle runs only on the default branch): create `main` from it (or rename
  it) and make `main` the default.
- **Review the sample chapters** (`guide/01`, `guide/02`; the PDF from the `guide` workflow's
  artifact or `python3 tools/build.py pdf`): the look (keycaps, steps with screens, chapter-page
  numbers), the tone, the depth. Decide before more chapters are written.
- **fxprgm/c47-cg**: merge its branch `claude/hopeful-lovelace-qhl315` (the PC build's
  `lcd FILE` command, which the engine uses). `C47_VERSION` pins c47-cg by that commit until then.
- **Tell the C47 team** (forum, or the documentation people on GitLab) about the guide and the
  bundles before the guide grows, so it reads as a companion to their Owner's Manual.

## To do

- **Chapters.** Proposed order after 1-2: numbers and their types (integers, reals, fractions,
  display formats), the math functions, complex numbers, units and constants, statistics,
  financial (TVM), integers and bases, matrices and vectors, equations (solver, integration),
  plotting, text (alpha), programming (several chapters, an examples library), customising
  (user mode, assignments), files and USB, then appendices generated from RefDB47: every
  function, every menu (with its screen), flags, error messages, the keyboard of each model.
- **Generated appendices**: a script reading `build/engine/c47-cg/upstream/docs/refdb47/data/*.tsv`
  (items, menus, flags, errors) into Markdown, and a script making a screen of every menu page.
- **Examples checked on the calculator**: a script command that compares X with an expected
  value, so a worked example that stops being true fails the `screens` workflow.
- **C47 edition** (DM42 keyboard): the same text with the DM42 key legends; needs key
  references by function rather than by R47 legend.
- **Website**: the `site` format on GitHub Pages.
- **Engine**: long presses (the engine presses each key for 80 ms), so CLSTK-by-holding and
  similar can be shown.

## Done (newest first)

- 2026-11-26: repository set up. Bundles of the C47 team's Owner's Manual and application
  notes (bundle/, weekly workflow, release `bundle`); the screenshot engine (c47-cg's PC build
  without its CG50 layout patch, `lcd` command) and shooter; the build to PDF (whole and per
  chapter), HTML (one page and a site), EPUB and DOCX with Typst and Pandoc from pip; the
  keyboard drawn from RefDB47; chapters 1 (Getting Acquainted) and 2 (RPN and the Stack) with
  38 screens. Found on the way: DISP's region settings are on its second page (the Owner's
  Manual of 2026-11-15 says the third).
