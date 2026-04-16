"""
Emrys Interpreter — The Immortal Language
A Chick-fil-A themed stack-based interpreted language.
Run with: python3 emrys.py <program.emrys>
"""

import sys


class Stack:
    def __init__(self, size=1024):
        self.data = [0] * size
        self.sp = -1

    def push(self, value):
        self.sp += 1
        if self.sp >= len(self.data):
            raise RuntimeError("Stack overflow — too many items on the tray!")
        self.data[self.sp] = value

    def pop(self):
        if self.sp < 0:
            raise RuntimeError("Stack underflow — the tray is already empty!")
        val = self.data[self.sp]
        self.sp -= 1
        return val

    def top(self):
        if self.sp < 0:
            raise RuntimeError("Can't peek — the tray is empty!")
        return self.data[self.sp]

    def is_empty(self):
        return self.sp < 0


def parse(source_lines):
    """Parse source lines into a flat program list and a label map."""
    program = []
    labels = {}
    token_counter = 0

    for line in source_lines:
        line = line.strip()
        if '#' in line:
            line = line[:line.index('#')].strip()
        if not line:
            continue

        parts = line.split()
        opcode = parts[0].upper()

        # Label definition
        if opcode.endswith(':'):
            labels[opcode[:-1]] = token_counter
            continue

        program.append(opcode)
        token_counter += 1

        # Instructions with arguments
        if opcode == 'SERVE':
            arg = parts[1]
            if arg.startswith("'") and arg.endswith("'"):
                program.append(ord(arg[1]))
            else:
                program.append(int(arg))
            token_counter += 1

        elif opcode == 'ANNOUNCE':
            if len(parts) > 1 and parts[1].startswith('"'):
                text = ' '.join(parts[1:])[1:]
                if text.endswith('"'):
                    text = text[:-1]
                text = text.replace('\\n', '\n').replace('\\t', '\t')
                program.append(text)
            else:
                program.append('')
            token_counter += 1

        elif opcode in ('IFEMPTY', 'IFMORE', 'IFLESS', 'GOTO'):
            program.append(parts[1])
            token_counter += 1

    return program, labels


def execute(program, labels):
    stack = Stack()
    pc = 0

    while pc < len(program):
        opcode = program[pc]
        pc += 1

        if opcode == 'CLOSING':
            break

        # --- Stack ops ---
        elif opcode == 'SERVE':
            stack.push(program[pc]); pc += 1

        elif opcode == 'TOSS':
            stack.pop()

        elif opcode == 'REFILL':
            stack.push(stack.top())

        elif opcode == 'SWITCHORDER':
            a = stack.pop(); b = stack.pop()
            stack.push(a); stack.push(b)

        # --- Arithmetic ---
        elif opcode == 'COMBO':
            a = stack.pop(); b = stack.pop()
            stack.push(b + a)

        elif opcode == 'NOPICKLE':
            a = stack.pop(); b = stack.pop()
            stack.push(b - a)

        elif opcode == 'EXTRAEXTRA':
            a = stack.pop(); b = stack.pop()
            stack.push(b * a)

        elif opcode == 'FLIPNUM':
            stack.push(-stack.pop())

        # --- Input ---
        elif opcode == 'ORDER':
            stack.push(int(input()))

        elif opcode == 'CUSTOMORDER':
            line = input()
            for ch in reversed(line):
                stack.push(ord(ch))
            stack.push(len(line))

        # --- Output ---
        elif opcode == 'ANNOUNCE':
            print(program[pc], end=''); pc += 1

        elif opcode == 'CALLOUT':
            print(chr(stack.pop()), end='')

        elif opcode == 'RECEIPT':
            print(stack.pop(), end='')

        elif opcode == 'PEEKRECEIPT':
            print(stack.top(), end='')

        elif opcode == 'LINEBREAK':
            print()

        # --- Control flow ---
        elif opcode == 'GOTO':
            label = program[pc]
            pc = labels[label]

        elif opcode == 'IFEMPTY':
            label = program[pc]; pc += 1
            if stack.top() == 0:
                pc = labels[label]

        elif opcode == 'IFMORE':
            label = program[pc]; pc += 1
            if stack.top() > 0:
                pc = labels[label]

        elif opcode == 'IFLESS':
            label = program[pc]; pc += 1
            if stack.top() < 0:
                pc = labels[label]

        # --- String helpers ---
        elif opcode == 'FLIPORDER':
            n = stack.pop()
            chars = [stack.pop() for _ in range(n)]
            for ch in chars:
                stack.push(ch)
            stack.push(n)

        elif opcode == 'DOUBLECUP':
            n = stack.pop()
            items = [stack.pop() for _ in range(n)]
            for item in reversed(items):
                stack.push(item)
            stack.push(n)
            for item in reversed(items):
                stack.push(item)
            stack.push(n)

        elif opcode == 'SAMETHING':
            n_a = stack.pop()
            chars_a = [stack.pop() for _ in range(n_a)]
            n_b = stack.pop()
            chars_b = [stack.pop() for _ in range(n_b)]
            stack.push(1 if chars_a == chars_b else 0)

        else:
            raise RuntimeError(f"Unknown instruction: '{opcode}' — not on the menu!")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 emrys.py <program.emrys>")
        sys.exit(1)

    filepath = sys.argv[1]
    with open(filepath, 'r') as f:
        lines = f.readlines()

    program, labels = parse(lines)
    execute(program, labels)


if __name__ == '__main__':
    main()
