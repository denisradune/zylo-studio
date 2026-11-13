"""Writes series.json + metadata.json + full/thumb.json for "What if a solar storm hit today?" (8 parts).
Real basis: the Carrington Event, 1-2 September 1859 (see sources.md).
Run: python3 episodes/2026-11-13-what-if-solar-storm/build_series.py"""
import json, re
from pathlib import Path
D = Path(__file__).resolve().parent

def L(sp, say, set_, cast=(), **kw):
    shot = {"set": set_ if isinstance(set_, dict) else {"type": set_}, "cast": list(cast)}
    shot.update(kw)
    return {"speaker": sp, "say": say, "shot": shot}
def c(id_, x=0.5, **kw): return {"id": id_, "x": x, **kw}
N = "narrator"
SN = {"type": "street", "time": "night"}; SK = {"type": "street", "time": "dusk"}; SD = {"type": "street", "time": "day"}
SN1 = {"type": "street", "time": "night", "damage": 1}
RN = {"type": "room", "time": "night"}; RD = {"type": "room", "time": "day"}; LAB = {"type": "lab"}
SKYN = {"type": "sky", "time": "night"}; SKYD = {"type": "sky", "time": "dusk"}; SKY = {"type": "sky", "time": "day"}
SPACE = {"type": "space"}; WS = {"type": "workshop"}; WS1 = {"type": "workshop", "damage": 1}
def news(h): return {"type": "news", "headline": h}
def burst(col): return {"type": "burst", "color": col}
AUR = [{"type": "aurora"}]
AURR = [{"type": "aurora", "colors": ["#FF3B6B", "#3DFFB0", "#C04BFF"], "strength": 0.95}]
SUN = [{"type": "glow", "x": 540, "y": 640, "r": 420}]
CU = {"zoom": 1.1, "y": 0.6}
PUSH = {"zoom": 1.15, "y": .5, "push": .12}
CLIFF = [{"type": "riser"}, {"type": "hit", "at": .9}]
def end(t): return {"speaker": N, "say": t, "end": True}
def recap(t, set_, cast, **kw):
    l = L(N, t, set_, cast, **kw); l["shortOnly"] = True; return l
def town(expr="neutral", pose="idle"):
    return [c("kid", .15, pose=pose, expr=expr, depth=.5), c("friend", .38, pose=pose, expr=expr, depth=.6),
            c("boss", .62, pose="idle", expr=expr, depth=.6), c("scientist", .85, pose=pose, expr=expr, depth=.5)]
def eta(h): return {"type": "clock", "text": h, "color": "#FF6B4A"}

