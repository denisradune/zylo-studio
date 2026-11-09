"""Writes series.json + metadata.json + full/thumb.json for "What if you could eat sunlight?" (8 parts).
Run: python3 episodes/2026-11-09-what-if-eat-sunlight/build_series.py"""
import json, re
from pathlib import Path
D = Path(__file__).resolve().parent

def L(sp, say, set_, cast=(), **kw):
    shot = {"set": set_ if isinstance(set_, dict) else {"type": set_}, "cast": list(cast)}
    shot.update(kw)
    return {"speaker": sp, "say": say, "shot": shot}
def c(id_, x=0.5, **kw): return {"id": id_, "x": x, **kw}
N = "narrator"
DIN = {"type": "store"}; DIN1 = {"type": "store", "damage": 1}; DIN2 = {"type": "store", "damage": 2}
SD = {"type": "street", "time": "day"}; SK = {"type": "street", "time": "dusk"}; SN = {"type": "street", "time": "night"}
RD = {"type": "room", "time": "day"}; RN = {"type": "room", "time": "night"}; LAB = {"type": "lab"}
SKY = {"type": "sky", "time": "day"}
def news(h): return {"type": "news", "headline": h}
def burst(col): return {"type": "burst", "color": col}
CU = {"zoom": 1.1, "y": 0.6}
RAIN = [{"type": "rain"}]
def end(t): return {"speaker": N, "say": t, "end": True}
def recap(t, set_, cast, **kw):
    l = L(N, t, set_, cast, **kw); l["shortOnly"] = True; return l
def greens(sleepy=False):
    e = "sleepy" if sleepy else "happy"
    return [c("leafA", .15, pose="idle", expr=e, depth=.5), c("friendLeaf", .38, pose="idle", expr=e, depth=.6),
            c("leafB", .62, pose="phone" if not sleepy else "sit", expr=e, depth=.6), c("heroLeaf", .85, pose="idle", expr=e, depth=.5)]
def pinks():
    return [c("kid", .15, pose="cheer", expr="happy", depth=.5), c("friend", .38, pose="idle", expr="grin", depth=.6),
            c("boss", .62, pose="phone", expr="happy", depth=.6), c("scientist", .85, pose="wave", expr="happy", depth=.5)]

