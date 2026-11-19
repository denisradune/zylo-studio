"""Writes series.json + metadata.json for the standalone comedy Short "What if your voice message wouldn't stop recording?".
Everyday-cringe comedy (daily funny Short, owner's request 2026-11-16). Pure fiction, no real facts.
Run: python3 episodes/2026-11-19-what-if-voice-message/build_series.py"""
import json, re
from pathlib import Path
D = Path(__file__).resolve().parent

def L(sp, say, set_, cast=(), **kw):
    shot = {"set": set_ if isinstance(set_, dict) else {"type": set_}, "cast": list(cast)}
    shot.update(kw)
    return {"speaker": sp, "say": say, "shot": shot}
def c(id_, x=0.5, **kw): return {"id": id_, "x": x, **kw}
N = "narrator"
RD = {"type": "room", "time": "day"}; RK = {"type": "room", "time": "dusk"}
CU = {"zoom": 1.12, "y": 0.6}
PUSH = {"zoom": 1.08, "y": .45, "push": .1}
SHAKE = {"zoom": 1.05, "y": .55, "shake": .6}

def chat(msgs, **kw):
    return {"type": "phone", "time": "day", "screen": {"title": "BUILDING 12 🏢", "sub": "64 neighbors", "clock": "18:12", "msgs": msgs, **kw}}
SYS = lambda t: {"from": "sys", "text": t}
ME = lambda t: {"from": "me", "text": t}
def them(n): return lambda t: {"from": "them", "name": n, "text": t}
ROSE, KEV, LEE = them("Mrs. Rose (4B)"), them("Kev (5A)"), them("Building Manager")
VOICE = lambda m: ME(f"🎤 Voice message · {m}")
def rule(n, text): return {"type": "card", "text": f"RULE #{n}", "sub": text, "color": "#FF4A3D"}

lines = [
 L(N, "What if your voice message *wouldn't stop*?", chat([VOICE("4:12 ● REC")]), [], camera=PUSH, sfx=[{"type": "pop"}, {"type": "riser", "at": .4}]),
 L(N, "You hold the mic. Quick question for the *neighbors*.", chat([LEE("Water off tomorrow 9-11.")]), [], sfx=[{"type": "tick"}]),
 L("hero", "Hi, is the water off *all day*?", RD, [c("hero", .5, pose="phone", expr="happy", scale=1.7)]),
 L(N, "Then the phone slides into your *pocket*.", RD, [c("hero", .5, pose="idle", expr="neutral", scale=1.6)], sfx=[{"type": "whoosh"}]),
 L(N, "Still *recording*.", chat([VOICE("0:41 ● REC")]), [], camera={"zoom": 1.3, "y": .5}, sfx=[{"type": "hit"}]),
 L(N, "You complain about the drummer in *5A*.", RD, [c("hero", .5, pose="point", expr="angry", scale=1.8)], camera=CU),
 L(N, "You sing in the shower. Loud. *Badly*.", RK, [c("hero", .5, pose="cheer", expr="grin", scale=1.9)], fx=[{"type": "rain"}], sfx=[{"type": "ding"}]),
 L(N, "Bit narrates your *pasta*.", RK, [c("bit", .5, expr="smug", scale=1.6)], sfx=[{"type": "pop"}]),
 L(N, "You lift the phone. Nine minutes. *Sent*.", chat([VOICE("9:14")], seen="Delivered"), [], camera=SHAKE, sfx=[{"type": "boom"}]),
 L(N, "Rule number one. *Delete for everyone*.", RD, [c("hero", .5, pose="panic", expr="scared", scale=1.25)], ui=rule(1, "DELETE IT")),
 L(N, "Your thumb hits *play* instead. Volume max.", RD, [c("hero", .5, pose="phone", expr="shocked", scale=2.0)], camera=SHAKE, fx=[{"type": "speedLines"}], sfx=[{"type": "alarm"}]),
 L(N, "Played by one. Played by *nineteen*.", chat([VOICE("9:14")], seen="Played by 19"), [], sfx=[{"type": "ding"}, {"type": "ding", "at": .4}]),
 L(N, "Rule number two. Pretend you *moved out*.", RD, [c("hero", .5, pose="facepalm", expr="sad", scale=1.3)], ui=rule(2, "MOVE OUT")),
 L(N, "Rule number three. Never let your AI *help*.", RD, [c("bit", .5, expr="smug", scale=1.6)], ui=rule(3, "NO AI HELP")),
 L("bit", "I added *subtitles*. For accessibility.", chat([VOICE("9:14"), ME("📝 \"the drummer in 5A is a menace\"")]), [], sfx=[{"type": "pop"}]),
 L(N, "Then 5A starts *typing*.", chat([ME("📝 \"the drummer in 5A is a menace\"")], typing="Kev (5A) is typing"), [], camera=PUSH, sfx=[{"type": "heartbeat"}]),
 L("hero", "He's coming up. With *drumsticks*.", RD, [c("hero", .5, pose="panic", expr="scared", scale=2.1)], camera=CU),
 L(N, "Kev's message *arrives*.", chat([ME("📝 \"the drummer in 5A is a menace\""), KEV("who is singing at 3:20??")]), [], sfx=[{"type": "ding"}]),
 L(N, "Then Mrs. Rose. Then *twelve* more.", chat([KEV("who is singing at 3:20??"), ROSE("I cried. Beautiful voice.")]), [], sfx=[{"type": "ding"}, {"type": "ding", "at": .3}]),
 L(N, "Kev needs a singer. His band plays *Friday*.", chat([ROSE("I cried. Beautiful voice."), KEV("we need a singer. friday?")]), [], camera={"zoom": 1.1, "y": .5}, sfx=[{"type": "ding"}]),
 L(N, "Friday. Rooftop. Sixty-four *neighbors*.", RK, [c("friend", .2, pose="cheer", expr="grin", scale=1.0), c("hero", .5, pose="cheer", expr="grin", scale=1.2), c("kid", .8, pose="cheer", expr="happy", scale=1.0)], sfx=[{"type": "powerup"}]),
 L(N, "The band's name? *The Water Is Off*.", RK, [c("hero", .5, pose="cheer", expr="grin", scale=1.15), c("bit", .82, expr="smug", scale=.7)], ui={"type": "card", "text": "THE WATER IS OFF", "sub": "LIVE · ROOF · FRIDAY", "color": "#2F7BFF"}, sfx=[{"type": "ding"}]),
 {"speaker": N, "say": "Follow for a new What if every day.", "end": True},
]

series = {
 "title": "What If Your Voice Message Wouldn't Stop?",
 "rubric": "what-if: comedy (everyday cringe)", "mood": "warm", "seed": 6700, "standalone": True,
 "names": {"hero": "JAY", "bit": "BIT", "friend": "NEIGHBOR", "kid": "NEIGHBOR"},
 "finale": {"text": "THE END", "sub": "Follow for a new What if every day"},
 "parts": [{"title": "Voice Message", "lines": lines}],
}
(D / "series.json").write_text(json.dumps(series, indent=1, ensure_ascii=False) + "\n")

meta = {"part1": {
    "title": "What If Your Voice Message Wouldn't Stop? 🎤 #shorts", "short": True,
    "description": "One quick voice message to the neighbors' chat. Then the phone slid into your pocket. Still recording. Nine minutes.\nAn original animated \"What if...?\" comedy by zylo.\n\nFollow for a new \"What if...?\" every day.\n\n#whatif #relatable #funny #animation #shorts",
    "tags": ["what if", "voice message", "pocket recording", "neighbors group chat", "relatable", "funny animation", "cringe", "shorts"],
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