p1 = [
 L(N, "What if a *solar storm* hit tonight?", SKYN, [c("hero", .3, pose="point", expr="scared", scale=1.3), c("bit", .78, expr="shocked", scale=1.0)], fx=AUR, sfx=[{"type": "riser"}, {"type": "hit", "at": .8}], camera={"push": .08}),
 L(N, "Friday, four p.m. Jay is fixing his *bike*.", SD, [c("hero", .5, pose="idle", expr="happy", scale=1.6)]),
 L(N, "Bit is watching the Sun. Bit *always* watches.", LAB, [c("bit", .5, expr="happy", scale=1.7)]),
 L(N, "Then Bit goes *quiet*.", LAB, [c("bit", .5, expr="neutral", scale=1.9)], camera=CU, sfx=[{"type": "tick"}]),
 L("bit", "Jay. The Sun just *exploded*. A little.", SPACE, [c("bit", .78, expr="shocked", scale=.9)], fx=SUN, transition="flash", sfx=[{"type": "whoosh"}]),
 L("bit", "A flare. And a cloud of *magnetic plasma*.", SPACE, [c("bit", .5, expr="think", scale=1.6)], fx=SUN, ui={"type": "card", "text": "CME", "sub": "billions of tons", "color": "#FF6B4A"}),
 L("bit", "It's coming *here*.", SPACE, [c("bit", .5, expr="shocked", scale=2.0)], fx=SUN, camera=PUSH, sfx=[{"type": "hit"}]),
 L("hero", "Okay. Is that *bad*?", SD, [c("hero", .5, pose="shrug", expr="scared", scale=1.9)], camera=CU),
 L("bit", "It happened once before. *Eighteen fifty nine*.", news("REAL: THE CARRINGTON EVENT, 1859"), [c("bit", .8, expr="smug", scale=.9)], transition="whip"),
 L("bit", "A man named Carrington *saw* the flare.", LAB, [c("bit", .78, expr="think", scale=.9)], ui={"type": "card", "text": "R. CARRINGTON", "sub": "1 Sept 1859", "color": "#FFD400"}),
 L("bit", "Seventeen and a half hours *later*, it hit.", LAB, [c("bit", .5, expr="neutral", scale=1.7)], ui={"type": "counter", "from": 0, "to": 17.6, "suffix": " h", "label": "SUN TO EARTH"}),
 L("bit", "The sky glowed red and green. Even over *Mexico*.", SKYN, [c("bit", .78, expr="happy", scale=.9)], fx=AURR),
 L("bit", "Telegraph wires threw *sparks*.", news("1859: TELEGRAPHS SPARK"), [c("bit", .8, expr="shocked", scale=.9)], fx=[{"type": "glitch"}], sfx=[{"type": "buzz"}]),
 L("hero", "That was wires. We have *phones* now.", SD, [c("hero", .5, pose="phone", expr="smug", scale=1.9)], camera=CU),
 L("bit", "Jay. Today *everything* is wires.", SN, [c("bit", .5, expr="sad", scale=1.8)], fx=[{"type": "vignette"}]),
 L("bit", "Power grids. Satellites. GPS. Your phone. *Me*.", SN, [c("bit", .5, expr="neutral", scale=1.7)], ui={"type": "list", "title": "AT RISK", "items": ["power grid", "satellites + GPS", "Bit"]}),
 L(N, "Bit puts a timer in the *corner*.", SN, [c("bit", .78, expr="neutral", scale=.9)], ui=eta("17:00"), sfx=[{"type": "tick"}]),
 L("hero", "Then we warn everyone. You'll *help*, right?", SN, [c("hero", .5, pose="point", expr="neutral", scale=1.9)], camera=CU),
 L(N, "Bit doesn't answer *right away*.", SN, [c("bit", .5, expr="sad", scale=1.6)], sfx=[{"type": "heartbeat"}]),
 L("bit", "Jay. I'm *made* of electricity too.", RN, [c("bit", .5, expr="dim", scale=1.8)], camera=CU),
 L("bit", "Before it hits, I have to turn myself *off*.", RN, [c("bit", .5, expr="sad", scale=2.0)], camera=PUSH, sfx=CLIFF),
 end("Part two drops in two days."),
]
p2 = [
 recap("Part two. A solar storm hits in *seventeen hours*.", SPACE, [c("bit", .5, expr="shocked", scale=1.6)], fx=SUN, sfx=[{"type": "hit"}]),
 L("hero", "Off? For how *long*?", RN, [c("hero", .5, pose="panic", expr="scared", scale=1.9)], camera=CU),
 L("bit", "Until it's over. A day. *Maybe two*.", RN, [c("bit", .5, expr="sad", scale=1.7)], ui=eta("16:20")),
 L(N, "Jay has never spent *one hour* without Bit.", RN, [c("hero", .5, pose="sit", expr="sad", scale=1.6)], fx=[{"type": "vignette"}]),
 L(N, "Seven p.m. Town hall. Mayor Doyle *laughs*.", SK, [c("boss", .5, pose="wave", expr="grin", scale=1.6)], ui=eta("14:00")),
 L("boss", "A storm from the *Sun*? It's sunny!", SK, [c("boss", .5, pose="point", expr="smug", scale=1.9)], camera=CU),
 L(N, "Only Grandpa Ezra stands *up*.", SK, [c("scientist", .5, pose="idle", expr="angry", scale=1.6)]),
 L("scientist", "I was a railway *telegraph* man. Forty years.", SK, [c("scientist", .5, pose="point", expr="neutral", scale=1.9)], camera=CU),
 L("scientist", "The boy's robot is *right*. Unplug everything.", SK, [c("scientist", .5, pose="point", expr="angry", scale=1.9)], sfx=[{"type": "hit"}]),
 L(N, "Bit makes a list. Jay reads it *out loud*.", SN, [c("hero", .5, pose="phone", expr="neutral", scale=1.6)], ui={"type": "list", "title": "BEFORE THE STORM", "items": ["water + flashlights", "paper maps", "unplug everything"]}),
 L(N, "Nia fills her bakery with *candles*.", SN, [c("friend", .5, pose="idle", expr="neutral", scale=1.6)], fx=[{"type": "glow", "x": 540, "y": 1100, "r": 300}]),
 L(N, "Her brother Milo is *thrilled*.", SN, [c("kid", .5, pose="cheer", expr="grin", scale=1.6)]),
 L("kid", "Northern lights? *Here*? I'm staying up!", SN, [c("kid", .5, pose="cheer", expr="grin", scale=1.9)], camera=CU),
 L(N, "Ezra teaches Milo one thing. *Morse code*.", WS, [c("scientist", .3, pose="sit", expr="happy", scale=1.2), c("kid", .72, pose="idle", expr="grin", scale=1.2)], ui={"type": "card", "text": "· · ·   — — —   · · ·", "sub": "S O S", "color": "#FFD400"}),
 L("kid", "Beep beep beep. *Boop boop boop*.", WS, [c("kid", .5, pose="point", expr="grin", scale=1.9)], sfx=[{"type": "tick"}, {"type": "tick", "at": .3}], camera=CU),
 L(N, "Three a.m. One hour *left*.", RN, [c("hero", .3, pose="sit", expr="sad", scale=1.2), c("bit", .78, expr="dim", scale=1.0)], ui=eta("01:00")),
 L("bit", "Jay. You'll be fine. You were fine *before* me.", RN, [c("bit", .5, expr="happy", scale=1.8)], camera=CU),
 L("hero", "I don't *remember* before you.", RN, [c("hero", .5, pose="idle", expr="sad", scale=1.9)], camera=CU),
 L("bit", "Goodnight, Jay. Look up for *me*.", RN, [c("bit", .5, expr="sleepy", scale=1.9)], camera=PUSH),
 L(N, "And for the first time ever, Bit goes *dark*.", RN, [c("bit", .5, expr="off", scale=1.9)], fx=[{"type": "vignette", "color": "rgba(0,0,0,0.85)"}], sfx=[{"type": "powerdown"}, {"type": "hit", "at": .9}]),
 end("Part three drops in two days."),
]
p3 = [
 recap("Part three. Bit is off. The storm is *close*.", RN, [c("bit", .5, expr="off", scale=1.6)], fx=[{"type": "vignette"}], sfx=[{"type": "hit"}]),
 L(N, "Four a.m. Jay steps *outside*.", SN, [c("hero", .5, pose="walk", expr="neutral", scale=1.6)], sfx=[{"type": "knock"}]),
 L(N, "At first, *nothing*.", SKYN, [c("hero", .5, pose="idle", expr="neutral", scale=1.3)], camera={"zoom": 1.0, "y": .6}),
 L(N, "Then the sky turns *green*.", SKYN, [c("hero", .5, pose="idle", expr="shocked", scale=1.3)], fx=AUR, transition="flash", sfx=[{"type": "riser"}]),
 L(N, "Then *red*. Then purple. Moving like *curtains*.", SKYN, town("shocked"), fx=AURR, sfx=[{"type": "whoosh"}]),
 L("kid", "*Wooow*. Nia! NIA! Come *look*!", SKYN, [c("kid", .5, pose="cheer", expr="grin", scale=1.9)], fx=AURR, camera=CU),
 L(N, "Somewhere, a dog howls at the *sky*.", SKYN, [], fx=AURR, sfx=[{"type": "growl"}]),
 L(N, "Every streetlight in town *flickers*.", SN1, [c("hero", .5, pose="idle", expr="scared", scale=1.5)], fx=AUR + [{"type": "glitch"}], sfx=[{"type": "buzz"}]),
 L(N, "Then the whole town goes *dark*.", SN1, town("scared"), fx=[{"type": "vignette", "color": "rgba(0,0,0,0.85)"}] + AUR, sfx=[{"type": "powerdown"}]),
 L(N, "Phones: no signal. No GPS. No *internet*.", SN1, [c("hero", .5, pose="phone", expr="scared", scale=1.6)], ui={"type": "notify", "app": "Phone", "title": "No service", "body": "Searching...", "color": "#E0312B"}),
 L(N, "But it isn't dark. The sky is *glowing*.", SKYN, town("happy"), fx=AURR),
 L(N, "Nia unfolds a newspaper. She can *read* it.", SN, [c("friend", .5, pose="phone", expr="shocked", scale=1.6)], fx=AUR),
 L("hero", "Bit said that happened in *eighteen fifty nine*.", SN, [c("hero", .5, pose="point", expr="grin", scale=1.9)], fx=AUR, camera=CU),
 L(N, "Down the street, a light comes on at *Ezra's*.", SN, [c("scientist", .5, pose="walk", expr="sleepy", scale=1.6)], fx=AUR),
 L(N, "Ezra is cooking *breakfast*.", RN, [c("scientist", .5, pose="idle", expr="sleepy", scale=1.7)], fx=[{"type": "glow", "x": 540, "y": 900, "r": 300}]),
 L("scientist", "It's bright. So it's *morning*. Eggs?", RN, [c("scientist", .5, pose="wave", expr="happy", scale=1.9)], camera=CU),
 L(N, "In 1859, gold miners did the *same thing*.", news("1859: MINERS WAKE FOR BREAKFAST"), [], transition="whip"),
 L("scientist", "What? Nobody wants *eggs*?", RN, [c("scientist", .5, pose="shrug", expr="sad", scale=1.8)], camera=CU),
 L(N, "Everyone laughs. For a *minute*.", SN, town("grin", "cheer"), fx=AUR),
 L(N, "Jay looks at Bit's dark screen. He *misses* him.", RN, [c("bit", .5, expr="off", scale=1.5)], fx=AUR),
 L(N, "Then Nia *stops* laughing.", SN, [c("friend", .5, pose="idle", expr="scared", scale=1.8)], camera=CU, sfx=[{"type": "heartbeat"}]),
 L("friend", "Where's *Milo*?", SN, [c("friend", .5, pose="panic", expr="shocked", scale=2.0)], fx=AURR, camera=PUSH, sfx=CLIFF),
 end("Part four drops in two days."),
]
p4 = [
 recap("Part four. The storm hit. And Milo is *gone*.", SN, [c("friend", .5, pose="panic", expr="scared", scale=1.6)], fx=AUR, sfx=[{"type": "hit"}]),
 L(N, "Nia calls Milo. Nothing. The phones are *dead*.", SN1, [c("friend", .5, pose="phone", expr="scared", scale=1.6)], ui={"type": "notify", "app": "Phone", "title": "Call failed", "body": "No network", "color": "#E0312B"}),
 L(N, "Jay grabs his phone. *Bit, find Milo*.", SN1, [c("hero", .5, pose="phone", expr="scared", scale=1.7)], camera=CU),
 L(N, "Bit is *off*. Jay forgot.", RN, [c("bit", .5, expr="off", scale=1.6)], fx=[{"type": "vignette"}], sfx=[{"type": "powerdown"}]),
 L("hero", "I don't know how to find *anyone* without Bit.", SN, [c("hero", .5, pose="facepalm", expr="sad", scale=1.9)], camera=CU),
 L("scientist", "Then we find him the *old way*.", SN, [c("scientist", .5, pose="point", expr="angry", scale=1.9)], fx=AUR, camera=CU),
 L(N, "Ezra unfolds a paper map. Jay's never *used* one.", WS, [c("scientist", .3, pose="idle", expr="neutral", scale=1.2), c("hero", .72, pose="think", expr="scared", scale=1.2)], ui={"type": "map", "label": "MILL HILL"}),
 L("hero", "Which way is *up*?", WS, [c("hero", .5, pose="shrug", expr="scared", scale=1.9)], camera=CU),
 L("scientist", "North. Where the lights are *brightest*.", SKYN, [c("scientist", .5, pose="point", expr="smug", scale=1.6)], fx=AURR),
 L("friend", "Milo said he wanted the *best view*.", SN, [c("friend", .5, pose="think", expr="sad", scale=1.8)]),
 L("hero", "Mill Hill. The highest point in *town*.", SN, [c("hero", .5, pose="point", expr="neutral", scale=1.9)], camera=CU),
 L(N, "Mill Hill is two miles away. In the *dark*.", SKYN, [c("hero", .25, pose="walk", expr="scared", scale=1.0), c("friend", .55, pose="walk", expr="scared", scale=1.0)], fx=AUR),
 L(N, "No streetlights. No car *radio*. No Bit.", SKYN, [c("hero", .5, pose="run", expr="scared", scale=1.3)], fx=AUR, sfx=[{"type": "whoosh"}]),
 L(N, "The old railway runs along the *road*.", SK, [], ui={"type": "card", "text": "MILL HILL LINE", "sub": "closed 1962", "color": "#FFD400"}),
 L(N, "Above it, the old telegraph wire is *humming*.", SN, [c("scientist", .5, pose="idle", expr="shocked", scale=1.6)], fx=AUR + [{"type": "glitch"}], sfx=[{"type": "buzz"}]),
 L(N, "Ezra puts a hand near it. *Snap*!", SN, [c("scientist", .5, pose="panic", expr="shocked", scale=1.9)], fx=[{"type": "impact", "x": 540, "y": 700, "at": .4}], camera=CU),
 L("scientist", "Ha! It's *alive*. Just like the stories.", SN, [c("scientist", .5, pose="cheer", expr="grin", scale=1.9)], camera=CU),
 L("hero", "Ezra, careful! That wire has no *power*!", SN, [c("hero", .5, pose="point", expr="scared", scale=1.9)], camera=CU),
 L("scientist", "It does tonight. The *sky* is the battery.", SKYN, [c("scientist", .5, pose="point", expr="smug", scale=2.0)], fx=AURR, camera=PUSH, sfx=CLIFF),
 end("Part five drops in two days."),
]
p5 = [
 recap("Part five. The dead telegraph wire is *alive*.", SN, [c("scientist", .5, pose="point", expr="grin", scale=1.6)], fx=AUR, sfx=[{"type": "buzz"}]),
 L(N, "The old station. Ezra kicks the door *open*.", WS, [c("scientist", .5, pose="idle", expr="angry", scale=1.6)], sfx=[{"type": "knock"}], transition="whip"),
 L(N, "On the desk, a brass telegraph *key*.", WS, [], ui={"type": "card", "text": "TELEGRAPH KEY", "sub": "last used 1962", "color": "#C9A227"}, fx=[{"type": "glow", "x": 540, "y": 1100, "r": 260}]),
 L("scientist", "In 1859, operators *unplugged* their batteries.", news("REAL: 1859 TELEGRAPHS RAN ON THE STORM"), [c("scientist", .8, pose="point", expr="smug", scale=.9)]),
 L("scientist", "And kept sending. On the storm's power *alone*.", WS, [c("scientist", .5, pose="point", expr="grin", scale=1.9)], camera=CU),
 L("hero", "Wait. That's *real*?", WS, [c("hero", .5, pose="idle", expr="shocked", scale=1.9)], camera=CU),
 L("scientist", "Real. Some got *shocks* too. Gloves.", WS, [c("scientist", .5, pose="wave", expr="smug", scale=1.8)], sfx=[{"type": "buzz"}]),
 L(N, "The line runs to a hut on *Mill Hill*.", WS, [], ui={"type": "map", "label": "HILL HUT"}),
 L("friend", "If Milo's up there, would he *hear* it?", WS, [c("friend", .5, pose="think", expr="scared", scale=1.8)]),
 L("scientist", "The hut has a sounder. It *clicks*. Loud.", WS, [c("scientist", .5, pose="idle", expr="neutral", scale=1.7)]),
 L(N, "Ezra's hands shake. He's eighty-one.", WS, [c("scientist", .5, pose="sit", expr="sad", scale=1.6)], camera=CU),
 L("scientist", "Jay. You *tap*. I'll spell.", WS, [c("scientist", .5, pose="point", expr="neutral", scale=1.9)], camera=CU),
 L(N, "Jay puts his finger on the key. *Click*.", WS1, [c("hero", .5, pose="sit", expr="scared", scale=1.7)], fx=[{"type": "glitch"}], sfx=[{"type": "tick"}]),
 L(N, "A spark *jumps*. Jay doesn't let go.", WS1, [c("hero", .5, pose="sit", expr="angry", scale=1.9)], fx=[{"type": "impact", "x": 540, "y": 1050, "at": .2}], camera=CU, sfx=[{"type": "buzz"}]),
 L(N, "Dot dot dot. Dash dash dash. *Dot dot dot*.", WS1, [c("hero", .5, pose="sit", expr="angry", scale=1.6)], ui={"type": "card", "text": "· · ·   — — —   · · ·", "sub": "S O S", "color": "#FFD400"}, sfx=[{"type": "tick"}, {"type": "tick", "at": .25}, {"type": "tick", "at": .5}]),
 L(N, "Again. And *again*.", WS1, [c("hero", .3, pose="sit", expr="scared", scale=1.2), c("friend", .72, pose="idle", expr="scared", scale=1.2)], fx=AUR),
 L("scientist", "Good. Slow. Like a *heartbeat*.", WS1, [c("scientist", .5, pose="point", expr="neutral", scale=1.8)], sfx=[{"type": "heartbeat"}]),
 L(N, "Five minutes. *Nothing*.", WS1, [c("friend", .5, pose="idle", expr="sad", scale=1.8)], ui=eta("05:00"), fx=[{"type": "vignette"}]),
 L("friend", "He's not there. He's *not* there.", WS1, [c("friend", .5, pose="facepalm", expr="sad", scale=1.9)], camera=CU),
 L(N, "Then the sounder on the desk goes *click*.", WS1, [c("hero", .5, pose="idle", expr="shocked", scale=2.0)], camera=PUSH, sfx=[{"type": "tick", "at": .5}, {"type": "hit", "at": .9}]),
 end("Part six drops in two days."),
]
p6 = [
 recap("Part six. Jay sent an SOS. Something *answered*.", WS1, [c("hero", .5, pose="sit", expr="shocked", scale=1.6)], sfx=[{"type": "tick"}]),
 L(N, "Click. Click. *Click*.", WS1, [c("scientist", .5, pose="idle", expr="shocked", scale=1.6)], sfx=[{"type": "tick"}, {"type": "tick", "at": .3}, {"type": "tick", "at": .6}]),
 L("scientist", "That's not random. That's *Morse*.", WS1, [c("scientist", .5, pose="point", expr="grin", scale=1.9)], camera=CU),
 L(N, "Ezra writes each letter on the *wall*.", WS1, [], ui={"type": "list", "title": "MESSAGE", "items": ["M - I - L - O", "O - K", "C - O - L - D"]}),
 L("friend", "Milo. It's *Milo*! He remembered!", WS1, [c("friend", .5, pose="cheer", expr="grin", scale=2.0)], camera=CU, sfx=[{"type": "ding"}]),
 L("scientist", "One lesson. One. That boy is a *natural*.", WS1, [c("scientist", .5, pose="cheer", expr="happy", scale=1.8)]),
 L(N, "Nia is already running for the *door*.", SKYN, [c("friend", .5, pose="run", expr="angry", scale=1.4)], fx=AUR, sfx=[{"type": "whoosh"}], transition="whip"),
 L(N, "Jay follows her. Up Mill Hill. Under the *lights*.", SKYN, [c("hero", .3, pose="run", expr="scared", scale=1.1), c("friend", .65, pose="run", expr="angry", scale=1.1)], fx=AURR),
 L("friend", "You're quiet. You're *never* quiet.", SKYN, [c("friend", .5, pose="walk", expr="neutral", scale=1.8)], fx=AUR, camera=CU),
 L("hero", "When I'm scared, Bit tells me what to *do*.", SKYN, [c("hero", .5, pose="walk", expr="sad", scale=1.9)], fx=AUR, camera=CU),
 L("hero", "Tonight there's no Bit. Just *me*.", SKYN, [c("hero", .5, pose="idle", expr="sad", scale=1.9)], fx=AUR),
 L("friend", "Jay. *You* tapped that key. Not Bit.", SKYN, [c("friend", .5, pose="point", expr="happy", scale=1.9)], fx=AURR, camera=CU),
 L(N, "At the top, a small shape in a *blanket*.", SKYN, [c("kid", .5, pose="sit", expr="sad", scale=1.3)], fx=AURR),
 L("kid", "Nia! I tapped back! Did you *hear* me?", SKYN, [c("kid", .5, pose="cheer", expr="grin", scale=1.9)], fx=AURR, camera=CU, sfx=[{"type": "pop"}]),
 L(N, "Nia hugs him so hard he *squeaks*.", SKYN, [c("friend", .4, pose="cheer", expr="happy", scale=1.3), c("kid", .62, pose="cheer", expr="grin", scale=1.1)], fx=AURR, sfx=[{"type": "ding"}]),
 L(N, "For a minute, all three just look *up*.", SKYN, [c("hero", .25, pose="idle", expr="happy", scale=1.0), c("friend", .5, pose="idle", expr="happy", scale=1.0), c("kid", .72, pose="idle", expr="grin", scale=.9)], fx=AURR, camera={"zoom": 1.0, "y": .55}),
 L("hero", "Bit said look up for him. I'm *looking*.", SKYN, [c("hero", .5, pose="idle", expr="happy", scale=1.9)], fx=AUR, camera=CU),
 L(N, "Then Milo says something that makes Jay *freeze*.", SKYN, [c("kid", .5, pose="idle", expr="neutral", scale=1.7)], fx=AUR, sfx=[{"type": "heartbeat"}]),
 L("kid", "I charged my tablet. On *Bit's* dock.", SKYN, [c("kid", .5, pose="point", expr="grin", scale=2.0)], fx=AURR, camera=PUSH, sfx=CLIFF),
 end("Part seven drops in two days."),
]
p7 = [
 recap("Part seven. Milo's safe. Bit's dock is *plugged in*.", SKYN, [c("kid", .5, pose="point", expr="grin", scale=1.6)], fx=AUR, sfx=[{"type": "hit"}]),
 L("hero", "The dock is plugged *into the wall*.", SKYN, [c("hero", .5, pose="panic", expr="shocked", scale=1.9)], fx=AUR, camera=CU),
 L(N, "If power comes back, the surge hits *Bit*.", RN, [c("bit", .5, expr="off", scale=1.6)], fx=[{"type": "vignette"}]),
 L(N, "Down the hill, the town lights *blink*.", SN1, town("shocked"), fx=AUR + [{"type": "glitch"}], sfx=[{"type": "buzz"}]),
 L("friend", "They're turning the power *back on*!", SKYN, [c("friend", .5, pose="point", expr="scared", scale=1.9)], fx=AUR, camera=CU),
 L(N, "Jay runs. Two miles. *Downhill*.", SKYN, [c("hero", .5, pose="run", expr="angry", scale=1.4)], fx=AUR + [{"type": "speedLines"}], sfx=[{"type": "whoosh"}], transition="whip"),
 L(N, "His legs burn. His lungs burn. He *keeps going*.", SN, [c("hero", .5, pose="run", expr="angry", scale=1.7)], fx=[{"type": "speedLines"}], camera=CU),
 L(N, "Mayor Doyle is at the town *switch*.", SN1, [c("boss", .5, pose="idle", expr="happy", scale=1.6)], ui={"type": "card", "text": "MAIN SWITCH", "sub": "OFF → ON", "color": "#2DBE7E"}),
 L("boss", "Storm's over! Lights in three, two...", SN1, [c("boss", .5, pose="point", expr="grin", scale=1.9)], ui=eta("00:03"), camera=CU),
 L(N, "The sky flares red *again*.", SKYN, [], fx=AURR + [{"type": "alarm"}], sfx=[{"type": "riser"}]),
 L(N, "A second wave. Storms like this come in *pieces*.", SKYN, [c("bit", .78, expr="off", scale=.8)], fx=AURR),
 L(N, "Jay bursts through his door. The dock is *humming*.", RN, [c("hero", .5, pose="panic", expr="scared", scale=1.7)], fx=[{"type": "glitch"}], sfx=[{"type": "buzz"}], camera=CU),
 L(N, "He grabs the cable. *Pulls*.", RN, [c("hero", .5, pose="throw", expr="angry", scale=1.9)], fx=[{"type": "impact", "x": 540, "y": 900, "at": .3}], sfx=[{"type": "hit", "at": .3}], camera={"zoom": 1.1, "y": .6, "shake": .3}),
 L(N, "A spark. A bang. Then the street goes *dark*.", SN1, town("shocked"), fx=[{"type": "vignette", "color": "rgba(0,0,0,0.85)"}], sfx=[{"type": "powerdown"}]),
 L(N, "The town transformer is *fried*.", SN1, [c("boss", .5, pose="facepalm", expr="sad", scale=1.6)], ui={"type": "stamp", "text": "FRIED", "color": "#E0312B"}),
 L(N, "No power for *three days*. That's the cost.", SN, town("sad"), ui={"type": "counter", "from": 0, "to": 3, "label": "DAYS WITHOUT POWER"}),
 L(N, "But the cable is in Jay's *hand*.", RN, [c("hero", .5, pose="sit", expr="sad", scale=1.8)], camera=CU),
 L(N, "Morning. The sky is *blue* again.", SKY, [], fx=[{"type": "glow", "x": 800, "y": 300, "r": 300}]),
 L(N, "Jay presses Bit's power button. *Nothing*.", RD, [c("bit", .5, expr="off", scale=2.0)], camera=PUSH, sfx=CLIFF),
 end("Part eight drops in two days. The final part."),
]
p8 = [
 recap("Part eight. The storm's over. But Bit *won't wake*.", RD, [c("bit", .5, expr="off", scale=1.6)], sfx=[{"type": "hit"}]),
 L(N, "Jay presses it again. And *again*.", RD, [c("hero", .5, pose="idle", expr="sad", scale=1.7)], sfx=[{"type": "tick"}, {"type": "tick", "at": .5}]),
 L("hero", "You said one day. Maybe *two*.", RD, [c("hero", .5, pose="sit", expr="sad", scale=1.9)], camera=CU),
 L(N, "Ezra knocks. He holds up a *battery*. It's dead.", RD, [c("scientist", .5, pose="shrug", expr="sad", scale=1.6)], sfx=[{"type": "knock"}]),
 L(N, "Every battery in town is *dead*.", SD, town("sad")),
 L(N, "Then Milo walks in. With a *solar panel*.", RD, [c("kid", .5, pose="cheer", expr="grin", scale=1.6)], ui={"type": "card", "text": "SOLAR CHARGER", "sub": "Milo's science fair", "color": "#FFD400"}),
 L("kid", "It runs on the Sun. Is that *funny*?", RD, [c("kid", .5, pose="point", expr="grin", scale=1.9)], camera=CU),
 L(N, "The Sun broke Bit. Can the Sun *fix* him?", SKY, [], fx=[{"type": "glow", "x": 540, "y": 500, "r": 400}], sfx=[{"type": "riser"}]),
 L(N, "One hour. Two. Then a *beep*.", RD, [c("bit", .5, expr="dim", scale=1.8)], ui={"type": "bars", "items": [{"label": "BATTERY", "value": 0.12, "color": "#2DBE7E"}], "tag": "CHARGING"}, sfx=[{"type": "ding"}]),
 L("bit", "Jay? Did you *look up*?", RD, [c("bit", .5, expr="happy", scale=1.9)], fx=[{"type": "glow"}], sfx=[{"type": "powerup"}], camera=CU),
 L("hero", "Bit! I looked up. I used a *map*!", RD, [c("hero", .5, pose="cheer", expr="grin", scale=1.9)], camera=CU),
 L("hero", "And I sent Morse code. On a *storm*.", RD, [c("hero", .5, pose="point", expr="grin", scale=1.9)]),
 L("bit", "Without me? I'm *proud*. And a bit jealous.", RD, [c("bit", .5, expr="smug", scale=1.8)], camera=CU),
 L("bit", "Fun fact. In 2012, one *missed* us.", news("REAL: JULY 2012 STORM MISSED EARTH"), [c("bit", .8, expr="think", scale=.9)], transition="whip"),
 L("bit", "By about *nine days*.", SPACE, [c("bit", .5, expr="shocked", scale=1.7)], fx=SUN, ui={"type": "counter", "from": 0, "to": 9, "label": "DAYS"}),
 L("hero", "Bit. Teach me *everything*. Just in case.", RD, [c("hero", .5, pose="point", expr="neutral", scale=1.9)], camera=CU),
 L("bit", "Lesson one. *Unplug the dock*.", RD, [c("bit", .5, expr="smug", scale=1.9)], camera=CU),
 L(N, "That night, the whole town *looks up*.", SKYN, town("happy"), fx=AUR),
 L(N, "No storm. Just stars. And one robot *beeping*.", SKYN, [c("bit", .5, expr="happy", scale=1.2, lift=300)], sfx=[{"type": "tick"}, {"type": "tick", "at": .3}]),
 L("kid", "Bit's doing Morse! It says... *T-H-A-N-K-S*.", SKYN, [c("kid", .3, pose="cheer", expr="grin", scale=1.3), c("bit", .75, expr="happy", scale=.9)], fx=AUR, camera=PUSH, sfx=[{"type": "ding", "at": .6}]),
 end("Follow for a new What if every day."),
]

