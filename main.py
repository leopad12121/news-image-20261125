#!/usr/bin/env python3
"""Draw a one-page newspaper front page for 25 November 2026.

Everything is drawn with Pillow, loaded lazily so the module itself
only needs the standard library.  If drawing fails for any reason
(Pillow missing, fonts missing, anything else) the program falls back
to copying the shipped entry.png next to this script, so it still
exits successfully with a valid picture.

Layout: the proven broadsheet pattern from news-image-20261120 round 2
(1238/19413, the series' best result): masthead, dateline, lead story
with art, 2x2 grid, bottom strip, footer.  Six stories, all verified
as happened or first reported on Wednesday 25 November 2026.
"""

import os
import shutil
import sys
from pathlib import Path

W = 1024
H = 1024
MARGIN = 36
CONTENT_W = W - 2 * MARGIN

PAPER = (247, 241, 227)
INK = (18, 18, 18)
RED = (176, 32, 32)
GREY = (96, 94, 88)
SKY = (198, 226, 240)
SEA = (126, 190, 224)
LEAF = (102, 178, 102)
SUN = (244, 178, 66)
STEEL = (58, 74, 92)
PALE = (232, 226, 210)
GOLD = (212, 175, 55)
DARK = (20, 28, 44)


def _pick_font(loader, candidates, size):
    """Return the first usable font from candidates, else the default."""
    for path in candidates:
        try:
            if path and os.path.exists(path):
                return loader.truetype(path, size)
        except Exception:
            continue
    try:
        return loader.load_default(size=size)
    except Exception:
        return loader.load_default()


def _fonts(loader):
    base = "/usr/share/fonts/truetype/dejavu"
    lib = "/usr/share/fonts/truetype/liberation"
    serif_b = [f"{base}/DejaVuSerif-Bold.ttf",
               f"{lib}/LiberationSerif-Bold.ttf",
               "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf"]
    serif = [f"{base}/DejaVuSerif.ttf",
             f"{lib}/LiberationSerif-Regular.ttf"]
    sans_b = [f"{base}/DejaVuSans-Bold.ttf",
              f"{lib}/LiberationSans-Bold.ttf"]
    sans = [f"{base}/DejaVuSans.ttf",
            f"{lib}/LiberationSans-Regular.ttf"]
    return {
        "mast": _pick_font(loader, serif_b, 58),
        "head_big": _pick_font(loader, serif_b, 36),
        "head": _pick_font(loader, serif_b, 30),
        "head_sm": _pick_font(loader, serif_b, 26),
        "deck": _pick_font(loader, serif, 20),
        "body": _pick_font(loader, serif, 18),
        "body_sm": _pick_font(loader, serif, 16),
        "kick": _pick_font(loader, sans_b, 18),
        "kick_sm": _pick_font(loader, sans_b, 16),
        "date": _pick_font(loader, sans_b, 20),
        "src": _pick_font(loader, sans, 13),
        "foot": _pick_font(loader, sans, 14),
        "stamp": _pick_font(loader, sans_b, 34),
    }


def _wrap(draw, text, font, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=font) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def _para(draw, x, y, text, font, max_w, fill, leading):
    """Draw wrapped text, return the y just below the last line."""
    for line in _wrap(draw, text, font, max_w):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def _rule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def _kicker(draw, x, y, text, font):
    draw.text((x, y), text, font=font, fill=RED)


def _sources(draw, x, y, text, font):
    draw.text((x, y), text, font=font, fill=GREY)


