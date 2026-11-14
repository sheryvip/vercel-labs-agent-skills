#!/usr/bin/env python3
"""Build the website logo files from brand/logo-2026-source.png (mark + "SANA" on white).

  python3 brand/make-logo.py

Outputs (site/): assets/logo.png (light pages), assets/logo-light.png (dark pages),
assets/mark.png (hero), favicon.png, apple-touch-icon.png.
If you get the original logo file (PNG/SVG with transparency), replace the source and re-run.
"""
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "..", "site")
src = Image.open(os.path.join(HERE, "logo-2026-source.png")).convert("RGB")
W, H = src.size
MARK_RIGHT = 300          # x where the round mark ends in the source
WORD_BOX = (330, 60, W, 180)  # "SANA" only; the tagline line is left out


def unmix(img):
    """White background -> transparent, keeping anti-aliased edges."""
    out = Image.new("RGBA", img.size)
    p, o = img.load(), out.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            c = p[x, y]
            a = max(0.0, min(1.0, (max(255 - v for v in c) - 8) / 120))
            if a <= 0:
                o[x, y] = (0, 0, 0, 0)
                continue
            o[x, y] = tuple(max(0, min(255, round((c[i] - (1 - a) * 255) / a))) for i in range(3)) + (round(a * 255),)
    return out


# Round mark: the white "S" touches the outside, so it turns transparent too.
# Fill the S back with white using a morphological closing of the mark's shape
# (it bridges the narrow S gaps but leaves the outer outline where it is), so the S
# stays white on any background with no white rim.
import numpy as np
from PIL import ImageFilter


def convex_hull(points):
    """Andrew's monotone chain; points = list of (x, y)."""
    pts = sorted(set(points))
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


m = unmix(src.crop((0, 0, MARK_RIGHT, H)))
m = m.crop(m.getbbox())
w, h = m.size
PAD = 40
S = max(w, h) + 2 * PAD
ox, oy = (S - w) // 2, (S - h) // 2
layer = Image.new("RGBA", (S, S))
layer.paste(m, (ox, oy), m)
solid = np.array(layer.getchannel("A")) > 100
ys, xs = np.nonzero(solid)
hull = convex_hull(list(zip(xs.tolist(), ys.tolist())))
k = 4  # supersample for a smooth edge
big = Image.new("L", (S * k, S * k), 0)
ImageDraw.Draw(big).polygon([(x * k + k / 2, y * k + k / 2) for x, y in hull], fill=255)
fill = big.resize((S, S), Image.LANCZOS).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(0.6))  # ~2px inside the edge
white = Image.new("RGBA", (S, S), (255, 255, 255, 0))
white.putalpha(fill)
mark = Image.alpha_composite(white, layer)
mark = mark.crop(mark.getbbox())
side = max(mark.size)
sq = Image.new("RGBA", (side, side))
sq.paste(mark, ((side - mark.size[0]) // 2, (side - mark.size[1]) // 2), mark)
mark = sq

word = unmix(src.crop(WORD_BOX))
word = word.crop(word.getbbox())
word_light = word.copy()
px = word_light.load()
for y in range(word_light.size[1]):
    for x in range(word_light.size[0]):
        if px[x, y][3]:
            px[x, y] = (236, 226, 255, px[x, y][3])


def lockup(wordmark):
    mh = 200
    mk = mark.resize((mh, mh), Image.LANCZOS)
    wh = round(mh * 0.42)
    ww = round(wordmark.size[0] * wh / wordmark.size[1])
    wd = wordmark.resize((ww, wh), Image.LANCZOS)
    gap = round(mh * 0.18)
    out = Image.new("RGBA", (mh + gap + ww, mh))
    out.paste(mk, (0, 0), mk)
    out.paste(wd, (mh + gap, (mh - wh) // 2), wd)
    return out


lockup(word).save(os.path.join(SITE, "assets", "logo.png"), optimize=True)
lockup(word_light).save(os.path.join(SITE, "assets", "logo-light.png"), optimize=True)
mark.resize((520, 520), Image.LANCZOS).save(os.path.join(SITE, "assets", "mark.png"), optimize=True)
mark.resize((180, 180), Image.LANCZOS).save(os.path.join(SITE, "apple-touch-icon.png"))
mark.resize((64, 64), Image.LANCZOS).save(os.path.join(SITE, "favicon.png"))
mark.save(os.path.join(HERE, "mark-2026.png"))
print("logo files written; mark", mark.size)
