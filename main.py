#!/usr/bin/env python3

from drivers.max7219cng import max7219cng
from font import get_symbol_line, get_symbol
from time import sleep

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"

# Escape Sequence Renaming Table
ESRT: dict[int, str] = {}
PUA_LOWER = 0xE000
PUA_UPPER = 0xF8FF

# Uses only numbers in Unicode's 'Private Use Areas'
# https://en.wikipedia.org/wiki/Private_Use_Areas#Assignment

ESRT_COUNTER = PUA_LOWER


def replace_escape_sequence(msg: str, idx: int) -> str:
    global ESRT_COUNTER
    rev_sequence = ''

    for i in reversed(msg[:idx]):
        if i == '\\':
            break

        rev_sequence += i
    else:
        raise Exception(f'Escape rev_sequence at index {idx} is never closed.')

    if len(rev_sequence) == 0:
        return '\\'

    sequence = rev_sequence[::-1]

    msg = msg.replace(f'\\{sequence}\\', chr(ESRT_COUNTER))
    ESRT[ESRT_COUNTER] = sequence
    ESRT_COUNTER += 1
    return msg


def preprocess_escape_sequences(msg: str) -> str:
    while True:
        for idx in range(len(msg) - 1, 0, -1):
            if msg[idx] == '\\':
                msg = replace_escape_sequence(msg, idx)
                break
        else:
            break

    return msg


def escape_char(char: str) -> str:
    if ord(char) >= PUA_LOWER and ord(char) <= PUA_UPPER:  # noqa
        return f'__{ESRT[ord(char)]}__'

    return char


def remove_rename(code: int) -> None:
    global ESRT_COUNTER
    if code != ESRT_COUNTER:
        raise Exception('Escape sequence were handled incorrectly')

    ESRT_COUNTER -= 1


def preprocess_slice_message(msg: str) -> list[tuple[str, int]]:
    msg_layout: list[tuple[str, int]] = []

    for char in msg:
        for idx in range(1, get_symbol(escape_char(char)).width + 1):
            msg_layout.append((char, idx))

        msg_layout.append((' ', 1))

    return msg_layout


def main(conn: max7219cng):
    msg = f'   {input("Your Message: ")}   '
    msg = preprocess_escape_sequences(msg)
    layout = preprocess_slice_message(msg)
    for msg_line in range(len(layout) - 8):
        for matrix_line in range(8):
            c_l_tuple = layout[msg_line + matrix_line]

            char = escape_char(c_l_tuple[0])
            conn.write(get_symbol_line(char, c_l_tuple[1], matrix_line + 1))
        sleep(0.1)

    for i in range(ESRT_COUNTER - 1, PUA_LOWER, -1):
        remove_rename(i)


def test(conn: max7219cng):
    conn.test(3)


if __name__ == '__main__':
    try:
        matrix = max7219cng(clk=16, cs=20, mosi=21)

        r = 0
        while True:
            r = int(input("1: Run)  2: Test) 3: Quit)\n> "), 10)

            if r == 1:
                main(matrix)
                break
            elif r == 2:
                test(matrix)
                break
            elif r == 3:
                break

    except KeyboardInterrupt:
        pass
