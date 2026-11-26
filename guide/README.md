# Writing the User's Guide

Each chapter is a Markdown file here, listed in `book.toml` in reading order. Plain Markdown
works as usual (Pandoc's flavour: headings, lists, tables, `*emphasis*`, `**bold**`). A few
additions express what a calculator guide needs. `tools/build.py` turns them into each format.

## Keys

| Write | For | Shows as |
|---|---|---|
| `[[ENTER]]` | a key, by its legend | a dark keycap |
| `[[f]]`, `[[g]]` | the shift keys | an orange or a blue keycap |
| `[[f DISP]]` | an f-shifted function, by its orange legend | the name in an orange-edged cap |
| `[[g STK]]` | a g-shifted function, by its blue legend | the name in a blue-edged cap |
| `[[s CLSTK]]` | a softkey label, as the screen shows it | the name in a square box |
| `[[F1]]` … `[[F6]]` | a softkey itself | a dark keycap |

Write the legends exactly as the keyboard has them (`guide/data/keyboard-r47.json`):
`[[x⇄y]]`, `[[R↓]]`, `[[←]]`, `[[÷]]`.

**In procedures, spell out the keys**, then name the function: "press `[[g]] [[x⇄y]]`
(`[[g STK]]`)". A reader looks for the keys; the name says what they are.

## Screens

```markdown
![Caption under the screen.](screen:menu-stk)
```

`screen:NAME` is `shots/png/NAME.png`, made by a `shot NAME` line in a script in
`shots/scripts/`. Never draw or edit a screen by hand: change the script and run
`shots/shoot.py`.

## Procedures

A numbered list whose items hold screens becomes a procedure: each step's text on the
left, its screen on the right (in the web formats, under it on a narrow screen).

```markdown
1. Press [[g]] [[x⇄y]] to open the stack menu, [[g STK]].

   Its functions appear in three rows above the softkeys.

   ![](screen:menu-stk)

2. Press [[f]].

   ![](screen:menu-stk-f)
```

Indent the screen and any further paragraphs by three spaces, so that they belong to the
step. A step may have no screen, or two.

## Boxes

```markdown
::: tip
Text of the tip.
:::
```

`note`, `tip`, `caution` and `example` are the four kinds. Give one its own heading with
`::: caution title="If you know other RPN calculators"`.

## The keyboard

```markdown
::: keyboard
:::
```

draws the R47 keyboard from `guide/data/keyboard-r47.json`, which `tools/gen_keyboard.py`
makes from C47's RefDB47 tables.

## Rules of the house

- **Every statement is checked on the calculator.** A screen is the best check. Where the
  text says what a key does, a script should show it. Where the engine can't (a long press,
  the power switch), check against the firmware source or the Owner's Manual, and keep the
  claim modest.
- Short sentences, one idea each. Present tense, second person: "Press [[ENTER]]. The 3
  moves up."
- Say what something is for before how it works.
- Name things as the calculator does: its legends, its menu names, its messages.
