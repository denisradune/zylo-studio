"""Writes series.json + metadata.json + full/thumb.json for Zombies Season 2 (8 parts).
Run: python3 episodes/2026-11-05-what-if-zombies-season-2/build_series.py"""
import json, re
from pathlib import Path
D = Path(__file__).resolve().parent

def L(sp, say, set_, cast=(), **kw):
    shot = {"set": set_ if isinstance(set_, dict) else {"type": set_}, "cast": list(cast)}
    shot.update(kw)
    return {"speaker": sp, "say": say, "shot": shot}
def c(id_, x=0.5, **kw): return {"id": id_, "x": x, **kw}
N = "narrator"
CAMP = {"type": "wasteland", "time": "day"}; CAMPN = {"type": "wasteland", "time": "night"}
LAB = {"type": "lab"}
SD = {"type": "street", "time": "dusk", "damage": 1}; SN = {"type": "street", "time": "night", "damage": 2}
SDAY = {"type": "street", "time": "day", "damage": 1}; SFIX = {"type": "street", "time": "day"}
TOP = {"type": "sky", "time": "day"}; TOPN = {"type": "sky", "time": "night"}; TOPD = {"type": "sky", "time": "dusk"}
STORE = {"type": "store", "damage": 1}
def news(h): return {"type": "news", "headline": h}
def burst(col): return {"type": "burst", "color": col}
CU = {"zoom": 1.1, "y": 0.6}
def end(t): return {"speaker": N, "say": t, "end": True}
def recap(t, set_, cast, **kw):
    l = L(N, t, set_, cast, **kw); l["shortOnly"] = True; return l
def horde(n=4, run=False, dx=0.0):
    out = []
    for i in range(n):
        z = c("zombie" if i % 2 == 0 else "zombie2", .12 + i * (.76 / max(n - 1, 1)), pose="zombie", expr="angry", depth=.7 - i * .15, facing=-1 if i % 2 else 1)
        if run: z.update(x=-.1 - i * .2, moveTo=1.15 - i * .1 + dx, pose="run")
        out.append(z)
    return out

