"""Original pixel-art sprites for the DSBA Jurassic README (all drawn by hand, grid by grid)."""
from pixelkit import P

# common dino palettes ---------------------------------------------------
GREEN = {"O": "#10261c", "B": P["g3"], "D": P["g1"], "L": P["g5"], "H": P["g4"], "E": "#ffffff", "K": "#0d1117",
         "T": "#ffffff", "R": P["red"], "S": P["dusk4"], "C": P["bone"], "X": P["g2"]}


def recolor(base, **kw):
    p = dict(base)
    p.update(kw)
    return p


ORANGE = recolor(GREEN, O="#2b1408", B="#f4a261", D="#c8553d", L="#ffe8c2", H="#ffd29b", X="#e76f51", S=P["g3"])
BLUE = recolor(GREEN, O="#0c1733", B="#4cc9f0", D="#3a56d4", L="#d7f4ff", H="#9be7ff", X="#4895ef", S=P["gold"])
PURPLE = recolor(GREEN, O="#1d0b2e", B="#b388eb", D="#7b2cbf", L="#f1e3ff", H="#d7b8ff", X="#9d4edd", S=P["pink"])
PINK = recolor(GREEN, O="#2e0b1c", B="#ff85a1", D="#d6336c", L="#ffe0e9", H="#ffc2d1", X="#f25c84", S=P["sky"])
YELLOW = recolor(GREEN, O="#2b2205", B="#ffd166", D="#e09f3e", L="#fff5d6", H="#ffe8a3", X="#f4b942", S=P["red"])

# ── T-REX (right-facing), two running frames ───────────────────────────
_TREX_TOP = [
    "............BBBBBBBBB...",
    "...........BHHHHHHBBBB..",
    "...........BHBEKBBBBBBB.",
    "...........BBBKKBBBBBBBB",
    "...........BBBBBBBBBBBBB",
    "...........BBBBBBBBBBBBB",
    "...........BBBBBBBTT.T.T",
    "...........BBBBBRRRRRRR.",
    "...........BBBBBBT.T.T..",
    "...........BBBBBBBBBB...",
    "S.........BXBBBBB.......",
    "SS.......BXBBBBBBB......",
    ".BB.....BXBBBBBBBBBB....",
    "..BB...BBBBBBBBLLBBBC...",
    "..BBBBBBBBBBBBLLLL..C...",
    "...DBBBBBBBBBBLLLL......",
    "....DDDBBBBBBBLLL.......",
    "......DDBBBBBBBL........",
]
TREX_A = _TREX_TOP + [
    ".......DBBB...DBB.......",
    ".......DBB.....DBB......",
    "......DBB.......DBB.....",
    "......CCC........CCC....",
]
TREX_B = _TREX_TOP + [
    "........DBBBDBB.........",
    ".........DBBBB..........",
    ".........DBBB...........",
    "........CCCCC...........",
]

# ── SAUROPOD (long neck, right-facing), two walking frames ─────────────
_SAURO_TOP = [
    "..................................BBBB.",
    ".................................BBEKBB",
    ".................................BBBBBB",
    "................................BBBBB..",
    "...............................BBBB....",
    "..............................BBBB.....",
    ".............................BBBB......",
    "............................BBBB.......",
    "...........................BBBB........",
    "..............XXXXXX......BBBB.........",
    "...........XXBBBBBBBBXX..BBBB..........",
    ".........XBBBBBBBBBBBBBBBBBBB..........",
    ".......XBBBBBBBBBBBBBBBBBBBB...........",
    "......BBBBBBBBBBBBBBBBBBBBBB...........",
    "....BBBBBBBBBBBBBBBBBBBBBBB............",
    "..BBBBBBBLLLLLLLLLLLLLBBBBB............",
    "BBBB...DDLLLLLLLLLLLLLLDBB.............",
]
SAURO_A = _SAURO_TOP + [
    ".......DBB..DBB.....DBB.DBB............",
    ".......DBB..DBB.....DBB.DBB............",
    ".......DBB...DBB....DBB..DBB...........",
    ".......CCC...CCC....CCC..CCC...........",
]
SAURO_B = _SAURO_TOP + [
    "........DBBDBB.......DBBDBB............",
    "........DBBDBB.......DBBDBB............",
    ".......DBB..DBB.....DBB..DBB...........",
    ".......CCC..CCC.....CCC..CCC...........",
]

