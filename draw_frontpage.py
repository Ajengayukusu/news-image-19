#!/usr/bin/env python3
"""Draw the 19 November 2026 front page (1024x1024 PNG).

A newspaper front page drawn from scratch with Pillow: masthead naming the
date, a flat illustration of the day's top story (the first-ever Trump-Xi-
Putin trilateral summit in Shenzhen), and five more reported stories of the
day, each with a small pictogram, a headline and one faithful line.

Every story below was reported on Thursday 19 November 2026:
  * Trump, Xi and Putin meet in Shenzhen (APEC sidelines)
  * Gulf war spreads: Iran strikes US bases in Kuwait and Bahrain
  * Anthropic raises $81.3bn in the biggest IPO ever
  * Van Gogh sells for a record $190.4m
  * Voyager 1 reaches one light-day from Earth
  * GTA VI begins its global rollout

Run:  python3 draw_frontpage.py
Writes: assets/entry.png (deterministic: fixed palette, fonts, layout).
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "entry.png")

W, H = 1024, 1024
PAPER = (251, 247, 238)
NAVY = (20, 33, 61)
NAVY_LIGHT = (38, 58, 94)
GOLD = (212, 160, 60)
RED = (178, 34, 34)
INK = (32, 32, 32)
GREY = (88, 88, 88)
SKY_TOP = (186, 214, 238)
SKY_BOT = (238, 242, 247)
PANEL = (255, 253, 248)
RULE = (180, 172, 150)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Wrap text to fit max_w pixels; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_flag(draw, x, y, w, h, kind):
    """A small flat flag on a pole at (x, y); returns the pole top."""
    draw.line([(x, y), (x, y + 150)], fill=NAVY, width=5)
    draw.ellipse([x - 4, y - 4, x + 4, y + 4], fill=GOLD)
    if kind == "us":
        for i in range(7):
            draw.rectangle([x + 5, y + i * h // 7, x + 5 + w, y + (i + 1) * h // 7],
                           fill=(255, 255, 255) if i % 2 else (178, 34, 34))
        draw.rectangle([x + 5, y, x + 5 + w * 2 // 5, y + h * 4 // 7], fill=(30, 50, 110))
        for r in range(3):
            for c in range(4):
                cx = x + 12 + c * 13
                cy = y + 8 + r * 11
                draw.ellipse([cx, cy, cx + 4, cy + 4], fill=(255, 255, 255))
    elif kind == "cn":
        draw.rectangle([x + 5, y, x + 5 + w, y + h], fill=(222, 41, 16))
        draw.regular_polygon((x + 22, y + 15, 7), 5, fill=(255, 222, 0))
        for sx, sy in [(42, 8), (50, 16), (50, 26), (42, 32)]:
            draw.regular_polygon((x + sx, y + sy, 3), 5, fill=(255, 222, 0))
    elif kind == "ru":
        third = h // 3
        for i, col in enumerate([(255, 255, 255), (0, 60, 160), (200, 30, 30)]):
            draw.rectangle([x + 5, y + i * third, x + 5 + w, y + (i + 1) * third],
                           fill=col)


def pictogram(draw, x, y, s, kind, fg, bg):
    """A small square pictogram for a story row."""
    draw.rounded_rectangle([x, y, x + s, y + s], radius=10, fill=bg)
    c = s // 2
    if kind == "burst":
        for k in range(8):
            ang = k * 3.14159 / 4
            x1 = x + c + int(10 * 0.7 * (1 if abs(ang) < 1 else 1))
            draw.line([(x + c, y + c),
                       (x + c + int(24 * __import__("math").cos(ang)),
                        y + c + int(24 * __import__("math").sin(ang)))],
                      fill=fg, width=5)
        draw.ellipse([x + c - 9, y + c - 9, x + c + 9, y + c + 9], fill=fg)
    elif kind == "chart":
        pts = [(x + 12, y + s - 16), (x + 26, y + s - 30), (x + 38, y + s - 22),
               (x + 52, y + s - 40)]
        draw.line(pts, fill=fg, width=5, joint="curve")
        draw.polygon([(x + 52, y + s - 40), (x + 44, y + s - 40), (x + 52, y + s - 32)],
                     fill=fg)
    elif kind == "frame":
        draw.rectangle([x + 14, y + 12, x + s - 14, y + s - 12], outline=fg, width=4)
        draw.ellipse([x + 26, y + 24, x + s - 26, y + s - 24], outline=fg, width=3)
        draw.line([(x + 14, y + s - 12), (x + s - 14, y + 12)], fill=fg, width=3)
    elif kind == "probe":
        draw.ellipse([x + 16, y + 16, x + s - 16, y + s - 16], outline=fg, width=4)
        draw.line([(x + c, y + c), (x + s - 10, y + 10)], fill=fg, width=4)
        draw.ellipse([x + s - 18, y + 4, x + s - 6, y + 16], fill=fg)
        draw.ellipse([x + c - 5, y + c - 5, x + c + 5, y + c + 5], fill=fg)
    elif kind == "pad":
        draw.rounded_rectangle([x + 12, y + 18, x + s - 12, y + s - 18], radius=12,
                               outline=fg, width=4)
        draw.ellipse([x + 22, y + 28, x + 30, y + 36], fill=fg)
        draw.ellipse([x + s - 30, y + 28, x + s - 22, y + 36], fill=fg)
        draw.line([(x + c - 8, y + s - 26), (x + c + 8, y + s - 26)], fill=fg, width=4)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([4, 4, W - 5, H - 5], outline=RULE, width=2)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 148], fill=NAVY)
    title = "THE WORLD IN ONE DAY"
    tf = SERIF_B(58)
    d.text(((W - d.textlength(title, font=tf)) / 2, 22), title, font=tf,
           fill=(255, 255, 255))
    d.line([(90, 104), (W - 90, 104)], fill=GOLD, width=3)
    date = "THURSDAY  \u00b7  19 NOVEMBER 2026"
    df = SANS_B(30)
    d.text(((W - d.textlength(date, font=df)) / 2, 112), date, font=df,
           fill=GOLD)

    # ---- Lead panel ----
    d.rounded_rectangle([28, 168, W - 28, 566], radius=8, fill=PANEL,
                        outline=NAVY, width=2)
    # sky + sun + skyline illustration
    ix0, iy0, ix1, iy1 = 48, 188, W - 48, 396
    for yy in range(iy0, iy1):
        t = (yy - iy0) / (iy1 - iy0)
        col = tuple(int(SKY_TOP[i] + (SKY_BOT[i] - SKY_TOP[i]) * t) for i in range(3))
        d.line([(ix0, yy), (ix1, yy)], fill=col)
    d.ellipse([ix1 - 120, iy0 + 18, ix1 - 52, iy0 + 86], fill=(255, 214, 90),
              outline=(230, 180, 60), width=3)
    skyline = [(0, 150), (70, 108), (130, 132), (200, 84), (260, 118),
               (330, 92), (400, 140), (470, 100), (540, 128), (610, 88),
               (680, 124), (750, 96), (820, 136), (880, 110)]
    base = iy1
    for bx, bh in skyline:
        d.rectangle([ix0 + bx, base - bh, ix0 + bx + 58, base], fill=NAVY_LIGHT)
        for wy in range(base - bh + 12, base - 10, 18):
            for wx in range(ix0 + bx + 10, ix0 + bx + 50, 16):
                d.rectangle([wx, wy, wx + 6, wy + 8], fill=(255, 220, 130))
    d.rectangle([ix0, base - 8, ix1, base], fill=(150, 40, 40))
    # three flags above the skyline
    draw_flag(d, 150, iy0 + 8, 72, 48, "us")
    draw_flag(d, 470, iy0 + 8, 72, 48, "cn")
    draw_flag(d, 800, iy0 + 8, 72, 48, "ru")

    # lead headline + standfirst (shrink the headline until it fits the panel)
    hl = "TRUMP, XI AND PUTIN MEET IN SHENZHEN"
    hl_size = 40
    while hl_size > 20:
        hf = SERIF_B(hl_size)
        if d.textlength(hl, font=hf) <= W - 120:
            break
        hl_size -= 1
    d.text(((W - d.textlength(hl, font=hf)) / 2, 410), hl, font=hf, fill=NAVY)
    d.line([(300, 462), (W - 300, 462)], fill=GOLD, width=3)
    sub = ("First-ever trilateral summit on the APEC sidelines \u2014 "
           "nuclear arms control and the Gulf war top the agenda.")
    sf = SANS(23)
    y = 474
    for line in wrap(d, sub, sf, W - 140):
        d.text(((W - d.textlength(line, font=sf)) / 2, y), line, font=sf,
               fill=INK)
        y += 30

    # ---- Five more stories ----
    stories = [
        ("burst", (178, 34, 34), (253, 226, 226),
         "GULF WAR SPREADS",
         "Iran strikes US bases in Kuwait and Bahrain; a tanker is hit near Oman."),
        ("chart", (20, 90, 40), (214, 238, 214),
         "ANTHROPIC'S RECORD IPO",
         "AI firm raises $81.3bn in the biggest listing ever; debut tops $1.4tn."),
        ("frame", (120, 70, 10), (246, 232, 200),
         "VAN GOGH SELLS FOR $190.4M",
         "Record price for the painting after a row over its Nazi-era history."),
        ("probe", (30, 50, 110), (220, 226, 246),
         "VOYAGER 1, ONE LIGHT-DAY AWAY",
         "NASA probe reaches the milestone 50 years after it left Earth."),
        ("pad", (110, 40, 110), (238, 222, 246),
         "GTA VI ROLLS OUT WORLDWIDE",
         "Gamers enter Vice City as the 13-year wait finally ends."),
    ]
    y = 592
    for kind, fg, bg, head, body in stories:
        pictogram(d, 48, y, 64, kind, fg, bg)
        hf2 = SANS_B(27)
        d.text((132, y + 2), head, font=hf2, fill=NAVY)
        bf = SANS(21)
        d.text((132, y + 36), body, font=bf, fill=GREY)
        y += 78
        if kind != "pad":
            d.line([(48, y - 8), (W - 48, y - 8)], fill=RULE, width=1)

    # ---- Footer ----
    d.rectangle([0, H - 44, W, H], fill=NAVY)
    foot = "19 NOVEMBER 2026  \u00b7  THE DAY'S NEWS IN ONE IMAGE"
    ff = SANS_B(20)
    d.text(((W - d.textlength(foot, font=ff)) / 2, H - 36), foot, font=ff,
           fill=(255, 255, 255))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
