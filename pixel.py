"""The brig / hull pixel wordmark, drawn on a square grid.

Every stroke is two units. The x-height is five units, the ascender is eight,
and the descender drops three below the baseline. Letters are tracked two units
apart. Coordinates below are in units, with y growing downward and y=0 at the
ascender line, so the baseline sits at y=8.

Each glyph is a list of (x, y, w, h) rectangles plus its advance width. The
rectangles of one word are emitted as a single SVG path so that abutting
strokes share no seam when the file is rasterised at a fractional scale.
"""

STROKE = 2
X_HEIGHT = 5
ASCENDER = 8
DESCENDER = 3
TRACKING = 2
BODY = ASCENDER + DESCENDER   # 11 units, ascender line to descender line

# glyph -> (rectangles in units, advance width in units)
GLYPHS = {
    'b': ([(0, 0, 2, 8), (2, 3, 4, 2), (4, 3, 2, 5), (2, 6, 4, 2)], 6),
    'r': ([(0, 3, 2, 5), (2, 3, 3, 2)], 5),
    'i': ([(0, 0, 2, 2), (0, 3, 2, 5)], 2),
    'g': ([(0, 3, 6, 2), (0, 3, 2, 5), (4, 3, 2, 8),
           (0, 6, 6, 2), (0, 9, 6, 2)], 6),
    'h': ([(0, 0, 2, 8), (2, 3, 4, 2), (4, 3, 2, 5)], 6),
    'u': ([(0, 3, 2, 5), (4, 3, 2, 5), (0, 6, 6, 2)], 6),
    'l': ([(0, 0, 2, 8)], 2),
}


def rects(text):
    """Return (rectangles in units, width in units, height in units)."""
    out, x = [], 0
    for ch in text:
        if ch not in GLYPHS:
            raise KeyError(
                '%r has no glyph. Add it to GLYPHS in pixel.py, on the grid.'
                % ch)
        shapes, advance = GLYPHS[ch]
        out += [(x + rx, ry, rw, rh) for rx, ry, rw, rh in shapes]
        x += advance + TRACKING
    width = x - TRACKING
    height = max(ry + rh for _, ry, _, rh in out)
    return out, width, height


def path(shapes, unit=1, dx=0, dy=0):
    """One path, all subpaths wound the same way so nonzero fill unions them."""
    d = []
    for x, y, w, h in shapes:
        d.append('M%d %dh%dv%dh%dz' % (dx + x * unit, dy + y * unit,
                                       w * unit, h * unit, -w * unit))
    return ''.join(d)


def wordmark(text, unit, pad=0):
    """(path data, canvas width, canvas height) for a word, padded all round."""
    shapes, w, h = rects(text)
    return (path(shapes, unit, pad, pad),
            w * unit + 2 * pad, h * unit + 2 * pad)


def glyph_square(ch, unit, box=12):
    """(path data, side) for one glyph centred in a square box of `box` units.

    The b sits three units in from each side and two down from the top, which
    is what keeps it readable when GitHub renders the avatar at 16 px.
    """
    shapes, advance = GLYPHS[ch]
    side = box * unit
    dx = (box - advance) // 2 * unit
    dy = (box - ASCENDER) // 2 * unit
    return path(shapes, unit, dx, dy), side
