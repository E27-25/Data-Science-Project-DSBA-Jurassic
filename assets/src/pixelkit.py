"""pixelkit — tiny toolkit for hand-made pixel-art SVGs (fonts, sprites, helpers).

Every sprite is a list of strings; each character is a palette key and '.' is empty.
Sprites get an automatic dark outline so they read well on any background.
All drawing is grouped into one <path> per colour, keeping the SVGs small.
"""
from collections import defaultdict

# ─────────────────────────────── palette ────────────────────────────────
P = {
    "ink": "#0d1117",
    "night0": "#0b0e1c", "night1": "#121633", "night2": "#1b2150", "night3": "#2a2f6b",
    "dusk0": "#4b2f6e", "dusk1": "#7a3a6e", "dusk2": "#b8475f", "dusk3": "#e8674a", "dusk4": "#ff9a3c", "sun": "#ffd166",
    "bone": "#f4e7c9", "bone2": "#d8c49b", "bone3": "#a8916a",
    "g0": "#1b4332", "g1": "#2d6a4f", "g2": "#40916c", "g3": "#52b788", "g4": "#95d5b2", "g5": "#d8f3dc",
    "lava": "#ff5a36", "lava2": "#ffb03a", "rock0": "#241a2e", "rock1": "#3b2a45", "rock2": "#5a3f5e",
    "sky": "#4cc9f0", "blue": "#4361ee", "purple": "#7b2cbf", "pink": "#f72585", "gold": "#ffc300", "red": "#e63946",
    "white": "#ffffff", "black": "#000000", "grey": "#8b93a7", "grey2": "#4a5068",
}

# ─────────────────────────────── font 5x7 ───────────────────────────────
_F = {
 "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
 "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
 "C": [".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."],
 "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
 "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
 "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
 "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".####"],
 "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
 "I": ["###", ".#.", ".#.", ".#.", ".#.", ".#.", "###"],
 "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
 "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
 "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
 "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
 "N": ["#...#", "#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#"],
 "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
 "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
 "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
 "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
 "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
 "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
 "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
 "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
 "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."],
 "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
 "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
 "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
 "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."],
 "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
 "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
 "3": ["####.", "....#", "....#", ".###.", "....#", "....#", "####."],
 "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
 "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
 "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
 "7": ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."],
 "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
 "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
 ".": ["..", "..", "..", "..", "..", "##", "##"],
 ",": ["..", "..", "..", "..", "##", ".#", "#."],
 ":": ["..", "##", "##", "..", "##", "##", ".."],
 "-": ["....", "....", "....", "####", "....", "....", "...."],
 "+": [".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."],
 "/": ["....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."],
 "%": ["##..#", "##..#", "...#.", "..#..", ".#...", "#..##", "#..##"],
 "(": ["..#", ".#.", "#..", "#..", "#..", ".#.", "..#"],
 ")": ["#..", ".#.", "..#", "..#", "..#", ".#.", "#.."],
 "!": ["#", "#", "#", "#", "#", ".", "#"],
 "?": [".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."],
 ">": ["#...", ".#..", "..#.", "...#", "..#.", ".#..", "#..."],
 "<": ["...#", "..#.", ".#..", "#...", ".#..", "..#.", "...#"],
 "*": [".....", "#.#.#", ".###.", "#####", ".###.", "#.#.#", "....."],
 "=": [".....", ".....", "#####", ".....", "#####", ".....", "....."],
 "_": [".....", ".....", ".....", ".....", ".....", ".....", "#####"],
 "'": ["#", "#", ".", ".", ".", ".", "."],
 "·": ["..", "..", "..", "##", "##", "..", ".."],
 "&": [".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"],
 "²": ["###", "..#", "###", "#..", "###", "...", "..."],
 "×": [".....", ".....", "#...#", ".#.#.", "..#..", ".#.#.", "#...#"],
 "→": [".....", "...#.", "....#", "#####", "....#", "...#.", "....."],
 "♥": [".##.##.", "#######", "#######", ".#####.", "..###..", "...#...", "......."],
 "▶": ["#...", "##..", "###.", "####", "###.", "##..", "#..."],
 "✓": [".....", "....#", "...#.", "#.#..", ".#...", ".....", "....."],
 "#": [".#.#.", "#####", ".#.#.", ".#.#.", "#####", ".#.#.", "....."],
 " ": ["...", "...", "...", "...", "...", "...", "..."],
}


