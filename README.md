# Emrys — The Immortal Language

Emrys is a stack-based interpreted language written in Python.  
Named after the Welsh word for *immortal*, Emrys keeps things simple — no variables, no types, no fluff. Just a stack, some instructions, and your imagination.

```bash
python3 emrys.py <program.emrys>
```

---

## How It Works

Emrys is **stack-based** — all memory lives on a single stack. There are no variable names. You push values on, operate on them, and pop them off.

Think of the stack like a tray at Chick-fil-A — you stack items on top and always work from the top down. Last item on is the first item off.

```
SERVE 5    → stack: [5]
SERVE 3    → stack: [3, 5]   ← 3 is on top
COMBO      → stack: [8]      ← 3 + 5 combined into one
```

The **stack pointer** always tracks the top item. Two instructions drive everything:
- `SERVE` — puts a value on top
- `TOSS` — removes and discards the top value

---

## Instruction Set

### Stack Operations

| Instruction | Description |
|---|---|
| `SERVE n` | Push integer `n` onto the stack |
| `TOSS` | Pop and discard the top value |
| `REFILL` | Duplicate the top value |
| `SWITCHORDER` | Swap the top two values |

**Examples:**
```
SERVE 7        # stack: [7]
SERVE 3        # stack: [3, 7]
SWITCHORDER    # stack: [7, 3]
REFILL         # stack: [7, 7, 3]
TOSS           # stack: [7, 3]
```

---

### Arithmetic

| Instruction | Description |
|---|---|
| `COMBO` | Pop two values, push their sum |
| `NOPICKLE` | Pop two values, push `b - a` (b is deeper, a is on top) |
| `EXTRAEXTRA` | Pop two values, push their product |
| `FLIPNUM` | Negate the top value |
| `DIVIDE` | Pop two values, push quotient then remainder on top |

**NOPICKLE order matters** — `b - a` where `b` is the deeper value and `a` is on top:
```
SERVE 10       # stack: [10]
SERVE 3        # stack: [3, 10]
NOPICKLE       # stack: [7]   ← 10 - 3 = 7
```

**DIVIDE pushes two values** — quotient first, remainder on top:
```
SERVE 17       # stack: [17]
SERVE 5        # stack: [5, 17]
DIVIDE         # stack: [2, 3]   ← remainder 2 on top, quotient 3 below
```

---

### Input

| Instruction | Description |
|---|---|
| `ORDER` | Read an integer from the user, push it |
| `ORDERCHAR` | Read one character, push its ASCII code |
| `CUSTOMORDER` | Read a full line of text — pushes each character as ASCII then pushes the length N on top |

**CUSTOMORDER buffer layout** — for input `"hi"`:
```
After CUSTOMORDER: stack top→bottom = 2  h  i
                                       ↑
                                    length N on top
Popping gives: h then i (original order)
```

---

### Output

| Instruction | Description |
|---|---|
| `ANNOUNCE "text"` | Print a string literal. Supports `\n` and `\t` |
| `CALLOUT` | Pop a value and print it as an ASCII character |
| `RECEIPT` | Pop a value and print it as an integer |
| `PEEKRECEIPT` | Print the top value as an integer without popping |
| `LINEBREAK` | Print a newline |

**CALLOUT vs RECEIPT:**
```
SERVE 65
CALLOUT     # prints: A       ← treats 65 as ASCII character

SERVE 65
RECEIPT     # prints: 65      ← treats 65 as a number
```

---

### Control Flow

| Instruction | Description |
|---|---|
| `GOTO label` | Jump unconditionally to a label |
| `IFEMPTY label` | Jump if top == 0. Peeks — does NOT pop |
| `IFMORE label` | Jump if top > 0. Peeks — does NOT pop |
| `IFLESS label` | Jump if top < 0. Peeks — does NOT pop |
| `CLOSING` | Stop execution |

**IFEMPTY, IFMORE, IFLESS peek — they never pop.**  
The value stays on the stack after the check. TOSS it manually when you no longer need it.

**Loop pattern:**
```
SERVE 3        # counter = 3

LOOP:
    IFEMPTY DONE       # if counter == 0, exit
    PEEKRECEIPT        # print current counter
    LINEBREAK
    SERVE 1
    NOPICKLE           # counter -= 1
    GOTO LOOP

DONE:
    TOSS               # clean up the 0
    CLOSING
```
Output: `3  2  1`

**If / else pattern:**
```
ORDER
IFEMPTY ISZERO
ANNOUNCE "not zero"
LINEBREAK
CLOSING

ISZERO:
ANNOUNCE "zero"
LINEBREAK
CLOSING
```

---

### String Helpers

| Instruction | Description |
|---|---|
| `FLIPORDER` | Reverse the string buffer in place. Pops N, reverses N chars, pushes back with N on top |
| `COPYSTRING` | Copy the string buffer. Pushes a second identical copy on top of the original |
| `SAMETHING` | Compare two string buffers. Pops both, pushes 1 if equal, 0 if not |

