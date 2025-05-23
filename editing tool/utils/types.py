from __future__ import annotations

import re
from fractions import Fraction


class CoerceError(Exception):
    pass


def split_num_str(val: str | float) -> tuple[float, str]:
    if isinstance(val, float | int):
        return val, ""

    index = 0
    for char in val:
        if char not in "0123456789_ .-":
            break
        index += 1
    num, unit = val[:index], val[index:]
    try:
        float(num)
    except ValueError:
        raise CoerceError(f"Invalid number: '{val}'")
    return float(num), unit


# Numbers: 0, 1, 2, 3, ...
def natural(val: str | float) -> int:
    num, unit = split_num_str(val)
    if unit != "":
        raise CoerceError(f"'{val}': Natural does not allow units.")
    if not isinstance(num, int) and not num.is_integer():
        raise CoerceError(f"'{val}': Natural must be a valid integer.")
    if num < 0:
        raise CoerceError(f"'{val}': Natural cannot be negative.")
    return int(num)


def number(val: str | float) -> float:
    if isinstance(val, str) and "/" in val:
        nd = val.split("/")
        if len(nd) != 2:
            raise CoerceError(f"'{val}': One divisor allowed.")
        vs = []
        for v in nd:
            try:
                vs.append(int(v))
            except ValueError:
                raise CoerceError(
                    f"'{val}': Numerator and Denominator must be integers."
                )
        if vs[1] == 0:
            raise CoerceError(f"'{val}': Denominator must not be zero.")
        return vs[0] / vs[1]

    num, unit = split_num_str(val)
    if unit == "%":
        return num / 100
    if unit == "":
        return num
    raise CoerceError(f"Unknown unit: '{unit}'")


def frame_rate(val: str) -> Fraction:
    if val == "ntsc":
        return Fraction(30000, 1001)
    if val == "ntsc_film":
        return Fraction(24000, 1001)
    if val == "pal":
        return Fraction(25)
    if val == "film":
        return Fraction(24)
    return Fraction(val)


def time(val: str, tb: Fraction) -> int:
    if ":" in val:
        boxes = val.split(":")
        if len(boxes) == 2:
            return round((int(boxes[0]) * 60 + float(boxes[1])) * tb)
        if len(boxes) == 3:
            return round(
                (int(boxes[0]) * 3600 + int(boxes[1]) * 60 + float(boxes[2])) * tb
            )
        raise CoerceError(f"'{val}': Invalid time format")

    num, unit = split_num_str(val)
    if unit in {"s", "sec", "secs", "second", "seconds"}:
        return round(num * tb)
    if unit in {"min", "mins", "minute", "minutes"}:
        return round(num * tb * 60)
    if unit == "hour":
        return round(num * tb * 3600)

    if unit != "":
        raise CoerceError(f"'{val}': Time format got unknown unit: `{unit}`")
    if not num.is_integer():
        raise CoerceError(f"'{val}': Time format expects: int?")
    return int(num)


def parse_color(val: str) -> str:
    """
    Convert a color str into an RGB tuple

    Accepts:
        - color names (black, red, blue)
        - 3 digit hex codes (#FFF, #3AE)
        - 6 digit hex codes (#3F0401, #005601)
    """

    color = val.lower()

    if color in colormap:
        color = colormap[color]

    if re.match("#[a-f0-9]{3}$", color):
        return "#" + "".join([x * 2 for x in color[1:]])

    if re.match("#[a-f0-9]{6}$", color):
        return color

    raise ValueError(f"Invalid Color: '{color}'")