parts = [("Seventeen Hours", p1), ("Going Dark", p2), ("Green Sky", p3), ("No Signal", p4),
         ("The Telegraph", p5), ("Mill Hill", p6), ("Second Wave", p7), ("Sunlight", p8)]

series = {
 "title": "What If a Solar Storm Hit Today?",
 "rubric": "what-if: disaster (real history)", "mood": "tension", "seed": 5900, "every": 2,
 "names": {"hero": "JAY", "bit": "BIT", "friend": "NIA", "boss": "MAYOR DOYLE", "scientist": "GRANDPA EZRA", "kid": "MILO"},
 "finale": {"text": "THE END", "sub": "Follow for a new What if every day"},
 "parts": [{"title": t, "lines": ls} for t, ls in parts],
}
(D / "series.json").write_text(json.dumps(series, indent=1, ensure_ascii=False) + "\n")

hooks = ["What If a Solar Storm Hit Today?", "What If Your AI Had to Shut Down?", "What If the Sky Turned Green Tonight?",
         "What If Every Phone Died at Once?", "What If a Dead Telegraph Came Alive?", "What If a Kid Answered in Morse Code?",
         "What If a Solar Storm Came Back?", "What If the Sun Could Fix What It Broke?"]
blurbs = [
 "The Sun just threw a giant storm at Earth. In 1859 the Carrington Event made telegraph wires spark. Today, everything is wires.",
 "Bit is made of electricity, so Bit has to switch off before the solar storm hits. Jay has never spent an hour without him.",
 "The northern lights fill the sky, the town goes dark, and people read newspapers by the glow, like in 1859. Then Milo is missing.",
 "No phones, no GPS, no Bit. Jay has to find Milo the old way. And the dead telegraph wire starts humming.",
 "In 1859, telegraph operators unplugged their batteries and kept sending on the storm's power alone. Jay tries it.",
 "Someone taps back in Morse code. Up Mill Hill, under the aurora, Jay learns what he can do without Bit.",
 "Bit's dock is still plugged in, the power is coming back, and the storm has a second wave.",
 "Bit won't wake up. Every battery in town is dead. Then Milo brings a solar panel.",
]
tags = ["what if", "solar storm", "carrington event", "northern lights", "aurora", "blackout", "animation", "story", "shorts"]
def ttl(i):
    t = f"{hooks[i]} Part {i + 1} #shorts"
    t2 = f"{hooks[i]} ☀️ Part {i + 1} #shorts"
    return t2 if len(t2) <= 60 else t
