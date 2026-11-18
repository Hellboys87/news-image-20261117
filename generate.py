#!/usr/bin/env python3
"""
generate.py -- hand-drawn newspaper infographic for one day of world news.

Day covered : Tuesday 17 November 2026
Output      : entry.png, a 1024 x 1024 PNG written next to this file.

Every panel below was checked against a wire or official source that
dates the event to Tuesday 17 November 2026:

  * Crimean Bridge  -- Reuters, 17 Nov 2026: Ukraine struck the bridge
    "for a second straight day on Tuesday"; traffic suspended.
  * Tara Gas tanker -- Seatrade Maritime / Maritime Executive, 17 Nov:
    second strike that day forced the crew to abandon ship; India's
    foreign ministry condemned the attack the same day.
  * ASEAN Manila    -- AP news summary, 17 Nov: Trump arrived in the
    Philippines on Tuesday as the 49th ASEAN summit closed in Manila.
  * Gold / dollar   -- Reuters via Hindu BusinessLine, updated 17 Nov:
    gold near a more-than-one-year low, dollar at a fresh 19-month
    peak, CME FedWatch pricing a December hike.
  * Retail sales    -- Reuters, 17 Nov: US October retail sales rose
    0.2%, the Census Bureau said on Tuesday; core sales rose 0.6%.
  * Cyclone Akvan   -- IMD National Bulletin No. 14, dated 17.11.2026:
    cyclonic storm over the Bay of Bengal, orange alert for Andhra
    Pradesh; the landfall in the caption is labelled as a forecast.

The picture is drawn entirely with Pillow primitives and real TTF
fonts, so all text is rendered programmatically and stays crisp.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas
SIZE = 1024
PAPER = (247, 243, 234)      # warm newsprint
INK = (20, 32, 43)           # near-black blue ink
CARD = (255, 255, 255)
MUTED = (96, 106, 116)
MASTHEAD_BG = (16, 34, 54)   # deep navy band
MASTHEAD_FG = (250, 246, 236)
GOLD_LINE = (198, 154, 52)

OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---------------------------------------------------------------- fonts
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_DATE = load_font("DejaVuSerif-Bold.ttf", 52)   # masthead date line
F_KICKER = load_font("DejaVuSans-Bold.ttf", 21)  # small caps-style labels
F_SUB = load_font("DejaVuSans.ttf", 20)          # masthead subtitle
F_CAT = load_font("DejaVuSans-Bold.ttf", 19)     # panel category strip
F_HEAD = load_font("DejaVuSans-Bold.ttf", 27)    # panel headlines
F_CAP = load_font("DejaVuSans.ttf", 19)          # panel captions
F_FOOT = load_font("DejaVuSans.ttf", 16)         # footer sources line


# ---------------------------------------------------------------- helpers
def wrap(draw, text, font, max_width):
    """Greedy word wrap using real glyph widths."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centred(draw, cx, y, text, font, fill):
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)


# ---------------------------------------------------------------- icons
# Each icon is drawn inside a 96 x 96 box whose top-left corner is (x, y).

def icon_bridge(d, x, y, accent):
    # two pylons and a deck with a broken gap in the middle
    d.line([(x + 6, y + 58), (x + 38, y + 58)], fill=INK, width=6)
    d.line([(x + 58, y + 58), (x + 90, y + 58)], fill=INK, width=6)
    d.rectangle([x + 17, y + 22, x + 24, y + 58], fill=INK)
    d.rectangle([x + 72, y + 22, x + 79, y + 58], fill=INK)
    # straight stay-cables fanning from the pylon tops down to the deck
    for deck_x in (8, 14, 32, 38):
        d.line([(x + 20, y + 24), (x + deck_x, y + 56)], fill=accent, width=3)
    for deck_x in (58, 64, 82, 88):
        d.line([(x + 76, y + 24), (x + deck_x, y + 56)], fill=accent, width=3)
    # burst where the span is broken
    cx, cy = x + 48, y + 50
    for ang in range(0, 360, 45):
        r1, r2 = 5, 13 if ang % 90 == 0 else 10
        d.line([(cx + r1 * math.cos(math.radians(ang)),
                 cy + r1 * math.sin(math.radians(ang))),
                (cx + r2 * math.cos(math.radians(ang)),
                 cy + r2 * math.sin(math.radians(ang)))],
               fill=(224, 122, 32), width=3)
    # water underneath
    for i, wy in enumerate((74, 84)):
        d.arc([x + 8 + i * 14, y + wy, x + 34 + i * 14, y + wy + 10],
              start=180, end=360, fill=(64, 116, 168), width=3)
        d.arc([x + 52 + i * 14, y + wy, x + 78 + i * 14, y + wy + 10],
              start=180, end=360, fill=(64, 116, 168), width=3)


