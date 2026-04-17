# Emrys — The Immortal Language

Emrys is a stack-based interpreted language written in Python.  
Named after the Welsh word for *immortal*, Emrys keeps things simple: no variables, no types. Just a stack, some instructions, and your imagination.

Run any Emrys program with:
```bash
python3 emrys.py <program.emrys>
```

---

## How It Works

Emrys is **stack-based** — all memory lives on a single stack. There are no variable names. You push values on, operate on them, and pop them off. Think of the stack like a tray at Chick-fil-A — you stack items on top and always work from the top down.

The **stack pointer** always points at the top item. Two core operations drive everything:
- **SERVE** — puts a value on top of the stack
- **TOSS** — removes the top value and discards it

---

## Instruction Set

### Stack Operations

| Instruction | Description |
|---|---|
| `SERVE n` | Push integer `n` onto the stack |
| `TOSS` | Pop and discard the top value |
| `REFILL` | Duplicate the top value |
| `SWITCHORDER` | Swap the top two values |

### Arithmetic

| Instruction | Description |
|---|---|
| `COMBO` | Pop two values, push their sum |
| `NOPICKLE` | Pop two values, push `b - a` (b is deeper, a is top) |
| `EXTRAEXTRA` | Pop two values, push their product |
| `FLIPNUM` | Negate the top value |

### Input

| Instruction | Description |
|---|---|
| `ORDER` | Read an integer from the user, push it |
| `CUSTOMORDER` | Read a line of text — pushes each character as ASCII in reverse, then pushes the length N on top. Popping gives original order. |

### Output

| Instruction | Description |
|---|---|
| `ANNOUNCE "text"` | Print a string literal. Supports `\n` and `\t` |
| `CALLOUT` | Pop a value and print it as an ASCII character |
| `RECEIPT` | Pop a value and print it as an integer |
| `PEEKRECEIPT` | Print the top value as an integer without popping |
| `LINEBREAK` | Print a newline |

### Control Flow

| Instruction | Description |
|---|---|
| `GOTO label` | Jump unconditionally to a label |
| `IFEMPTY label` | Jump to label if top of stack == 0. Peeks — does NOT pop. |
| `IFMORE label` | Jump to label if top of stack > 0. Peeks — does NOT pop. |
| `IFLESS label` | Jump to label if top of stack < 0. Peeks — does NOT pop. |
| `CLOSING` | Stop execution |

### String Helpers

| Instruction | Description |
|---|---|
| `FLIPORDER` | Reverse the string buffer on the stack. Pops N, reverses the top N chars, pushes them back with N on top |
| `DOUBLECUP` | Duplicate the string buffer. Makes two identical copies of the top string (with lengths) on the stack |
| `SAMETHING` | Compare two string buffers. Pops both, pushes 1 if equal, 0 if not |

---

## Important Rules

**IFEMPTY, IFMORE, and IFLESS peek — they do not pop.**  
The value stays on the stack after the check. You must TOSS it manually if you no longer need it.

**NOPICKLE order matters.**  
`b - a` where `b` is the deeper value and `a` is on top. If your stack is `[1 | 5]` (5 on top), NOPICKLE gives `1 - 5 = -4`.

**CUSTOMORDER buffer layout.**  
After `CUSTOMORDER`, the stack looks like this (top to bottom):
```
N  char1  char2  ...  charN
```
`char1` is the first character typed. N is the length. Popping after CUSTOMORDER gives characters in original order.

**Always end with CLOSING.**  
Without CLOSING the interpreter runs off the end of the file. If you have multiple branches, every branch needs its own CLOSING.

---

## Labels

Define a label by writing its name followed by a colon on its own line:
```
LOOP:
    SERVE 2
    NOPICKLE
    GOTO LOOP
```
Labels are recorded during parsing and never executed as instructions — they are just named positions in the code.

---

## Comments

Any text after `#` on a line is ignored:
```
SERVE 5    # push the number 5
# this whole line is a comment
```

---

## Writing Your First Program

### Hello World
```
ANNOUNCE "Hello, World!"
LINEBREAK
CLOSING
```

### Read and print a number
```
ANNOUNCE "Enter a number: "
ORDER
ANNOUNCE "You entered: "
RECEIPT
LINEBREAK
CLOSING
```

### Count down from 5
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

### If / else pattern
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

## Included Programs

| File | Description |
|---|---|
| `helloworld.emrys` | Prints Hello, World! |
| `cat.emrys` | Reads a line and echoes it back |
| `multiply.emrys` | Multiplies two integers from user input |
| `repeater.emrys` | Repeats a character N times (enter ASCII code + count) |
| `reverse_string.emrys` | Reads a string and prints it reversed |
| `is_palindrome.emrys` | Checks whether a string is a palindrome |
| `is_even.emrys` | Checks whether an integer is even or odd |

---

## Full Keyword Reference

| Emrys | Meaning |
|---|---|
| SERVE | Push a value |
| TOSS | Discard top |
| REFILL | Duplicate top |
| SWITCHORDER | Swap top two |
| COMBO | Add |
| NOPICKLE | Subtract |
| EXTRAEXTRA | Multiply |
| FLIPNUM | Negate |
| ORDER | Read integer |
| CUSTOMORDER | Read string |
| ANNOUNCE | Print string literal |
| CALLOUT | Print character |
| RECEIPT | Print integer (pop) |
| PEEKRECEIPT | Print integer (peek) |
| LINEBREAK | Print newline |
| GOTO | Unconditional jump |
| IFEMPTY | Jump if top == 0 |
| IFMORE | Jump if top > 0 |
| IFLESS | Jump if top < 0 |
| CLOSING | Stop program |
| FLIPORDER | Reverse string buffer |
| DOUBLECUP | Duplicate string buffer |
| SAMETHING | Compare two string buffers |

---

## Requirements

- Python 3.6 or higher
- No external dependencies

---

## Author

Lewis — Oklahoma Christian University  
Dual B.S. Computer Science & Cybersecurity / M.S. Cybersecurity
EOF
echo "README written"
Output

