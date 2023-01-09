#!/usr/bin/env python

import spi
from font import get_symbol_line
from time import sleep
# FONT: https://www.youtube.com/watch?v=gODVeG_qio8

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"


def msg_slice(msg: str, n: int) -> tuple[str, int]:
    idx = 0
    while n > 6:
        n = n - 6
        idx += 1

    return (msg[idx], n)


if __name__ == '__main__':
    # Initialize an SPI connection using BCM-mode pins 21, 20, and 16
    max7219 = spi.SPI(clk=21, cs=16, mosi=20, miso=None, verbose=True)

    # Zero out all registers
    for cmd in range(16):
        packet = cmd << 8
        max7219.put(packet, 12)

    input("WAIT")

    # Set the scan limit register to binary 7 to enable all columns.
    max7219.put(int("101100000111", 2), 12)

    # Disable shutdown register.
    max7219.put(int("110000000001", 2), 12)

    MSG = ' BALD '
    for i in range(6 * (len(MSG) - 1)):
        print(i)
        for line in range(1, 8):
            a = msg_slice(MSG, i + line)
            max7219.put(get_symbol_line(a[0], a[1], line), 12)
        sleep(0.2)

    try:
        input("Press return to continue")
    except:
        pass
