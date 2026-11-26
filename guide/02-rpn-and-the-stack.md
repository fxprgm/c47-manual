# RPN and the Stack

The calculator works in RPN, Reverse Polish Notation: you enter the numbers first and the
operation after them. There is no equals key, and no parentheses. Intermediate
results wait on the **stack** until they are needed. This chapter shows how that works,
starting with a single addition.

## Your first calculation

To add 3 and 4:

1. Type [[3]].

   The 3 appears at the left of the X line, the bottom line of the stack. You are still
   typing it: a number being entered sits at the left.

   ![](screen:rpn-3)

2. Press [[ENTER]].

   The 3 is complete. It moves to the right, where finished numbers stand.

   ![](screen:rpn-3-enter)

3. Type [[4]].

   The 4 is typed on the X line, and the 3 moves up one line, to Y.

   ![](screen:rpn-4)

4. Press [[+]].

   The calculator adds Y and X and leaves the sum, 7, in X.

   ![](screen:rpn-7)

That is all of RPN: **numbers first, then the operation**. Every operation that needs two
numbers, such as [[+]], [[-]], [[×]], [[÷]] and [[yˣ]], takes them from Y and X and puts its
result in X. Operations on one number, such as [[√]], [[1/x]] or [[LN]], work on X alone.

::: note
The 7 has no decimal point: it is an *integer*, exact to any number of digits. The zeros
above it, `0.`, have one: they are *real* numbers. C47 keeps the two kinds apart. The
chapter on numbers explains when a result is an integer and when it is real.
:::

## The stack

The stack is a column of registers. The bottom four are always on screen, named, from the
bottom up:

| Register | Holds |
|---|---|
| X | the number you are working on, and every result |
| Y | the number before it: the first operand of [[+]], [[-]], [[×]], [[÷]] |
| Z, T | older numbers, waiting their turn |

Above T there are four more registers, out of view: the stack is eight registers deep. When
a new number arrives, everything moves up one place (the stack **lifts**). When an operation
combines X and Y into one result, everything above moves down one place (the stack
**drops**). So you never need to write down an intermediate result.

### A calculation in steps

Work out (12 + (6 × 4 − 4)) ÷ 8. Start with the innermost parentheses and work outwards:

1. Type [[6]] and press [[ENTER]].

   ![](screen:chain-6)

2. Type [[4]] and press [[×]].

   6 × 4 = 24. Pressing an operation also completes the number you were typing, so
   [[ENTER]] is not needed before it.

   ![](screen:chain-24)

3. Type [[4]] and press [[-]].

   24 − 4 = 20.

   ![](screen:chain-20)

4. Type [[1]] [[2]] and press [[+]].

   12 + 20 = 32. Addition does not mind the order of its numbers. The 12 could come second.

   ![](screen:chain-32)

5. Type [[8]] and press [[÷]].

   32 ÷ 8 = 4.

   ![](screen:chain-4)

Twelve keystrokes, no parentheses and nothing written down: each result was in X, ready for
the next operation.

::: tip
For [[-]] and [[÷]] the order matters: they work out Y − X and Y ÷ X. Type the number you
subtract from, or divide, first.
:::

## Entering numbers

| To enter | Press |
|---|---|
| a decimal fraction | [[.]] between the digits: [[1]] [[.]] [[5]] |
| a power of ten | [[EEX]] before the exponent: [[6]] [[.]] [[0]] [[2]] [[EEX]] [[2]] [[3]] for 6.02 × 10²³ |
| a negative number | [[CHS]] after it (or after its exponent, for a negative exponent) |
| a correction | [[←]] deletes the last digit typed |

1. Type [[6]] [[.]] [[0]] [[2]] [[EEX]] [[2]] [[3]].

   The exponent is shown raised, as it is written on paper.

   ![](screen:entry-eex)

2. Press [[ENTER]].

   ![](screen:entry-eex-enter)

3. Type [[1]] [[.]] [[5]] and press [[CHS]].

   [[CHS]] (change sign) makes the number you are typing negative. Pressed again, it
   makes it positive.

   ![](screen:entry-chs)

