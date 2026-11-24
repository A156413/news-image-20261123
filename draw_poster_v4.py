"""Draw version 4 of the 23 November 2026 world-news poster.

Same eleven stories, same words as v3 (criteria 2 and 4); what
changes is the layout craft (criteria 3 and 5), fixing the three
faults the v3 render showed on inspection:

1. The lead banner becomes a real main visual: the COP31
   headline grows to 46px on one measured line, the sun
   pictogram grows to 104px and drops to the lower right so it
   never crowds the headline, and a red rule sets the deck off.
2. Story cards tighten up: the cards shrink from 246px to
   234px tall and the headlines start right under the
   pictogram row (v3 left a gap there), and the deck grey
   deepens from (92, 86, 78) to (70, 66, 60) so small type
   keeps contrast. The pictograms stay at 80px and the
   headlines at 43px: any larger, and a two-line headline
   either hits the pictogram or wraps to three lines.
3. The footer briefs leave the bottom edge: six briefs in a
   2-column x 3-row grid at 24px, each at most two lines, with
   a proper bottom margin. "ALSO TODAY" becomes a red label
   sitting on the divider rule instead of a text prefix, which
   is what pushed the Mexico brief to three lines in v3's
   full-width rows.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (245, 240, 230)
INK = (22, 22, 22)
RED = (168, 32, 24)
GREY = (92, 86, 78)
DECK_GREY = (70, 66, 60)
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
F_LEAD_DECK = font(SANS, 28)
F_BRIEF = font(SANS, 24)
F_LABEL = font(SANS_B, 20)


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


LEAD = ("01 · CLIMATE — THE DAY'S LEAD STORY", icon_sun,
        "COP31 ends with no climate pact",
        "No deal in Antalya; \u201cno ambiguity in the science\u201d.")

STORIES = [
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
]

# The six footer briefs, in v3's reading order, laid out as
# row pairs: (Mexico, Korea), (Nigeria, EU), (India-Nepal, Pant).
BRIEFS = [
    "Mexico: FBI most-wanted drug lord held in Sinaloa",
    "Korea: education chief quits over AI exam cheating",
    "Nigeria: 24 dead in boat accident",
    "EU drafts a Big Tech tax",
    "India–Nepal leaders meet in Delhi",
    "Pant's record 128 at Wellington",
]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # masthead, unchanged from v3
    d.text((48, 26), "THE WORLD IN ONE DAY", font=F_TITLE, fill=INK)
    d.text((48, 106), "Monday, 23 November 2026", font=F_DATE, fill=RED)
    d.line([48, 164, W - 48, 164], fill=LINE, width=5)
    d.line([48, 173, W - 48, 173], fill=LINE, width=2)

    # the lead banner: 196px tall, headline at 46px on one
    # measured line; the sun sits lower right, its top ray
    # clearing the headline's foot, and the deck runs under
    # a red rule
    lead_y, lead_h = 192, 196
    kicker, icon, head, deck = LEAD
    d.rounded_rectangle([48, lead_y, W - 48, lead_y + lead_h], 14,
                        fill=CARD, outline=(216, 208, 192), width=2)
    d.text((70, lead_y + 14), kicker, font=F_KICKER, fill=RED)
    F_LEAD = font(SANS_B, 46)
    head_lines = wrap(d, head, F_LEAD, W - 96 - 44)
    assert len(head_lines) == 1, "lead headline must stay on one line"
    d.text((70, lead_y + 46), head_lines[0], font=F_LEAD, fill=INK)
    icon(d, W - 48 - 22 - 104, lead_y + 88, 104)
    d.line([70, lead_y + 124, W - 48 - 22 - 104 - 18, lead_y + 124],
           fill=LINE, width=3)
    deck_lines = wrap(d, deck, F_LEAD_DECK,
                      W - 48 - 22 - 104 - 18 - 70)
    assert len(deck_lines) == 1, "lead deck must stay on one line"
    d.text((70, lead_y + 138), deck_lines[0], font=F_LEAD_DECK,
           fill=DECK_GREY)


    # story cards, 2 columns x 2 rows, 234px tall; the
    # headline starts right under the pictogram row so the
    # type fills the card instead of floating in it as in v3
    F_CARD = font(SANS_B, 43)
    top, card_h, gap = lead_y + lead_h + 12, 234, 12
    col_w = (W - 96 - gap) // 2
    for i, (kicker, icon, head, deck) in enumerate(STORIES):
        cx = 48 + (i % 2) * (col_w + gap)
        cy = top + (i // 2) * (card_h + gap)
        d.rounded_rectangle([cx, cy, cx + col_w, cy + card_h], 14,
                            fill=CARD, outline=(216, 208, 192), width=2)
        d.text((cx + 22, cy + 14), kicker, font=F_KICKER, fill=RED)
        icon(d, cx + col_w - 22 - 80, cy + 4, 80)
        lines = wrap(d, head, F_CARD, col_w - 44)
        assert len(lines) <= 2, f"headline wraps past 2 lines: {head!r}"
        yy = cy + 88
        for ln in lines:
            d.text((cx + 22, yy), ln, font=F_CARD, fill=INK)
            yy += 50
        deck_lines = wrap(d, deck, F_DECK, col_w - 44)
        assert len(deck_lines) == 1, f"deck wraps past 1 line: {deck!r}"
        d.text((cx + 22, cy + card_h - 36), deck_lines[0], font=F_DECK,
               fill=DECK_GREY)

    # footer briefs: "ALSO TODAY" as a red label on the divider,
    # then the six briefs in a 2 x 3 grid at 24px, each wrapped
    # to its column and at most two lines, bottom margin kept
    div_y = top + 2 * card_h + gap + 12
    d.text((48, div_y - 10), "ALSO TODAY", font=F_LABEL, fill=RED)
    d.line([216, div_y, W - 48, div_y], fill=LINE, width=3)
    col_x = [48, 524]
    col_w_b = 452
    yy = div_y + 12
    for r in range(3):
        row = []
        for c in range(2):
            lines = wrap(d, BRIEFS[r * 2 + c], F_BRIEF, col_w_b)
            assert len(lines) <= 2, f"brief wraps past 2 lines: {BRIEFS[r * 2 + c]!r}"
            row.append(lines)
        for c in range(2):
            for j, ln in enumerate(row[c]):
                d.text((col_x[c], yy + j * 25), ln, font=F_BRIEF,
                       fill=INK)
        yy += max(len(row[0]), len(row[1])) * 25
    assert yy <= H - 16, "briefs crowd the bottom margin"

    import os
    here = os.path.dirname(os.path.abspath(__file__))
    img.save(os.path.join(here, "entry.png"), optimize=True)
    img.save("/tmp/news-v4.png", optimize=True)
    print("saved entry.png and /tmp/news-v4.png")


if __name__ == "__main__":
    main()