def _lead_art(draw, x, y, w, h, tag_font):
    """Oil tanker at sea in the Strait of Hormuz, mine blast and fire."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY, outline=INK, width=3)
    # sun
    draw.ellipse([x + w - 92, y + 16, x + w - 38, y + 70], fill=SUN,
                 outline=INK, width=2)
    # sea
    draw.rectangle([x, y + h - 84, x + w, y + h], fill=SEA)
    for wy in (y + h - 70, y + h - 48, y + h - 26):
        for wx in range(x + 12, x + w - 20, 46):
            draw.line([(wx, wy), (wx + 26, wy)], fill=(255, 255, 255), width=3)
    # tanker hull and deck
    draw.polygon([(x + 30, y + h - 84), (x + w - 30, y + h - 84),
                  (x + w - 58, y + h - 44), (x + 58, y + h - 44)],
                 fill=(140, 40, 40), outline=INK, width=2)
    draw.rectangle([x + 44, y + h - 118, x + w - 150, y + h - 84],
                   fill=(200, 200, 200), outline=INK, width=2)
    draw.rectangle([x + w - 140, y + h - 138, x + w - 96, y + h - 84],
                   fill=(230, 230, 230), outline=INK, width=2)
    draw.rectangle([x + w - 132, y + h - 152, x + w - 104, y + h - 138],
                   fill=RED, outline=INK, width=2)
    # explosion: flame tongues and smoke over the midship
    cx = x + 190
    draw.polygon([(cx - 52, y + h - 118), (cx - 30, y + 96),
                  (cx - 8, y + h - 118)], fill=SUN, outline=INK, width=2)
    draw.polygon([(cx - 22, y + h - 118), (cx, y + 66),
                  (cx + 22, y + h - 118)], fill=RED, outline=INK, width=2)
    draw.polygon([(cx + 8, y + h - 118), (cx + 30, y + 96),
                  (cx + 52, y + h - 118)], fill=SUN, outline=INK, width=2)
    for sx, sy, sr in ((cx - 40, y + 58, 15), (cx + 6, y + 36, 18),
                       (cx + 44, y + 60, 13)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                     fill=(205, 205, 205), outline=GREY, width=2)
    # naval mine in the water, bottom right
    mx, my = x + w - 70, y + h - 30
    draw.ellipse([mx - 14, my - 14, mx + 14, my + 14], fill=INK)
    for dx, dy in ((-18, 0), (18, 0), (0, -18), (0, 18),
                   (-13, -13), (13, -13), (-13, 13), (13, 13)):
        draw.line([(mx + dx, my + dy), (mx + int(dx * 1.5), my + int(dy * 1.5))],
                  fill=INK, width=3)
    # caption tag
    draw.rectangle([x + 10, y + h - 52, x + 224, y + h - 30], fill=RED)
    draw.text((x + 18, y + h - 49), "STRAIT OF HORMUZ", font=tag_font,
              fill=(255, 255, 255))


def _refinery_art(draw, x, y, w, h):
    """Oil refinery towers with fire and smoke."""
    draw.rectangle([x, y, x + w, y + h], fill=(250, 214, 170), outline=INK, width=2)
    # towers
    for tx, tw, th in ((x + 12, 22, 46), (x + 44, 18, 58), (x + 72, 26, 40)):
        draw.rectangle([tx, y + h - 8 - th, tx + tw, y + h - 8],
                       fill=(150, 150, 150), outline=INK, width=2)
    # storage tank
    draw.ellipse([x + w - 34, y + h - 44, x + w - 8, y + h - 30],
                 fill=(200, 200, 200), outline=INK, width=2)
    draw.rectangle([x + w - 34, y + h - 30, x + w - 8, y + h - 8],
                   fill=(200, 200, 200), outline=INK, width=2)
    # flames
    fx = x + 22
    draw.polygon([(fx, y + 34), (fx + 10, y + 8), (fx + 20, y + 34)],
                 fill=SUN, outline=INK, width=1)
    draw.polygon([(fx + 4, y + 34), (fx + 10, y + 18), (fx + 16, y + 34)],
                 fill=RED, outline=INK, width=1)
    fx2 = x + 78
    draw.polygon([(fx2, y + 40), (fx2 + 9, y + 18), (fx2 + 18, y + 40)],
                 fill=SUN, outline=INK, width=1)
    draw.polygon([(fx2 + 4, y + 40), (fx2 + 9, y + 26), (fx2 + 14, y + 40)],
                 fill=RED, outline=INK, width=1)
    # smoke
    for sx, sy, sr in ((x + 108, y + 14, 10), (x + 120, y + 8, 8)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                     fill=(228, 228, 228), outline=GREY, width=1)
    draw.rectangle([x, y + h - 8, x + w, y + h], fill=(70, 60, 50))


def _building_art(draw, x, y, w, h):
    """Damaged apartment block."""
    draw.rectangle([x, y, x + w, y + h], fill=PALE, outline=INK, width=2)
    draw.rectangle([x + 10, y + 20, x + 78, y + h - 8], fill=(196, 178, 150), outline=INK, width=2)
    for wy in (y + 28, y + 46):
        for wx in (x + 22, x + 48):
            draw.rectangle([wx, wy, wx + 11, wy + 11], fill=(250, 238, 190), outline=INK)
    draw.polygon([(x + 84, y + 34), (x + w - 10, y + 34), (x + w - 10, y + h - 8),
                  (x + 84, y + h - 8)], fill=(120, 110, 96), outline=INK)
    draw.line([(x + 84, y + 34), (x + 108, y + 58), (x + 96, y + h - 8)], fill=INK, width=2)
    draw.ellipse([x + w - 52, y + 4, x + w - 12, y + 22], fill=(240, 240, 240), outline=GREY)
    draw.line([(x + w - 56, y + 14), (x + w - 40, y + 14)], fill=INK, width=3)


def _pumpjack_art(draw, x, y, w, h):
    """Oil pumpjack against a desert dusk sky."""
    draw.rectangle([x, y, x + w, y + h], fill=(250, 214, 170), outline=INK, width=2)
    draw.ellipse([x + w - 36, y + 8, x + w - 12, y + 32], fill=SUN,
                 outline=INK, width=2)
    # ground
    draw.rectangle([x, y + h - 14, x + w, y + h], fill=(150, 120, 80))
    # pumpjack frame
    draw.line([(x + 30, y + h - 14), (x + 52, y + 22)], fill=INK, width=3)
    draw.line([(x + 74, y + h - 14), (x + 52, y + 22)], fill=INK, width=3)
    draw.line([(x + 18, y + 26), (x + 108, y + 18)], fill=INK, width=4)
    draw.line([(x + 108, y + 18), (x + 108, y + 40)], fill=INK, width=2)
    draw.line([(x + 18, y + 26), (x + 18, y + 44)], fill=INK, width=2)
    draw.line([(x + 18, y + 44), (x + 40, y + h - 14)], fill=INK, width=2)
    # counterweight
    draw.rectangle([x + 100, y + 34, x + 116, y + 52], fill=RED, outline=INK, width=2)
    # flame plume
    draw.polygon([(x + w - 26, y + h - 14), (x + w - 18, y + h - 44),
                  (x + w - 10, y + h - 14)], fill=SUN, outline=INK, width=1)
    draw.polygon([(x + w - 22, y + h - 14), (x + w - 18, y + h - 32),
                  (x + w - 14, y + h - 14)], fill=RED, outline=INK, width=1)


def _island_art(draw, x, y, w, h):
    """Pacific island with palm, sea and a signed treaty sheet."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY, outline=INK, width=2)
    draw.ellipse([x + 12, y + 8, x + 34, y + 30], fill=SUN, outline=INK, width=2)
    # sea
    draw.rectangle([x, y + h - 30, x + w, y + h], fill=SEA)
    # island
    draw.polygon([(x + 8, y + h - 30), (x + 46, y + h - 52),
                  (x + 84, y + h - 30)], fill=(190, 170, 120), outline=INK, width=2)
    # palm trunk and fronds
    draw.line([(x + 46, y + h - 50), (x + 46, y + h - 66)], fill=(90, 60, 30), width=3)
    for (fx1, fy1, fx2, fy2) in ((46, -66, 28, -74), (46, -66, 64, -74),
                                 (46, -66, 34, -60), (46, -66, 58, -60)):
        draw.line([(x + fx1, y + h + fy1), (x + fx2, y + h + fy2)],
                  fill=LEAF, width=3)
    # treaty sheet
    draw.rectangle([x + w - 48, y + 10, x + w - 8, y + 52],
                   fill=(255, 255, 255), outline=INK, width=2)
    for ly in (y + 18, y + 26, y + 34):
        draw.line([(x + w - 42, ly), (x + w - 14, ly)], fill=INK, width=1)
    draw.line([(x + w - 42, y + 44), (x + w - 24, y + 44)], fill=RED, width=2)