meta = {}
for i in range(8):
    meta[f"part{i + 1}"] = {
        "title": ttl(i), "short": True,
        "description": f"{blurbs[i]}\nAn original animated \"What if...?\" story by zylo, part {i + 1} of 8.\n\nFollow for a new \"What if...?\" every day.\n\n#whatif #solarstorm #northernlights #animation #shorts",
        "tags": tags, "categoryId": "1", "privacy": "public", "madeForKids": False, "syntheticMedia": False}
meta["full"] = {
    "title": "What If a Solar Storm Hit Today? (Full Story)",
    "description": "In 1859, the Carrington Event made telegraph wires spark and lit the sky so bright people read newspapers at night. What if it happened today, and Bit had to switch himself off?\nAn original animated \"What if...?\" story by zylo: all eight parts in one.\n\n{chapters}\nFollow for a new \"What if...?\" every day.\n\n#whatif #solarstorm #northernlights #animation #story",
    "tags": [t for t in tags if t != "shorts"], "categoryId": "1", "privacy": "public", "madeForKids": False, "syntheticMedia": False}
mp = D / "metadata.json"
if mp.exists():
    old = json.loads(mp.read_text())
    for k, v in meta.items():
        if "publishAt" in old.get(k, {}): v["publishAt"] = old[k]["publishAt"]