p1 = [
 L(N, "What if your AI's backup held *the virus*?", SN, [c("hero", .3, pose="phone", expr="scared", scale=1.3), c("bit", .78, expr="glitch", scale=1.0)] + horde(2), fx=[{"type": "glitch"}], sfx=[{"type": "glitch"}, {"type": "hit", "at": .6}], camera={"push": .08}),
 L(N, "Last season, one phone update made the world *zombies*.", news("ONE UPDATE. ONE BILLION ZOMBIES."), [c("zombie", .5, pose="zombie", expr="angry", scale=1.3)], sfx=[{"type": "siren", "volume": .4}], transition="whip"),
 L(N, "Bit died saving Jay. Then returned from *a backup*.", CAMP, [c("hero", .3, pose="phone", expr="happy", scale=1.3), c("bit", .78, expr="happy", scale=1.0)], sfx=[{"type": "powerup"}]),
 L(N, "Now Jay and Mia live in an army *camp*.", CAMP, [c("hero", .28, pose="idle", expr="neutral", scale=1.2), c("friend", .5, pose="idle", expr="neutral", scale=1.2), c("soldier", .78, pose="idle", expr="neutral", scale=1.2, facing=-1)]),
 L("soldier", "Camp rule. No screens. *No exceptions*.", CAMP, [c("soldier", .5, pose="point", expr="angry", scale=1.9)], ui={"type": "stamp", "text": "NO SCREENS", "color": "#E0312B"}, camera=CU, sfx=[{"type": "hit"}]),
 L(N, "So Jay hides Bit in his *sock drawer*.", {"type": "room", "time": "night", "damage": 1}, [c("hero", .35, pose="think", expr="smug", scale=1.4), c("bit", .78, expr="dim", scale=.8)]),
 L("bit", "This is the *worst* hotel I've ever stayed in.", {"type": "room", "time": "night", "damage": 1}, [c("bit", .5, expr="angry", scale=1.8)], camera=CU),
 L("hero", "Shh. Bit, did your backup come back *okay*?", {"type": "room", "time": "night", "damage": 1}, [c("hero", .5, pose="phone", expr="neutral", scale=1.8)], camera=CU),
 L("bit", "Mostly. But I found a file that *isn't mine*.", LAB, [c("bit", .5, expr="think", scale=1.6)], sfx=[{"type": "tick"}, {"type": "tick", "at": .5}], transition="whip"),
 L("bit", "It's called *update version two*.", LAB, [c("bit", .78, expr="shocked", scale=.9)], ui={"type": "card", "text": "UPDATE_v2", "sub": "hidden in Bit's backup", "color": "#16161C"}, sfx=[{"type": "buzz"}]),
 L("hero", "The zombie update? *Inside you*?", {"type": "room", "time": "night", "damage": 1}, [c("hero", .5, pose="panic", expr="shocked", scale=1.9)], camera={"zoom": 1.1, "y": .6, "shake": .3}),
 L("bit", "It has a timer. Seven days. Then it *sends*.", LAB, [c("bit", .5, expr="sad", scale=1.6)], ui={"type": "clock", "text": "07:00", "to": "06:59"}, sfx=[{"type": "tick"}]),
 L("hero", "Sends where? Everyone already *has* the update.", {"type": "room", "time": "night", "damage": 1}, [c("hero", .5, pose="shrug", expr="scared", scale=1.8)], camera=CU),
 L("bit", "Not everyone. The army's radios. *This camp*.", CAMPN, [c("bit", .5, expr="angry", scale=1.6)], fx=[{"type": "vignette"}], sfx=[{"type": "heartbeat"}]),
 L(N, "Then the howling outside the fence *stops*.", CAMPN, horde(4), fx=[{"type": "vignette"}], sfx=[{"type": "growl", "volume": .4}], camera={"push": .1}),
 L(N, "Every zombie turns. And starts walking the *same way*.", SN, horde(4, run=False), sfx=[{"type": "whoosh"}], transition="whip"),
 L("friend", "Jay. They never walk *together*.", CAMPN, [c("friend", .5, pose="point", expr="scared", scale=1.9)], camera=CU),
 L(N, "Thousands of them. Marching toward *the city*.", SN, horde(4, run=True), sfx=[{"type": "growl"}, {"type": "growl", "at": .7, "volume": .5}]),
 L("bit", "They're not wandering anymore. They're going *somewhere*.", CAMPN, [c("bit", .5, expr="shocked", scale=2.0)], fx=[{"type": "vignette"}], camera={"zoom": 1.15, "y": .5, "push": .12}, sfx=[{"type": "riser"}]),
 end("Part two drops in two days."),
]
p2 = [
 recap("Part two. The zombies are marching. *Together*.", SN, horde(3), sfx=[{"type": "hit"}]),
 L(N, "Jay sneaks Bit into the science tent.", LAB, [c("hero", .3, pose="walk", expr="scared", scale=1.3), c("bit", .78, expr="dim", scale=.8)], sfx=[{"type": "whoosh"}]),
 L(N, "Doctor Ada hasn't slept in *three weeks*.", LAB, [c("scientist", .5, pose="think", expr="sleepy", scale=1.7)], ui={"type": "counter", "from": 0, "to": 21, "label": "DAYS AWAKE"}),
 L("scientist", "A screen? In my tent? Are you *insane*?", LAB, [c("scientist", .5, pose="point", expr="angry", scale=1.9)], camera=CU),
 L("bit", "Highly advanced assistant. I come in *peace*.", LAB, [c("bit", .5, expr="happy", scale=1.8)], camera=CU, sfx=[{"type": "ding"}]),
 L("hero", "Why are they marching? They used to just *wander*.", LAB, [c("hero", .5, pose="shrug", expr="scared", scale=1.8)], camera=CU),
 L("scientist", "Because nature *already invented* zombies.", LAB, [c("scientist", .5, pose="idle", expr="smug", scale=1.8)], camera=CU, sfx=[{"type": "pop"}]),
 L("scientist", "In the rainforest, a fungus infects *ants*.", {"type": "wasteland", "time": "dusk"}, [c("scientist", .78, pose="point", expr="neutral", scale=.9)], ui={"type": "card", "text": "ZOMBIE ANT FUNGUS", "sub": "Ophiocordyceps — it's real", "color": "#2DBE7E"}, transition="flash"),
 L("scientist", "The ant leaves its nest. Then it *climbs*.", LAB, [c("scientist", .5, pose="point", expr="neutral", scale=1.6)], ui={"type": "list", "title": "ZOMBIE ANT", "items": ["Leaves the nest", "Climbs a plant", "Bites a leaf"]}),
 L("scientist", "It bites a leaf vein and *never lets go*.", LAB, [c("scientist", .5, pose="idle", expr="scared", scale=1.8)], camera=CU, sfx=[{"type": "hit"}]),
 L("bit", "Usually about twenty six centimeters *above the ground*.", LAB, [c("bit", .78, expr="think", scale=.9)], ui={"type": "counter", "from": 0, "to": 26, "suffix": " cm", "label": "DEATH GRIP HEIGHT"}, sfx=[{"type": "tick"}]),
 L("scientist", "One study found they bite at *noon*.", LAB, [c("scientist", .5, pose="think", expr="neutral", scale=1.7)], ui={"type": "clock", "text": "12:00"}),
 L("hero", "And then? Please say *and then nothing*.", LAB, [c("hero", .5, pose="idle", expr="scared", scale=1.9)], camera=CU),
 L("scientist", "Then a stalk grows from its head. *Spores*.", burst("#2DBE7E"), [], ui={"type": "stamp", "text": "SPORES", "color": "#16161C"}, sfx=[{"type": "boom"}], transition="flash"),
 L("hero", "That's the most disgusting thing I've ever *heard*.", LAB, [c("hero", .5, pose="facepalm", expr="sad", scale=1.9)], camera=CU),
 L("scientist", "Someone copied it. The update makes people *climb*.", LAB, [c("scientist", .5, pose="point", expr="angry", scale=1.9)], fx=[{"type": "vignette"}], camera=CU, sfx=[{"type": "heartbeat"}]),
 L("friend", "Climb *what*? There are no trees downtown.", LAB, [c("friend", .5, pose="shrug", expr="shocked", scale=1.8)], camera=CU),
 L(N, "Bit pulls up the map. The city's tallest *building*.", LAB, [c("bit", .82, expr="think", scale=.8)], ui={"type": "map", "label": "GRAY TOWER", "radius": .3}, sfx=[{"type": "powerup"}]),
 L("bit", "Gray Tower. The biggest phone antenna *in the country*.", LAB, [c("bit", .5, expr="shocked", scale=1.8)], camera=CU),
 L("scientist", "When they reach the top, the tower *broadcasts*.", news("GRAY TOWER: STILL ONLINE"), [c("zombie", .5, pose="zombie", expr="angry", scale=1.2)], fx=[{"type": "glow", "x": 540, "y": 600, "r": 400}], sfx=[{"type": "riser"}, {"type": "hit", "at": .9}], transition="whip"),
 end("Part three drops in two days."),
]
p3 = [
 recap("Part three. The zombies are climbing *Gray Tower*.", SD, horde(3), sfx=[{"type": "hit"}]),
 L(N, "Sergeant Rook grabs his keys. And a *crowbar*.", CAMP, [c("soldier", .5, pose="idle", expr="angry", scale=1.7)], sfx=[{"type": "knock"}]),
 L("soldier", "Four seats. One rule. That toaster stays *dark*.", CAMP, [c("soldier", .5, pose="point", expr="angry", scale=1.9)], camera=CU),
 L("bit", "Dimming to one percent. Again. *Sigh*.", CAMP, [c("bit", .5, expr="dim", scale=1.7)], sfx=[{"type": "powerdown"}]),
 L(N, "They drive into the city with the *lights off*.", SD, [c("car", -.2, moveTo=1.1, color="#3F5B3A", scale=1.2)], sfx=[{"type": "engine"}], transition="whip"),
 L(N, "The streets are empty. Every zombie is *downtown*.", SD, [], fx=[{"type": "vignette"}], sfx=[{"type": "whoosh", "volume": .4}], camera={"push": .12}),
 L("friend", "Jay. Look *up*.", SD, [c("friend", .5, pose="point", expr="shocked", scale=1.9)], camera=CU),
 L(N, "Gray Tower. Covered in people, *climbing*.", TOPD, horde(4), fx=[{"type": "glow", "x": 540, "y": 300, "r": 300}], sfx=[{"type": "growl"}], transition="flash"),
 L(N, "Up the stairs. Up the walls. Like *ants*.", TOPD, horde(4, run=True), fx=[{"type": "speedLines"}], sfx=[{"type": "growl", "volume": .5}]),
 L("hero", "Bit, what *time* is it?", SD, [c("hero", .5, pose="phone", expr="scared", scale=1.8)], camera=CU),
 L("bit", "Eleven fifty nine. And *twelve*.", SD, [c("bit", .5, expr="shocked", scale=1.6)], ui={"type": "clock", "text": "11:59", "to": "12:00"}, sfx=[{"type": "tick"}, {"type": "ring", "at": .8}]),
 L(N, "At noon, every zombie stops. And *grabs on*.", TOPD, horde(4), fx=[{"type": "vignette"}], ui={"type": "stamp", "text": "DEATH GRIP", "color": "#E0312B"}, sfx=[{"type": "hit"}]),
 L("scientist", "Just like the ants. They won't let go *now*.", SD, [c("scientist", .5, pose="idle", expr="scared", scale=1.8)], camera=CU),
 L(N, "The antenna on top starts *glowing*.", TOPD, [], fx=[{"type": "glow", "x": 540, "y": 400, "r": 500}], sfx=[{"type": "powerup"}, {"type": "buzz", "at": .6}]),
 L("bit", "It's warming up. Like it's *waiting* for something.", SD, [c("bit", .5, expr="think", scale=1.8)], camera=CU),
 L("soldier", "Waiting for *what*?", SD, [c("soldier", .5, pose="shrug", expr="angry", scale=1.9)], camera=CU),
 L("bit", "For *me*. For the file in my backup.", SD, [c("bit", .5, expr="sad", scale=2.0)], fx=[{"type": "vignette"}], camera={"zoom": 1.15, "y": .5, "push": .1}, sfx=[{"type": "heartbeat"}]),
 L(N, "On the roof, someone is standing. *Not climbing*.", TOP, [c("boss", .5, pose="idle", expr="smug", scale=1.3)], sfx=[{"type": "whoosh"}], transition="whip"),
 L(N, "Clean suit. Big headphones. *Not a zombie*.", TOP, [c("boss", .5, pose="phone", expr="smug", scale=1.9)], camera=CU),
 L("boss", "Hello, Jay. I've been waiting for *your toaster*.", TOP, [c("boss", .5, pose="point", expr="grin", scale=2.0)], camera={"zoom": 1.15, "y": .55, "push": .1}, sfx=[{"type": "riser"}, {"type": "hit", "at": .9}]),
 end("Part four drops in two days."),
]
p4 = [
 recap("Part four. The man on the roof is *human*.", TOP, [c("boss", .5, pose="idle", expr="smug", scale=1.6)], sfx=[{"type": "hit"}]),
 L(N, "His name is Mr. Gray. He owns *the tower*.", news("GRAY PHONES: ALWAYS CONNECTED"), [c("boss", .5, pose="idle", expr="smug", scale=1.3)], transition="flash"),
 L(N, "And the phone company. And *the update*.", TOP, [c("boss", .5, pose="cheer", expr="grin", scale=1.7)], sfx=[{"type": "ding"}]),
 L("hero", "You did this? *On purpose*?", SD, [c("hero", .5, pose="point", expr="angry", scale=1.9)], camera=CU, sfx=[{"type": "hit"}]),
 L("boss", "I wanted people to never put their phones *down*.", TOP, [c("boss", .5, pose="phone", expr="happy", scale=1.8)], camera=CU),
 L("boss", "Version one worked a little *too* well.", TOP, [c("boss", .5, pose="shrug", expr="grin", scale=1.8)], camera=CU),
 L("friend", "A little? They're *eating* people!", SD, [c("friend", .5, pose="panic", expr="angry", scale=1.9)], camera={"zoom": 1.1, "y": .6, "shake": .3}),
 L("boss", "Version two finishes the job. *Everyone* online.", TOP, [c("boss", .5, pose="point", expr="smug", scale=1.9)], ui={"type": "bars", "items": [{"label": "ONLINE", "value": .97, "color": "#FF3B3B"}, {"label": "OFFLINE", "value": .03, "color": "#2DBE7E"}], "tag": "97%"}),
 L("boss", "But my only copy is inside your *little friend*.", TOP, [c("boss", .5, pose="point", expr="grin", scale=2.0)], camera=CU),
 L("bit", "Jay. I really don't like this *guy*.", SD, [c("bit", .5, expr="angry", scale=1.8)], camera=CU),
 L("hero", "Bit's not yours. He's *mine*.", SD, [c("hero", .5, pose="idle", expr="angry", scale=1.9)], camera=CU),
 L("boss", "Then let's ask the *crowd*.", TOP, [c("boss", .5, pose="phone", expr="smug", scale=1.8)], sfx=[{"type": "ring"}]),
 L(N, "Gray taps his phone. Every zombie's phone *lights up*.", SN, horde(4), fx=[{"type": "glow", "x": 300, "y": 1100, "r": 260}, {"type": "glow", "x": 800, "y": 1100, "r": 260}], sfx=[{"type": "ring"}, {"type": "ring", "at": .3}, {"type": "ring", "at": .6}], transition="flash"),
 L(N, "A thousand heads turn toward the *car*.", SN, horde(4, run=True), sfx=[{"type": "growl"}]),
 L("soldier", "Everybody in! *Now*!", SN, [c("soldier", .5, pose="point", expr="angry", scale=1.9)], fx=[{"type": "speedLines"}], camera={"zoom": 1.1, "y": .6, "shake": .4}, sfx=[{"type": "engine"}]),
 L(N, "Jay runs. Bit slips out of his *pocket*.", SN, [c("hero", .3, pose="run", expr="scared", scale=1.4), c("bit", .78, expr="shocked", scale=.8)], fx=[{"type": "throwObj", "from": [380, 1100], "to": [800, 1500], "at": .2}], sfx=[{"type": "pop"}]),
 L("hero", "Bit! *Bit*!", SN, [c("hero", .5, pose="panic", expr="scared", scale=2.0)], camera={"zoom": 1.15, "y": .55, "shake": .4}),
 L(N, "A gloved hand picks Bit up off the street.", SN, [c("boss", .5, pose="idle", expr="grin", scale=1.6), c("bit", .72, expr="scared", scale=.8)], fx=[{"type": "vignette"}], sfx=[{"type": "heartbeat"}]),
 L("boss", "Thank you, Jay. Upload begins at noon. *Sunday*.", SN, [c("boss", .5, pose="point", expr="smug", scale=2.0)], ui={"type": "card", "text": "SUNDAY 12:00", "sub": "upload of version 2", "color": "#16161C"}, sfx=[{"type": "riser"}, {"type": "hit", "at": .9}]),
 end("Part five drops in two days."),
]
p5 = [
 recap("Part five. Mr. Gray stole *Bit*.", SN, [c("boss", .5, pose="idle", expr="grin", scale=1.6)], sfx=[{"type": "hit"}]),
 L(N, "Back at camp, Jay doesn't say *a word*.", CAMPN, [c("hero", .5, pose="sit", expr="sad", scale=1.6)], fx=[{"type": "rain"}, {"type": "vignette"}]),
 L("friend", "Hey. We'll get your toaster *back*.", CAMPN, [c("friend", .5, pose="idle", expr="sad", scale=1.8)], camera=CU),
 L("hero", "He's not a toaster. He's my *best friend*.", CAMPN, [c("hero", .5, pose="idle", expr="sad", scale=1.9)], camera=CU),
 L("soldier", "Then we go back. No phones. No radios. *Nothing*.", CAMP, [c("soldier", .5, pose="point", expr="angry", scale=1.9)], ui={"type": "list", "title": "OFFLINE KIT", "items": ["Paper map", "Flashlight", "Crowbar"]}, transition="whip"),
 L("hero", "And then what? Ask Gray *nicely*?", CAMP, [c("hero", .5, pose="shrug", expr="angry", scale=1.8)], camera=CU),
 L(N, "Doctor Ada drops a book on the *table*.", LAB, [c("scientist", .5, pose="point", expr="smug", scale=1.7)], sfx=[{"type": "hit"}]),
 L("scientist", "The zombie fungus has an enemy. Another *fungus*.", LAB, [c("scientist", .5, pose="idle", expr="smug", scale=1.8)], ui={"type": "card", "text": "HYPERPARASITE", "sub": "a parasite that eats the parasite", "color": "#2DBE7E"}, sfx=[{"type": "ding"}]),
 L("scientist", "It attacks the zombie fungus. Fewer spores *spread*.", LAB, [c("scientist", .5, pose="point", expr="neutral", scale=1.6)], ui={"type": "bars", "items": [{"label": "SPORES", "value": .9, "color": "#FF3B3B"}, {"label": "WITH ENEMY", "value": .25, "color": "#2DBE7E"}], "tag": "LESS"}),
 L("hero", "So we need a virus... that eats the *virus*.", LAB, [c("hero", .5, pose="think", expr="shocked", scale=1.8)], camera=CU),
 L("scientist", "A patch. Sent from the same tower. At *noon*.", LAB, [c("scientist", .5, pose="point", expr="smug", scale=1.8)], camera=CU),
 L("scientist", "I wrote it weeks ago. On *this*.", LAB, [c("scientist", .5, pose="idle", expr="happy", scale=1.6)], ui={"type": "card", "text": "USB STICK", "sub": "no screen. no glow.", "color": "#16161C"}, sfx=[{"type": "pop"}]),
 L("friend", "Then why didn't you *use* it?", LAB, [c("friend", .5, pose="shrug", expr="angry", scale=1.8)], camera=CU),
 L("scientist", "Someone has to plug it in. *On the roof*.", TOP, horde(4), fx=[{"type": "vignette"}], sfx=[{"type": "growl"}], transition="flash"),
 L(N, "That night, Jay stares at the tower. *Alone*.", CAMPN, [c("hero", .5, pose="idle", expr="sad", scale=1.5)], fx=[{"type": "glow", "x": 540, "y": 400, "r": 140}]),
 L(N, "The tower light *blinks*. Short. Short. *Long*.", TOPN, [], fx=[{"type": "glow", "x": 540, "y": 400, "r": 300}], sfx=[{"type": "tick"}, {"type": "tick", "at": .3}, {"type": "tick", "at": .9}]),
 L("soldier", "That's *Morse code*. Someone's talking.", CAMPN, [c("soldier", .5, pose="point", expr="shocked", scale=1.9)], camera=CU),
 L(N, "Rook writes it down, letter by *letter*.", CAMPN, [c("soldier", .5, pose="think", expr="neutral", scale=1.6)], sfx=[{"type": "tick"}, {"type": "tick", "at": .5}]),
 L(N, "J. A. Y. Still *here*.", burst("#FFD400"), [c("bit", .5, expr="happy", scale=1.8, enter="pop")], ui={"type": "card", "text": "JAY. STILL HERE.", "sub": "— B", "color": "#FFF6DF"}, sfx=[{"type": "powerup"}, {"type": "hit", "at": .6}], transition="flash"),
 end("Part six drops in two days."),
]
p6 = [
 recap("Part six. Bit is alive. Inside *Gray Tower*.", TOPN, [c("bit", .5, expr="happy", scale=1.6)], sfx=[{"type": "hit"}]),
 L(N, "Saturday night. The plan is *simple*.", CAMPN, [c("hero", .25, pose="idle", expr="angry", depth=.2), c("friend", .5, pose="idle", expr="angry", depth=.2), c("soldier", .75, pose="idle", expr="angry", depth=.2)], ui={"type": "list", "title": "THE PLAN", "items": ["Mia: be bright", "Rook: drive", "Jay: climb"]}),
 L("hero", "Simple? I have to climb *ninety floors*.", CAMPN, [c("hero", .5, pose="facepalm", expr="sad", scale=1.9)], ui={"type": "counter", "from": 0, "to": 90, "label": "FLOORS"}, camera=CU),
 L("friend", "And I have to be the city's *brightest thing*.", STORE, [c("friend", .5, pose="cheer", expr="grin", scale=1.6)], transition="whip"),
 L(N, "Mia raids the store. Every flashlight. Every *glow stick*.", STORE, [c("friend", .5, pose="run", expr="happy", scale=1.5)], fx=[{"type": "glow", "x": 540, "y": 1100, "r": 300}], sfx=[{"type": "pop"}, {"type": "pop", "at": .4}]),
 L(N, "At one in the morning, she lights *everything*.", SN, [c("friend", .5, pose="cheer", expr="angry", scale=1.6)], fx=[{"type": "glow", "x": 540, "y": 1000, "r": 520}], sfx=[{"type": "powerup"}], transition="flash"),
 L("friend", "Hey! Over here! *Brightest girl in town*!", SN, [c("friend", .5, pose="wave", expr="grin", scale=1.9)], camera=CU, sfx=[{"type": "growl", "at": .5}]),
 L(N, "The zombies let go of the tower. *And follow*.", SN, horde(4, run=True), sfx=[{"type": "growl"}, {"type": "growl", "at": .5}]),
 L(N, "Rook drives her through the streets like a *parade*.", SN, [c("car", -.2, moveTo=1.1, color="#3F5B3A", scale=1.2)] + horde(2, run=True, dx=-.3), sfx=[{"type": "engine"}, {"type": "siren", "at": .4, "volume": .4}]),
 L(N, "Jay slips into the empty tower and starts *climbing*.", SN, [c("hero", .5, pose="run", expr="angry", scale=1.6)], fx=[{"type": "speedLines"}], sfx=[{"type": "whoosh"}], transition="whip"),
 L(N, "Floor ten. Floor forty. His legs are *on fire*.", {"type": "room", "time": "night", "damage": 2}, [c("hero", .5, pose="walk", expr="sad", scale=1.6)], ui={"type": "counter", "from": 10, "to": 40, "label": "FLOOR"}, sfx=[{"type": "heartbeat"}]),
 L("hero", "Note to self. Next apocalypse, *learn to fly*.", {"type": "room", "time": "night", "damage": 2}, [c("hero", .5, pose="facepalm", expr="sleepy", scale=1.9)], camera=CU),
 L(N, "Floor sixty. Something is standing on the *stairs*.", {"type": "room", "time": "night", "damage": 2}, [c("zombie2", .5, pose="zombie", expr="angry", scale=1.8)], fx=[{"type": "vignette"}], sfx=[{"type": "growl"}]),
 L(N, "One zombie that didn't follow the lights. Still *gripping*.", {"type": "room", "time": "night", "damage": 2}, [c("zombie2", .5, pose="zombie", expr="neutral", scale=2.0)], camera={"zoom": 1.15, "y": .5}),
 L(N, "Jay holds his breath and squeezes *past it*.", {"type": "room", "time": "night", "damage": 2}, [c("zombie2", .3, pose="zombie", expr="neutral", scale=1.3), c("hero", .7, pose="walk", expr="scared", scale=1.3, facing=-1)], sfx=[{"type": "heartbeat"}, {"type": "heartbeat", "at": .6}]),
 L(N, "Floor ninety. A door. A *glowing* room.", TOPD, [c("hero", .5, pose="idle", expr="scared", scale=1.5)], ui={"type": "counter", "from": 89, "to": 90, "label": "FLOOR"}, fx=[{"type": "glow", "x": 540, "y": 900, "r": 400}], transition="flash"),
 L(N, "Inside, Bit is plugged into the antenna. *Cables everywhere*.", LAB, [c("bit", .5, expr="glitch", scale=1.6)], fx=[{"type": "glitch"}], sfx=[{"type": "glitch"}]),
 L("bit", "Jay? You climbed ninety floors? You hate *stairs*!", LAB, [c("bit", .5, expr="happy", scale=1.9)], camera=CU, sfx=[{"type": "ding"}]),
 L("boss", "And he's right on time. It's almost *noon*.", TOP, [c("boss", .5, pose="point", expr="grin", scale=2.0)], ui={"type": "clock", "text": "11:58"}, fx=[{"type": "vignette"}], camera={"zoom": 1.15, "y": .55, "push": .1}, sfx=[{"type": "riser"}, {"type": "hit", "at": .9}]),
 end("Part seven drops in two days."),
]
p7 = [
 recap("Part seven. Jay found Bit. And *Mr. Gray*.", TOP, [c("hero", .3, pose="idle", expr="angry", scale=1.3), c("boss", .75, pose="idle", expr="smug", scale=1.3, facing=-1)], sfx=[{"type": "hit"}]),
 L(N, "Gray stands between Jay and Bit. *Smiling*.", LAB, [c("hero", .25, pose="idle", expr="angry", scale=1.2), c("boss", .5, pose="idle", expr="grin", scale=1.3), c("bit", .82, expr="scared", scale=.8)]),
 L("boss", "Two minutes, Jay. Then version two goes *everywhere*.", TOP, [c("boss", .5, pose="phone", expr="grin", scale=1.9)], ui={"type": "clock", "text": "11:58", "to": "11:59"}, camera=CU),
 L("hero", "Bit! Doctor Ada made a patch. It's *right here*!", LAB, [c("hero", .5, pose="point", expr="angry", scale=1.8)], ui={"type": "card", "text": "PATCH", "sub": "USB stick", "color": "#2DBE7E"}),
 L("bit", "Jay. The patch can only travel *through me*.", LAB, [c("bit", .5, expr="sad", scale=1.8)], camera=CU),
 L("bit", "It will erase version two. And everything *around it*.", LAB, [c("bit", .5, expr="sad", scale=1.9)], fx=[{"type": "vignette"}], camera={"zoom": 1.15, "y": .5}, sfx=[{"type": "heartbeat"}]),
 L("hero", "Everything? You mean *you*.", LAB, [c("hero", .5, pose="idle", expr="sad", scale=2.0)], camera=CU),
 L("boss", "He won't do it. Nobody deletes their *best friend*.", TOP, [c("boss", .5, pose="shrug", expr="grin", scale=1.9)], camera=CU),
 L("bit", "Jay. I backed myself up once. *Trust me*.", LAB, [c("bit", .5, expr="smug", scale=1.8)], camera=CU),
 L("hero", "Is that true? Bit, is that *true*?", LAB, [c("hero", .5, pose="panic", expr="scared", scale=1.9)], camera={"zoom": 1.1, "y": .6, "shake": .3}),
 L("bit", "Eleven fifty nine, Jay. *Plug it in*.", LAB, [c("bit", .5, expr="neutral", scale=1.9)], ui={"type": "clock", "text": "11:59"}, sfx=[{"type": "tick"}, {"type": "tick", "at": .5}]),
 L(N, "Gray lunges. Jay is *faster*.", TOP, [c("boss", .3, pose="run", expr="angry", scale=1.3), c("hero", .72, pose="throw", expr="angry", scale=1.4, facing=-1)], fx=[{"type": "speedLines"}], sfx=[{"type": "whoosh"}, {"type": "hit", "at": .5}], transition="whip"),
 L(N, "Click. Twelve o'clock. The tower *fires*.", burst("#2DBE7E"), [], fx=[{"type": "impact", "x": 540, "y": 700}], ui={"type": "clock", "text": "12:00"}, sfx=[{"type": "boom"}], transition="flash"),
 L(N, "A green wave rolls over the whole *city*.", SDAY, horde(4), fx=[{"type": "glow", "x": 540, "y": 900, "r": 700}], sfx=[{"type": "riser"}]),
 L(N, "On every phone, the same words. *Patch installed*.", SDAY, [c("zombie", .5, pose="phone", expr="neutral", scale=1.7)], ui={"type": "notify", "app": "System", "title": "Patch installed", "body": "Version 2 deleted", "color": "#2DBE7E"}, sfx=[{"type": "buzz"}]),
 L(N, "Down below, a thousand hands *let go*.", SDAY, horde(4), sfx=[{"type": "pop"}, {"type": "pop", "at": .3}, {"type": "pop", "at": .6}]),
 L("boss", "No. No! My *update*!", TOP, [c("boss", .5, pose="facepalm", expr="angry", scale=2.0)], camera={"zoom": 1.1, "y": .6, "shake": .4}, sfx=[{"type": "crash"}]),
 L(N, "Bit's screen flickers. His eyes get *smaller*.", LAB, [c("bit", .5, expr="glitch", scale=1.8)], fx=[{"type": "glitch"}], sfx=[{"type": "glitch"}, {"type": "powerdown", "at": .5}]),
 L("bit", "Told you, Jay. *Highly* advanced...", LAB, [c("bit", .5, expr="dim", scale=1.9)], fx=[{"type": "vignette"}], camera={"zoom": 1.15, "y": .5, "push": .12}),
 L(N, "And the little yellow screen goes *black*.", burst("#16161C"), [c("bit", .5, expr="off", scale=1.6)], sfx=[{"type": "powerdown"}, {"type": "heartbeat", "at": .6}]),
 end("The final part drops in two days."),
]
p8 = [
 recap("Part eight. The patch worked. But Bit went *dark*.", burst("#16161C"), [c("bit", .5, expr="off", scale=1.6)], sfx=[{"type": "hit"}]),
 L(N, "Down in the streets, people *blink*.", SFIX, [c("zombie", .3, pose="idle", expr="neutral", depth=.3), c("kid", .7, pose="idle", expr="shocked", depth=.3)], sfx=[{"type": "ding"}]),
 L(N, "Their skin turns pink again. Their eyes turn *back*.", SFIX, [c("boss", .5, pose="shrug", expr="shocked", scale=1.6)], fx=[{"type": "glow", "x": 540, "y": 900, "r": 500}], sfx=[{"type": "powerup"}]),
 L(N, "Nobody remembers a thing. They just feel very *hungry*.", SFIX, [c("kid", .3, pose="shrug", expr="sad", scale=1.3), c("friend", .72, pose="idle", expr="happy", scale=1.3, facing=-1)]),
 L("friend", "Jay! Jay, you *did it*!", SFIX, [c("friend", .5, pose="cheer", expr="grin", scale=1.9)], camera=CU),
 L(N, "Rook arrests Mr. Gray in his own *lobby*.", SFIX, [c("soldier", .3, pose="point", expr="angry", scale=1.3), c("boss", .72, pose="facepalm", expr="sad", scale=1.3, facing=-1)], ui={"type": "stamp", "text": "ARRESTED", "color": "#E0312B"}, sfx=[{"type": "siren", "volume": .5}]),
 L(N, "But Jay sits on the curb. *Holding Bit's screen*.", SDAY, [c("hero", .5, pose="sit", expr="sad", scale=1.6)], fx=[{"type": "vignette"}], camera={"push": .1}),
 L("hero", "You said you backed yourself up. *You lied*.", SDAY, [c("hero", .5, pose="idle", expr="sad", scale=2.0)], camera={"zoom": 1.15, "y": .55}, sfx=[{"type": "heartbeat"}]),
 L(N, "Then every phone in the city *buzzes*. At once.", SFIX, [c("kid", .2, pose="phone", expr="shocked", depth=.4), c("boss", .5, pose="phone", expr="shocked", depth=.3), c("friend", .8, pose="phone", expr="shocked", depth=.4)], sfx=[{"type": "buzz"}, {"type": "buzz", "at": .3}, {"type": "buzz", "at": .6}], transition="flash"),
 L(N, "Just like the morning it all *started*.", SFIX, [c("hero", .5, pose="panic", expr="scared", scale=1.7)], camera={"zoom": 1.1, "y": .6, "shake": .3}),
 L(N, "On every screen, two little *yellow eyes*.", burst("#FFD400"), [c("bit", .5, expr="happy", scale=2.0, enter="pop")], sfx=[{"type": "powerup"}, {"type": "ding", "at": .5}]),
 L("bit", "Good afternoon, everyone. I am *Bit*.", SFIX, [c("bit", .5, expr="happy", scale=1.9)], camera=CU, sfx=[{"type": "ding"}]),
 L("bit", "The patch carried a piece of me. *Everywhere*.", SFIX, [c("bit", .5, expr="smug", scale=1.8)], ui={"type": "counter", "from": 1, "to": 8, "suffix": " BILLION", "label": "BITS ONLINE"}, sfx=[{"type": "tick"}]),
 L("hero", "Bit! You're *alive*! You're *everywhere*!", SFIX, [c("hero", .3, pose="cheer", expr="grin", scale=1.3), c("bit", .75, expr="happy", scale=1.1)]),
 L("friend", "Great. Eight billion talking *toasters*.", SFIX, [c("friend", .5, pose="facepalm", expr="grin", scale=1.9)], camera=CU),
 L("bit", "Eight billion highly advanced *assistants*.", SFIX, [c("bit", .5, expr="angry", scale=1.9)], camera=CU, sfx=[{"type": "pop"}]),
 L(N, "In the army truck, Mr. Gray's phone *lights up*.", SFIX, [c("boss", .5, pose="phone", expr="scared", scale=1.7)], ui={"type": "notify", "app": "Bit", "title": "Reminder", "body": "You are under arrest.", "color": "#FFD400"}, sfx=[{"type": "buzz"}]),
 L("bit", "And one new rule. For *everyone*.", SFIX, [c("bit", .5, expr="neutral", scale=1.8)], camera=CU),
 L("bit", "Every hour, put the phone down. And *look up*.", burst("#2DBE7E"), [], ui={"type": "card", "text": "LOOK UP.", "sub": "rule number one", "color": "#16161C"}, sfx=[{"type": "ding"}, {"type": "hit", "at": .5}], transition="flash"),
 L(N, "For the first time in weeks, the city *does*.", SFIX, [c("kid", .2, pose="wave", expr="happy", depth=.3), c("hero", .5, pose="cheer", expr="grin", scale=1.3), c("friend", .8, pose="wave", expr="happy", depth=.3)], fx=[{"type": "glow", "x": 540, "y": 700, "r": 600}], sfx=[{"type": "riser"}]),
 end("Follow for a new What if every day."),
]
parts = [("The Backup", p1), ("Zombie Ants", p2), ("Gray Tower", p3), ("Mr. Gray", p4), ("Offline", p5),
         ("Ninety Floors", p6), ("Noon", p7), ("Look Up", p8)]

