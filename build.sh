#!/bin/bash
# Regenerate every brig/hull mark from source. Needs rsvg-convert (brew install librsvg).
set -euo pipefail
cd "$(dirname "$0")"
python3 gen.py
mkdir -p png
for s in 1024 512 256 128 64; do rsvg-convert -w $s -h $s svg/brig-avatar.svg -o png/brig-avatar-$s.png; done
for s in 512 256; do rsvg-convert -w $s -h $s svg/hull-avatar.svg -o png/hull-avatar-$s.png; done
for f in brig-lockup-on-dark brig-lockup-on-light brig-lockup-badge hull-lockup-on-dark hull-lockup-on-light; do
  rsvg-convert -h 240 "svg/$f.svg" -o "png/$f@2x.png"
done
for f in brig-mark-on-dark brig-mark-on-light hull-mark-on-dark hull-mark-on-light; do
  rsvg-convert -w 512 -h 512 "svg/$f.svg" -o "png/$f-512.png"
done
python3 page.py
echo "regenerated $(ls svg/*.svg | wc -l | tr -d ' ') SVGs and $(ls png/*.png | wc -l | tr -d ' ') PNGs"
