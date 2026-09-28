"""Refresh the live parts of the profile: assets/neofetch.svg and the latest Medium posts in README.md.

Run daily by .github/workflows/refresh-profile.yml with the workflow's GITHUB_TOKEN.

    python3 scripts/update_stats.py                   # live, needs GITHUB_TOKEN
    python3 scripts/update_stats.py --fixture f.json  # render from saved data, no network
"""
import datetime as dt
import email.utils
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

from make_art import HIDE, grad, life_frames
from svgkit import AMBER, BLUE, CHAR, CORAL, FAINT, FG, GREEN, MUTED, VIOLET, YELLOW, Timeline, esc, mono, window

LOGIN = "Miaad2004"
MEDIUM_FEED = "https://medium.com/feed/@mia.kimiagari"
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
README = os.path.join(HERE, "..", "README.md")

QUERY = """
query($login: String!, $after: String) {
  user(login: $login) {
    createdAt
    followers { totalCount }
    repositories(first: 100, after: $after, ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false,
                 orderBy: {field: PUSHED_AT, direction: DESC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        name
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } }
      }
    }
  }
}
"""

# notebooks here are Python work; count them as Python instead of letting their outputs dominate
ALIAS = {"Jupyter Notebook": "Python"}
COLORS = {"Python": "#3572A5"}


