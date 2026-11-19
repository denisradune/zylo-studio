"""Writes series.json + metadata.json for the tips Short "Why does your AI sound like a robot? The two-message trick".
New format (owner's reference video 2026-11-19): useful AI/productivity tip told as a dialogue — Jay asks, Bit explains —
in the pixel-art desk studio ("look": "tips"), each step drawn on the monitor. A common prompting technique, no
statistics or claims about real accounts.
Run: python3 episodes/2026-11-20-tips-two-messages/build_series.py"""
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
def face(expr="neutral", pose="idle", x=.5): return {"id": "hero", "x": x, "pose": pose, "expr": expr, "scale": 3.4, "lift": -950}
def W(screen, expr="neutral", jexpr=None, **kw):
    cast = ([jay(jexpr)] if jexpr else []) + [bit(expr)]
    return dict(set_=WIDE, cast=cast, screen=screen, **kw)
POP = [{"type": "pop"}]; DING = [{"type": "ding"}]; TICK = [{"type": "tick"}]
PROMPT1 = "Here's my topic: home workouts. Find 10 problems people worry about. For each one, write a sharp question."

lines = [
 L("hero", "Bit, why does my AI always sound like a *robot*?", CLOSE, [face("sad", "shrug")], sfx=[{"type": "riser"}]),
 L("bit", "Because you ask like everyone *else*.", **W({"kind": "prompts", "text": "write me a viral video", "n": 3}, "smug", "neutral"), sfx=POP),
 L("bit", "Everyone types: write me a viral video.", **W({"kind": "prompts", "text": "write me a viral video", "n": 3}, "neutral"), sfx=TICK),
 L("bit", "So everyone gets the *same* boring script.", **W({"kind": "chat", "from": "hero", "text": "write me a viral video", "reply": 4}, "sad"), sfx=[{"type": "buzz"}]),
 L("hero", "Okay. So how do I ask *right*?", CLOSE, [face("neutral", "think")]),
 L("bit", "Two messages. Not *one*.", **W({"kind": "title", "text": "2 MESSAGES", "sub": "not one"}, "happy", "neutral"), sfx=DING),
 L("bit", "Message one. Tell me your *topic*.", **W({"kind": "step", "n": 1, "text": "Here's my topic: home workouts."}, "neutral"), sfx=POP),
 L("bit", "Ask for ten problems people really *worry about*.", **W({"kind": "chat", "from": "hero", "text": PROMPT1}, "think"), sfx=TICK),
 L("bit", "And for each one, a question you can't *scroll past*.", **W({"kind": "cards", "n": 10, "mark": "?"}, "happy"), sfx=[{"type": "whoosh"}]),
 L("hero", "Ten questions. So I make ten *videos*?", CLOSE, [face("shocked", "shrug")]),
 L("bit", "No. Message *two*.", **W({"kind": "step", "n": 2}, "smug", "shocked"), sfx=POP),
 L("bit", "Pick the strongest question. Ask for a thirty-second *script*.", **W({"kind": "cards", "n": 10, "mark": "?", "pick": 3}, "think"), sfx=DING),
 L("bit", "First line *hooks*. Then simple words. Then a question for the *comments*.", **W({"kind": "slots", "title": "30-SECOND SCRIPT", "items": [{"icon": "hook", "label": "HOOK"}, {"icon": "lines", "label": "SIMPLE"}, {"icon": "question", "label": "QUESTION"}]}, "happy")),
 L("hero", "Script's ready. Can I post it?", CLOSE, [face("happy", "point")]),
 L("bit", "Not yet. First check: do videos on this question already get *views*?", **W({"kind": "videos", "title": "VIDEOS ON THIS QUESTION", "items": [{"views": "2.8M", "ok": True}, {"views": "940K", "ok": True}, {"views": "3.1M", "ok": True}]}, "neutral", "neutral"), sfx=[{"type": "ding"}, {"type": "ding", "at": .3}]),
 L("hero", "And if nobody made one?", CLOSE, [face("neutral", "think")]),
 L("bit", "Then take the *next* question. You still have nine.", **W({"kind": "cards", "n": 10, "mark": "?", "pick": 4}, "smug"), sfx=[{"type": "whoosh"}]),
 L("hero", "All that for *one* video?", CLOSE, [face("sad", "facepalm")]),
 L("bit", "For one video people actually *watch*.", **W({"kind": "list", "title": "THE TRICK", "items": ["Topic + 10 problems", "Best question = script", "Check it gets views"]}, "happy", "happy"), sfx=[{"type": "powerup"}]),
 {"speaker": "bit", "say": "Follow for one AI trick a day.", "end": True},
]

series = {
 "title": "Why Does Your AI Sound Like a Robot?",
 "rubric": "tips: AI (prompting)", "mood": "tech", "seed": 6800, "standalone": True, "look": "tips",
 "names": {"hero": "JAY", "bit": "BIT"},
 "finale": {"text": "1 AI TRICK A DAY", "sub": "Follow so you don't miss tomorrow's"},
 "parts": [{"title": "Two Messages", "lines": lines}],
}
(D / "series.json").write_text(json.dumps(series, indent=1, ensure_ascii=False) + "\n")

meta = {"part1": {
    "title": "Why Your AI Sounds Like a Robot (2-Message Fix) #shorts", "short": True,
    "description": "\"Write me a viral video\" gets everyone the same boring script. Ask AI in two messages instead: problems and questions first, then the script.\nAn original animated AI tip by zylo.\n\nFollow for one AI trick a day.\n\n#ai #chatgpt #aitips #productivity #shorts",
    "tags": ["ai tips", "how to prompt ai", "chatgpt tips", "prompt engineering", "viral script", "ai for content", "productivity", "shorts"],
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
