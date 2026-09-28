"""The eight featured project cards. Each one acts out what its project does."""
import math
import random

from make_art import LAKE, donut_frame, lake_outcomes, terminal, value_iteration
from svgkit import (AMBER, BG, BLUE, BORDER, CHAR, CORAL, FAINT, FG, GREEN, HIDE, MUTED, PANEL, VIOLET, YELLOW,
                    Timeline, card, glow, grad, mono)


def rng_(seed):
    return random.Random(seed)


# ---------------------------------------------------------------------------------------------
# DCGAN flowers
# ---------------------------------------------------------------------------------------------
def petal(length, width):
    L, w = length, width
    return (f"M0 0C{-w:.1f} {-L * 0.3:.1f} {-w * 0.85:.1f} {-L * 0.85:.1f} 0 {-L:.1f}"
            f"C{w * 0.85:.1f} {-L * 0.85:.1f} {w:.1f} {-L * 0.3:.1f} 0 0Z")


def flower(i, k, base, tip, back, center, rot, rng):
    cx, cy = 61, 62
    g = [f'<g transform="translate({cx} {cy}) rotate({rot})">']
    for j in range(k):
        a = j * 360 / k + 180 / k
        g.append(f'<path d="{petal(40, 13)}" transform="rotate({a:.1f})" fill="url(#pb{i})" opacity="0.9"/>')
    for j in range(k):
        a = j * 360 / k + rng.uniform(-6, 6)
        L = 47 + rng.uniform(-4, 3)
        g.append(f'<g transform="rotate({a:.1f})"><path d="{petal(L, 15)}" fill="url(#pf{i})" stroke="{back}" stroke-width="0.6"/>'
                 f'<path d="M0 -8 Q{rng.uniform(-2, 2):.1f} {-L * 0.5:.1f} 0 {-L * 0.86:.1f}" stroke="{tip}" stroke-width="0.8" '
                 f'fill="none" opacity="0.55"/>'
                 f'<path d="M-4 {-L * 0.3:.1f} Q-6 {-L * 0.6:.1f} -2 {-L * 0.8:.1f}" stroke="#ffffff" stroke-width="0.7" '
                 f'fill="none" opacity="0.18"/></g>')
    g.append(f'<circle r="13" fill="url(#pc{i})"/>')
    golden = math.pi * (3 - math.sqrt(5))
    for n in range(1, 60):
        r = 1.55 * math.sqrt(n)
        if r > 11.5:
            break
        a = n * golden
        g.append(f'<circle cx="{r * math.cos(a):.2f}" cy="{r * math.sin(a):.2f}" r="{0.55 + 0.04 * r:.2f}" fill="{center}" '
                 f'opacity="{0.5 + 0.04 * r:.2f}"/>')
    g.append('<path d="M-8 -6 A10 10 0 0 1 4 -10" stroke="#ffffff" stroke-width="1.2" fill="none" opacity="0.25"/>')
    g.append("</g>")
    return "".join(g)


def card_dcgan():
    T = 8.0
    tl = Timeline(T, "g")
    rng = rng_(7)
    S, gap = 122, 11
    x0, y0 = 16, 50
    specs = [(5, "#ff5d8f", "#ffd1dc", "#b8325a", "#ffcf5c", 12),
             (7, "#8f5cf7", "#e2cfff", "#5b2fb8", "#ffe08a", -8),
             (11, "#ffb020", "#fff0b8", "#b86d00", "#7a3b00", 4)]
    defs, parts = [], []
    for i, (k, base, tip, back, center, rot) in enumerate(specs):
        x = x0 + i * (S + gap)
        defs.append(f'<radialGradient id="pf{i}" cx="0.5" cy="1" r="1.1" fx="0.5" fy="1"><stop offset="0" stop-color="{back}"/>'
                    f'<stop offset="0.35" stop-color="{base}"/><stop offset="1" stop-color="{tip}"/></radialGradient>'
                    f'<radialGradient id="pb{i}" cx="0.5" cy="1" r="1"><stop offset="0" stop-color="{back}"/>'
                    f'<stop offset="1" stop-color="{base}"/></radialGradient>'
                    f'<radialGradient id="pc{i}"><stop offset="0" stop-color="#6b4210"/><stop offset="0.7" stop-color="#3a2206"/>'
                    f'<stop offset="1" stop-color="#1c1003"/></radialGradient>'
                    f'<clipPath id="tc{i}"><rect x="{x}" y="{y0}" width="{S}" height="{S}" rx="6"/></clipPath>'
                    f'<filter id="nz{i}" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" '
                    f'baseFrequency="0.62" numOctaves="2" seed="{i * 11 + 3}"/>'
                    f'<feColorMatrix type="matrix" values="2.6 0 0 0 -0.8  0 2.6 0 0 -0.8  0 0 2.6 0 -0.8  0 0 0 0 1"/></filter>')
        bokeh = "".join(f'<circle cx="{rng.uniform(0, S):.0f}" cy="{rng.uniform(0, S):.0f}" r="{rng.uniform(6, 16):.0f}" '
                        f'fill="{rng.choice(["#3f8f4a", "#7fb34a", "#2f6d3a", "#c9d86a"])}" opacity="{rng.uniform(0.15, 0.4):.2f}"/>'
                        for _ in range(9))
        start = 0.5 + i * 0.45
        noise = tl.kf([(0, "opacity:1"), (start, "opacity:1"), (start + 0.45, "opacity:0.78"), (start + 0.9, "opacity:0.55"),
                       (start + 1.35, "opacity:0.3"), (start + 1.8, "opacity:0.1"), (start + 2.2, "opacity:0"),
                       (T - 0.8, "opacity:0"), (T - 0.3, "opacity:1"), (T, "opacity:1")])
        soft = tl.kf([(0, "opacity:0"), (start, "opacity:0"), (start + 0.5, "opacity:1"), (start + 1.5, "opacity:1"),
                      (start + 2.1, "opacity:0"), (T, "opacity:0")])
        sharp = tl.show(start + 1.4, T - 0.9, fade=0.7)
        fl = flower(i, k, base, tip, back, center, rot, rng)
        parts.append(f'<g clip-path="url(#tc{i})"><g transform="translate({x} {y0})">'
                     f'<rect width="{S}" height="{S}" fill="url(#bg{i})"/>'
                     f'<g filter="url(#soft)">{bokeh}</g>'
                     f'</g>'
                     f'<g transform="translate({x} {y0})"><g class="{soft}" style="opacity:0" filter="url(#blur)">{fl}</g>'
                     f'<g class="{sharp}">{fl}</g></g>'
                     f'<rect x="{x}" y="{y0}" width="{S}" height="{S}" filter="url(#nz{i})" class="{noise}" style="opacity:0"/>'
                     f'</g><rect x="{x + 0.5}" y="{y0 + 0.5}" width="{S - 1}" height="{S - 1}" rx="6" fill="none" stroke="{BORDER}"/>')
        defs.append(f'<radialGradient id="bg{i}" cx="0.5" cy="0.45" r="0.75"><stop offset="0" stop-color="#1f4d2c"/>'
                    f'<stop offset="1" stop-color="#06120a"/></radialGradient>')
    body = "\n".join(parts)
    defs.append('<filter id="blur"><feGaussianBlur stdDeviation="5"/></filter>'
                '<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="4"/></filter>')
    # progress hairline under the tiles
    bar = tl.kf([(0, "transform:scaleX(0)"), (0.5, "transform:scaleX(0)"), (3.9, "transform:scaleX(1)"),
                 (T - 0.8, "transform:scaleX(1)"), (T - 0.3, "transform:scaleX(0)"), (T, "transform:scaleX(0)")])
    body += (f'<rect x="{x0}" y="181" width="{3 * S + 2 * gap}" height="2" rx="1" fill="{FAINT}"/>'
             f'<rect x="{x0}" y="181" width="{3 * S + 2 * gap}" height="2" rx="1" fill="url(#pg)" class="{bar}" '
             f'style="transform-origin:{x0}px 0"/>')
    defs.append(grad("pg", x0, x0 + 3 * S + 2 * gap, ("#ff5d8f", "#8f5cf7", "#ffb020")))
    return card("~/dcgan-flowers", "Flowers from noise", "a DCGAN in PyTorch that learns to paint flowers",
                "PyTorch", "#ee4c2c", body, tl.css(),
                "Three squares of colour noise resolve into detailed flowers.", "".join(defs))