def fetch_github(token):
    def page(after):
        req = urllib.request.Request(
            "https://api.github.com/graphql",
            data=json.dumps({"query": QUERY, "variables": {"login": LOGIN, "after": after}}).encode(),
            headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": LOGIN},
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            payload = json.load(r)
        if "errors" in payload:
            raise SystemExit(f"GraphQL error: {payload['errors']}")
        return payload["data"]["user"]

    u = page(None)
    nodes, info = list(u["repositories"]["nodes"]), u["repositories"]["pageInfo"]
    while info["hasNextPage"]:
        conn = page(info["endCursor"])["repositories"]
        nodes += conn["nodes"]
        info = conn["pageInfo"]
    repos = [r for r in nodes if r["name"] != LOGIN]
    return {
        "created_at": u["createdAt"],
        "followers": u["followers"]["totalCount"],
        "repos": [{"name": r["name"], "stars": r["stargazerCount"],
                   "languages": [{"name": e["node"]["name"], "color": e["node"]["color"], "size": e["size"]}
                                 for e in r["languages"]["edges"]]} for r in repos],
    }


def summarize(data, today):
    created = dt.datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")).date()
    months = (today.year - created.year) * 12 + today.month - created.month - (today.day < created.day)
    years, months = divmod(months, 12)
    uptime = f"{years} years, {months} months" if months else f"{years} years"
    share, colors = {}, dict(COLORS)
    for repo in data["repos"]:
        total = sum(l["size"] for l in repo["languages"])
        if not total:
            continue
        for l in repo["languages"]:
            name = ALIAS.get(l["name"], l["name"])
            share[name] = share.get(name, 0) + l["size"] / total
            colors.setdefault(name, l["color"] or MUTED)
    total = sum(share.values()) or 1
    langs = sorted(((n, v / total, colors[n]) for n, v in share.items()), key=lambda x: -x[1])
    top = max(data["repos"], key=lambda r: r["stars"])
    return {
        "uptime": uptime,
        "since": created.strftime("%b %Y"),
        "repos": len(data["repos"]),
        "stars": sum(r["stars"] for r in data["repos"]),
        "followers": data["followers"],
        "top": f"{top['name']} ({top['stars']} stars)",
        "latest": data["repos"][0]["name"],
        "langs": langs,
    }


def neofetch_svg(s):
    W, H = 880, 420
    tl = Timeline(18.0, "n")
    parts = [mono(28, 62, "$ ", 14, GREEN), mono(28 + 2 * 14 * CHAR, 62, "neofetch", 14, FG)]

    # logo: Game of Life seeded with the name
    cols, rows, fs, lh = 42, 29, 10, 10.2
    lx, ly = 30, 92
    gens, fps, hold = 72, 9, 1.4
    life = Timeline(0.3 + hold + (gens - 1) / fps + 0.6, "g")
    frames, _ = life_frames("ng", lx, ly, cols, rows, fs, lh, gens, fps, hold, life)
    parts.append(frames)

    x, FS, kw = 312, 13, 11
    vx = x + kw * FS * CHAR
    y = 92
    parts.append(f'<g class="{tl.show(0.3, fade=0.1)}">{mono(x, y, f"{LOGIN}@github", FS, AMBER, weight="700")}</g>')
    parts.append(f'<g class="{tl.show(0.38, fade=0.1)}">{mono(x, y + 17, "-" * (len(LOGIN) + 7), FS, MUTED)}</g>')
    y += 40
    at = 0.45

    def key(k, y, at):
        return mono(x, y, k + ":", FS, AMBER, weight="700")

    def row(k, v, y, at):
        parts.append(f'<g class="{tl.show(at, fade=0.1)}">{key(k, y, at)}{mono(vx, y, v[:44], FS, FG)}</g>')

    def count_row(k, n, suffix, y, at):
        """The number rolls up from 0 before settling."""
        parts.append(f'<g class="{tl.show(at, fade=0.1)}">{key(k, y, at)}</g>')
        steps = 12
        for i in range(steps + 1):
            v = round(n * (i / steps) ** 0.6)
            t0 = at + i * 0.07
            cls = tl.show(t0, fade=0.01) if i == steps else tl.pulse(t0, t0 + 0.07)
            rest = "" if i == steps else HIDE
            parts.append(f'<g class="{cls}"{rest}>{mono(vx, y, f"{v}{suffix}", FS, FG)}</g>')

    row("OS", "Computer Engineering @ University of Isfahan", y, at); y += 20; at += 0.08
    row("Host", f"github.com/{LOGIN}", y, at); y += 20; at += 0.08
    row("Uptime", f"{s['uptime']} (since {s['since']})", y, at); y += 20; at += 0.08
    count_row("Repos", s["repos"], " public", y, at); y += 20; at += 0.08
    count_row("Stars", s["stars"], "", y, at); y += 20; at += 0.08
    count_row("Followers", s["followers"], "", y, at); y += 20; at += 0.08
    row("Top repo", s["top"], y, at); y += 20; at += 0.08

    # latest push with a live pulse
    ring = Timeline(1.8, "r")
    rc = ring.kf([(0, "transform:scale(1);opacity:0.7"), (1.2, "transform:scale(2.6);opacity:0"),
                  (1.8, "transform:scale(2.6);opacity:0")], timing="ease-out")
    parts.append(f'<g class="{tl.show(at, fade=0.1)}">{key("Latest", y, at)}'
                 f'<g transform="translate({vx + 5} {y - 4.5})"><circle r="4" fill="{GREEN}"/>'
                 f'<circle r="4" fill="none" stroke="{GREEN}" class="{rc}" style="transform-box:fill-box;transform-origin:center"/></g>'
                 f'{mono(vx + 16, y, s["latest"][:42], FS, FG)}</g>')
    y += 20; at += 0.08

    # focus: cycles through what I work on, typed and erased like a live shell
    phrases = ["generative models", "reinforcement learning", "networking from scratch", "LLM agents", "games in a terminal"]
    cw = FS * CHAR
    per = [len(p_) * 0.06 * 2 + 1.8 for p_ in phrases]
    focus = Timeline(sum(per), "c")
    parts.append(f'<g class="{tl.show(at, fade=0.1)}">{key("Focus", y, at)}')
    t0 = 0.0
    for ph, span in zip(phrases, per):
        n, w = len(ph), len(ph) * cw
        typed, erase = t0 + n * 0.06, t0 + span - n * 0.06
        vis = focus.pulse(t0, t0 + span - 0.001)
        move = focus.kf([(0, "transform:translateX(0)"), (t0, "transform:translateX(0)"),
                         (typed, f"transform:translateX({w:.1f}px)"), (erase, f"transform:translateX({w:.1f}px)"),
                         (t0 + span, "transform:translateX(0)"), (focus.T, "transform:translateX(0)")],
                        timing=f"steps({n},end)")
        rest = "" if t0 == 0 else HIDE
        parts.append(f'<g class="{vis}"{rest}>{mono(vx, y, ph, FS, VIOLET)}'
                     f'<g class="{move}" style="transform:translateX({w:.1f}px)">'
                     f'<rect x="{vx - 1}" y="{y - FS}" width="{w + 4:.1f}" height="{FS + 5}" fill="#0b0f14"/>'
                     f'<rect x="{vx}" y="{y - FS + 1}" width="2" height="{FS + 2}" fill="{VIOLET}"/></g></g>')
        t0 += span
    parts.append("</g>")
    y += 20; at += 0.08

    # language bar: grows in, then a light sweeps across it
    parts.append(f'<g class="{tl.show(at, fade=0.1)}">{key("Langs", y, at)}</g>')
    bw = 846 - vx
    top = s["langs"][:6]
    rest = 1 - sum(p for _, p, _ in top)
    segs = top + ([("Other", rest, FAINT)] if rest > 0.005 else [])
    parts.append(f'<defs><clipPath id="bar"><rect x="{vx}" y="{y - 10}" width="{bw}" height="10" rx="3"/></clipPath>'
                 '<linearGradient id="gl" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
                 '<stop offset="0.5" stop-color="#fff" stop-opacity="0.45"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>'
                 '</linearGradient></defs>')
    grow = tl.kf([(0, "transform:scaleX(0)"), (at + 0.1, "transform:scaleX(0)"), (at + 1.1, "transform:scaleX(1)"),
                  (tl.T, "transform:scaleX(1)")], timing="ease-out")
    sweep = tl.kf([(0, "transform:translateX(-80px)"), (at + 1.4, "transform:translateX(-80px)"),
                   (at + 2.4, f"transform:translateX({bw + 80}px)"), (9.0, "transform:translateX(-80px)"),
                   (13.0, "transform:translateX(-80px)"), (14.0, f"transform:translateX({bw + 80}px)"),
                   (tl.T, f"transform:translateX({bw + 80}px)")], timing="ease-in-out")
    bar = [f'<g clip-path="url(#bar)"><g class="{grow}" style="transform-origin:{vx}px 0">']
    cx = vx
    for name, p, col in segs:
        bar.append(f'<rect x="{cx:.1f}" y="{y - 10}" width="{p * bw + 0.6:.1f}" height="10" fill="{col}"/>')
        cx += p * bw
    bar.append(f'</g><rect x="{vx}" y="{y - 10}" width="70" height="10" fill="url(#gl)" class="{sweep}" '
               f'style="transform:translateX({bw + 80}px)"/></g>')
    parts.append("".join(bar))
    y += 20
    for i, (name, p, col) in enumerate(segs[:6]):
        lx_, ly_ = vx + (i % 3) * 180, y + (i // 3) * 18
        parts.append(f'<g class="{tl.show(at + 1.0 + i * 0.08, fade=0.15)}"><circle cx="{lx_ + 4}" cy="{ly_ - 4}" r="4" fill="{col}"/>'
                     f'{mono(lx_ + 13, ly_, f"{name} {p * 100:.0f}%", 11, MUTED)}</g>')
    y += 34

    # the classic colour blocks, rippling
    wave = Timeline(2.4, "w")
    blocks = []
    for i, c in enumerate(["#1b1f24", CORAL, GREEN, YELLOW, BLUE, VIOLET, "#39c5cf", FG]):
        t0 = i * 0.12
        cls = wave.kf([(0, "transform:translateY(0)"), (t0, "transform:translateY(0)"),
                       (t0 + 0.25, "transform:translateY(-4px)"), (t0 + 0.5, "transform:translateY(0)"),
                       (2.4, "transform:translateY(0)")], timing="ease-in-out")
        blocks.append(f'<rect x="{vx + i * 26}" y="{y}" width="26" height="12" fill="{c}" class="{cls}"/>')
    parts.append(f'<g class="{tl.show(at + 1.6, fade=0.2)}">{"".join(blocks)}</g>')

    # a fresh prompt waiting for input
    py_ = H - 22
    parts.append(f'<g class="{tl.show(at + 2.0, fade=0.05)}">{mono(x, py_, "$", 14, GREEN)}'
                 f'<rect x="{x + 2 * 14 * CHAR:.1f}" y="{py_ - 13}" width="{14 * CHAR:.1f}" height="16" fill="{FG}" class="cur"/></g>')
    css = (tl.css() + life.css() + focus.css() + ring.css() + wave.css() +
           ".cur{animation:blink 1.06s steps(1) infinite}@keyframes blink{50%{opacity:0}}")
    label = (f"neofetch for {LOGIN}, next to Conway's Game of Life seeded with the name MIAAD: uptime {s['uptime']}, "
             f"{s['repos']} public repos, {s['stars']} stars, {s['followers']} followers; languages "
             + ", ".join(f"{n} {p * 100:.0f}%" for n, p, _ in top))
    return window(W, H, "~/miaad  -  neofetch", "\n".join(parts), css, label, grad("ng", lx, lx + cols * fs * CHAR))


def fetch_medium(limit=3):
    req = urllib.request.Request(MEDIUM_FEED, headers={"User-Agent": "Mozilla/5.0 (profile-readme-refresh)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        root = ET.fromstring(r.read())
    posts = []
    for item in list(root.iter("item"))[:limit]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").split("?")[0]
        date = email.utils.parsedate_to_datetime(item.findtext("pubDate")).strftime("%b %Y")
        if title and link:
            posts.append((title, link, date))
    return posts


def write_medium(posts):
    with open(README) as f:
        text = f.read()
    block = ""
    if posts:
        block = "\n### Latest writing\n\n" + "\n".join(f"- [{t.replace(']', ')')}]({l}) · {d}" for t, l, d in posts) + "\n"
    new = re.sub(r"(<!-- MEDIUM:START -->).*?(<!-- MEDIUM:END -->)", lambda m: m.group(1) + block + m.group(2),
                 text, flags=re.S)
    if new != text:
        with open(README, "w") as f:
            f.write(new)


def main():
    if "--fixture" in sys.argv:
        with open(sys.argv[sys.argv.index("--fixture") + 1]) as f:
            data = json.load(f)
        today = dt.date.fromisoformat(data.get("today", dt.date.today().isoformat()))
    else:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            raise SystemExit("GITHUB_TOKEN is not set")
        data = fetch_github(token)
        today = dt.date.today()
        try:
            write_medium(fetch_medium())
        except Exception as e:  # the feed being down should never block the stats refresh
            print(f"medium feed skipped: {e}")
    with open(os.path.join(ASSETS, "neofetch.svg"), "w") as f:
        f.write(neofetch_svg(summarize(data, today)))
    print("wrote assets/neofetch.svg")


if __name__ == "__main__":
    main()
