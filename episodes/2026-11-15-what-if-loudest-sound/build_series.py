"""Writes series.json + metadata.json + full/thumb.json for "What if the loudest sound in history happened today?" (8 parts).
Real basis: the 1883 eruption of Krakatoa and British Airways Flight 9 (1982), see sources.md.
Run: python3 episodes/2026-11-15-what-if-loudest-sound/build_series.py"""
import json, re
from pathlib import Path
D = Path(__file__).resolve().parent

def L(sp, say, set_, cast=(), **kw):
    shot = {"set": set_ if isinstance(set_, dict) else {"type": set_}, "cast": list(cast)}
    shot.update(kw)
    return {"speaker": sp, "say": say, "shot": shot}
def c(id_, x=0.5, **kw): return {"id": id_, "x": x, **kw}
N = "narrator"
SD = {"type": "street", "time": "day"}; SK = {"type": "street", "time": "dusk"}; SN = {"type": "street", "time": "night"}
SR = {"type": "street", "time": "red"}
RD = {"type": "room", "time": "day"}; RN = {"type": "room", "time": "night"}; RR = {"type": "room", "time": "red"}
LAB = {"type": "lab"}; SPACE = {"type": "space"}
SKY = {"type": "sky", "time": "day"}; SKYR = {"type": "sky", "time": "red"}; SKYN = {"type": "sky", "time": "night"}
HB = {"type": "harbor", "time": "day"}; HB1 = {"type": "harbor", "time": "day", "damage": 1}
HB2 = {"type": "harbor", "time": "day", "damage": 2}; HBR = {"type": "harbor", "time": "red"}
def news(h): return {"type": "news", "headline": h}
CU = {"zoom": 1.1, "y": 0.6}
PUSH = {"zoom": 1.15, "y": .5, "push": .12}
SHAKE = {"zoom": 1.05, "y": .55, "shake": .6}
CLIFF = [{"type": "riser"}, {"type": "hit", "at": .9}]
BOOM = [{"type": "boom"}, {"type": "crash", "at": .2}]
def end(t): return {"speaker": N, "say": t, "end": True}
def recap(t, set_, cast, **kw):
    l = L(N, t, set_, cast, **kw); l["shortOnly"] = True; return l
def town(expr="neutral", pose="idle"):
    return [c("kid", .15, pose=pose, expr=expr, depth=.5), c("friend", .38, pose=pose, expr=expr, depth=.6),
            c("boss", .62, pose="idle", expr=expr, depth=.6), c("scientist", .85, pose=pose, expr=expr, depth=.5)]
def eta(h): return {"type": "clock", "text": h, "color": "#FF6B4A"}
def alt(a, b): return {"type": "counter", "from": a, "to": b, "label": "FLIGHT 212 · FEET"}
GLOW = [{"type": "glow", "x": 540, "y": 900, "r": 320}]
VIG = [{"type": "vignette"}]

