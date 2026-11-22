"""Writes series.json + metadata.json for the tips Short "Long email? Ask AI three questions".
Tips format (owner's reference 2026-11-19): Jay asks, Bit explains, pixel desk studio, steps on the monitor.
A practical, honest productivity technique (incl. the caveat to double-check names, dates and numbers). No statistics.
Run: python3 episodes/2026-11-22-tips-long-email/build_series.py"""
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
Q3 = "What do they want from me? By when? Draft a 3-line reply."

lines = [
 L("hero", "Bit, my boss sent a nine-hundred-word *email*.", CLOSE, [face("shocked", "phone")], sfx=[{"type": "riser"}]),
 L("bit", "And you read it three times. Still *lost*.", **W({"kind": "stat", "label": "EMAIL LENGTH", "value": 900, "suffix": " WORDS", "sub": "read 3 times"}, "smug", "sad"), sfx=TICK),
 L("hero", "Can you just tell me what he *wants*?", CLOSE, [face("sad", "shrug")]),
 L("bit", "Better. I'll show you how to ask *any* AI.", **W({"kind": "title", "text": "3 QUESTIONS", "sub": "for any long email"}, "happy", "neutral"), sfx=DING),
 L("bit", "Step one. Paste the whole email. Don't *summarize* it yourself.", **W({"kind": "step", "n": 1, "text": "Here's an email from my boss: [paste]"}, "neutral"), sfx=POP),
 L("bit", "Step two. Ask three questions. *Not* summarize this.", **W({"kind": "compare", "bad": "Summarize this", "good": "What do they want? By when? Draft my reply."}, "think"), sfx=TICK),
 L("bit", "What do they want from me?", **W({"kind": "slots", "title": "ASK THESE 3", "items": [{"icon": "search", "label": "THE ASK"}, {"icon": "clock", "label": "DEADLINE"}, {"icon": "chat", "label": "MY REPLY"}]}, "neutral")),
 L("bit", "By *when*? And draft a three-line *reply*.", **W({"kind": "chat", "from": "hero", "text": Q3}, "happy"), sfx=TICK),
 L("hero", "Why not just ask for a *summary*?", CLOSE, [face("neutral", "think")]),
 L("bit", "A summary is shorter. Questions give you the next *move*.", **W({"kind": "chat", "from": "hero", "text": Q3, "reply": "He wants the Q4 report. By Friday 5 p.m. Reply: On it, you'll have it Friday."}, "smug", "neutral"), sfx=[{"type": "ding"}]),
 L("hero", "Nine hundred words. And it's just: report by *Friday*?", CLOSE, [face("shocked", "facepalm")], sfx=[{"type": "boom"}]),
 L("bit", "Step three. Before you send, check names, dates and *numbers*.", **W({"kind": "step", "n": 3, "text": "Check: names, dates, numbers."}, "think"), sfx=POP),
 L("bit", "AI can mix them up. That part is *your* job.", **W({"kind": "list", "title": "BEFORE YOU SEND", "items": ["Names right?", "Dates right?", "Numbers right?"]}, "neutral"), sfx=[{"type": "ding"}, {"type": "ding", "at": .4}]),
 L("hero", "Works for group chats too?", CLOSE, [face("happy", "point")]),
 L("bit", "Two hundred unread? Same three *questions*.", **W({"kind": "stat", "label": "UNREAD", "value": 214, "sub": "3 questions"}, "happy", "grin"), sfx=DING),
 L("hero", "Bit. The boss just sent a *second* email.", CLOSE, [face("scared", "phone")]),
 L("bit", "It says: thanks for the *fast reply*.", **W({"kind": "title", "text": "THANKS FOR THE FAST REPLY"}, "smug", "grin"), sfx=[{"type": "powerup"}]),
 {"speaker": "bit", "say": "Follow for one AI trick a day.", "end": True},
]

series = {
 "title": "Long Email? Ask AI These 3 Questions",
 "rubric": "tips: AI (productivity)", "mood": "tech", "seed": 7000, "standalone": True, "look": "tips",
 "names": {"hero": "JAY", "bit": "BIT"},
 "finale": {"text": "1 AI TRICK A DAY", "sub": "Follow so you don't miss tomorrow's"},
 "parts": [{"title": "Long Email", "lines": lines}],
}
(D / "series.json").write_text(json.dumps(series, indent=1, ensure_ascii=False) + "\n")

meta = {"part1": {
    "title": "Long Email? Ask AI These 3 Questions, Not Summarize #shorts", "short": True,
    "description": "Don't ask AI to summarize a long email. Ask: what do they want from me, by when, and draft a 3-line reply. Then check names, dates and numbers yourself.\nAn original animated AI tip by zylo.\n\nFollow for one AI trick a day.\n\n#ai #chatgpt #aitips #productivity #shorts",
    "tags": ["ai tips", "chatgpt tips", "email productivity", "summarize email with ai", "work hacks", "productivity", "shorts"],
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