# ── PTERODACTYL (right-facing), wings up / down ────────────────────────
PTERO_UP = [
    "......XX................",
    ".....XBBX...............",
    "....XBHBX...............",
    "...XBHBBX..........SS...",
    "..XBHBBBX.........SBBB..",
    ".XBHBBBBBX.......BBEKBBB",
    "XBBBBBBBBBBBBBBBBBBBRRRR",
    ".........DBBBBBBBB......",
    "...........DD..D........",
]
PTERO_DOWN = [
    "........................",
    "........................",
    "...................SS...",
    "..................SBBB..",
    ".................BBEKBBB",
    "........BBBBBBBBBBBBRRRR",
    "........XBBBBBBBBB......",
    ".......XBHBBBBBD........",
    "......XBHBBBX...........",
    ".....XBHBBX.............",
    "....XBHBX...............",
    "...XBBX.................",
    "...XX...................",
]

# ── TRICERATOPS (right-facing) ─────────────────────────────────────────
TRICERA = [
    "..................SSS.....C....",
    "................SSSSSS....CC...",
    "...............SSBBBBSS...CC...",
    "..............SSBBBBBBS..CC....",
    "......XXXXXX..SBBBBBBBBBBB.....",
    "....XXBBBBBBXXSBBBEKBBBBBBC....",
    "...XBBBBBBBBBBSBBBKKBBBBBBBCCC.",
    "..XBBBBBBBBBBBSBBBBBBBBBBBBB...",
    ".BBBBBBBBBBBBBBSBBBBBBBBBBB....",
    "BBBBBBBBBBBBBBBBSBBBBBBBBB.....",
    "BB.BBBLLLLLLLLLBBBBBBBB........",
    "...DDLLLLLLLLLLLBBBBB..........",
    "...DBB..DBB.....DBB.DBB........",
    "...DBB..DBB.....DBB.DBB........",
    "...CCC..CCC.....CCC.CCC........",
]

# ── STEGOSAURUS (right-facing) ─────────────────────────────────────────
STEGO = [
    ".............S..S...............",
    "..........S.SSSSSS.S............",
    ".......S.SSSSSSSSSSSS.S.........",
    "......SSSSSSSSSSSSSSSSSS........",
    ".....XXXXXXXXXXXXXXXXXXXX.......",
    "...XBBBBBBBBBBBBBBBBBBBBBBX.....",
    "..XBBBBBBBBBBBBBBBBBBBBBBBBBBBB.",
    ".BBBBBBBBBBBBBBBBBBBBBBBBBBEKBBB",
    "CBBBBBLLLLLLLLLLLLLLLLBBBBBBBBB.",
    "CC...DDLLLLLLLLLLLLLLLDDBBB.....",
    "......DBB..DBB....DBB..DBB......",
    "......DBB..DBB....DBB..DBB......",
    "......CCC..CCC....CCC..CCC......",
]

# ── BABY DINO (tiny, for icons / team) two hop frames ──────────────────
BABY = [
    "......BBBB..",
    ".....BBEKBB.",
    ".....BBBBBBB",
    ".....BBBRRR.",
    "S...BBBBB...",
    "SB.BBLLBBC..",
    ".BBBBLLLB...",
    "..DBBBLB....",
    "...DB.DB....",
    "...CC.CC....",
]

# ── EGG (whole / cracked / hatched) ────────────────────────────────────
EGG_PAL = {"O": "#2b2205", "W": P["bone"], "w": P["bone2"], "s": P["g3"], "c": "#2b2205",
           "B": P["g3"], "E": "#fff", "K": "#0d1117", "L": P["g5"]}
EGG = [
    "....WWWW....",
    "...WWWWWW...",
    "..WWWsWWWW..",
    "..WWWWWWsW..",
    ".WWsWWWWWWW.",
    ".WWWWWWsWWW.",
    ".WWWWWWWWWw.",
    ".WWWsWWWWww.",
    "..WWWWWWww..",
    "...wwwwww...",
]
EGG_CRACK = [
    "....WWWW....",
    "...WWcWWW...",
    "..WWWcWWWW..",
    "..WWcWcWsW..",
    ".WWsWWcWWWW.",
    ".WWWWWcsWWW.",
    ".WWWWWWWWWw.",
    ".WWWsWWWWww.",
    "..WWWWWWww..",
    "...wwwwww...",
]
EGG_HATCH = [
    "...BBBB.....",
    "..BBEKBB....",
    "..BBBBBBB...",
    "c.WcWWcW.c..",
    ".WWsWWWWWWW.",
    ".WWWWWWsWWW.",
    ".WWWWWWWWWw.",
    ".WWWsWWWWww.",
    "..WWWWWWww..",
    "...wwwwww...",
]