p1 = [
 L(N, "What if the *loudest sound* in history happened today?", SD, town("shocked"), fx=[{"type": "impact", "x": 540, "y": 700, "at": .3}], sfx=BOOM, camera=SHAKE),
 L(N, "Saturday, seven a.m. Every window in town *rattles*.", RD, [c("hero", .5, pose="panic", expr="shocked", scale=1.6)], camera=SHAKE, sfx=[{"type": "boom", "at": .1}]),
 L(N, "Jay falls out of *bed*.", RD, [c("hero", .5, pose="sit", expr="scared", scale=1.8)], camera=CU),
 L(N, "Outside, the whole street is staring at the *sky*.", SD, town("scared")),
 L(N, "No smoke. No fire. Just a *boom*.", SKY, [c("hero", .5, pose="shrug", expr="scared", scale=1.3)]),
 L("boss", "Fireworks! Who did this? Was it *you*, Jay?", SD, [c("boss", .5, pose="point", expr="angry", scale=1.9)], camera=CU),
 L("hero", "I was *asleep*!", SD, [c("hero", .5, pose="shrug", expr="angry", scale=1.9)], camera=CU),
 L("bit", "It wasn't fireworks. It was a *volcano*.", LAB, [c("bit", .5, expr="shocked", scale=1.8)], transition="whip", sfx=[{"type": "ding"}]),
 L("hero", "We don't *have* a volcano.", SD, [c("hero", .5, pose="idle", expr="shocked", scale=1.9)], camera=CU),
 L("bit", "An island. Three thousand miles *away*.", SPACE, [c("bit", .78, expr="think", scale=.9)], ui={"type": "map", "label": "3,000 MILES"}),
 L("bit", "The sound took almost four hours to *get here*.", LAB, [c("bit", .5, expr="neutral", scale=1.7)], ui={"type": "counter", "from": 0, "to": 3.9, "suffix": " h", "label": "SOUND TRAVEL TIME"}),
 L("hero", "Nothing is *that* loud.", SD, [c("hero", .5, pose="idle", expr="smug", scale=1.9)], camera=CU),
 L("bit", "One thing was. *Krakatoa*. Eighteen eighty three.", news("REAL: KRAKATOA, 1883"), [c("bit", .8, expr="smug", scale=.9)], transition="whip"),
 L("bit", "The loudest sound ever *recorded*.", news("LOUDEST SOUND EVER"), [c("bit", .8, expr="shocked", scale=.9)], sfx=[{"type": "boom"}]),
 L("bit", "People heard it three thousand miles away.", LAB, [c("bit", .5, expr="think", scale=1.7)], ui={"type": "card", "text": "4,800 KM", "sub": "heard on Rodrigues island", "color": "#FFD400"}),
 L("bit", "They thought it was a ship firing *cannons*.", LAB, [c("bit", .5, expr="smug", scale=1.7)], sfx=[{"type": "boom", "volume": 0.5}]),
 L("bit", "Sailors forty miles away lost their *eardrums*.", news("1883: EARDRUMS BURST"), [c("bit", .8, expr="sad", scale=.9)]),
 L(N, "Grandpa Ezra steps out, holding a brass *barometer*.", SD, [c("scientist", .5, pose="idle", expr="neutral", scale=1.6)]),
 L("scientist", "The needle *jumped*. Air doesn't do that.", SD, [c("scientist", .5, pose="point", expr="shocked", scale=1.9)], camera=CU),
 L("bit", "That's the air wave. It's going around the *planet*.", SPACE, [c("bit", .5, expr="think", scale=1.6)]),
 L("bit", "And it's coming back. From the *other side*.", SPACE, [c("bit", .5, expr="shocked", scale=2.0)], camera=PUSH, sfx=CLIFF),
 end("Part two drops in two days."),
]
p2 = [
 recap("Part two. A volcanic boom is circling the *Earth*.", SPACE, [c("bit", .5, expr="shocked", scale=1.6)], sfx=[{"type": "boom"}]),
 L("hero", "Coming back? A sound can't come *back*.", SD, [c("hero", .5, pose="shrug", expr="scared", scale=1.9)], camera=CU),
 L("bit", "This one can. It's a pressure wave. A *ripple*.", SPACE, [c("bit", .5, expr="think", scale=1.7)]),
 L("bit", "In 1883, it circled Earth over *three times*.", news("REAL: 3+ LAPS"), [c("bit", .8, expr="smug", scale=.9)], transition="whip"),
 L("bit", "Barometers caught it seven times. Over *five days*.", LAB, [c("bit", .5, expr="neutral", scale=1.7)], ui={"type": "counter", "from": 0, "to": 7, "label": "TIMES RECORDED"}),
 L(N, "Ezra sets the barometer on his *porch*.", SD, [c("scientist", .5, pose="sit", expr="happy", scale=1.6)]),
 L("scientist", "Then we *wait*. And we count.", SD, [c("scientist", .5, pose="point", expr="smug", scale=1.9)], camera=CU),
 L(N, "Milo grabs a pencil and makes a *chart*.", SD, [c("kid", .5, pose="point", expr="grin", scale=1.6)], ui={"type": "list", "title": "BOOM LAPS", "items": ["lap 1: 7:00 a.m."]}),
 L(N, "Mayor Doyle calls a press *conference*.", news("MAYOR: STAY CALM"), [c("boss", .8, pose="wave", expr="smug", scale=.9)]),
 L("boss", "It was a loud noise. It is *over*.", SK, [c("boss", .5, pose="point", expr="smug", scale=1.9)], camera=CU),
 L(N, "Nia isn't listening. She's staring at her *phone*.", SK, [c("friend", .5, pose="phone", expr="sad", scale=1.7)]),
 L("friend", "My mom flies home *tomorrow*. Over that ocean.", SK, [c("friend", .5, pose="phone", expr="scared", scale=1.9)], camera=CU),
 L("hero", "Bit? Is that *safe*?", SK, [c("hero", .5, pose="idle", expr="scared", scale=1.9)], camera=CU),
 L("bit", "The airlines are watching the ash. For *now*, yes.", SK, [c("bit", .5, expr="neutral", scale=1.6)]),
 L(N, "Midnight. Ezra's needle twitches. *Again*.", SN, [c("scientist", .5, pose="idle", expr="shocked", scale=1.7)], ui=eta("00:00"), sfx=[{"type": "tick"}]),
 L("kid", "Lap two! The boom went all the way *around*!", SN, [c("kid", .5, pose="cheer", expr="grin", scale=1.9)], camera=CU, sfx=[{"type": "ding"}]),
 L(N, "The whole street cheers. For a *sound*.", SN, town("grin", "cheer")),
 L(N, "But Bit is watching something *else*.", RN, [c("bit", .5, expr="think", scale=1.8)], fx=VIG),
 L("bit", "Jay. The harbor gauge just *moved*.", RN, [c("bit", .5, expr="shocked", scale=1.8)], camera=CU),
 L("bit", "In 1883, the sea felt it. Even in *England*.", news("1883: WAVES REACH UK"), [c("bit", .8, expr="sad", scale=.9)]),
 L("bit", "A wave is crossing the ocean. Landing at *noon*.", HB, [c("bit", .5, expr="shocked", scale=2.0)], camera=PUSH, sfx=CLIFF),
 end("Part three drops in two days."),
]
p3 = [
 recap("Part three. A wave hits the harbor at *noon*.", HB, [c("bit", .5, expr="shocked", scale=1.6)], sfx=[{"type": "hit"}]),
 L("hero", "A *tsunami*? Here?", RD, [c("hero", .5, pose="panic", expr="shocked", scale=1.9)], camera=CU),
 L("bit", "A small one. After that far, maybe *one meter*.", HB, [c("bit", .78, expr="think", scale=.9)], ui={"type": "counter", "from": 0, "to": 1, "suffix": " m", "label": "EXPECTED WAVE"}),
 L("hero", "One meter. That's my *waist*. That's nothing.", RD, [c("hero", .5, pose="shrug", expr="smug", scale=1.9)], camera=CU),
 L("bit", "A meter of moving sea can tip a *truck*.", HB, [c("bit", .5, expr="angry", scale=1.8)], sfx=[{"type": "crash"}]),
 L(N, "Eight a.m. Jay runs to the *mayor*.", SD, [c("hero", .5, pose="run", expr="angry", scale=1.4)], fx=[{"type": "speedLines"}], ui=eta("04:00"), transition="whip"),
 L("boss", "Close the fish market? On a *Saturday*?", SD, [c("boss", .5, pose="shrug", expr="smug", scale=1.9)], camera=CU),
 L("boss", "A wave from a volcano we can't even *see*?", SD, [c("boss", .5, pose="point", expr="grin", scale=1.9)]),
 L(N, "Ezra taps his barometer. *Lap three*.", SD, [c("scientist", .5, pose="point", expr="angry", scale=1.7)], sfx=[{"type": "tick"}]),
 L("scientist", "You couldn't see it either. But you *heard* it.", SD, [c("scientist", .5, pose="point", expr="angry", scale=1.9)], camera=CU),
 L(N, "The mayor doesn't *answer*.", SD, [c("boss", .5, pose="idle", expr="sad", scale=1.7)], sfx=[{"type": "tick"}]),
 L(N, "Eleven a.m. The harbor is *packed*.", HB, town("happy"), ui=eta("01:00")),
 L(N, "Fish stalls. Tourists. Boats coming in with the *catch*.", HB, [c("friend", .3, pose="idle", expr="happy", scale=1.1), c("boss", .72, pose="wave", expr="grin", scale=1.1)]),
 L(N, "And at the very end of the pier, *Milo*.", HB, [c("kid", .5, pose="sit", expr="grin", scale=1.5)]),
 L(N, "Fishing rod. Headphones. *Very* loud headphones.", HB, [c("kid", .5, pose="sit", expr="happy", scale=1.9)], camera=CU),
 L("friend", "Milo! MILO! He can't *hear* me.", HB, [c("friend", .5, pose="point", expr="scared", scale=1.9)], camera=CU),
 L(N, "Jay starts down the *pier*.", HB, [c("hero", .5, pose="walk", expr="scared", scale=1.5)]),
 L(N, "Eleven forty. Then the water does something *strange*.", HB, [c("hero", .5, pose="idle", expr="shocked", scale=1.5)], ui=eta("00:20"), sfx=[{"type": "heartbeat"}]),
 L(N, "It starts to *leave*.", HB1, [], sfx=[{"type": "whoosh"}], transition="flash"),
 L(N, "The whole harbor drains. Boats sit on *sand*.", HB1, [c("hero", .5, pose="idle", expr="shocked", scale=1.4)]),
 L(N, "And the crowd walks *out* to grab the fish.", HB1, town("grin", "walk"), camera=PUSH, sfx=CLIFF),
 end("Part four drops in two days."),
]
p4 = [
 recap("Part four. The sea pulled back. People walked *in*.", HB1, town("grin"), sfx=[{"type": "hit"}]),
 L("hero", "No! Get out of there! That's the *wave*!", HB1, [c("hero", .5, pose="point", expr="angry", scale=1.9)], camera=CU),
 L(N, "Bit taught him. When the sea leaves, it *returns*.", RD, [c("bit", .5, expr="angry", scale=1.6)]),
 L(N, "Nobody listens. Mayor Doyle holds up a *fish*.", HB1, [c("boss", .5, pose="cheer", expr="grin", scale=1.7)], sfx=[{"type": "pop"}]),
 L("boss", "Free lunch, everybody!", HB1, [c("boss", .5, pose="cheer", expr="grin", scale=1.9)], camera=CU),
 L(N, "Jay sees the old harbor *bell*.", HB1, [c("hero", .5, pose="point", expr="angry", scale=1.6)], ui={"type": "card", "text": "HARBOR BELL", "sub": "storm warning · since 1902", "color": "#C9A227"}),
 L(N, "He grabs the rope. And *pulls*.", HB1, [c("hero", .5, pose="throw", expr="angry", scale=1.9)], camera=SHAKE, sfx=[{"type": "ring"}, {"type": "ring", "at": .5}]),
 L(N, "Clang! Clang! *Clang*!", HB1, town("shocked"), sfx=[{"type": "ring"}, {"type": "ring", "at": .3}, {"type": "ring", "at": .6}]),
 L("scientist", "That bell means *run*! Up the hill! Now!", HB1, [c("scientist", .5, pose="point", expr="angry", scale=1.9)], camera=CU),
 L(N, "The old folks know that bell. They *run*.", HB1, town("scared", "run"), fx=[{"type": "speedLines"}], sfx=[{"type": "whoosh"}]),
 L(N, "Then everyone runs. Fish and *all*.", SD, town("scared", "run"), fx=[{"type": "speedLines"}]),
 L(N, "But Milo still has his *headphones* on.", HB1, [c("kid", .5, pose="sit", expr="happy", scale=1.6)]),
 L(N, "Jay sprints to the end of the *pier*.", HB1, [c("hero", .5, pose="run", expr="angry", scale=1.6)], fx=[{"type": "speedLines"}], camera=CU),
 L(N, "On the horizon, a gray line. *Growing*.", HB1, [], sfx=[{"type": "growl"}], camera={"zoom": 1.2, "y": .55, "push": .1}),
 L(N, "Jay yanks off the headphones. Milo *yelps*.", HB1, [c("hero", .35, pose="point", expr="angry", scale=1.2), c("kid", .7, pose="panic", expr="shocked", scale=1.1)], sfx=[{"type": "pop"}]),
 L("hero", "Don't ask. *Run*.", HB1, [c("hero", .5, pose="run", expr="angry", scale=1.9)], camera=CU),
 L(N, "They hit the hill steps as the water *arrives*.", HB2, [c("hero", .3, pose="run", expr="scared", scale=1.1), c("kid", .6, pose="run", expr="scared", scale=1.0)], sfx=[{"type": "crash"}, {"type": "whoosh", "at": .2}], camera=SHAKE),
 L(N, "Not a wall. A *fast, rising tide*.", HB2, [], sfx=[{"type": "whoosh"}]),
 L(N, "It floods the pier. It flips the fish *stalls*.", HB2, [], fx=[{"type": "impact", "x": 540, "y": 1300, "at": .3}], sfx=[{"type": "crash"}]),
 L(N, "From the hill, the whole town *watches*. Safe.", SKY, town("shocked")),
 L("boss", "I'll... buy that bell a new *rope*.", SD, [c("boss", .5, pose="facepalm", expr="sad", scale=1.9)], camera=CU),
 L("bit", "Jay. That was the small part. Look *up*.", SKYR, [c("bit", .5, expr="shocked", scale=1.9)], camera=PUSH, sfx=CLIFF),
 end("Part five drops in two days."),
]
p5 = [
 recap("Part five. The town is safe. The sky *isn't*.", SKYR, [c("bit", .5, expr="shocked", scale=1.6)], sfx=[{"type": "hit"}]),
 L(N, "Seven p.m. The sunset turns *blood red*.", SKYR, [], transition="flash", sfx=[{"type": "riser"}]),
 L(N, "Not orange. Not pink. *Red*. Like it's burning.", SR, town("shocked")),
 L(N, "Somebody calls the fire *department*.", SR, [c("boss", .5, pose="phone", expr="scared", scale=1.7)], sfx=[{"type": "ring"}]),
 L(N, "Three fire trucks race up the hill. Sirens *screaming*.", SR, [c("hero", .5, pose="idle", expr="shocked", scale=1.4)], fx=[{"type": "alarm"}], sfx=[{"type": "siren"}]),
 L(N, "There's no fire. There's *ash*.", SKYR, [c("bit", .78, expr="think", scale=.9)]),
 L("bit", "Volcanic ash, high in the sky. Bending the *sunlight*.", SKYR, [c("bit", .5, expr="think", scale=1.7)]),
 L("bit", "Krakatoa threw ash about fifty miles *up*.", news("REAL: ASH 80 KM HIGH"), [c("bit", .8, expr="shocked", scale=.9)], transition="whip"),
 L("bit", "Sunsets went red all over the world. For *months*.", SKYR, [c("bit", .5, expr="happy", scale=1.6)]),
 L("bit", "New York called out fire engines. *Real* story.", news("1883: FIRE ENGINES SENT"), [c("bit", .8, expr="smug", scale=.9)], sfx=[{"type": "siren", "volume": 0.4}]),
 L("hero", "So the mayor did it *twice*. Once in history.", SR, [c("hero", .5, pose="point", expr="grin", scale=1.9)], camera=CU),
 L("boss", "I heard that.", SR, [c("boss", .5, pose="idle", expr="angry", scale=1.9)], camera=CU),
 L(N, "Everyone laughs. Except *Nia*.", SR, [c("friend", .5, pose="phone", expr="sad", scale=1.7)], sfx=[{"type": "heartbeat"}]),
 L("friend", "Mom's flight left early. To beat the *ash*.", SR, [c("friend", .5, pose="phone", expr="scared", scale=1.9)], camera=CU),
 L(N, "Flight two-twelve. Over the ocean. *Right now*.", SKYN, [], ui={"type": "card", "text": "FLIGHT 212", "sub": "over the ocean · 36,000 ft", "color": "#FFD400"}),
 L("hero", "Bit. Can you see her *plane*?", RN, [c("hero", .5, pose="phone", expr="scared", scale=1.9)], camera=CU),
 L("bit", "Tracking. Thirty six thousand feet. *Steady*.", RN, [c("bit", .5, expr="neutral", scale=1.7)], ui={"type": "bars", "items": [{"label": "SIGNAL", "value": 0.9, "color": "#2DBE7E"}], "tag": "FLIGHT 212"}),
 L(N, "Nia breathes out. Milo falls asleep on her *shoulder*.", RN, [c("friend", .4, pose="sit", expr="sad", scale=1.3), c("kid", .62, pose="sit", expr="sleepy", scale=1.1)]),
 L(N, "Eleven p.m. Bit's screen flickers *orange*.", RN, [c("bit", .5, expr="glitch", scale=1.8)], fx=[{"type": "glitch"}], sfx=[{"type": "alarm"}]),
 L("bit", "The ash cloud moved. It's *in her path*.", RN, [c("bit", .5, expr="shocked", scale=1.9)], camera=CU),
 L("bit", "Flight two-twelve is *descending*. Fast.", RN, [c("bit", .5, expr="shocked", scale=2.0)], ui=alt(36000, 31000), camera=PUSH, sfx=CLIFF),
 end("Part six drops in two days."),
]
p6 = [
 recap("Part six. Nia's mom's plane flew into *volcanic ash*.", RN, [c("friend", .5, pose="phone", expr="scared", scale=1.6)], sfx=[{"type": "hit"}]),
 L("friend", "Why is it going *down*?", RN, [c("friend", .5, pose="panic", expr="scared", scale=1.9)], camera=CU),
 L("bit", "Ash melts inside jet engines. Engines can *stop*.", RN, [c("bit", .5, expr="sad", scale=1.7)], ui=alt(31000, 26000)),
 L(N, "Nobody says anything. The room is *silent*.", RN, town("scared"), fx=VIG, sfx=[{"type": "heartbeat"}]),
 L("bit", "Nia. Listen. This happened *before*. In 1982.", news("REAL: FLIGHT 9, 1982"), [c("bit", .8, expr="neutral", scale=.9)], transition="whip"),
 L("bit", "A jumbo jet flew into volcanic ash at *night*.", SKYN, [c("bit", .78, expr="think", scale=.9)]),
 L("bit", "All *four* engines stopped.", SKYN, [c("bit", .5, expr="shocked", scale=1.8)], ui={"type": "card", "text": "ENGINES 0 / 4", "sub": "British Airways Flight 9", "color": "#E0312B"}, sfx=[{"type": "powerdown"}]),
 L("bit", "The captain said: we have a small *problem*.", RN, [c("bit", .5, expr="smug", scale=1.7)], camera=CU),
 L("hero", "A *small* problem?", RN, [c("hero", .5, pose="shrug", expr="shocked", scale=1.9)], camera=CU),
 L("bit", "The plane glided. Down, out of the *ash*.", SKYN, [c("bit", .5, expr="neutral", scale=1.6)], ui={"type": "counter", "from": 37000, "to": 12000, "label": "FLIGHT 9 · FEET"}),
 L("bit", "In clean air, the engines started *again*.", SKYN, [c("bit", .5, expr="happy", scale=1.7)], sfx=[{"type": "powerup"}]),
 L("bit", "Everyone on board *lived*. Two hundred sixty three.", news("1982: ALL 263 SURVIVE"), [c("bit", .8, expr="happy", scale=.9)], sfx=[{"type": "ding"}]),
 L(N, "Nia holds onto that like a *rope*.", RN, [c("friend", .5, pose="sit", expr="sad", scale=1.8)], camera=CU),
 L("friend", "So they *glide*. And it works.", RN, [c("friend", .5, pose="idle", expr="neutral", scale=1.9)], camera=CU),
 L("bit", "Twenty thousand feet. Still *dropping*.", RN, [c("bit", .5, expr="neutral", scale=1.7)], ui=alt(26000, 20000)),
 L(N, "Ezra comes in with an old radio *scanner*.", RN, [c("scientist", .5, pose="walk", expr="neutral", scale=1.6)], sfx=[{"type": "knock"}]),
 L("scientist", "Air traffic channels. Let's *listen*.", RN, [c("scientist", .5, pose="sit", expr="neutral", scale=1.8)], fx=[{"type": "glitch"}], sfx=[{"type": "buzz"}]),
 L(N, "Static. Then a calm *voice*.", RN, [c("hero", .5, pose="idle", expr="scared", scale=1.8)], sfx=[{"type": "buzz"}]),
 L(N, "Two-twelve, engines out, *gliding*.", RN, [c("bit", .5, expr="sad", scale=1.8)], fx=[{"type": "glitch"}]),
 L(N, "Nia grabs Jay's hand. He *doesn't* let go.", RN, [c("hero", .4, pose="sit", expr="sad", scale=1.3), c("friend", .62, pose="sit", expr="scared", scale=1.3)], camera=CU),
 L("bit", "Fifteen thousand. Then the signal *stops*.", RN, [c("bit", .5, expr="off", scale=2.0)], ui=alt(20000, 15000), camera=PUSH, sfx=CLIFF),
 end("Part seven drops in two days."),
]
p7 = [
 recap("Part seven. The plane is gliding. Signal *gone*.", RN, [c("bit", .5, expr="glitch", scale=1.6)], sfx=[{"type": "hit"}]),
 L("friend", "Bit? *Bit*! Where is she?", RN, [c("friend", .5, pose="panic", expr="scared", scale=1.9)], camera=CU),
 L("bit", "Low planes drop off my map. That's *normal*.", RN, [c("bit", .5, expr="sad", scale=1.7)]),
 L(N, "The scanner hisses. Nothing. *Nothing*.", RN, [c("scientist", .5, pose="sit", expr="sad", scale=1.6)], fx=VIG, sfx=[{"type": "buzz"}]),
 L(N, "Milo wakes up. He looks at all their *faces*.", RN, [c("kid", .5, pose="sit", expr="sleepy", scale=1.7)]),
 L("kid", "Is it Mom? Is Mom *okay*?", RN, [c("kid", .5, pose="idle", expr="scared", scale=1.9)], camera=CU),
 L(N, "Nia can't answer. So Jay *does*.", RN, [c("hero", .5, pose="sit", expr="neutral", scale=1.7)]),
 L("hero", "Her plane is gliding. Planes are *good* at gliding.", RN, [c("hero", .5, pose="point", expr="neutral", scale=1.9)], camera=CU),
 L("hero", "In 1982, a plane did this. Everyone *lived*.", RN, [c("hero", .5, pose="idle", expr="happy", scale=1.9)]),
 L("hero", "Her pilots know about ash. They *train* for it.", RN, [c("hero", .5, pose="point", expr="neutral", scale=1.9)]),
 L(N, "Jay is not sure he believes *himself*.", RN, [c("hero", .5, pose="sit", expr="sad", scale=1.9)], camera=CU, sfx=[{"type": "heartbeat"}]),
 L(N, "Three minutes. Four. *Five*.", RN, town("sad"), ui=eta("05:00"), sfx=[{"type": "tick"}, {"type": "tick", "at": .5}]),
 L(N, "Then the scanner *crackles*.", RN, [c("scientist", .5, pose="idle", expr="shocked", scale=1.8)], fx=[{"type": "glitch"}], sfx=[{"type": "buzz"}]),
 L(N, "Two-twelve. Engine one *relit*.", RN, [c("bit", .5, expr="happy", scale=1.8)], sfx=[{"type": "powerup"}], ui={"type": "card", "text": "ENGINES 1 / 4", "sub": "flight 212", "color": "#FFD400"}),
 L(N, "Engine two *relit*.", RN, [c("friend", .5, pose="idle", expr="shocked", scale=1.9)], ui={"type": "card", "text": "ENGINES 2 / 4", "sub": "flight 212", "color": "#FFD400"}, sfx=[{"type": "powerup"}]),
 L(N, "Three. *Four*.", RN, [c("friend", .5, pose="cheer", expr="grin", scale=2.0)], ui={"type": "card", "text": "ENGINES 4 / 4", "sub": "flight 212", "color": "#2DBE7E"}, sfx=[{"type": "powerup"}, {"type": "ding", "at": .5}]),
 L(N, "Jay squeezes Nia's hand. She squeezes *back*.", RN, [c("hero", .4, pose="sit", expr="happy", scale=1.3), c("friend", .62, pose="sit", expr="shocked", scale=1.3)]),
 L(N, "The room *explodes*.", RN, town("grin", "cheer"), sfx=[{"type": "pop"}, {"type": "pop", "at": .3}]),
 L("scientist", "Ha! Small problem! *Small problem*!", RN, [c("scientist", .5, pose="cheer", expr="grin", scale=1.9)], camera=CU),
 L("bit", "Signal back. Twelve thousand feet. *Climbing*.", RN, [c("bit", .5, expr="happy", scale=1.8)], ui=alt(12000, 14000)),
 L(N, "Ninety minutes later, Nia's phone *rings*.", RN, [c("friend", .5, pose="phone", expr="shocked", scale=1.8)], sfx=[{"type": "ring"}]),
 L(N, "A crackly line. A *voice*.", RN, [c("friend", .5, pose="phone", expr="scared", scale=2.0)], fx=[{"type": "glitch"}]),
 L("friend", "Mom? Mom, where *are* you?", RN, [c("friend", .5, pose="phone", expr="scared", scale=2.0)], camera=PUSH, sfx=CLIFF),
 end("Part eight drops in two days. The final part."),
]
p8 = [
 recap("Part eight. Engines back. Then Nia's phone *rang*.", RN, [c("friend", .5, pose="phone", expr="scared", scale=1.6)], sfx=[{"type": "ring"}]),
 L(N, "Mom landed at a small airport. Far from *ash*.", SKY, [], ui={"type": "card", "text": "LANDED", "sub": "flight 212 · all safe", "color": "#2DBE7E"}, sfx=[{"type": "ding"}]),
 L("friend", "She says... *we had a small problem*.", RN, [c("friend", .5, pose="phone", expr="grin", scale=1.9)], camera=CU),
 L(N, "Nia laughs and cries at the same *time*.", RN, [c("friend", .4, pose="cheer", expr="happy", scale=1.3), c("kid", .64, pose="cheer", expr="grin", scale=1.1)]),
 L(N, "Two days later, Mom's home. Milo hugs her *hard*.", SD, [c("kid", .5, pose="cheer", expr="grin", scale=1.7)], camera=CU),
 L(N, "The boom passes over town one last *time*.", SD, [c("scientist", .5, pose="point", expr="grin", scale=1.6)], sfx=[{"type": "tick"}]),
 L("kid", "Lap seven. Same as 1883! My chart was *right*!", SD, [c("kid", .5, pose="cheer", expr="grin", scale=1.9)], ui={"type": "counter", "from": 6, "to": 7, "label": "BOOM LAPS"}, camera=CU),
 L(N, "Mayor Doyle unveils a new rope for the *bell*.", HB, [c("boss", .5, pose="wave", expr="happy", scale=1.6)], ui={"type": "card", "text": "JAY'S BELL", "sub": "ring it. then run.", "color": "#C9A227"}),
 L("boss", "And a *siren*. Just in case.", HB, [c("boss", .5, pose="point", expr="smug", scale=1.9)], sfx=[{"type": "siren", "volume": 0.4}], camera=CU),
 L(N, "For weeks, every sunset stays *red*.", SKYR, []),
 L(N, "Milo paints a face *screaming* at a red sky.", RR, [c("kid", .5, pose="point", expr="grin", scale=1.6)]),
 L("bit", "Fun fact. Some think *The Scream* shows that sky.", news("REAL: THE SCREAM, 1893"), [c("bit", .8, expr="smug", scale=.9)], transition="whip"),
 L("bit", "Munch painted it ten years after *Krakatoa*.", RR, [c("bit", .5, expr="think", scale=1.7)], ui={"type": "card", "text": "1883 → 1893", "sub": "red skies over Norway", "color": "#FF6B4A"}),
 L("bit", "Next summer, the north was point four degrees *cooler*.", LAB, [c("bit", .5, expr="think", scale=1.6)], ui={"type": "counter", "from": 0, "to": 0.4, "suffix": " °C", "label": "COOLER SUMMER"}),
 L("hero", "One volcano. And the whole planet *felt* it.", SR, [c("hero", .5, pose="idle", expr="happy", scale=1.9)], camera=CU),
 L("bit", "One sound. And the whole town *listened*. Eventually.", SR, [c("bit", .5, expr="smug", scale=1.8)]),
 L(N, "That night, they all sit on the hill. *Quiet*.", SKYR, town("happy")),
 L("friend", "Jay. Thanks for *ringing* the bell.", SR, [c("friend", .5, pose="idle", expr="happy", scale=1.9)], camera=CU),
 L("hero", "Thanks for not *letting go*.", SR, [c("hero", .5, pose="idle", expr="happy", scale=1.9)], camera=CU),
 L("bit", "Can we stop having *small problems* now?", SKYR, [c("bit", .5, expr="happy", scale=1.6, lift=250)], camera=PUSH, sfx=[{"type": "ding", "at": .6}]),
 end("Follow for a new What if every day."),
]

