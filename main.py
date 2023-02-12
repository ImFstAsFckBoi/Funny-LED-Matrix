#!/usr/bin/env python3

from drivers.max7219cng import max7219cng
from lib import print2matrix
from font.basic import basic_font

if __name__ == '__main__':
    try:
        matrix = max7219cng(clk=16, cs=20, mosi=21)

        mode = 0
        while True:
            try:
                mode = int(input('1: Run) 2: Contiguous) 3: Test) 4: Quit)\n> ')) # noqa
            except ValueError:
                continue
            if mode == 1:
                print2matrix(input('Your message: '), matrix, font=basic_font)
                break
            elif mode == 2:
                msg = input('Your message: ')
                print('Ctrl + C to stop')
                while True:
                    print2matrix(msg, matrix, font=basic_font)
            elif mode == 3:
                matrix.test(3)
                break
            elif mode == 4:
                break

    except KeyboardInterrupt:
        pass