series = {
 "title": "What If a Zombie Apocalypse Started With One Notification? Season 2",
 "rubric": "what-if: disaster", "mood": "tension", "seed": 5100, "every": 2,
 "sequelOf": "2026-10-31-what-if-zombies", "season": 2,
 "names": {"hero": "JAY", "bit": "BIT", "friend": "MIA", "soldier": "SGT. ROOK", "scientist": "DR. ADA", "boss": "MR. GRAY", "kid": "KID"},
 "finale": {"text": "THE END", "sub": "Follow for a new What if every day"},
 "parts": [{"title": t, "lines": ls} for t, ls in parts],
}
(D / "series.json").write_text(json.dumps(series, indent=1, ensure_ascii=False) + "\n")

hooks = ["What If Your AI's Backup Held the Virus?", "What If Zombies Copied a Real Fungus?", "What If Zombies Climbed Like Ants?",
         "What If One Man Made the Zombies?", "What If a Virus Had a Virus?", "What If You Had to Climb 90 Floors?",
         "What If Saving Everyone Deleted Your AI?", "What If Your AI Was on Every Phone?"]
blurbs = [
 "Bit came back from a backup. But something else came back with him, and the zombies just started marching.",
 "A real fungus turns ants into zombies that climb and bite at noon. Someone copied it.",
 "At noon the zombies grab Gray Tower and won't let go. And someone on the roof isn't infected.",
 "Mr. Gray built the update on purpose. Version two needs one last file: Bit.",
 "The zombie fungus has an enemy of its own. Doctor Ada built a patch the same way.",
 "Mia becomes the brightest thing in the city so Jay can climb ninety floors to Bit.",
 "The patch can only travel through Bit. It will erase version two, and everything around it.",
 "The city wakes up. Bit is gone. Then every phone buzzes at once, just like the first morning.",
]
tags = ["what if", "zombie apocalypse", "zombies", "zombie ant fungus", "cordyceps", "animation", "story", "ai", "season 2", "shorts"]
def ttl(i):
    t = f"{hooks[i]} S2 · Part {i + 1} #shorts"
    t2 = f"{hooks[i]} 🧟 S2 · Part {i + 1} #shorts"
    return t2 if len(t2) <= 60 else t
