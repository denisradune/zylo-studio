"""Writes series.json + metadata.json for the tips Short "Photo of your messy room -> 15-minute cleaning plan".
Tips format (owner's reference 2026-11-19): Jay asks, Bit explains, pixel desk studio, steps on the monitor.
Everyday-life AI tip (the 'fridge photo' tip was the channel's best on 2026-11-24). Honest, no statistics.
Run: python3 episodes/2026-11-24-tips-messy-room/build_series.py"""
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
P = "Here's my room. Give me a 15-minute cleaning plan. Smallest steps first. Set a timer for each."

lines = [
 L("hero", "Bit, my room is a *disaster*. I don't know where to start.", CLOSE, [face("sad", "facepalm")], sfx=[{"type": "riser"}]),
 L("bit", "That's the real problem. Not the mess. The *start*.", **W({"kind": "title", "text": "WHERE DO I START?"}, "smug", "sad"), sfx=TICK),
 L("bit", "Step one. Take one photo of the *whole* room.", **W({"kind": "step", "n": 1, "text": "Take a photo of your room."}, "neutral"), sfx=POP),
 L("bit", "Send it to an AI chat that reads *pictures*.", **W({"kind": "chat", "from": "hero", "text": "[photo of my room]"}, "neutral"), sfx=TICK),
 L("bit", "Step two. Ask for a plan with a *time limit*.", **W({"kind": "step", "n": 2, "text": P}, "think"), sfx=POP),
 L("hero", "Why fifteen minutes? I need *five hours*.", CLOSE, [face("shocked", "shrug")]),
 L("bit", "Five hours sounds scary. Fifteen minutes sounds *doable*.", **W({"kind": "compare", "bad": "Clean my room", "good": "15-minute plan. Smallest steps first."}, "happy", "neutral"), sfx=DING),
 L("bit", "Look. It sees your room and splits it into *tiny* jobs.", **W({"kind": "list", "title": "YOUR 15 MINUTES", "items": ["3 min: clothes in basket", "4 min: dishes out", "5 min: clear the desk", "3 min: trash bag"]}, "happy"), sfx=[{"type": "ding"}, {"type": "ding", "at": .3}, {"type": "ding", "at": .6}]),
 L("hero", "Three minutes for clothes? I can do *three minutes*.", CLOSE, [face("grin", "point")]),
 L("bit", "That's the trick. Small first, so you *keep going*.", **W({"kind": "slots", "title": "WHY IT WORKS", "items": [{"icon": "search", "label": "IT SEES"}, {"icon": "clock", "label": "TIME LIMIT"}, {"icon": "check", "label": "TINY WINS"}]}, "smug")),
 L("bit", "Step three. Done? Take a new photo. Ask: what's *next*?", **W({"kind": "step", "n": 3, "text": "Here's my room now. What's next?"}, "neutral"), sfx=POP),
 L("hero", "Wait. Is the AI going to *judge* my room?", CLOSE, [face("scared", "think")]),
 L("bit", "No. And if you don't want to share, describe it in *words*.", **W({"kind": "chat", "from": "hero", "text": "Clothes on the chair, cups on the desk, bed not made."}, "happy", "scared"), sfx=TICK),
 L("hero", "Fifteen minutes later: a *clean* room.", CLOSE, [face("happy", "cheer")], sfx=[{"type": "powerup"}]),
 L("bit", "And under the bed it found your *other sock*.", **W({"kind": "title", "text": "SOCK FOUND", "sub": "missing since 2024"}, "smug", "grin"), sfx=[{"type": "ding"}]),
 {"speaker": "bit", "say": "Follow for one AI trick a day.", "end": True},
]

series = {
 "title": "Messy Room? Send AI One Photo",
 "rubric": "tips: AI (everyday life)", "mood": "tech", "seed": 7200, "standalone": True, "look": "tips",
 "names": {"hero": "JAY", "bit": "BIT"},
 "finale": {"text": "1 AI TRICK A DAY", "sub": "Follow so you don't miss tomorrow's"},
 "parts": [{"title": "Messy Room", "lines": lines}],
}
(D / "series.json").write_text(json.dumps(series, indent=1, ensure_ascii=False) + "\n")

meta = {"part1": {
    "title": "Messy Room? Send AI One Photo (15-Minute Plan) #shorts", "short": True,
    "description": "Don't know where to start cleaning? Send an AI chat one photo of your room and ask for a 15-minute plan, smallest steps first. Then send a new photo and ask what's next.\nAn original animated AI tip by zylo.\n\nFollow for one AI trick a day.\n\n#ai #chatgpt #aitips #cleaningmotivation #shorts",
    "tags": ["ai tips", "chatgpt tips", "cleaning motivation", "messy room", "how to start cleaning", "life hacks", "productivity", "shorts"],
    "categoryId": "26", "privacy": "public", "madeForKids": False, "syntheticMedia": False}}
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