parts = [("The Boom", p1), ("Seven Laps", p2), ("Noon", p3), ("The Bell", p4),
         ("Red Sky", p5), ("Small Problem", p6), ("Engine One", p7), ("The Scream", p8)]

series = {
 "title": "What If the Loudest Sound in History Happened Today?",
 "rubric": "what-if: disaster (real history)", "mood": "tension", "seed": 6100, "every": 2,
 "names": {"hero": "JAY", "bit": "BIT", "friend": "NIA", "boss": "MAYOR DOYLE", "scientist": "GRANDPA EZRA", "kid": "MILO"},
 "finale": {"text": "THE END", "sub": "Follow for a new What if every day"},
 "parts": [{"title": t, "lines": ls} for t, ls in parts],
}
(D / "series.json").write_text(json.dumps(series, indent=1, ensure_ascii=False) + "\n")

hooks = ["What If the Loudest Sound Ever Hit Today?", "What If a Sound Circled the Earth?", "What If the Sea Just Left?",
         "What If Nobody Heard the Warning?", "What If the Sky Turned Blood Red?", "What If All Four Engines Stopped?",
         "What If the Engines Came Back?", "What If a Volcano Painted the Sky?"]
blurbs = [
 "A boom shakes the whole town, but the volcano is 3,000 miles away. In 1883, Krakatoa made the loudest sound ever recorded.",
 "The volcano's pressure wave keeps circling the planet. In 1883, barometers recorded it seven times over five days.",
 "A small tsunami is crossing the ocean. Then the harbor drains, and the crowd walks out to grab the fish.",
 "The sea pulled back. Nobody listens to Jay, so he rings the old harbor bell.",
 "The sunset turns blood red and someone calls the fire trucks, just like New York did in 1883. Then Nia's mom's plane hits the ash.",
 "In 1982, a jumbo jet flew into volcanic ash and all four engines stopped. Nia's mom is in the same trouble.",
 "Flight 212 is gliding and the signal is gone. Then the radio crackles.",
 "Mom is home, the boom finishes lap seven, and the sunsets stay red. Some think The Scream shows a sky like that.",
]
tags = ["what if", "krakatoa", "loudest sound", "volcano", "tsunami", "volcanic ash", "animation", "story", "shorts"]
def ttl(i):
    t = f"{hooks[i]} Part {i + 1} #shorts"
    t2 = f"{hooks[i]} 🌋 Part {i + 1} #shorts"
    return t2 if len(t2) <= 60 else t