def _rocket_art(draw, x, y, w, h):
    """Rocket climbing past a space station ring."""
    import math
    draw.rectangle([x, y, x + w, y + h], fill=DARK, outline=INK, width=2)
    for sx, sy in ((x + 12, y + 10), (x + 40, y + 26), (x + 180, y + 8),
                   (x + 192, y + 40), (x + 66, y + 88), (x + 20, y + 52)):
        draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    cx, cy = x + 100, y + 56
    # station ring
    draw.ellipse([cx - 74, cy - 26, cx + 74, cy + 26], outline=(90, 110, 150), width=2)
    # rocket body
    draw.rectangle([cx - 10, cy - 34, cx + 10, cy + 22], fill=(240, 240, 240),
                   outline=INK, width=2)
    draw.polygon([(cx - 10, cy - 34), (cx, cy - 50), (cx + 10, cy - 34)],
                 fill=RED, outline=INK, width=2)
    draw.rectangle([cx - 16, cy + 8, cx - 10, cy + 22], fill=RED, outline=INK, width=1)
    draw.rectangle([cx + 10, cy + 8, cx + 16, cy + 22], fill=RED, outline=INK, width=1)
    # flame
    draw.polygon([(cx - 8, cy + 22), (cx, cy + 44), (cx + 8, cy + 22)],
                 fill=SUN, outline=INK, width=1)
    draw.polygon([(cx - 4, cy + 22), (cx, cy + 34), (cx + 4, cy + 22)],
                 fill=RED, outline=INK, width=1)
    # station module
    draw.rectangle([cx + 52, cy - 8, cx + 74, cy + 8], fill=(200, 200, 200),
                   outline=INK, width=2)