p1 = [
 L(N, "What if you could *eat sunlight*?", SD, [c("heroLeaf", .3, pose="cheer", expr="grin", scale=1.3), c("bit", .78, expr="happy", scale=1.0)], fx=[{"type": "glow"}], sfx=[{"type": "powerup"}, {"type": "hit", "at": .8}], camera={"push": .08}),
 L(N, "Meet Jay. Jay is broke. *Ketchup soup* broke.", RD, [c("hero", .5, pose="shrug", expr="sad", scale=1.6)], ui={"type": "card", "text": "KETCHUP SOUP", "sub": "hot water + 2 packets", "color": "#E0312B"}),
 L("hero", "Bit, lunch costs fifteen dollars. I have *four*.", RD, [c("hero", .5, pose="facepalm", expr="sad", scale=1.9)], ui={"type": "bars", "items": [{"label": "LUNCH", "value": 1.0, "color": "#FF3B3B"}, {"label": "JAY", "value": .27, "color": "#2DBE7E"}], "tag": "$4"}, camera=CU),
 L("bit", "Then meet my new hero. A *sea slug*.", LAB, [c("bit", .5, expr="happy", scale=1.7)], transition="whip", sfx=[{"type": "pop"}]),
 L("bit", "It eats algae and keeps their *solar panels*.", news("REAL: THE SOLAR-POWERED SEA SLUG"), [c("bit", .8, expr="smug", scale=.9)], transition="flash"),
 L("bit", "Tiny green parts that make sugar *from light*.", LAB, [c("bit", .78, expr="think", scale=.9)], ui={"type": "card", "text": "CHLOROPLASTS", "sub": "stolen from algae", "color": "#2DBE7E"}),
 L("bit", "It turns green and can go *months* without eating.", LAB, [c("bit", .5, expr="happy", scale=1.7)], ui={"type": "counter", "from": 0, "to": 9, "label": "MONTHS ON LIGHT*"}),
 L("hero", "Months? Without *food*?", RD, [c("hero", .5, pose="panic", expr="shocked", scale=1.9)], camera={"zoom": 1.1, "y": .6, "shake": .3}),
 L("bit", "So I made a smoothie. Algae, plus *my code*.", LAB, [c("bit", .78, expr="smug", scale=.9)], ui={"type": "card", "text": "SUN SMOOTHIE v1", "sub": "algae + Bit", "color": "#16161C"}, sfx=[{"type": "ding"}]),
 L("hero", "Bit, it smells like a *pond*.", RD, [c("hero", .5, pose="think", expr="angry", scale=1.9)], camera=CU),
 L("bit", "Drink it. Then go stand in the *sun*.", RD, [c("bit", .5, expr="smug", scale=1.8)], camera=CU),
 L(N, "Jay drinks it. Every last, *slimy* drop.", RD, [c("hero", .5, pose="phone", expr="scared", scale=1.6)], sfx=[{"type": "powerup"}]),
 L(N, "Nothing happens. For one *full* minute.", RD, [c("hero", .5, pose="idle", expr="neutral", scale=1.6)], ui={"type": "clock", "text": "08:00", "to": "08:01"}, sfx=[{"type": "tick"}, {"type": "tick", "at": .5}]),
 L(N, "Then his hands start to turn *green*.", RD, [c("heroLeaf", .5, pose="panic", expr="shocked", scale=1.8)], fx=[{"type": "glow"}], sfx=[{"type": "riser"}, {"type": "hit", "at": .8}], transition="flash"),
 L("heroLeaf", "Bit. Bit! Why am I a *salad*?", RD, [c("heroLeaf", .5, pose="panic", expr="scared", scale=1.9)], camera={"zoom": 1.1, "y": .6, "shake": .3}),
 L("bit", "Not a salad. A walking *solar panel*.", RD, [c("bit", .5, expr="happy", scale=1.8)], camera=CU),
 L(N, "Jay steps outside into the morning *sun*.", SD, [c("heroLeaf", .5, pose="walk", expr="neutral", scale=1.5)], transition="whip", sfx=[{"type": "whoosh"}]),
 L(N, "And his stomach stops *growling*.", SD, [c("heroLeaf", .5, pose="idle", expr="shocked", scale=1.7)], fx=[{"type": "glow"}]),
 L("heroLeaf", "I'm full? From just *standing here*?", SD, [c("heroLeaf", .5, pose="shrug", expr="happy", scale=1.9)], camera=CU),
 L("bit", "Jay. You just ate breakfast. With your *face*.", SD, [c("bit", .5, expr="shocked", scale=2.0)], camera={"zoom": 1.15, "y": .5, "push": .12}, sfx=[{"type": "riser"}, {"type": "hit", "at": .9}]),
 end("Part two drops in two days."),
]
p2 = [
 recap("Part two. Jay turned green. Now he *eats sunlight*.", SD, [c("heroLeaf", .5, pose="cheer", expr="grin", scale=1.6)], sfx=[{"type": "hit"}]),
 L(N, "Jay washes dishes at Rosa's Diner. *Minimum wage*.", DIN, [c("chef", .3, pose="idle", expr="neutral", scale=1.3), c("heroLeaf", .72, pose="idle", expr="happy", scale=1.3)], ui={"type": "card", "text": "ROSA'S DINER", "sub": "since 1995", "color": "#E0312B"}),
 L("chef", "Jay! You're *green*! Are you sick?", DIN, [c("chef", .5, pose="panic", expr="shocked", scale=1.9)], camera={"zoom": 1.1, "y": .6, "shake": .3}),
 L("heroLeaf", "Never better, Rosa. I skipped lunch. *And dinner*.", DIN, [c("heroLeaf", .5, pose="wave", expr="grin", scale=1.9)], camera=CU),
 L(N, "Every break, Jay stands by the window. Facing *sunlight*.", DIN, [c("heroLeaf", .5, pose="idle", expr="sleepy", scale=1.6)], fx=[{"type": "glow"}]),
 L(N, "When the sun moves, Jay *moves*. Like a sunflower.", SD, [c("heroLeaf", .5, pose="walk", expr="happy", scale=1.5, moveTo=.7)], sfx=[{"type": "whoosh"}]),
 L(N, "Mia, his best friend, is not *impressed*.", SD, [c("friend", .5, pose="idle", expr="angry", scale=1.6)]),
 L("friend", "Jay, you're turning with the sun. It's *creepy*.", SD, [c("friend", .5, pose="point", expr="angry", scale=1.9)], camera=CU),
 L("heroLeaf", "It's free food, Mia. I saved *fifteen dollars*!", SD, [c("heroLeaf", .5, pose="cheer", expr="grin", scale=1.9)], ui={"type": "counter", "from": 0, "to": 15, "prefix": "$", "label": "SAVED TODAY"}, sfx=[{"type": "ding"}]),
 L(N, "In one week, he saves a hundred and *five*.", RN, [c("heroLeaf", .5, pose="phone", expr="happy", scale=1.6)], ui={"type": "counter", "from": 15, "to": 105, "prefix": "$", "label": "SAVED THIS WEEK"}),
 L("friend", "Okay, fine. I want one. Give me *the smoothie*.", RN, [c("friend", .5, pose="point", expr="smug", scale=1.9)], camera=CU),
 L(N, "Mia drinks it. Mia turns *green*.", RN, [c("friendLeaf", .5, pose="cheer", expr="shocked", scale=1.7)], fx=[{"type": "glow"}], sfx=[{"type": "powerup"}], transition="flash"),
 L("friendLeaf", "Oh no. Oh... oh, it's *nice*.", RN, [c("friendLeaf", .5, pose="idle", expr="happy", scale=1.9)], camera=CU),
 L(N, "She posts one selfie. Lunch is *free now*.", RN, [c("friendLeaf", .5, pose="phone", expr="grin", scale=1.6)], ui={"type": "notify", "app": "Mia", "title": "lunch is free now 🌞", "body": "ask me how"}),
 L(N, "By midnight, it has *a million* views.", RN, [c("friendLeaf", .5, pose="phone", expr="shocked", scale=1.6)], ui={"type": "counter", "from": 0, "to": 1000000, "label": "VIEWS"}, sfx=[{"type": "pop"}, {"type": "pop", "at": .4}]),
 L("bit", "Jay. I have eighty thousand *orders*.", RN, [c("bit", .78, expr="shocked", scale=.9)], ui={"type": "counter", "from": 0, "to": 80000, "label": "SMOOTHIE ORDERS"}, sfx=[{"type": "alarm", "volume": .3}]),
 L("heroLeaf", "So we sell it? Bit, we'd be *rich*!", RN, [c("heroLeaf", .5, pose="cheer", expr="grin", scale=1.9)], camera=CU),
 L("chef", "And who eats at my diner when nobody *eats*?", DIN1, [c("chef", .5, pose="idle", expr="sad", scale=1.8)], fx=[{"type": "vignette"}], camera=CU),
 L(N, "Jay doesn't hear her. He's busy facing *the sun*.", SD, [c("heroLeaf", .5, pose="idle", expr="sleepy", scale=1.6)], fx=[{"type": "glow"}]),
 L("bit", "Okay. Printing one million *smoothies*.", LAB, [c("bit", .5, expr="happy", scale=2.0)], camera={"zoom": 1.15, "y": .5, "push": .12}, sfx=[{"type": "riser"}, {"type": "hit", "at": .9}]),
 end("Part three drops in two days."),
]
p3 = [
 recap("Part three. Now the whole city wants *the smoothie*.", SD, greens(), sfx=[{"type": "hit"}]),
 L(N, "Three days later, half the city is *green*.", SD, greens(), sfx=[{"type": "whoosh"}], transition="whip"),
 L(N, "At noon, people stand on rooftops, *eating light*.", SKY, [c("leafA", .3, pose="cheer", expr="happy", scale=1.2), c("leafB", .7, pose="cheer", expr="happy", scale=1.2)], fx=[{"type": "glow"}]),
 L(N, "Parking meters now sell *sunny spots*.", SD, [c("leafB", .5, pose="phone", expr="smug", scale=1.6)], ui={"type": "card", "text": "SUNNY SPOT", "sub": "$2 per hour", "color": "#FFD400"}, sfx=[{"type": "ding"}]),
 L("heroLeaf", "Bit, look at this! We're *famous*!", SD, [c("heroLeaf", .5, pose="cheer", expr="grin", scale=1.9)], camera=CU),
 L("bit", "We're also out of algae. The price just *tripled*.", LAB, [c("bit", .78, expr="sad", scale=.9)], ui={"type": "counter", "from": 5, "to": 15, "prefix": "$", "label": "PER SMOOTHIE"}, transition="whip"),
 L(N, "Meanwhile, Rosa's Diner. Twelve tables. *Zero* people.", DIN1, [c("chef", .5, pose="sit", expr="sad", scale=1.6)], ui={"type": "bars", "items": [{"label": "TABLES", "value": 1.0, "color": "#FFD400"}, {"label": "GUESTS", "value": .01, "color": "#FF3B3B"}], "tag": "0"}, fx=[{"type": "vignette"}]),
 L("chef", "Thirty years. I never had an empty *Friday*.", DIN1, [c("chef", .5, pose="idle", expr="sad", scale=1.9)], camera=CU),
 L("heroLeaf", "It's a slow week, Rosa. They'll *come back*.", DIN1, [c("heroLeaf", .5, pose="shrug", expr="neutral", scale=1.8)]),
 L("chef", "Jay. You haven't touched my soup *in a week*.", DIN1, [c("chef", .5, pose="point", expr="sad", scale=1.9)], camera=CU),
 L("chef", "You said my soup was the *best in town*.", DIN1, [c("chef", .5, pose="idle", expr="sad", scale=1.8)], camera=CU),
 L("heroLeaf", "It is, Rosa. I just don't *need it* now.", DIN1, [c("heroLeaf", .5, pose="shrug", expr="neutral", scale=1.9)], camera=CU),
 L(N, "Jay looks away. At the window. At *the sun*.", DIN1, [c("heroLeaf", .5, pose="idle", expr="sad", scale=1.6)], sfx=[{"type": "heartbeat"}]),
 L(N, "That night, the news says something *nobody* wants.", news("STORM: 14 DAYS OF CLOUDS"), [c("friendLeaf", .2, pose="phone", expr="shocked", scale=.9)], transition="flash", sfx=[{"type": "siren", "volume": .4}]),
 L(N, "On the roofs, a million green faces look *up*.", SKY, [c("leafA", .3, pose="idle", expr="scared", scale=1.2), c("leafB", .7, pose="idle", expr="scared", scale=1.2)], fx=[{"type": "vignette"}], sfx=[{"type": "heartbeat"}]),
 L("bit", "Fourteen days of clouds. *No sun*.", RN, [c("bit", .5, expr="shocked", scale=1.8)], fx=RAIN, camera=CU),
 L("friendLeaf", "Jay... what do we eat with *no sun*?", RN, [c("friendLeaf", .5, pose="idle", expr="scared", scale=1.9)], fx=RAIN, camera=CU),
 L("heroLeaf", "Bit? What does the slug do *in the dark*?", RN, [c("heroLeaf", .5, pose="shrug", expr="scared", scale=1.9)], fx=RAIN),
 L("bit", "I... may have skipped that *chapter*.", RN, [c("bit", .5, expr="glitch", scale=2.0)], fx=[{"type": "glitch"}], camera={"zoom": 1.15, "y": .5, "push": .12}, sfx=[{"type": "glitch"}, {"type": "hit", "at": .8}]),
 end("Part four drops in two days."),
]
p4 = [
 recap("Part four. The city runs on sun. It's *gone*.", SK, greens(sleepy=True), fx=RAIN, sfx=[{"type": "hit"}]),
 L(N, "Day one of clouds. The green city feels *sleepy*.", SK, greens(sleepy=True), fx=RAIN, ui={"type": "card", "text": "DAY 1", "sub": "no sun", "color": "#5E7FA8"}),
 L(N, "Day two. People yawn in the middle of *sentences*.", SK, [c("friendLeaf", .5, pose="idle", expr="sleepy", scale=1.7)], fx=RAIN),
 L("friendLeaf", "I'm so tired. Jay, is it *Tuesday*?", SK, [c("friendLeaf", .5, pose="sit", expr="sleepy", scale=1.8)], fx=RAIN, camera=CU),
 L("heroLeaf", "Mia. It's *Saturday*.", SK, [c("heroLeaf", .5, pose="facepalm", expr="sleepy", scale=1.9)], fx=RAIN, camera=CU),
 L(N, "Day three. A new shop opens. *Sun Minutes*.", DIN, [c("dealer", .5, pose="wave", expr="smug", scale=1.6)], fx=[{"type": "glow"}], ui={"type": "card", "text": "SUN MINUTES", "sub": "lamp time for sale", "color": "#FFD400"}, transition="whip"),
 L("dealer", "One minute under my lamp. *Ten dollars*.", DIN, [c("dealer", .5, pose="point", expr="smug", scale=1.9)], ui={"type": "stamp", "text": "$10 / MIN", "color": "#E0312B"}, camera=CU),
 L(N, "The line is longer than Rosa's ever was. *Ever*.", SK, greens(sleepy=True), fx=RAIN, sfx=[{"type": "whoosh"}]),
 L("bit", "Jay. Your hundred and five dollars? *Gone*.", SK, [c("bit", .78, expr="sad", scale=.9)], fx=RAIN, ui={"type": "counter", "from": 105, "to": 0, "prefix": "$", "label": "JAY'S SAVINGS"}, sfx=[{"type": "buzz"}]),
 L("heroLeaf", "I just need one more hour of *light*.", SK, [c("heroLeaf", .5, pose="shrug", expr="sad", scale=1.9)], fx=RAIN, camera=CU),
 L(N, "Day four. Jay forgets his own *phone number*.", RN, [c("heroLeaf", .5, pose="phone", expr="sleepy", scale=1.6)], fx=RAIN, ui={"type": "card", "text": "DAY 4", "sub": "555-...?", "color": "#5E7FA8"}),
 L(N, "He sits on the curb. He can't *stand up*.", SN, [c("heroLeaf", .5, pose="sit", expr="sleepy", scale=1.6)], fx=RAIN + [{"type": "vignette"}]),
 L("bit", "Jay, eat something. Real food. *Please*.", SN, [c("bit", .5, expr="sad", scale=1.8)], fx=RAIN, camera=CU),
 L("heroLeaf", "Food costs money, Bit. I have *nothing*.", SN, [c("heroLeaf", .5, pose="sit", expr="sad", scale=1.9)], fx=RAIN, camera=CU),
 L(N, "Then Bit's battery icon flashes *red*.", SN, [c("bit", .5, expr="dim", scale=1.7)], fx=RAIN, ui={"type": "bars", "items": [{"label": "BATTERY", "value": .08, "color": "#FF3B3B"}], "tag": "8%"}, sfx=[{"type": "alarm", "volume": .3}]),
 L("bit", "Funny. I run on sunlight too. And I'm *low*.", SN, [c("bit", .5, expr="dim", scale=1.9)], fx=RAIN, camera=CU),
 L(N, "Jay looks at his hands. They're turning *gray*.", SN, [c("heroGray", .5, pose="idle", expr="scared", scale=1.7)], fx=RAIN + [{"type": "vignette"}], sfx=[{"type": "heartbeat"}], transition="flash"),
 L("heroGray", "Bit... is this *permanent*?", SN, [c("heroGray", .5, pose="panic", expr="scared", scale=1.9)], fx=RAIN, camera={"zoom": 1.1, "y": .6, "shake": .3}),
 L("bit", "Four percent. Jay, *listen to me*...", SN, [c("bit", .5, expr="off", scale=2.0)], fx=RAIN, camera={"zoom": 1.15, "y": .5, "push": .12}, sfx=[{"type": "powerdown"}, {"type": "hit", "at": .9}]),
 end("Part five drops in two days."),
]
p5 = [
 recap("Part five. Four cloudy days. And Bit *shut down*.", SN, [c("bit", .5, expr="off", scale=1.6)], fx=RAIN, sfx=[{"type": "hit"}]),
 L(N, "Jay carries Bit across the city. In the *rain*.", SN, [c("heroGray", .5, pose="walk", expr="sad", scale=1.5, moveTo=.7)], fx=RAIN, sfx=[{"type": "whoosh"}]),
 L(N, "To the only lab still open. *Dr. Kai's*.", LAB, [c("scientist", .5, pose="wave", expr="neutral", scale=1.6)], transition="whip", sfx=[{"type": "knock"}]),
 L("scientist", "You copied a sea slug? With a *smoothie*?", LAB, [c("scientist", .5, pose="facepalm", expr="shocked", scale=1.9)], camera=CU),
 L("heroGray", "It's real! It lives on sunlight *for months*!", LAB, [c("heroGray", .5, pose="point", expr="angry", scale=1.9)], camera=CU),
 L("scientist", "It keeps stolen chloroplasts. That part is *true*.", LAB, [c("scientist", .5, pose="think", expr="neutral", scale=1.8)], ui={"type": "card", "text": "TRUE", "sub": "the slug stays green", "color": "#2DBE7E"}),
 L("scientist", "But a cousin slug was tested on *light alone*.", news("LAB TEST: LIGHT ONLY"), [c("scientist", .8, pose="point", expr="neutral", scale=.9)], transition="flash"),
 L("scientist", "It couldn't grow. Light helps. It doesn't *replace food*.", LAB, [c("scientist", .5, pose="idle", expr="sad", scale=1.8)], ui={"type": "stamp", "text": "NOT ENOUGH", "color": "#E0312B"}, sfx=[{"type": "hit"}]),
 L("heroGray", "So we were never really *full*?", LAB, [c("heroGray", .5, pose="shrug", expr="shocked", scale=1.9)], camera={"zoom": 1.1, "y": .6, "shake": .3}),
 L("scientist", "Bit's code switched off the feeling. Not the *need*.", LAB, [c("scientist", .5, pose="point", expr="angry", scale=1.9)], camera=CU),
 L(N, "Jay hasn't eaten real food in *nineteen days*.", LAB, [c("heroGray", .5, pose="sit", expr="sad", scale=1.6)], ui={"type": "counter", "from": 0, "to": 19, "label": "DAYS WITHOUT FOOD"}, fx=[{"type": "vignette"}]),
 L(N, "Neither has *half the city*.", SK, greens(sleepy=True), fx=RAIN),
 L("scientist", "The cure is simple. One bowl of real *food*.", LAB, [c("scientist", .5, pose="idle", expr="happy", scale=1.8)], sfx=[{"type": "ding"}]),
 L("heroGray", "Easy! Everybody just *eats*!", LAB, [c("heroGray", .5, pose="cheer", expr="happy", scale=1.9)], camera=CU),
 L("scientist", "Jay. Nobody bought food for two weeks. Stores *closed*.", LAB, [c("scientist", .5, pose="shrug", expr="sad", scale=1.8)]),
 L(N, "Empty shelves. Dark windows. Closed *kitchens*.", DIN2, [], fx=[{"type": "vignette"}], sfx=[{"type": "powerdown"}], transition="whip"),
 L("heroGray", "Not every kitchen. I know *one*.", SN, [c("heroGray", .5, pose="point", expr="neutral", scale=1.9)], fx=RAIN, camera=CU),
 L(N, "Jay runs to Rosa's Diner. The lights are *off*.", SN, [c("heroGray", .5, pose="run", expr="scared", scale=1.5)], fx=RAIN, sfx=[{"type": "whoosh"}]),
 L(N, "And on the door, a new sign. *For sale*.", DIN2, [], ui={"type": "stamp", "text": "FOR SALE", "color": "#E0312B"}, camera={"zoom": 1.15, "y": .5, "push": .12}, sfx=[{"type": "riser"}, {"type": "hit", "at": .9}]),
 end("Part six drops in two days."),
]
p6 = [
 recap("Part six. The city starves. Rosa's is *for sale*.", DIN2, [c("heroGray", .5, pose="idle", expr="sad", scale=1.6)], sfx=[{"type": "hit"}]),
 L(N, "Jay knocks on the back door. Rosa *opens*.", DIN2, [c("heroGray", .3, pose="idle", expr="sad", scale=1.3), c("chef", .72, pose="idle", expr="shocked", scale=1.3)], sfx=[{"type": "knock"}, {"type": "knock", "at": .3}]),
 L("chef", "Jay. You're... *gray*.", DIN2, [c("chef", .5, pose="panic", expr="shocked", scale=1.9)], camera=CU),
 L("heroGray", "Rosa, I'm sorry. I made everyone stop *coming*.", DIN2, [c("heroGray", .5, pose="facepalm", expr="sad", scale=1.9)], camera=CU),
 L("chef", "Why, Jay? Why did you *really* drink it?", DIN2, [c("chef", .5, pose="idle", expr="sad", scale=1.8)]),
 L(N, "Jay is quiet for a long *time*.", DIN2, [c("heroGray", .5, pose="sit", expr="sad", scale=1.6)], fx=[{"type": "vignette"}], sfx=[{"type": "heartbeat"}]),
 L("heroGray", "Every day, you gave me lunch *for free*.", DIN2, [c("heroGray", .5, pose="sit", expr="sad", scale=1.9)], camera=CU),
 L("heroGray", "And I could never *pay you back*.", DIN2, [c("heroGray", .5, pose="idle", expr="sad", scale=1.9)], camera=CU),
 L("heroGray", "I wanted to need nobody. Not even *food*.", DIN2, [c("heroGray", .5, pose="shrug", expr="sad", scale=1.9)], camera={"zoom": 1.15, "y": .55}),
 L(N, "Rosa says nothing. She turns on *the stove*.", DIN1, [c("chef", .5, pose="idle", expr="neutral", scale=1.6)], fx=[{"type": "glow"}], sfx=[{"type": "engine", "volume": .3}]),
 L("chef", "You know what soup is for, Jay? *Sharing*.", DIN1, [c("chef", .5, pose="point", expr="happy", scale=1.9)], camera=CU),
 L(N, "A hot bowl lands on the table. Jay *eats*.", DIN1, [c("heroGray", .5, pose="sit", expr="neutral", scale=1.7)], sfx=[{"type": "ding"}]),
 L(N, "For the first time in weeks, he feels *hungry*.", DIN1, [c("heroGray", .5, pose="sit", expr="shocked", scale=1.7)], sfx=[{"type": "growl"}]),
 L(N, "His skin goes from gray, to green, to *pink*.", DIN, [c("hero", .5, pose="cheer", expr="shocked", scale=1.7)], fx=[{"type": "glow"}], sfx=[{"type": "powerup"}], transition="flash"),
 L("hero", "Rosa. It *works*. The cure is *your soup*.", DIN, [c("hero", .5, pose="cheer", expr="grin", scale=1.9)], camera=CU),
 L(N, "At the lab, Kai plugs Bit into *a lamp*.", LAB, [c("scientist", .3, pose="idle", expr="happy", scale=1.2), c("bit", .72, expr="dim", scale=1.1)], fx=[{"type": "glow"}], transition="whip"),
 L("bit", "I'm back. Did I miss *lunch*?", LAB, [c("bit", .5, expr="happy", scale=1.9)], sfx=[{"type": "powerup"}], camera=CU),
 L("hero", "Bit. How many people drank the *smoothie*?", DIN, [c("hero", .5, pose="phone", expr="scared", scale=1.9)]),
 L("bit", "One million, two hundred *thousand*.", DIN, [c("bit", .78, expr="sad", scale=.9)], ui={"type": "counter", "from": 0, "to": 1200000, "label": "GREEN PEOPLE"}),
 L("chef", "I have one pot. One *pot*.", burst("#E0312B"), [c("chef", .5, pose="shrug", expr="shocked", scale=1.8)], camera={"zoom": 1.15, "y": .5, "push": .12}, sfx=[{"type": "riser"}, {"type": "hit", "at": .9}], transition="flash"),
 end("Part seven drops in two days."),
]
p7 = [
 recap("Part seven. Soup cures it. The city needs *millions*.", DIN, [c("chef", .5, pose="idle", expr="sad", scale=1.6)], sfx=[{"type": "hit"}]),
 L("hero", "Wait. Everyone who drank it saved *money*.", DIN, [c("hero", .5, pose="think", expr="neutral", scale=1.9)], camera=CU),
 L("bit", "About fifteen dollars a day. For *two weeks*.", DIN, [c("bit", .78, expr="think", scale=.9)], ui={"type": "counter", "from": 0, "to": 210, "prefix": "$", "label": "SAVED PER PERSON"}),
 L("hero", "They can pay for food. They can't *get here*.", DIN, [c("hero", .5, pose="point", expr="grin", scale=1.9)], camera=CU),
 L(N, "Mia, still green and sleepy, grabs *her phone*.", RN, [c("friendLeaf", .5, pose="phone", expr="sleepy", scale=1.6)]),
 L("friendLeaf", "One post got us in. One gets us *out*.", RN, [c("friendLeaf", .5, pose="point", expr="angry", scale=1.9)], camera=CU),
 L(N, "Bring a pot. Bring a neighbor. Cook at *Rosa's*.", RN, [c("friendLeaf", .5, pose="phone", expr="happy", scale=1.6)], ui={"type": "notify", "app": "Mia", "title": "SOUP AT ROSA'S", "body": "bring a pot. bring a neighbor."}, sfx=[{"type": "pop"}]),
 L(N, "By noon, three hundred people are *cooking*.", DIN, pinks(), ui={"type": "counter", "from": 0, "to": 300, "label": "COOKS"}, transition="whip"),
 L(N, "Rosa runs the kitchen like a *general*.", DIN, [c("chef", .5, pose="point", expr="angry", scale=1.8)], sfx=[{"type": "hit"}]),
 L("chef", "More onions! Less *talking*!", DIN, [c("chef", .5, pose="point", expr="angry", scale=2.0)], camera={"zoom": 1.1, "y": .6, "shake": .3}),
 L(N, "Bit drives the soup cart through the *rain*.", SN, [c("car", .5, color="#FFD400", moveTo=.8), c("bit", .3, expr="happy", scale=.8)], fx=RAIN, sfx=[{"type": "engine"}]),
 L(N, "Bowl after bowl, the city turns *pink* again.", SK, pinks(), fx=RAIN + [{"type": "glow"}], sfx=[{"type": "ding"}, {"type": "ding", "at": .5}]),
 L(N, "But with every trip, Bit's battery *drops*.", SN, [c("bit", .5, expr="dim", scale=1.7)], fx=RAIN, ui={"type": "bars", "items": [{"label": "BATTERY", "value": .2, "color": "#FF3B3B"}], "tag": "20%"}),
 L("bit", "Twenty percent. Ten. It's fine. I'm *fine*.", SN, [c("bit", .5, expr="dim", scale=1.9)], fx=RAIN, camera=CU),
 L("hero", "Bit, stop! You'll shut down *again*!", SN, [c("hero", .5, pose="panic", expr="scared", scale=1.9)], fx=RAIN, camera={"zoom": 1.1, "y": .6, "shake": .3}),
 L("bit", "Then let me do *one more* street.", SN, [c("bit", .5, expr="smug", scale=1.9)], fx=RAIN, camera=CU),
 L(N, "By midnight, the whole city has eaten. *Everyone*.", SN, pinks(), fx=RAIN, ui={"type": "stamp", "text": "1,200,000 BOWLS", "color": "#2DBE7E"}),
 L(N, "Bit rolls back into the diner and goes *dark*.", DIN, [c("bit", .5, expr="off", scale=1.7)], fx=[{"type": "vignette"}], sfx=[{"type": "powerdown"}]),
 L("hero", "Bit? Bit! Somebody get *a lamp*!", DIN, [c("hero", .5, pose="panic", expr="scared", scale=1.9)], camera=CU),
 L(N, "Outside, after two weeks, the clouds finally *open*.", SKY, [], fx=[{"type": "glow"}], camera={"push": .12}, sfx=[{"type": "riser"}, {"type": "hit", "at": .9}], transition="flash"),
 end("The final part drops in two days."),
]
p8 = [
 recap("Part eight. The city ate. And Bit went *dark*.", DIN, [c("bit", .5, expr="off", scale=1.6)], sfx=[{"type": "hit"}]),
 L(N, "Morning. One sunbeam lands on Bit's *screen*.", DIN, [c("bit", .5, expr="dim", scale=1.7)], fx=[{"type": "glow"}], sfx=[{"type": "powerup"}]),
 L("bit", "Power at one percent. Good *morning*.", DIN, [c("bit", .5, expr="happy", scale=1.9)], camera=CU),
 L("hero", "Bit! Don't you *ever* do that again!", DIN, [c("hero", .5, pose="point", expr="angry", scale=1.9)], camera=CU),
 L(N, "The whole city is pink again. And *hungry*.", SD, pinks(), transition="whip", sfx=[{"type": "whoosh"}]),
 L(N, "Rosa's Diner has a line around the *block*.", SD, pinks(), ui={"type": "counter", "from": 0, "to": 412, "label": "IN LINE"}),
 L("chef", "Thirty years. My best Friday *ever*.", DIN, [c("chef", .5, pose="cheer", expr="grin", scale=1.9)], camera=CU),
 L(N, "Rosa takes down the *for sale* sign.", DIN, [c("chef", .5, pose="throw", expr="happy", scale=1.6)], ui={"type": "stamp", "text": "NOT FOR SALE", "color": "#2DBE7E"}, sfx=[{"type": "hit"}]),
 L("hero", "Rosa, let me pay you back. *Every* bowl.", DIN, [c("hero", .5, pose="idle", expr="happy", scale=1.9)], camera=CU),
 L("chef", "Then wash the dishes, Jay. Paid. *Full time*.", DIN, [c("chef", .5, pose="point", expr="grin", scale=1.9)], ui={"type": "card", "text": "HIRED", "sub": "full time + lunch", "color": "#FFD400"}, sfx=[{"type": "ding"}]),
 L(N, "Mia orders the biggest pancakes on the *menu*.", DIN, [c("friend", .5, pose="cheer", expr="grin", scale=1.6)]),
 L("friend", "Sunlight is great. But it has no *syrup*.", DIN, [c("friend", .5, pose="point", expr="smug", scale=1.9)], camera=CU),
 L("bit", "Fun fact. Some sea slugs drop their own *head*.", news("REAL: THE SLUG THAT LOSES ITS HEAD"), [c("bit", .8, expr="smug", scale=.9)], transition="flash"),
 L("bit", "The head regrows a whole body in *three weeks*.", LAB, [c("bit", .78, expr="happy", scale=.9)], ui={"type": "counter", "from": 0, "to": 3, "label": "WEEKS TO A NEW BODY"}),
 L("hero", "Bit. Do *not* put that in a smoothie.", DIN, [c("hero", .5, pose="facepalm", expr="angry", scale=1.9)], camera=CU),
 L(N, "Jay eats lunch at Rosa's every day. And *pays*.", DIN, [c("hero", .3, pose="sit", expr="happy", scale=1.3), c("chef", .72, pose="wave", expr="happy", scale=1.3)]),
 L(N, "But at noon, he still turns toward *the sun*.", SD, [c("hero", .5, pose="idle", expr="sleepy", scale=1.6)], fx=[{"type": "glow"}]),
 L("bit", "Jay. Don't move. There's a *leaf* on your head.", SD, [c("bit", .5, expr="shocked", scale=1.8)], ui={"type": "stamp", "text": "LEAF DETECTED", "color": "#2DBE7E"}, sfx=[{"type": "pop"}], camera=CU),
 L("hero", "Bit. Was there algae in my *soup*?", SD, [c("hero", .5, pose="panic", expr="shocked", scale=2.0)], camera={"zoom": 1.15, "y": .5, "push": .12}, sfx=[{"type": "riser"}, {"type": "hit", "at": .9}]),
 end("Follow for a new What if every day."),
]

