"""Render the static animated art for the profile: the hero, the project cards and the footer.

    python3 scripts/make_art.py        # writes assets/*.svg and assets/cards/*.svg

Deterministic (fixed seeds), so re-running only changes files when this script changes.
"""
import math
import os
import random

from svgkit import (BG, BORDER, CHAR, FG, GREEN, HIDE, MONO, MUTED, Timeline, esc, grad, mono, save,
                    window)


# ---------------------------------------------------------------------------------------------
# Frozen Lake dynamics (slippery 4x4, gym conventions)
# ---------------------------------------------------------------------------------------------
LAKE = ["SFFF", "FHFH", "FFFH", "HFFG"]
MOVES = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # gym order: left, down, right, up as (dx, dy)


def lake_step(s, a):
    x, y = s % 4, s // 4
    dx, dy = MOVES[a]
    nx, ny = min(3, max(0, x + dx)), min(3, max(0, y + dy))
    return ny * 4 + nx


def lake_outcomes(s, a):
    return [lake_step(s, b) for b in ((a - 1) % 4, a, (a + 1) % 4)]


def terminal(s):
    return LAKE[s // 4][s % 4] in "HG"


def value_iteration(gamma=0.99, sweeps=200):
    V = [0.0] * 16
    history = [V[:]]
    for _ in range(sweeps):
        nv = V[:]
        for s in range(16):
            if terminal(s):
                continue
            nv[s] = max(sum((1.0 if LAKE[t // 4][t % 4] == "G" else 0.0) + gamma * V[t] for t in lake_outcomes(s, a)) / 3
                        for a in range(4))
        V = nv
        history.append(V[:])
    pi = []
    for s in range(16):
        pi.append(max(range(4), key=lambda a: sum((1.0 if LAKE[t // 4][t % 4] == "G" else 0.0) + gamma * V[t]
                                                  for t in lake_outcomes(s, a))))
    return history, pi


# ---------------------------------------------------------------------------------------------
def donut_frame(A, B, cols, rows, aspect):
    R1, R2, K2 = 1.0, 2.0, 5.0
    K1 = cols * K2 * 3 / (8 * (R1 + R2))
    out = [[" "] * cols for _ in range(rows)]
    zb = [[0.0] * cols for _ in range(rows)]
    cA, sA, cB, sB = math.cos(A), math.sin(A), math.cos(B), math.sin(B)
    ramp = ".,-~:;=!*#$@"
    th = 0.0
    while th < 2 * math.pi:
        ct, st = math.cos(th), math.sin(th)
        ph = 0.0
        while ph < 2 * math.pi:
            cp, sp = math.cos(ph), math.sin(ph)
            cx, cy = R2 + R1 * ct, R1 * st
            x = cx * (cB * cp + sA * sB * sp) - cy * cA * sB
            y = cx * (sB * cp - sA * cB * sp) + cy * cA * cB
            ooz = 1 / (K2 + cA * cx * sp + cy * sA)
            xp, yp = int(cols / 2 + K1 * ooz * x), int(rows / 2 - K1 * ooz * y * aspect)
            L = cp * ct * sB - cA * ct * sp - sA * st + cB * (cA * st - ct * sA * sp)
            if L > 0 and 0 <= xp < cols and 0 <= yp < rows and ooz > zb[yp][xp]:
                zb[yp][xp] = ooz
                out[yp][xp] = ramp[min(int(L * 8), len(ramp) - 1)]
            ph += 0.025
        th += 0.08
    return ["".join(r) for r in out]


def donut_frames(g_id, x0, y0, cols, rows, fs, lh, n, tl):
    cw = fs * CHAR
    parts = [f'<g fill="url(#{g_id})">']
    for i in range(n):
        # the torus is symmetric under a half turn about x and about z, so pi per loop is seamless
        rows_ = donut_frame(math.pi * i / n + 1.0, math.pi * i / n + 0.8, cols, rows, cw / lh)
        cls = tl.pulse(i * tl.T / n, (i + 1) * tl.T / n)
        parts.append(f'<g class="{cls}"{HIDE if i else ""}>')
        for r, row in enumerate(rows_):
            s = row.rstrip()
            if not s.strip():
                continue
            lead = len(s) - len(s.lstrip())
            parts.append(mono(x0 + lead * cw, y0 + r * lh, s.lstrip(), fs, fill="inherit"))
        parts.append("</g>")
    parts.append("</g>")
    return "".join(parts)


# ---------------------------------------------------------------------------------------------
FONT_SMALL = {"M": ["10001", "11011", "10101", "10001", "10001"], "I": ["111", "010", "010", "010", "111"],
              "A": ["0110", "1001", "1111", "1001", "1001"], "D": ["1110", "1001", "1001", "1001", "1110"]}


def life_seed(cols, rows, word="MIAAD", soup=120, seed=32):
    cells = set()
    width = sum(len(FONT_SMALL[c][0]) for c in word) + len(word) - 1
    x, oy = (cols - width) // 2, (rows - 5) // 2
    for ch in word:
        for r, line in enumerate(FONT_SMALL[ch]):
            for c, bit in enumerate(line):
                if bit == "1":
                    cells.add((x + c, oy + r))
        x += len(FONT_SMALL[ch][0]) + 1
    rng = random.Random(seed)
    while soup:  # a little primordial soup away from the name keeps the board busy
        p = (rng.randrange(cols), rng.randrange(rows))
        if abs(p[1] - (oy + 2)) > 5:
            cells.add(p)
            soup -= 1
    return cells


def life_step(cells, cols, rows):
    count = {}
    for x, y in cells:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx or dy:
                    k = ((x + dx) % cols, (y + dy) % rows)
                    count[k] = count.get(k, 0) + 1
    return {k for k, n in count.items() if n == 3 or (n == 2 and k in cells)}


def life_frames(g_id, x0, y0, cols, rows, fs, lh, gens, fps, hold, rest=0.8):
    """Frames as text rows; newborn '@', alive '#', and a fading '+' '.' trail where cells just died.

    Each generation blends into the next, and the last one melts back into the seed, so the loop never blinks.
    Returns (svg, timeline).
    """
    cw = fs * CHAR
    cells = life_seed(cols, rows)
    age, gone = {}, {}
    grids = []
    for gen in range(gens):
        grid = [[" "] * cols for _ in range(rows)]
        for (x, y), d in gone.items():
            grid[y][x] = "+" if d == 1 else "."
        for c in cells:
            grid[c[1]][c[0]] = "@" if age.get(c, 0) < 1 else "#"
        grids.append(grid)
        nxt = life_step(cells, cols, rows)
        gone = {k: d + 1 for k, d in gone.items() if d < 2 and k not in nxt}
        gone.update({c: 1 for c in cells - nxt})
        age = {c: age.get(c, 0) + 1 for c in nxt & cells}
        cells = nxt
    starts = [0] + [hold + k / fps for k in range(gens - 1)]
    tl = Timeline(starts[-1] + rest, "g")
    out = [f'<g fill="url(#{g_id})" font-size="{fs}">']
    for grid, (cls, style) in zip(grids, tl.frames(starts, 1 / fps, wrap=0.6)):
        out.append(f'<g class="{cls}"{style}>')
        for r, row in enumerate(grid):
            s_ = "".join(row).rstrip()
            if s_.strip():
                lead = len(s_) - len(s_.lstrip())
                body = s_.lstrip()
                out.append(f'<text x="{x0 + lead * cw:.1f}" y="{y0 + r * lh:.1f}" textLength="{len(body) * cw:.1f}" '
                           f'lengthAdjust="spacingAndGlyphs">{esc(body)}</text>')
        out.append("</g>")
    out.append("</g>")
    return "".join(out), tl


# ---------------------------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------------------------
def footer():
    W, H = 880, 120
    T = 12.0
    tl = Timeline(T, "e", end=2.2)
    cmd = "exit"
    x = 28 + 2 * 14 * CHAR
    cover = tl.kf([(0, "transform:translateX(0)"), (0.6, "transform:translateX(0)"),
                   (0.6 + len(cmd) * 0.12, f"transform:translateX({len(cmd) * 14 * CHAR:.1f}px)"),
                   (T - 0.3, f"transform:translateX({len(cmd) * 14 * CHAR:.1f}px)"), (T - 0.29, "transform:translateX(0)"),
                   (T, "transform:translateX(0)")], timing=f"steps({len(cmd)},end)")
    l2 = tl.show(1.4, fade=0.05)
    l3 = tl.show(1.8, fade=0.05)
    body = [
        mono(28, 64, "$ ", 14, GREEN), mono(x, 64, cmd, 14, FG),
        f'<rect x="{x - 1}" y="50" width="{len(cmd) * 14 * CHAR + 2:.1f}" height="20" fill="{BG}" class="{cover}"/>',
        f'<g class="{l2}">{mono(28, 88, "logout", 14, MUTED)}</g>',
        f'<g class="{l3}">{mono(28, 110, "Connection to github.com closed.", 14, MUTED)}</g>',
    ]
    return window(W, H, "~/miaad", "\n".join(body), tl.css(), "$ exit. logout. Connection to github.com closed.")


# ---------------------------------------------------------------------------------------------
# Social buttons: one SVG per link (an <img> can only carry one link)
# ---------------------------------------------------------------------------------------------
SANS = "font-family:-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
SOCIAL = [
    ("linkedin", "LinkedIn", "Miaad Kimiagari", "#0a66c2",
     f'<text x="16" y="22.5" text-anchor="middle" font-size="17" font-weight="700" fill="#ffffff" style="{SANS}">in</text>'),
    ("kaggle", "Kaggle", "miaadkimiagari2004", "#20beff",
     f'<text x="16" y="23.5" text-anchor="middle" font-size="21" font-weight="700" fill="#ffffff" style="{SANS}">k</text>'),
    ("medium", "Medium", "@mia.kimiagari", "#f2f2f2",
     '<circle cx="11" cy="16" r="6.5" fill="#111"/><ellipse cx="21.2" cy="16" rx="3.2" ry="6" fill="#111"/>'
     '<ellipse cx="26.6" cy="16" rx="1.2" ry="5.4" fill="#111"/>'),
    ("stackoverflow", "Stack Overflow", "users/20930226", "#f48024",
     '<path d="M8.5 19v6.5h15V19" fill="none" stroke="#fff" stroke-width="2"/>'
     '<g fill="#fff"><rect x="11" y="21" width="10" height="2"/>'
     '<rect x="11" y="21" width="10" height="2" transform="rotate(-12 11 21) translate(0.6 -3.4)"/>'
     '<rect x="11" y="21" width="10" height="2" transform="rotate(-26 11 21) translate(1.8 -6.6)"/>'
     '<rect x="11" y="21" width="10" height="2" transform="rotate(-42 11 21) translate(3.6 -9.6)"/></g>'),
    ("leetcode", "LeetCode", "user3197d", "#ffa116",
     '<path d="M19.5 7.5L11 16l8.5 8.5" fill="none" stroke="#1b1b1b" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
     '<path d="M15.5 16H24" stroke="#1b1b1b" stroke-width="3" stroke-linecap="round" opacity="0.55"/>'),
]


def social(i, key, name, handle, color, glyph):
    W, H = 184, 56
    at = 0.6 + i * 0.3
    T = 7.0
    tl = Timeline(T, "s", end=at + 1.4)
    glow = tl.kf([(0, "stroke-opacity:0"), (at, "stroke-opacity:0"), (at + 0.35, "stroke-opacity:1"),
                  (at + 1.3, "stroke-opacity:0"), (T, "stroke-opacity:0")], timing="ease-in-out")
    shine = tl.kf([(0, "transform:translateX(-80px)"), (at, "transform:translateX(-80px)"),
                   (at + 0.9, f"transform:translateX({W + 40}px)"), (T, f"transform:translateX({W + 40}px)")],
                  timing="ease-in-out")
    body = [
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="{BG}" stroke="{BORDER}"/>',
        f'<g clip-path="url(#b)"><g transform="skewX(-20)"><rect x="0" y="-10" width="46" height="{H + 20}" fill="url(#sh)" '
        f'class="{shine}" style="transform:translateX(-80px)"/></g></g>',
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{color}" '
        f'stroke-width="1.5" class="{glow}" style="stroke-opacity:0"/>',
        f'<g transform="translate(12 12)"><rect width="32" height="32" rx="8" fill="{color}"/>{glyph}</g>',
        mono(56, 26, name, 12.5, FG, weight="700"),
        mono(56, 42, handle, 10, MUTED),
        f'<path d="M{W - 16} 9h6v6M{W - 10} 9l-7 7" fill="none" stroke="{MUTED}" stroke-width="1.5" '
        f'stroke-linecap="round" stroke-linejoin="round"/>',
    ]
    defs = (f'<clipPath id="b"><rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12"/></clipPath>'
            '<linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
            '<stop offset="0.5" stop-color="#fff" stop-opacity="0.09"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="{esc(name)}: {esc(handle)}"><style>text{{font-family:{MONO};white-space:pre}}{tl.css()}'
            '@media (prefers-reduced-motion:reduce){*{animation:none!important}}</style>'
            f'<defs>{defs}</defs>' + "\n".join(body) + "</svg>\n")


if __name__ == "__main__":
    import art_cards
    import art_hero
    import art_more

    save("hero.svg", art_hero.hero())
    for name, fn in art_cards.CARDS + art_more.CARDS:
        save(f"cards/{name}.svg", fn())
    save("footer.svg", footer())
    for i, item in enumerate(SOCIAL):
        save(f"social/{item[0]}.svg", social(i, *item))
