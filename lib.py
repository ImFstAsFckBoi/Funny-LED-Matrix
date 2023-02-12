"""Library for printing scrolling text to a LED matrix
"""

from drivers.max7219cng import max7219cng
from font import get_symbol_line, get_symbol
from font.types import font_t
from font.basic import basic_font
from time import sleep

# Escape Sequence Renaming Table
# Uses only numbers in Unicode's 'Private Use Areas'
# https://en.wikipedia.org/wiki/Private_Use_Areas#Assignment
__ESRT: dict[int, str] = {}
__PUA_LOWER = 0xE000
__PUA_UPPER = 0xF8FF
__ESRT_COUNTER = __PUA_LOWER


class EscapeError(Exception):
    ...


def __replace_escape_sequence(msg: str, idx: int) -> str:
    global __ESRT_COUNTER
    rev_sequence = ''

    for i in reversed(msg[:idx]):
        if i == '\\':
            break

        rev_sequence += i
    else:
        raise EscapeError(f'Escape sequence at index {idx} is never closed.')

    if len(rev_sequence) == 0:
        return msg[:idx] + msg[idx + 1:]

    sequence = rev_sequence[::-1]

    msg = msg.replace(f'\\{sequence}\\', chr(__ESRT_COUNTER))
    __ESRT[__ESRT_COUNTER] = sequence
    __ESRT_COUNTER += 1
    return msg


def __preprocess_escape_sequences(msg: str) -> str:
    while True:
        idx = len(msg) - 1

        while idx >= 0:
            if msg[idx] == '\\':
                msg = __replace_escape_sequence(msg, idx)
                if idx < len(msg) and msg[idx - 1] == '\\':
                    idx -= 1
                else:
                    break
            idx -= 1
        else:
            break

    return msg


def __escape_char(char: str) -> str:
    if ord(char) >= __PUA_LOWER and ord(char) <= __PUA_UPPER:  # noqa
        return f'__{__ESRT[ord(char)]}__'

    return char


def __remove_rename(code: int) -> None:
    global __ESRT_COUNTER
    if code != __ESRT_COUNTER:
        raise EscapeError('Escape character was handled incorrectly')

    __ESRT_COUNTER -= 1


def __preprocess_slice_message(msg: str,
                               font: font_t = basic_font
                               ) -> list[tuple[str, int]]:

    """Convert a string into a sequence of tuples containing
    (<character>, <line of character>) to be used as print instruction.

    Args:
        `msg` (str): String to convert.
        `font` (font_t, optional): The font to use. Default to basic
    Returns:
        list[tuple[str, int]]: Sequence of print instructions.
    """
    msg_layout: list[tuple[str, int]] = []

    for char in msg:
        for idx in range(1, get_symbol(__escape_char(char), font).width + 1):
            msg_layout.append((char, idx))

        msg_layout.append((' ', 1))

    return msg_layout


def print2matrix(msg: str, matrix: max7219cng,
                 font: font_t = basic_font,
                 sleep_time: float = 0.1,
                 lpadding: int = 2,
                 rpadding: int = 2):
    """Print scrolling text to max7219cng LED matrix.

    Args:
        `msg` (str): String to print.
        `matrix` (max7219cng): Driver object to print to.
        `font` (font_t, optional): The font to use. Default to basic
        `sleep_time` (float, optional): Sleeping time between instructions,
        Lower = Faster. Defaults to 0.1.
        `lpadding` (int, optional): Space padding before message,
        Defaults to 3.
        `rpadding` (int, optional): Space padding after message,
        Defaults to 3.
    """

    msg = f'{" " * lpadding}{msg}{" " * rpadding}'

    try:
        msg = __preprocess_escape_sequences(msg)
    except EscapeError:
        print('Incorrectly formatted sequence')
        return

    layout = __preprocess_slice_message(msg, font)

    for msg_line in range(len(layout) - 8):
        for matrix_line in range(8):
            char, line = layout[msg_line + matrix_line]

            char = __escape_char(char)
            matrix.write(get_symbol_line(char, line, matrix_line + 1, font))
        sleep(sleep_time)

    for i in range(__ESRT_COUNTER - 1, __PUA_LOWER, -1):
        __remove_rename(i)
