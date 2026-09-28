"""Shared palette and helpers for the profile's hand-built SVGs.

Everything is plain SVG + CSS keyframes so GitHub renders it inside a README <img>.
"""

BG = "#0b0f14"
PANEL = "#141a23"
BAR = "#121822"
BORDER = "#2a3140"
FG = "#e6edf3"
MUTED = "#8b949e"
FAINT = "#3d4550"
GREEN = "#7ee787"
AMBER = "#ffa657"
CORAL = "#ff7b72"
VIOLET = "#d2a8ff"
BLUE = "#79c0ff"
YELLOW = "#e3b341"

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono','DejaVu Sans Mono',monospace"
CHAR = 0.6  # monospace advance as a fraction of font size


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def mono(x, y, s, size, fill=FG, cls="", anchor=None, weight=None, fit=True, extra=""):
    """Monospace text pinned to an exact width so layouts don't drift between fonts."""
    attrs = [f'x="{x:.1f}"', f'y="{y:.1f}"', f'font-size="{size}"', f'fill="{fill}"']
    if cls:
        attrs.append(f'class="{cls}"')
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    if weight:
        attrs.append(f'font-weight="{weight}"')
    if fit and s:
        attrs.append(f'textLength="{len(s) * size * CHAR:.1f}" lengthAdjust="spacingAndGlyphs"')
    if extra:
        attrs.append(extra)
    return f'<text {" ".join(attrs)}>{esc(s)}</text>'


class Timeline:
    """Builds looping keyframe classes from (seconds, css) stops on a shared period."""

    def __init__(self, period, prefix="k"):
        self.T = period
        self.prefix = prefix
        self.rules = []
        self.n = 0

    def pct(self, t):
        return max(0.0, min(100.0, t / self.T * 100))

    def kf(self, stops, timing="linear"):
        name = f"{self.prefix}{self.n}"
        self.n += 1
        body = "".join(f"{self.pct(t):.3f}%{{{css}}}" for t, css in stops)
        self.rules.append(f"@keyframes {name}{{{body}}}.{name}{{animation:{name} {self.T:.3f}s {timing} infinite}}")
        return name

    def show(self, on, off=None, fade=0.2, base=1):
        """Hidden, fades in at `on`, fades out at `off` (default: just before the loop restarts)."""
        off = self.T - 0.35 if off is None else off
        return self.kf([(0, "opacity:0"), (on, "opacity:0"), (on + fade, f"opacity:{base}"),
                        (off, f"opacity:{base}"), (off + fade, "opacity:0"), (self.T, "opacity:0")])

    def pulse(self, on, off, fade=0.05):
        """Visible only between on and off with near-instant edges (for frame flipping)."""
        return self.kf([(0, "opacity:0"), (on, "opacity:0"), (on + 0.001, "opacity:1"),
                        (off, "opacity:1"), (off + 0.001, "opacity:0"), (self.T, "opacity:0")])

    def css(self):
        return "".join(self.rules)


def window(w, h, title, body, css="", label="", defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">
<style>text{{font-family:{MONO};white-space:pre}}{css}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
<defs><clipPath id="win"><rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="12"/></clipPath>{defs}</defs>
<g clip-path="url(#win)">
<rect width="{w}" height="{h}" fill="{BG}"/>
<rect width="{w}" height="34" fill="{BAR}"/>
<path d="M0 34.5H{w}" stroke="{BORDER}"/>
<circle cx="20" cy="17" r="5.5" fill="#ff5f57"/><circle cx="38" cy="17" r="5.5" fill="#febc2e"/><circle cx="56" cy="17" r="5.5" fill="#28c840"/>
{mono(w / 2, 21, title, 12, MUTED, anchor="middle")}
{body}
</g>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="12" fill="none" stroke="{BORDER}"/>
</svg>
'''


CARD_W, CARD_H = 420, 250


def card(path, name, desc, lang, lang_color, body, css="", label="", defs=""):
    """Project card: animated visual in y 44..190, name + language + one-line description below."""
    foot = [
        mono(18, 216, name, 14, FG, weight="700"),
        f'<circle cx="{CARD_W - 18 - len(lang) * 11 * CHAR - 9:.1f}" cy="212" r="4.5" fill="{lang_color}"/>',
        mono(CARD_W - 18, 216, lang, 11, MUTED, anchor="end"),
        mono(18, 236, desc, 12, MUTED),
    ]
    return window(CARD_W, CARD_H, path, body + "\n" + "\n".join(foot), css, label or f"{name}: {desc}", defs)


HIDE = ' style="opacity:0"'


def grad(id_, x1, x2, stops=(AMBER, CORAL, VIOLET), y1=0, y2=0):
    s = "".join(f'<stop offset="{i / (len(stops) - 1):.2f}" stop-color="{c}"/>' for i, c in enumerate(stops))
    return (f'<linearGradient id="{id_}" gradientUnits="userSpaceOnUse" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
            f'{s}</linearGradient>')


def glow(id_, std=2.5):
    return (f'<filter id="{id_}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{std}" result="b"/>'
            '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')


def save(rel, svg):
    import os
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(svg)
    print(f"{rel:32s} {len(svg) / 1024:6.1f} KB")
