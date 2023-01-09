#!/usr/bin/env python3

from drivers.max7219cng import max7219cng
from font import get_symbol_line
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
    sequence = ''

    for i in msg[idx + 1:]:
        if i == '\\':
            break

        sequence += i
    else:
        raise Exception(f'Escape sequence at index {idx} is never closed.')

    msg = msg.replace(f'\\{sequence}\\', chr(ESRT_COUNTER))
    ESRT[ESRT_COUNTER] = sequence
    ESRT_COUNTER += 1
    return msg


def preprocess_escape_sequences(msg: str) -> str:
    while True:
        for idx in range(len(msg)):
            if msg[idx] == '\\':
                msg = replace_escape_sequence(msg, idx)
                break
        else:
            break
    
    return msg


def msg_slice(msg: str, n: int) -> tuple[str, int]:
    idx = 0
    while n > 6:
        n = n - 6
        idx += 1

    return (msg[idx], n)


def main(conn: max7219cng):
    msg = f' {input("Your Message: ")} '
    msg = preprocess_escape_sequences(msg)
    for msg_line in range(6 * (len(msg) - 1)):
        for matrix_line in range(1, 8):
            c_l_tuple = msg_slice(msg, msg_line + matrix_line)

            if ord(c_l_tuple[0]) >= PUA_LOWER and ord(c_l_tuple[0]) <= PUA_UPPER:  # noqa
                char = f'__{ESRT[ord(c_l_tuple[0])]}__'
            else:
                char = c_l_tuple[0]
            conn.write(get_symbol_line(char, c_l_tuple[1], matrix_line))
        sleep(0.2)


def test(conn: max7219cng):
    conn.test(3)


if __name__ == '__main__':
    try:
        matrix = max7219cng(clk=21, cs=16, mosi=20)

        r = 0
        while True:
            r = int(input("1: Run)  2: Test) 3: Quit)\n> "))

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
