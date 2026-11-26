# Getting Acquainted

This chapter introduces the calculator: its keys, its screen, and the menus that hold most
of its functions. Read it first. Every later chapter assumes you can find a function in a
menu, and that you know how to back out when something unexpected appears.

## About this guide

This guide is written for the **R47**, SwissMicros' calculator that runs the C47 firmware.
The same firmware runs as the **C47** on the DM42 and DM42n. Its screens and functions are
the same, but its keyboard is arranged differently. Where a key differs, the
[keyboard map](#the-keyboard) of your model tells you which key to press.

Every screen in this guide is the calculator's own. It was made by running the C47
firmware with exactly the keystrokes the text describes, so what you see is what the
calculator shows. The version of C47 the screens come from is on the title page. A newer
version may change a menu or two, and each new edition of the guide follows it.

### How keys are shown

| In this guide | Means |
|---|---|
| [[ENTER]] [[7]] [[x⇄y]] | the key with this legend |
| [[f]] [[g]] | the two shift keys, orange and blue |
| [[f DISP]] | the function printed in orange above a key: press [[f]], then that key |
| [[g STK]] | the function printed in blue above a key: press [[g]], then that key |
| [[s CLSTK]] | a label on the bottom of the screen: press the softkey under it ([[F1]] to [[F6]]) |

In step-by-step instructions the keys are written out in full, for example "press [[g]]
[[x⇄y]] ([[g STK]])". Elsewhere the shorter form is used.

## Turning the calculator on and off

1. Press [[EXIT]] to turn the calculator on.

   The screen shows the stack: four numbers, with the status bar above them and a row of
   labels below.

   ![](screen:start)

2. Press [[f]] [[EXIT]] ([[f OFF]]) to turn it off.

The calculator keeps everything while it is off: the numbers on the stack, your programs,
your settings. It also switches itself off after about ten minutes without a key press. You
lose nothing that way either.

::: caution
The memory is kept alive by the coin cell. Before you change the cell, save the calculator's
state to its flash memory, with [[s SAVE]] in the I/O menu, [[g I/O]]. Then nothing is lost even if
the change takes longer than planned.
:::

## The keyboard

::: keyboard
:::

Each key does up to three things:

- its **primary function**, the legend on the key itself, when you just press it;
- its **f-shifted function**, the orange legend above it, when you press [[f]] first;
- its **g-shifted function**, the blue legend above it, when you press [[g]] first.

1. Press [[f]].

   An **f** appears at the left of the status bar. The next key you press runs its orange
   function.

   ![](screen:shift-f)

2. Press [[g]] instead.

   Now a **g** appears, and the next key runs its blue function.

   ![](screen:shift-g)

Pressing the other shift key changes your mind: [[g]] after [[f]] makes it a **g**. Pressing
the same shift key again cancels it.

Many orange and blue legends are names in capitals, such as [[f DISP]], [[g STK]] or
[[f CAT]]. These open **menus** of related functions, as the next sections show. The
others, such as [[f ASIN]] or [[g π]], run a function at once.

The keys [[F1]] to [[F6]] along the top of the keyboard are the **softkeys**. They have no
legend of their own. Each runs whatever function the screen shows just above it.

## The display

The screen has three parts, from top to bottom.

![The screen as the calculator starts: the status bar, the four lowest stack registers and a row of softkey labels.](screen:start)

**The status bar.** The top line shows the date and the modes in force. At the start these
are a small angle sign (complex numbers are shown in rectangular form), a degree sign (angles
are in degrees), the fraction setting, and the integer word size, `64:2` (64-bit integers in
two's complement).
When a shift key is pressed, its **f** or **g** appears at the left. Each item can be hidden.
A full list is in the chapter on the status bar.

**The stack.** The four large numbers are the registers of the stack, X at the bottom and
T at the top. Chapter 2 explains them. The number you are typing appears on the X line,
at the left.

**The softkey menu.** The bottom rows label the softkeys [[F1]] to [[F6]]. When no menu is
open, the calculator shows a row of common functions: [[s x!]], [[s 10ˣ]] and others.

## Menus

Most functions live in menus, which open on the softkey rows. A menu has up to three rows
of six labels. The bottom row is reached with the softkeys alone, the middle row with [[f]]
and the top row with [[g]].

1. Press [[g]] [[x⇄y]] to open the stack menu, [[g STK]].

   Its functions appear in three rows above the softkeys.

   ![](screen:menu-stk)

2. Press [[f]].

   The middle row is now underlined: [[F1]] to [[F6]] reach the functions in it. [[f]]
   [[F6]], for example, runs the function above [[s CLSTK]].

   ![](screen:menu-stk-f)

3. Press [[f]] again to cancel the shift, then [[EXIT]] to close the menu.

A label in white on black, such as [[s MULTSTK]] above, opens another menu: a
**submenu**. [[EXIT]] goes back from a submenu to the menu it came from, one step at a time.

### Menus of several pages

A menu with more than eighteen functions continues on further pages. A small pair of
triangles at the top left of the menu (▴▾) tells you there is more. [[↑]] and [[↓]] turn the
pages. After the last page, the first comes round again.

1. Press [[f]] [[CHS]] to open the display settings, [[f DISP]].

   The first page sets how numbers are shown: [[s FIX]], [[s SCI]], [[s ENG]] and more.

   ![](screen:menu-disp)

2. Press [[↓]].

   The second page sets the regional conventions, the decimal mark and digit grouping among
   them: [[s CHINA]], [[s EUROP]], [[s INDIA]], [[s JAPAN]], [[s UK]], [[s USA]], or the
   factory setting [[s DEFLT]].

   ![](screen:menu-disp-2)

3. Press [[↓]] again for the third page, then [[EXIT]] to close the menu.

   ![](screen:menu-disp-3)

A small circle or diamond after a label marks one choice of several: the filled one is in
force. A small square marks a switch that is on (filled) or off (empty).

## The catalog

When you know a function's name but not its menu, look it up in the catalog. Press [[f]]
[[+]] ([[f CAT]]): its first row lists the catalogs.

![The catalog menu, [[f CAT]].](screen:cat)

| Softkey | Lists |
|---|---|
| [[s FCNS]] | every function, in alphabetical order |
| [[s CNST]] | the built-in constants |
| [[s CHARS]] | every character, for text |
| [[s PROGS]] | your programs |
| [[s VARS]] | your variables |
| [[s MENUS]] | every menu |

1. Press [[F1]] ([[s FCNS]]).

   The functions appear, eighteen to a page, starting with those whose names begin with
   a digit. The **A** in the status bar shows that the keys now type letters.

   ![](screen:cat-fcns)

2. Type the first one or two letters of the name you want. The list jumps to the first
   function at or after them.

3. Press the softkey of the function to run it, with [[f]] or [[g]] first if it is in the
   middle or top row. [[EXIT]] leaves the catalog without running anything.

## Getting out of trouble

Whatever has happened, these keys bring you back:

- [[EXIT]] closes a menu, cancels a prompt or a shift, and abandons a number you are typing.
  Press it as often as needed to get back to the plain stack.
- [[←]] deletes the last digit while you type a number. When you are not typing, it clears
  the number in X.
- [[f]] [[←]] ([[f ⎌]], UNDO) takes back the last operation.

::: tip
Hold [[EXIT]] down: the top left of the screen names what will happen when you let go, and
after a moment shows `CLRMOD`. Releasing it then closes every menu and ends every
special entry mode at once. If you hold a key by mistake, keep holding until `NOP` (no
operation) appears and let go: nothing happens.
:::

## Two settings to make first

The factory settings suit most work. Two are worth checking before you start.

**The angle unit.** Press [[g]] [[CHS]] ([[g TRG]]). The bottom row offers [[s DEG]],
[[s RAD]] and [[s GRAD]] among others. The filled circle shows the one in force: degrees, at
first.

![The angle menu, [[g TRG]]: degrees are in force.](screen:menu-trg)

**The number format and the region.** In [[f DISP]], as above: page 1 for the number of
digits ([[s FIX]], [[s SCI]], [[s ENG]], [[s ALL]]), page 2 for your country's conventions.