colormap = {
    # Taken from https://www.w3.org/TR/css-color-4/#named-color
    "aliceblue": "#f0f8ff",
    "antiquewhite": "#faebd7",
    "aqua": "#00ffff",
    "aquamarine": "#7fffd4",
    "azure": "#f0ffff",
    "beige": "#f5f5dc",
    "bisque": "#ffe4c4",
    "black": "#000000",
    "blanchedalmond": "#ffebcd",
    "blue": "#0000ff",
    "blueviolet": "#8a2be2",
    "brown": "#a52a2a",
    "burlywood": "#deb887",
    "cadetblue": "#5f9ea0",
    "chartreuse": "#7fff00",
    "chocolate": "#d2691e",
    "coral": "#ff7f50",
    "cornflowerblue": "#6495ed",
    "cornsilk": "#fff8dc",
    "crimson": "#dc143c",
    "cyan": "#00ffff",
    "darkblue": "#00008b",
    "darkcyan": "#008b8b",
    "darkgoldenrod": "#b8860b",
    "darkgray": "#a9a9a9",
    "darkgrey": "#a9a9a9",
    "darkgreen": "#006400",
    "darkkhaki": "#bdb76b",
    "darkmagenta": "#8b008b",
    "darkolivegreen": "#556b2f",
    "darkorange": "#ff8c00",
    "darkorchid": "#9932cc",
    "darkred": "#8b0000",
    "darksalmon": "#e9967a",
    "darkseagreen": "#8fbc8f",
    "darkslateblue": "#483d8b",
    "darkslategray": "#2f4f4f",
    "darkslategrey": "#2f4f4f",
    "darkturquoise": "#00ced1",
    "darkviolet": "#9400d3",
    "deeppink": "#ff1493",
    "deepskyblue": "#00bfff",
    "dimgray": "#696969",
    "dimgrey": "#696969",
    "dodgerblue": "#1e90ff",
    "firebrick": "#b22222",
    "floralwhite": "#fffaf0",
    "forestgreen": "#228b22",
    "fuchsia": "#ff00ff",
    "gainsboro": "#dcdcdc",
    "ghostwhite": "#f8f8ff",
    "gold": "#ffd700",
    "goldenrod": "#daa520",
    "gray": "#808080",
    "grey": "#808080",
    "green": "#008000",
    "greenyellow": "#adff2f",
    "honeydew": "#f0fff0",
    "hotpink": "#ff69b4",
    "indianred": "#cd5c5c",
    "indigo": "#4b0082",
    "ivory": "#fffff0",
    "khaki": "#f0e68c",
    "lavender": "#e6e6fa",
    "lavenderblush": "#fff0f5",
    "lawngreen": "#7cfc00",
    "lemonchiffon": "#fffacd",
    "lightblue": "#add8e6",
    "lightcoral": "#f08080",
    "lightcyan": "#e0ffff",
    "lightgoldenrodyellow": "#fafad2",
    "lightgreen": "#90ee90",
    "lightgray": "#d3d3d3",
    "lightgrey": "#d3d3d3",
    "lightpink": "#ffb6c1",
    "lightsalmon": "#ffa07a",
    "lightseagreen": "#20b2aa",
    "lightskyblue": "#87cefa",
    "lightslategray": "#778899",
    "lightslategrey": "#778899",
    "lightsteelblue": "#b0c4de",
    "lightyellow": "#ffffe0",
    "lime": "#00ff00",
    "limegreen": "#32cd32",
    "linen": "#faf0e6",
    "magenta": "#ff00ff",
    "maroon": "#800000",
    "mediumaquamarine": "#66cdaa",
    "mediumblue": "#0000cd",
    "mediumorchid": "#ba55d3",
    "mediumpurple": "#9370db",
    "mediumseagreen": "#3cb371",
    "mediumslateblue": "#7b68ee",
    "mediumspringgreen": "#00fa9a",
    "mediumturquoise": "#48d1cc",
    "mediumvioletred": "#c71585",
    "midnightblue": "#191970",
    "mintcream": "#f5fffa",
    "mistyrose": "#ffe4e1",
    "moccasin": "#ffe4b5",
    "navajowhite": "#ffdead",
    "navy": "#000080",
    "oldlace": "#fdf5e6",
    "olive": "#808000",
    "olivedrab": "#6b8e23",
    "orange": "#ffa500",
    "orangered": "#ff4500",
    "orchid": "#da70d6",
    "palegoldenrod": "#eee8aa",
    "palegreen": "#98fb98",
    "paleturquoise": "#afeeee",
    "palevioletred": "#db7093",
    "papayawhip": "#ffefd5",
    "peachpuff": "#ffdab9",
    "peru": "#cd853f",
    "pink": "#ffc0cb",
    "plum": "#dda0dd",
    "powderblue": "#b0e0e6",
    "purple": "#800080",
    "rebeccapurple": "#663399",
    "red": "#ff0000",
    "rosybrown": "#bc8f8f",
    "royalblue": "#4169e1",
    "saddlebrown": "#8b4513",
    "salmon": "#fa8072",
    "sandybrown": "#f4a460",
    "seagreen": "#2e8b57",
    "seashell": "#fff5ee",
    "sienna": "#a0522d",
    "silver": "#c0c0c0",
    "skyblue": "#87ceeb",
    "slateblue": "#6a5acd",
    "slategray": "#708090",
    "slategrey": "#708090",
    "snow": "#fffafa",
    "springgreen": "#00ff7f",
    "steelblue": "#4682b4",
    "tan": "#d2b48c",
    "teal": "#008080",
    "thistle": "#d8bfd8",
    "tomato": "#ff6347",
    "turquoise": "#40e0d0",
    "violet": "#ee82ee",
    "wheat": "#f5deb3",
    "white": "#ffffff",
    "whitesmoke": "#f5f5f5",
    "yellow": "#ffff00",
    "yellowgreen": "#9acd32",
}
