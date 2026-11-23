"""Writes series.json + metadata.json for the tips Short "Photo of your fridge -> dinner in 20 minutes".
Tips format (owner's reference 2026-11-19): Jay asks, Bit explains, pixel desk studio, steps on the monitor.
A real everyday use of multimodal AI chat apps (send a photo, ask for a recipe with limits), with the honest
caveat that AI can't check freshness or allergies. No statistics.
Run: python3 episodes/2026-11-23-tips-fridge-photo/build_series.py"""
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
P = "What can I cook in 20 minutes with only this? No shopping. Easy steps."

lines = [
 L("hero", "Bit, my fridge is full. And there's *nothing* to eat.", CLOSE, [face("sad", "shrug")], sfx=[{"type": "riser"}]),
 L("bit", "Classic. Open the fridge. Take *one photo*.", **W({"kind": "step", "n": 1, "text": "Take a photo of your fridge."}, "smug", "sad"), sfx=POP),
 L("bit", "Send it to any AI chat app that takes *pictures*.", **W({"kind": "chat", "from": "hero", "text": "[photo of my fridge]"}, "neutral"), sfx=TICK),
 L("bit", "Then the important part. Give it *limits*.", **W({"kind": "step", "n": 2, "text": P}, "think"), sfx=POP),
 L("hero", "Why limits? Just ask for a *recipe*.", CLOSE, [face("neutral", "think")]),
 L("bit", "Without limits, it suggests lasagna. And a trip to the *store*.", **W({"kind": "compare", "bad": "Give me a recipe", "good": "Only what's in the photo. 20 minutes. No shopping."}, "smug", "neutral"), sfx=[{"type": "buzz"}]),
 L("bit", "Time. Only these ingredients. Your *skill level*.", **W({"kind": "slots", "title": "ADD 3 LIMITS", "items": [{"icon": "clock", "label": "TIME"}, {"icon": "search", "label": "ONLY THIS"}, {"icon": "star", "label": "SKILL"}]}, "happy")),
 L("bit", "Now look what it *finds*.", **W({"kind": "chat", "from": "hero", "text": P, "reply": "Eggs + leftover rice + peas = fried rice. 15 minutes. Step 1: heat the pan..."}, "happy", "shocked"), sfx=DING),
 L("hero", "Fried rice? I had *all* of that?", CLOSE, [face("shocked", "point")], sfx=[{"type": "hit"}]),
 L("bit", "Step three. Ask for *two more* options.", **W({"kind": "cards", "n": 3, "mark": "?", "pick": 1}, "neutral"), sfx=[{"type": "whoosh"}]),
 L("bit", "The first idea is rarely the *best* one.", **W({"kind": "list", "title": "3 OPTIONS", "items": ["Fried rice", "Cheesy omelette", "Pasta with peas"]}, "think"), sfx=[{"type": "ding"}, {"type": "ding", "at": .4}]),
 L("hero", "Can it tell if the milk is *still good*?", CLOSE, [face("scared", "think")]),
 L("bit", "No. It can't smell. Dates and allergies are *your* job.", **W({"kind": "title", "text": "IT CAN'T SMELL", "sub": "check dates + allergies yourself"}, "sad", "neutral"), sfx=[{"type": "buzz"}]),
 L("hero", "Fifteen minutes later: *dinner*.", CLOSE, [face("happy", "cheer")], sfx=[{"type": "powerup"}]),
 L("bit", "And one more thing it found in the photo.", **W({"kind": "chat", "from": "bit", "text": "Also: the cheese behind the jam is from March."}, "smug", "shocked"), sfx=[{"type": "ding"}]),
 L("hero", "March of *which year*?", CLOSE, [face("scared", "facepalm")], sfx=[{"type": "boom"}]),
 {"speaker": "bit", "say": "Follow for one AI trick a day.", "end": True},
]

series = {
 "title": "Photo of Your Fridge = Dinner in 20 Minutes",
 "rubric": "tips: AI (everyday life)", "mood": "tech", "seed": 7100, "standalone": True, "look": "tips",
 "names": {"hero": "JAY", "bit": "BIT"},
 "finale": {"text": "1 AI TRICK A DAY", "sub": "Follow so you don't miss tomorrow's"},
 "parts": [{"title": "Fridge Photo", "lines": lines}],
}
(D / "series.json").write_text(json.dumps(series, indent=1, ensure_ascii=False) + "\n")

meta = {"part1": {
    "title": "Nothing to Eat? Send AI a Photo of Your Fridge #shorts", "short": True,
    "description": "Take one photo of your fridge, send it to an AI chat app and give it limits: 20 minutes, only what's in the photo, no shopping. Then ask for two more options. (It can't smell the milk, though.)\nAn original animated AI tip by zylo.\n\nFollow for one AI trick a day.\n\n#ai #chatgpt #aitips #cookinghacks #shorts",
    "tags": ["ai tips", "chatgpt tips", "what to cook", "fridge recipe", "ai cooking", "life hacks", "productivity", "shorts"],
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