## Rearranging the stack

Sometimes the numbers are on the stack in the wrong order. These keys move them around
without changing them. To follow the examples, first put 1, 2, 3 and 4 on the stack with
[[1]] [[ENTER]] [[2]] [[ENTER]] [[3]] [[ENTER]] [[4]] [[ENTER]].

![The stack holds 1, 2, 3 and 4.](screen:stack-1234)

1. Press [[x⇄y]].

   X and Y change places. This is the key to use when the two numbers of [[-]] or [[÷]]
   are the wrong way round.

   ![](screen:stack-swap)

2. Press [[R↓]] (roll down).

   Every number moves down one register, and the one in X goes round to the top of the
   stack: to the eighth register, out of view. The register that comes into view as T is
   still empty.

   ![](screen:stack-rdn)

3. Press [[g]] [[R↓]] ([[g R↑]], roll up).

   The opposite of [[R↓]]: the 3 comes back down from the top into X.

   ![](screen:stack-rup)

More stack functions are in the stack menu, [[g STK]]. Among them are [[s FILL]], which
copies X into every register, and [[s CLSTK]], which clears the whole stack.

### LASTx: the number before the operation

Every operation keeps a copy of the X it used, called **LASTx**. [[f]] [[x⇄y]]
([[f LASTx]]) brings it back. It is the quickest way to reuse a number, or to undo an
operation done on the wrong number.

1. Work out 2 + 3: [[2]] [[ENTER]] [[3]] [[+]].

   ![](screen:lastx-5)

2. Press [[f]] [[x⇄y]] ([[f LASTx]]).

   The 3 that [[+]] used comes back into X, and the sum moves up to Y.

   ![](screen:lastx-3)

## What ENTER does

[[ENTER]] completes the number you are typing and puts it on the stack. That is all it does
in the calculator's standard setting, **eRPN** (entry RPN).

::: caution title="If you know other RPN calculators"
On HP's classic RPN calculators, [[ENTER]] also copies X into Y, so that 4 [[ENTER]] [[×]]
squares 4. With eRPN, it does not: [[×]] then multiplies the 4 by whatever was already in Y.
:::

1. With 7 in X (from 3 [[ENTER]] 4 [[+]]), type [[4]] and press [[ENTER]].

   The 4 is now in X, and the 7 in Y. There is no second copy of the 4.

   ![](screen:erpn-enter)

2. Press [[×]].

   7 × 4 = 28, not 4 × 4.

   ![](screen:erpn-28)

To square a number, press [[x²]]. If you prefer the classic behaviour, clear the flag eRPN
in the preferences menu, [[f PREF]].

## Percentages

[[f]] [[RCL]] ([[f %]]) works out X percent of Y, and keeps Y. So the result can be added to
the original amount at once, or taken from it. To add 19 % sales tax to a price of 200:

1. Type [[2]] [[0]] [[0]], press [[ENTER]] and type [[1]] [[9]].

   ![](screen:pct-19)

2. Press [[f]] [[RCL]] ([[f %]]).

   19 % of 200 is 38. The 200 stays in Y.

   ![](screen:pct-38)

3. Press [[+]].

   The price with tax: 238.

   ![](screen:pct-238)

[[g]] [[RCL]] ([[g Δ%]]) works out the change from Y to X, in percent.

## Correcting and clearing

1. While typing a number, [[←]] deletes the last digit: 123 becomes 12.

   ![](screen:bsp-123)
   ![](screen:bsp-12)

2. When you are not typing, [[←]] clears X: the number in X becomes 0, and the stack does
   not move. Here 12 and 5 were entered, and [[←]] cleared the 5.

   ![](screen:clx)

3. To clear the whole stack, open [[g STK]] and press [[F6]] ([[s CLSTK]]). Holding
   [[←]] until `CLSTK` appears at the top of the screen does the same.

   ![](screen:clstk)

::: tip
[[f]] [[←]] ([[f ⎌]], UNDO) takes back the last operation.
:::