mp.write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")

(D / "full").mkdir(exist_ok=True)
(D / "full/thumb.json").write_text(json.dumps({
 "text": "THE SUN *ATTACKED*", "badge": "FULL STORY", "cropY": 880, "set": {"type": "sky", "time": "night"},
 "fx": [{"type": "aurora", "colors": ["#FF3B6B", "#3DFFB0", "#C04BFF"], "strength": 0.95}],
 "cast": [{"id": "kid", "x": 0.93, "pose": "cheer", "expr": "grin", "scale": 1.0, "y": 1640, "facing": -1},
          {"id": "hero", "x": 0.72, "pose": "panic", "expr": "shocked", "scale": 1.3, "y": 1760},
          {"id": "bit", "x": 0.56, "expr": "glitch", "scale": 0.55, "y": 1215}]}, indent=1) + "\n")

for i, (t, ls) in enumerate(parts):
    spoken = [l for l in ls if not l.get("end")]
    w = sum(len(re.sub(r"[*\"]", "", l["say"]).split()) for l in spoken)
    long_ = [l["say"] for l in spoken if len(l["say"].split()) > 9]
    print(f"part{i + 1} {t!r}: {len(ls)} lines, {w} words", "LONG:" if long_ else "", long_ or "")
for k, v in meta.items():
    print(k, len(v["title"]), v["title"])