**How FLIPORDER works:**
```
# After CUSTOMORDER "hello": stack = [5, h, e, l, l, o]
FLIPORDER
# stack = [5, o, l, l, e, h]
# Now popping gives o, l, l, e, h — reversed
```

**How COPYSTRING works:**
```
# Before: stack = [3, h, i, !]
COPYSTRING
# After:  stack = [3, h, i, !, 3, h, i, !]
#                  ↑ copy on top  ↑ original below
```

**How SAMETHING works:**
```
# Stack has two string buffers loaded
SAMETHING
# Pops both strings, pushes 1 if they match, 0 if they don't
# Used in is_palindrome: load original, copy it, flip copy, compare
```

---

## Labels

Define a label with a name followed by a colon on its own line:
```
LOOP:
    SERVE 1
    NOPICKLE
    GOTO LOOP
```
Labels are recorded during parsing and never executed — they are named positions in the code that GOTO and IF instructions jump to.

---

## Comments

Any text after `#` is ignored:
```
SERVE 5       # push the number 5
# this whole line is a comment
COMBO         # add top two values
```

---

## Writing Programs

### Hello World
```
ANNOUNCE "Hello, World!"
LINEBREAK
CLOSING
```

### Read and echo a number
```
ANNOUNCE "Enter a number: "
ORDER
ANNOUNCE "You entered: "
RECEIPT
LINEBREAK
CLOSING
```

### Square a number
```
ANNOUNCE "Enter a number: "
ORDER
REFILL             # duplicate so we have two copies
EXTRAEXTRA         # multiply them together
ANNOUNCE "Squared: "
RECEIPT
LINEBREAK
CLOSING
```

### Count down from N
```
SERVE 5

LOOP:
    IFEMPTY DONE
    PEEKRECEIPT
    LINEBREAK
    SERVE 1
    NOPICKLE
    GOTO LOOP

DONE:
    TOSS
    CLOSING
```

### Repeat a character
```
ORDERCHAR          # read one character
ORDER              # read repeat count

LOOP:
    IFEMPTY DONE
    SWITCHORDER
    REFILL
    CALLOUT
    SWITCHORDER
    SERVE 1
    NOPICKLE
    GOTO LOOP

DONE:
    TOSS
    TOSS
    LINEBREAK
    CLOSING
```

### Reverse a string
```
ANNOUNCE "Enter a string: "
CUSTOMORDER
FLIPORDER

LOOP:
    IFEMPTY DONE
    SWITCHORDER
    CALLOUT
    SERVE 1
    NOPICKLE
    GOTO LOOP

DONE:
    TOSS
    LINEBREAK
    CLOSING
```

### Check palindrome
```
ANNOUNCE "Enter a string: "
CUSTOMORDER        # load string
COPYSTRING         # make a copy
FLIPORDER          # reverse the copy
SAMETHING          # compare — pushes 1 or 0

IFEMPTY NOTPALINDROME
ANNOUNCE "palindrome"
LINEBREAK
CLOSING

NOTPALINDROME:
ANNOUNCE "not a palindrome"
LINEBREAK
CLOSING
```

---

## Included Programs

| File | Description |
|---|---|
| `helloworld.emrys` | Prints Hello, World! |
| `cat.emrys` | Reads a line and echoes it back |
| `multiply.emrys` | Multiplies two integers from user input |
| `repeater.emrys` | Repeats a character N times |
| `reverse_string.emrys` | Reads a string and prints it reversed |
| `is_palindrome.emrys` | Checks whether a string is a palindrome |
| `is_even.emrys` | Checks whether an integer is even or odd |

---

## Full Keyword Reference

| Keyword | One job |
|---|---|
| `SERVE n` | Push one value |
| `TOSS` | Discard top |
| `REFILL` | Duplicate top |
| `SWITCHORDER` | Swap top two |
| `COMBO` | Add top two |
| `NOPICKLE` | Subtract top two (b - a) |
| `EXTRAEXTRA` | Multiply top two |
| `DIVIDE` | Divide top two, push quotient + remainder |
| `FLIPNUM` | Negate top value |
| `ORDER` | Read integer from user |
| `ORDERCHAR` | Read one character from user |
| `CUSTOMORDER` | Read full line from user |
| `ANNOUNCE "..."` | Print string literal |
| `CALLOUT` | Print top as character |
| `RECEIPT` | Print top as integer (pops) |
| `PEEKRECEIPT` | Print top as integer (no pop) |
| `LINEBREAK` | Print newline |
| `GOTO label` | Unconditional jump |
| `IFEMPTY label` | Jump if top == 0 (peek) |
| `IFMORE label` | Jump if top > 0 (peek) |
| `IFLESS label` | Jump if top < 0 (peek) |
| `CLOSING` | Stop program |
| `FLIPORDER` | Reverse string buffer |
| `COPYSTRING` | Copy string buffer |
| `SAMETHING` | Compare two string buffers |

---

## Requirements

- Python 3.6 or higher
- No external dependencies

---

## Author

Lewis — Oklahoma Christian University  
Dual B.S. Computer Science & Cybersecurity / M.S. Cybersecurity
