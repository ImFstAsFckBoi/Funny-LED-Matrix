from dataclasses import dataclass
line_t = str
symbol_data_t = list[line_t]


@dataclass
class symbol_t():
    width: int
    height: int
    data: symbol_data_t


font_t = dict[str, symbol_t]
