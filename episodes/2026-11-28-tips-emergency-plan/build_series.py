"""Writes series.json + metadata.json for the tips Short "Power out for 3 days? Make an AI emergency plan in 10 minutes".
Tips format, blended with the channel's best theme (disaster). Honest: AI makes a checklist, official local guidance wins;
no medical/legal claims, no statistics.
Run: python3 episodes/2026-11-28-tips-emergency-plan/build_series.py"""
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
P = "Make a 3-day power outage plan for my home: 2 adults, 1 cat, small apartment. Checklist, what to buy, where to meet."

lines = [
 L("hero", "Bit, what if the power goes out for *three days*?", CLOSE, [face("scared", "think")], sfx=[{"type": "riser"}]),
 L("bit", "Most people have *no plan*. Let's fix that in ten minutes.", **W({"kind": "title", "text": "NO POWER. 3 DAYS.", "sub": "do you have a plan?"}, "neutral", "scared"), sfx=[{"type": "alarm"}]),
 L("bit", "Step one. Tell AI who lives in your *home*.", **W({"kind": "chat", "from": "hero", "text": P}, "neutral"), sfx=TICK),
 L("hero", "Why does it need to know about my *cat*?", CLOSE, [face("neutral", "shrug")]),
 L("bit", "Because the cat needs water and food *too*.", **W({"kind": "compare", "bad": "Make an emergency plan", "good": "Plan for 2 adults, 1 cat, small apartment"}, "smug", "neutral"), sfx=DING),
 L("bit", "Now you get a real *checklist*.", **W({"kind": "list", "title": "3-DAY KIT", "items": ["Water for everyone (+ cat)", "Food you don't need to cook", "Flashlight + batteries", "Power bank, charged"]}, "happy"), sfx=[{"type": "ding"}, {"type": "ding", "at": .3}, {"type": "ding", "at": .6}]),
 L("bit", "Step two. Ask: what do I *already* have?", **W({"kind": "step", "n": 2, "text": "Here's what's in my kitchen. What's missing?"}, "think"), sfx=POP),
 L("bit", "So you only buy what's *missing*.", **W({"kind": "cards", "n": 6, "mark": "?", "pick": 2}, "happy"), sfx=[{"type": "whoosh"}]),
 L("bit", "Step three. A *meeting point*. If phones are down, where do you meet?", **W({"kind": "step", "n": 3, "text": "No signal? Meet at the library."}, "neutral"), sfx=POP),
 L("hero", "Can I trust the AI's *plan*?", CLOSE, [face("scared", "think")]),
 L("bit", "Use it as a start. Then check your *local* official guidance.", **W({"kind": "slots", "title": "THE TRICK", "items": [{"icon": "chat", "label": "WHO"}, {"icon": "check", "label": "MISSING"}, {"icon": "search", "label": "OFFICIAL"}]}, "think")),
 L("hero", "Ten minutes. And now we *have* a plan.", CLOSE, [face("happy", "cheer")], sfx=[{"type": "powerup"}]),
 L("bit", "And the cat approves. The snacks are *hers*.", **W({"kind": "title", "text": "CAT APPROVED", "sub": "snacks reserved"}, "smug", "grin"), sfx=[{"type": "ding"}]),
 {"speaker": "bit", "say": "Follow for one AI trick a day.", "end": True},
]

series = {
 "title": "Power Out for 3 Days? Make an AI Plan",
 "rubric": "tips: AI (disaster prep)", "mood": "tech", "seed": 7700, "standalone": True, "look": "tips",
 "names": {"hero": "JAY", "bit": "BIT"},
 "finale": {"text": "1 AI TRICK A DAY", "sub": "Follow so you don't miss tomorrow's"},
 "parts": [{"title": "Emergency Plan", "lines": lines}],
}
(D / "series.json").write_text(json.dumps(series, indent=1, ensure_ascii=False) + "\n")

meta = {"part1": {
    "title": "What If the Power Went Out for 3 Days? Ask AI #shorts", "short": True,
    "description": "Tell AI who lives in your home (pets too), get a 3-day checklist, ask what you're missing, and pick a meeting point. Then check your local official guidance.\nAn original animated AI tip by zylo.\n\nFollow for one AI trick a day.\n\n#ai #chatgpt #emergencyprep #poweroutage #shorts",
    "tags": ["ai tips", "chatgpt tips", "power outage", "emergency plan", "emergency kit", "preparedness", "what if", "shorts"],
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
