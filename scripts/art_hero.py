"""Hero banner: the name sampled out of Gaussian noise with a real cosine noise schedule.

The glyphs come from a rasterised bold font, shaded with a directional light so the letters read as
embossed, then quantised onto a fine ASCII ramp. Needs numpy + Pillow (only when rendering the art).
"""
import math
import os

from svgkit import BORDER, CHAR, FG, GREEN, HIDE, MUTED, Timeline, glow, grad, mono, window

RAMP = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
FONTS = [
    os.environ.get("HERO_FONT", ""),  # set this to any bold .ttf to override
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # what the committed hero was rendered with
    "/Library/Fonts/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "DejaVuSans-Bold.ttf",  # bare name: Pillow also searches the system font folders
]


def load_font(size):
    from PIL import ImageFont

    for path in filter(None, FONTS):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    raise SystemExit("no bold TrueType font found for the hero; set HERO_FONT=/path/to/font.ttf")


def name_field(cols, rows, cw, lh, word="MIAAD"):
    import numpy as np
    from PIL import Image, ImageDraw

    sx = 10  # supersampling per character column
    W, Hh = cols * sx, int(rows * sx * lh / cw)
    img = Image.new("L", (W, Hh), 0)
    d = ImageDraw.Draw(img)
    size = int(Hh * 1.02)
    while True:
        f = load_font(size)
        l, t, r, b = d.textbbox((0, 0), word, font=f)
        if r - l <= W * 0.97 and b - t <= Hh * 0.86:
            break
        size -= 4
    d.text(((W - (r - l)) / 2 - l, (Hh - (b - t)) / 2 - t), word, font=f, fill=255)
    a = np.asarray(img, dtype=np.float64) / 255
    ys = Hh / rows
    cov = np.zeros((rows, cols))
    for j in range(rows):
        y0, y1 = int(j * ys), int((j + 1) * ys)
        cov[j] = a[y0:y1].reshape(y1 - y0, cols, sx).mean(axis=(0, 2))
    # emboss: light from the upper left on a softened height field
    blur = cov.copy()
    for _ in range(2):
        blur = (blur + np.roll(blur, 1, 0) + np.roll(blur, -1, 0) + np.roll(blur, 1, 1) + np.roll(blur, -1, 1)) / 5
    gy, gx = np.gradient(blur)
    nx, ny, nz = -gx * 3.0, -gy * 3.0 * (cw / lh), np.ones_like(gx)
    n = np.sqrt(nx ** 2 + ny ** 2 + nz ** 2)
    L = np.array([-0.55, -0.6, 0.58])
    L = L / np.linalg.norm(L)
    lit = np.clip((nx * L[0] + ny * L[1] + nz * L[2]) / n, 0, 1)
    return np.clip(cov * (0.58 + 0.62 * lit), 0, 1)


def to_rows(v):
    out = []
    for row in v:
        s = "".join(RAMP[min(int(x * len(RAMP)), len(RAMP) - 1)] for x in row)
        out.append(s)
    return out


def hero():
    import numpy as np

    W, H = 880, 356
    fs, lh = 6.4, 6.7
    cw = fs * CHAR
    cols, rows = 208, 29
    x0, y0 = (W - cols * cw) / 2, 58
    x_final = name_field(cols, rows, cw, lh)
    rng = np.random.default_rng(2004)

    def field():
        e = rng.standard_normal((rows, cols))
        e = (e + 0.5 * (np.roll(e, 1, 1) + np.roll(e, -1, 1)) + 0.3 * (np.roll(e, 1, 0) + np.roll(e, -1, 0))) / 2.0
        return e / e.std()

    K = 18
    step = 0.17
    T = 12.0
    tl = Timeline(T, "h")
    x0v = x_final * 2 - 1
    eps = field()
    parts = [f'<g fill="url(#hg)">']
    for k in range(K):
        s = k / (K - 1)
        abar = math.sin(s * math.pi / 2) ** 2  # signal fraction as t runs 1000 -> 0
        eps = 0.85 * eps + 0.53 * field()
        eps /= eps.std()
        xt = math.sqrt(abar) * x0v + math.sqrt(1 - abar) * eps * 0.9
        v = np.clip((xt + 1) / 2, 0, 1)
        if k == K - 1:
            v = x_final
        on = 0.3 + k * step
        off = on + step if k < K - 1 else T - 0.3
        if k == 0:
            cls = tl.kf([(0, "opacity:1"), (off, "opacity:1"), (off + 0.001, "opacity:0"),
                         (T - 0.3, "opacity:0"), (T - 0.299, "opacity:1"), (T, "opacity:1")])
        else:
            cls = tl.pulse(on, off)
        attrs = ' filter="url(#bloom)"' if k == K - 1 else ""
        parts.append(f'<g class="{cls}"{"" if k == K - 1 else HIDE}{attrs}>')
        for r, line in enumerate(to_rows(v)):
            t = line.rstrip()
            if t.strip():
                lead = len(t) - len(t.lstrip())
                parts.append(mono(x0 + lead * cw, y0 + r * lh, t.lstrip(), fs, fill="inherit"))
        parts.append("</g>")
    parts.append("</g>")

    # tqdm-style progress, timed to the animation itself
    by = y0 + rows * lh + 22
    parts.append(f'<path d="M{x0:.1f} {by - 14}H{W - x0:.1f}" stroke="{BORDER}"/>')
    total_time = (K - 1) * step
    for k in range(K):
        s = k / (K - 1)
        done = round(1000 * s)
        el = s * total_time
        rate = 1000 / total_time
        rem = (1000 - done) / rate
        blocks = s * 24
        bar = "█" * int(blocks) + (" ▏▎▍▌▋▊▉"[int((blocks % 1) * 8)] if blocks < 24 else "")
        bar = bar.ljust(24)
        line = f"sampling {int(s * 100):3d}%|{bar}| {done:4d}/1000 [00:{int(el):02d}<00:{int(math.ceil(rem)):02d}, {rate:.2f}it/s]"
        on = 0.3 + k * step
        off = on + step if k < K - 1 else T - 0.3
        cls = tl.pulse(on, off) if k else tl.kf([(0, "opacity:1"), (off, "opacity:1"), (off + 0.001, "opacity:0"),
                                                 (T - 0.3, "opacity:0"), (T - 0.299, "opacity:1"), (T, "opacity:1")])
        parts.append(f'<g class="{cls}"{"" if k == K - 1 else HIDE}>{mono(x0, by + 4, line, 11, MUTED)}</g>')

    ty = by + 36
    parts.append(f'<g class="{tl.show(0.3 + K * step, fade=0.5)}">'
                 f'{mono(x0, ty, "Miaad Kimiagari", 16, FG, weight="700")}'
                 f'{mono(x0 + 17 * 16 * CHAR, ty, "Computer Engineering, University of Isfahan", 13, MUTED)}</g>')
    defs = grad("hg", x0, W - x0) + glow("bloom", 1.4)
    label = ("MIAAD rendered in ASCII, sampled out of noise over a thousand diffusion steps. "
             "Miaad Kimiagari, Computer Engineering, University of Isfahan.")
    return window(W, H, "~/miaad  -  python sample.py", "\n".join(parts), tl.css(), label, defs)