# ---------------------------------------------------------------------------------------------
# A cat, drawn two ways (line art and full colour), 100 x 100 box
# ---------------------------------------------------------------------------------------------
HEAD = "M17 52C16 40 17 26 21 12L39 29C46 27 54 27 61 29L79 12C83 26 84 40 83 52C85 74 70 88 50 89C30 88 15 74 17 52Z"
TUFT_L = "M18 58L11 61L17 64L10 68L18 70L13 75L21 75"
TUFT_R = "M82 58L89 61L83 64L90 68L82 70L87 75L79 75"
EAR_IN = "M24 19L36 31L26 36Z M76 19L64 31L74 36Z"
STRIPES = "M50 30V41 M43 31L45 41 M57 31L55 41 M38 33Q41 38 40 43 M62 33Q59 38 60 43"
CHEEK = "M22 56L31 58 M21 62L30 62 M78 56L69 58 M79 62L70 62"
EYES = "M30 51Q37 43 45 51Q37 58 30 51Z M55 51Q63 43 70 51Q63 58 55 51Z"
PUPILS = "M37.5 46.5V55.5 M62.5 46.5V55.5"
NOSE = "M46 62Q50 60 54 62L50.8 66.5Q50 67.3 49.2 66.5Z"
MOUTH = "M50 67V70 M50 70Q46 75 41 72 M50 70Q54 75 59 72"
WHISK = ("M38 66Q24 62 8 61 M38 69Q24 68 7 70 M39 72Q26 74 11 79 "
         "M62 66Q76 62 92 61 M62 69Q76 68 93 70 M61 72Q74 74 89 79")


def cat_line(cls):
    paths = [HEAD, TUFT_L, TUFT_R, EAR_IN, STRIPES, CHEEK, EYES, PUPILS, NOSE, MOUTH, WHISK]
    return "".join(f'<path d="{d}" pathLength="1" class="{cls}"/>' for d in paths)


CAT_DEFS = ('<radialGradient id="fur" cx="0.5" cy="0.35" r="0.7"><stop offset="0" stop-color="#ffb65c"/>'
            '<stop offset="0.6" stop-color="#e8862f"/><stop offset="1" stop-color="#b85f16"/></radialGradient>'
            '<linearGradient id="ear" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7c0ad"/>'
            '<stop offset="1" stop-color="#d98a74"/></linearGradient>'
            '<radialGradient id="muz" cx="0.5" cy="0.4" r="0.6"><stop offset="0" stop-color="#fff6e8"/>'
            '<stop offset="1" stop-color="#f1cfa0"/></radialGradient>'
            '<radialGradient id="iris" cx="0.5" cy="0.5" r="0.55"><stop offset="0" stop-color="#e8f27a"/>'
            '<stop offset="0.55" stop-color="#9ccc3c"/><stop offset="1" stop-color="#4d7d17"/></radialGradient>'
            '<linearGradient id="nose" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f5a0a8"/>'
            '<stop offset="1" stop-color="#c85468"/></linearGradient>'
            '<filter id="shadow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3"/></filter>')


def cat_color():
    r = rng_(3)
    fur = "".join(f'<path d="M{x:.1f} {y:.1f}l{r.uniform(-1.5, 1.5):.1f} {r.uniform(2, 4):.1f}" stroke="#9c4f12" '
                  f'stroke-width="0.7" opacity="0.55"/>'
                  for x, y in [(r.uniform(22, 78), r.uniform(20, 84)) for _ in range(46)]
                  if not (30 < x < 70 and 45 < y < 76))
    return (f'<ellipse cx="50" cy="90" rx="30" ry="5" fill="#000" opacity="0.35" filter="url(#shadow)"/>'
            f'<path d="{TUFT_L}Z" fill="#e8862f"/><path d="{TUFT_R}Z" fill="#e8862f"/>'
            f'<path d="{HEAD}" fill="url(#fur)" stroke="#8a4512" stroke-width="0.8"/>'
            f'<path d="{EAR_IN}" fill="url(#ear)"/>'
            '<path d="M27 22L31 30 M73 22L69 30 M29 21L33 28 M71 21L67 28" stroke="#fff3e6" stroke-width="0.5" opacity="0.8"/>'
            f'{fur}'
            f'<path d="{STRIPES}" stroke="#9c4e14" stroke-width="2.2" stroke-linecap="round" fill="none"/>'
            f'<path d="{CHEEK}" stroke="#9c4e14" stroke-width="2" stroke-linecap="round"/>'
            '<ellipse cx="44" cy="69" rx="8" ry="6.5" fill="url(#muz)"/><ellipse cx="56" cy="69" rx="8" ry="6.5" fill="url(#muz)"/>'
            '<ellipse cx="50" cy="76" rx="7" ry="4.5" fill="url(#muz)"/>'
            f'<path d="{EYES}" fill="url(#iris)" stroke="#2b1a08" stroke-width="1.3"/>'
            '<ellipse cx="37.5" cy="51" rx="1.8" ry="5" fill="#0c0f14"/><ellipse cx="62.5" cy="51" rx="1.8" ry="5" fill="#0c0f14"/>'
            '<circle cx="35.8" cy="48.6" r="1.3" fill="#fff"/><circle cx="60.8" cy="48.6" r="1.3" fill="#fff"/>'
            '<circle cx="39.4" cy="53" r="0.6" fill="#fff" opacity="0.7"/><circle cx="64.4" cy="53" r="0.6" fill="#fff" opacity="0.7"/>'
            f'<path d="{NOSE}" fill="url(#nose)"/><ellipse cx="48.6" cy="62.3" rx="1.4" ry="0.7" fill="#fff" opacity="0.6"/>'
            f'<path d="{MOUTH}" stroke="#5a2c10" stroke-width="1.1" fill="none" stroke-linecap="round"/>'
            f'<path d="{WHISK}" stroke="#fffaf0" stroke-width="0.55" fill="none" opacity="0.9"/>'
            '<circle cx="42" cy="68" r="0.6" fill="#8a5a30"/><circle cx="45" cy="70" r="0.6" fill="#8a5a30"/>'
            '<circle cx="58" cy="68" r="0.6" fill="#8a5a30"/><circle cx="55" cy="70" r="0.6" fill="#8a5a30"/>')


