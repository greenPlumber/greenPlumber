#!/usr/bin/env python3
"""Generates the profile README and its pixel art.

Run `python3 tools/build.py` from the repo root after changing any copy below.
Everything downstream -- box alignment, glyph geometry, SVG output -- is derived,
so the text in CAREER/POWER_UPS/BONUS is the only thing worth hand-editing.
"""

import os
from pixelfont import text, text_centered, text_width, rect, sprite

# ---------------------------------------------------------------- palette

SCREEN = "#12111C"   # the CRT background. every SVG paints its own.
GREEN  = "#4EC94E"   # the handle, the primary
GOLD   = "#F8D848"   # metrics and records only
BONE   = "#E8E8F0"   # body text
DIM    = "#6A6A8C"   # labels, secondary
RED    = "#E05B4A"   # used sparingly

NIGHT  = "#1D2A3A"   # hills
BRICK  = "#2A2438"   # ground

SLATE   = "#4A4A5E"  # the castle drops green and gold entirely
SLATE_D = "#33334A"
SLATE_L = "#5E5E75"
IT_G, IT_W, IT_R = "#009246", "#F1F2F1", "#CE2B37"

HERO = {
    "G": GREEN, "S": "#F0B888", "K": SCREEN, "B": "#3B5DC9", "D": "#7A4A21",
}
HERO_ART = [
    "....GGGG....",
    "...GGGGGGG..",
    "..GGGGGGGG..",
    "...SSSSSS...",
    "...SKSSKS...",
    "...SSSSSS...",
    "....SSSS....",
    "..GGGGGGGG..",
    ".G.GBBBG.G..",
    ".G.GBBBG.G..",
    ".GGGBBBGGG..",
    "...BBBBBB...",
    "...BB..BB...",
    "...BB..BB...",
    "..DDD..DDD..",
    "..DDD..DDD..",
]


def svg(w, h, body, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" shape-rendering="crispEdges" '
        f'role="img" aria-label="{title}">'
        f'<rect width="{w}" height="{h}" fill="{SCREEN}"/>'
        f"{body}</svg>\n"
    )


def blink(dur="1.2s"):
    return (f'<animate attributeName="opacity" values="1;1;0;0" '
            f'keyTimes="0;0.5;0.5;1" dur="{dur}" repeatCount="indefinite"/>')


# ---------------------------------------------------------------- title

