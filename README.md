# brig / hull brand marks

The wordmark is the mark. There is no symbol.

The letters are drawn on a square grid with a two-unit stroke, which is the
shape of a terminal cell and the shape of a bar. `brig` and `hull` share the
grid, the stroke and the palette, so the relationship between them is the
drawing itself rather than a symbol they both carry. That means one file per
mark and nothing to keep in sync.

## Construction

Every stroke is two units. The x-height is five units, the ascender is eight,
and the descender drops three below the baseline. Letters are tracked two units
apart. The glyph table lives in `pixel.py`, in units, and `gen.py` scales it to
16 px per unit.

Scale by whole units only. A fractional unit puts a stroke on a half pixel and
the letters go soft, which is why the PNG sizes below are multiples of the grid
rather than round powers of two.

## Palette

| Role | Hex | Use |
| --- | --- | --- |
| Navy | `#0E2233` | Field, and the ink on light backgrounds |
| Deep | `#071521` | The darker field, for terminal blocks on the site |
| Paper | `#F2EFE6` | The ink on dark backgrounds |
| Brass | `#E7A33E` | The avatar glyph, and one accent per page |
| Brass deep | `#B9761C` | Brass on a light background, where the lighter brass fails contrast |

Brass because ships are brass; navy because it is the sea, not another
cloud-native blue.

## Files

| File | Use |
| --- | --- |
| `svg/brig-lockup-on-{dark,light}.svg` | The wordmark, transparent, for README headers via `<picture>`. |
| `svg/brig-lockup-badge.svg` | The wordmark on its own navy field, with clear space baked in, for slides and anywhere the background is out of our hands. |
| `svg/brig-avatar.svg`, `png/brig-avatar-*.png` | Org and repo avatar: the `b` on a full-bleed navy square, no baked corner radius, because GitHub rounds it. |
| `svg/brig-mark-on-{dark,light}.svg` | The same glyph with the field taken away, for a background you control. |
| `svg/hull-*.svg` | The same set for `hull`, built from the same grid. |

PNG exports live in `png/`. The 960 and 480 avatars are what GitHub wants for
the org picture; everything else is convenience.

## Rules

- Lowercase, always. There is no capital form.
- Clear space is four units on every side. The badge already carries it; the
  transparent files do not, so the page that places them owns it.
- The wordmark holds down to about 33 px tall. Below that the stroke falls
  under two device pixels and the counters close up. Use the avatar instead.
- One brass wordmark per page. Everything else is paper or navy.
- Never set the name in a typeface. If it is the name, it is the wordmark.

## Building

Everything here is generated. Edit `pixel.py` or `gen.py` and rebuild, never
the SVGs by hand.

```
./build.sh
```

That regenerates all 11 SVGs, all 16 PNGs and `identity.html`, a review page
with every asset inlined. The build is reproducible: from a clean tree it gives
back byte-identical files.

You need `rsvg-convert` (`brew install librsvg`) for the PNGs. The SVGs need
Python and nothing else. The marks carry no font dependency, because there is
no font: the letters are rectangles.

## Copies in the repos

`brig-sh/brig` and `brig-sh/hull` keep copies under `assets/`, so their READMEs
render without a cross-repo fetch. Those copies are byte-identical to the files
here, verified on 2026-09-10. If a mark changes, refresh them too.