# ── FOSSIL BITS ────────────────────────────────────────────────────────
BONE_PAL = {"O": "#3b2a1a", "W": P["bone"], "w": P["bone2"]}
BONE = [
    "WW........WW",
    "WWW......WWW",
    ".WWWWWWWWWW.",
    ".wwwwwwwwww.",
    "www......www",
    "ww........ww",
]
AMMO_PAL = {"O": "#3b2a1a", "A": "#e9c46a", "a": "#b08a3e", "d": "#6b4f2a"}
AMMONITE = [
    "...AAAAAA...",
    "..AaaaaaaA..",
    ".AaAAAAAAaA.",
    "AaAddddddAaA",
    "AaAdAAAAdAaA",
    "AaAdAddAdAaA",
    "AaAdAAdAdAaA",
    "AaAddddAdAa.",
    ".AaAAAAAdAa.",
    ".AaaaaaaAa..",
    "..AAAAAAA...",
]
SKULL_PAL = {"O": "#3b2a1a", "W": P["bone"], "w": P["bone2"], "K": "#2b1d12"}
SKULL = [
    "....WWWWWWW.....",
    "..WWWWWWWWWWW...",
    ".WWWKKWWWWWWWWW.",
    ".WWWKKWWWWWKWWWW",
    "WWWWWWWWWWWWWWWW",
    "WWWwwwwWWWWWWWW.",
    "WW.W.W.W.W.W....",
    "W..............",
    "WW.W.W.W.W......",
    ".wwwwwwwwww.....",
]
FOOT_PAL = {"O": "#1a120b", "F": "#6b4f2a"}
FOOT = [
    "F...F...F",
    "F...F...F",
    ".F..F..F.",
    ".F..F..F.",
    "..FFFFF..",
    "..FFFFF..",
    "...FFF...",
]

# ── SCENERY ────────────────────────────────────────────────────────────
PALM_PAL = {"O": "#0a1a12", "G": P["g2"], "g": P["g1"], "T": "#7a5230", "t": "#5a3a22", "c": "#8b5a2b"}
PALM = [
    "....GGG.......GG....",
    "..GGGGGGG...GGGGGG..",
    ".GGG..gGGG.GGGg.GGG.",
    "GG......gGGGg.....GG",
    "G....GGGGgcgGGGG...G",
    "...GGGGg..Tc.gGGGG..",
    "..GG......T....GGG..",
    ".GG.......tT.....GG.",
    ".G........Tt......G.",
    "..........tT........",
    "..........Tt........",
    "...........T........",
    "...........tT.......",
    "...........Tt.......",
    "...........tT.......",
    "..........TTtT......",
]
FERN_PAL = {"O": "#0a1a12", "G": P["g1"], "g": P["g0"]}
FERN = [
    "....G.......G....",
    "G...GG..G..GG...G",
    ".G...GG.G.GG...G.",
    "..GG..GGGGG..GG..",
    "....GG.GGG.GG....",
    ".......GgG.......",
    "......GGgGG......",
]

SAT_PAL = {"O": "#0b0e1c", "P": "#4361ee", "p": "#2a3ca8", "l": "#9bb4ff", "B": "#d9dde8", "b": "#8b93a7",
           "R": P["red"], "Y": P["gold"]}
SATELLITE = [
    "PPPPPP....R....PPPPPP",
    "PlPlPp....b....PlPlPp",
    "PPPPPPbbBBBBBbbPPPPPP",
    "PlPlPp..BBYBB..PlPlPp",
    "PPPPPP..BBBBB..PPPPPP",
    "..........b..........",
    ".........bbb.........",
]

METEOR_PAL = {"O": "#1a0b05", "Y": P["sun"], "o": P["dusk4"], "r": P["lava"], "d": P["dusk2"]}
METEOR = [
    "d...........",
    ".dr.........",
    "..rro.......",
    "...roo......",
    "....ooYYY...",
    ".....oYYYY..",
    "......YYYYY.",
    "......YYYYY.",
    ".......YYY..",
]

HEART_PAL = {"O": "#2e0b12", "R": P["red"], "r": "#9d0208", "W": "#ffd6dc"}
HEART = [
    ".RR.RR.",
    "RWRRRRR",
    "RRRRRRR",
    ".RRRRr.",
    "..RRr..",
    "...r...",
]
STAR_PAL = {"O": "#2b2205", "Y": P["gold"], "y": "#e09f3e", "W": "#fff7cc"}
STAR = [
    "...Y...",
    "..YYY..",
    "YYYWYYY",
    ".YYYYY.",
    "..YyY..",
    ".Yy.yY.",
    "Y.....Y",
]
TROPHY_PAL = {"O": "#2b2205", "Y": P["gold"], "y": "#e09f3e", "W": "#fff7cc", "B": P["bone2"]}
TROPHY = [
    "YYYYYYYYY",
    "YWYYYYYyY",
    "YWYYYYYyY",
    ".YYYYYyY.",
    "..YYYyY..",
    "...YyY...",
    "....Y....",
    "...yyy...",
    "..YYYYY..",
]
