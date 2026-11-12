#!/bin/bash
# Regenerate every brig/hull mark from source. Needs rsvg-convert (brew install librsvg).
set -euo pipefail
cd "$(dirname "$0")"
python3 gen.py
rm -rf png && mkdir -p png
# Avatar and mark rasters at whole multiples of the 12-unit grid, so no stroke
# ever lands on a half pixel.
for s in 960 480 240 120 60; do rsvg-convert -w $s -h $s svg/brig-avatar.svg -o png/brig-avatar-$s.png; done
for s in 480 240; do rsvg-convert -w $s -h $s svg/hull-avatar.svg -o png/hull-avatar-$s.png; done
for f in brig-mark-on-dark brig-mark-on-light hull-mark-on-dark hull-mark-on-light; do
  rsvg-convert -w 480 -h 480 "svg/$f.svg" -o "png/$f-480.png"
done
# Lockups at exactly twice the SVG, which is 32 px to the unit.
for f in brig-lockup-on-dark brig-lockup-on-light brig-lockup-badge hull-lockup-on-dark hull-lockup-on-light; do
  rsvg-convert -z 2 "svg/$f.svg" -o "png/$f@2x.png"
done
python3 page.py
echo "regenerated $(ls svg/*.svg | wc -l | tr -d ' ') SVGs and $(ls png/*.png | wc -l | tr -d ' ') PNGs"