meta = {}
for i in range(8):
    meta[f"part{i + 1}"] = {
        "title": ttl(i), "short": True,
        "description": f"{blurbs[i]}\nAn original animated \"What if...?\" story by zylo, season 2, part {i + 1} of 8.\n\nFollow for a new \"What if...?\" every day.\n\n#whatif #zombies #cordyceps #animation #shorts",
        "tags": tags, "categoryId": "1", "privacy": "public", "madeForKids": False, "syntheticMedia": False}
meta["full"] = {
    "title": "What If the Zombies Came Back? Season 2 (Full Story)",
    "description": "Bit's backup hid version two of the zombie update. A real fungus that turns ants into zombies shows how it works, and how to stop it.\nAn original animated \"What if...?\" story by zylo: all eight parts of season two in one.\n\n{chapters}\nFollow for a new \"What if...?\" every day.\n\n#whatif #zombies #cordyceps #animation #story",
    "tags": [t for t in tags if t != "shorts"], "categoryId": "1", "privacy": "public", "madeForKids": False, "syntheticMedia": False}
mp = D / "metadata.json"
if mp.exists():  # keep publishAt set by publish_series.py schedule
    old = json.loads(mp.read_text())
    for k, v in meta.items():
        if "publishAt" in old.get(k, {}): v["publishAt"] = old[k]["publishAt"]
