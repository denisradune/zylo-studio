"""Writes series.json + metadata.json for the tips Short "Your plant is dying? Send AI one photo".
Tips format (owner's reference 2026-11-19). Everyday-life photo tip (the 'fridge photo' tip is the channel's best,
13.75x median on 2026-11-25). Honest caveat: AI guesses from a photo, check one thing at a time. No statistics.
Run: python3 episodes/2026-11-25-tips-plant-photo/build_series.py"""
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
P = "Here's my plant. What's wrong? Ask me 3 questions first: light, water, how long I've had it."

lines = [
 L("hero", "Bit, my plant is *dying*. And I water it every day!", CLOSE, [face("sad", "facepalm")], sfx=[{"type": "riser"}]),
 L("bit", "Every day? That might be the *problem*.", **W({"kind": "title", "text": "EVERY DAY?!"}, "shocked", "sad"), sfx=[{"type": "buzz"}]),
 L("bit", "Step one. Take a close photo of the *leaves*.", **W({"kind": "step", "n": 1, "text": "Take a close photo of the leaves."}, "neutral"), sfx=POP),
 L("bit", "Send it to an AI chat that reads *pictures*.", **W({"kind": "chat", "from": "hero", "text": "[photo of my plant]"}, "neutral"), sfx=TICK),
 L("bit", "Step two. Don't just ask what's wrong. Let it ask *you* first.", **W({"kind": "step", "n": 2, "text": P}, "think"), sfx=POP),
 L("hero", "Why does it need to ask *me*?", CLOSE, [face("neutral", "think")]),
 L("bit", "Yellow leaves can mean too much water. Or too little *light*.", **W({"kind": "compare", "bad": "What's wrong with my plant?", "good": "Ask me about light and water first."}, "happy", "neutral"), sfx=DING),
 L("bit", "Your answers help it guess *right*.", **W({"kind": "list", "title": "IT ASKS YOU", "items": ["How much light?", "How often water?", "Drainage hole?"]}, "neutral"), sfx=[{"type": "ding"}, {"type": "ding", "at": .4}]),
 L("hero", "Drainage hole? Like, a hole in the *pot*?", CLOSE, [face("shocked", "point")], sfx=[{"type": "hit"}]),
 L("bit", "Yes. No hole, water stays in. The roots *drown*.", **W({"kind": "chat", "from": "hero", "text": P, "reply": "Likely too much water + no drainage. Water once a week, move to a pot with a hole."}, "smug", "shocked"), sfx=POP),
 L("bit", "Step three. Change *one* thing. Then send a new photo in a week.", **W({"kind": "step", "n": 3, "text": "Here it is one week later. Better?"}, "neutral"), sfx=POP),
 L("bit", "It's a guess from a photo. So test one change at a *time*.", **W({"kind": "slots", "title": "THE TRICK", "items": [{"icon": "search", "label": "PHOTO"}, {"icon": "question", "label": "ITS QUESTIONS"}, {"icon": "check", "label": "ONE CHANGE"}]}, "think")),
 L("hero", "One week later: a new *leaf*!", CLOSE, [face("happy", "cheer")], sfx=[{"type": "powerup"}]),
 L("bit", "Congratulations. You stopped *drowning* it.", **W({"kind": "title", "text": "PLANT SAVED", "sub": "water: once a week"}, "smug", "grin"), sfx=[{"type": "ding"}]),
 {"speaker": "bit", "say": "Follow for one AI trick a day.", "end": True},
]

series = {
 "title": "Your Plant Is Dying? Send AI One Photo",
 "rubric": "tips: AI (everyday life)", "mood": "tech", "seed": 7400, "standalone": True, "look": "tips",
 "names": {"hero": "JAY", "bit": "BIT"},
 "finale": {"text": "1 AI TRICK A DAY", "sub": "Follow so you don't miss tomorrow's"},
 "parts": [{"title": "Plant Photo", "lines": lines}],
}
(D / "series.json").write_text(json.dumps(series, indent=1, ensure_ascii=False) + "\n")

meta = {"part1": {
    "title": "Your Plant Is Dying? Send AI One Photo #shorts", "short": True,
    "description": "Send an AI chat a close photo of the leaves and let it ask you about light, water and drainage first. Then change one thing and send a new photo in a week.\nAn original animated AI tip by zylo.\n\nFollow for one AI trick a day.\n\n#ai #chatgpt #aitips #plantcare #shorts",
    "tags": ["ai tips", "chatgpt tips", "plant care", "dying plant", "yellow leaves", "plant tips", "life hacks", "shorts"],
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
