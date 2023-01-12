from font.basic import basic_font
from font.types import font_t, symbol_t
from typing import Union

__lazy_column_lut = {
    1: "0001",
    2: "0010",
    3: "0011",
    4: "0100",
    5: "0101",
    6: "0110",
    7: "0111",
    8: "1000"
}


def get_symbol(char: str, font: font_t = basic_font) -> symbol_t:
    """Wrapped font query that returns __DEFAULT__ symbol if 'char' not found.

    Args:
        char (str): Character to get.
        font (font_t, optional): Font use. Defaults to basic_font.
    """

    try:
        return font[char]
    except KeyError:
        # print(f'[INFO] Failed to get character {char}, defaulting')
        return font['__DEFAULT__']


def get_symbol_line(char: str,
                    char_line: int,
                    matrix_line: Union[int, None] = None,  # int | None = None, requires python3.10 # noqa
                    font: font_t = basic_font) -> int:

    """Get the matrix print command for one line in a symbol.

    Args:
        char (str): Character to get line from.
        char_line (int): Line in symbol (int 1 - 8).
        matrix_line (int | None, optional): Line in matrix int (1 - 8)
        None defaults to char_line.
        font (font_t, optional): Font to use. Defaults to basic.

    Raises:
        IndexError: Incorrect char_line range.

    Returns:
        int: 12 bit matrix print command.
    """

    if char_line < 1 or char_line > 8:
        raise IndexError

    if matrix_line is None:
        matrix_line = char_line

    cmd = __lazy_column_lut[matrix_line]
    cmd += get_symbol(char, font).data[char_line - 1]
    return int(cmd, 2)