def build_title():
    W, H, GROUND = 200, 92, 78
    o = []

    # a few stars, fixed positions so the output is deterministic
    for x, y in [(18, 8), (46, 14), (72, 6), (108, 16), (152, 9), (176, 20),
                 (34, 26), (128, 29), (190, 5), (8, 31)]:
        o.append(rect(x, y, 1, 1, DIM))

    # parallax hills: one 100-wide tile drawn three times, drifting left.
    # peaks stay below y=60 so nothing collides with the copy above them.
    hill = "".join(
        f'<polygon points="{a},{GROUND} {a + 14},{GROUND - 12} {a + 28},{GROUND}" fill="{NIGHT}"/>'
        for a in (4, 46)
    ) + f'<polygon points="74,{GROUND} 88,{GROUND - 16} 102,{GROUND}" fill="{NIGHT}"/>'
    tiles = "".join(f'<g transform="translate({i * 100},0)">{hill}</g>' for i in range(3))
    o.append(
        f'<g>{tiles}<animateTransform attributeName="transform" type="translate" '
        f'values="0 0;-100 0" dur="48s" repeatCount="indefinite"/></g>'
    )

    # ground: brick courses, offset every other row
    o.append(rect(0, GROUND, W, H - GROUND, BRICK))
    for r in range(GROUND, H, 4):
        o.append(rect(0, r, W, 1, SCREEN))
        off = 0 if (r - GROUND) % 8 == 0 else 4
        for x in range(off, W, 8):
            o.append(rect(x, r, 1, 4, SCREEN))

    o.append(text_centered("greenPlumber", W // 2, 14, 2, GREEN))
    o.append(text_centered("usually handed the part", W // 2, 34, 1, DIM))
    o.append(text_centered("that isn't allowed to fail", W // 2, 43, 1, DIM))

    o.append(f'<g>{text_centered("> PRESS START", W // 2, 54, 1, GOLD)}{blink()}</g>')

    o.append(
        f'<g>{sprite(HERO_ART, HERO, 16, GROUND - 16, 1)}'
        f'<animateTransform attributeName="transform" type="translate" '
        f'values="0 0;0 -1;0 0" dur="1.6s" repeatCount="indefinite"/></g>'
    )
    return svg(W, H, "".join(o), "greenPlumber - press start")


# ---------------------------------------------------------------- world map

MAP_NODES = [
    ("W1-1", ["AMADEUS"]),
    ("W2-1", ["OPEN", "REPLY"]),
    ("W3-1", ["ALPIAN"]),
    ("W4-1", ["FACEIT"]),
    ("W5-1", ["SYSDIG"]),
    ("W6-4", ["PUBLIC", "SERVICE"]),
]


def build_worldmap():
    W, H = 310, 64
    xs = [26, 74, 122, 170, 218, 272]
    NY = 26  # node top
    o = []

    # dotted route between nodes
    for i in range(len(xs) - 1):
        for x in range(xs[i] + 8, xs[i + 1] - 6, 5):
            o.append(rect(x, NY + 4, 2, 2, SLATE))

    for i, (label, name) in enumerate(MAP_NODES):
        x = xs[i]
        o.append(text_centered(label, x, 12, 1, DIM))
        if i < 5:
            o.append(rect(x - 5, NY, 10, 10, GREEN))
            o.append(rect(x - 3, NY + 2, 6, 6, SCREEN))
            o.append(rect(x - 2, NY + 3, 4, 4, GREEN))
        else:
            # the castle: slate, no green, no gold
            o.append(rect(x - 9, NY - 2, 18, 12, SLATE))
            for cx in range(x - 9, x + 9, 4):
                o.append(rect(cx, NY - 5, 2, 3, SLATE))
            o.append(rect(x - 2, NY + 4, 4, 6, SLATE_D))
            o.append(f'<g>{rect(x - 12, NY - 8, 24, 21, "none")}'
                     f'<rect x="{x - 12}" y="{NY - 8}" width="24" height="21" '
                     f'fill="none" stroke="{SLATE_L}" stroke-width="1">'
                     f'<animate attributeName="opacity" values="0.15;0.75;0.15" '
                     f'dur="2.4s" repeatCount="indefinite"/></rect></g>')
        # the castle's label stays dim: quieter than the companies, by design
        colour = DIM if i == 5 else BONE
        for j, line in enumerate(name):
            o.append(text_centered(line, x, 44 + j * 9, 1, colour))

    return svg(W, H, "".join(o), "career world map, six worlds")


# ---------------------------------------------------------------- castle

def build_castle():
    W, H = 140, 108
    GROUND = 78
    o = []

    o.append(rect(0, GROUND, W, 10, SLATE_D))

    def tower(x0, x1, top):
        parts = [rect(x0, top, x1 - x0, GROUND - top, SLATE)]
        for cx in range(x0, x1 - 2, 6):
            parts.append(rect(cx, top - 4, 4, 4, SLATE))
        parts.append(rect(x0, top, x1 - x0, 1, SLATE_L))
        return "".join(parts)

    o.append(tower(40, 100, 34))   # keep
    o.append(tower(20, 40, 26))    # left tower
    o.append(tower(100, 120, 26))  # right tower

    for wx, wy in [(28, 38), (106, 38), (54, 44), (80, 44)]:
        o.append(rect(wx, wy, 5, 7, SLATE_D))

    # gate
    o.append(rect(60, 54, 20, GROUND - 54, SLATE_D))
    o.append(rect(62, 50, 16, 6, SLATE_D))

    # flagpole and flag -- the only colour in the panel
    o.append(rect(69, 8, 1, 26, SLATE_L))
    flag = (rect(70, 10, 6, 11, IT_G) + rect(76, 10, 6, 11, IT_W)
            + rect(82, 10, 6, 11, IT_R))
    o.append(
        f'<g>{flag}<animateTransform attributeName="transform" type="skewY" '
        f'values="0;2.5;0;-2.5;0" dur="4s" repeatCount="indefinite" '
        f'additive="sum"/></g>'
    )

    # label sits below the ground band, on the screen colour, so it stays legible
    o.append(text_centered("WORLD 6-4", W // 2, GROUND + 18, 1, DIM))
    return svg(W, H, "".join(o), "world 6-4, the castle")


# ---------------------------------------------------------------- bonus

def build_bonus():
    W, H = 170, 66
    TRACK = "M 34 26 H 136 A 13 13 0 0 1 136 52 H 34 A 13 13 0 0 1 34 26 Z"
    o = [text_centered("BONUS STAGE", W // 2, 8, 1, GOLD)]

    o.append(f'<path d="{TRACK}" fill="none" stroke="{SLATE_D}" stroke-width="11"/>')
    o.append(f'<path d="{TRACK}" fill="none" stroke="{DIM}" stroke-width="1" '
             f'stroke-dasharray="3 5" opacity="0.5"/>')

    # start/finish, centred on the 11-wide top straight
    for r in range(5):
        for c in range(2):
            if (r + c) % 2 == 0:
                o.append(rect(84 + c * 2, 21 + r * 2, 2, 2, BONE))

    kart = (rect(0, 1, 6, 3, GREEN) + rect(1, 0, 4, 1, GREEN)
            + rect(0, 0, 1, 1, SCREEN) + rect(5, 0, 1, 1, SCREEN)
            + rect(0, 4, 2, 1, SCREEN) + rect(4, 4, 2, 1, SCREEN))
    o.append(
        f'<g><g transform="translate(-3,-2)">{kart}</g>'
        f'<animateMotion dur="5.5s" repeatCount="indefinite" path="{TRACK}"/></g>'
    )
    return svg(W, H, "".join(o), "bonus stage, a kart lap")


# ---------------------------------------------------------------- continue

def build_continue():
    W, H = 120, 78
    o = []
    o.append(f'<rect x="4" y="4" width="{W - 8}" height="{H - 8}" fill="none" '
             f'stroke="{SLATE}" stroke-width="1"/>')
    o.append(f'<rect x="7" y="7" width="{W - 14}" height="{H - 14}" fill="none" '
             f'stroke="{SLATE_D}" stroke-width="1"/>')

    o.append(text_centered("CONTINUE?", W // 2, 14, 1, BONE))
    # ">" is drawn by the font as a solid triangle, so pass the raw character --
    # it never reaches the SVG as markup, only as rects.
    o.append(f'<g>{text(">", 36, 30, 1, GREEN)}{blink("0.9s")}</g>')
    o.append(text("YES", 46, 30, 1, GREEN))
    o.append(text("NO", 46, 40, 1, DIM))

    # arcade countdown: 9 down to 0, one second each, looping
    x0 = (W - text_width("00", 2)) // 2
    o.append(text("0", x0, 54, 2, GOLD))
    for i, d in enumerate("9876543210"):
        o.append(
            f'<g opacity="0">{text(d, x0 + 12, 54, 2, GOLD)}'
            f'<animate attributeName="opacity" values="1;1;0;0" '
            f'keyTimes="0;0.099;0.1;1" dur="10s" begin="{i}s" '
            f'repeatCount="indefinite"/></g>'
        )
    return svg(W, H, "".join(o), "continue? countdown")


# ---------------------------------------------------------------- copy

INNER = 60   # characters between the box walls
LABEL = 12   # width of the label column

POWER_UPS = [
    ("Go", "first reach, every time"),
    ("Java", "fluent"),
    ("Python", "fluent"),
    ("design", "greenfield, or someone else's decade-old"),
    ("", "codebase - both are fine"),
    ("security", "authn / authz"),
    ("AI tools", "used properly, not decoratively"),
]

CAREER = [
    dict(world="1-1", name="AMADEUS", where="Nice, FR",
         sub="travel tech at global scale - the first level",
         rows=[("STAGE", "learn how big systems actually behave"),
               ("STAKES", "the world's flight bookings")],
         marks=[("CLEARED", "two years abroad, fundamentals banked")]),
    dict(world="2-1", name="OPEN REPLY", where="Italy",
         sub="consulting and startups, back home",
         rows=[("STAGE", "many codebases, every maturity level"),
               ("STAKES", "clients who needed it working yesterday")],
         marks=[("CLEARED", "useful in someone else's codebase by week one")]),
    dict(world="3-1", name="ALPIAN", where="Switzerland",
         sub="Switzerland's first digital private bank",
         rows=[("STAGE", "build a bank from zero"),
               ("ROLE", "authn / authz, across the whole platform"),
               ("STAKES", "other people's money")],
         marks=[("FLAGPOLE", "Oct 2022 - live"),
                ("RECORD", "zero downtime since. still standing."),
                ("COINS", "hundreds of millions managed")]),
    dict(world="4-1", name="FACEIT", where="2024",
         sub="a new revenue line, from nothing",
         rows=[("STAGE", "the Shop initiative"),
               ("ROLE", "zero-cost digital assets"),
               ("STAKES", "the company's cashflow")],
         marks=[("TIME", "06:59   €0 -> €500,000        NEW RECORD!")]),
    dict(world="5-1", name="SYSDIG", where="senior SWE",
         sub="cloud security, at volume",
         rows=[("STAGE", "near-realtime cloud workload analysis"),
               ("STAKES", "everyone else's cloud")],
         marks=[("RECORD", "scaled to millions of records per day"),
                ("COINS", "IaC scanning shipped to GA")]),
]

BONUS = [
    ("karting", "amateur, and actually driving"),
    ("watching", "F1, MotoGP, anything on wheels"),
    ("words", "reading and writing, technical and creative"),
]


def _fit(s, width, where):
    if len(s) > width:
        raise SystemExit(f"copy too long ({len(s)} > {width}) in {where}: {s!r}")
    return s.ljust(width)


def row(s, where="row"):
    return "║" + _fit(s, INNER, where) + "║"


def split(left, right, where="header"):
    pad = INNER - len(left) - len(right) - 2
    if pad < 1:
        raise SystemExit(f"header too wide in {where}: {left!r} {right!r}")
    return "║" + left + " " * pad + right + "  " + "║"


TOP = "╔" + "═" * INNER + "╗"
MID = "╠" + "═" * INNER + "╣"
BOT = "╚" + "═" * INNER + "╝"


def field(label, value, bullet=False):
    lead = "  > " if bullet else "  "
    width = LABEL - (2 if bullet else 0)
    return row(lead + label.ljust(width) + value, label)


def card(head_left, head_right, sub, blocks):
    out = [TOP, split("  " + head_left, head_right), row("  " + sub), MID]
    for i, block in enumerate(blocks):
        if i:
            out.append(MID)
        out.extend(block)
    out.append(BOT)
    return "\n".join(out)


def world_card(w):
    plain = [field(k, v) for k, v in w["rows"]]
    marks = [field(k, v, bullet=True) for k, v in w["marks"]]
    return card(f"WORLD {w['world']}   >  {w['name']}", w["where"], w["sub"],
                [plain, marks])


# ---------------------------------------------------------------- readme

def img(src, alt, width):
    return f'<img src="{src}" width="{width}" alt="{alt}">'


def build_readme():
    player = card("PLAYER 1   >  greenPlumber", "", "backend, mostly",
                  [[row("  POWER-UPS")] + [field(k, v) for k, v in POWER_UPS]])
    bonus = card("BONUS STAGE   >  OFF THE CLOCK", "", "the other half",
                 [[field(k, v) for k, v in BONUS]])

    worlds = "\n\n".join(f"```\n{world_card(w)}\n```" for w in CAREER)

    return f"""<div align="center">

{img("assets/title.svg", "greenPlumber - press start", 760)}

</div>

```
{player}
```

<div align="center">

{img("assets/worldmap.svg", "career world map", 760)}

</div>

{worlds}

<div align="center">

{img("assets/castle.svg", "world 6-4, the castle", 320)}

</div>

> **WORLD 6-4 — public service.**
> Cybersecurity, for the country.
>
> Every level before this one was about reaching the castle.
> This one is about holding it.

<div align="center">

{img("assets/bonus-track.svg", "bonus stage", 460)}

</div>

```
{bonus}
```

<div align="center">

{img("assets/continue.svg", "continue?", 260)}

<sub>no pitch, nothing to sell — thanks for playing.</sub>

</div>
"""


# ---------------------------------------------------------------- main

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(here)
    assets = os.path.join(repo, "assets")
    os.makedirs(assets, exist_ok=True)

    for name, fn in [("title", build_title), ("worldmap", build_worldmap),
                     ("castle", build_castle), ("bonus-track", build_bonus),
                     ("continue", build_continue)]:
        path = os.path.join(assets, f"{name}.svg")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(fn())
        print(f"wrote assets/{name}.svg ({os.path.getsize(path)} bytes)")

    readme = os.path.join(repo, "README.md")
    with open(readme, "w", encoding="utf-8") as fh:
        fh.write(build_readme())
    print(f"wrote README.md ({os.path.getsize(readme)} bytes)")


if __name__ == "__main__":
    main()
