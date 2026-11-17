"""Writes series.json + metadata.json for the standalone comedy Short "What if your mom joined the group chat?".
Everyday-cringe comedy (daily funny Short, owner's request 2026-11-16). Pure fiction, no real facts.
Run: python3 episodes/2026-11-17-what-if-mom-group-chat/build_series.py"""
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

CHAT = {"title": "THE BOYS 🔥", "sub": "Max, Leo, Sam, You", "clock": "16:20"}
def chat(msgs, **kw):
    sc = {**CHAT, **kw.pop("head", {}), "msgs": msgs, **kw}
    return {"type": "phone", "time": "day", "screen": sc}
SYS = lambda t: {"from": "sys", "text": t}
MAX = lambda t: {"from": "them", "name": "Max", "text": t}
LEO = lambda t: {"from": "them", "name": "Leo", "text": t}
MOM = lambda t: {"from": "them", "name": "Mom ❤️", "text": t}
ME = lambda t: {"from": "me", "text": t}
PLAN = MAX("party at mine friday 9pm")
LIE = ME("cant wait. told mom im studying lol")
ADDED = SYS("Bit added Mom ❤️ to the chat")
def rule(n, text): return {"type": "card", "text": f"RULE #{n}", "sub": text, "color": "#FF4A3D"}
HEAD4 = {"sub": "Max, Leo, Sam, Mom ❤️, You"}

