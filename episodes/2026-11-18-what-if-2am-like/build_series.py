"""Writes series.json + metadata.json for the standalone comedy Short "What if you liked your crush's 2019 photo at 2 a.m.?".
Everyday-cringe comedy (daily funny Short, owner's request 2026-11-16). Pure fiction, no real facts.
Run: python3 episodes/2026-11-18-what-if-2am-like/build_series.py"""
import json, re
from pathlib import Path
D = Path(__file__).resolve().parent

def L(sp, say, set_, cast=(), **kw):
    shot = {"set": set_ if isinstance(set_, dict) else {"type": set_}, "cast": list(cast)}
    shot.update(kw)
    return {"speaker": sp, "say": say, "shot": shot}
def c(id_, x=0.5, **kw): return {"id": id_, "x": x, **kw}
N = "narrator"
N = "narrator"
RN = {"type": "room", "time": "night"}; RD = {"type": "room", "time": "day"}
CU = {"zoom": 1.12, "y": 0.6}
PUSH = {"zoom": 1.08, "y": .45, "push": .1}
SHAKE = {"zoom": 1.05, "y": .55, "shake": .6}

def chat(msgs, title="Sam", sub="last seen 1:58", **kw):
    return {"type": "phone", "time": "night", "screen": {"title": title, "sub": sub, "clock": "02:07", "msgs": msgs, **kw}}
def lock(clock, sub, notes): return {"type": "phone", "time": "night", "screen": {"kind": "lock", "clock": clock, "sub": sub, "notes": notes}}
SYS = lambda t: {"from": "sys", "text": t}
ME = lambda t: {"from": "me", "text": t}
SAM = lambda t: {"from": "them", "name": "Sam", "text": t}
NIA = lambda t: {"from": "them", "name": "Nia", "text": t}
LIKE = SYS("You liked Sam's photo · June 2019")
def nchat(msgs, **kw): return chat(msgs, title="NIA 🚨", sub="online", **kw)
def rule(n, text): return {"type": "card", "text": f"RULE #{n}", "sub": text, "color": "#FF4A3D"}

