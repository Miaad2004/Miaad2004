"""Cards for the "More projects" grid. Same frame as the featured cards, each acting out its project."""
import math
import random

from svgkit import (AMBER, BLUE, BORDER, CHAR, CORAL, FAINT, FG, GREEN, HIDE, MUTED, PANEL, VIOLET, YELLOW,
                    Timeline, card, glow, grad, mono)

JUPYTER = ("Jupyter", "#DA5B0B")
PY = ("Python", "#3572A5")
CPP = ("C++", "#f34b7d")
CS = ("C#", "#178600")
JS = ("JavaScript", "#f1e05a")
HTML = ("HTML", "#e34c26")


def panel(x, y, w, h, fill=PANEL, rx=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{BORDER}"/>'


# ---------------------------------------------------------------------------------------------
# Self-driving in Need for Speed
# ---------------------------------------------------------------------------------------------
def card_selfdrive():
    T = 6.0
    tl = Timeline(T, "d")
    X, Y, W, H = 16, 46, 250, 142
    hx, hy = X + W / 2, Y + 70
    sway = [(0, 0), (1.2, -14), (2.4, 6), (3.6, 16), (4.8, -4), (6.0, 0)]
    steer = [(0, 0.0), (1.2, -0.31), (2.4, 0.12), (3.6, 0.36), (4.8, -0.08), (6.0, 0.0)]
    parts = [f'<defs><clipPath id="gv"><rect x="{X}" y="{Y}" width="{W}" height="{H}" rx="8"/></clipPath></defs>',
             f'<g clip-path="url(#gv)">',
             f'<rect x="{X}" y="{Y}" width="{W}" height="{H}" fill="url(#dusk)"/>',
             f'<circle cx="{hx + 40}" cy="{hy - 8}" r="18" fill="#ffd27a" opacity="0.9" filter="url(#g2)"/>',
             f'<path d="M{X} {hy}L{X + 30} {hy - 22}L{X + 58} {hy - 8}L{X + 92} {hy - 30}L{X + 130} {hy - 6}L{X + 170} {hy - 26}L{X + 210} {hy - 4}L{X + W} {hy - 18}V{hy}Z" fill="#3a2350"/>',
             f'<path d="M{X} {hy}L{X + 44} {hy - 10}L{X + 90} {hy - 2}L{X + 150} {hy - 14}L{X + 200} {hy - 3}L{X + W} {hy - 9}V{hy}Z" fill="#261637"/>',
             f'<rect x="{X}" y="{hy}" width="{W}" height="{Y + H - hy}" fill="#18231a"/>',
             f'<path d="M{hx - 3} {hy}L{hx + 3} {hy}L{X + W - 10} {Y + H}L{X + 10} {Y + H}Z" fill="#2c2f36"/>']
    # rumble strips and lane dashes rushing toward the camera
    for side in (-1, 1):
        x2 = X + 10 if side < 0 else X + W - 10
        parts.append(f'<path d="M{hx + 3 * side} {hy}L{x2} {Y + H}" stroke="#e5e7eb" stroke-width="3" stroke-dasharray="6 6" class="rush"/>')
    parts.append(f'<path d="M{hx} {hy}L{hx} {Y + H}" stroke="#f5d565" stroke-width="3" stroke-dasharray="4 10" class="rush2"/>')
    # the car sways with the predicted steering
    car = tl.kf([(t, f"transform:translateX({x}px)") for t, x in sway], timing="ease-in-out")
    cx, cy = hx, Y + H - 22
    parts.append(f'<g class="{car}"><g transform="translate({cx} {cy})">'
                 '<ellipse cx="0" cy="17" rx="40" ry="5" fill="#000" opacity="0.45"/>'
                 '<path d="M-36 12V-2Q-34 -10 -24 -12L-16 -24Q-12 -28 0 -28Q12 -28 16 -24L24 -12Q34 -10 36 -2V12Z" fill="#1e5fd6"/>'
                 '<path d="M-14 -22L-20 -12H20L14 -22Z" fill="#9fc6ff" opacity="0.8"/>'
                 '<path d="M-36 0H36" stroke="#0d2e6b" stroke-width="1.5"/>'
                 '<rect x="-31" y="2" width="14" height="5" rx="2" fill="#ff3b3b" filter="url(#g2)"/>'
                 '<rect x="17" y="2" width="14" height="5" rx="2" fill="#ff3b3b" filter="url(#g2)"/>'
                 '<rect x="-10" y="4" width="20" height="5" rx="1" fill="#e6edf3"/>'
                 '<rect x="-34" y="10" width="12" height="7" rx="2" fill="#111"/><rect x="22" y="10" width="12" height="7" rx="2" fill="#111"/>'
                 '</g></g>')
    parts.append("</g>")
    parts.append(f'<rect x="{X + 0.5}" y="{Y + 0.5}" width="{W - 1}" height="{H - 1}" rx="8" fill="none" stroke="{BORDER}"/>')
    # right: CNN feature maps and a steering gauge
    RX = 280
    parts.append(mono(RX, 60, "cnn", 10, MUTED))
    r = random.Random(4)
    for k in range(3):
        for i in range(4):
            for j in range(4):
                fl = tl.kf([(0, f"opacity:{r.uniform(0.2, 1):.2f}"), (1.5, f"opacity:{r.uniform(0.2, 1):.2f}"),
                            (3.0, f"opacity:{r.uniform(0.2, 1):.2f}"), (4.5, f"opacity:{r.uniform(0.2, 1):.2f}"),
                            (T, "opacity:0.5")])
                parts.append(f'<rect x="{RX + k * 40 + j * 8}" y="{68 + i * 8}" width="7" height="7" rx="1" '
                             f'fill="{[BLUE, VIOLET, GREEN][k]}" class="{fl}"/>')
    gx, gy = RX + 58, 158
    parts.append(f'<path d="M{gx - 44} {gy}A44 44 0 0 1 {gx + 44} {gy}" fill="none" stroke="{FAINT}" stroke-width="6" stroke-linecap="round"/>')
    parts.append(f'<path d="M{gx - 44} {gy}A44 44 0 0 1 {gx + 44} {gy}" fill="none" stroke="url(#arc)" stroke-width="6" stroke-linecap="round" opacity="0.8"/>')
    needle = tl.kf([(t, f"transform:rotate({s * 120:.0f}deg)") for t, s in steer], timing="ease-in-out")
    parts.append(f'<g transform="translate({gx} {gy})"><g class="{needle}"><path d="M-2 0L0 -40L2 0Z" fill="{FG}"/></g>'
                 f'<circle r="4" fill="{FG}"/></g>')
    for i, (t, s) in enumerate(steer[:-1]):
        cls = tl.pulse(t, steer[i + 1][0]) if i else tl.kf([(0, "opacity:1"), (1.2, "opacity:1"), (1.201, "opacity:0"), (T, "opacity:0")])
        parts.append(f'<g class="{cls}"{"" if i == 0 else HIDE}>{mono(gx, gy + 20, f"steer {s:+.2f}", 10, AMBER, anchor="middle")}</g>')
    css = (tl.css() + ".rush{animation:rush .5s linear infinite}.rush2{animation:rush2 .5s linear infinite}"
           "@keyframes rush{to{stroke-dashoffset:-12}}@keyframes rush2{to{stroke-dashoffset:-14}}")
    defs = ('<linearGradient id="dusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b1a4a"/>'
            '<stop offset="0.45" stop-color="#c2527a"/><stop offset="0.52" stop-color="#ff9e5e"/><stop offset="1" stop-color="#18231a"/></linearGradient>'
            + glow("g2", 2) + grad("arc", RX + 14, RX + 102, (CORAL, GREEN, CORAL)))
    return card("~/self-driving-nfs", "Self-driving in Need for Speed", "a CNN that learned to steer from gameplay",
                *JUPYTER, "\n".join(parts), css, "A car races down a dusk road while a CNN's steering gauge swings with each turn.", defs)


# ---------------------------------------------------------------------------------------------
# One-shot face recognition with a Siamese network
# ---------------------------------------------------------------------------------------------
def face(x, y, skin, hair, style):
    hairpath = {"short": "M-16 -6Q-16 -24 0 -24Q16 -24 16 -6Q12 -16 0 -16Q-12 -16 -16 -6Z",
                "long": "M-18 14Q-20 -24 0 -24Q20 -24 18 14L12 14Q14 -12 0 -14Q-14 -12 -12 14Z",
                "curly": "M-17 -4Q-22 -14 -14 -20Q-10 -28 0 -25Q10 -28 14 -20Q22 -14 17 -4Q12 -14 0 -14Q-12 -14 -17 -4Z"}[style]
    return (f'<g transform="translate({x} {y})"><rect x="-26" y="-28" width="52" height="56" rx="6" fill="#1a2230"/>'
            f'<path d="M-20 28Q-20 12 0 12Q20 12 20 28Z" fill="#3b4b66"/>'
            f'<ellipse cx="0" cy="-4" rx="14" ry="17" fill="{skin}"/>'
            f'<path d="{hairpath}" fill="{hair}"/>'
            f'<circle cx="-5" cy="-5" r="1.6" fill="#1b1b1b"/><circle cx="5" cy="-5" r="1.6" fill="#1b1b1b"/>'
            f'<path d="M-4 5Q0 8 4 5" stroke="#6b3a2a" stroke-width="1.2" fill="none"/></g>')


def card_siamese():
    T = 9.0
    tl = Timeline(T, "s")
    half = T / 2
    parts = [face(44, 76, "#e8b98f", "#3a2a1c", "short")]
    b1 = face(44, 150, "#e3b48a", "#3a2a1c", "short")
    b2 = face(44, 150, "#c98e62", "#141414", "curly")
    parts.append(f'<g class="{tl.show(0, half - 0.2, fade=0.2)}">{b1}</g>')
    parts.append(f'<g class="{tl.show(half, T - 0.2, fade=0.2)}"{HIDE}>{b2}</g>')
    # twin towers with shared weights
    for yy in (76, 150):
        for i, w in enumerate([10, 8, 6, 4]):
            parts.append(f'<rect x="{90 + i * 20}" y="{yy - 18 + i * 3}" width="{w + 6}" height="{36 - i * 6}" rx="2" fill="#1f2a3a" stroke="{BLUE}" stroke-width="0.8"/>')
        parts.append(f'<path d="M76 {yy}H88" stroke="{FAINT}"/>')
    parts.append(f'<path d="M113 98V128M133 101V125M153 104V122" stroke="{VIOLET}" stroke-dasharray="2 2"/>')
    parts.append(mono(160, 116, "shared", 8, VIOLET))
    # embeddings
    r = random.Random(11)
    base = [r.uniform(0, 1) for _ in range(12)]
    same = [min(1, max(0, v + r.uniform(-0.12, 0.12))) for v in base]
    diff = [r.uniform(0, 1) for _ in range(12)]

    def emb(vals, y, cls=""):
        return (f'<g class="{cls}">' if cls else "<g>") + "".join(
            f'<rect x="{186 + i * 9}" y="{y - 6}" width="8" height="12" rx="1.5" fill="{AMBER}" fill-opacity="{0.15 + 0.85 * v:.2f}"/>'
            for i, v in enumerate(vals)) + "</g>"
    parts.append(emb(base, 76))
    parts.append(f'<g class="{tl.show(0.6, half - 0.2, fade=0.3)}">{emb(same, 150)}</g>')
    parts.append(f'<g class="{tl.show(half + 0.6, T - 0.2, fade=0.3)}"{HIDE}>{emb(diff, 150)}</g>')
    d1 = math.sqrt(sum((a - b) ** 2 for a, b in zip(base, same)))
    d2 = math.sqrt(sum((a - b) ** 2 for a, b in zip(base, diff)))
    # distance meter
    MX, MW = 310, 88
    parts.append(f'<rect x="{MX}" y="104" width="{MW}" height="8" rx="4" fill="url(#dist)"/>')
    parts.append(f'<path d="M{MX + MW * 0.4} 100V116" stroke="{FG}" stroke-dasharray="2 2"/>')
    parts.append(mono(MX, 86, "distance", 9, MUTED))
    m = tl.kf([(0, "transform:translateX(0)"), (0.8, "transform:translateX(0)"),
               (1.8, f"transform:translateX({MW * min(1, d1 / 2):.1f}px)"), (half - 0.2, f"transform:translateX({MW * min(1, d1 / 2):.1f}px)"),
               (half + 0.8, "transform:translateX(0)"), (half + 1.8, f"transform:translateX({MW * min(1, d2 / 2):.1f}px)"),
               (T - 0.2, f"transform:translateX({MW * min(1, d2 / 2):.1f}px)"), (T, "transform:translateX(0)")], timing="ease-out")
    parts.append(f'<g class="{m}"><path d="M{MX} 100l-4 -6h8Z" fill="{FG}"/></g>')
    parts.append(f'<g class="{tl.show(1.9, half - 0.2)}">{mono(MX, 134, f"d = {d1:.2f}", 10, FG)}{mono(MX, 150, "same person", 10, GREEN)}</g>')
    parts.append(f'<g class="{tl.show(half + 1.9, T - 0.2)}"{HIDE}>{mono(MX, 134, f"d = {d2:.2f}", 10, FG)}{mono(MX, 150, "different", 10, CORAL)}</g>')
    defs = grad("dist", MX, MX + MW, (GREEN, YELLOW, CORAL))
    return card("~/siamese-faces", "One-shot face recognition", "a Siamese network in TensorFlow",
                *JUPYTER, "\n".join(parts), tl.css(),
                "Two faces pass through twin networks with shared weights; their embeddings are compared by distance.", defs)


# ---------------------------------------------------------------------------------------------
# Packet Tools: building a DNS query layer by layer
# ---------------------------------------------------------------------------------------------
def card_packets():
    T = 9.0
    tl = Timeline(T, "k")
    layers = [("DNS", "A? github.com  id=0x1f3a", "#2d6a4f", GREEN),
              ("UDP", "sport=50712 dport=53", "#1d4e89", BLUE),
              ("IPv4", "ttl=64 proto=17 > 1.1.1.1", "#5a3d8a", VIOLET),
              ("ETH", "type=0x0800", "#7a4a12", AMBER)]
    parts = []
    for i, (name, fields, bg, fg) in enumerate(layers):
        on = 0.4 + i * 0.7
        y = 124 - i * 24
        x = 60 - i * 12
        w = 300 + i * 24
        mv = tl.kf([(0, "transform:translateX(-30px);opacity:0"), (on, "transform:translateX(-30px);opacity:0"),
                    (on + 0.35, "transform:translateX(0);opacity:1"), (T - 0.6, "transform:translateX(0);opacity:1"),
                    (T - 0.3, "transform:translateX(0);opacity:0"), (T, "transform:translateX(0);opacity:0")], timing="ease-out")
        parts.append(f'<g class="{mv}"><rect x="{x}" y="{y}" width="{w}" height="20" rx="4" fill="{bg}" stroke="{fg}" stroke-opacity="0.6"/>'
                     f'{mono(x + 8, y + 14, name, 10, fg, weight="700")}{mono(x + 52, y + 14, fields, 9.5, FG)}</g>')
    # send and receive
    send = tl.kf([(0, "opacity:0"), (3.3, "opacity:0"), (3.5, "opacity:1"), (T - 0.6, "opacity:1"), (T - 0.3, "opacity:0"), (T, "opacity:0")])
    parts.append(f'<g class="{send}">{mono(24, 166, "tx 74 bytes", 10, MUTED)}</g>')
    for j in range(6):
        on = 3.4 + j * 0.12
        pk = tl.kf([(0, "transform:translateX(0);opacity:0"), (on, "transform:translateX(0);opacity:1"),
                    (on + 0.9, "transform:translateX(250px);opacity:1"), (on + 0.95, "transform:translateX(250px);opacity:0"), (T, "opacity:0")])
        parts.append(f'<rect x="110" y="{158 + (j % 3) * 4}" width="10" height="3" rx="1" fill="{GREEN}" class="{pk}" style="opacity:0"/>')
    rx = tl.show(4.9, T - 0.6, fade=0.3)
    parts.append(f'<g class="{rx}">{mono(24, 184, "rx", 10, MUTED)}{mono(48, 184, "github.com.  60  IN  A  140.82.121.3", 10, AMBER)}</g>')
    return card("~/packet-tools", "Packet Tools", "TCP, UDP, ICMP and DNS built from scratch",
                *PY, "\n".join(parts), tl.css(),
                "A DNS query is wrapped in UDP, IPv4 and Ethernet headers layer by layer, sent, and the answer comes back.")


# ---------------------------------------------------------------------------------------------
# Sliding puzzle solving itself
# ---------------------------------------------------------------------------------------------
def card_puzzle():
    solved = list(range(1, 16)) + [0]
    r = random.Random(15)
    state = solved[:]
    blank = 15
    moves = []
    prev = None
    for _ in range(14):
        bx, by = blank % 4, blank // 4
        opts = [(bx + dx, by + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                if 0 <= bx + dx < 4 and 0 <= by + dy < 4 and (by + dy) * 4 + bx + dx != prev]
        nx, ny = r.choice(opts)
        nb = ny * 4 + nx
        state[blank], state[nb] = state[nb], state[blank]
        prev, blank = blank, nb
        moves.append(nb)
    # replay the scramble backwards = a solution
    start = state[:]
    path = []
    s = start[:]
    b = blank
    for tgt in reversed([15] + moves[:-1]):
        tile = s[tgt]
        path.append((tile, tgt, b))
        s[b], s[tgt] = s[tgt], s[b]
        b = tgt
    T = 10.0
    tl = Timeline(T, "z")
    C, X0, Y0 = 33, 36, 48
    pos = {t: i for i, t in enumerate(start) if t}
    tiles = {t: [(0, pos[t])] for t in pos}
    t0, dt = 0.6, 0.45
    for k, (tile, frm, to) in enumerate(path):
        tt = t0 + k * dt
        tiles[tile].append((tt, frm))
        tiles[tile].append((tt + 0.22, to))
    parts = [f'<rect x="{X0 - 6}" y="{Y0 - 6}" width="{4 * C + 12}" height="{4 * C + 12}" rx="8" fill="#101722" stroke="{BORDER}"/>']
    for tile, stops in tiles.items():
        home = tile - 1
        kf = [(0, f"transform:translate({(stops[0][1] % 4) * C}px,{(stops[0][1] // 4) * C}px)")]
        for tt, p in stops[1:]:
            kf.append((tt, f"transform:translate({(p % 4) * C}px,{(p // 4) * C}px)"))
        endp = stops[-1][1]
        kf.append((T - 0.4, f"transform:translate({(endp % 4) * C}px,{(endp // 4) * C}px)"))
        kf.append((T - 0.39, f"transform:translate({(pos[tile] % 4) * C}px,{(pos[tile] // 4) * C}px)"))
        kf.append((T, f"transform:translate({(pos[tile] % 4) * C}px,{(pos[tile] // 4) * C}px)"))
        cls = tl.kf(kf, timing="ease-in-out")
        hue = [BLUE, VIOLET, CORAL, AMBER][home // 4]
        parts.append(f'<g class="{cls}" style="transform:translate({(home % 4) * C}px,{(home // 4) * C}px)">'
                     f'<rect x="{X0 + 1.5}" y="{Y0 + 1.5}" width="{C - 3}" height="{C - 3}" rx="5" fill="#1b2433" stroke="{hue}" stroke-opacity="0.7"/>'
                     f'<rect x="{X0 + 1.5}" y="{Y0 + 1.5}" width="{C - 3}" height="4" rx="2" fill="{hue}" opacity="0.35"/>'
                     f'{mono(X0 + C / 2, Y0 + C / 2 + 5, str(tile), 13, FG, anchor="middle", weight="700")}</g>')
    done = t0 + len(path) * dt
    for k in range(len(path) + 1):
        on = t0 + k * dt if k else 0
        off = t0 + (k + 1) * dt if k < len(path) else T - 0.4
        cls = tl.pulse(on, off)
        parts.append(f'<g class="{cls}"{"" if k == len(path) else HIDE}>{mono(210, 80, f"moves  {k:02d}", 12, FG)}</g>')
    parts.append(f'<g class="{tl.show(done + 0.1, T - 0.4, fade=0.2)}">{mono(210, 104, "solved", 12, GREEN)}</g>')
    return card("~/sliding-puzzle", "Sliding Puzzle", "the 15-puzzle in the console, in C++",
                *CPP, "\n".join(parts), tl.css(), "A 15-puzzle slides itself back into order.")


# ---------------------------------------------------------------------------------------------
# Candy Crush: swap, match, fall
# ---------------------------------------------------------------------------------------------
CANDY = {
    "r": ('<circle r="10" fill="url(#cr)"/><path d="M-10 0l-5 -5v10ZM10 0l5 -5v10Z" fill="#ff8a8a"/>', "#ff4d5e"),
    "b": ('<path d="M0 -11L10 0L0 11L-10 0Z" fill="url(#cb)"/>', "#4d9dff"),
    "g": ('<rect x="-9" y="-9" width="18" height="18" rx="4" fill="url(#cg)"/>', "#43d17a"),
    "y": ('<path d="M0 -11C8 -2 9 4 0 10C-9 4 -8 -2 0 -11Z" fill="url(#cy)"/>', "#ffd23f"),
    "p": ('<path d="M0 -11L9.5 -5.5V5.5L0 11L-9.5 5.5V-5.5Z" fill="url(#cp)"/>', "#b86bff"),
}


def candy(kind):
    shape, _ = CANDY[kind]
    return shape + '<ellipse cx="-3" cy="-5" rx="4" ry="2" fill="#fff" opacity="0.45"/>'


def card_candy():
    T = 7.0
    tl = Timeline(T, "c")
    grid = ["gpbyr", "ybrgp", "rgpyg", "bbybr", "pryby"]
    grid = [list(row) for row in grid]
    C, X0, Y0 = 27, 34, 48
    # swapping (3,2) y with (3,3) b lines up three blues on row 3
    parts = [f'<rect x="{X0 - 6}" y="{Y0 - 4}" width="{5 * C + 12}" height="{5 * C + 8}" rx="10" fill="#1d1430" stroke="#3b2a5c"/>']
    for r in range(5):
        for c in range(5):
            parts.append(f'<rect x="{X0 + c * C + 1}" y="{Y0 + r * C + 1}" width="{C - 2}" height="{C - 2}" rx="5" '
                         f'fill="{"#281c40" if (r + c) % 2 else "#2e2148"}"/>')
    sw_t, pop_t, fall_t = 1.0, 1.7, 2.3
    new_col = {0: "g", 1: "y", 2: "r"}
    for r in range(5):
        for c in range(5):
            k = grid[r][c]
            x, y = X0 + c * C + C / 2, Y0 + r * C + C / 2
            kf = None
            if (r, c) == (3, 2):  # moves right, then stays
                kf = [(0, "transform:translate(0px,0px)"), (sw_t, "transform:translate(0px,0px)"), (sw_t + 0.3, f"transform:translate({C}px,0px)"),
                      (T - 0.3, f"transform:translate({C}px,0px)"), (T - 0.29, "transform:translate(0px,0px)"), (T, "transform:translate(0px,0px)")]
            elif (r, c) == (3, 3):  # the blue slides left into the match and pops
                kf = [(0, "transform:translate(0px,0px) scale(1);opacity:1"), (sw_t, "transform:translate(0px,0px) scale(1);opacity:1"),
                      (sw_t + 0.3, f"transform:translate({-C}px,0px) scale(1);opacity:1"), (pop_t, f"transform:translate({-C}px,0px) scale(1);opacity:1"),
                      (pop_t + 0.3, f"transform:translate({-C}px,0px) scale(1.5);opacity:0"),
                      (T - 0.29, f"transform:translate({-C}px,0px) scale(1.5);opacity:0"), (T - 0.28, "transform:translate(0px,0px) scale(1);opacity:1"),
                      (T, "transform:translate(0px,0px) scale(1);opacity:1")]
            elif r == 3 and c in (0, 1):
                kf = [(0, "transform:scale(1);opacity:1"), (pop_t, "transform:scale(1);opacity:1"), (pop_t + 0.3, "transform:scale(1.5);opacity:0"),
                      (T - 0.29, "transform:scale(1.5);opacity:0"), (T - 0.28, "transform:scale(1);opacity:1"), (T, "transform:scale(1);opacity:1")]
            elif r < 3 and c in (0, 1, 2):
                kf = [(0, "transform:translateY(0px)"), (fall_t, "transform:translateY(0px)"), (fall_t + 0.35, f"transform:translateY({C}px)"),
                      (T - 0.3, f"transform:translateY({C}px)"), (T - 0.29, "transform:translateY(0px)"), (T, "transform:translateY(0px)")]
            inner = f'<g transform="translate({x} {y})"><g class="CLS" style="transform-box:fill-box;transform-origin:center">{candy(k)}</g></g>'
            if kf:
                cls = tl.kf(kf, timing="ease-in-out")
                parts.append(inner.replace("CLS", cls))
            else:
                parts.append(inner.replace(' class="CLS"', ""))
    for c, k in new_col.items():
        x, y = X0 + c * C + C / 2, Y0 - C / 2
        kf = [(0, "transform:translateY(0px);opacity:0"), (fall_t, "transform:translateY(0px);opacity:0"),
              (fall_t + 0.05, "transform:translateY(0px);opacity:1"), (fall_t + 0.4, f"transform:translateY({C}px);opacity:1"),
              (T - 0.3, f"transform:translateY({C}px);opacity:1"), (T - 0.29, "transform:translateY(0px);opacity:0"), (T, "opacity:0")]
        cls = tl.kf(kf, timing="ease-in")
        parts.append(f'<g transform="translate({x} {y})"><g class="{cls}" style="opacity:0">{candy(k)}</g></g>')
    # sparkles and score
    for j in range(10):
        a = j * 36
        sx, sy = X0 + 1.5 * C, Y0 + 3.5 * C
        dx, dy = 22 * math.cos(math.radians(a)), 22 * math.sin(math.radians(a))
        sp = tl.kf([(0, "transform:translate(0px,0px);opacity:0"), (pop_t, "transform:translate(0px,0px);opacity:0"),
                    (pop_t + 0.01, "transform:translate(0px,0px);opacity:1"), (pop_t + 0.5, f"transform:translate({dx:.0f}px,{dy:.0f}px);opacity:0"),
                    (T, f"transform:translate({dx:.0f}px,{dy:.0f}px);opacity:0")], timing="ease-out")
        parts.append(f'<g transform="translate({sx} {sy})"><path d="M0 -3L1 -1L3 0L1 1L0 3L-1 1L-3 0L-1 -1Z" fill="#fff6c2" class="{sp}" style="opacity:0"/></g>')
    sc = tl.kf([(0, "transform:translateY(0);opacity:0"), (pop_t, "transform:translateY(0);opacity:0"), (pop_t + 0.1, "transform:translateY(0);opacity:1"),
                (pop_t + 1.2, "transform:translateY(-16px);opacity:0"), (T, "transform:translateY(-16px);opacity:0")])
    parts.append(f'<g class="{sc}" style="opacity:0">{mono(X0 + 1.5 * C, Y0 + 3 * C, "+60", 13, YELLOW, anchor="middle", weight="700")}</g>')
    # side panel: score and moves
    SX = 222
    parts.append(panel(SX, 52, 176, 120, "#151020"))
    parts.append(mono(SX + 14, 76, "SCORE", 10, MUTED))
    parts.append(f'<g class="{tl.show(0, pop_t + 0.2, fade=0.01)}">{mono(SX + 14, 100, "1,240", 20, FG, weight="700")}</g>')
    parts.append(f'<g class="{tl.show(pop_t + 0.2, T - 0.3, fade=0.01)}"{HIDE}>{mono(SX + 14, 100, "1,300", 20, YELLOW, weight="700")}</g>')
    parts.append(mono(SX + 14, 128, "MOVES", 10, MUTED))
    parts.append(f'<g class="{tl.show(0, sw_t + 0.3, fade=0.01)}">{mono(SX + 14, 150, "18", 16, FG, weight="700")}</g>')
    parts.append(f'<g class="{tl.show(sw_t + 0.3, T - 0.3, fade=0.01)}"{HIDE}>{mono(SX + 14, 150, "17", 16, FG, weight="700")}</g>')
    parts.append(mono(SX + 100, 76, "vs", 10, MUTED))
    parts.append(mono(SX + 100, 100, "player2", 11, VIOLET))
    parts.append(mono(SX + 100, 118, "1,180", 11, FG))
    defs = "".join(f'<radialGradient id="c{k}" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#ffffff"/>'
                   f'<stop offset="0.25" stop-color="{col}"/><stop offset="1" stop-color="#1a1030"/></radialGradient>'
                   for k, (_, col) in CANDY.items())
    return card("~/candy-crush", "Candy Crush", "Unity game with a WPF launcher and matchmaking",
                *CS, "\n".join(parts), tl.css(), "Two candies swap, three blue candies match and pop, and the column refills.", defs)


# ---------------------------------------------------------------------------------------------
# Hogwarts management: house cup standings
# ---------------------------------------------------------------------------------------------
def card_hogwarts():
    T = 8.0
    tl = Timeline(T, "w")
    houses = [("Gryffindor", "#ae0001", "#eeba30", 482), ("Slytherin", "#1a472a", "#aaaaaa", 472),
              ("Ravenclaw", "#222f5b", "#946b2d", 426), ("Hufflepuff", "#ecb939", "#372e29", 352)]
    parts = []
    X0 = 22
    for i, (name, c1, c2, pts) in enumerate(houses):
        x = X0 + i * 96
        # pennant with crest
        parts.append(f'<path d="M{x} 48h86v56l-43 18l-43 -18Z" fill="url(#h{i})" stroke="{c2}" stroke-width="1.2"/>')
        parts.append(f'<path d="M{x + 43} 60l14 6v12q0 12 -14 18q-14 -6 -14 -18v-12Z" fill="{c2}" opacity="0.9"/>')
        parts.append(f'<path d="M{x + 43} 64l9 4v9q0 8 -9 12q-9 -4 -9 -12v-9Z" fill="{c1}"/>')
        parts.append(mono(x + 43, 136, name, 9, FG, anchor="middle"))
        # hourglass-style points bar
        top, H = 142, 34
        frac = pts / 500
        grow = tl.kf([(0, "transform:scaleY(0)"), (0.4 + i * 0.15, "transform:scaleY(0)"), (2.4 + i * 0.15, f"transform:scaleY({frac:.3f})"),
                      (T - 0.5, f"transform:scaleY({frac:.3f})"), (T - 0.2, "transform:scaleY(0)"), (T, "transform:scaleY(0)")], timing="ease-out")
        parts.append(f'<rect x="{x + 28}" y="{top}" width="30" height="{H}" rx="4" fill="#161d28" stroke="{BORDER}"/>')
        parts.append(f'<rect x="{x + 30}" y="{top + 2}" width="26" height="{H - 4}" rx="3" fill="{c2 if i != 3 else c1}" class="{grow}" '
                     f'style="transform-origin:0 {top + H - 2}px;transform:scaleY({frac:.3f})"/>')
        for k in range(6):
            v = round(pts * (k / 5) ** 0.7)
            on = 0.4 + i * 0.15 + k * 0.4
            last = k == 5
            cls = tl.show(on, T - 0.5, fade=0.01) if last else tl.pulse(on, on + 0.4)
            parts.append(f'<g class="{cls}"{"" if last else HIDE}>{mono(x + 43, top + H + 12, str(v), 10, AMBER if i == 0 else MUTED, anchor="middle")}</g>')
    defs = "".join(f'<linearGradient id="h{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/>'
                   f'<stop offset="1" stop-color="{c1}" stop-opacity="0.55"/></linearGradient>' for i, (_, c1, _, _) in enumerate(houses))
    return card("~/hogwarts-wpf", "Hogwarts Management System", "a school management app in C# and WPF",
                *CS, "\n".join(parts), tl.css(), "Four house pennants with house-cup points rising.", defs)


# ---------------------------------------------------------------------------------------------
# Graph social network: friend suggestions from mutual friends
# ---------------------------------------------------------------------------------------------
def card_social():
    T = 8.0
    tl = Timeline(T, "n")
    people = {"you": (60, 108), "ali": (140, 62), "sara": (150, 150), "reza": (212, 104), "nima": (82, 160),
              "mina": (276, 60), "omid": (300, 140), "tara": (372, 92), "kian": (228, 162)}
    edges = [("you", "ali"), ("you", "sara"), ("you", "reza"), ("you", "nima"), ("ali", "mina"), ("reza", "mina"),
             ("sara", "omid"), ("reza", "omid"), ("sara", "kian"), ("omid", "tara"), ("mina", "tara"), ("nima", "sara")]
    friends = {b for a, b in edges if a == "you"} | {a for a, b in edges if b == "you"}
    adj = {p: set() for p in people}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    mutual = {p: len(adj[p] & friends) for p in people if p != "you" and p not in friends}
    best = max(mutual, key=lambda p: (mutual[p], p))
    parts = []
    for a, b in edges:
        (x1, y1), (x2, y2) = people[a], people[b]
        hot = "you" in (a, b)
        on = 0.6 if hot else 1.6
        cls = tl.kf([(0, "stroke-opacity:0.25"), (on, "stroke-opacity:0.25"), (on + 0.3, f"stroke-opacity:{0.9 if hot else 0.6}"),
                     (T - 0.4, f"stroke-opacity:{0.9 if hot else 0.6}"), (T - 0.1, "stroke-opacity:0.25"), (T, "stroke-opacity:0.25")])
        parts.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{BLUE if hot else VIOLET}" stroke-width="1.3" class="{cls}" style="stroke-opacity:0.25"/>')
    bx, by = people[best]
    yx, yy = people["you"]
    sug = tl.kf([(0, "stroke-dashoffset:1"), (2.6, "stroke-dashoffset:1"), (3.4, "stroke-dashoffset:0"), (T - 0.4, "stroke-dashoffset:0"),
                 (T - 0.1, "stroke-dashoffset:1"), (T, "stroke-dashoffset:1")])
    parts.append(f'<path d="M{yx} {yy}Q{(yx + bx) / 2} {min(yy, by) - 50} {bx} {by}" pathLength="1" stroke="{GREEN}" stroke-width="1.6" '
                 f'fill="none" style="stroke-dasharray:1" class="{sug}"/>')
    for name, (x, y) in people.items():
        me = name == "you"
        col = AMBER if me else (BLUE if name in friends else (GREEN if name == best else "#6e7681"))
        on = 0 if me else (0.6 if name in friends else 1.6)
        cls = tl.kf([(0, "opacity:0.45"), (on, "opacity:0.45"), (on + 0.3, "opacity:1"), (T - 0.4, "opacity:1"), (T - 0.1, "opacity:0.45"),
                     (T, "opacity:0.45")]) if not me else ""
        parts.append(f'<g class="{cls}"><circle cx="{x}" cy="{y}" r="{13 if me else 11}" fill="#161d28" stroke="{col}" stroke-width="2"/>'
                     f'{mono(x, y + 3.5, name[0].upper(), 10, col, anchor="middle", weight="700")}'
                     f'{mono(x, y + 25, name, 8.5, MUTED, anchor="middle")}</g>')
    ring = tl.kf([(0, "transform:scale(1);opacity:0"), (3.4, "transform:scale(1);opacity:0.9"), (4.4, "transform:scale(2);opacity:0"),
                  (4.41, "transform:scale(1);opacity:0.9"), (5.4, "transform:scale(2);opacity:0"), (T, "transform:scale(2);opacity:0")])
    parts.append(f'<g transform="translate({bx} {by})"><circle r="11" fill="none" stroke="{GREEN}" class="{ring}" '
                 f'style="transform-box:fill-box;transform-origin:center;opacity:0"/></g>')
    label = f"+ {mutual[best]} mutual"
    lw = len(label) * 9 * CHAR + 16
    parts.append(f'<g class="{tl.show(3.4, fade=0.3)}"><rect x="{bx + 16}" y="{by + 4}" width="{lw:.1f}" height="18" rx="9" fill="#12261a" stroke="{GREEN}"/>'
                 f'{mono(bx + 24, by + 16.5, label, 9, GREEN)}</g>')
    return card("~/graph-social-network", "Graph social network", "friend suggestions from a graph, Django + React",
                *PY, "\n".join(parts), tl.css(),
                f"A friendship graph lights up your friends, then friends of friends, and suggests {best} with {mutual[best]} mutual friends.")


# ---------------------------------------------------------------------------------------------
# Linux file system simulator: commands grow a tree
# ---------------------------------------------------------------------------------------------
def card_linuxfs():
    T = 10.0
    tl = Timeline(T, "x")
    cmds = [("mkdir home", [("home", 1)]), ("mkdir home/miaad", [("miaad", 2)]), ("cd home/miaad", []),
            ("mkdir projects", [("projects", 3)]), ("touch notes.txt", [("notes.txt", 3)]),
            ("mkdir projects/ai", [("ai", 4)]), ("tree /", [])]
    parts = [panel(16, 46, 190, 142, "#0a0e13")]
    tree_lines = [("/", 0)]
    t = 0.4
    y = 64
    node_times = {"/": 0}
    for cmd, adds in cmds:
        n = len(cmd)
        prompt = mono(26, y, "$", 10, GREEN)
        full = mono(26 + 2 * 10 * CHAR, y, cmd, 10, FG)
        w = n * 10 * CHAR
        cover = tl.kf([(0, "transform:translateX(0)"), (t, "transform:translateX(0)"), (t + n * 0.05, f"transform:translateX({w:.1f}px)"),
                       (T - 0.4, f"transform:translateX({w:.1f}px)"), (T - 0.39, "transform:translateX(0)"), (T, "transform:translateX(0)")],
                      timing=f"steps({n},end)")
        parts.append(f'<g class="{tl.show(t - 0.05, fade=0.01)}">{prompt}{full}'
                     f'<rect x="{26 + 2 * 10 * CHAR - 1:.1f}" y="{y - 10}" width="{w + 2:.1f}" height="14" fill="#0a0e13" class="{cover}" '
                     f'style="transform:translateX({w:.1f}px)"/></g>')
        t += n * 0.05 + 0.25
        for name, depth in adds:
            tree_lines.append((name, depth))
            node_times[name] = t
        y += 17
    # tree on the right, grown in order of creation but drawn in tree order
    order = ["/", "home", "miaad", "projects", "ai", "notes.txt"]
    depth = {n: d for n, d in tree_lines}
    TX, TY = 226, 62
    for i, name in enumerate(order):
        d = depth[name]
        x, yy = TX + d * 22, TY + i * 22
        on = node_times[name]
        is_dir = not name.endswith(".txt")
        cls = tl.show(on, fade=0.25)
        conn = ""
        if d:
            parent_i = max(j for j in range(i) if depth[order[j]] == d - 1)
            px, py = TX + (d - 1) * 22, TY + parent_i * 22
            conn = f'<path d="M{px + 7} {py + 8}V{yy}H{x - 4}" stroke="{FAINT}" fill="none"/>'
        icon = (f'<path d="M{x} {yy - 6}h6l2 2h8v10h-16Z" fill="{AMBER}"/>' if is_dir else
                f'<path d="M{x + 2} {yy - 7}h9l4 4v12h-13Z" fill="{BLUE}"/>')
        parts.append(f'<g class="{cls}">{conn}{icon}{mono(x + 22, yy + 3, name, 10, FG if is_dir else MUTED)}</g>')
    return card("~/linux-fs-sim", "Linux file system simulator", "general trees behind a terminal UI",
                *CS, "\n".join(parts), tl.css(), "Shell commands type out on the left and grow a directory tree on the right.")


# ---------------------------------------------------------------------------------------------
# Scientific calculator: shunting-yard in action
# ---------------------------------------------------------------------------------------------
def shunting_yard(tokens):
    prec = {"+": 1, "-": 1, "*": 2, "/": 2}
    out, ops, trace = [], [], []
    for tok in tokens:
        if tok.isdigit():
            out.append(tok)
        elif tok == "(":
            ops.append(tok)
        elif tok == ")":
            while ops[-1] != "(":
                out.append(ops.pop())
            ops.pop()
        else:
            while ops and ops[-1] != "(" and prec[ops[-1]] >= prec[tok]:
                out.append(ops.pop())
            ops.append(tok)
        trace.append((tok, out[:], ops[:]))
    while ops:
        out.append(ops.pop())
    trace.append(("", out[:], []))
    return trace


def card_calc():
    tokens = list("3+4*(2-1)")
    trace = shunting_yard(tokens)
    T = 11.0
    tl = Timeline(T, "q")
    parts = [f'<rect x="20" y="48" width="118" height="138" rx="10" fill="#1a2130" stroke="{BORDER}"/>',
             f'<rect x="28" y="56" width="102" height="28" rx="4" fill="#0c1a14"/>']
    keys = ["7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "(", "0", ")", "+"]
    kpos = {}
    for i, k in enumerate(keys):
        x, y = 28 + (i % 4) * 26, 92 + (i // 4) * 23
        kpos[k] = (x, y)
        op = k in "/*-+()"
        parts.append(f'<rect x="{x}" y="{y}" width="22" height="19" rx="4" fill="{"#2b3547" if op else "#232b3a"}"/>'
                     f'{mono(x + 11, y + 13.5, k.replace("*", "x"), 10, AMBER if op else FG, anchor="middle")}')
    step = 0.6
    for i, (tok, out, ops) in enumerate(trace):
        on = 0.5 + i * step
        off = on + step if i < len(trace) - 1 else T - 0.4
        cls = tl.pulse(on, off) if i < len(trace) - 1 else tl.show(on, off, fade=0.01)
        rest = "" if i == len(trace) - 1 else HIDE
        expr = "".join(tokens[:i + 1]).replace("*", "x")
        g = [f'<g class="{cls}"{rest}>', mono(126, 75, expr[-14:], 11, GREEN, anchor="end")]
        g.append(mono(160, 64, "output", 9, MUTED))
        for j, o in enumerate(out):
            g.append(f'<rect x="{160 + j * 26}" y="70" width="22" height="20" rx="4" fill="#15233a" stroke="{BLUE}" stroke-opacity="0.7"/>'
                     f'{mono(171 + j * 26, 84, o.replace("*", "x"), 11, FG, anchor="middle")}')
        g.append(mono(160, 110, "operators", 9, MUTED))
        for j, o in enumerate(ops):
            g.append(f'<rect x="{160 + j * 26}" y="116" width="22" height="20" rx="4" fill="#2a1d12" stroke="{AMBER}" stroke-opacity="0.7"/>'
                     f'{mono(171 + j * 26, 130, o.replace("*", "x"), 11, AMBER, anchor="middle")}')
        g.append("</g>")
        parts.append("".join(g))
        if tok:
            kx, ky = kpos[tok]
            press = tl.kf([(0, "opacity:0"), (on, "opacity:0"), (on + 0.02, "opacity:0.6"), (on + 0.3, "opacity:0"), (T, "opacity:0")])
            parts.append(f'<rect x="{kx}" y="{ky}" width="22" height="19" rx="4" fill="#ffffff" class="{press}" style="opacity:0"/>')
    # evaluate RPN
    rpn = trace[-1][1]
    st = []
    for tok in rpn:
        if tok.isdigit():
            st.append(int(tok))
        else:
            b_, a_ = st.pop(), st.pop()
            st.append({"+": a_ + b_, "-": a_ - b_, "*": a_ * b_, "/": a_ // b_}[tok])
    res_on = 0.5 + len(trace) * step
    parts.append(f'<g class="{tl.show(res_on, T - 0.4, fade=0.2)}">{mono(160, 166, "= " + str(st[0]), 16, GREEN, weight="700")}'
                 f'{mono(218, 166, "rpn: " + " ".join(rpn).replace("*", "x"), 9.5, MUTED)}</g>')
    return card("~/web-calculator", "Scientific web calculator", "stack-based expression parsing in JavaScript",
                *JS, "\n".join(parts), tl.css(),
                "Typing 3+4x(2-1) on a calculator while the shunting-yard algorithm fills the output queue and operator stack, then evaluates to 7.")


# ---------------------------------------------------------------------------------------------
# Data structures: binary search tree insertions
# ---------------------------------------------------------------------------------------------
def card_bst():
    keys = [50, 30, 70, 20, 40, 60, 80, 35, 65]
    T = 10.0
    tl = Timeline(T, "b")
    pos, parent = {}, {}
    xs = {1: (210, 120), 2: (80, 60), 3: (40, 20), 4: (20, 10)}
    root = None
    paths = {}
    for k in keys:
        if root is None:
            root = k
            pos[k] = (210, 62)
            paths[k] = [k]
            continue
        cur, depth, path = root, 1, [root]
        while True:
            go_left = k < cur
            child = [c for c in pos if parent.get(c) == cur and ((c < cur) == go_left)]
            if child:
                cur = child[0]
                depth += 1
                path.append(cur)
            else:
                px, py = pos[cur]
                dx = [0, 100, 50, 25][depth]
                pos[k] = (px - dx if go_left else px + dx, py + 38)
                parent[k] = cur
                paths[k] = path + [k]
                break
    parts = []
    step = 0.85
    for i, k in enumerate(keys):
        on = 0.4 + i * step
        if k in parent:
            (x1, y1), (x2, y2) = pos[parent[k]], pos[k]
            parts.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{FAINT}" stroke-width="1.5" class="{tl.show(on + 0.5, fade=0.2)}"/>')
    for i, k in enumerate(keys):
        on = 0.4 + i * step
        x, y = pos[k]
        # comparison path highlight
        for j, p in enumerate(paths[k][:-1]):
            px, py = pos[p]
            hl = tl.kf([(0, "opacity:0"), (on + j * 0.14, "opacity:0"), (on + j * 0.14 + 0.05, "opacity:1"),
                        (on + j * 0.14 + 0.3, "opacity:0"), (T, "opacity:0")])
            parts.append(f'<circle cx="{px}" cy="{py}" r="15" fill="none" stroke="{AMBER}" stroke-width="2" class="{hl}" style="opacity:0"/>')
        pop = tl.kf([(0, "transform:scale(0)"), (on + 0.45, "transform:scale(0)"), (on + 0.65, "transform:scale(1.15)"),
                     (on + 0.8, "transform:scale(1)"), (T - 0.4, "transform:scale(1)"), (T - 0.2, "transform:scale(0)"), (T, "transform:scale(0)")])
        parts.append(f'<g transform="translate({x} {y})"><g class="{pop}" style="transform-box:fill-box;transform-origin:center">'
                     f'<circle r="12" fill="#161d28" stroke="{GREEN if i == len(keys) - 1 else BLUE}" stroke-width="1.6"/>'
                     f'{mono(0, 4, str(k), 10, FG, anchor="middle", weight="700")}</g></g>')
        off = on + step if i < len(keys) - 1 else T - 0.4
        cls = tl.pulse(on, off) if i < len(keys) - 1 else tl.show(on, off, fade=0.01)
        parts.append(f'<g class="{cls}"{"" if i == len(keys) - 1 else HIDE}>{mono(24, 62, f"insert {k}", 11, AMBER)}'
                     f'{mono(24, 78, f"depth {len(paths[k]) - 1}", 10, MUTED)}</g>')
    return card("~/data-structures", "Data structures collection", "common data structures in several languages",
                *CPP, "\n".join(parts), tl.css(), "Keys are inserted into a binary search tree one at a time, each walking down from the root.")


# ---------------------------------------------------------------------------------------------
# Pure-Python ML: k-means converging (computed here, no libraries)
# ---------------------------------------------------------------------------------------------
def card_kmeans():
    r = random.Random(21)
    blobs = [((150, 120), 18), ((250, 158), 17), ((330, 84), 16)]
    pts = [(r.gauss(cx, s), r.gauss(cy, s * 0.8)) for (cx, cy), s in blobs for _ in range(22)]
    pts = [(min(396, max(24, x)), min(182, max(50, y))) for x, y in pts]
    cents = [(60, 170), (200, 60), (380, 170)]
    iters = []
    for _ in range(8):
        lab = [min(range(3), key=lambda k: (x - cents[k][0]) ** 2 + (y - cents[k][1]) ** 2) for x, y in pts]
        iters.append((cents[:], lab))
        new = []
        for k in range(3):
            mem = [p for p, l in zip(pts, lab) if l == k]
            new.append((sum(p[0] for p in mem) / len(mem), sum(p[1] for p in mem) / len(mem)) if mem else cents[k])
        if new == cents:
            break
        cents = new
    T = 9.0
    tl = Timeline(T, "m")
    cols = [CORAL, GREEN, BLUE]
    step = 0.9
    parts = []
    for i, (cs, lab) in enumerate(iters):
        on = 0.3 + i * step
        last = i == len(iters) - 1
        off = on + step if not last else T - 0.3
        cls = tl.pulse(on, off) if not last else tl.show(on, off, fade=0.01)
        g = [f'<g class="{cls}"{"" if last else HIDE}>']
        for (x, y), l in zip(pts, lab):
            g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="{cols[l]}" opacity="0.85"/>')
        g.append(mono(24, 62, f"iter {i + 1}", 11, AMBER))
        inertia = sum((x - cs[l][0]) ** 2 + (y - cs[l][1]) ** 2 for (x, y), l in zip(pts, lab))
        g.append(mono(24, 78, f"inertia {inertia / 1000:.1f}k", 10, MUTED))
        g.append("</g>")
        parts.append("".join(g))
    # centroids glide between iterations, leaving trails
    for k in range(3):
        trail = " ".join(f"{'M' if i == 0 else 'L'}{cs[k][0]:.1f} {cs[k][1]:.1f}" for i, (cs, _) in enumerate(iters))
        parts.append(f'<path d="{trail}" stroke="{cols[k]}" stroke-width="1" stroke-dasharray="3 3" fill="none" opacity="0.6"/>')
        kf = []
        for i, (cs, _) in enumerate(iters):
            on = 0.3 + i * step
            kf.append((on, f"transform:translate({cs[k][0]:.1f}px,{cs[k][1]:.1f}px)"))
            kf.append((on + step * 0.6, f"transform:translate({cs[k][0]:.1f}px,{cs[k][1]:.1f}px)"))
        kf = [(0, kf[0][1])] + kf + [(T - 0.3, kf[-1][1]), (T, kf[0][1])]
        cls = tl.kf(kf, timing="ease-in-out")
        fx, fy = iters[-1][0][k]
        parts.append(f'<g class="{cls}" style="transform:translate({fx:.1f}px,{fy:.1f}px)"><circle r="7" fill="#0b0f14" stroke="{cols[k]}" stroke-width="2"/>'
                     f'<path d="M-3 -3L3 3M3 -3L-3 3" stroke="{cols[k]}" stroke-width="2"/></g>')
    return card("~/pure-python-ml", "ML in pure Python", "linear regression, k-means and KNN, no libraries",
                *PY, "\n".join(parts), tl.css(), f"k-means on three clusters converging in {len(iters)} iterations.")


# ---------------------------------------------------------------------------------------------
# Sudoku solver: backtracking fills the grid
# ---------------------------------------------------------------------------------------------
PUZZLE = ("530070000600195000098000060800060003400803001700020006060000280000419005000080079")


def solve(board):
    order, tries = [], [0]

    def ok(b, i, v):
        r, c = divmod(i, 9)
        if any(b[r * 9 + k] == v for k in range(9)) or any(b[k * 9 + c] == v for k in range(9)):
            return False
        br, bc = r // 3 * 3, c // 3 * 3
        return all(b[(br + a) * 9 + bc + d] != v for a in range(3) for d in range(3))

    def rec(b):
        try:
            i = b.index(0)
        except ValueError:
            return True
        for v in range(1, 10):
            if ok(b, i, v):
                b[i] = v
                tries[0] += 1
                if rec(b):
                    return True
                b[i] = 0
        return False
    b = board[:]
    rec(b)
    for i in range(81):
        if board[i] == 0:
            order.append((i, b[i]))
    return order, tries[0]


def card_sudoku():
    board = [int(c) for c in PUZZLE]
    order, tries = solve(board)
    T = 9.0
    tl = Timeline(T, "u")
    C, X0, Y0 = 15, 30, 48
    parts = [f'<rect x="{X0}" y="{Y0}" width="{9 * C}" height="{9 * C}" fill="#101722"/>']
    for i in range(10):
        w = 1.6 if i % 3 == 0 else 0.5
        col = MUTED if i % 3 == 0 else FAINT
        parts.append(f'<path d="M{X0 + i * C} {Y0}V{Y0 + 9 * C}M{X0} {Y0 + i * C}H{X0 + 9 * C}" stroke="{col}" stroke-width="{w}"/>')
    for i, v in enumerate(board):
        if v:
            r, c = divmod(i, 9)
            parts.append(mono(X0 + c * C + C / 2, Y0 + r * C + C / 2 + 3.5, str(v), 9.5, FG, anchor="middle", weight="700"))
    dt = 5.4 / len(order)
    for n, (i, v) in enumerate(order):
        r, c = divmod(i, 9)
        on = 0.4 + n * dt
        parts.append(f'<g class="{tl.show(on, fade=0.08)}">{mono(X0 + c * C + C / 2, Y0 + r * C + C / 2 + 3.5, str(v), 9.5, GREEN, anchor="middle")}</g>')
    cur = tl.kf([(0, "opacity:0")] + [(0.4 + n * dt, f"opacity:1;transform:translate({(i % 9) * C}px,{(i // 9) * C}px)")
                                      for n, (i, _) in enumerate(order)] + [(0.4 + len(order) * dt, "opacity:0"), (T, "opacity:0")],
                timing=f"steps(1,end)")
    parts.append(f'<rect x="{X0}" y="{Y0}" width="{C}" height="{C}" fill="{AMBER}" fill-opacity="0.25" stroke="{AMBER}" class="{cur}" style="opacity:0"/>')
    SX = 190
    for k in range(10):
        on = 0.4 + k * 0.54
        last = k == 9
        filled = round(len(order) * (k + 1) / 10)
        cls = tl.pulse(on, on + 0.54) if not last else tl.show(on, T - 0.3, fade=0.01)
        parts.append(f'<g class="{cls}"{"" if last else HIDE}>{mono(SX, 80, f"filled {filled:2d}/{len(order)}", 11, FG)}</g>')
    parts.append(mono(SX, 102, f"placements tried: {tries}", 10, MUTED))
    parts.append(mono(SX, 118, "depth-first backtracking", 10, MUTED))
    parts.append(f'<g class="{tl.show(0.4 + len(order) * dt + 0.1, T - 0.3)}">{mono(SX, 146, "solved", 12, GREEN, weight="700")}</g>')
    return card("~/web-sudoku-solver", "Web Sudoku Solver", "a backtracking Sudoku solver in JavaScript",
                *HTML, "\n".join(parts), tl.css(), "A Sudoku grid fills itself in, cell by cell, as the backtracking solver places digits.")


CARDS = [("more/selfdrive", card_selfdrive), ("more/siamese", card_siamese), ("more/packets", card_packets),
         ("more/puzzle", card_puzzle), ("more/candy", card_candy), ("more/hogwarts", card_hogwarts),
         ("more/social", card_social), ("more/linuxfs", card_linuxfs), ("more/calc", card_calc),
         ("more/bst", card_bst), ("more/kmeans", card_kmeans), ("more/sudoku", card_sudoku)]
