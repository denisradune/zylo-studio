"""Writes series.json + metadata.json for the standalone comedy Short "What if your boss meme hit the work chat?".
Everyday-cringe comedy (owner's request 2026-11-16: funny, relatable, phone close-ups). Pure fiction, no real facts.
Run: python3 episodes/2026-11-16-what-if-wrong-chat/build_series.py"""
import json, re
from pathlib import Path
D = Path(__file__).resolve().parent

def L(sp, say, set_, cast=(), **kw):
    shot = {"set": set_ if isinstance(set_, dict) else {"type": set_}, "cast": list(cast)}
    shot.update(kw)
    return {"speaker": sp, "say": say, "shot": shot}
def c(id_, x=0.5, **kw): return {"id": id_, "x": x, **kw}
N = "narrator"
RN = {"type": "room", "time": "night"}; RD = {"type": "room", "time": "day"}
CU = {"zoom": 1.12, "y": 0.6}
PUSH = {"zoom": 1.08, "y": .45, "push": .1}
SHAKE = {"zoom": 1.05, "y": .55, "shake": .6}

GROUP = {"title": "WORK · ALL STAFF", "sub": "48 members", "clock": "23:47"}
MEME = {"from": "me", "img": "meme", "text": "the boss every monday"}
DOG = {"from": "me", "img": "dog", "text": "anyway look at this puppy"}
BITPIC = {"from": "me", "img": "bit"}
R1 = {"from": "them", "name": "Mr. Brant (Boss)", "text": "Haha. Cute dog."}
R2 = {"from": "them", "name": "Mr. Brant (Boss)", "text": "Wait. Is the meme about me?"}
R3 = {"from": "me", "text": "yes :)"}
R4 = {"from": "them", "name": "Mr. Brant (Boss)", "text": "My office. Monday. 9 a.m."}
def phone(msgs, **kw): return {"type": "phone", "time": "night", "screen": {**GROUP, "msgs": msgs, **kw}}
def rule(n, text): return {"type": "card", "text": f"RULE #{n}", "sub": text, "color": "#FF4A3D"}

