"""Generate the brig / hull logo family."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wordmark import outline

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'svg')
os.makedirs(OUT, exist_ok=True)

NAVY = '#0E2233'
DEEP = '#071521'
PAPER = '#F2EFE6'
BRASS = '#E7A33E'
BRASS_DEEP = '#B9761C'

# --- mark geometry, on a 256 grid, centred at (128,128) -----------------
R_RING = 84          # ring centreline
W_RING = 22          # ring stroke
R_IN = 72            # porthole glass
RIVET_R = 6
RIVET_ORBIT = 84

RIVETS = [(128 + RIVET_ORBIT * c, 128 + RIVET_ORBIT * s) for c, s in [
    (1, 0), (0.7071, 0.7071), (0, 1), (-0.7071, 0.7071),
    (-1, 0), (-0.7071, -0.7071), (0, -1), (0.7071, -0.7071)]]

WAVES = ('M46 132 C72 132 78 112 104 112 C130 112 138 132 164 132 '
         'C186 132 196 118 214 116')
WAVES2 = ('M46 178 C72 178 78 158 104 158 C130 158 138 178 164 178 '
          'C186 178 196 164 214 162')


def mark(uid, kind='brig', ring=PAPER, glass=DEEP, bars=BRASS, rivet=NAVY,
         glass_fill=True):
    """The porthole. kind='brig' -> bars; kind='hull' -> open water."""
    p = []
    p.append(f'<defs><clipPath id="{uid}-in">'
             f'<circle cx="128" cy="128" r="{R_IN - 2}"/></clipPath></defs>')
    if glass_fill:
        p.append(f'<circle cx="128" cy="128" r="{R_IN}" fill="{glass}"/>')
    if kind == 'brig':
        p.append(f'<g clip-path="url(#{uid}-in)" fill="{bars}">')
        for x in (73, 117, 161):
            p.append(f'<rect x="{x}" y="40" width="22" height="176" rx="11"/>')
        p.append('</g>')
    else:
        p.append(f'<g clip-path="url(#{uid}-in)" fill="none" stroke="{bars}" '
                 f'stroke-width="20" stroke-linecap="round">')
        p.append(f'<path d="{WAVES}"/><path d="{WAVES2}"/>')
        p.append('</g>')
    p.append(f'<circle cx="128" cy="128" r="{R_RING}" fill="none" '
             f'stroke="{ring}" stroke-width="{W_RING}"/>')
    p.append(f'<g fill="{rivet}">')
    for cx, cy in RIVETS:
        p.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{RIVET_R}"/>')
    p.append('</g>')
    return '\n  '.join(p)


def write(name, body, w, h, label):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
           f'width="{w}" height="{h}" role="img" aria-label="{label}">\n'
           f'  <title>{label}</title>\n  {body}\n</svg>\n')
    with open(os.path.join(OUT, name), 'w') as f:
        f.write(svg)
    print('wrote', name)


# --- 1. square avatars (the GitHub org / repo picture) ------------------
for kind, nm in (('brig', 'brig'), ('hull', 'hull')):
    body = (f'<rect width="256" height="256" fill="{NAVY}"/>\n  '
            + mark(f'{nm}-av', kind))
    write(f'{nm}-avatar.svg', body, 256, 256, nm)

# --- 2. standalone marks, transparent, for dark and light backgrounds ---
for kind, nm in (('brig', 'brig'), ('hull', 'hull')):
    write(f'{nm}-mark-on-dark.svg', mark(f'{nm}-d', kind), 256, 256, nm)
    write(f'{nm}-mark-on-light.svg',
          mark(f'{nm}-l', kind, ring=NAVY, glass='#FFFFFF', bars=BRASS_DEEP,
               rivet=PAPER),
          256, 256, nm)


# --- 3. horizontal lockups ---------------------------------------------
def lockup(name, text, kind, ring, ink, bars, rivet, glass, bg=None):
    MH = 128.0                 # mark box height
    S = 92.0                   # wordmark size
    TRK = 1.0
    GAP = 28.0
    PAD = 20.0
    d, wd = outline(text, S, TRK, x0=0, y_baseline=0)
    asc, desc = 0.756 * S, 0.21 * S
    baseline = PAD + MH / 2 + (asc - desc) / 2
    tx = PAD + MH + GAP
    W = tx + wd + PAD
    H = MH + 2 * PAD
    scale = MH / 256.0
    body = []
    if bg:
        body.append(f'<rect width="{W:.0f}" height="{H:.0f}" fill="{bg}"/>')
    body.append(f'<g transform="translate({PAD},{PAD}) scale({scale:.6f})">'
                f'{mark(name, kind, ring=ring, glass=glass, bars=bars, rivet=rivet)}</g>')
    body.append(f'<g transform="translate({tx:.1f},{baseline:.1f})">'
                f'<path d="{d}" fill="{ink}"/></g>')
    write(f'{name}.svg', '\n  '.join(body), round(W), round(H), text)


lockup('brig-lockup-on-dark', 'brig', 'brig', PAPER, PAPER, BRASS, NAVY, DEEP)
lockup('brig-lockup-on-light', 'brig', 'brig', NAVY, NAVY, BRASS_DEEP, PAPER, '#FFFFFF',
       bg=None)
lockup('brig-lockup-badge', 'brig', 'brig', PAPER, PAPER, BRASS, NAVY, DEEP, bg=NAVY)
lockup('hull-lockup-on-dark', 'hull', 'hull', PAPER, PAPER, BRASS, NAVY, DEEP)
lockup('hull-lockup-on-light', 'hull', 'hull', NAVY, NAVY, BRASS_DEEP, PAPER, '#FFFFFF')