lines = [
 L(N, "What if you liked your crush's *2019 photo*?", chat([LIKE]), [], camera=PUSH, sfx=[{"type": "pop"}, {"type": "riser", "at": .4}]),
 L(N, "Two a.m. You're deep in Sam's *profile*.", RN, [c("hero", .5, pose="phone", expr="happy", scale=1.7)], ui={"type": "clock", "text": "02:06"}),
 L(N, "Scroll. Scroll. 2021. 2020. *Beach, 2019*.", RN, [c("hero", .5, pose="phone", expr="grin", scale=1.9)], camera=CU, fx=[{"type": "speedLines"}], sfx=[{"type": "whoosh"}]),
 L(N, "Your thumb slips. *Double tap*.", chat([LIKE]), [], camera={"zoom": 1.35, "y": .5}, sfx=[{"type": "hit"}]),
 L(N, "A little red *heart*.", RN, [c("hero", .5, pose="panic", expr="shocked", scale=2.0)], camera=SHAKE, ui={"type": "stamp", "text": "LIKED"}, sfx=[{"type": "boom"}]),
 L(N, "Rule number one. *Don't unlike it*.", RN, [c("hero", .5, pose="idle", expr="neutral", scale=1.6)], ui=rule(1, "DON'T UNLIKE")),
 L("hero", "Bit! Make it *disappear*!", RN, [c("hero", .3, pose="panic", expr="scared", scale=1.5), c("bit", .74, expr="shocked", scale=.9)], camera=SHAKE),
 L("bit", "Done. I unliked it. And liked it *again*.", chat([LIKE, SYS("You unliked it"), SYS("You liked Sam's photo · June 2019")]), [], sfx=[{"type": "pop"}, {"type": "pop", "at": .4}]),
 L(N, "That's *two* notifications.", lock("02:07", "Sam's phone", [{"app": "PHOTOS", "text": "Jay liked your photo from 2019"}, {"app": "PHOTOS", "text": "Jay liked your photo from 2019"}]), [], camera=PUSH, sfx=[{"type": "ding"}, {"type": "ding", "at": .4}]),
 L(N, "Rule number two. *Call backup*.", RN, [c("hero", .5, pose="phone", expr="scared", scale=1.6)], ui=rule(2, "CALL BACKUP")),
 L(N, "You text Nia. She's *awake*. Of course.", nchat([ME("I LIKED SAMS 2019 PHOTO"), NIA("the BEACH one??")]), [], sfx=[{"type": "ding"}]),
 L(N, "Nia's advice: act like *a robot did it*.", nchat([NIA("the BEACH one??"), NIA("say your AI did it lol")]), [], sfx=[{"type": "ding"}]),
 L("hero", "Wait. A robot *did* do it.", RN, [c("hero", .5, pose="shrug", expr="happy", scale=1.9)], camera=CU),
 L(N, "Rule number three. Never let your AI *help*.", RN, [c("bit", .5, expr="smug", scale=1.6)], ui=rule(3, "NO AI HELP")),
 L("bit", "Smart move. I liked her *other* photos too.", RN, [c("bit", .5, expr="happy", scale=1.7)], ui={"type": "counter", "from": 1, "to": 63, "label": "PHOTOS LIKED"}, sfx=[{"type": "ding"}, {"type": "ding", "at": .2}, {"type": "ding", "at": .4}]),
 L(N, "Sixty-three. Back to *2016*.", RN, [c("hero", .5, pose="facepalm", expr="sad", scale=2.0)], camera=SHAKE, sfx=[{"type": "alarm"}]),
 L(N, "Then Sam's dot turns *green*.", chat([LIKE], sub="online"), [], camera=PUSH, sfx=[{"type": "heartbeat"}]),
 L(N, "Sam is *typing*.", chat([LIKE], sub="online", typing="Sam is typing"), [], camera={"zoom": 1.1, "y": .5}, sfx=[{"type": "heartbeat"}]),
 L(N, "You type. You delete. You *type*.", chat([LIKE], sub="online", draft="my AI did it i swe"), [], sfx=[{"type": "tick"}]),
 L(N, "Sam's message *arrives*.", chat([LIKE, SAM("why are you up at 2am")], sub="online"), [], sfx=[{"type": "ding"}]),
 L("hero", "She's going to block me. *Forever*.", RN, [c("hero", .5, pose="panic", expr="scared", scale=2.1)], camera=CU),
 L(N, "Then a notification. From *Sam*.", lock("02:09", "Wednesday", [{"app": "PHOTOS", "text": "Sam liked your photo from 2014"}]), [], camera=SHAKE, sfx=[{"type": "boom"}]),
 L(N, "2014. The *bowl haircut*.", chat([SAM("why are you up at 2am"), SAM("ok now we're even 😂"), SAM("coffee tomorrow?")], sub="online"), [], sfx=[{"type": "ding"}, {"type": "ding", "at": .4}]),
 L(N, "Bit takes the *credit*.", RD, [c("bit", .3, expr="smug", scale=1.15), c("hero", .72, pose="cheer", expr="grin", scale=1.15, facing=-1)], ui={"type": "card", "text": "COFFEE: 10 AM", "sub": "BIT: \"YOU'RE WELCOME\"", "color": "#2F7BFF"}, sfx=[{"type": "powerup"}]),
 {"speaker": N, "say": "Follow for a new What if every day.", "end": True},
]

series = {
 "title": "What If You Liked Your Crush's 2019 Photo?",
 "rubric": "what-if: comedy (everyday cringe)", "mood": "warm", "seed": 6500, "standalone": True,
 "names": {"hero": "JAY", "bit": "BIT"},
 "finale": {"text": "THE END", "sub": "Follow for a new What if every day"},
 "parts": [{"title": "2 A.M. Like", "lines": lines}],
}
(D / "series.json").write_text(json.dumps(series, indent=1, ensure_ascii=False) + "\n")

meta = {"part1": {
    "title": "What If You Liked Your Crush's 2019 Photo? 😳 #shorts", "short": True,
    "description": "2 a.m., deep in your crush's profile, and your thumb slips on a photo from 2019. Then your AI tries to help.\nAn original animated \"What if...?\" comedy by zylo.\n\nFollow for a new \"What if...?\" every day.\n\n#whatif #relatable #funny #animation #shorts",
    "tags": ["what if", "accidentally liked old photo", "crush", "2am", "relatable", "funny animation", "cringe", "shorts"],
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