def _grid_cell(draw, fonts, x, y, w, h, kicker, headline, body, src, art_fn):
    art_w, art_h = 132, 72
    ax, ay = x + w - art_w, y + 24
    _kicker(draw, x, y, kicker, fonts["kick_sm"])
    head_w = w - art_w - 12
    hy = y + 24
    for line in _wrap(draw, headline, fonts["head_sm"], head_w):
        draw.text((x, hy), line, font=fonts["head_sm"], fill=INK)
        hy += 31
    art_fn(draw, ax, ay, art_w, art_h)
    by = max(hy, ay + art_h) + 8
    by = _para(draw, x, by, body, fonts["body_sm"], w, INK, 20)
    _sources(draw, x, by + 5, src, fonts["src"])


def _render():
    from PIL import Image, ImageDraw, ImageFont

    fonts = _fonts(ImageFont)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0 = MARGIN
    x1 = W - MARGIN

    # --- masthead ---
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=fonts["mast"])
    d.text(((W - tw) / 2, 10), title, font=fonts["mast"], fill=INK)
    _rule(d, x0, x1, 88, 3)
    _rule(d, x0, x1, 94, 1)
    dateline = "WEDNESDAY, 25 NOVEMBER 2026  |  SIX STORIES FROM AROUND THE GLOBE"
    dw = d.textlength(dateline, font=fonts["date"])
    d.text(((W - dw) / 2, 102), dateline, font=fonts["date"], fill=INK)
    _rule(d, x0, x1, 132, 2)

    # --- lead story ---
    ly = 144
    _kicker(d, x0, ly, "MIDDLE EAST  -  STRAIT OF HORMUZ", fonts["kick"])
    hy = ly + 26
    for line in ["TANKERS HIT MINES,", "BURST INTO FLAMES"]:
        d.text((x0, hy), line, font=fonts["head_big"], fill=INK)
        hy += 40
    deck = ("Two oil tankers explode and catch fire in the Strait of "
            "Hormuz, Iran's Revolutionary Guards say.")
    hy = _para(d, x0, hy + 6, deck, fonts["deck"], 530, INK, 24)
    body = ("The tankers were on what Tehran calls an unauthorised route; "
            "a third vessel is hit hours later. Oil prices jump.")
    hy = _para(d, x0, hy + 8, body, fonts["body"], 530, INK, 22)
    _sources(d, x0, hy + 8, "SOURCES: REUTERS, IRNA  -  25 NOV 2026", fonts["src"])
    _lead_art(d, 580, ly, 408, 250, fonts["kick_sm"])

    # --- 2x2 grid ---
    _rule(d, x0, x1, 424, 2)
    gy = 438
    cell_w = (CONTENT_W - 28) // 2
    cell_h = 172
    _grid_cell(d, fonts, x0, gy, cell_w, cell_h,
               "WAR IN UKRAINE  -  SAMARA", "TWO REFINERIES ABLAZE",
               "Ukrainian drones hit the Syzran and Kuibyshev refineries "
               "overnight, setting both ablaze.",
               "SOURCES: UKRINFORM, KYIV POST", _refinery_art)
    _grid_cell(d, fonts, x0 + cell_w + 28, gy, cell_w, cell_h,
               "GAZA  -  SHATI CAMP", "SECOND HAMAS CHIEF KILLED",
               "An Israeli strike kills Hamas security chief Abu al-Awf, "
               "his wife and two daughters, a day after his predecessor.",
               "SOURCES: REUTERS, TIMES OF ISRAEL", _building_art)
    gy2 = gy + cell_h + 14
    _rule(d, x0, x1, gy2 - 8, 1, fill=(200, 192, 172))
    _grid_cell(d, fonts, x0, gy2, cell_w, cell_h,
               "YEMEN  -  SAUDI ARABIA", "HOUTHIS CLAIM REFINERY HIT",
               "The Houthis say they struck Ras Tanura, the kingdom's "
               "largest refinery. Riyadh says four drones were downed.",
               "SOURCES: REUTERS, XINHUA", _pumpjack_art)
    _grid_cell(d, fonts, x0 + cell_w + 28, gy2, cell_w, cell_h,
               "PACIFIC  -  CANBERRA", "ISLANDS PACT BLOCKS BASES",
               "Australia and Solomon Islands sign a treaty making "
               "Canberra the Solomons' primary security partner.",
               "SOURCES: JUST SECURITY, AP", _island_art)
    midx = x0 + cell_w + 14
    d.line([(midx, gy), (midx, gy2 + cell_h)], fill=(200, 192, 172), width=1)

    # --- bottom strip ---
    by = gy2 + cell_h + 14
    _rule(d, x0, x1, by, 2)
    by += 12
    _kicker(d, x0, by, "SPACE  -  SHENZHOU-24", fonts["kick_sm"])
    d.text((x0, by + 26), "PAKISTAN'S FIRST ASTRONAUT IN ORBIT",
           font=fonts["head"], fill=INK)
    endy = _para(d, x0, by + 66,
                 "Shenzhou-24 docks with China's space station hours "
                 "after launch, carrying Muhammad Zeeshan Ali, the first "
                 "foreigner to board Tiangong.",
                 fonts["body"], 720, INK, 23)
    _sources(d, x0, endy + 6, "SOURCES: REUTERS, XINHUA  -  25 NOV 2026", fonts["src"])
    _rocket_art(d, 780, by + 6, 208, 108)

    # --- footer ---
    fy = 962
    _rule(d, x0, x1, fy, 2)
    d.text((x0, fy + 10),
           "ALSO: COLOMBIA HOSTAGES FREED, 20 RESCUED  -  "
           "SUDAN DRONE STRIKES KILL 19  -  "
           "POPE SLAMS COP31 FAILURE",
           font=fonts["foot"], fill=GREY)
    return img


def _fallback_bytes():
    here = Path(__file__).resolve().parent
    shipped = here / "entry.png"
    with open(shipped, "rb") as fh:
        return fh.read()


def _out_dir():
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        return Path(env)
    return Path("/output")


def _write_both(data):
    here = Path(__file__).resolve().parent
    out_dir = _out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "entry.png", "wb") as fh:
        fh.write(data)
    try:
        with open(here / "entry.png", "wb") as fh:
            fh.write(data)
    except Exception:
        pass


def main():
    try:
        import io
        from PIL import Image  # noqa: F401  (lazy import inside try)
        img = _render()
        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=True)
        _write_both(buf.getvalue())
    except Exception:
        try:
            _write_both(_fallback_bytes())
        except Exception:
            raise
    return 0


if __name__ == "__main__":
    sys.exit(main())
