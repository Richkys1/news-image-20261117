#!/usr/bin/env python3
"""Draw the front page for Tuesday 17 November 2026 as one 1024x1024 PNG.

Every story below was reported on 17 November 2026. The script draws the
image with Pillow and the system DejaVu fonts, then writes entry.png.
Deterministic: the same script always writes the same bytes.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (251, 247, 236)      # warm newsprint
INK = (20, 33, 61)           # near-black navy
NAVY = (11, 37, 69)          # masthead band
RED = (180, 35, 24)          # kicker red
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
TINT = (232, 238, 244)       # icon panel tint
RULE = (180, 35, 24)
GREY = (90, 100, 114)
ORANGE = (214, 106, 24)
GOLD = (233, 196, 29)
STEEL = (70, 110, 150)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_DATE = font("DejaVuSans-Bold.ttf", 54)
F_KICK = font("DejaVuSans-Bold.ttf", 21)
F_LEAD_HEAD = font("DejaVuSans-Bold.ttf", 40)
F_LEAD_BODY = font("DejaVuSans.ttf", 24)
F_CELL_KICK = font("DejaVuSans-Bold.ttf", 16)
F_CELL_HEAD = font("DejaVuSans-Bold.ttf", 22)
F_CELL_BODY = font("DejaVuSans.ttf", 18)
F_FOOT = font("DejaVuSans.ttf", 15)
F_FOOT_B = font("DejaVuSans-Bold.ttf", 15)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    """Draw lines starting at (x, y); returns the y after the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, fill, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def starburst(draw, cx, cy, r_out, r_in, points, fill):
    """A spiky burst polygon centred on (cx, cy)."""
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def arrow(draw, x0, y0, x1, y1, fill, width=4):
    """A straight arrow from (x0, y0) to (x1, y1)."""
    draw.line([(x0, y0), (x1, y1)], fill=fill, width=width)
    ang = math.atan2(y1 - y0, x1 - x0)
    for da in (2.6, -2.6):
        draw.line(
            [(x1, y1),
             (x1 - 14 * math.cos(ang + da), y1 - 14 * math.sin(ang + da))],
            fill=fill, width=width)


# ---------------------------------------------------------------------------
# Icons: bold flat shapes drawn with Pillow primitives, one per story.
# Each takes a draw context and the top-left corner of a square panel.
# ---------------------------------------------------------------------------

