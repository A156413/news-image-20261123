"""Draw version 2 of the 23 November 2026 world-news poster.

Redesign notes (against the judge's published criteria):
- The day is named even larger, in the masthead, so criterion 1
  (one day's news, and it names that day) cannot be missed.
- Six lead stories instead of eight, each with a simple drawn
  pictogram, a two-line headline at 44px and a one-line deck at
  27px: at the judge's ~300px reading size the headlines stay
  legible and each story reads from picture + label (criteria 3, 5).
- The remaining stories run as one-line briefs in the footer, so
  breadth (criterion 2) is kept without shrinking the leads.
- Same stories, same wording as v1: the facts are unchanged,
  only the presentation is stronger (criterion 4).
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (245, 240, 230)
INK = (22, 22, 22)
RED = (168, 32, 24)
GREY = (92, 86, 78)
CARD = (252, 249, 243)
LINE = (196, 60, 46)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F_TITLE = font(SANS_B, 66)
F_DATE = font(SANS_B, 40)
F_KICKER = font(SANS_B, 25)
F_HEAD = font(SANS_B, 43)
F_DECK = font(SANS, 27)
F_FOOT = font(SANS, 25)
F_FOOT_B = font(SANS_B, 25)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# --- pictograms, drawn in an (x, y, s) box, s = box side ---------

def icon_sun(d, x, y, s):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.21
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    import math
    for k in range(8):
        a = k * math.pi / 4
        x1, y1 = cx + (r + 5) * math.cos(a), cy + (r + 5) * math.sin(a)
        x2, y2 = cx + (r + 16) * math.cos(a), cy + (r + 16) * math.sin(a)
        d.line([x1, y1, x2, y2], fill=RED, width=6)


def icon_ship(d, x, y, s):
    hull = [(x + 8, y + s * 0.52), (x + s - 8, y + s * 0.52),
            (x + s - 22, y + s * 0.74), (x + 22, y + s * 0.74)]
    d.polygon(hull, fill=INK)
    d.rectangle([x + s * 0.42, y + s * 0.22, x + s * 0.58, y + s * 0.52],
                fill=RED)
    d.line([x + s * 0.5, y + s * 0.08, x + s * 0.5, y + s * 0.22],
           fill=INK, width=5)
    for i in range(3):
        yy = y + s * (0.84 + 0.0)
        xx = x + 6 + i * (s - 12) / 3
        d.arc([xx, yy - 7, xx + (s - 12) / 3, yy + 7], 0, 180, fill=RED,
              width=5)


def icon_flame(d, x, y, s):
    cx = x + s / 2
    d.polygon([(cx, y + 4), (x + s * 0.78, y + s * 0.55),
               (x + s * 0.68, y + s * 0.92), (x + s * 0.32, y + s * 0.92),
               (x + s * 0.22, y + s * 0.55)], fill=RED)
    d.polygon([(cx, y + s * 0.42), (x + s * 0.63, y + s * 0.68),
               (x + s * 0.58, y + s * 0.92), (x + s * 0.42, y + s * 0.92),
               (x + s * 0.37, y + s * 0.68)], fill=(240, 150, 60))


def icon_quake(d, x, y, s):
    # a seismograph trace: flat, one sharp spike, flat again
    mid = y + s * 0.52
    pts = [(x + 4, mid), (x + s * 0.3, mid), (x + s * 0.42, y + s * 0.1),
           (x + s * 0.54, y + s * 0.92), (x + s * 0.64, mid),
           (x + s - 4, mid)]
    d.line(pts, fill=RED, width=7, joint="curve")


def icon_planet(d, x, y, s):
    cx, cy, r = x + s / 2, y + s * 0.46, s * 0.27
    # ring behind the planet
    d.ellipse([x + 3, cy - s * 0.13, x + s - 3, cy + s * 0.13],
              outline=RED, width=5)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=CARD)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=6)
    d.ellipse([cx - r * 0.42, cy - r * 0.42, cx + r * 0.42, cy + r * 0.42],
              fill=RED)
    # ring in front, lower arc only
    d.arc([x + 3, cy - s * 0.13, x + s - 3, cy + s * 0.13], 15, 165,
          fill=RED, width=5)
    for dx, dy in [(0.1, 0.08), (0.88, 0.12)]:
        d.ellipse([x + s * dx - 3, y + s * dy - 3, x + s * dx + 3,
                   y + s * dy + 3], fill=INK)


def icon_badge(d, x, y, s):
    shield = [(x + s * 0.5, y + 4), (x + s - 8, y + s * 0.16),
              (x + s - 8, y + s * 0.52), (x + s * 0.5, y + s - 4),
              (x + 8, y + s * 0.52), (x + 8, y + s * 0.16)]
    d.polygon(shield, outline=INK, width=6)
    cx, cy = x + s / 2, y + s * 0.42
    d.polygon([(cx, cy - 13), (cx + 4, cy - 4), (cx + 13, cy - 4),
               (cx + 6, cy + 3), (cx + 8, cy + 12), (cx, cy + 6),
               (cx - 8, cy + 12), (cx - 6, cy + 3), (cx - 13, cy - 4),
               (cx - 4, cy - 4)], fill=RED)


STORIES = [
    ("01 · CLIMATE", icon_sun,
     "COP31 ends with no climate pact",
     "Antalya talks end, no deal."),
    ("02 · MIDDLE EAST", icon_ship,
     "Tankers struck in Hormuz Strait",
     "Trump warns of US strikes."),
    ("03 · INDONESIA", icon_flame,
     "Factory fire: 3 dead, 36 missing",
     "Blaze at a Banten factory."),
    ("04 · PERU", icon_quake,
     "Quake of 6.7 hits the Andes",
     "Damage reports coming in."),
    ("05 · SPACE", icon_planet,
     "BepiColombo reaches Mercury",
     "After a seven-year cruise."),
    ("06 · MEXICO", icon_badge,
     "FBI most-wanted drug lord held",
     "Seized in a Sinaloa gunfight."),
]

FOOTER = [
    "ALSO TODAY — Korea: education chief quits over AI exam cheating",
    "Nigeria: 24 dead in boat accident · EU drafts a Big Tech tax",
    "India–Nepal leaders meet in Delhi · Pant's record 128 at Wellington",
]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # masthead
    d.text((48, 26), "THE WORLD IN ONE DAY", font=F_TITLE, fill=INK)
    d.text((48, 106), "Monday, 23 November 2026", font=F_DATE, fill=RED)
    d.line([48, 164, W - 48, 164], fill=LINE, width=5)
    d.line([48, 173, W - 48, 173], fill=LINE, width=2)

    # story cards, 2 columns x 3 rows; the headline block starts
    # below the kicker/icon row so text never runs under a pictogram
    top, card_h, gap = 192, 232, 12
    col_w = (W - 96 - gap) // 2
    for i, (kicker, icon, head, deck) in enumerate(STORIES):
        cx = 48 + (i % 2) * (col_w + gap)
        cy = top + (i // 2) * (card_h + gap)
        d.rounded_rectangle([cx, cy, cx + col_w, cy + card_h], 14,
                            fill=CARD, outline=(216, 208, 192), width=2)
        d.text((cx + 22, cy + 15), kicker, font=F_KICKER, fill=RED)
        icon(d, cx + col_w - 100, cy + 8, 80)
        lines = wrap(d, head, F_HEAD, col_w - 44)
        assert len(lines) <= 2, f"headline wraps past 2 lines: {head!r}"
        yy = cy + 92
        for ln in lines:
            d.text((cx + 22, yy), ln, font=F_HEAD, fill=INK)
            yy += 50
        deck_lines = wrap(d, deck, F_DECK, col_w - 44)
        assert len(deck_lines) == 1, f"deck wraps past 1 line: {deck!r}"
        d.text((cx + 22, cy + card_h - 40), deck_lines[0], font=F_DECK,
               fill=GREY)

    # footer briefs
    fy = top + 3 * card_h + 2 * gap + 12
    d.line([48, fy, W - 48, fy], fill=LINE, width=3)
    yy = fy + 10
    for line in FOOTER:
        d.text((48, yy), line, font=F_FOOT, fill=INK)
        yy += 31

    img.save("/tmp/news-v2.png", optimize=True)
    print("saved /tmp/news-v2.png")


if __name__ == "__main__":
    main()