def icon_ship(d, x, y, accent):
    # hull of a tanker, a deck tank, a bridge tower and a fire on deck
    d.polygon([(x + 6, y + 58), (x + 90, y + 58), (x + 80, y + 74),
               (x + 16, y + 74)], fill=INK)
    d.rectangle([x + 22, y + 46, x + 58, y + 58], fill=accent)
    d.rectangle([x + 66, y + 34, x + 78, y + 58], fill=INK)
    d.rectangle([x + 69, y + 38, x + 75, y + 44], fill=(255, 255, 255))
    # flame: layered teardrops above the tank
    d.polygon([(x + 34, y + 46), (x + 40, y + 24), (x + 44, y + 38),
               (x + 49, y + 22), (x + 52, y + 46)], fill=(224, 90, 30))
    d.polygon([(x + 39, y + 46), (x + 43, y + 32), (x + 47, y + 46)],
              fill=(245, 178, 49))
    # waves
    for i, wy in enumerate((82,)):
        d.arc([x + 10 + i * 30, y + wy, x + 36 + i * 30, y + wy + 10],
              start=180, end=360, fill=(64, 116, 168), width=3)
        d.arc([x + 48 + i * 20, y + wy, x + 74 + i * 20, y + wy + 10],
              start=180, end=360, fill=(64, 116, 168), width=3)


def icon_summit(d, x, y, accent):
    # a summit hall: pediment, three columns, steps, and a flag on top
    d.polygon([(x + 48, y + 22), (x + 12, y + 42), (x + 84, y + 42)],
              outline=INK, width=4)
    for cx in (24, 44, 64):
        d.rectangle([x + cx, y + 48, x + cx + 8, y + 74], fill=accent)
    d.rectangle([x + 10, y + 76, x + 86, y + 81], fill=INK)
    d.rectangle([x + 6, y + 84, x + 90, y + 89], fill=INK)
    # flag pole and waving flag
    d.line([(x + 48, y + 4), (x + 48, y + 22)], fill=INK, width=3)
    d.polygon([(x + 48, y + 4), (x + 68, y + 8), (x + 48, y + 13)],
              fill=(198, 48, 49))


def icon_gold(d, x, y, accent):
    # three stacked gold bars and a falling chart line above them
    bar = (212, 160, 32)
    d.polygon([(x + 30, y + 52), (x + 66, y + 52), (x + 60, y + 64),
               (x + 36, y + 64)], fill=bar, outline=INK)
    d.polygon([(x + 14, y + 68), (x + 50, y + 68), (x + 44, y + 80),
               (x + 20, y + 80)], fill=bar, outline=INK)
    d.polygon([(x + 48, y + 68), (x + 84, y + 68), (x + 78, y + 80),
               (x + 54, y + 80)], fill=bar, outline=INK)
    # jagged line heading down to the right, with an arrowhead
    pts = [(x + 10, y + 14), (x + 32, y + 24), (x + 46, y + 18),
           (x + 66, y + 32), (x + 86, y + 40)]
    d.line(pts, fill=(198, 48, 49), width=5, joint="curve")
    d.polygon([(x + 86, y + 40), (x + 72, y + 38), (x + 80, y + 50)],
              fill=(198, 48, 49))


def icon_retail(d, x, y, accent):
    # rising bar chart with an arrow, plus a shopping bag in front
    base = y + 84
    for i, h in enumerate((22, 34, 48)):
        bx = x + 8 + i * 20
        d.rectangle([bx, base - h, bx + 14, base], fill=accent)
    d.line([(x + 10, y + 52), (x + 38, y + 38), (x + 62, y + 26)],
           fill=INK, width=4)
    d.polygon([(x + 62, y + 26), (x + 50, y + 26), (x + 58, y + 36)],
              fill=INK)
    # shopping cart in front of the bars: basket, handle and two wheels
    d.polygon([(x + 60, y + 54), (x + 92, y + 54), (x + 87, y + 74),
               (x + 65, y + 74)], outline=INK, width=3)
    d.line([(x + 66, y + 61), (x + 89, y + 61)], fill=INK, width=2)
    d.line([(x + 54, y + 50), (x + 60, y + 54)], fill=INK, width=3)
    for wx in (68, 84):
        d.ellipse([x + wx, y + 78, x + wx + 7, y + 85], fill=INK)


def icon_cyclone(d, x, y, accent):
    # spiral storm: concentric arcs opening outward, rain slanting below
    cx, cy = x + 48, y + 40
    for radius, start in ((10, 20), (20, 140), (31, 260), (42, 60)):
        box = [cx - radius, cy - radius, cx + radius, cy + radius]
        d.arc(box, start=start, end=start + 235, fill=accent, width=5)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=INK)
    for i in range(4):
        rx = x + 18 + i * 18
        d.line([(rx, y + 78), (rx - 6, y + 90)], fill=(64, 116, 168), width=3)