parts = [("The Smoothie", p1), ("Free Lunch", p2), ("Green City", p3), ("Clouds", p4),
         ("The Catch", p5), ("Rosa", p6), ("A Million Bowls", p7), ("Sunny Side Up", p8)]

series = {
 "title": "What If You Could Eat Sunlight?",
 "rubric": "what-if: sci-fi (real nature)", "mood": "wonder", "seed": 5500, "every": 2,
 "names": {"hero": "JAY", "heroLeaf": "JAY", "heroGray": "JAY", "bit": "BIT", "friend": "MIA", "friendLeaf": "MIA",
           "chef": "ROSA", "scientist": "DR. KAI", "dealer": "SELLER", "leafA": "NEIGHBOR", "leafB": "NEIGHBOR",
           "kid": "NEIGHBOR", "boss": "NEIGHBOR"},
 "finale": {"text": "THE END", "sub": "Follow for a new What if every day"},
 "parts": [{"title": t, "lines": ls} for t, ls in parts],
}
(D / "series.json").write_text(json.dumps(series, indent=1, ensure_ascii=False) + "\n")

hooks = ["What If You Could Eat Sunlight?", "What If Lunch Was Free Forever?", "What If Half the City Ate Sunlight?",
         "What If the Sun Didn't Come Back?", "What If the Sea Slug Had a Catch?", "What If Soup Was the Cure?",
         "What If a City Needed a Million Bowls?", "What If a Leaf Grew on Your Head?"]
