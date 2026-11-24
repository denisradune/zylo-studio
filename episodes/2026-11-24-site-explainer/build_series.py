"""Writes series.json + metadata.json for the Short "How zylo.video works" (owner's request 2026-11-24:
a full explanation of the site). Tips format: Jay asks, Bit walks through every part of zylo.video on the monitor.
Facts from the site itself (branch claude/keen-curie-0j1sci: site/index.html, episodes/2026-11-23-site-tour).
Ask zylo and the suggest form were not live yet (Vercel keys missing) -> shown honestly as "opening soon".
Run: python3 episodes/2026-11-24-site-explainer/build_series.py"""
import json, re
from pathlib import Path
D = Path(__file__).resolve().parent

def L(sp, say, set_, cast=(), **kw):
    shot = {"set": set_, "cast": list(cast)}
    shot.update(kw)
    return {"speaker": sp, "say": say, "shot": shot}
WIDE = {"type": "desk"}; CLOSE = {"type": "desk", "view": "close"}
def bit(expr="neutral", s=1.65): return {"id": "bit", "x": .5, "expr": expr, "scale": s, "lift": -int(1330 + 280 * s - 1480)}
def jay(expr="neutral", pose="sit"): return {"id": "hero", "x": .12, "pose": pose, "expr": expr, "scale": 1.45}
def face(expr="neutral", pose="idle"): return {"id": "hero", "x": .5, "pose": pose, "expr": expr, "scale": 3.4, "lift": -950}
def W(screen, expr="neutral", jexpr=None, **kw):
    cast = ([jay(jexpr)] if jexpr else []) + [bit(expr)]
    return dict(set_=WIDE, cast=cast, screen=screen, **kw)
POP = [{"type": "pop"}]; DING = [{"type": "ding"}]; TICK = [{"type": "tick"}]
ASK = "Write a birthday speech for my dad."
ASK2 = "Before you write, ask me 5 questions about him. One at a time."

lines = [
 L("hero", "Bit, where can I watch *every* zylo video? In one place?", CLOSE, [face("neutral", "think")], sfx=[{"type": "riser"}]),
 L("bit", "On our own website. *zylo dot video*.", **W({"kind": "title", "text": "ZYLO.VIDEO", "sub": "every video, one site"}, "happy", "neutral"), sfx=DING),
 L("bit", "Let me show you how it works. Step *one*: open it.", **W({"kind": "step", "n": 1, "text": "zylo.video"}, "smug"), sfx=POP),
 L("bit", "Up top: how many videos, the newest one, and total *views*.", **W({"kind": "stat", "label": "VIDEOS ON THE SITE", "value": 80, "suffix": "+", "sub": "updates itself"}, "neutral")),
 L("bit", "New video on YouTube? It appears here by *itself*. Usually in fifteen minutes.", **W({"kind": "list", "title": "AUTO-UPDATE", "items": ["New video on YouTube", "Site checks", "It's on zylo.video"]}, "happy"), sfx=[{"type": "ding"}, {"type": "ding", "at": .4}]),
 L("hero", "Eighty videos? How do I find *the one* I want?", CLOSE, [face("shocked", "shrug")]),
 L("bit", "Step two. Pick a *rubric*.", **W({"kind": "slots", "title": "RUBRICS", "items": [{"icon": "bolt", "label": "SCIENCE"}, {"icon": "star", "label": "MIND"}, {"icon": "money", "label": "MONEY"}, {"icon": "clock", "label": "HISTORY"}]}, "neutral")),
 L("bit", "Or search. Type *zombie*. Every zombie episode, in one second.", **W({"kind": "chat", "from": "hero", "text": "zombie"}, "smug"), sfx=TICK),
 L("bit", "Sort by newest, oldest, or *most viewed*.", **W({"kind": "videos", "title": "MOST VIEWED", "items": [{"views": "25"}, {"views": "19"}, {"views": "16"}]}, "happy"), sfx=POP),
 L("bit", "Step three. Tap a card. It plays *right there* on the page.", **W({"kind": "step", "n": 3}, "neutral"), sfx=POP),
 L("hero", "And if I'd rather watch on *YouTube*?", CLOSE, [face("neutral", "point")]),
 L("bit", "One button. It takes you *straight* there.", **W({"kind": "compare", "bad": "Search YouTube for it", "good": "One tap: Watch on YouTube"}, "happy", "neutral"), sfx=DING),
 L("bit", "Now the best part. Got an idea for a video? *Suggest* it.", **W({"kind": "chat", "from": "hero", "text": "What if cats could talk for one day?"}, "smug"), sfx=TICK),
 L("bit", "We read every idea. The best ones become *new videos*.", **W({"kind": "cards", "n": 7, "mark": "?", "pick": 3}, "happy"), sfx=[{"type": "whoosh"}]),
 L("bit", "And soon: Ask zylo. Any question. A short *answer*.", **W({"kind": "chat", "from": "hero", "text": "Why do we get goosebumps?", "reply": "Opening soon: short answers + a video link if we made one."}, "think")),
 L("hero", "Does it work on my *phone*?", CLOSE, [face("neutral", "phone")]),
 L("bit", "Yes. Big buttons. Dark at night, light in the *day*.", **W({"kind": "list", "title": "ON YOUR PHONE", "items": ["2 videos per row", "Big buttons", "Dark + light theme"]}, "happy"), sfx=[{"type": "ding"}]),
 L("hero", "So one site. Every video. And *my* ideas?", CLOSE, [face("happy", "cheer")], sfx=[{"type": "powerup"}]),
 L("bit", "Exactly. zylo dot video. Link in the *description*.", **W({"kind": "title", "text": "ZYLO.VIDEO", "sub": "link in description"}, "smug", "grin"), sfx=DING),
 {"speaker": "bit", "say": "Follow for one AI trick a day.", "end": True},
]

series = {
 "title": "How zylo.video Works",
 "rubric": "tips: channel (site)", "mood": "tech", "seed": 7300, "standalone": True, "look": "tips",
 "names": {"hero": "JAY", "bit": "BIT"},
 "finale": {"text": "ZYLO.VIDEO", "sub": "Every video. One site."},
 "parts": [{"title": "zylo.video", "lines": lines}],
}
(D / "series.json").write_text(json.dumps(series, indent=1, ensure_ascii=False) + "\n")

meta = {"part1": {
    "title": "Every zylo Video in One Place: zylo.video #shorts", "short": True,
    "description": "Watch every zylo video on zylo.video: search, rubrics, sort by most viewed, play right on the page, and suggest the next video. https://zylo.video\nAn original animated explainer by zylo.\n\nFollow for one AI trick a day.\n\n#zylo #ai #animation #website #shorts",
    "tags": ["zylo", "zylo.video", "zylo website", "every zylo video", "animation", "shorts"],
    "categoryId": "27", "privacy": "public", "madeForKids": False, "syntheticMedia": False}}
mp = D / "metadata.json"
if mp.exists():
    old = json.loads(mp.read_text())
    for k, v in meta.items():
        if "publishAt" in old.get(k, {}): v["publishAt"] = old[k]["publishAt"]
mp.write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")

spoken = [l for l in lines if not l.get("end")]
w = sum(len(re.sub(r"[*\"]", "", l["say"]).split()) for l in spoken)
print(f"{len(lines)} lines, {w} words")
print(len(meta["part1"]["title"]), meta["part1"]["title"])
