"""Writes series.json + metadata.json for the tips Short "Make AI interview you first".
Tips format (owner's reference 2026-11-19): Jay asks, Bit explains, pixel desk studio, steps on the monitor.
A real, widely used prompting technique (ask the model to ask you questions before it writes). No statistics.
Run: python3 episodes/2026-11-21-tips-interview-me/build_series.py"""
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
 L("hero", "Bit, AI wrote my dad's birthday speech. It's so *boring*.", CLOSE, [face("sad", "shrug")], sfx=[{"type": "riser"}]),
 L("bit", "Show me what you *asked*.", **W({"kind": "chat", "from": "hero", "text": ASK}, "think", "sad"), sfx=TICK),
 L("bit", "One line. It knows *nothing* about your dad.", **W({"kind": "chat", "from": "hero", "text": ASK, "reply": 4}, "smug")),
 L("bit", "So it writes a speech for *any* dad.", **W({"kind": "prompts", "text": ASK, "n": 3}, "sad"), sfx=[{"type": "buzz"}]),
 L("hero", "So I have to write *everything* myself?", CLOSE, [face("shocked", "shrug")]),
 L("bit", "No. Let the AI *interview* you.", **W({"kind": "title", "text": "LET IT INTERVIEW YOU"}, "happy", "neutral"), sfx=DING),
 L("bit", "Add one line before it *writes*.", **W({"kind": "step", "n": 1, "text": ASK}, "neutral"), sfx=POP),
 L("bit", "Ask me five questions first. *One at a time*.", **W({"kind": "chat", "from": "hero", "text": ASK + " " + ASK2}, "think"), sfx=TICK),
 L("bit", "Now it asks what only *you* know.", **W({"kind": "list", "title": "AI ASKS YOU", "items": ["What does he love?", "His worst joke?", "A story only you know?"]}, "happy"), sfx=[{"type": "ding"}, {"type": "ding", "at": .4}]),
 L("hero", "His worst joke? Oh, I have *ten*.", CLOSE, [face("grin", "point")]),
 L("bit", "Perfect. One at a time keeps the answers *short*.", **W({"kind": "chat", "from": "bit", "text": "Question 2 of 5: what's his worst joke?", "reply": "Why did the scarecrow win a prize? He was outstanding in his field."}, "smug", "grin"), sfx=POP),
 L("bit", "Then step two: tell it the *tone* and length.", **W({"kind": "step", "n": 2, "text": "Now write it. Funny, warm, under two minutes."}, "neutral"), sfx=POP),
 L("bit", "Details. Tone. *Length*. That's the whole script.", **W({"kind": "slots", "title": "A GOOD ANSWER NEEDS", "items": [{"icon": "chat", "label": "YOUR DETAILS"}, {"icon": "star", "label": "TONE"}, {"icon": "clock", "label": "LENGTH"}]}, "happy")),
 L("hero", "Works for speeches. What *else*?", CLOSE, [face("neutral", "think")]),
 L("bit", "Cover letters. Gift ideas. Trip plans. *Anything* personal.", **W({"kind": "compare", "bad": "Plan a trip to Rome", "good": "Ask me 5 questions, then plan my Rome trip"}, "happy", "neutral"), sfx=DING),
 L("hero", "Okay. Speech done. Dad *cried*.", CLOSE, [face("happy", "cheer")], sfx=[{"type": "powerup"}]),
 L("bit", "Happy tears? Or the *scarecrow* joke?", **W({"kind": "title", "text": "OUTSTANDING", "sub": "in his field"}, "smug", "grin"), sfx=[{"type": "ding"}]),
 {"speaker": "bit", "say": "Follow for one AI trick a day.", "end": True},
]

series = {
 "title": "Make AI Interview You First",
 "rubric": "tips: AI (prompting)", "mood": "tech", "seed": 6900, "standalone": True, "look": "tips",
 "names": {"hero": "JAY", "bit": "BIT"},
 "finale": {"text": "1 AI TRICK A DAY", "sub": "Follow so you don't miss tomorrow's"},
 "parts": [{"title": "Interview Me", "lines": lines}],
}
(D / "series.json").write_text(json.dumps(series, indent=1, ensure_ascii=False) + "\n")

meta = {"part1": {
    "title": "Your AI Writes Boring Stuff? Let It Interview You #shorts", "short": True,
    "description": "One-line prompts get generic answers. Add one line: \"Before you write, ask me 5 questions, one at a time.\" Then set the tone and length.\nAn original animated AI tip by zylo.\n\nFollow for one AI trick a day.\n\n#ai #chatgpt #aitips #productivity #shorts",
    "tags": ["ai tips", "chatgpt tips", "how to prompt ai", "prompt tips", "birthday speech", "ai writing", "productivity", "shorts"],
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
