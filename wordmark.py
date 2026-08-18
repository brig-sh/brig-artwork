"""Outline a short lowercase wordmark from Avenir Next Demi Bold into SVG path data."""
import sys
from fontTools.ttLib import TTCollection
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.misc.transform import Transform

FONT = '/System/Library/Fonts/Avenir Next.ttc'
FACE = 2  # Demi Bold


def outline(text, size, tracking=0.0, x0=0.0, y_baseline=0.0):
    f = TTCollection(FONT).fonts[FACE]
    upem = f['head'].unitsPerEm
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    hmtx = f['hmtx']
    s = size / upem
    pen_out = SVGPathPen(gs)
    x = x0
    for ch in text:
        gname = cmap[ord(ch)]
        # flip Y (font space is up-positive, SVG is down-positive)
        t = Transform(s, 0, 0, -s, x, y_baseline)
        rec = RecordingPen()
        gs[gname].draw(rec)
        tp = TransformPen(pen_out, t)
        rec.replay(tp)
        x += hmtx[gname][0] * s + tracking
    return pen_out.getCommands(), x - tracking - x0


if __name__ == '__main__':
    text = sys.argv[1] if len(sys.argv) > 1 else 'brig'
    size = float(sys.argv[2]) if len(sys.argv) > 2 else 100.0
    trk = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
    d, w = outline(text, size, trk)
    print('WIDTH', round(w, 2))
    print(d)
