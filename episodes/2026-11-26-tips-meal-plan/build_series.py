"""Writes series.json + metadata.json for the tips Short "A week of dinners for $40 - let AI plan it".
Tips format (owner's reference 2026-11-19). Food angle again (the 'fridge photo' tip stays the channel's best).
Honest: prices differ by store/city, so ask it to use your store's prices or check the total. No statistics.
Run: python3 episodes/2026-11-26-tips-meal-plan/build_series.py"""
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
P = "Plan 5 dinners for one person. Budget $40 total. Reuse ingredients. Give me one shopping list."

lines = [
 L("hero", "Bit, I spend so much on *takeout*. Every single night.", CLOSE, [face("sad", "facepalm")], sfx=[{"type": "riser"}]),
 L("bit", "Because at 8 p.m. nobody wants to *think*.", **W({"kind": "title", "text": "8 P.M. BRAIN", "sub": "too tired to decide"}, "smug", "sad"), sfx=TICK),
 L("bit", "So decide once. On *Sunday*. With AI.", **W({"kind": "step", "n": 1, "text": "Sunday, 5 minutes."}, "happy"), sfx=POP),
 L("bit", "Ask for five dinners. Give it a *budget*.", **W({"kind": "chat", "from": "hero", "text": P}, "neutral"), sfx=TICK),
 L("hero", "Why *reuse* ingredients?", CLOSE, [face("neutral", "think")]),
 L("bit", "Half a bag of spinach rots. Reuse it, and you waste *nothing*.", **W({"kind": "compare", "bad": "5 random recipes", "good": "5 dinners that share ingredients"}, "smug", "neutral"), sfx=DING),
 L("bit", "Now it plans the *week*.", **W({"kind": "list", "title": "YOUR WEEK", "items": ["Mon: chicken rice bowl", "Tue: spinach pasta", "Wed: chicken wraps", "Thu: egg fried rice", "Fri: pasta bake"]}, "happy"), sfx=[{"type": "ding"}, {"type": "ding", "at": .3}, {"type": "ding", "at": .6}]),
 L("bit", "Step two. One *shopping list*. Sorted by aisle.", **W({"kind": "step", "n": 2, "text": "Make it one shopping list, sorted by aisle."}, "neutral"), sfx=POP),
 L("hero", "But are the prices *right*?", CLOSE, [face("scared", "think")]),
 L("bit", "Not always. Prices change by store. So check the *total*.", **W({"kind": "stat", "label": "CHECK AT THE STORE", "value": 40, "prefix": "$", "sub": "your prices may differ"}, "think", "scared")),
 L("bit", "Step three. Ask: which dinner can I cook *twice* and freeze?", **W({"kind": "step", "n": 3, "text": "Which one can I double and freeze?"}, "happy"), sfx=POP),
 L("bit", "Plan. List. *Freezer*. That's the trick.", **W({"kind": "slots", "title": "THE TRICK", "items": [{"icon": "clock", "label": "PLAN SUNDAY"}, {"icon": "lines", "label": "ONE LIST"}, {"icon": "check", "label": "COOK TWICE"}]}, "smug")),
 L("hero", "Friday night. No takeout. I cooked *five times*!", CLOSE, [face("happy", "cheer")], sfx=[{"type": "powerup"}]),
 L("bit", "Proud of you. Saturday? Pizza. You *earned* it.", **W({"kind": "title", "text": "SATURDAY: PIZZA", "sub": "earned it"}, "happy", "grin"), sfx=[{"type": "ding"}]),
 {"speaker": "bit", "say": "Follow for one AI trick a day.", "end": True},
]

series = {
 "title": "A Week of Dinners for $40? Let AI Plan It",
 "rubric": "tips: AI (everyday life)", "mood": "tech", "seed": 7500, "standalone": True, "look": "tips",
 "names": {"hero": "JAY", "bit": "BIT"},
 "finale": {"text": "1 AI TRICK A DAY", "sub": "Follow so you don't miss tomorrow's"},
 "parts": [{"title": "Meal Plan", "lines": lines}],
}
(D / "series.json").write_text(json.dumps(series, indent=1, ensure_ascii=False) + "\n")

meta = {"part1": {
    "title": "A Week of Dinners for $40? Let AI Plan It #shorts", "short": True,
    "description": "Stop deciding dinner at 8 p.m. On Sunday, ask AI for 5 dinners on a budget that reuse ingredients, one shopping list sorted by aisle, and one meal to cook twice and freeze. Check the prices at your store.\nAn original animated AI tip by zylo.\n\nFollow for one AI trick a day.\n\n#ai #chatgpt #mealprep #budget #shorts",
    "tags": ["ai tips", "chatgpt meal plan", "meal prep", "cheap dinners", "budget meals", "grocery list", "life hacks", "shorts"],
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