def wipe(tl, x, y, w, h, t_on, t_off, color, cid):
    """Cover that slides down to reveal what is under it, with a bright scan edge."""
    cover = tl.kf([(0, "transform:translateY(0)"), (t_on, "transform:translateY(0)"),
                   (t_on + 1.1, f"transform:translateY({h}px)"), (t_off, f"transform:translateY({h}px)"),
                   (t_off + 0.01, "transform:translateY(0)"), (tl.T, "transform:translateY(0)")], timing="ease-in-out")
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" class="{cover}" style="transform:translateY({h}px)"/>'
            f'<rect x="{x}" y="{y - 1}" width="{w}" height="2" fill="#7ee7ff" filter="url(#{cid})" class="{cover}" '
            f'style="transform:translateY({h}px)"/>')


# ---------------------------------------------------------------------------------------------
# pix2pix: edges to cats
# ---------------------------------------------------------------------------------------------
def card_pix2pix():
    T = 8.0
    tl = Timeline(T, "p")
    L, R, Y, S = 26, 274, 50, 122
    draw = tl.kf([(0, "stroke-dashoffset:1"), (0.3, "stroke-dashoffset:1"), (2.4, "stroke-dashoffset:0"),
                  (T - 0.5, "stroke-dashoffset:0"), (T - 0.2, "stroke-dashoffset:1"), (T, "stroke-dashoffset:1")],
                 timing="ease-in-out")
    parts = [
        f'<rect x="{L}" y="{Y}" width="{S}" height="{S}" rx="6" fill="#f4f1ea"/>',
        f'<rect x="{L}" y="{Y}" width="{S}" height="{S}" rx="6" fill="url(#paper)" opacity="0.5"/>',
        f'<g transform="translate({L + 4} {Y + 4}) scale(1.14)" fill="none" stroke="#23272e" stroke-width="1.15" '
        f'stroke-linejoin="round" stroke-linecap="round" style="stroke-dasharray:1">{cat_line(draw)}</g>',
        f'<defs><clipPath id="rc"><rect x="{R}" y="{Y}" width="{S}" height="{S}" rx="6"/></clipPath></defs>',
        f'<g clip-path="url(#rc)"><rect x="{R}" y="{Y}" width="{S}" height="{S}" fill="url(#sky)"/>'
        f'<circle cx="{R + 96}" cy="{Y + 24}" r="26" fill="#ffffff" opacity="0.25" filter="url(#shadow)"/>'
        f'<g transform="translate({R + 4} {Y + 4}) scale(1.14)">{cat_color()}</g>'
        f'{wipe(tl, R, Y, S, S, 3.3, T - 0.5, PANEL, "scan")}</g>',
        f'<rect x="{R + 0.5}" y="{Y + 0.5}" width="{S - 1}" height="{S - 1}" rx="6" fill="none" stroke="{BORDER}"/>',
    ]
    # generator in the middle: encoder-decoder hourglass with signal dots
    mx = (L + S + R) / 2
    parts.append(f'<path d="M{mx - 38} {Y + 30}L{mx - 6} {Y + 52}V{Y + 70}L{mx - 38} {Y + 92}Z" fill="#1a2332" stroke="{BLUE}" stroke-width="1"/>'
                 f'<path d="M{mx + 38} {Y + 30}L{mx + 6} {Y + 52}V{Y + 70}L{mx + 38} {Y + 92}Z" fill="#1a2332" stroke="{GREEN}" stroke-width="1"/>'
                 f'<rect x="{mx - 6}" y="{Y + 52}" width="12" height="18" fill="#241a33" stroke="{VIOLET}"/>')
    for j in range(5):
        on = 2.3 + j * 0.16
        d = tl.kf([(0, "transform:translateX(0);opacity:0"), (on, "transform:translateX(0);opacity:0"),
                   (on + 0.05, "transform:translateX(0);opacity:1"), (on + 0.9, "transform:translateX(76px);opacity:1"),
                   (on + 0.95, "transform:translateX(76px);opacity:0"), (T, "transform:translateX(76px);opacity:0")])
        parts.append(f'<circle cx="{mx - 38}" cy="{Y + 61 + (j - 2) * 5}" r="1.8" fill="{AMBER}" class="{d}" style="opacity:0"/>')
    parts.append(mono(mx, Y + 112, "G", 12, AMBER, anchor="middle", weight="700"))
    parts.append(mono(L + S / 2, 186, "edges", 10, MUTED, anchor="middle"))
    parts.append(mono(R + S / 2, 186, "G(edges)", 10, MUTED, anchor="middle"))
    defs = (CAT_DEFS + glow("scan", 1.5) +
            '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a9c7e3"/>'
            '<stop offset="1" stop-color="#e9e2d6"/></linearGradient>'
            '<pattern id="paper" width="6" height="6" patternUnits="userSpaceOnUse"><path d="M0 6L6 0" stroke="#d9d3c5" stroke-width="0.4"/></pattern>')
    return card("~/edges-to-cats", "Edges to cats", "pix2pix in TensorFlow: draw a sketch, get a cat",
                "TensorFlow", "#ff6f00", "\n".join(parts), tl.css(),
                "A cat sketch draws itself, passes through an encoder-decoder, and comes out as a fully coloured cat.", defs)


# ---------------------------------------------------------------------------------------------
# U-Net segmentation
# ---------------------------------------------------------------------------------------------
def slab(x, y, w, h, d, front, top, side):
    return (f'<path d="M{x} {y}h{w}v{h}h{-w}Z" fill="{front}"/>'
            f'<path d="M{x} {y}l{d} {-d / 2}h{w}l{-d} {d / 2}Z" fill="{top}"/>'
            f'<path d="M{x + w} {y}l{d} {-d / 2}v{h}l{-d} {d / 2}Z" fill="{side}"/>')