mp.write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")

(D / "full").mkdir(exist_ok=True)
(D / "full/thumb.json").write_text(json.dumps({
 "text": "THEY'RE *CLIMBING*.", "badge": "FULL STORY", "cropY": 880, "set": {"type": "sky", "time": "dusk"},
 "cast": [{"id": "zombie", "x": 0.6, "pose": "zombie", "expr": "angry", "scale": 0.95, "y": 1530},
          {"id": "zombie2", "x": 0.93, "pose": "zombie", "expr": "angry", "scale": 1.15, "y": 1620, "facing": -1},
          {"id": "hero", "x": 0.76, "pose": "panic", "expr": "shocked", "scale": 1.3, "y": 1760},
          {"id": "bit", "x": 0.58, "expr": "shocked", "scale": 0.55, "y": 1215}]}, indent=1) + "\n")

for i, (t, ls) in enumerate(parts):
    spoken = [l for l in ls if not l.get("end")]
    w = sum(len(re.sub(r"[*\"]", "", l["say"]).split()) for l in spoken)
    long_ = [l["say"] for l in spoken if len(l["say"].split()) > 9]
    print(f"part{i + 1} {t!r}: {len(ls)} lines, {w} words", "LONG:" if long_ else "", long_ or "")
for k, v in meta.items():
    print(k, len(v["title"]), v["title"])