def text_width(s, scale=1, spacing=1):
    w = 0
    for ch in s.upper():
        g = _F.get(ch, _F["?"])
        w += (len(g[0]) + spacing) * scale
    return w - spacing * scale if s else 0


def text_pixels(s, x=0, y=0, scale=1, spacing=1):
    """yield (x, y, size) squares for a string, top-left at (x, y)."""
    cx = x
    for ch in s.upper():
        g = _F.get(ch, _F["?"])
        for ry, row in enumerate(g):
            for rx, c in enumerate(row):
                if c == "#":
                    yield (cx + rx * scale, y + ry * scale, scale)
        cx += (len(g[0]) + spacing) * scale


def rects_to_path(squares):
    """squares: iterable of (x, y, w, h) -> compact path data (merges horizontal runs)."""
    rows = defaultdict(list)
    for (x, y, w, h) in squares:
        rows[(y, h)].append((x, w))
    d = []
    for (y, h), items in sorted(rows.items()):
        items.sort()
        runs = []
        for x, w in items:
            if runs and abs(runs[-1][0] + runs[-1][1] - x) < 1e-9:
                runs[-1][1] += w
            else:
                runs.append([x, w])
        for x, w in runs:
            d.append(f"M{fmt(x)} {fmt(y)}h{fmt(w)}v{fmt(h)}h-{fmt(w)}z")
    return "".join(d)


def fmt(v):
    v = round(v, 2)
    return str(int(v)) if v == int(v) else str(v)


def text_svg(s, x, y, scale=2, fill="#fff", shadow=None, spacing=1, cls=None, extra=""):
    sq = [(a, b, c, c) for a, b, c in text_pixels(s, x, y, scale, spacing)]
    out = ""
    if shadow:
        sh = [(a + scale, b + scale, c, c) for a, b, c in text_pixels(s, x, y, scale, spacing)]
        out += f'<path fill="{shadow}" d="{rects_to_path(sh)}"/>'
    c = f' class="{cls}"' if cls else ""
    out += f'<path{c} fill="{fill}" d="{rects_to_path(sq)}" {extra}/>'
    return out


# ─────────────────────────────── sprites ────────────────────────────────

def outline(grid, key="O", diag=False):
    """add a 1-px outline around all filled pixels (grid grows by 1 on each side)."""
    h, w = len(grid), len(grid[0])
    g = [["."] * (w + 2) for _ in range(h + 2)]
    for y in range(h):
        for x in range(w):
            g[y + 1][x + 1] = grid[y][x]
    out = [row[:] for row in g]
    nb = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if diag:
        nb += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for y in range(h + 2):
        for x in range(w + 2):
            if g[y][x] != ".":
                continue
            for dx, dy in nb:
                xx, yy = x + dx, y + dy
                if 0 <= xx < w + 2 and 0 <= yy < h + 2 and g[yy][xx] not in ".":
                    out[y][x] = key
                    break
    return ["".join(r) for r in out]


def norm(grid):
    w = max(len(r) for r in grid)
    return [r.ljust(w, ".") for r in grid]


def sprite_paths(grid, pal, x=0, y=0, s=4, flip=False):
    """return svg <path>s for a sprite grid at (x, y) with pixel size s."""
    grid = norm(grid)
    w = len(grid[0])
    by = defaultdict(list)
    for ry, row in enumerate(grid):
        for rx, c in enumerate(row):
            if c == "." or c not in pal:
                continue
            px = (w - 1 - rx) if flip else rx
            by[c].append((x + px * s, y + ry * s, s, s))
    return "".join(f'<path fill="{pal[c]}" d="{rects_to_path(sq)}"/>' for c, sq in by.items())


def size(grid):
    grid = norm(grid)
    return len(grid[0]), len(grid)


def svg_doc(w, h, body, style="", title="", desc=""):
    from xml.sax.saxutils import escape
    t = f"<title>{escape(title)}</title>" if title else ""
    d = f"<desc>{escape(desc)}</desc>" if desc else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'shape-rendering="crispEdges" role="img">{t}{d}'
            f'<style>{style}@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}</style>'
            f'{body}</svg>')