def card_unet():
    T = 8.0
    tl = Timeline(T, "u")
    L, R, Y, S = 16, 282, 52, 122
    parts = [f'<defs><clipPath id="pl"><rect x="{L}" y="{Y}" width="{S}" height="{S}" rx="6"/></clipPath>'
             f'<clipPath id="pr"><rect x="{R}" y="{Y}" width="{S}" height="{S}" rx="6"/></clipPath></defs>']
    photo = (f'<rect x="{L}" y="{Y}" width="{S}" height="{S}" fill="url(#wall)"/>'
             f'<rect x="{L}" y="{Y + 78}" width="{S}" height="{S - 78}" fill="#5b4636"/>'
             f'<rect x="{L}" y="{Y + 78}" width="{S}" height="{S - 78}" fill="#000" filter="url(#weave)" opacity="0.35"/>'
             f'<path d="M{L} {Y + 78}H{L + S}" stroke="#3b2c21" stroke-width="2"/>'
             f'<rect x="{L + 8}" y="{Y + 10}" width="30" height="40" rx="2" fill="#2d3a4d" stroke="#1e2733"/>'
             f'<g transform="translate({L + 8} {Y + 6}) scale(1.06)">{cat_color()}</g>')
    scan = tl.kf([(0, "transform:translateY(0);opacity:0"), (0.3, "transform:translateY(0);opacity:1"),
                  (1.7, f"transform:translateY({S}px);opacity:1"), (1.75, f"transform:translateY({S}px);opacity:0"),
                  (T, f"transform:translateY({S}px);opacity:0")], timing="ease-in-out")
    parts.append(f'<g clip-path="url(#pl)">{photo}<rect x="{L}" y="{Y}" width="{S}" height="2" fill="#7ee7ff" '
                 f'filter="url(#scan)" class="{scan}" style="opacity:0"/></g>')
    parts.append(f'<rect x="{L + 0.5}" y="{Y + 0.5}" width="{S - 1}" height="{S - 1}" rx="6" fill="none" stroke="{BORDER}"/>')
    # isometric U-Net
    levels = [(146, 62, 56, 5), (160, 78, 40, 7), (175, 92, 26, 9)]
    bott = (193, 104, 16, 12)
    dec = [(214, 92, 26, 9), (230, 78, 40, 7), (247, 62, 56, 5)]
    order = levels + [bott] + dec
    colors = [(BLUE, "#a8d4ff", "#3d6a99")] * 3 + [(VIOLET, "#ecdcff", "#7d5bb0")] + [(GREEN, "#c3f5c9", "#3f8a4a")] * 3
    for (ex, ey, eh, ew), (dx, dy, dh, dw) in zip(levels, reversed(dec)):
        parts.append(f'<path d="M{ex + ew + 4} {ey - 8}Q{(ex + dx) / 2 + 4} {ey - 22} {dx + 4} {dy - 8}" fill="none" '
                     f'stroke="{FAINT}" stroke-dasharray="2 3"/>')
    for i, ((x, y, h, w), (f, tp, sd)) in enumerate(zip(order, colors)):
        parts.append(slab(x, y, w, h, 8, "#1b2230", "#2a3345", "#141a24"))
        on = 1.8 + i * 0.22
        lit = tl.kf([(0, "opacity:0"), (on, "opacity:0"), (on + 0.12, "opacity:1"), (T - 0.6, "opacity:1"),
                     (T - 0.3, "opacity:0"), (T, "opacity:0")])
        parts.append(f'<g class="{lit}" style="opacity:1" filter="url(#lift)">{slab(x, y, w, h, 8, f, tp, sd)}</g>')
    parts.append(mono(206, 186, "u-net", 10, MUTED, anchor="middle"))
    # mask: pet / boundary / background (Oxford-IIIT trimap)
    mask = (f'<rect x="{R}" y="{Y}" width="{S}" height="{S}" fill="#120e22"/>'
            f'<rect x="{R}" y="{Y}" width="{S}" height="{S}" fill="url(#grid)"/>'
            f'<g transform="translate({R + 8} {Y + 6}) scale(1.06)">'
            f'<path d="{HEAD}" fill="{VIOLET}" fill-opacity="0.85" stroke="{AMBER}" stroke-width="2.6"/>'
            f'<path d="{TUFT_L}" fill="none" stroke="{AMBER}" stroke-width="2.6"/>'
            f'<path d="{TUFT_R}" fill="none" stroke="{AMBER}" stroke-width="2.6"/></g>')
    parts.append(f'<g clip-path="url(#pr)">{mask}{wipe(tl, R, Y, S, S, 3.6, T - 0.5, PANEL, "scan")}</g>')
    parts.append(f'<rect x="{R + 0.5}" y="{Y + 0.5}" width="{S - 1}" height="{S - 1}" rx="6" fill="none" stroke="{BORDER}"/>')
    for i, (lab, col) in enumerate([("pet", VIOLET), ("edge", AMBER), ("bg", "#3a2f5c")]):
        lx = R + 8 + i * 40
        parts.append(f'<rect x="{lx}" y="180" width="8" height="8" rx="2" fill="{col}"/>{mono(lx + 12, 187, lab, 9, MUTED)}')
    parts.append(mono(L + S / 2, 186, "image", 10, MUTED, anchor="middle"))
    defs = (CAT_DEFS + glow("scan", 1.5) + glow("lift", 1.6) +
            '<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5f7189"/>'
            '<stop offset="1" stop-color="#46546a"/></linearGradient>'
            '<filter id="weave" x="0" y="0" width="100%" height="100%"><feTurbulence type="turbulence" baseFrequency="0.9 0.25" '
            'numOctaves="2" seed="4"/><feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1.2 -0.2"/></filter>'
            '<pattern id="grid" width="6" height="6" patternUnits="userSpaceOnUse"><path d="M6 0H0V6" fill="none" stroke="#2a2346" '
            'stroke-width="0.5"/></pattern>')
    return card("~/unet-segmentation", "U-Net pet segmentation", "pixel-level pet masks on Oxford-IIIT Pet",
                "TensorFlow", "#ff6f00", "\n".join(parts), tl.css(),
                "A pet photo is scanned, the signal runs down and back up a U-Net, and a pet mask with boundary is revealed.",
                defs)