meta = {}
for i in range(8):
    meta[f"part{i + 1}"] = {
        "title": ttl(i), "short": True,
        "description": f"{blurbs[i]}\nAn original animated \"What if...?\" story by zylo, part {i + 1} of 8.\n\nFollow for a new \"What if...?\" every day.\n\n#whatif #krakatoa #volcano #animation #shorts",
        "tags": tags, "categoryId": "1", "privacy": "public", "madeForKids": False, "syntheticMedia": False}
meta["full"] = {
    "title": "What If the Loudest Sound Ever Happened Today? (Full Story)",
    "description": "In 1883, Krakatoa made the loudest sound ever recorded: heard 3,000 miles away, picked up by barometers seven times as it circled the Earth. What if it happened today?\nAn original animated \"What if...?\" story by zylo: all eight parts in one.\n\n{chapters}\nFollow for a new \"What if...?\" every day.\n\n#whatif #krakatoa #volcano #animation #story",
    "tags": [t for t in tags if t != "shorts"], "categoryId": "1", "privacy": "public", "madeForKids": False, "syntheticMedia": False}
mp = D / "metadata.json"
if mp.exists():
    old = json.loads(mp.read_text())
    for k, v in meta.items():
        if "publishAt" in old.get(k, {}): v["publishAt"] = old[k]["publishAt"]
mp.write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")

(D / "full").mkdir(exist_ok=True)
(D / "full/thumb.json").write_text(json.dumps({
 "text": "LOUDEST SOUND *EVER*", "badge": "FULL STORY", "cropY": 880, "set": {"type": "harbor", "time": "red"},
 "cast": [{"id": "friend", "x": 0.93, "pose": "panic", "expr": "scared", "scale": 1.0, "y": 1640, "facing": -1},
          {"id": "hero", "x": 0.72, "pose": "panic", "expr": "shocked", "scale": 1.3, "y": 1760},
          {"id": "bit", "x": 0.56, "expr": "shocked", "scale": 0.55, "y": 1215}]}, indent=1) + "\n")

for i, (t, ls) in enumerate(parts):
    spoken = [l for l in ls if not l.get("end")]
    w = sum(len(re.sub(r"[*\"]", "", l["say"]).split()) for l in spoken)
    long_ = [l["say"] for l in spoken if len(re.sub(r"[*\"]", "", l["say"]).split()) > 9]
    print(f"part{i + 1} {t!r}: {len(ls)} lines, {w} words", "LONG:" if long_ else "", long_ or "")
for k, v in meta.items():
    print(k, len(v["title"]), v["title"])