lines = [
 L(N, "What if your boss meme hit the *work chat*?", phone([MEME], seen="Delivered"), [], camera=PUSH, sfx=[{"type": "pop"}, {"type": "riser", "at": .4}]),
 L(N, "Eleven forty-seven p.m. You meant the *friends* chat.", RN, [c("hero", .5, pose="phone", expr="happy", scale=1.7)], ui={"type": "clock", "text": "23:47"}),
 L(N, "Then you read the name. *All staff*.", phone([MEME], seen="Delivered"), [], camera={"zoom": 1.35, "y": .1, "x": .5}, sfx=[{"type": "hit"}]),
 L(N, "Forty-eight people. Including *the boss*.", RN, [c("hero", .5, pose="phone", expr="shocked", scale=2.0)], ui={"type": "counter", "from": 1, "to": 48, "label": "PEOPLE IN THE CHAT"}, camera=SHAKE, sfx=[{"type": "heartbeat"}]),
 L("hero", "Bit! Unsend it! *Now*!", RN, [c("hero", .3, pose="panic", expr="scared", scale=1.5), c("bit", .74, expr="shocked", scale=.9)], camera=SHAKE),
 L("bit", "The unsend window closed four seconds *ago*.", RN, [c("bit", .5, expr="sad", scale=1.6)], ui={"type": "stamp", "text": "TOO LATE"}, sfx=[{"type": "buzz"}]),
 L(N, "Rule number one. Do not *panic*.", RN, [c("hero", .5, pose="idle", expr="neutral", scale=1.6)], ui=rule(1, "DON'T PANIC")),
 L(N, "You *panic*.", RN, [c("hero", .5, pose="panic", expr="scared", scale=2.0)], camera=SHAKE, sfx=[{"type": "alarm"}], fx=[{"type": "speedLines"}]),
 L(N, "Seen by two.", phone([MEME], seen="Seen by 2"), [], sfx=[{"type": "ding"}]),
 L(N, "Seen by *nine*.", phone([MEME], seen="Seen by 9"), [], camera={"zoom": 1.06, "y": .5}, sfx=[{"type": "ding"}, {"type": "ding", "at": .4}]),
 L(N, "Then the boss starts *typing*.", phone([MEME], typing="Mr. Brant is typing"), [], camera=PUSH, sfx=[{"type": "heartbeat"}]),
 L("hero", "Why is he typing so *long*?", RN, [c("hero", .5, pose="phone", expr="scared", scale=2.1)], camera=CU),
 L(N, "Rule number two. Change the subject. *Fast*.", RN, [c("hero", .5, pose="point", expr="angry", scale=1.6)], ui=rule(2, "CHANGE THE SUBJECT")),
 L("hero", "Bit, send something *cute*!", RN, [c("hero", .3, pose="point", expr="scared", scale=1.5), c("bit", .74, expr="happy", scale=.9)]),
 L("bit", "Sending the cutest puppy on *Earth*.", phone([MEME, DOG]), [], sfx=[{"type": "pop"}]),
 L(N, "And then, just in case, his own *selfie*.", phone([MEME, DOG, BITPIC]), [], camera={"zoom": 1.1, "y": .5}, sfx=[{"type": "pop"}]),
 L(N, "Rule number three. Never let your AI *help*.", RN, [c("bit", .5, expr="smug", scale=1.6)], ui=rule(3, "NO AI HELP")),
 L(N, "The boss *replies*.", phone([MEME, DOG, BITPIC, R1]), [], sfx=[{"type": "ding"}]),
 L("hero", "He likes the dog. We're *saved*!", RN, [c("hero", .5, pose="cheer", expr="grin", scale=1.8)], sfx=[{"type": "powerup"}]),
 L(N, "One more message.", phone([DOG, BITPIC, R1, R2]), [], camera=PUSH, sfx=[{"type": "ding"}, {"type": "hit", "at": .5}]),
 L(N, "You type. You delete. You *type*.", phone([BITPIC, R1, R2], draft="it's about my other bo"), [], sfx=[{"type": "tick"}]),
 L("bit", "Done! I answered for you. Honestly.", phone([R1, R2, R3]), [], sfx=[{"type": "pop"}]),
 L(N, "Monday. Nine a.m. Your boss's *office*.", {"type": "phone", "time": "night", "screen": {"kind": "lock", "clock": "23:52", "sub": "Sunday", "notes": [{"app": "WORK CHAT", "text": "Boss: My office. Monday. 9 a.m."}]}}, [], camera=SHAKE, sfx=[{"type": "boom"}]),
 L(N, "He wants the meme. On a *T-shirt*.", RD, [c("boss", .32, pose="cheer", expr="grin", scale=1.4, facing=1), c("hero", .72, pose="shrug", expr="shocked", scale=1.4, facing=-1)], ui={"type": "card", "text": "NEW TEAM SHIRT", "sub": "\"QUICK 5 MIN CALL\"", "color": "#2F7BFF"}, sfx=[{"type": "ding"}]),
 {"speaker": N, "say": "Follow for a new What if every day.", "end": True},
]

series = {
 "title": "What If Your Boss Meme Hit the Work Chat?",
 "rubric": "what-if: comedy (everyday cringe)", "mood": "warm", "seed": 6200, "standalone": True,
 "names": {"hero": "JAY", "bit": "BIT", "boss": "MR. BRANT"},
 "finale": {"text": "THE END", "sub": "Follow for a new What if every day"},
 "parts": [{"title": "Wrong Chat", "lines": lines}],
}
(D / "series.json").write_text(json.dumps(series, indent=1, ensure_ascii=False) + "\n")

meta = {"part1": {
    "title": "What If Your Boss Meme Hit the Work Chat? 😬 #shorts", "short": True,
    "description": "You meant to send a boss meme to your friends. It went to the work chat. 48 people. Including the boss.\nAn original animated \"What if...?\" comedy by zylo.\n\nFollow for a new \"What if...?\" every day.\n\n#whatif #relatable #funny #animation #shorts",
    "tags": ["what if", "wrong chat", "work group chat", "boss meme", "relatable", "funny animation", "cringe", "shorts"],
    "categoryId": "23", "privacy": "public", "madeForKids": False, "syntheticMedia": False}}
mp = D / "metadata.json"
if mp.exists():
    old = json.loads(mp.read_text())
    for k, v in meta.items():
        if "publishAt" in old.get(k, {}): v["publishAt"] = old[k]["publishAt"]
mp.write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")

spoken = [l for l in lines if not l.get("end")]
w = sum(len(re.sub(r"[*\"]", "", l["say"]).split()) for l in spoken)
long_ = [l["say"] for l in spoken if len(re.sub(r"[*\"]", "", l["say"]).split()) > 9]
print(f"{len(lines)} lines, {w} words", "LONG:" if long_ else "", long_ or "")
print(len(meta["part1"]["title"]), meta["part1"]["title"])