lines = [
 L(N, "What if your mom joined the *group chat*?", chat([PLAN, LIE, ADDED], head=HEAD4), [], camera=PUSH, sfx=[{"type": "pop"}, {"type": "riser", "at": .4}]),
 L("hero", "Bit, add *Max* to the new chat.", RK, [c("hero", .3, pose="phone", expr="happy", scale=1.5), c("bit", .74, expr="happy", scale=.9)]),
 L(N, "Bit scrolls your contacts. *M*.", {"type": "phone", "time": "day", "screen": {"kind": "lock", "clock": "16:19", "sub": "Contacts: M", "notes": [{"app": "CONTACTS", "text": "Max"}, {"app": "CONTACTS", "text": "Mom ❤️"}]}}, [], sfx=[{"type": "tick"}]),
 L("bit", "Done! I picked the one with a *heart*.", RK, [c("bit", .5, expr="smug", scale=1.7)], sfx=[{"type": "ding"}]),
 L(N, "Mom is in the chat. With *everything*.", chat([PLAN, LIE, ADDED], head=HEAD4), [], camera={"zoom": 1.3, "y": .55}, sfx=[{"type": "hit"}]),
 L(N, "Including the word *studying*.", chat([PLAN, LIE], head=HEAD4), [], camera={"zoom": 1.45, "y": .5}, ui={"type": "stamp", "text": "LIAR"}, sfx=[{"type": "boom"}]),
 L(N, "Rule number one. Remove her *before she reads*.", RK, [c("hero", .5, pose="phone", expr="scared", scale=1.6)], ui=rule(1, "REMOVE MOM")),
 L(N, "Only admins can remove members. The admin is *Max*.", chat([LIE, ADDED, ME("max remove my mom NOW")], head=HEAD4), [], sfx=[{"type": "pop"}]),
 L(N, "Max is at *football practice*.", RD, [c("hero", .5, pose="panic", expr="scared", scale=2.0)], camera=SHAKE, sfx=[{"type": "alarm"}], fx=[{"type": "speedLines"}]),
 L(N, "Then three dots. Mom is *typing*.", chat([LIE, ADDED], head=HEAD4, typing="Mom ❤️ is typing"), [], camera=PUSH, sfx=[{"type": "heartbeat"}]),
 L(N, "Rule number two. *Act normal*.", RK, [c("hero", .5, pose="idle", expr="grin", scale=1.6)], ui=rule(2, "ACT NORMAL")),
 L(N, "You send a photo of a *math book*.", chat([ADDED, ME("studying hard 📚📚📚")], head=HEAD4), [], sfx=[{"type": "pop"}]),
 L(N, "Upside down. In the *dark*.", RK, [c("hero", .5, pose="facepalm", expr="sad", scale=1.8)], camera=CU),
 L(N, "Mom's message finally *arrives*.", chat([ME("studying hard 📚📚📚"), MOM("Hello boys! This is Jay's mom.")], head=HEAD4), [], sfx=[{"type": "ding"}]),
 L(N, "And another one. And *another*.", chat([MOM("Hello boys! This is Jay's mom."), MOM("Party Friday? How fun!"), MOM("What snacks do you like?")], head=HEAD4), [], camera={"zoom": 1.06, "y": .5}, sfx=[{"type": "ding"}, {"type": "ding", "at": .3}, {"type": "ding", "at": .6}]),
 L(N, "Rule number three. Never let your AI *help*.", RK, [c("bit", .5, expr="smug", scale=1.6)], ui=rule(3, "NO AI HELP")),
 L("bit", "I told her you like *mini pizzas*.", chat([MOM("What snacks do you like?"), ME("mini pizzas pls"), LEO("MINI PIZZAS 🍕🍕")], head=HEAD4), [], sfx=[{"type": "pop"}]),
 L(N, "Leo hearts it. Then *Sam*.", chat([ME("mini pizzas pls"), LEO("MINI PIZZAS 🍕🍕"), {"from": "them", "name": "Sam", "text": "jay's mom is a legend"}], head=HEAD4), [], sfx=[{"type": "ding"}]),
 L("hero", "Wait. Is this... *working*?", RK, [c("hero", .5, pose="shrug", expr="happy", scale=1.9)], camera=CU),
 L(N, "Max is back. He reads everything. He *acts*.", chat([LEO("MINI PIZZAS 🍕🍕"), SYS("Max made Mom ❤️ an admin")], head=HEAD4), [], camera=PUSH, sfx=[{"type": "ding"}, {"type": "hit", "at": .5}]),
 L(N, "The new admin's first move? She *renames* the chat.", chat([SYS("Max made Mom ❤️ an admin"), SYS("Mom ❤️ renamed the chat: MOM'S BOYS 🍕")], head={"title": "MOM'S BOYS 🍕", "sub": "Max, Leo, Sam, Mom ❤️, You"}), [], sfx=[{"type": "pop"}]),
 L(N, "Her second move: *you*.", chat([SYS("Mom ❤️ renamed the chat: MOM'S BOYS 🍕"), SYS("Mom ❤️ removed You")], head={"title": "MOM'S BOYS 🍕", "sub": "Max, Leo, Sam, Mom ❤️"}), [], camera=SHAKE, sfx=[{"type": "boom"}], ui={"type": "stamp", "text": "REMOVED"}),
 L(N, "Friday. The party is at your house. You're *studying*.", RD, [c("mom", .3, pose="cheer", expr="grin", scale=1.3, facing=1), c("hero", .72, pose="sit", expr="sad", scale=1.3, facing=-1)], ui={"type": "card", "text": "FRIDAY 9 PM", "sub": "MINI PIZZAS: 0 FOR JAY", "color": "#2F7BFF"}, sfx=[{"type": "ding"}]),
 {"speaker": N, "say": "Follow for a new What if every day.", "end": True},
]

series = {
 "title": "What If Your Mom Joined the Group Chat?",
 "rubric": "what-if: comedy (everyday cringe)", "mood": "warm", "seed": 6400, "standalone": True,
 "names": {"hero": "JAY", "bit": "BIT", "mom": "MOM"},
 "finale": {"text": "THE END", "sub": "Follow for a new What if every day"},
 "parts": [{"title": "Mom Joined", "lines": lines}],
}
(D / "series.json").write_text(json.dumps(series, indent=1, ensure_ascii=False) + "\n")

meta = {"part1": {
    "title": "What If Your Mom Joined the Group Chat? 😳 #shorts", "short": True,
    "description": "Your AI added Mom to the group chat instead of Max. The chat where you planned Friday's party. The one where you said you're studying.\nAn original animated \"What if...?\" comedy by zylo.\n\nFollow for a new \"What if...?\" every day.\n\n#whatif #relatable #funny #animation #shorts",
    "tags": ["what if", "mom in the group chat", "group chat", "relatable", "funny animation", "cringe", "shorts"],
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