def icon_radar_drone(draw, x, y, s):
    """Radar dish with a drone above it: Iran's drones at the US radar base."""
    # radar dish: a bowl with a sweeping beam
    draw.arc([x + 8, y + s - 62, x + s - 8, y + s + 18], 180, 360, fill=STEEL, width=7)
    draw.line([(x + s // 2, y + s - 22), (x + s // 2, y + s - 4)], fill=STEEL, width=7)
    draw.line([(x + 18, y + s - 4), (x + s - 18, y + s - 4)], fill=STEEL, width=7)
    draw.line([(x + s // 2, y + s - 22), (x + s - 26, y + s - 52)],
              fill=ORANGE, width=5)
    # drone: body, arms and four rotors
    cx, cy = x + s // 2, y + 34
    draw.ellipse([cx - 13, cy - 8, cx + 13, cy + 8], fill=INK)
    draw.line([(cx - 26, cy - 12), (cx + 26, cy - 12)], fill=INK, width=4)
    draw.line([(cx - 26, cy + 12), (cx + 26, cy + 12)], fill=INK, width=4)
    for rx in (cx - 30, cx + 30):
        draw.ellipse([rx - 13, cy - 18, rx + 13, cy - 6], outline=INK, width=3)
        draw.ellipse([rx - 13, cy + 6, rx + 13, cy + 18], outline=INK, width=3)
    draw.ellipse([cx - 4, cy - 3, cx + 4, cy + 3], fill=RED)


def icon_radiation(draw, x, y, s):
    """Warning triangle with a radiation trefoil: the dirty-bomb plot."""
    cx, cy = x + s // 2, y + s // 2 + 6
    tri = [(cx, y + 8), (x + s - 10, y + s - 10), (x + 10, y + s - 10)]
    draw.polygon(tri, fill=GOLD, outline=INK, width=4)
    # trefoil: three blades around a centre disc
    for ang in (90, 210, 330):
        a = math.radians(ang)
        bx, by = cx + 15 * math.cos(a), cy - 2 + 15 * math.sin(a)
        draw.pieslice([bx - 15, by - 15, bx + 15, by + 15],
                      ang - 55, ang + 55, fill=INK)
    draw.ellipse([cx - 6, cy - 8, cx + 6, cy + 4], fill=INK)


def icon_bridge(draw, x, y, s):
    """A bridge snapped in two with a blast burst at the break."""
    cy = y + s // 2 + 12
    # left deck and tower
    draw.rectangle([x + 8, cy, x + s // 2 - 14, cy + 10], fill=STEEL)
    draw.rectangle([x + 22, cy - 34, x + 30, cy], fill=STEEL)
    # right deck and tower
    draw.rectangle([x + s // 2 + 14, cy, x + s - 8, cy + 10], fill=STEEL)
    draw.rectangle([x + s - 30, cy - 34, x + s - 22, cy], fill=STEEL)
    # cables
    draw.line([(x + 26, cy - 34), (x + s // 2 - 14, cy)], fill=STEEL, width=3)
    draw.line([(x + s - 26, cy - 34), (x + s // 2 + 14, cy)], fill=STEEL, width=3)
    # blast burst over the gap
    starburst(draw, x + s // 2, cy - 18, 30, 14, 8, ORANGE)
    starburst(draw, x + s // 2, cy - 18, 18, 8, 8, GOLD)


def icon_globe_plane(draw, x, y, s):
    """Globe with a plane crossing it: Trump flies to Asia for APEC."""
    cx, cy = x + s // 2, y + s // 2 + 4
    r = s // 2 - 14
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=STEEL)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=4)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=WHITE, width=3)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=WHITE, width=3)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 180, fill=WHITE, width=3)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 180, 360, fill=WHITE, width=3)
    # plane: delta body with wings, flying up-right
    px, py = cx + 6, cy - 6
    draw.polygon([(px + 26, py - 26), (px - 6, py + 2), (px - 2, py + 10),
                  (px + 2, py + 2), (px + 10, py - 2), (px + 2, py - 6)],
                 fill=RED)


def icon_ballot(draw, x, y, s):
    """Ballot box with a paper going in: election-day arrests in Israel."""
    bx, by = x + 22, y + s - 62
    draw.rectangle([bx, by, bx + s - 44, by + 44], fill=NAVY)
    draw.rectangle([bx + 8, by - 12, bx + s - 52, by], fill=NAVY)
    draw.rectangle([bx + 20, by - 8, bx + s - 64, by - 2], fill=GOLD)
    # paper slip above the slot, tilted, with a check mark
    draw.polygon([(bx + 22, by - 46), (bx + 58, by - 40), (bx + 52, by - 8),
                  (bx + 16, by - 14)], fill=WHITE, outline=INK, width=2)
    draw.line([(bx + 24, by - 28), (bx + 30, by - 20), (bx + 44, by - 36)],
              fill=RED, width=4)


def icon_jet_sun(draw, x, y, s):
    """Rising-sun disc with a fighter jet: Japan scrambles jets."""
    cx, cy = x + s // 2, y + s // 2
    draw.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=RED)
    # jet: delta wing silhouette flying right
    jx, jy = cx - 6, cy + 2
    draw.polygon([(jx + 44, jy), (jx + 8, jy - 12), (jx - 2, jy - 22),
                  (jx - 10, jy - 6), (jx - 34, jy - 4), (jx - 34, jy + 6),
                  (jx - 10, jy + 8), (jx - 2, jy + 22), (jx + 8, jy + 12)],
                 fill=INK)


def icon_tanker_mine(draw, x, y, s):
    """Tanker with a spiked naval mine: mines in the Strait of Hormuz."""
    cy = y + s // 2 + 16
    # hull and containers
    draw.polygon([(x + 10, cy), (x + s - 10, cy), (x + s - 22, cy + 22),
                  (x + 22, cy + 22)], fill=NAVY)
    for i, col in enumerate((RED, GOLD, STEEL)):
        cx0 = x + 22 + i * 24
        draw.rectangle([cx0, cy - 20, cx0 + 20, cy - 2], fill=col, outline=INK, width=2)
    draw.rectangle([x + s - 46, cy - 34, x + s - 30, cy - 2], fill=INK)
    # spiked mine floating ahead of the bow
    mx, my = x + s - 26, y + 26
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        draw.line([(mx + 10 * math.cos(a), my + 10 * math.sin(a)),
                   (mx + 20 * math.cos(a), my + 20 * math.sin(a))],
                  fill=INK, width=4)
    draw.ellipse([mx - 11, my - 11, mx + 11, my + 11], fill=INK)
    starburst(draw, mx, my, 26, 12, 7, ORANGE)


# ---------------------------------------------------------------------------
# Stories: the day's news, as reported on 17 November 2026.
# ---------------------------------------------------------------------------

LEAD = {
    "kicker": "MIDDLE EAST  •  LEAD",
    "headline": "Iran fires drones at US radar base in Bahrain",
    "summary": ("Bahrain says the drones were intercepted and no one was "
                "hurt at the Sheikh Isa base."),
    "icon": icon_radar_drone,
}

GRID = [
    {
        "kicker": "WASHINGTON  •  US",
        "headline": "US intel: Iran \u2018dirty bomb\u2019 plot vs Trump officials",
        "summary": ("New intelligence says Tehran plans to hit senior "
                    "officials in DC."),
        "icon": icon_radiation,
    },
    {
        "kicker": "UKRAINE  •  CRIMEA",
        "headline": "Ukraine badly damages the Kerch Bridge",
        "summary": ("Zelenskyy hails \u2018an unprecedented operation\u2019 "
                    "on the bridge to Crimea."),
        "icon": icon_bridge,
    },
    {
        "kicker": "ASIA  •  APEC",
        "headline": "Trump heads to Asia for APEC \u2014 and Xi\u2013Putin talks",
        "summary": ("A Shenzhen trilateral on 19 Nov covers nuclear "
                    "stability and Ukraine."),
        "icon": icon_globe_plane,
    },
    {
        "kicker": "ISRAEL  •  WEST BANK",
        "headline": "Israel: election-day arrests and UK sanctions",
        "summary": ("UK sanctions 8 settlement firms; a settler kills a "
                    "woman, 72, in Jericho."),
        "icon": icon_ballot,
    },
    {
        "kicker": "JAPAN  •  ASIA",
        "headline": "Japan scrambles jets after Russian airspace breach",
        "summary": ("Jets launched after suspected Russian planes violated "
                    "Japanese airspace."),
        "icon": icon_jet_sun,
    },
    {
        "kicker": "GULF  •  HORMUZ",
        "headline": "Tankers hit by naval mines in the Strait of Hormuz",
        "summary": ("Commercial tankers struck by mines in the world\u2019s "
                    "busiest oil chokepoint."),
        "icon": icon_tanker_mine,
    },
]

FOOTER = ("Houthis advance in Yemen as government forces retreat toward "
          "Aden  \u2022  Five European states plan a joint migrant return "
          "centre in Rwanda  \u2022  128 states meet in Geneva on a ban on "
          "lethal autonomous weapons  \u2022  Depardieu pleads guilty in "
          "Paris  \u2022  Doubts raised over Epstein\u2019s death")
FOOTER_PREFIX = "ALSO TODAY \u2014 "


# ---------------------------------------------------------------------------
# Layout: masthead, lead story, 2x3 grid, footer strip.
# ---------------------------------------------------------------------------

def draw_masthead(draw):
    draw.rectangle([0, 0, W, 118], fill=NAVY)
    draw.text((W // 2, 14), "THE WORLD IN ONE DAY",
              font=F_KICK, fill=(255, 210, 120), anchor="ma")
    date = "TUESDAY 17 NOVEMBER 2026"
    # shrink the date until it fits inside the page with margin
    size = 54
    while size > 36 and draw.textlength(date, font=font("DejaVuSans-Bold.ttf", size)) > W - 48:
        size -= 2
    draw.text((W // 2, 42), date,
              font=font("DejaVuSans-Bold.ttf", size), fill=WHITE, anchor="ma")
    hline(draw, 32, W - 32, 112, RED, width=4)


def draw_lead(draw):
    x0, y0, x1, y1 = 16, 128, W - 16, 322
    draw.rectangle([x0, y0, x1, y1], fill=CARD, outline=INK, width=2)
    draw.rectangle([x0, y0, x0 + 8, y1], fill=RED)
    # icon panel on the right
    draw.rectangle([x1 - 196, y0, x1, y1], fill=TINT)
    LEAD["icon"](draw, x1 - 188, y0 + 12, 180)
    tx = x0 + 24
    draw.text((tx, y0 + 14), LEAD["kicker"], font=F_KICK, fill=RED)
    y = text_block(draw, tx, y0 + 40,
                   wrap(draw, LEAD["headline"], F_LEAD_HEAD, x1 - 196 - tx - 16)[:2],
                   F_LEAD_HEAD, INK, 44)
    text_block(draw, tx, y + 4,
               wrap(draw, LEAD["summary"], F_LEAD_BODY, x1 - 196 - tx - 16)[:2],
               F_LEAD_BODY, GREY, 28)


def draw_cell(draw, story, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=CARD, outline=INK, width=2)
    draw.rectangle([x0, y0, x0 + 7, y0 + h], fill=RED)
    # icon panel on the left
    draw.rectangle([x0 + 7, y0, x0 + 119, y0 + h], fill=TINT)
    story["icon"](draw, x0 + 12, y0 + (h - 100) // 2, 100)
    tx = x0 + 132
    tw = x0 + w - tx - 12
    draw.text((tx, y0 + 12), story["kicker"], font=F_CELL_KICK, fill=RED)
    y = text_block(draw, tx, y0 + 36,
                   wrap(draw, story["headline"], F_CELL_HEAD, tw)[:2],
                   F_CELL_HEAD, INK, 27)
    text_block(draw, tx, y + 4,
               wrap(draw, story["summary"], F_CELL_BODY, tw)[:2],
               F_CELL_BODY, GREY, 22)


def draw_footer(draw):
    y0 = 958
    draw.rectangle([0, y0, W, H], fill=NAVY)
    prefix_w = draw.textlength(FOOTER_PREFIX, font=F_FOOT_B)
    lines = wrap(draw, FOOTER, F_FOOT, W - 48 - prefix_w)
    y = y0 + 5
    for i, line in enumerate(lines[:3]):
        draw.text((24, y), FOOTER_PREFIX if i == 0 else "", font=F_FOOT_B,
                  fill=(255, 210, 120))
        draw.text((24 + (prefix_w if i == 0 else 0), y), line, font=F_FOOT,
                  fill=WHITE)
        y += 20


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_lead(draw)
    # 2 columns x 3 rows of stories
    gx, gy, cw, ch, gap = 16, 334, 488, 197, 12
    for i, story in enumerate(GRID):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (ch + gap)
        draw_cell(draw, story, cx, cy, cw, ch)
    draw_footer(draw)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")
    # layout audit: every wrapped block must fit in two lines
    audit = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    for story in [LEAD] + GRID:
        hw = len(wrap(audit, story["headline"],
                      F_LEAD_HEAD if story is LEAD else F_CELL_HEAD,
                      756 if story is LEAD else 344))
        sw = len(wrap(audit, story["summary"],
                      F_LEAD_BODY if story is LEAD else F_CELL_BODY,
                      756 if story is LEAD else 344))
        print("lines:", story["headline"][:28], "head", hw, "summary", sw)
    print("footer lines:", len(wrap(audit, FOOTER, F_FOOT, W - 48 - 110)))


if __name__ == "__main__":
    main()
