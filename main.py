#!/usr/bin/env python3

from drivers.max7219cng import max7219cng
from font import get_symbol_line
from time import sleep

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"


def msg_slice(msg: str, n: int) -> tuple[str, int]:
    idx = 0
    while n > 6:
        n = n - 6
        idx += 1

    return (msg[idx], n)


def main(conn: max7219cng):
    msg = f' {input("Your Message: ")} '
    for msg_line in range(6 * (len(msg) - 1)):
        for matrix_line in range(1, 8):
            a = msg_slice(msg, msg_line + matrix_line)
            conn.write(get_symbol_line(a[0], a[1], matrix_line))
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
