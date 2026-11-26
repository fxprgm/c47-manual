# What's next

The running list of pending work. Read it at the start of a session; update it when something
is done or found.

## Waiting on the user

- **Review the sample chapters** (`guide/01`, `guide/02`): the user is reading them now. Nothing
  below is started until they have (decided 2026-11-26). Questions for them: the look (steps
  on the left with the screen on the right, keycaps in the R47's colours, chapter-page numbers),
  the depth of chapters 1-2, A4 only or a US Letter edition too.
- **Tell the C47 team, and answer the Reddit thread** that asked for one complete manual
  (r/SwissMicrosC47R47 or similar): the bundle PDF answers it today. Draft the posts for the
  user to send (under their name), once they have reviewed the chapters.
- **Compare a few screens with a real R47** (start, STK, DISP page 2, CAT), if the user or
  someone with an R47 can: they should match except the date and the battery icon, which come
  from DMCP on the calculator and from c47-cg's stand-in here.

## Next, in this order, after the review

1. **Generated appendices, no writing needed:** a *menu atlas*, every page of every menu as a
   real screen (RefDB47 `softmenus`/`menus` tables + the engine; about 190 menus), and a
   *function index*, every command with its menu, key and description (`items` table).
2. **Self-checking examples:** a script command that checks X (for example `expect X 238`),
   so a worked example that stops being true fails the `screens` workflow.
3. **Chapter 3: numbers and how they are shown** (integers and reals, fractions, FIX / SCI /
   ENG / ALL, digit grouping). Then the chapters in the order under "To do".

## To do

- **Chapters.** Proposed order after 1-2: numbers and their types (integers, reals, fractions,
  display formats), the math functions, complex numbers, units and constants, statistics,
  financial (TVM), integers and bases, matrices and vectors, equations (solver, integration),
  plotting, text (alpha), programming (several chapters, an examples library), customising
  (user mode, assignments), files and USB, then appendices generated from RefDB47: every
  function, every menu (with its screen), flags, error messages, the keyboard of each model.
- **More generated appendices**: flags and error messages, from RefDB47 `flags` and `errors`.
- **C47 edition** (DM42 keyboard): the same text with the DM42 key legends; needs key
  references by function rather than by R47 legend.
- **Website**: the `site` format on GitHub Pages.
- **Engine**: long presses (the engine presses each key for 80 ms), so CLSTK-by-holding and
  similar can be shown.

## Done (newest first)

- 2026-11-26: the repository's branch renamed to `main` (the default); fxprgm/c47-cg's branch
  with the `lcd` command and the CMake 4 fix merged (c47-cg#1), so `C47_VERSION`'s pin d043587
  is on c47-cg's main.
- 2026-11-26: repository set up. Bundles of the C47 team's Owner's Manual and application
  notes (bundle/, weekly workflow, release `bundle`); the screenshot engine (c47-cg's PC build
  without its CG50 layout patch, `lcd` command) and shooter; the build to PDF (whole and per
  chapter), HTML (one page and a site), EPUB and DOCX with Typst and Pandoc from pip; the
  keyboard drawn from RefDB47; chapters 1 (Getting Acquainted) and 2 (RPN and the Stack) with
  38 screens. Found on the way: DISP's region settings are on its second page (the Owner's
  Manual of 2026-11-15 says the third).
