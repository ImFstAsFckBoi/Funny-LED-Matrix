# Scrolling-LED-Matrix-text
Display scrolling text on an [MAX7219CNG](https://www.electrokit.com/en/product/led-module-8x8-serial/) 8x8 LED Matrix using Raspberry-Pi GPIO pins

![Demo gif](./demo.gif)

## Install and run (only tested on Python 3.9+):

```cmd
git clone https://github.com/ImFstAsFckBoi/Scrolling-LED-Matrix-text.git
cd Scrolling-LED-Matrix-text
pip install -r requirements.txt
python3 ./main.py
```

## Font
Most ASCII characters, as well as Å Ä Ö, is supported by the basic font. Any unsupported character you need can be added with the following code added to the list of symbols in the font file, by default this is [basic.py](./font/basic.py). 
<br>
<br>
**!!! IMPORTANT** The 8x8 bitmap is rotated 90 degrees to the right. See below how the character **`A`** would look like
```
"<custom character>": symbol_t(<width>, <height>, [
        "11111100",
        "00010010",
        "00010010",
        "00010010",
        "11111100",
        "00000000",
        "00000000",
        "00000000"
    ])
```

You can also use your own font by first making your own (use basic as a reference).
Then change the font argument on line 18 and 24 in [main.py](./main.py).
Make sure to implement `__DEFAULT__` as this is the fallback symbol if you use an unsupported character.

### Escape sequences:
By inputting `\name\` you can print custom symbols which does not correspond to one character but to one or more words. The basic font comes with:
- `\heart\`
- `\smile\`
- `\star\`

You can add your own in the same way as previously described for single characters but instead with two leading and trailing underscores in the name like this:
```
"__<custom name>__": symbol_t(<width>, <height>, [
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000"
    ])
```