# ---------------------------------------------------------------- panels
PANELS = [
    {
        "cat": "WAR · UKRAINE",
        "accent": (176, 48, 48),
        "icon": icon_bridge,
        "head": "CRIMEAN BRIDGE STRUCK AGAIN",
        "cap": "Ukraine hit the Russia–Crimea bridge a second straight "
               "day; traffic was suspended and two people were killed.",
    },
    {
        "cat": "SHIPPING · HORMUZ",
        "accent": (18, 110, 130),
        "icon": icon_ship,
        "head": "TANKER ABANDONED IN HORMUZ",
        "cap": "LPG tanker Tara Gas, struck again, was abandoned: 21 of "
               "24 Indian crew reached Khasab, one still missing.",
    },
    {
        "cat": "DIPLOMACY · MANILA",
        "accent": (62, 78, 160),
        "icon": icon_summit,
        "head": "ASEAN SUMMIT ENDS IN MANILA",
        "cap": "The 49th ASEAN summit closed as Trump arrived for the "
               "ASEAN–US summit; the chair passes to Singapore.",
    },
    {
        "cat": "MARKETS · GOLD",
        "accent": (168, 124, 20),
        "icon": icon_gold,
        "head": "GOLD NEAR ONE-YEAR LOW",
        "cap": "Gold held near a one-year low as the dollar hit a "
               "19-month peak; markets priced 95.4% odds of a Dec Fed hike.",
    },
    {
        "cat": "US ECONOMY · RETAIL",
        "accent": (44, 128, 84),
        "icon": icon_retail,
        "head": "RETAIL SALES EDGE UP 0.2%",
        "cap": "US October retail sales rose 0.2% after September's 0.8% "
               "jump; core sales climbed 0.6%, Census said Tuesday.",
    },
    {
        "cat": "WEATHER · BAY OF BENGAL",
        "accent": (224, 122, 32),
        "icon": icon_cyclone,
        "head": "CYCLONE AKVAN STRENGTHENS",
        "cap": "IMD put Akvan 610 km east of Chennai under an orange "
               "alert; forecast: Andhra landfall on 20 Nov.",
    },
]


# ---------------------------------------------------------------- layout
MARGIN = 28
GAP = 16
MASTHEAD_Y = 24
MASTHEAD_H = 158
GRID_Y = MASTHEAD_Y + MASTHEAD_H + 18
FOOTER_Y = SIZE - 44
PANEL_W = (SIZE - 2 * MARGIN - GAP) // 2          # 476
PANEL_H = (FOOTER_Y - GRID_Y - 2 * GAP) // 3      # rows of three


def draw_masthead(d):
    d.rectangle([MARGIN, MASTHEAD_Y, SIZE - MARGIN,
                 MASTHEAD_Y + MASTHEAD_H], fill=MASTHEAD_BG)
    d.rectangle([MARGIN, MASTHEAD_Y + MASTHEAD_H - 6, SIZE - MARGIN,
                 MASTHEAD_Y + MASTHEAD_H], fill=GOLD_LINE)
    centred(d, SIZE / 2, MASTHEAD_Y + 14,
            "THE WORLD IN ONE PICTURE", F_KICKER, (214, 186, 120))
    centred(d, SIZE / 2, MASTHEAD_Y + 44,
            "TUESDAY 17 NOVEMBER 2026", F_DATE, MASTHEAD_FG)
    centred(d, SIZE / 2, MASTHEAD_Y + 118,
            "Six stories verified against the day's wires",
            F_SUB, (188, 198, 210))


def draw_panel(d, panel, px, py):
    # card body and category strip
    d.rectangle([px, py, px + PANEL_W, py + PANEL_H], fill=CARD,
                outline=(210, 204, 188), width=2)
    d.rectangle([px, py, px + PANEL_W, py + 36], fill=panel["accent"])
    d.text((px + 16, py + 8), panel["cat"], font=F_CAT,
           fill=(255, 255, 255))

    # icon on the left, headline to its right
    icon_x, icon_y = px + 18, py + 52
    panel["icon"](d, icon_x, icon_y, panel["accent"])
    head_x = px + 130
    head_lines = wrap(d, panel["head"], F_HEAD, PANEL_W - 130 - 16)
    for i, line in enumerate(head_lines[:3]):
        d.text((head_x, py + 54 + i * 34), line, font=F_HEAD, fill=INK)

    # caption across the full width under the icon row
    cap_y = py + 162
    d.line([(px + 16, cap_y - 10), (px + PANEL_W - 16, cap_y - 10)],
           fill=(226, 220, 204), width=2)
    cap_lines = wrap(d, panel["cap"], F_CAP, PANEL_W - 32)
    for i, line in enumerate(cap_lines[:3]):
        d.text((px + 16, cap_y + i * 25), line, font=F_CAP, fill=(52, 62, 72))


def main():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)

    draw_masthead(d)
    for idx, panel in enumerate(PANELS):
        col, row = idx % 2, idx // 2
        px = MARGIN + col * (PANEL_W + GAP)
        py = GRID_Y + row * (PANEL_H + GAP)
        draw_panel(d, panel, px, py)

    centred(d, SIZE / 2, FOOTER_Y + 6,
            "Sources: Reuters · AP · Seatrade Maritime · India MEA · IMD "
            "— all dated Tuesday 17 Nov 2026",
            F_FOOT, MUTED)

    img.save(OUT_PATH, format="PNG", optimize=True)
    print("wrote", OUT_PATH, os.path.getsize(OUT_PATH), "bytes")


if __name__ == "__main__":
    main()
