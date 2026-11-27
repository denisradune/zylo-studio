"""Writes series.json + metadata.json for the tips Short "You're paying for subscriptions you forgot".
Tips format (owner's reference 2026-11-19). Everyday money tip with a stronger curiosity hook (recent tips slowed).
Safety: hide card/account numbers before pasting; AI only lists, you cancel. No statistics.
Run: python3 episodes/2026-11-27-tips-subscriptions/build_series.py"""
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
P = "Here are my card payments for 3 months (numbers hidden). List every repeating charge, how much per year, and which ones I might not use."

lines = [
 L("hero", "Bit, why is my money *gone* every month?", CLOSE, [face("sad", "shrug")], sfx=[{"type": "riser"}]),
 L("bit", "Maybe you're paying for things you *forgot*.", **W({"kind": "title", "text": "FORGOTTEN SUBSCRIPTIONS?"}, "smug", "sad"), sfx=[{"type": "buzz"}]),
 L("bit", "Step one. Open your banking app. Copy three months of *payments*.", **W({"kind": "step", "n": 1, "text": "Copy 3 months of card payments."}, "neutral"), sfx=POP),
 L("bit", "But first: hide card numbers and account *numbers*.", **W({"kind": "compare", "bad": "Card 4921 8830 ...", "good": "Card ****  (numbers hidden)"}, "think"), sfx=DING),
 L("bit", "Step two. Ask AI to find every *repeating* charge.", **W({"kind": "chat", "from": "hero", "text": P}, "neutral"), sfx=TICK),
 L("hero", "Why ask for the price per *year*?", CLOSE, [face("neutral", "think")]),
 L("bit", "Nine ninety-nine sounds small. A hundred twenty a year *doesn't*.", **W({"kind": "stat", "label": "PER YEAR", "value": 120, "prefix": "$", "sub": "just $9.99 a month"}, "smug", "neutral")),
 L("bit", "Now it shows the *list*.", **W({"kind": "list", "title": "REPEATING CHARGES", "items": ["Music app: $11/mo", "Old gym app: $8/mo", "Cloud storage x2: $6/mo", "Free trial (not free): $15/mo"]}, "happy"), sfx=[{"type": "ding"}, {"type": "ding", "at": .3}, {"type": "ding", "at": .6}]),
 L("hero", "Two cloud storages? And a gym app? I don't *go* to the gym!", CLOSE, [face("shocked", "facepalm")], sfx=[{"type": "boom"}]),
 L("bit", "Step three. You cancel. Not the AI. *You*.", **W({"kind": "step", "n": 3, "text": "Cancel in each app or store settings."}, "neutral"), sfx=POP),
 L("bit", "Ask it how to cancel each one, step by step.", **W({"kind": "slots", "title": "THE TRICK", "items": [{"icon": "search", "label": "FIND"}, {"icon": "money", "label": "PER YEAR"}, {"icon": "cross", "label": "CANCEL"}]}, "happy")),
 L("hero", "Three cancelled. That's money back every *month*.", CLOSE, [face("happy", "cheer")], sfx=[{"type": "powerup"}]),
 L("bit", "Don't celebrate yet. One more charge: *zylo premium*.", **W({"kind": "title", "text": "ZYLO PREMIUM?", "sub": "just kidding. zylo is free."}, "smug", "shocked"), sfx=[{"type": "ding"}]),
 {"speaker": "bit", "say": "Follow for one AI trick a day.", "end": True},
]

series = {
 "title": "You're Paying for Subscriptions You Forgot",
 "rubric": "tips: AI (money)", "mood": "tech", "seed": 7600, "standalone": True, "look": "tips",
 "names": {"hero": "JAY", "bit": "BIT"},
 "finale": {"text": "1 AI TRICK A DAY", "sub": "Follow so you don't miss tomorrow's"},
 "parts": [{"title": "Subscriptions", "lines": lines}],
}
(D / "series.json").write_text(json.dumps(series, indent=1, ensure_ascii=False) + "\n")

meta = {"part1": {
    "title": "You're Paying for Subscriptions You Forgot #shorts", "short": True,
    "description": "Copy 3 months of card payments (hide your card and account numbers), ask AI to list every repeating charge and its price per year, then cancel the ones you don't use yourself.\nAn original animated AI tip by zylo.\n\nFollow for one AI trick a day.\n\n#ai #chatgpt #moneytips #savemoney #shorts",
    "tags": ["ai tips", "chatgpt tips", "save money", "cancel subscriptions", "forgotten subscriptions", "budget", "money tips", "shorts"],
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
