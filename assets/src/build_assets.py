"""Build every animated pixel-art SVG used by the README.

    python assets/src/build_assets.py        (run from the repository root)

Outputs go to assets/*.svg. Only the standard library + Pillow (for the satellite panel) are needed.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from pixelkit import (P, outline, norm, sprite_paths, size, text_pixels, text_width, text_svg,
                      rects_to_path, svg_doc, _F)
import sprites as S

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "assets")
os.makedirs(OUT, exist_ok=True)


def save(name, svg):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  {name:28s} {len(svg)/1024:7.1f} KB")


def spr(grid, pal, x, y, s=4, flip=False, ol=True):
    g = outline(norm(grid)) if ol else norm(grid)
    return sprite_paths(g, pal, x, y, s, flip)


def spr_size(grid, s=4, ol=True):
    w, h = size(grid)
    return (w + (2 if ol else 0)) * s, (h + (2 if ol else 0)) * s


def rect(x, y, w, h, fill, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" {extra}/>'


def squares_path(sq, fill, extra=""):
    return f'<path fill="{fill}" d="{rects_to_path(sq)}" {extra}/>'


def title_text(s, x, y, scale, rows_pal, shadow="#0d1117", spacing=1, per_letter_cls=None, depth=1,
               ol_col="#0b2545"):
    """Retro title: per-row colour bands, a 1-px dark outline and a chunky drop shadow.
    Each letter is wrapped in its own <g> so it can be animated separately."""
    out = []
    cx = x
    for i, ch in enumerate(s.upper()):
        g = _F.get(ch, _F["?"])
        gw = len(g[0])
        if ch != " ":
            ring = outline(g, "O", diag=True)
            by, ol_sq, sh_sq = {}, [], []
            for ry, row in enumerate(ring):
                for rx, c in enumerate(row):
                    if c == ".":
                        continue
                    px, py = cx + (rx - 1) * scale, y + (ry - 1) * scale
                    for d in range(1, depth + 1):
                        sh_sq.append((px + d * scale // 2, py + d * scale // 2, scale, scale))
                    if c == "O":
                        ol_sq.append((px, py, scale, scale))
                    else:
                        by.setdefault(rows_pal[ry - 1], []).append((px, py, scale, scale))
            body = squares_path(sh_sq, shadow) + squares_path(ol_sq, ol_col)
            body += "".join(squares_path(sq, col) for col, sq in by.items())
            cls = f' class="{per_letter_cls}" style="animation-delay:{i*0.09:.2f}s"' if per_letter_cls else ""
            out.append(f"<g{cls}>{body}</g>")
        cx += (gw + spacing) * scale
    return "".join(out)


def text_ol(s, x, y, scale, fill, ol_col="#0b2545", shadow=None, spacing=1):
    """pixel text with a crisp 1-px outline (reads on any background)."""
    return title_text(s, x, y, scale, [fill] * 7, shadow=shadow or ol_col, spacing=spacing, depth=1, ol_col=ol_col)


def frames_css(prefix, period):
    """two-frame flip-book classes."""
    return (f".{prefix}a{{animation:{prefix}a {period}s steps(1,end) infinite}}"
            f".{prefix}b{{opacity:0;animation:{prefix}b {period}s steps(1,end) infinite}}"
            f"@keyframes {prefix}a{{0%{{opacity:1}}50%{{opacity:0}}100%{{opacity:0}}}}"
            f"@keyframes {prefix}b{{0%{{opacity:0}}50%{{opacity:1}}100%{{opacity:1}}}}")


def dither_band(y, h, top, bottom, W, s=4, frac=0.5, seed=0):
    """band of colour `top` with a checker-dither row blending into `bottom`."""
    out = rect(0, y, W, h, top)
    sq = []
    for x in range(0, W, s * 2):
        sq.append((x + (s if (x // (s * 2)) % 2 else 0), y + h - s, s, s))
    out += squares_path([(x, yy, s, s) for x, yy, _, _ in sq], bottom)
    return out


# ════════════════════════════════════════════════════════════════════════
#  HERO BANNER
# ════════════════════════════════════════════════════════════════════════

def hero():
    W, H = 960, 330
    rnd = random.Random(7)
    body = []
    css = []

    # sky bands (dithered) — bright daytime Jurassic sky
    bands = [(0, 40, "#2b7de0"), (40, 30, "#3a8ee9"), (70, 28, "#4c9ff0"), (98, 26, "#5fb0f5"),
             (124, 24, "#74c0f8"), (148, 22, "#8bcffb"), (170, 22, "#a3dcfd"), (192, 22, "#bce7fe"),
             (214, 66, "#d6f1ff")]
    for i, (y, h, c) in enumerate(bands):
        nxt = bands[i + 1][2] if i + 1 < len(bands) else c
        body.append(dither_band(y, h, c, nxt, W))

    # sparkles high in the sky
    star_groups = {0: [], 1: [], 2: []}
    for _ in range(26):
        x, y = rnd.randrange(0, W, 4), rnd.randrange(4, 60, 4)
        star_groups[rnd.randrange(3)].append((x, y, 4, 4))
    for k, sq in star_groups.items():
        body.append(squares_path(sq, "#e8f7ff", f'class="tw" style="animation-delay:{k*0.8}s"'))
    css.append(".tw{animation:tw 2.4s steps(2,end) infinite}@keyframes tw{0%,100%{opacity:.9}50%{opacity:.1}}")

    # sun (pixel disc) + glow
    cx, cy, r = 708, 172, 34
    sun, rim, glow = [], [], []
    for yy in range(cy - r - 12, cy + r + 12, 4):
        for xx in range(cx - r - 12, cx + r + 12, 4):
            d = math.hypot(xx + 2 - cx, yy + 2 - cy)
            if d <= r - 6:
                sun.append((xx, yy, 4, 4))
            elif d <= r:
                rim.append((xx, yy, 4, 4))
            elif d <= r + 8 and (xx // 4 + yy // 4) % 2 == 0:
                glow.append((xx, yy, 4, 4))
    body.append(squares_path(glow, "#fff8d6", 'class="glow"'))
    body.append(squares_path(rim, P["sun"]))
    body.append(squares_path(sun, "#fff3b0"))
    body.append(squares_path([(cx - 12, cy - 16, 8, 8), (cx - 16, cy - 8, 4, 4)], "#ffffff"))
    css.append(".glow{animation:glow 3s steps(3,end) infinite}@keyframes glow{0%,100%{opacity:.3}50%{opacity:1}}")

    # clouds (fluffy white)
    def cloud(x, y, w, col, col2):
        sq, sh = [], []
        for i in range(0, w, 4):
            t = i / w
            hgt = int((math.sin(t * math.pi) * 4 + (1 if (i // 12) % 2 else 0))) * 4 + 4
            sq.append((x + i, y - hgt, 4, hgt))
            sh.append((x + i, y, 4, 4))
        return squares_path(sq, col) + squares_path(sh, col2)
    cl = cloud(40, 176, 104, "#ffffff", "#cde9fb") + cloud(300, 150, 76, "#ffffff", "#cde9fb") + \
        cloud(520, 196, 124, "#ffffff", "#cde9fb") + cloud(800, 118, 64, "#f4fbff", "#cde9fb")
    body.append(f'<g class="drift">{cl}<g transform="translate(960 0)">{cl}</g></g>')
    css.append(".drift{animation:drift 120s linear infinite}@keyframes drift{to{transform:translateX(-960px)}}")

    # meteor
    body.append(f'<g class="met">{spr(S.METEOR, S.METEOR_PAL, 40, -40, 3)}</g>')
    css.append(".met{opacity:0;animation:met 9s steps(30,end) infinite}"
               "@keyframes met{0%{opacity:1;transform:translate(0,0)}10%{opacity:1;transform:translate(330px,165px)}"
               "10.1%,100%{opacity:0;transform:translate(330px,165px)}}")

    # far mountains (static, distant)
    def ridge(base, amp, col, top_col, seed, step=8, phase=0):
        sq, tops = [], []
        for x in range(0, W, step):
            t = x / W * 2 * math.pi
            h = base - amp * (0.55 * math.sin(3 * t + phase) + 0.3 * math.sin(7 * t + seed) + 0.15 * math.sin(13 * t))
            h = int(h // 4 * 4)
            sq.append((x, h, step, 280 - h))
            tops.append((x, h, step, 4))
        return squares_path(sq, col) + squares_path(tops, top_col)
    body.append(ridge(214, 26, "#8dbfe3", "#b3d9f2", 1.3))

    # volcano
    vx, vtop, vbase = 846, 142, 262
    vol, lit, lava = [], [], []
    for y in range(vtop, vbase, 4):
        hw = 18 + int((y - vtop) * 0.95) // 4 * 4
        vol.append((vx - hw, y, hw * 2, 4))
        lit.append((vx - hw, y, max(4, hw // 2) // 4 * 4, 4))
    lava += [(vx - 14, vtop, 28, 4), (vx - 10, vtop + 4, 20, 4)]
    streams = []
    for sx0, dirn in ((vx - 4, -1), (vx + 6, 1)):
        x = sx0
        for y in range(vtop + 8, vtop + 70, 4):
            streams.append((x, y, 4, 4))
            if rnd.random() < 0.45:
                x += dirn * 4
    body.append(squares_path(vol, "#5b6f95") + squares_path(lit, "#7a8fb5"))
    body.append(squares_path(lava, P["lava2"], 'class="lava"') + squares_path(streams, P["lava"], 'class="lava"'))
    css.append(".lava{animation:lava 1.2s steps(2,end) infinite}@keyframes lava{50%{fill:#ffd166}}")
    for i in range(6):
        sz = rnd.choice((8, 12, 16))
        body.append(f'<rect class="smoke" x="{vx - sz//2 + rnd.randrange(-8, 9, 4)}" y="{vtop - sz}" width="{sz}" height="{sz}" '
                    f'fill="#eef6ff" style="animation-delay:{i*0.7:.1f}s"/>')
    css.append(".smoke{opacity:0;animation:smoke 4.2s steps(14,end) infinite}"
               "@keyframes smoke{0%{opacity:.85;transform:translate(0,0)}100%{opacity:0;transform:translate(-36px,-84px)}}")

    # nearer hills
    body.append(ridge(242, 12, "#6aa6d4", "#8dbfe3", 4.1, step=8, phase=1.1))

    # ── mid layer: jungle band (scrolls slowly) ──
    PALM_D = dict(S.PALM_PAL, G="#1f5a43", g="#174a36", T="#4a3423", t="#3a2819", c="#5a3a22")
    FERN_D = dict(S.FERN_PAL, G="#1f5a43", g="#174a36")
    mid = [rect(0, 252, W, 28, "#1b4d38"), rect(0, 252, W, 4, "#2d6a4f")]
    for x in range(0, W, 8):
        if rnd.random() < 0.5:
            mid.append(rect(x, 248, 4, 4, "#2d6a4f"))
    for px in (40, 250, 470, 690, 880):
        pw, ph = spr_size(S.PALM, 4)
        mid.append(spr(S.PALM, PALM_D, px, 256 - ph + 4, 4))
    for fx in (160, 380, 600, 790):
        fw, fh = spr_size(S.FERN, 4)
        mid.append(spr(S.FERN, FERN_D, fx, 256 - fh + 4, 4))
    mid_s = "".join(mid)
    body.append(f'<g class="midscroll">{mid_s}<g transform="translate(960 0)">{mid_s}</g></g>')
    css.append(".midscroll{animation:scroll 30s steps(240,end) infinite}@keyframes scroll{to{transform:translateX(-960px)}}")

    # sauropod walking in the jungle
    sw, sh = spr_size(S.SAURO_A, 4)
    sx, sy = 96, 262 - sh
    body.append(f'<g class="bob2"><g class="sa">{spr(S.SAURO_A, S.ORANGE, sx, sy)}</g>'
                f'<g class="sb">{spr(S.SAURO_B, S.ORANGE, sx, sy)}</g></g>')
    css.append(frames_css("s", 0.9))
    css.append(".bob2{animation:bob2 .9s steps(1,end) infinite}@keyframes bob2{50%{transform:translateY(-4px)}}")

    # pterodactyls crossing the sky
    for i, (yy, dur, delay, pal, sc) in enumerate(((156, 16, 0, S.PURPLE, 3), (196, 22, 7, S.PINK, 2), (176, 19, 12, S.PURPLE, 2))):
        pu = spr(S.PTERO_UP, pal, 0, yy, sc)
        pd = spr(S.PTERO_DOWN, pal, 0, yy, sc)
        body.append(f'<g class="fly" style="animation-duration:{dur}s;animation-delay:-{delay}s">'
                    f'<g class="pa">{pu}</g><g class="pb">{pd}</g></g>')
    css.append(frames_css("p", 0.5))
    css.append(".fly{animation:fly 16s steps(160,end) infinite}"
               "@keyframes fly{0%{transform:translate(-90px,0)}50%{transform:translate(470px,-16px)}100%{transform:translate(1060px,0)}}")

    # ── foreground ground (scrolls fast) ──
    g = [rect(0, 280, W, 50, "#5a3a22"), rect(0, 280, W, 8, P["g3"]), rect(0, 288, W, 4, P["g1"])]
    tufts, specks, dark = [], [], []
    for x in range(0, W, 4):
        if rnd.random() < 0.35:
            tufts.append((x, 276, 4, 4))
    for _ in range(140):
        specks.append((rnd.randrange(0, W, 4), rnd.randrange(296, 330, 4), 4, 4))
    for _ in range(60):
        dark.append((rnd.randrange(0, W, 4), rnd.randrange(296, 330, 4), 8, 4))
    g += [squares_path(tufts, P["g3"]), squares_path(dark, "#4a2f1b"), squares_path(specks, "#7a5230")]
    for bx in (60, 420, 760):
        g.append(spr(S.BONE, S.BONE_PAL, bx, 302, 2))
    for ax in (250, 610):
        g.append(spr(S.AMMONITE, S.AMMO_PAL, ax, 298, 2))
    g.append(spr(S.SKULL, S.SKULL_PAL, 880, 300, 2))
    gs = "".join(g)
    body.append(f'<g class="gscroll">{gs}<g transform="translate(960 0)">{gs}</g></g>')
    css.append(".gscroll{animation:scroll 7s steps(240,end) infinite}")

    # T-rex running + baby following
    tw, th = spr_size(S.TREX_A, 4)
    tx, ty = 560, 284 - th
    body.append(f'<g class="run"><g class="ta">{spr(S.TREX_A, S.GREEN, tx, ty)}</g>'
                f'<g class="tb">{spr(S.TREX_B, S.GREEN, tx, ty)}</g></g>')
    css.append(frames_css("t", 0.32))
    css.append(".run{animation:run .32s steps(1,end) infinite}@keyframes run{50%{transform:translateY(-4px)}}")
    bw, bh = spr_size(S.BABY, 4)
    body.append(f'<g class="hop">{spr(S.BABY, S.PINK, 470, 284 - bh)}</g>')
    css.append(".hop{animation:hop .64s steps(4,end) infinite}@keyframes hop{0%,100%{transform:translateY(0)}50%{transform:translateY(-16px)}}")
    # dust puffs behind the T-rex
    body.append(f'<g class="dust">{squares_path([(tx - 8, 276, 8, 8), (tx - 20, 272, 4, 4)], "#c9a27a")}</g>')
    css.append(".dust{animation:dust .32s steps(2,end) infinite}@keyframes dust{0%{opacity:.9;transform:translateX(0)}100%{opacity:0;transform:translateX(-16px)}}")

    # ── title + HUD ──
    rows = ["#fff3b0", P["sun"], P["sun"], P["dusk4"], P["dusk4"], P["dusk3"], P["dusk3"]]
    title = "DSBA JURASSIC"
    sc = 7
    tw_ = text_width(title, sc)
    body.append(title_text(title, (W - tw_) // 2, 44, sc, rows, shadow="#0b2545", per_letter_cls="wave", depth=2))
    css.append(".wave{animation:wave 2.4s steps(3,end) infinite}"
               "@keyframes wave{0%,30%,100%{transform:translateY(0)}15%{transform:translateY(-8px)}}")
    sub = "MULTI-MODAL DEEP LEARNING FOR THAI FOSSILS"
    body.append(text_ol(sub, (W - text_width(sub, 2)) // 2, 118, 2, "#ffffff"))

    hud_l = "1UP"
    body.append(text_svg(hud_l, 16, 12, 2, P["gold"], shadow="#000"))
    for i in range(3):
        body.append(spr(S.HEART, S.HEART_PAL, 56 + i * 20, 10, 2, ol=False))
    hs = "HI-SCORE 99.09%"
    body.append(text_svg(hs, W - 16 - text_width(hs, 2), 12, 2, P["gold"], shadow="#000"))
    ps = "▶ PRESS START"
    body.append(f'<g class="blink">{text_svg(ps, (W - text_width(ps, 2)) // 2, 12, 2, "#ffffff", shadow="#000")}</g>')
    css.append(".blink{animation:blink 1.1s steps(1,end) infinite}@keyframes blink{50%{opacity:0}}")

    save("hero.svg", svg_doc(W, H, "".join(body), "".join(css), "DSBA Jurassic",
                             "Animated pixel-art banner: a T-rex runs through a Jurassic sunset with a sauropod, pterodactyls and a volcano."))




# ════════════════════════════════════════════════════════════════════════
#  shared sky-blue scenery helpers
# ════════════════════════════════════════════════════════════════════════
NAVY = "#0b2545"
SKY = ["#3a8ee9", "#4c9ff0", "#5fb0f5", "#74c0f8", "#8bcffb", "#a3dcfd", "#bce7fe", "#d6f1ff"]


def sky_bg(W, H, top=0, colors=None):
    colors = colors or SKY
    n = len(colors)
    out = []
    bh = max(4, (H - top) // n // 4 * 4)
    y = top
    for i, c in enumerate(colors):
        h = bh if i < n - 1 else H - y
        nxt = colors[i + 1] if i + 1 < n else c
        out.append(dither_band(y, h, c, nxt, W))
        y += h
    return "".join(out)


def cloud_sq(x, y, w, col="#ffffff", col2="#cde9fb", amp=3):
    sq, sh = [], []
    for i in range(0, w, 4):
        t = i / w
        hgt = int((math.sin(t * math.pi) * amp + (1 if (i // 12) % 2 else 0))) * 4 + 4
        sq.append((x + i, y - hgt, 4, hgt))
        sh.append((x + i, y, 4, 4))
    return squares_path(sq, col) + squares_path(sh, col2)


def grass(y, W, rnd, h=None, dirt=True):
    out = [rect(0, y, W, 8, P["g3"]), rect(0, y + 8, W, 4, P["g1"])]
    tufts = [(x, y - 4, 4, 4) for x in range(0, W, 4) if rnd.random() < 0.3]
    out.append(squares_path(tufts, P["g3"]))
    if dirt:
        out.append(rect(0, y + 12, W, 400, "#6b4f2a"))
        sp = [(rnd.randrange(0, W, 4), rnd.randrange(y + 16, y + 60, 4), 4, 4) for _ in range(W // 10)]
        out.append(squares_path(sp, "#8a6a3f"))
    return "".join(out)


def frame(x, y, w, h, fill="#ffffff", border=NAVY, shade="#cfe3f5", light="#ffffff", b=4):
    """RPG dialogue box with notched pixel corners."""
    out = [rect(x + b, y, w - 2 * b, h, border), rect(x, y + b, w, h - 2 * b, border),
           rect(x + b, y + b, w - 2 * b, h - 2 * b, fill)]
    out.append(rect(x + b, y + h - 2 * b, w - 2 * b, b, shade))
    out.append(rect(x + w - 2 * b, y + b, b, h - 2 * b, shade))
    out.append(rect(x + b, y + b, w - 3 * b, b, light))
    return "".join(out)


def fit_scale(grid, max_w, max_h):
    w, h = size(grid)
    return max(1, min(4, max_h // (h + 2), max_w // (w + 2)))


# ════════════════════════════════════════════════════════════════════════
#  SECTION BANNERS
# ════════════════════════════════════════════════════════════════════════
SECTIONS = [
    ("abstract", "PROJECT ABSTRACT", "STAGE 01", S.AMMONITE, S.AMMO_PAL, "#ffc300"),
    ("objectives", "OBJECTIVES", "STAGE 02", S.STAR, S.STAR_PAL, "#ffc300"),
    ("problem", "THE PROBLEM", "STAGE 03", S.METEOR, S.METEOR_PAL, "#ff5a36"),
    ("overview", "PROJECT OVERVIEW", "STAGE 04", S.TRICERA, S.ORANGE, "#f4a261"),
    ("context", "RESEARCH CONTEXT", "STAGE 05", S.SKULL, S.SKULL_PAL, "#f4e7c9"),
    ("pipeline", "CRISP-DM PIPELINE", "STAGE 06", S.FOOT, S.FOOT_PAL, "#95d5b2"),
    ("architecture", "MODEL ARCHITECTURE", "STAGE 07", S.STEGO, S.YELLOW, "#ffd166"),
    ("satellite", "SATELLITE VIEW", "STAGE 08", S.SATELLITE, S.SAT_PAL, "#4cc9f0"),
    ("results", "RESULTS & SCORES", "STAGE 09", S.TROPHY, S.TROPHY_PAL, "#ffc300"),
    ("applications", "APPLICATIONS", "STAGE 10", S.PTERO_UP, S.PURPLE, "#b388eb"),
    ("conclusions", "CONCLUSIONS", "STAGE 11", S.EGG_HATCH, S.EGG_PAL, "#95d5b2"),
    ("roadmap", "FUTURE ROADMAP", "STAGE 12", S.EGG, S.EGG_PAL, "#f4e7c9"),
    ("repo", "REPO MAP", "STAGE 13", S.BONE, S.BONE_PAL, "#f4e7c9"),
    ("start", "GETTING STARTED", "STAGE 14", S.TREX_A, S.GREEN, "#52b788"),
    ("team", "THE TEAM", "STAGE 15", S.BABY, S.PINK, "#ff85a1"),
    ("license", "LICENSE & CITATION", "BONUS", S.HEART, S.HEART_PAL, "#e63946"),
]


def section_banner(key, title, stage, grid, pal, accent, idx):
    W, H = 960, 84
    rnd = random.Random(100 + idx)
    body, css = [], []
    body.append(sky_bg(W, H, colors=["#5fb0f5", "#74c0f8", "#8bcffb", "#a3dcfd", "#bce7fe"]))
    cl = cloud_sq(rnd.randrange(360, 520, 4), 28, 72) + cloud_sq(rnd.randrange(620, 760, 4), 44, 56, amp=2)
    body.append(f'<g class="drift">{cl}<g transform="translate(960 0)">{cl}</g></g>')
    css.append(".drift{animation:drift 60s linear infinite}@keyframes drift{to{transform:translateX(-960px)}}")
    body.append(grass(H - 12, W, rnd, dirt=False))
    # icon on a little pedestal
    s = fit_scale(grid, 88, 56)
    iw, ih = spr_size(grid, s)
    ix, iy = 20 + (88 - iw) // 2, H - 12 - ih
    body.append(f'<g class="bob">{spr(grid, pal, ix, iy, s)}</g>')
    css.append(".bob{animation:bob 1.2s steps(2,end) infinite}@keyframes bob{50%{transform:translateY(-4px)}}")
    # title
    body.append(text_ol(title, 124, 22, 4, "#ffffff", ol_col=NAVY))
    # stage badge + blinking cursor
    bw = text_width(stage, 2) + 24
    bx = W - bw - 24
    body.append(frame(bx, 24, bw, 28, fill=accent, border=NAVY, shade=accent, light="#ffffff"))
    body.append(text_svg(stage, bx + 12, 31, 2, NAVY))
    cx = 124 + text_width(title, 4) + 16
    body.append(f'<g class="blink">{text_ol("▶", cx, 26, 3, P["gold"], ol_col=NAVY)}</g>')
    css.append(".blink{animation:blink 1s steps(1,end) infinite}@keyframes blink{50%{opacity:0}}")
    # frame border
    body.append(f'<path fill="{NAVY}" d="M0 0h{W}v4h-{W}zM0 {H-4}h{W}v4h-{W}zM0 0h4v{H}h-4zM{W-4} 0h4v{H}h-4z"/>')
    save(f"sec_{key}.svg", svg_doc(W, H, "".join(body), "".join(css), title.title(), f"Pixel-art section banner: {title.title()}"))


# ════════════════════════════════════════════════════════════════════════
#  DIVIDERS
# ════════════════════════════════════════════════════════════════════════

def divider_run():
    W, H = 960, 56
    rnd = random.Random(21)
    body, css = [], []
    body.append(rect(0, 44, W, 4, P["g3"]) + rect(0, 48, W, 4, P["g1"]) + rect(0, 52, W, 4, "#6b4f2a"))
    body.append(squares_path([(x, 40, 4, 4) for x in range(0, W, 4) if rnd.random() < 0.3], P["g3"]))
    for bx in (140, 380, 620, 860):
        body.append(spr(S.BONE, S.BONE_PAL, bx, 34, 1))
    bw, bh = spr_size(S.BABY, 3)
    dino = spr(S.BABY, S.PINK, 0, 44 - bh, 3)
    body.append(f'<g class="go"><g class="hop">{dino}</g></g>')
    css.append(".go{animation:go 10s steps(250,end) infinite}@keyframes go{from{transform:translateX(-50px)}to{transform:translateX(1000px)}}")
    css.append(".hop{animation:hop .5s steps(4,end) infinite}@keyframes hop{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}")
    save("div_run.svg", svg_doc(W, H, "".join(body), "".join(css), "divider", "A baby dinosaur hops along the grass"))


def divider_fly():
    W, H = 960, 56
    rnd = random.Random(22)
    body, css = [], []
    body.append(rect(0, 44, W, 4, P["g3"]) + rect(0, 48, W, 4, P["g1"]) + rect(0, 52, W, 4, "#6b4f2a"))
    for fx in range(20, W, 110):
        body.append(spr(S.FERN, S.FERN_PAL, fx + rnd.randrange(0, 40, 4), 22, 2))
    pu, pd = spr(S.PTERO_UP, S.BLUE, 0, 2, 2), spr(S.PTERO_DOWN, S.BLUE, 0, 2, 2)
    body.append(f'<g class="fly"><g class="pa">{pu}</g><g class="pb">{pd}</g></g>')
    css.append(frames_css("p", 0.5))
    css.append(".fly{animation:fly 12s steps(240,end) infinite}"
               "@keyframes fly{0%{transform:translate(-60px,4px)}50%{transform:translate(470px,-2px)}100%{transform:translate(1000px,4px)}}")
    save("div_fly.svg", svg_doc(W, H, "".join(body), "".join(css), "divider", "A pterodactyl glides over ferns"))


def divider_eggs():
    W, H = 960, 56
    body, css = [], []
    body.append(rect(0, 44, W, 4, P["g3"]) + rect(0, 48, W, 4, P["g1"]) + rect(0, 52, W, 4, "#6b4f2a"))
    ew, eh = spr_size(S.EGG, 3)
    for i, ex in enumerate(range(60, W, 120)):
        y = 44 - eh
        d = f"animation-delay:{i*0.6:.1f}s"
        body.append(f'<g class="e1" style="{d}">{spr(S.EGG, S.EGG_PAL, ex, y, 3)}</g>'
                    f'<g class="e2" style="{d}">{spr(S.EGG_CRACK, S.EGG_PAL, ex, y, 3)}</g>'
                    f'<g class="e3" style="{d}">{spr(S.EGG_HATCH, S.EGG_PAL, ex, y, 3)}</g>')
    css.append(".e1,.e2,.e3{animation:6s steps(1,end) infinite}.e1{animation-name:e1}.e2{opacity:0;animation-name:e2}.e3{opacity:0;animation-name:e3}"
               "@keyframes e1{0%{opacity:1}40%,100%{opacity:0}}"
               "@keyframes e2{0%{opacity:0}40%{opacity:1}60%,100%{opacity:0}}"
               "@keyframes e3{0%,40%{opacity:0}60%{opacity:1}95%{opacity:1}100%{opacity:0}}")
    save("div_eggs.svg", svg_doc(W, H, "".join(body), "".join(css), "divider", "A row of dinosaur eggs hatching"))


# ════════════════════════════════════════════════════════════════════════
#  RESULTS — RPG STAT CARD
# ════════════════════════════════════════════════════════════════════════

def stats_card():
    W, H = 960, 400
    rnd = random.Random(31)
    body, css = [], []
    body.append(sky_bg(W, H))
    body.append(cloud_sq(700, 40, 96) + cloud_sq(40, 380, 80, amp=2))
    body.append(frame(16, 16, W - 32, H - 32, fill="#ffffff", border=NAVY, shade="#d6ecfb"))
    # portrait
    body.append(frame(40, 40, 200, 200, fill="#bce7fe", border=NAVY, shade="#8bcffb"))
    body.append(rect(44, 196, 192, 40, P["g3"]) + rect(44, 204, 192, 32, "#6b4f2a"))
    tw, th = spr_size(S.TREX_A, 6)
    tx, ty = 40 + (200 - tw) // 2, 200 - th
    body.append(f'<g class="idle"><g class="ta">{spr(S.TREX_A, S.GREEN, tx, ty, 6)}</g>'
                f'<g class="tb">{spr(S.TREX_B, S.GREEN, tx, ty, 6)}</g></g>')
    css.append(frames_css("t", 1.0))
    css.append(".idle{animation:idle 1s steps(1,end) infinite}@keyframes idle{50%{transform:translateY(-6px)}}")
    body.append(text_svg("MULTI-MODAL DNN", 40, 260, 2, NAVY))
    body.append(text_svg("LV.99 FOSSIL HUNTER", 40, 286, 2, "#3a56d4"))
    for i in range(3):
        body.append(spr(S.HEART, S.HEART_PAL, 40 + i * 24, 314, 3, ol=False))
    # bars
    bars = [("PERIOD ACC", 99.09, "#ffc300"), ("SPECIES TOP-5", 89.36, "#52b788"),
            ("SPECIES TOP-3", 78.21, "#4cc9f0"), ("SPECIES TOP-1", 53.64, "#ff85a1"),
            ("APPROACH-1 RF", 81.00, "#f4a261")]
    bx, by0, seg, gap, nseg = 272, 48, 10, 2, 40
    for i, (lab, val, col) in enumerate(bars):
        y = by0 + i * 56
        body.append(text_svg(lab, bx, y, 2, NAVY))
        v = f"{val:.2f}%"
        body.append(text_svg(v, W - 44 - text_width(v, 3), y + 18, 3, NAVY))
        # empty track
        body.append(rect(bx, y + 20, nseg * (seg + gap) + 6, 24, NAVY))
        body.append(squares_path([(bx + 4 + k * (seg + gap), y + 24, seg, 16) for k in range(nseg)], "#dbe7f3"))
        n = round(val / 100 * nseg)
        for k in range(n):
            body.append(f'<rect class="sg{k}" x="{bx + 4 + k * (seg + gap)}" y="{y + 24}" width="{seg}" height="16" fill="{col}"/>')
        body.append(squares_path([(bx + 4 + k * (seg + gap), y + 24, seg, 4) for k in range(n)], "#ffffff",
                                 'opacity=".45"'))
    for k in range(nseg):
        on = 2 + k * 1.4
        css.append(f".sg{k}{{animation:sg{k} 8s steps(1,end) infinite}}"
                   f"@keyframes sg{k}{{0%{{opacity:0}}{on:.1f}%{{opacity:1}}94%{{opacity:1}}95%,100%{{opacity:0}}}}")
    # XP chips
    chips = [("8,756+ RECORDS", "#ffd166"), ("118 FEATURES", "#95d5b2"), ("200+ SPECIES", "#a3dcfd"), ("15 PERIODS", "#ffc2d1")]
    x = 272
    for lab, col in chips:
        w = text_width(lab, 2) + 20
        body.append(frame(x, 340, w, 28, fill=col, border=NAVY, shade=col))
        body.append(text_svg(lab, x + 10, 347, 2, NAVY))
        x += w + 10
    save("stats.svg", svg_doc(W, H, "".join(body), "".join(css), "Results",
                              "RPG-style stat card: period accuracy 99.09%, species top-5 89.36%, top-3 78.21%, top-1 53.64%, approach-1 random forest 81%."))


# ════════════════════════════════════════════════════════════════════════
#  PIPELINE — side-scrolling level map
# ════════════════════════════════════════════════════════════════════════

def pipeline():
    W, H = 960, 300
    rnd = random.Random(41)
    body, css = [], []
    body.append(sky_bg(W, H))
    body.append(cloud_sq(120, 60, 88) + cloud_sq(520, 44, 120) + cloud_sq(820, 70, 72, amp=2))
    body.append(text_ol("WORLD 1 · CRISP-DM", 24, 20, 3, "#ffffff", ol_col=NAVY))
    body.append(grass(212, W, rnd))
    stages = [("1", "COLLECT", "FOSSIL DB", "+ SATELLITE"), ("2", "MERGE", "FUZZY MATCH", "85%+"),
              ("3", "FILL", "3-WAY", "IMPUTATION"), ("4", "FEATURES", "118 TOTAL", "64 NEW"),
              ("5", "TRAIN", "MULTI-MODAL", "DNN"), ("6", "DEPLOY", "GRADIO", "WEB APP")]
    xs = [100 + i * 152 for i in range(6)]
    period = 14.0
    # path dots
    body.append(squares_path([(x, 206, 8, 4) for x in range(40, 900, 16)], "#f4e7c9"))
    for i, (n, name, l1, l2) in enumerate(stages):
        x = xs[i]
        arrive = (0.06 + i * 0.15)
        # flag pole
        body.append(rect(x - 2, 128, 4, 84, NAVY))
        # flag (grey -> colour once the dino arrives)
        flag = f'M{x+2} 128h36v8h-8v8h8v8h-36z'
        pct = arrive * 100
        body.append(f'<path d="{flag}" fill="#8b93a7"/>')
        body.append(f'<path d="{flag}" fill="{["#ffc300", "#4cc9f0", "#95d5b2", "#ff85a1", "#b388eb", "#ff5a36"][i]}" '
                    f'class="fl{i}"/>')
        css.append(f".fl{i}{{animation:fl{i} {period}s steps(1,end) infinite}}"
                   f"@keyframes fl{i}{{0%{{opacity:0}}{pct:.1f}%{{opacity:1}}96%{{opacity:1}}100%{{opacity:0}}}}")
        body.append(text_svg(n, x + 8, 131, 2, NAVY))
        # sign
        sw = 144
        sx = x - sw // 2
        body.append(frame(sx, 228, sw, 66, fill="#ffffff", border=NAVY, shade="#d6ecfb"))
        for li, (t_, col_) in enumerate(((name, "#3a56d4"), (l1, NAVY), (l2, NAVY))):
            body.append(text_svg(t_, sx + (sw - text_width(t_, 2)) // 2, 236 + li * 18, 2, col_))
    # trophy at the end
    body.append(spr(S.TROPHY, S.TROPHY_PAL, 902, 175, 3))
    # walking T-rex with pauses at each stage
    tw, th = spr_size(S.TREX_A, 2)
    keys = []
    for i, x in enumerate(xs):
        a = 0.06 + i * 0.15
        keys.append(f"{a*100 - 6 if i else 0:.1f}%{{transform:translateX({x - 60 - (0 if i else 40)}px)}}")
        keys.append(f"{a*100:.1f}%,{a*100 + 7:.1f}%{{transform:translateX({x - 60}px)}}")
    keys.append(f"100%{{transform:translateX({xs[-1] - 60}px)}}")
    walker = f'<g class="walk"><g class="ta">{spr(S.TREX_A, S.GREEN, 0, 212 - th, 2)}</g><g class="tb">{spr(S.TREX_B, S.GREEN, 0, 212 - th, 2)}</g></g>'
    body.append(walker)
    css.append(frames_css("t", 0.4))
    css.append(f".walk{{animation:walk {period}s steps(120,end) infinite}}@keyframes walk{{{''.join(keys)}}}")
    save("pipeline.svg", svg_doc(W, H, "".join(body), "".join(css), "CRISP-DM pipeline",
                                 "A T-rex walks through six level flags: collect, merge, fill, features, train, deploy."))


# ════════════════════════════════════════════════════════════════════════
#  ARCHITECTURE — data packets flowing through the multi-modal network
# ════════════════════════════════════════════════════════════════════════

def architecture():
    W, H = 960, 460
    rnd = random.Random(51)
    body, css = [], []
    body.append(sky_bg(W, H))
    body.append(cloud_sq(60, 214, 72, amp=2) + cloud_sq(820, 230, 96, amp=2))
    inputs = [("BINARY", "9 DIM", "#ffd166"), ("NUMERIC", "20+ DIM", "#95d5b2"), ("CATEGORY", "EMB 200", "#ffc2d1"),
              ("THAI TEXT", "BERT 768", "#b388eb"), ("IMAGE", "CNN 300²×3", "#4cc9f0")]
    cw, gap, x0, y0 = 172, 12, 26, 20
    centers = []
    for i, (a, b, col) in enumerate(inputs):
        x = x0 + i * (cw + gap)
        body.append(frame(x, y0, cw, 84, fill=col, border=NAVY, shade=col))
        body.append(text_svg(a, x + (cw - text_width(a, 2)) // 2, y0 + 20, 2, NAVY))
        body.append(text_svg(b, x + (cw - text_width(b, 2)) // 2, y0 + 48, 2, NAVY))
        centers.append(x + cw // 2)
    # fusion box
    fx, fy, fw, fh = 230, 190, 500, 112
    for i, c in enumerate(centers):
        # dotted wire down to fusion
        body.append(squares_path([(c - 2, y, 4, 4) for y in range(y0 + 88, 170, 8)], NAVY))
        body.append(squares_path([(min(c, 480) - 2 if c < 480 else 478, 170, abs(c - 480) + 4, 4)], NAVY))
        for k in range(3):
            body.append(f'<rect class="pk" x="{c-4}" y="{y0+88}" width="8" height="8" fill="{inputs[i][2]}" stroke="{NAVY}" stroke-width="2" '
                        f'style="animation-delay:{i*0.3 + k*0.8:.1f}s"/>')
    body.append(squares_path([(478, 170, 4, 20)], NAVY))
    css.append(".pk{opacity:0;animation:pk 2.4s steps(10,end) infinite}"
               "@keyframes pk{0%{opacity:1;transform:translateY(0)}90%{opacity:1;transform:translateY(64px)}100%{opacity:0;transform:translateY(64px)}}")
    body.append(f'<g class="pulse">{frame(fx - 8, fy - 8, fw + 16, fh + 16, fill="#ffc300", border="#ffc300", shade="#ffc300", light="#ffc300")}</g>')
    css.append(".pulse{animation:pulse 1.2s steps(1,end) infinite}@keyframes pulse{50%{opacity:0}}")
    body.append(frame(fx, fy, fw, fh, fill="#ffffff", border=NAVY, shade="#d6ecfb"))
    body.append(text_svg("FUSION LAYERS", fx + (fw - text_width("FUSION LAYERS", 3)) // 2, fy + 14, 3, NAVY))
    for j, (n, frac) in enumerate(((512, 1.0), (256, 0.66), (128, 0.4))):
        bw = int((fw - 170) * frac) // 4 * 4
        bx = fx + 20
        yy = fy + 46 + j * 20
        body.append(rect(bx, yy, bw, 12, ["#3a56d4", "#4c9ff0", "#8bcffb"][j]))
        body.append(text_svg(f"DENSE {n}", fx + fw - 20 - text_width(f"DENSE {n}", 2), yy - 1, 2, NAVY))
    # outputs
    outs = [(fx - 150, "SCI_NAME", "200+ SPECIES", "TOP-5 89.36%", S.SKULL, S.SKULL_PAL),
            (fx + fw - 170, "PERIODFROM", "15 PERIODS", "ACC 99.09%", S.AMMONITE, S.AMMO_PAL)]
    for k, (ox, a, b, c, g, pal) in enumerate(outs):
        oy = 348
        cxo = ox + 160
        body.append(squares_path([(cxo - 2, y, 4, 4) for y in range(fy + fh + 4, oy, 8)], NAVY))
        body.append(f'<rect class="pk2" x="{cxo-4}" y="{fy+fh+4}" width="8" height="8" fill="#ffc300" stroke="{NAVY}" stroke-width="2" style="animation-delay:{k*0.6}s"/>')
        body.append(frame(ox, oy, 320, 92, fill="#ffffff", border=NAVY, shade="#d6ecfb"))
        s = fit_scale(g, 64, 64)
        body.append(spr(g, pal, ox + 14, oy + 16, s))
        body.append(text_svg(a, ox + 96, oy + 16, 2, "#3a56d4"))
        body.append(text_svg(b, ox + 96, oy + 40, 2, NAVY))
        body.append(text_svg(c, ox + 96, oy + 64, 2, "#2d6a4f"))
    css.append(".pk2{opacity:0;animation:pk2 1.6s steps(6,end) infinite}"
               "@keyframes pk2{0%{opacity:1;transform:translateY(0)}90%{opacity:1;transform:translateY(24px)}100%{opacity:0}}")
    save("architecture.svg", svg_doc(W, H, "".join(body), "".join(css), "Model architecture",
                                     "Five input branches (binary, numeric, categorical, Thai BERT text, CNN image) flow into fusion layers 512-256-128 and two outputs: species and geological period."))


# ════════════════════════════════════════════════════════════════════════
#  SATELLITE VIEW — pixelated ESRI / Sentinel-2 tiles with scanning beams
# ════════════════════════════════════════════════════════════════════════
SAT_KNOWN = [("PHAYAO", "1.00"), ("NAN", "0.98"), ("YALA", "0.95"), ("UBON RATCHATHANI", "0.93"), ("PHANG NGA", "0.90")]
SAT_CAND = [("AMNAT CHAROEN", "0.38"), ("ROI ET", "0.38"), ("NARATHIWAT", "0.34"), ("CHAI NAT", "0.34"), ("ANG THONG", "0.33")]
TILE_SRC = 56   # pixels per tile edge (the "pixel art" resolution)
TILE_SC = 3     # upscale factor → 168 px tiles


def make_sat_tiles():
    """cut the 10 ESRI panels + the Sentinel-2 app tile into one tiny pixelated strip (source/sat_tiles.png)."""
    from PIL import Image
    src = os.path.join(os.path.dirname(__file__), "source")
    big = os.path.join(src, "satellite_views_esri.png")
    out = os.path.join(src, "sat_tiles.png")
    if not os.path.exists(big):
        return out
    im = Image.open(big).convert("RGB")
    cols = [(13, 545), (583, 1115), (1153, 1685), (1724, 2256), (2294, 2826)]
    rows = [(96, 628), (654, 1185)]
    tiles = []
    for (y0, y1) in rows:
        cy = (y0 + y1) // 2
        for (x0, x1) in cols:
            cx = (x0 + x1) // 2
            tiles.append(im.crop((cx - 240, cy - 240, cx + 240, cy + 240)))
    tiles.append(Image.open(os.path.join(src, "sentinel2_bangkok_app.png")).convert("RGB"))
    strip = Image.new("RGB", (TILE_SRC * len(tiles), TILE_SRC))
    for i, t in enumerate(tiles):
        t = t.resize((TILE_SRC, TILE_SRC), Image.LANCZOS)
        t = t.quantize(colors=24, method=Image.MEDIANCUT, dither=Image.NONE).convert("RGB")
        strip.paste(t, (i * TILE_SRC, 0))
    strip.save(out, optimize=True)
    return out


def tile_uri(strip, i):
    import base64
    import io
    from PIL import Image
    t = strip.crop((i * TILE_SRC, 0, (i + 1) * TILE_SRC, TILE_SRC)).resize((TILE_SRC * TILE_SC,) * 2, Image.NEAREST)
    t = t.quantize(colors=24, method=Image.MEDIANCUT, dither=Image.NONE)
    buf = io.BytesIO()
    t.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def satellite():
    from PIL import Image
    strip = Image.open(make_sat_tiles()).convert("RGB")
    W = 960
    TS = TILE_SRC * TILE_SC
    rnd = random.Random(61)
    body, css = [], []
    H = 900
    body.append(sky_bg(W, H, colors=["#2b7de0", "#3a8ee9", "#4c9ff0", "#5fb0f5", "#74c0f8", "#8bcffb", "#a3dcfd", "#bce7fe"]))
    body.append(cloud_sq(700, 64, 96) + cloud_sq(40, 470, 80, amp=2) + cloud_sq(820, 480, 88, amp=2))
    # header
    body.append(text_ol("ORBITAL SCAN · THAILAND", 24, 22, 4, "#ffffff", ol_col=NAVY))
    body.append(text_ol("ESRI WORLD IMAGERY · ZOOM 11 · 60×60 KM PER PANEL", 24, 64, 2, "#ffffff", ol_col=NAVY))
    # orbiting satellite + scan beam
    sat = spr(S.SATELLITE, S.SAT_PAL, 0, 6, 2)
    beam = squares_path([(18 - k * 2 + 4, 26 + k * 4, 4 + k * 4, 4) for k in range(10) if k % 2 == 0], "#ffffff", 'opacity=".5"')
    body.append(f'<g class="orbit">{sat}<g class="beam">{beam}</g></g>')
    css.append(".orbit{animation:orbit 16s steps(320,end) infinite}"
               "@keyframes orbit{from{transform:translateX(600px)}to{transform:translateX(1000px)}}"
               ".beam{animation:blink .6s steps(1,end) infinite}@keyframes blink{50%{opacity:0}}")

    def row(y, label, chip, items, offset, col):
        lw = text_width(label, 2) + 24
        body.append(frame(32, y, lw, 30, fill=chip, border=NAVY, shade=chip))
        body.append(text_svg(label, 44, y + 8, 2, NAVY))
        ty = y + 44
        for i, (name, p) in enumerate(items):
            x = 36 + i * (TS + 12)
            body.append(frame(x - 4, ty - 4, TS + 8, TS + 8, fill=NAVY, border=NAVY, shade=NAVY, light=NAVY))
            body.append(f'<image x="{x}" y="{ty}" width="{TS}" height="{TS}" href="{tile_uri(strip, offset + i)}" '
                        f'style="image-rendering:pixelated"/>')
            # scan line
            body.append(f'<rect class="scan" x="{x}" y="{ty}" width="{TS}" height="6" fill="#ffffff" opacity=".55" '
                        f'style="animation-delay:{(offset + i) * 0.37:.2f}s"/>')
            # target marker: pixel crosshair + footprint
            mx, my = x + TS // 2, ty + TS // 2
            ring = [(mx - 16, my - 16, 32, 4), (mx - 16, my + 12, 32, 4), (mx - 16, my - 16, 4, 32), (mx + 12, my - 16, 4, 32)]
            body.append(f'<g class="lock" style="animation-delay:{i*0.2:.1f}s">{squares_path(ring, col)}</g>')
            body.append(spr(S.FOOT, dict(S.FOOT_PAL, F=col, O=NAVY), mx - 11, my - 9, 2))
            # probability badge
            pt = f"P={p}"
            pw = text_width(pt, 2) + 12
            body.append(rect(x, ty, pw, 22, NAVY))
            body.append(text_svg(pt, x + 6, ty + 4, 2, col))
            # name (wrap to two lines if needed)
            words = name.split()
            lines = [name] if text_width(name, 2) <= TS else [" ".join(words[:-1]), words[-1]]
            for li, ln in enumerate(lines):
                body.append(text_ol(ln, x + (TS - text_width(ln, 2)) // 2, ty + TS + 12 + li * 20, 2, "#ffffff", ol_col=NAVY))
        css.append(".scan{animation:scan 3.2s steps(28,end) infinite}"
                   f"@keyframes scan{{0%{{transform:translateY(0);opacity:.6}}90%{{transform:translateY({TS-6}px);opacity:.6}}100%{{opacity:0;transform:translateY({TS-6}px)}}}}"
                   ".lock{animation:lock 1.4s steps(1,end) infinite}@keyframes lock{50%{opacity:0}}")

    row(100, "KNOWN FOSSIL SITES", "#95d5b2", SAT_KNOWN, 0, "#52ff9a")
    row(400, "ML CANDIDATE PROVINCES", "#ffc2a3", SAT_CAND, 5, "#ffb03a")

    # Sentinel-2 live fetch panel from the Gradio app
    y = 706
    body.append(frame(24, y, W - 48, 176, fill="#ffffff", border=NAVY, shade="#d6ecfb"))
    ts2 = 140
    t_uri = tile_uri(strip, 10)
    body.append(rect(40, y + 16, ts2 + 8, ts2 + 8, NAVY))
    body.append(f'<image x="44" y="{y + 20}" width="{ts2}" height="{ts2}" href="{t_uri}" style="image-rendering:pixelated"/>')
    body.append(f'<rect class="scan2" x="44" y="{y+20}" width="{ts2}" height="4" fill="#ffffff" opacity=".6"/>')
    css.append(f".scan2{{animation:scan2 2.6s steps(34,end) infinite}}@keyframes scan2{{to{{transform:translateY({ts2-4}px)}}}}")
    tx = 212
    body.append(text_svg("SENTINEL-2 LIVE FETCH · GRADIO APP", tx, y + 20, 2, "#3a56d4"))
    body.append(text_svg("LAT 13.7563  LON 100.5018  ERA: MESOZOIC", tx, y + 46, 2, NAVY))
    body.append(text_svg("BANDS B02 B03 B04 B08 → RGB + NDVI", tx, y + 70, 2, NAVY))
    # NDVI bar red → green with marker at 0.16
    nd_cols = ["#a50026", "#d73027", "#f46d43", "#fdae61", "#fee08b", "#ffffbf", "#d9ef8b", "#a6d96a", "#66bd63", "#1a9850", "#006837"]
    bx, bw_ = tx, 560
    seg = bw_ // len(nd_cols)
    for k, c in enumerate(nd_cols):
        body.append(rect(bx + k * seg, y + 104, seg, 20, c))
    body.append(f'<path fill="none" stroke="{NAVY}" stroke-width="4" d="M{bx-2} {y+102}h{seg*len(nd_cols)+4}v24h-{seg*len(nd_cols)+4}z"/>')
    mk = bx + int((0.16 + 1) / 2 * seg * len(nd_cols))
    body.append(f'<g class="blink2">{rect(mk - 2, y + 96, 4, 36, NAVY)}{squares_path([(mk - 6, y + 92, 12, 4)], NAVY)}</g>')
    css.append(".blink2{animation:blink 1s steps(1,end) infinite}")
    body.append(text_svg("-1.0", bx, y + 138, 2, NAVY))
    body.append(text_svg("NDVI 0.16", mk - text_width("NDVI 0.16", 2) // 2, y + 138, 2, "#2d6a4f"))
    body.append(text_svg("1.0", bx + seg * len(nd_cols) - text_width("1.0", 2), y + 138, 2, NAVY))
    save("satellite.svg", svg_doc(W, H, "".join(body), "".join(css), "Satellite view",
                                  "Pixelated satellite panels of known Thai fossil provinces and ML-predicted candidates, plus a Sentinel-2 tile fetched by the Gradio app."))


# ════════════════════════════════════════════════════════════════════════
#  TEAM + FOOTER
# ════════════════════════════════════════════════════════════════════════

def team():
    W, H = 960, 200
    rnd = random.Random(71)
    body, css = [], []
    body.append(sky_bg(W, H))
    body.append(cloud_sq(80, 40, 80) + cloud_sq(760, 56, 104, amp=2))
    body.append(text_ol("6 STUDENTS · DSBA · IT KMITL", (W - text_width("6 STUDENTS · DSBA · IT KMITL", 3)) // 2, 16, 3, "#ffffff", ol_col=NAVY))
    body.append(grass(150, W, rnd))
    roles = [("ML LEAD", S.GREEN), ("DATA ENG", S.ORANGE), ("GEOSPATIAL", S.BLUE), ("THAI NLP", S.PURPLE),
             ("WEB APP", S.PINK), ("DOMAIN", S.YELLOW)]
    slot = W // 6
    bw, bh = spr_size(S.BABY, 5)
    for i, (r, pal) in enumerate(roles):
        x = i * slot + (slot - bw) // 2
        body.append(f'<g class="hop" style="animation-delay:{i*0.12:.2f}s">{spr(S.BABY, pal, x, 150 - bh, 5)}</g>')
        body.append(text_svg(r, i * slot + (slot - text_width(r, 2)) // 2, 172, 2, "#fff5d6"))
    css.append(".hop{animation:hop .9s steps(4,end) infinite}@keyframes hop{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-16px)}}")
    save("team.svg", svg_doc(W, H, "".join(body), "".join(css), "The team", "Six baby dinosaurs, one per team role, hop in a wave."))


def footer():
    W, H = 960, 240
    rnd = random.Random(81)
    body, css = [], []
    body.append(sky_bg(W, H))
    cl = cloud_sq(60, 60, 96) + cloud_sq(400, 40, 72, amp=2) + cloud_sq(720, 70, 120)
    body.append(f'<g class="drift">{cl}<g transform="translate(960 0)">{cl}</g></g>')
    css.append(".drift{animation:drift 80s linear infinite}@keyframes drift{to{transform:translateX(-960px)}}")
    t = "THANKS FOR VISITING!"
    body.append(title_text(t, (W - text_width(t, 5)) // 2, 34, 5,
                           ["#fff3b0", P["sun"], P["sun"], P["dusk4"], P["dusk4"], P["dusk3"], P["dusk3"]],
                           shadow=NAVY, per_letter_cls="wave", depth=1))
    css.append(".wave{animation:wave 2.4s steps(3,end) infinite}@keyframes wave{0%,30%,100%{transform:translateY(0)}15%{transform:translateY(-6px)}}")
    sv = "✓ PROGRESS SAVED · 2567 / 2024"
    body.append(f'<g class="blink">{text_ol(sv, (W - text_width(sv, 2)) // 2, 92, 2, "#ffffff", ol_col=NAVY)}</g>')
    css.append(".blink{animation:blink 1.4s steps(1,end) infinite}@keyframes blink{70%{opacity:0}}")
    for px in (8, 860):
        pw, ph = spr_size(S.PALM, 4)
        body.append(spr(S.PALM, S.PALM_PAL, px, 196 - ph + 8, 4))
    body.append(grass(196, W, rnd))
    # parade: stego, tricera, sauro walking together (scrolling across)
    parade = []
    sw, sh = spr_size(S.STEGO, 3)
    parade.append(f'<g class="bob">{spr(S.STEGO, S.YELLOW, 0, 196 - sh, 3)}</g>')
    tw, th = spr_size(S.TRICERA, 3)
    parade.append(f'<g class="bob" style="animation-delay:.2s">{spr(S.TRICERA, S.ORANGE, 130, 196 - th, 3)}</g>')
    bw, bh = spr_size(S.BABY, 3)
    parade.append(f'<g class="hop">{spr(S.BABY, S.PINK, 240, 196 - bh, 3)}</g>')
    tr = f'<g class="ta">{spr(S.TREX_A, S.GREEN, 300, 196 - 72, 3)}</g><g class="tb">{spr(S.TREX_B, S.GREEN, 300, 196 - 72, 3)}</g>'
    parade.append(tr)
    body.append(f'<g class="parade">{"".join(parade)}</g>')
    css.append(frames_css("t", 0.5))
    css.append(".bob{animation:bob .5s steps(1,end) infinite}@keyframes bob{50%{transform:translateY(-3px)}}"
               ".hop{animation:hop .5s steps(4,end) infinite}@keyframes hop{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}"
               ".parade{animation:parade 24s steps(480,end) -9s infinite}@keyframes parade{from{transform:translateX(-420px)}to{transform:translateX(980px)}}")
    save("footer.svg", svg_doc(W, H, "".join(body), "".join(css), "Thanks for visiting",
                               "A dinosaur parade walks across the grass under a light blue sky."))


def build_all():
    hero()
    for i, sec in enumerate(SECTIONS):
        section_banner(*sec, i)
    divider_run()
    divider_fly()
    divider_eggs()
    stats_card()
    pipeline()
    architecture()
    satellite()
    team()
    footer()


if __name__ == "__main__":
    build_all()