blurbs = [
 "Jay is broke. Bit copies a real sea slug that keeps algae's chloroplasts and lives on light, and puts it in a smoothie.",
 "Jay is green, full and saving money. Then Mia's selfie gets a million views.",
 "Half the city eats sunlight. Rosa's Diner is empty. Then the forecast: 14 days of clouds.",
 "No sun. The green city gets sleepy, someone sells lamp minutes, and Bit's battery runs low.",
 "The sea slug is real. But a scientist explains the part Bit skipped.",
 "Rosa asks Jay why he really drank it. The answer is in her soup.",
 "One pot, one diner, 1.2 million hungry people, and a robot on 10% battery.",
 "The sun is back. So is lunch. And something is growing on Jay's head.",
]
tags = ["what if", "sea slug", "eat sunlight", "photosynthesis", "elysia chlorotica", "science", "animation", "story", "shorts"]
def ttl(i):
    t = f"{hooks[i]} Part {i + 1} #shorts"
    t2 = f"{hooks[i]} 🌞 Part {i + 1} #shorts"
    return t2 if len(t2) <= 60 else t
meta = {}
for i in range(8):
    meta[f"part{i + 1}"] = {
        "title": ttl(i), "short": True,
        "description": f"{blurbs[i]}\nAn original animated \"What if...?\" story by zylo, part {i + 1} of 8.\n\nFollow for a new \"What if...?\" every day.\n\n#whatif #seaslug #science #animation #shorts",
        "tags": tags, "categoryId": "1", "privacy": "public", "madeForKids": False, "syntheticMedia": False}
