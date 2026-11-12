"""Generate the brig / hull wordmark family from the glyph table in pixel.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pixel

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'svg')
os.makedirs(OUT, exist_ok=True)

NAVY = '#0E2233'
PAPER = '#F2EFE6'
BRASS = '#E7A33E'

UNIT = 16          # px per grid unit in the generated files
CLEAR = 4          # clear space, in units, baked into the badge
AVATAR_BOX = 12    # avatar side, in units


def write(name, body, w, h, label):
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
           'width="%d" height="%d" role="img" aria-label="%s" '
           'shape-rendering="crispEdges">\n'
           '  <title>%s</title>\n  %s\n</svg>\n'
           % (w, h, w, h, label, label, body))
    with open(os.path.join(OUT, name), 'w') as f:
        f.write(svg)
    print('wrote %-28s %4d x %4d' % (name, w, h))


def lockup(name, text, ink, bg=None):
    pad = CLEAR * UNIT if bg else 0
    d, w, h = pixel.wordmark(text, UNIT, pad)
    body = []
    if bg:
        body.append('<rect width="%d" height="%d" fill="%s"/>' % (w, h, bg))
    body.append('<path d="%s" fill="%s"/>' % (d, ink))
    write('%s.svg' % name, '\n  '.join(body), w, h, text)


def square(name, text, ink, bg=None):
    """One glyph in a square box: the avatar, and the mark on its own."""
    d, side = pixel.glyph_square(text[0], UNIT, AVATAR_BOX)
    body = []
    if bg:
        body.append('<rect width="%d" height="%d" fill="%s"/>' % (side, side, bg))
    body.append('<path d="%s" fill="%s"/>' % (d, ink))
    write('%s.svg' % name, '\n  '.join(body), side, side, text)


for name in ('brig', 'hull'):
    # The avatar, and the same glyph with the field taken away.
    square('%s-avatar' % name, name, BRASS, NAVY)
    square('%s-mark-on-dark' % name, name, PAPER)
    square('%s-mark-on-light' % name, name, NAVY)

    # The wordmark, transparent, for README headers via <picture>.
    lockup('%s-lockup-on-dark' % name, name, PAPER)
    lockup('%s-lockup-on-light' % name, name, NAVY)

# One badge, for slides and anywhere the background is out of our hands.
lockup('brig-lockup-badge', 'brig', PAPER, bg=NAVY)