# ---------------------------------------------------------------------------------------------
# Frozen Lake, isometric, with real value iteration and a real slippery episode
# ---------------------------------------------------------------------------------------------
def card_frozen_lake():
    history, pi = value_iteration()
    for seed in range(1000):
        r = rng_(seed)
        s, path = 0, [0]
        while not terminal(s) and len(path) < 16:
            s = r.choice(lake_outcomes(s, pi[s]))
            path.append(s)
        if LAKE[s // 4][s % 4] == "G" and 8 <= len(path) <= 12:
            break
    T = 12.0
    tl = Timeline(T, "f")
    TW, TH, TD = 58, 29, 9
    ox, oy = 256, 54

    def iso(c, r_):
        return ox + (c - r_) * TW / 2, oy + (c + r_) * TH / 2

    def diamond(cx, cy, s=1.0):
        w, h = TW / 2 * s, TH / 2 * s
        return f"M{cx:.1f} {cy - h:.1f}L{cx + w:.1f} {cy:.1f}L{cx:.1f} {cy + h:.1f}L{cx - w:.1f} {cy:.1f}Z"

    parts = []
    tiles = sorted(range(16), key=lambda s_: (s_ % 4 + s_ // 4))
    for s_ in tiles:
        c, r_ = s_ % 4, s_ // 4
        cx, cy = iso(c, r_)
        cy += TH / 2
        t = LAKE[r_][c]
        parts.append(f'<path d="M{cx - TW / 2:.1f} {cy:.1f}L{cx:.1f} {cy + TH / 2:.1f}V{cy + TH / 2 + TD:.1f}L{cx - TW / 2:.1f} {cy + TD:.1f}Z" fill="#4e7d99"/>'
                     f'<path d="M{cx + TW / 2:.1f} {cy:.1f}L{cx:.1f} {cy + TH / 2:.1f}V{cy + TH / 2 + TD:.1f}L{cx + TW / 2:.1f} {cy + TD:.1f}Z" fill="#3b6680"/>')
        if t == "H":
            parts.append(f'<path d="{diamond(cx, cy)}" fill="url(#water)"/>')
            rip = tl.kf([(0, "transform:scale(0.3);opacity:0.8"), (2.0, "transform:scale(1);opacity:0"),
                         (2.01, "transform:scale(0.3);opacity:0.8"), (4.0, "transform:scale(1);opacity:0"),
                         (4.01, "transform:scale(0.3);opacity:0.8"), (6.0, "transform:scale(1);opacity:0"),
                         (6.01, "transform:scale(0.3);opacity:0.8"), (8.0, "transform:scale(1);opacity:0"),
                         (8.01, "transform:scale(0.3);opacity:0.8"), (10.0, "transform:scale(1);opacity:0"),
                         (10.01, "transform:scale(0.3);opacity:0.8"), (12.0, "transform:scale(1);opacity:0")])
            parts.append(f'<g transform="translate({cx:.1f} {cy:.1f})"><ellipse rx="18" ry="9" fill="none" stroke="#9fd3ff" '
                         f'stroke-width="0.8" class="{rip}" style="animation-delay:{-s_ * 0.37:.2f}s"/></g>')
        else:
            parts.append(f'<path d="{diamond(cx, cy)}" fill="url(#ice)"/>'
                         f'<path d="M{cx - 12:.1f} {cy - 2:.1f}l7 2 4 -3 6 4" stroke="#ffffff" stroke-width="0.6" fill="none" opacity="0.5"/>')
        if t == "G":
            parts.append(f'<path d="{diamond(cx, cy, 0.8)}" fill="{GREEN}" opacity="0.35"/>'
                         f'<path d="M{cx:.1f} {cy:.1f}V{cy - 24:.1f}" stroke="#e6edf3" stroke-width="1.4"/>'
                         f'<path d="M{cx:.1f} {cy - 24:.1f}l13 4 -13 4Z" fill="{GREEN}" class="flag"/>')
    # value sweeps (real numbers)
    sweeps = [1, 2, 3, 5, 8, 13, 30, 200]
    vmax = max(history[-1])
    for n, it in enumerate(sweeps):
        on = 0.4 + n * 0.55
        last = n == len(sweeps) - 1
        cls = tl.show(on, 5.2, fade=0.05) if last else tl.pulse(on, on + 0.55)
        g = [f'<g class="{cls}"{"" if last else HIDE}>']
        for s_ in range(16):
            if terminal(s_):
                continue
            c, r_ = s_ % 4, s_ // 4
            cx, cy = iso(c, r_)
            cy += TH / 2
            v = history[it][s_]
            g.append(f'<path d="{diamond(cx, cy, 0.86)}" fill="{AMBER}" fill-opacity="{0.1 + 0.8 * v / vmax:.2f}"/>')
            g.append(mono(cx, cy + 3, f"{v:.2f}"[1:], 8.5, "#0b0f14", anchor="middle", weight="700"))
        g.append(mono(22, 62, f"sweep {it:>3}", 10, AMBER))
        g.append(mono(22, 78, f"V(S) {history[it][0]:.3f}", 10, FG))
        g.append("</g>")
        parts.append("".join(g))
    parts.append(mono(22, 94, "gamma 0.99", 10, MUTED))
    # greedy policy arrows on the ice
    arrows = [f'<g class="{tl.show(5.0, fade=0.3)}">']
    vec = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
    for s_ in range(16):
        if terminal(s_):
            continue
        c, r_ = s_ % 4, s_ // 4
        cx, cy = iso(c, r_)
        cy += TH / 2
        dc, dr = vec[pi[s_]]
        sx, sy = (dc - dr) * TW / 2, (dc + dr) * TH / 2
        ang = math.degrees(math.atan2(sy, sx))
        arrows.append(f'<path d="M-9 0H4M1 -4L7 0L1 4" stroke="#123047" stroke-width="2" fill="none" stroke-linecap="round" '
                      f'stroke-linejoin="round" transform="translate({cx:.1f} {cy:.1f}) rotate({ang:.1f})"/>')
    arrows.append("</g>")
    parts.append("".join(arrows))
    parts.append(f'<g class="{tl.show(5.0, fade=0.3)}">{mono(22, 120, "greedy policy", 10, MUTED)}'
                 f'{mono(22, 136, f"episode: {len(path) - 1} steps", 10, FG)}</g>')
    # agent hops along the sampled episode
    start, dt = 5.8, 0.42
    pts = []
    for s_ in path:
        cx, cy = iso(s_ % 4, s_ // 4)
        pts.append((cx, cy + TH / 2))
    stops = [(0, f"transform:translate({pts[0][0]:.1f}px,{pts[0][1]:.1f}px);opacity:0"),
             (start - 0.3, f"transform:translate({pts[0][0]:.1f}px,{pts[0][1]:.1f}px);opacity:0"),
             (start, f"transform:translate({pts[0][0]:.1f}px,{pts[0][1]:.1f}px);opacity:1")]
    for i in range(1, len(pts)):
        (ax, ay), (bx, by) = pts[i - 1], pts[i]
        t0 = start + (i - 1) * dt + 0.12
        stops.append((t0, f"transform:translate({ax:.1f}px,{ay:.1f}px);opacity:1"))
        stops.append((t0 + 0.14, f"transform:translate({(ax + bx) / 2:.1f}px,{(ay + by) / 2 - 12:.1f}px);opacity:1"))
        stops.append((t0 + 0.28, f"transform:translate({bx:.1f}px,{by:.1f}px);opacity:1"))
    ex, ey = pts[-1]
    stops += [(T - 0.5, f"transform:translate({ex:.1f}px,{ey:.1f}px);opacity:1"),
              (T - 0.2, f"transform:translate({ex:.1f}px,{ey:.1f}px);opacity:0"),
              (T, f"transform:translate({ex:.1f}px,{ey:.1f}px);opacity:0")]
    agent = tl.kf(stops)
    parts.append(f'<g class="{agent}" style="transform:translate({ex:.1f}px,{ey:.1f}px)">'
                 f'<ellipse cx="0" cy="1" rx="7" ry="3.5" fill="#000" opacity="0.35"/>'
                 f'<circle cx="0" cy="-7" r="7" fill="url(#ball)"/></g>')
    css = tl.css() + ".flag{transform-box:fill-box;transform-origin:left center;animation:wave 1.2s ease-in-out infinite}" \
                     "@keyframes wave{50%{transform:scaleX(0.75) skewY(4deg)}}"
    defs = ('<linearGradient id="ice" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e8f7ff"/>'
            '<stop offset="1" stop-color="#9cc9e2"/></linearGradient>'
            '<radialGradient id="water"><stop offset="0" stop-color="#03101c"/><stop offset="1" stop-color="#0f3552"/></radialGradient>'
            '<radialGradient id="ball" cx="0.35" cy="0.35" r="0.7"><stop offset="0" stop-color="#fff1d6"/>'
            f'<stop offset="0.35" stop-color="{AMBER}"/><stop offset="1" stop-color="#9a4a00"/></radialGradient>')
    return card("~/frozen-lake-rl", "Frozen Lake RL", "value iteration, then a real slippery episode",
                "Python", "#3572A5", "\n".join(parts), css,
                "An isometric frozen lake: state values converge sweep by sweep, policy arrows appear, and an agent hops to the goal, slipping on the way.",
                defs)


# ---------------------------------------------------------------------------------------------
# FTP over a hand-written TCP/IP stack
# ---------------------------------------------------------------------------------------------
def card_ftp():
    T = 10.0
    tl = Timeline(T, "t")
    CX, SX = 64, 356
    msgs = [(">", "SYN", "49152 > 21 [SYN] seq=0 win=64240 mss=1460"),
            ("<", "SYN, ACK", "21 > 49152 [SYN, ACK] seq=0 ack=1 win=65160"),
            (">", "ACK", "49152 > 21 [ACK] seq=1 ack=1 win=64240"),
            (">", "USER miaad / PASS ****", "49152 > 21 [PSH, ACK] len=11  USER miaad"),
            ("<", "230 Login successful", "21 > 49152 [PSH, ACK] len=23  230 Login successful"),
            (">", "RETR notes.txt", "49152 > 21 [PSH, ACK] len=16  RETR notes.txt"),
            ("<", "150 data", "20 > 49153 [PSH, ACK] len=1460  (file data)")]
    laptop = (f'<g transform="translate({CX - 14} 44)"><rect x="3" y="0" width="22" height="14" rx="1.5" fill="#1a2332" stroke="{BLUE}"/>'
              f'<rect x="5" y="2" width="18" height="10" fill="#0e2238"/><path d="M0 16h28l-3 3H3Z" fill="{BLUE}"/></g>')
    server = [f'<g transform="translate({SX - 11} 42)">']
    for i in range(3):
        blink = tl.kf([(0, "opacity:1"), (0.3 + i * 0.4, "opacity:1"), (0.35 + i * 0.4, "opacity:0.2"), (0.5 + i * 0.4, "opacity:1"),
                       (T, "opacity:1")])
        server.append(f'<rect x="0" y="{i * 7}" width="22" height="6" rx="1" fill="#1a2332" stroke="{CORAL}" stroke-width="0.8"/>'
                      f'<circle cx="4" cy="{i * 7 + 3}" r="1.2" fill="{GREEN}" class="{blink}"/>'
                      f'<path d="M9 {i * 7 + 3}h10" stroke="{FAINT}" stroke-width="1"/>')
    server.append("</g>")
    parts = [laptop, "".join(server),
             f'<path d="M{CX} 66V168M{SX} 66V168" stroke="{FAINT}" stroke-dasharray="2 3"/>']
    y0, gap = 78, 13.5
    step = 0.95
    for i, (d, label, wire) in enumerate(msgs):
        y = y0 + i * gap
        on = 0.5 + i * step
        x1, x2 = (CX + 3, SX - 3) if d == ">" else (SX - 3, CX + 3)
        col = BLUE if d == ">" else CORAL
        line = tl.kf([(0, "stroke-dashoffset:1"), (on, "stroke-dashoffset:1"), (on + 0.5, "stroke-dashoffset:0"),
                      (T - 0.5, "stroke-dashoffset:0"), (T - 0.3, "stroke-dashoffset:1"), (T, "stroke-dashoffset:1")])
        parts.append(f'<path d="M{x1} {y}H{x2}" pathLength="1" stroke="{col}" stroke-width="1.2" stroke-opacity="0.8" '
                     f'class="{line}" style="stroke-dasharray:1"/>')
        sg = 1 if d == ">" else -1
        parts.append(f'<path d="M{x2 - 5 * sg} {y - 3}L{x2} {y}L{x2 - 5 * sg} {y + 3}" fill="none" stroke="{col}" '
                     f'stroke-width="1.2" class="{tl.show(on + 0.5, fade=0.05)}"/>')
        parts.append(f'<g class="{tl.show(on + 0.25, fade=0.2)}">{mono((CX + SX) / 2, y - 3, label, 8.5, FG, anchor="middle")}</g>')
        pk = tl.kf([(0, "transform:translateX(0);opacity:0"), (on - 0.01, "transform:translateX(0);opacity:0"),
                    (on, "transform:translateX(0);opacity:1"),
                    (on + 0.5, f"transform:translateX({x2 - x1}px);opacity:1"),
                    (on + 0.55, f"transform:translateX({x2 - x1}px);opacity:0"), (T, "opacity:0")], timing="ease-in")
        parts.append(f'<rect x="{x1 - 6}" y="{y - 3}" width="12" height="6" rx="2" fill="{col}" filter="url(#pg)" '
                     f'class="{pk}" style="opacity:0"/>')
        off = on + step if i < len(msgs) - 1 else T - 0.4
        wc = tl.pulse(on, off) if i < len(msgs) - 1 else tl.show(on, off, fade=0.05)
        parts.append(f'<g class="{wc}"{"" if i == len(msgs) - 1 else HIDE}>{mono(CX - 22, 184, wire, 9, GREEN if i < 3 else MUTED)}</g>')
    parts.append(f'<rect x="{CX - 30}" y="173" width="{SX - CX + 60}" height="16" rx="3" fill="none" stroke="{BORDER}"/>')
    parts.append(mono(CX + 20, 58, "client", 9, BLUE))
    parts.append(mono(SX - 17, 58, "server", 9, CORAL, anchor="end"))
    return card("~/ftp-tcpip-stack", "FTP on a custom TCP/IP stack", "secure FTP over a TCP/IP stack written from scratch",
                "Python", "#3572A5", "\n".join(parts), tl.css(),
                "Packets fly between a laptop and a server: TCP handshake, FTP login and a file transfer, with each packet's header shown below.",
                glow("pg", 1.5))


# ---------------------------------------------------------------------------------------------
# LLM home agent: a dark room lights up after a tool call
# ---------------------------------------------------------------------------------------------
def card_llm_home():
    T = 10.0
    tl = Timeline(T, "l")
    parts = []
    msg = "lights on in the living room?"
    fs = 9.5
    w = len(msg) * fs * CHAR + 16
    parts.append(f'<g class="{tl.show(0.5, fade=0.3)}"><rect x="{206 - w:.1f}" y="48" width="{w:.1f}" height="20" rx="10" fill="#1f6feb"/>'
                 f'{mono(214 - w, 61.5, msg, fs, "#ffffff")}</g>')
    for i in range(3):
        d = tl.kf([(0, "opacity:0"), (1.2, "opacity:0"), (1.3 + i * 0.12, "opacity:1"), (1.6 + i * 0.12, "opacity:0.3"),
                   (1.9 + i * 0.12, "opacity:1"), (2.2, "opacity:0.3"), (2.3, "opacity:0"), (T, "opacity:0")])
        parts.append(f'<circle cx="{26 + i * 8}" cy="84" r="2.6" fill="{MUTED}" class="{d}" style="opacity:0"/>')
    call = 'light.turn_on("living_room")'
    cw_ = len(call) * 9 * CHAR + 16
    parts.append(f'<g class="{tl.show(2.4, fade=0.25)}"><rect x="16" y="76" width="{cw_:.1f}" height="19" rx="4" fill="#111a26" '
                 f'stroke="{BORDER}"/>{mono(24, 89, call, 9, GREEN)}</g>')
    parts.append(f'<g class="{tl.show(3.1, fade=0.25)}">{mono(24, 110, "{ state: on, brightness: 80 }", 9, MUTED)}</g>')
    reply = "Living room lamp is on."
    rw = len(reply) * fs * CHAR + 16
    parts.append(f'<g class="{tl.show(3.8, fade=0.3)}"><rect x="16" y="122" width="{rw:.1f}" height="20" rx="10" fill="#262f3d"/>'
                 f'{mono(24, 135.5, reply, fs, FG)}</g>')
    # the room
    RX, RY, RW, RH = 226, 46, 178, 142
    room = [f'<defs><clipPath id="room"><rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" rx="8"/></clipPath></defs>',
            f'<g clip-path="url(#room)">',
            f'<rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" fill="#4a3f52"/>',
            f'<rect x="{RX}" y="{RY + 104}" width="{RW}" height="{RH - 104}" fill="#6b4f3a"/>',
            f'<path d="M{RX} {RY + 104}H{RX + RW}" stroke="#3a2c22" stroke-width="2"/>',
            # window with night sky
            f'<rect x="{RX + 96}" y="{RY + 14}" width="62" height="50" rx="2" fill="url(#night)" stroke="#2c2433" stroke-width="3"/>',
            f'<path d="M{RX + 127} {RY + 14}V{RY + 64}M{RX + 96} {RY + 39}H{RX + 158}" stroke="#2c2433" stroke-width="2"/>',
            f'<circle cx="{RX + 145}" cy="{RY + 27}" r="6" fill="#f3efe0"/><circle cx="{RX + 148}" cy="{RY + 25}" r="5.5" fill="#1b2140"/>']
    r = rng_(9)
    for _ in range(9):
        sx, sy = RX + 99 + r.uniform(0, 56), RY + 17 + r.uniform(0, 44)
        tw = tl.kf([(0, "opacity:1"), (r.uniform(0.5, 9), "opacity:0.2"), (T, "opacity:1")])
        room.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="0.7" fill="#fff" class="{tw}"/>')
    room += [
        # rug, sofa, plant, lamp
        f'<ellipse cx="{RX + 70}" cy="{RY + 126}" rx="56" ry="9" fill="#8a3b4a"/>',
        f'<rect x="{RX + 20}" y="{RY + 74}" width="92" height="30" rx="7" fill="#2f5d6e"/>',
        f'<rect x="{RX + 14}" y="{RY + 84}" width="14" height="26" rx="5" fill="#29525f"/><rect x="{RX + 104}" y="{RY + 84}" width="14" height="26" rx="5" fill="#29525f"/>',
        f'<rect x="{RX + 26}" y="{RY + 92}" width="80" height="16" rx="4" fill="#3a7084"/>',
        f'<path d="M{RX + 66} {RY + 92}V{RY + 108}" stroke="#2a5664" stroke-width="1.2"/>',
        f'<rect x="{RX + 40}" y="{RY + 80}" width="18" height="12" rx="3" fill="#e0b25a" transform="rotate(-8 {RX + 49} {RY + 86})"/>',
        f'<path d="M{RX + 150} {RY + 116}h14l-2 14h-10Z" fill="#9a5b3a"/>',
        f'<path d="M{RX + 157} {RY + 116}C{RX + 150} {RY + 100} {RX + 142} {RY + 96} {RX + 138} {RY + 88}M{RX + 157} {RY + 116}C{RX + 158} {RY + 98} {RX + 166} {RY + 92} {RX + 170} {RY + 84}M{RX + 157} {RY + 116}C{RX + 156} {RY + 104} {RX + 152} {RY + 94} {RX + 156} {RY + 82}" '
        f'stroke="#3f8a4a" stroke-width="5" stroke-linecap="round" fill="none"/>',
        f'<path d="M{RX + 134} {RY + 132}V{RY + 52}" stroke="#1d1a22" stroke-width="2.4"/>'
        f'<ellipse cx="{RX + 134}" cy="{RY + 132}" rx="9" ry="2.5" fill="#1d1a22"/>',
        f'<path d="M{RX + 123} {RY + 52}h22l-4 -16h-14Z" fill="#e9d8b4"/>',
    ]
    on = 2.9
    dark = tl.kf([(0, "opacity:0.78"), (on, "opacity:0.78"), (on + 0.6, "opacity:0"), (T - 0.5, "opacity:0"),
                  (T - 0.2, "opacity:0.78"), (T, "opacity:0.78")], timing="ease-out")
    light = tl.kf([(0, "opacity:0"), (on, "opacity:0"), (on + 0.5, "opacity:1"), (T - 0.5, "opacity:1"),
                   (T - 0.2, "opacity:0"), (T, "opacity:0")], timing="ease-out")
    room.append(f'<rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" fill="#070b1a" class="{dark}" style="opacity:0"/>')
    room.append(f'<g class="{light}"><path d="M{RX + 123} {RY + 52}L{RX + 96} {RY + 140}H{RX + 172}L{RX + 145} {RY + 52}Z" fill="url(#cone)"/>'
                f'<circle cx="{RX + 134}" cy="{RY + 48}" r="44" fill="url(#halo)"/>'
                f'<path d="M{RX + 123} {RY + 52}h22l-4 -16h-14Z" fill="#fff4d6"/></g>')
    room.append("</g>")
    room.append(f'<rect x="{RX + 0.5}" y="{RY + 0.5}" width="{RW - 1}" height="{RH - 1}" rx="8" fill="none" stroke="{BORDER}"/>')
    parts += room
    defs = ('<linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d1330"/>'
            '<stop offset="1" stop-color="#2a2a5a"/></linearGradient>'
            '<linearGradient id="cone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd98a" stop-opacity="0.55"/>'
            '<stop offset="1" stop-color="#ffd98a" stop-opacity="0"/></linearGradient>'
            '<radialGradient id="halo"><stop offset="0" stop-color="#ffe7a8" stop-opacity="0.55"/>'
            '<stop offset="1" stop-color="#ffe7a8" stop-opacity="0"/></radialGradient>')
    return card("~/llm-home-assist-agent", "LLM home agent", "an LLM agent that runs a smart home, in TypeScript",
                "TypeScript", "#3178c6", "\n".join(parts), tl.css(),
                "A chat asks for the living room lights; the agent calls a tool and a dark room lights up.", defs)


# ---------------------------------------------------------------------------------------------
# ASCII animation: a high-resolution shaded donut with a frame timeline
# ---------------------------------------------------------------------------------------------
def card_ascii():
    n = 30
    tl = Timeline(n / 12, "a")
    cols, rows, fs, lh = 62, 31, 6.2, 4.75
    cw = fs * CHAR
    x0, y0 = 18, 50
    out = ['<g fill="url(#dg)" filter="url(#bloom)">']
    for i in range(n):
        frame = donut_frame(math.pi * i / n + 1.0, math.pi * i / n + 0.8, cols, rows, cw / lh)
        cls = tl.pulse(i * tl.T / n, (i + 1) * tl.T / n)
        out.append(f'<g class="{cls}"{HIDE if i else ""}>')
        for r, row in enumerate(frame):
            s = row.rstrip()
            if s.strip():
                lead = len(s) - len(s.lstrip())
                out.append(mono(x0 + lead * cw, y0 + r * lh, s.lstrip(), fs, fill="inherit"))
        out.append("</g>")
    out.append("</g>")
    rx = 262
    out.append(mono(rx, 70, "donut.anim", 11, FG, weight="700"))
    for i in range(n):
        cls = tl.pulse(i * tl.T / n, (i + 1) * tl.T / n)
        out.append(f'<g class="{cls}"{HIDE if i else ""}>{mono(rx, 90, f"frame {i + 1:02d} / {n}", 10, AMBER)}</g>')
    # timeline strip: one tick per frame and a playhead
    sw = 128
    for i in range(n):
        out.append(f'<rect x="{rx + i * sw / n:.1f}" y="104" width="{sw / n - 1:.1f}" height="12" rx="1" fill="#1a2230"/>')
    head = tl.kf([(0, "transform:translateX(0)"), (tl.T, f"transform:translateX({sw}px)")], timing=f"steps({n},end)")
    out.append(f'<rect x="{rx}" y="102" width="{sw / n - 1:.1f}" height="16" rx="1" fill="{AMBER}" class="{head}"/>')
    out.append(mono(rx, 136, "12 fps  loop", 10, MUTED))
    defs = grad("dg", x0, x0 + cols * cw, (AMBER, CORAL, VIOLET), y1=y0, y2=y0 + rows * lh) + glow("bloom", 1.1)
    return card("~/ascii-animation", "ASCII Animation Generator", "an object-oriented C++ engine for console animation",
                "C++", "#f34b7d", "\n".join(out), tl.css(),
                "A high-resolution ASCII donut spins while a frame counter and playhead advance.", defs)


# ---------------------------------------------------------------------------------------------
# OpenGL ping pong on a CRT
# ---------------------------------------------------------------------------------------------
def card_pong():
    T = 8.0
    tl = Timeline(T, "o")
    AX, AY, AW, AH = 18, 46, 384, 140
    PL, PR = AX + 16, AX + AW - 16
    top, bot = AY + 8, AY + AH - 8
    hits = [74, 150, 98, 166, 64, 128]
    n = len(hits)
    seg = T / n
    pts = []
    hit_events = []
    for i in range(n):
        x1 = PL + 7 if i % 2 == 0 else PR - 7
        x2 = PR - 7 if i % 2 == 0 else PL + 7
        y1, y2 = hits[i], hits[(i + 1) % n]
        t1 = i * seg
        pts.append((t1, x1, y1))
        hit_events.append((t1, x1, y1, 1 if i % 2 == 0 else -1))
        wall = top if (i % 3 == 0) else bot
        d1, d2 = abs(y1 - wall), abs(y2 - wall)
        bx = x1 + (x2 - x1) * d1 / (d1 + d2)
        pts.append((t1 + seg * d1 / (d1 + d2), bx, wall))
    pts.append((T, pts[0][1], pts[0][2]))
    ball = tl.kf([(t, f"transform:translate({x:.1f}px,{y:.1f}px)") for t, x, y in pts])
    parts = [f'<rect x="{AX}" y="{AY}" width="{AW}" height="{AH}" rx="14" fill="url(#crt)"/>',
             f'<path d="M{AX + AW / 2} {AY + 8}V{AY + AH - 8}" stroke="#5ef2ff" stroke-opacity="0.35" stroke-dasharray="5 6" stroke-width="2"/>']
    for k, lag in enumerate([0.16, 0.13, 0.1, 0.07, 0.045, 0.02]):
        parts.append(f'<g class="{ball}" style="animation-delay:{lag - T:.3f}s" opacity="{0.08 + k * 0.07:.2f}">'
                     f'<circle r="{3 + k * 0.4:.1f}" fill="#5ef2ff"/></g>')
    parts.append(f'<g class="{ball}" filter="url(#glow)"><circle r="5.5" fill="#ffffff"/></g>')
    # sparks at every paddle hit
    r = rng_(5)
    for t, x, y, sgn in hit_events:
        for j in range(7):
            ang = r.uniform(-70, 70)
            dist = r.uniform(10, 24)
            dx, dy = sgn * dist * math.cos(math.radians(ang)), dist * math.sin(math.radians(ang))
            sp = tl.kf([(0, "transform:translate(0px,0px);opacity:0"), (max(0, t - 0.001), "transform:translate(0px,0px);opacity:0"),
                        (t, "transform:translate(0px,0px);opacity:1"),
                        (t + 0.45, f"transform:translate({dx:.1f}px,{dy:.1f}px);opacity:0"), (T, f"transform:translate({dx:.1f}px,{dy:.1f}px);opacity:0")],
                       timing="ease-out")
            col = "#5ef2ff" if sgn > 0 else "#ff5ec8"
            parts.append(f'<g transform="translate({x} {y})"><circle r="1.3" fill="{col}" class="{sp}" style="opacity:0"/></g>')
    for side, px, col in [(0, PL, "#5ef2ff"), (1, PR, "#ff5ec8")]:
        pst = [(i * seg, hits[i]) for i in range(n) if i % 2 == side]
        pst = [(t - T, y) for t, y in pst] + pst + [(t + T, y) for t, y in pst]

        def at(t):
            for (ta, ya), (tb, yb) in zip(pst, pst[1:]):
                if ta <= t <= tb:
                    return ya + (yb - ya) * (t - ta) / (tb - ta)
            return pst[0][1]
        kf = [(t, f"transform:translateY({y - 17:.1f}px)") for t, y in pst if 0 <= t <= T]
        if kf[0][0] > 0:
            kf.insert(0, (0, f"transform:translateY({at(0) - 17:.1f}px)"))
        if kf[-1][0] < T:
            kf.append((T, f"transform:translateY({at(T) - 17:.1f}px)"))
        cls = tl.kf(kf, timing="ease-in-out")
        parts.append(f'<g class="{cls}"><rect x="{px - 3}" y="0" width="6" height="34" rx="3" fill="{col}" filter="url(#glow)"/></g>')
    parts.append(f'<rect x="{AX}" y="{AY}" width="{AW}" height="{AH}" rx="14" fill="url(#scan)"/>')
    parts.append(f'<rect x="{AX}" y="{AY}" width="{AW}" height="{AH}" rx="14" fill="url(#vig)"/>')
    parts.append(f'<rect x="{AX + 0.5}" y="{AY + 0.5}" width="{AW - 1}" height="{AH - 1}" rx="14" fill="none" stroke="#1d2a33" stroke-width="2"/>')
    parts.append(f'<path d="M{AX + 20} {AY + 10}Q{AX + AW / 2} {AY + 2} {AX + AW - 20} {AY + 10}" stroke="#ffffff" stroke-opacity="0.06" stroke-width="6" fill="none"/>')
    defs = (glow("glow", 2.6) +
            '<radialGradient id="crt" cx="0.5" cy="0.5" r="0.7"><stop offset="0" stop-color="#0c1a22"/><stop offset="1" stop-color="#03070a"/></radialGradient>'
            '<radialGradient id="vig" cx="0.5" cy="0.5" r="0.72"><stop offset="0.65" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#000" stop-opacity="0.75"/></radialGradient>'
            '<pattern id="scan" width="4" height="3" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#ffffff" opacity="0.04"/></pattern>')
    return card("~/opengl-pingpong", "OpenGL Ping Pong", "pong with shaders, in C++ with FreeGLUT and GLEW",
                "C++", "#f34b7d", "\n".join(parts), tl.css(),
                "A neon pong rally on a curved CRT, with ball trails and sparks on every hit.", defs)


CARDS = [("dcgan", card_dcgan), ("pix2pix", card_pix2pix), ("unet", card_unet), ("frozen-lake", card_frozen_lake),
         ("ftp-tcpip", card_ftp), ("llm-home", card_llm_home), ("ascii", card_ascii), ("pong", card_pong)]