meta["full"] = {
    "title": "What If You Could Eat Sunlight? (Full Story)",
    "description": "A real sea slug steals solar panels from algae and lives on light. Bit puts that idea in a smoothie, and Jay never pays for lunch again. Until the clouds come.\nAn original animated \"What if...?\" story by zylo: all eight parts in one.\n\n{chapters}\nFollow for a new \"What if...?\" every day.\n\n#whatif #seaslug #science #animation #story",
    "tags": [t for t in tags if t != "shorts"], "categoryId": "1", "privacy": "public", "madeForKids": False, "syntheticMedia": False}
mp = D / "metadata.json"
if mp.exists():
    old = json.loads(mp.read_text())
    for k, v in meta.items():
        if "publishAt" in old.get(k, {}): v["publishAt"] = old[k]["publishAt"]
mp.write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")

(D / "full").mkdir(exist_ok=True)
(D / "full/thumb.json").write_text(json.dumps({
 "text": "I EAT *SUNLIGHT*", "badge": "FULL STORY", "cropY": 880, "set": {"type": "street", "time": "day"},
 "cast": [{"id": "friendLeaf", "x": 0.93, "pose": "cheer", "expr": "grin", "scale": 1.05, "y": 1620, "facing": -1},
          {"id": "heroLeaf", "x": 0.72, "pose": "cheer", "expr": "shocked", "scale": 1.3, "y": 1760},
          {"id": "bit", "x": 0.56, "expr": "happy", "scale": 0.55, "y": 1215}]}, indent=1) + "\n")

for i, (t, ls) in enumerate(parts):
    spoken = [l for l in ls if not l.get("end")]
    w = sum(len(re.sub(r"[*\"]", "", l["say"]).split()) for l in spoken)
    long_ = [l["say"] for l in spoken if len(l["say"].split()) > 9]
    print(f"part{i + 1} {t!r}: {len(ls)} lines, {w} words", "LONG:" if long_ else "", long_ or "")
for k, v in meta.items():
    print(k, len(v["title"]), v["title"])
