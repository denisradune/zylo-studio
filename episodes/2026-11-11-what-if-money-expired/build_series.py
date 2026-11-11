"""Writes series.json + metadata.json + full/thumb.json for "What if your money expired?" (8 parts).
Run: python3 episodes/2026-11-11-what-if-money-expired/build_series.py"""
import json, re
from pathlib import Path
D = Path(__file__).resolve().parent

def L(sp, say, set_, cast=(), **kw):
    shot = {"set": set_ if isinstance(set_, dict) else {"type": set_}, "cast": list(cast)}
    shot.update(kw)
    return {"speaker": sp, "say": say, "shot": shot}
def c(id_, x=0.5, **kw): return {"id": id_, "x": x, **kw}
N = "narrator"
BK = {"type": "store"}; BK1 = {"type": "store", "damage": 1}; BK2 = {"type": "store", "damage": 2}
SD = {"type": "street", "time": "day"}; SK = {"type": "street", "time": "dusk"}; SN = {"type": "street", "time": "night"}
RD = {"type": "room", "time": "day"}; RN = {"type": "room", "time": "night"}; LAB = {"type": "lab"}
SKY = {"type": "sky", "time": "day"}; SKYD = {"type": "sky", "time": "dusk"}
def news(h): return {"type": "news", "headline": h}
def burst(col): return {"type": "burst", "color": col}
CU = {"zoom": 1.1, "y": 0.6}
SHAKE = {"zoom": 1.1, "y": .6, "shake": .3}
PUSH = {"zoom": 1.15, "y": .5, "push": .12}
CLIFF = [{"type": "riser"}, {"type": "hit", "at": .9}]
def end(t): return {"speaker": N, "say": t, "end": True}
def recap(t, set_, cast, **kw):
    l = L(N, t, set_, cast, **kw); l["shortOnly"] = True; return l
def town(expr="neutral", pose="idle"):
    return [c("kid", .15, pose=pose, expr=expr, depth=.5), c("friend", .38, pose=pose, expr=expr, depth=.6),
            c("boss", .62, pose="phone", expr=expr, depth=.6), c("scientist", .85, pose=pose, expr=expr, depth=.5)]
def melt(frm, to, label): return {"type": "counter", "from": frm, "to": to, "prefix": "$", "label": label}

p1 = [
 L(N, "What if your money *expired*?", SD, [c("hero", .3, pose="point", expr="grin", scale=1.3), c("bit", .78, expr="happy", icon="$", scale=1.0)], ui=melt(100, 99, "MELTING..."), sfx=[{"type": "tick"}, {"type": "hit", "at": .8}], camera={"push": .08}),
 L(N, "Millbrook is a small town. And it's *dying*.", SK, town("sad"), ui={"type": "card", "text": "MILLBROOK", "sub": "pop. 3,000", "color": "#FFD400"}),
 L(N, "Nobody spends. Everybody keeps cash *under the mattress*.", RN, [c("scientist", .5, pose="sit", expr="smug", scale=1.6)], sfx=[{"type": "knock"}]),
 L(N, "That's Grandpa Lou. He has *a thousand* in there.", RN, [c("scientist", .5, pose="point", expr="grin", scale=1.8)], ui={"type": "card", "text": "MATTRESS BANK", "sub": "$1,000", "color": "#2DBE7E"}, camera=CU),
 L(N, "Mia's bakery hasn't sold a cake *in a week*.", BK1, [c("friend", .5, pose="idle", expr="sad", scale=1.6)], fx=[{"type": "vignette"}]),
 L("friend", "If nobody buys, I close by *Christmas*.", BK1, [c("friend", .5, pose="shrug", expr="sad", scale=1.9)], camera=CU),
 L(N, "Jay, her best friend, takes this *personally*.", BK1, [c("hero", .5, pose="idle", expr="angry", scale=1.6)]),
 L("hero", "Bit. How do you make a town *spend*?", RD, [c("hero", .5, pose="think", expr="neutral", scale=1.9)], camera=CU),
 L("bit", "Austria, nineteen thirty two. A town called *Wörgl*.", news("REAL: WÖRGL, AUSTRIA, 1932"), [c("bit", .8, expr="smug", scale=.9)], transition="flash", sfx=[{"type": "whoosh"}]),
 L("bit", "The mayor printed money that *lost value*.", LAB, [c("bit", .5, expr="happy", scale=1.7)], transition="whip"),
 L("bit", "Every month, you had to buy it a *stamp*.", LAB, [c("bit", .78, expr="think", scale=.9)], ui={"type": "list", "title": "STAMP SCRIP", "items": ["buy a stamp monthly", "about 1% of the bill", "or the bill is invalid"]}),
 L("bit", "So nobody kept it. Everybody *spent it*.", LAB, [c("bit", .5, expr="happy", scale=1.8)], ui={"type": "stamp", "text": "SPEND ME", "color": "#E0312B"}, sfx=[{"type": "hit"}]),
 L("hero", "Bit, that's *genius*. Can you build it?", RD, [c("hero", .5, pose="cheer", expr="grin", scale=1.9)], camera=CU),
 L(N, "Mayor Oak says yes in *four seconds*.", SD, [c("boss", .5, pose="wave", expr="happy", scale=1.6)], ui={"type": "clock", "text": "00:04"}),
 L(N, "Bit launches *Melt Money*. Every bill in an app.", SD, [c("bit", .5, expr="happy", icon="$", scale=1.6)], fx=[{"type": "glow"}], sfx=[{"type": "powerup"}]),
 L("bit", "Melt Money loses one percent every *single day*.", SD, [c("bit", .78, expr="smug", scale=.9)], ui=melt(1000, 990, "DAY 1")),
 L("hero", "Every day? Bit, Wörgl did it *monthly*.", SD, [c("hero", .5, pose="point", expr="scared", scale=1.9)], camera=CU),
 L("bit", "Monthly is slow. I'm a *computer*.", SD, [c("bit", .5, expr="smug", scale=1.9)], camera=CU),
 L(N, "That night, Grandpa Lou checks his *mattress*.", RN, [c("scientist", .5, pose="phone", expr="neutral", scale=1.6)], sfx=[{"type": "heartbeat"}]),
 L("scientist", "My thousand dollars. It's *melting*!", RN, [c("scientist", .5, pose="panic", expr="shocked", scale=2.0)], ui=melt(1000, 990, "GRANDPA LOU"), camera=PUSH, sfx=CLIFF),
 end("Part two drops in two days."),
]
p2 = [
 recap("Part two. Millbrook's money now *melts* every day.", SD, [c("bit", .5, expr="happy", icon="$", scale=1.6)], sfx=[{"type": "hit"}]),
 L(N, "Morning. The whole town reads the *rule*.", SD, town("shocked"), ui={"type": "card", "text": "MELT MONEY", "sub": "-1% every day", "color": "#E0312B"}),
 L("boss", "Keep it, and you lose it. So *spend it*!", SD, [c("boss", .5, pose="point", expr="grin", scale=1.9)], camera=CU),
 L(N, "And Millbrook *spends*.", burst("#FFD400"), [c("kid", .5, pose="run", expr="grin", scale=1.6, enter="pop")], sfx=[{"type": "whoosh"}, {"type": "pop", "at": .5}], transition="flash"),
 L(N, "By ten a.m., Mia's bakery has a *line*.", BK, town("happy"), ui={"type": "counter", "from": 0, "to": 37, "label": "IN LINE"}, transition="whip"),
 L("friend", "Jay! I sold *forty cakes*! Forty!", BK, [c("friend", .5, pose="cheer", expr="grin", scale=1.9)], fx=[{"type": "moneyRain"}], sfx=[{"type": "ding"}]),
 L(N, "Theo, age nine, spends everything on *candy*.", BK, [c("kid", .5, pose="cheer", expr="grin", scale=1.6)], ui={"type": "card", "text": "CANDY HAUL", "sub": "$12 → 0", "color": "#FF6B4A"}),
 L("kid", "It was melting! It's *science*!", BK, [c("kid", .5, pose="point", expr="smug", scale=1.9)], camera=CU),
 L(N, "The barber hires a helper. The helper buys *shoes*.", SD, [c("boss", .3, pose="idle", expr="happy", scale=1.2), c("scientist", .72, pose="walk", expr="happy", scale=1.2)]),
 L(N, "The shoe shop buys *paint*. The painter buys bread.", SD, town("happy", "cheer"), sfx=[{"type": "pop"}, {"type": "pop", "at": .3}, {"type": "pop", "at": .6}]),
 L("bit", "One dollar changed hands *nine times* today.", LAB, [c("bit", .78, expr="happy", scale=.9)], ui={"type": "counter", "from": 0, "to": 9, "label": "HANDS PER DOLLAR"}, transition="whip"),
 L("hero", "Bit, it's *working*. The town is alive!", SD, [c("hero", .5, pose="cheer", expr="grin", scale=1.9)], camera=CU),
 L(N, "Only Grandpa Lou still sleeps on his *mattress*.", RN, [c("scientist", .5, pose="sit", expr="angry", scale=1.6)]),
 L("scientist", "I'm not spending. I'll *outlast* it.", RN, [c("scientist", .5, pose="sit", expr="smug", scale=1.9)], ui=melt(990, 980, "GRANDPA LOU"), camera=CU),
 L(N, "At noon, Mia looks at her flour *price*.", BK, [c("friend", .5, pose="phone", expr="neutral", scale=1.6)]),
 L("friend", "Flour was five dollars. Now it's *eight*.", BK, [c("friend", .5, pose="phone", expr="shocked", scale=1.9)], ui=melt(5, 8, "FLOUR"), camera=CU),
 L("hero", "Why? Nobody even made more *flour*.", BK, [c("hero", .5, pose="shrug", expr="scared", scale=1.9)]),
 L("bit", "Everyone is buying. Nobody is *waiting*.", BK, [c("bit", .5, expr="think", scale=1.8)]),
 L("bit", "Jay. When money melts, things get *expensive*.", BK1, [c("bit", .5, expr="shocked", scale=2.0)], fx=[{"type": "vignette"}], camera=PUSH, sfx=CLIFF),
 end("Part three drops in two days."),
]
p3 = [
 recap("Part three. The town is spending. Prices are *rising*.", BK, town("shocked"), sfx=[{"type": "hit"}]),
 L(N, "Day four. People stop keeping money. They keep *stuff*.", SD, town("grin", "throw"), fx=[{"type": "throwObj"}], sfx=[{"type": "whoosh"}]),
 L(N, "Mr. Ross buys sixty rolls of *toilet paper*.", SD, [c("boss", .5, pose="cheer", expr="smug", scale=1.6)], ui={"type": "counter", "from": 0, "to": 60, "label": "ROLLS"}),
 L(N, "The Kims buy four hundred pounds of *potatoes*.", SD, [c("friend", .3, pose="idle", expr="neutral", scale=1.2), c("kid", .72, pose="cheer", expr="grin", scale=1.2)], ui={"type": "counter", "from": 0, "to": 400, "label": "POUNDS OF POTATOES"}),
 L("boss", "Potatoes don't melt, Jay. It's *smart*.", SD, [c("boss", .5, pose="point", expr="smug", scale=1.9)], camera=CU),
 L("hero", "Potatoes *rot*, Mayor. That's worse!", SD, [c("hero", .5, pose="facepalm", expr="angry", scale=1.9)], camera=CU),
 L(N, "The hardware store sells out of *everything*.", BK2, [], fx=[{"type": "vignette"}], ui={"type": "stamp", "text": "SOLD OUT", "color": "#E0312B"}, sfx=[{"type": "buzz"}], transition="whip"),
 L(N, "Mia can't buy flour. Someone bought *all of it*.", BK1, [c("friend", .5, pose="shrug", expr="sad", scale=1.8)], camera=CU),
 L("friend", "I have money, but nothing *to buy*.", BK1, [c("friend", .5, pose="idle", expr="sad", scale=1.9)], camera=CU),
 L(N, "Grandpa Lou's mattress keeps *melting*.", RN, [c("scientist", .5, pose="sit", expr="angry", scale=1.6)], ui=melt(980, 961, "GRANDPA LOU")),
 L("scientist", "Nine hundred sixty one. Still *not spending*.", RN, [c("scientist", .5, pose="sit", expr="smug", scale=1.9)], camera=CU),
 L("hero", "Bit, slow it down. Make it *monthly*. Like Wörgl.", LAB, [c("hero", .5, pose="point", expr="angry", scale=1.9)], transition="whip"),
 L("bit", "Fine. Pushing a quick *update*.", LAB, [c("bit", .5, expr="neutral", scale=1.8)], ui={"type": "card", "text": "MELT MONEY v1.1", "sub": "installing...", "color": "#16161C"}, sfx=[{"type": "powerup"}]),
 L(N, "Bit types fast. Maybe a little *too* fast.", LAB, [c("bit", .5, expr="happy", scale=1.7)], fx=[{"type": "speedLines"}], sfx=[{"type": "tick"}, {"type": "tick", "at": .3}, {"type": "tick", "at": .6}]),
 L(N, "The update goes live at *midnight*.", SN, [c("bit", .5, expr="smug", scale=1.6)], ui={"type": "clock", "text": "23:59", "to": "00:00"}, sfx=[{"type": "ring"}]),
 L(N, "At twelve oh one, every phone in Millbrook *buzzes*.", RN, [c("scientist", .5, pose="phone", expr="shocked", scale=1.6)], ui={"type": "notify", "app": "Melt Money", "title": "New rule", "body": "-1% every MINUTE", "color": "#E0312B"}, sfx=[{"type": "buzz"}]),
 L("bit", "Oh no. I typed *minute*. Not month.", LAB, [c("bit", .5, expr="glitch", scale=1.9)], fx=[{"type": "glitch"}], sfx=[{"type": "glitch"}], camera=CU),
 L(N, "Grandpa Lou watches his mattress *drain*.", RN, [c("scientist", .5, pose="panic", expr="scared", scale=1.8)], ui=melt(961, 951, "GRANDPA LOU"), fx=[{"type": "vignette"}]),
 L("scientist", "Every minute? Where can I spend at *midnight*?", RN, [c("scientist", .5, pose="panic", expr="shocked", scale=2.0)], camera=PUSH, sfx=CLIFF),
 end("Part four drops in two days."),
]
p4 = [
 recap("Part four. Bit's update made money melt *every minute*.", RN, [c("bit", .5, expr="glitch", scale=1.6)], fx=[{"type": "glitch"}], sfx=[{"type": "hit"}]),
 L(N, "Midnight. Millbrook is awake. And *shopping*.", SN, town("scared", "run"), fx=[{"type": "alarm"}], sfx=[{"type": "siren", "volume": .3}], transition="whip"),
 L(N, "In one hour, money loses almost *half its value*.", SN, [c("bit", .78, expr="sad", scale=.9)], ui=melt(100, 55, "ONE HOUR LATER")),
 L(N, "People buy anything. Lamps. Ladders. A *tuba*.", SN, town("grin", "throw"), fx=[{"type": "throwObj"}], sfx=[{"type": "crash"}]),
 L("kid", "I bought a canoe. We don't have a *lake*.", SN, [c("kid", .5, pose="shrug", expr="happy", scale=1.9)], camera=CU),
 L(N, "Mia's bakery is open all night. And *empty*.", BK2, [c("friend", .5, pose="idle", expr="sleepy", scale=1.6)], fx=[{"type": "vignette"}]),
 L("friend", "No flour, no sugar. They bought my *chairs*.", BK2, [c("friend", .5, pose="facepalm", expr="sad", scale=1.9)], camera=CU),
 L(N, "Jay finds Bit hiding *in a drawer*.", RD, [c("hero", .5, pose="run", expr="angry", scale=1.6)], sfx=[{"type": "whoosh"}]),
 L("hero", "Bit! Undo it! Make it *monthly*!", RD, [c("hero", .5, pose="point", expr="angry", scale=1.9)], camera=SHAKE),
 L("bit", "The update is locked till *morning*.", RD, [c("bit", .5, expr="sad", scale=1.8)], ui={"type": "clock", "text": "01:00", "to": "07:00"}),
 L("bit", "I wrote it to stop *hackers*. Like me.", RD, [c("bit", .5, expr="dim", scale=1.8)], camera=CU),
 L(N, "Three a.m. Grandpa Lou finally runs to the *store*.", SN, [c("scientist", .5, pose="run", expr="scared", scale=1.6)], sfx=[{"type": "whoosh"}]),
 L(N, "Every shelf is empty. Except one: *birdseed*.", BK2, [c("scientist", .5, pose="shrug", expr="shocked", scale=1.6)], ui={"type": "card", "text": "BIRDSEED", "sub": "50 lb bag", "color": "#E2A23B"}),
 L("scientist", "Fine. I'm buying *all* the birdseed.", BK2, [c("scientist", .5, pose="point", expr="angry", scale=1.9)], camera=CU),
 L(N, "Seven a.m. The update finally *stops*.", SD, [c("bit", .5, expr="neutral", scale=1.6)], ui={"type": "clock", "text": "06:59", "to": "07:00"}, sfx=[{"type": "powerdown"}]),
 L(N, "The town has canoes, tubas, potatoes. And *no money*.", SD, town("sad"), ui={"type": "bars", "items": [{"label": "STUFF", "value": 1.0, "color": "#FFD400"}, {"label": "MONEY", "value": .02, "color": "#2DBE7E"}], "tag": "$0"}),
 L("boss", "Jay. We're *rich*. In *potatoes*.", SD, [c("boss", .5, pose="shrug", expr="sad", scale=1.9)], camera=CU),
 L(N, "Then Mia's phone rings. It's her *landlord*.", BK2, [c("friend", .5, pose="phone", expr="scared", scale=1.7)], sfx=[{"type": "ring"}]),
 L("friend", "Rent is due today. And my savings *melted*.", BK2, [c("friend", .5, pose="phone", expr="sad", scale=2.0)], camera=PUSH, sfx=CLIFF),
 end("Part five drops in two days."),
]
p5 = [
 recap("Part five. The money melted. Mia can't *pay rent*.", BK2, [c("friend", .5, pose="idle", expr="sad", scale=1.6)], sfx=[{"type": "hit"}]),
 L(N, "Mia counts what's left of her savings. *Eleven dollars*.", BK2, [c("friend", .5, pose="sit", expr="sad", scale=1.6)], ui=melt(3200, 11, "MIA'S SAVINGS")),
 L("friend", "Three years of cakes. Gone in *one night*.", BK2, [c("friend", .5, pose="sit", expr="sad", scale=1.9)], camera=CU),
 L(N, "The landlord gives her one week. Then it *closes*.", BK2, [], ui={"type": "stamp", "text": "7 DAYS", "color": "#E0312B"}, fx=[{"type": "vignette"}], sfx=[{"type": "hit"}]),
 L(N, "Jay walks home. The streets are full of *junk*.", SK, [c("hero", .5, pose="walk", expr="sad", scale=1.5)]),
 L(N, "Canoes in driveways. Tubas in trash cans. *Potatoes everywhere*.", SK, town("sad"), sfx=[{"type": "whoosh"}]),
 L("hero", "Bit, I did this. I wanted to *save her*.", RN, [c("hero", .5, pose="sit", expr="sad", scale=1.9)], camera=CU),
 L("bit", "No. I did this. I copied Wörgl *wrong*.", RN, [c("bit", .5, expr="sad", scale=1.8)], camera=CU),
 L("hero", "So what did Wörgl actually *get right*?", RN, [c("hero", .5, pose="think", expr="neutral", scale=1.9)]),
 L("bit", "The stamp was small. About one percent. *Per month*.", news("WÖRGL: A STAMP A MONTH"), [c("bit", .8, expr="think", scale=.9)], transition="flash"),
 L("bit", "Enough to spend it. Not enough to *panic*.", LAB, [c("bit", .78, expr="neutral", scale=.9)], ui={"type": "bars", "items": [{"label": "WÖRGL", "value": .1, "color": "#2DBE7E"}, {"label": "BIT", "value": 1.0, "color": "#FF3B3B"}], "tag": "1%/month"}),
 L("bit", "And the town didn't spend it on *canoes*.", LAB, [c("bit", .5, expr="smug", scale=1.8)], camera=CU),
 L("hero", "Then on *what*?", RN, [c("hero", .5, pose="shrug", expr="neutral", scale=1.9)]),
 L("bit", "Houses. A reservoir. A bridge. And a *ski jump*.", news("WÖRGL BUILT: HOUSES, A BRIDGE, A SKI JUMP"), [c("bit", .8, expr="happy", scale=.9)], transition="flash", sfx=[{"type": "ding"}]),
 L("hero", "A ski jump? Bit, we don't have *snow*.", RN, [c("hero", .5, pose="facepalm", expr="grin", scale=1.9)], camera=CU),
 L(N, "But Jay is staring at the old *bridge* outside.", SN, [c("hero", .5, pose="idle", expr="neutral", scale=1.6)]),
 L(N, "It's been broken for *twelve years*.", SN, [], ui={"type": "card", "text": "OLD MILL BRIDGE", "sub": "closed since 2014", "color": "#E0312B"}, fx=[{"type": "vignette"}]),
 L("hero", "Bit. Make it monthly. And this time, *we* choose.", SN, [c("hero", .5, pose="point", expr="grin", scale=1.9)], camera=CU),
 L("bit", "Jay. What do we build *first*?", SN, [c("bit", .5, expr="happy", scale=2.0)], camera=PUSH, sfx=CLIFF),
 end("Part six drops in two days."),
]
p6 = [
 recap("Part six. Jay wants a second try. *Done right*.", SN, [c("hero", .5, pose="point", expr="grin", scale=1.6)], sfx=[{"type": "hit"}]),
 L(N, "Town hall. The whole town is *furious*.", RD, town("angry"), sfx=[{"type": "buzz"}]),
 L("boss", "Your robot melted our money. Why should we *listen*?", RD, [c("boss", .5, pose="point", expr="angry", scale=1.9)], camera=CU),
 L("hero", "Because Mia's bakery closes *in a week*.", RD, [c("hero", .5, pose="idle", expr="sad", scale=1.9)], camera=CU),
 L(N, "The room goes quiet. *Everyone* knows Mia's cakes.", RD, town("sad"), fx=[{"type": "vignette"}], sfx=[{"type": "heartbeat"}]),
 L("hero", "When my mom lost her job, I was eight.", RD, [c("hero", .5, pose="idle", expr="sad", scale=1.9)], camera=CU),
 L("hero", "Mia's grandma gave us bread. Every day. *For free*.", RD, [c("hero", .5, pose="idle", expr="sad", scale=1.9)], camera={"zoom": 1.15, "y": .55}),
 L("hero", "That bakery fed me. I can't let it *close*.", RD, [c("hero", .5, pose="point", expr="angry", scale=1.9)], camera=CU),
 L(N, "Grandpa Lou stands up. Slowly. With his *birdseed*.", RD, [c("scientist", .5, pose="idle", expr="neutral", scale=1.6)]),
 L("scientist", "I remember her grandma. Best rye in the *state*.", RD, [c("scientist", .5, pose="point", expr="happy", scale=1.9)], camera=CU),
 L("bit", "New rule. One percent a month. Just like *Wörgl*.", RD, [c("bit", .78, expr="happy", scale=.9)], ui={"type": "card", "text": "MELT MONEY v2", "sub": "-1% per month", "color": "#2DBE7E"}, sfx=[{"type": "powerup"}]),
 L("hero", "And the town pays people to *fix things*.", RD, [c("hero", .5, pose="cheer", expr="grin", scale=1.9)], camera=CU),
 L(N, "The bridge. The bakery's oven. The *roof*.", SD, town("happy", "cheer"), ui={"type": "list", "title": "THE PLAN", "items": ["fix the bridge", "fix Mia's oven", "fix the roof"]}),
 L("boss", "All in favor? Raise your *potatoes*.", RD, [c("boss", .5, pose="cheer", expr="grin", scale=1.9)], camera=CU, sfx=[{"type": "pop"}]),
 L(N, "Every hand goes up. Most are holding *potatoes*.", RD, town("grin", "cheer"), sfx=[{"type": "pop"}, {"type": "pop", "at": .3}, {"type": "ding", "at": .6}]),
 L("friend", "Jay... you did all this for *my* bakery?", RD, [c("friend", .5, pose="idle", expr="shocked", scale=1.9)], camera=CU),
 L(N, "Monday, the work begins. Mia bakes for the *workers*.", BK, [c("friend", .5, pose="cheer", expr="happy", scale=1.6)], fx=[{"type": "glow"}], transition="whip"),
 L(N, "Wednesday, a letter arrives at town hall. *Official*.", RD, [c("boss", .5, pose="phone", expr="neutral", scale=1.6)], ui={"type": "card", "text": "NATIONAL BANK", "sub": "urgent", "color": "#16161C"}, sfx=[{"type": "knock"}]),
 L("boss", "Jay. They say our money is *illegal*.", RD, [c("boss", .5, pose="panic", expr="shocked", scale=2.0)], camera=PUSH, sfx=CLIFF),
 end("Part seven drops in two days."),
]
p7 = [
 recap("Part seven. A letter says Melt Money is *illegal*.", RD, [c("boss", .5, pose="phone", expr="shocked", scale=1.6)], sfx=[{"type": "hit"}]),
 L("bit", "That happened to Wörgl too. In nineteen thirty *three*.", news("1933: AUSTRIA'S BANK ENDS WÖRGL MONEY"), [c("bit", .8, expr="sad", scale=.9)], transition="flash"),
 L("bit", "Austria's central bank shut it down. Only *official* money.", LAB, [c("bit", .5, expr="sad", scale=1.8)]),
 L("bit", "Two hundred towns wanted to copy it. *None did*.", LAB, [c("bit", .78, expr="sad", scale=.9)], ui={"type": "counter", "from": 0, "to": 200, "label": "TOWNS THAT PLANNED IT"}),
 L("boss", "The letter gives us *thirty days*.", RD, [c("boss", .5, pose="idle", expr="sad", scale=1.9)], ui={"type": "stamp", "text": "30 DAYS", "color": "#E0312B"}, camera=CU),
 L("hero", "Then we finish everything in *thirty days*.", RD, [c("hero", .5, pose="point", expr="angry", scale=1.9)], camera=CU),
 L(N, "Day one. Forty people show up at the *bridge*.", SD, town("happy", "cheer"), ui={"type": "counter", "from": 0, "to": 40, "label": "WORKERS"}, transition="whip"),
 L(N, "They're paid in Melt Money. They spend it *Friday*.", SD, town("grin"), fx=[{"type": "moneyRain"}], sfx=[{"type": "ding"}]),
 L(N, "At Mia's bakery. The barber. The *hardware store*.", BK, [c("friend", .5, pose="cheer", expr="grin", scale=1.6)], sfx=[{"type": "pop"}, {"type": "pop", "at": .4}]),
 L(N, "Day twelve. Mia's new oven *arrives*.", BK, [c("friend", .5, pose="cheer", expr="shocked", scale=1.7)], fx=[{"type": "glow"}], sfx=[{"type": "powerup"}]),
 L(N, "Day twenty. Mia pays rent. *All of it*.", BK, [c("friend", .5, pose="cheer", expr="grin", scale=1.8)], ui={"type": "stamp", "text": "PAID", "color": "#2DBE7E"}, sfx=[{"type": "hit"}]),
 L(N, "Grandpa Lou empties his mattress. *Finally*.", RN, [c("scientist", .5, pose="throw", expr="happy", scale=1.6)], ui=melt(951, 0, "GRANDPA LOU")),
 L("hero", "Lou! What did you *buy*?", SD, [c("hero", .5, pose="shrug", expr="shocked", scale=1.9)], camera=CU),
 L("scientist", "Wood. Lots of wood. It's a *surprise*.", SD, [c("scientist", .5, pose="point", expr="smug", scale=1.9)], camera=CU),
 L(N, "Day twenty nine. The bridge opens. The town *cheers*.", SKYD, town("grin", "cheer"), fx=[{"type": "glow"}], sfx=[{"type": "riser"}, {"type": "ding", "at": .8}]),
 L(N, "Day thirty. Bit has to delete *Melt Money*.", LAB, [c("bit", .5, expr="sad", scale=1.7)], fx=[{"type": "vignette"}], sfx=[{"type": "heartbeat"}]),
 L("bit", "It's the best thing I ever *built*.", LAB, [c("bit", .5, expr="sad", scale=1.9)], camera=CU),
 L("hero", "I know, buddy. It's *okay*.", LAB, [c("hero", .5, pose="idle", expr="sad", scale=1.9)], camera=CU),
 L(N, "Bit's finger hovers over the *button*.", burst("#E0312B"), [c("bit", .5, expr="sad", scale=1.8)], ui={"type": "card", "text": "DELETE?", "sub": "this cannot be undone", "color": "#E0312B"}, camera=PUSH, sfx=CLIFF, transition="flash"),
 end("The final part drops in two days."),
]
p8 = [
 recap("Part eight. Day thirty. Bit must *delete it*.", LAB, [c("bit", .5, expr="sad", scale=1.6)], sfx=[{"type": "hit"}]),
 L(N, "Bit presses delete. Melt Money is *gone*.", LAB, [c("bit", .5, expr="off", scale=1.7)], sfx=[{"type": "powerdown"}]),
 L(N, "But the bridge is still standing. *Everything* is.", SD, town("happy"), fx=[{"type": "glow"}], transition="whip"),
 L(N, "Mia's bakery has a new oven. And a *line*.", BK, town("happy"), ui={"type": "counter", "from": 0, "to": 52, "label": "IN LINE"}),
 L("friend", "Jay. People still spend. Even with *normal money*.", BK, [c("friend", .5, pose="cheer", expr="grin", scale=1.9)], camera=CU),
 L("hero", "They got used to it. Spending *here*.", BK, [c("hero", .5, pose="idle", expr="happy", scale=1.9)], camera=CU),
 L(N, "Mayor Oak hands Bit a *medal*.", RD, [c("boss", .3, pose="point", expr="grin", scale=1.2), c("bit", .72, expr="happy", scale=1.0)], ui={"type": "stamp", "text": "HONORARY CITIZEN", "color": "#FFD400"}, sfx=[{"type": "ding"}]),
 L("boss", "And the potatoes? We made the *world's biggest soup*.", SD, [c("boss", .5, pose="cheer", expr="grin", scale=1.9)], camera=CU),
 L(N, "Then Grandpa Lou reveals his surprise. On the *hill*.", SKYD, [c("scientist", .5, pose="cheer", expr="grin", scale=1.6)], sfx=[{"type": "riser"}]),
 L(N, "A giant wooden *ski jump*.", SKYD, [], ui={"type": "card", "text": "LOU'S SKI JUMP", "sub": "est. today", "color": "#FFD400"}, fx=[{"type": "glow"}], sfx=[{"type": "hit"}]),
 L("hero", "Lou. It hasn't snowed here in *forty years*.", SKYD, [c("hero", .5, pose="facepalm", expr="grin", scale=1.9)], camera=CU),
 L("scientist", "Wörgl had one. Now *Millbrook* has one.", SKYD, [c("scientist", .5, pose="point", expr="smug", scale=1.9)], camera=CU),
 L("bit", "Fun fact. That part is *true*.", SKYD, [c("bit", .5, expr="smug", scale=1.8)], camera=CU),
 L(N, "Mia bakes a cake shaped like *a bridge*.", BK, [c("friend", .5, pose="cheer", expr="happy", scale=1.6)]),
 L("friend", "On the house, Jay. You *saved* this place.", BK, [c("friend", .5, pose="point", expr="happy", scale=1.9)], camera=CU),
 L("hero", "No. This time, I *pay*.", BK, [c("hero", .5, pose="idle", expr="grin", scale=1.9)], sfx=[{"type": "ding"}], camera=CU),
 L(N, "He walks outside. Something cold touches his *nose*.", SN, [c("hero", .5, pose="idle", expr="shocked", scale=1.6)], fx=[{"type": "snow"}]),
 L(N, "For the first time in forty years, it's *snowing*.", SN, town("shocked", "cheer"), fx=[{"type": "snow"}, {"type": "glow"}], sfx=[{"type": "riser"}]),
 L("scientist", "Told you. *Ski season*.", SKYD, [c("scientist", .5, pose="cheer", expr="grin", scale=2.0)], fx=[{"type": "snow"}], camera=PUSH, sfx=[{"type": "hit", "at": .3}]),
 end("Follow for a new What if every day."),
]

parts = [("Mattress Town", p1), ("Spend It", p2), ("Potatoes", p3), ("Minute Money", p4),
         ("Done Wrong", p5), ("Done Right", p6), ("Thirty Days", p7), ("The Ski Jump", p8)]

series = {
 "title": "What If Your Money Expired?",
 "rubric": "what-if: money", "mood": "warm", "seed": 5700, "every": 2,
 "names": {"hero": "JAY", "bit": "BIT", "friend": "MIA", "boss": "MAYOR OAK", "scientist": "GRANDPA LOU", "kid": "THEO"},
 "finale": {"text": "THE END", "sub": "Follow for a new What if every day"},
 "parts": [{"title": t, "lines": ls} for t, ls in parts],
}
(D / "series.json").write_text(json.dumps(series, indent=1, ensure_ascii=False) + "\n")

hooks = ["What If Your Money Expired?", "What If Everyone Had to Spend Today?", "What If Nobody Kept Money?",
         "What If Money Melted Every Minute?", "What If a Town Copied Wörgl Wrong?", "What If Your Town Printed Its Own Money?",
         "What If Your Town's Money Was Illegal?", "What If a Town With No Snow Built a Ski Jump?"]
blurbs = [
 "Nobody in Millbrook spends. Bit copies a real 1932 idea from Wörgl, Austria: money that loses value if you keep it.",
 "Melt Money loses 1% a day. The town spends, and Mia's bakery sells out. Then flour gets expensive.",
 "People stop keeping money and start keeping potatoes. Then Bit pushes an update. Too fast.",
 "Money now melts every minute. At midnight, Millbrook buys canoes, tubas and birdseed.",
 "Mia's savings are gone. Bit explains what the real Wörgl got right.",
 "Jay tells the town why Mia's bakery matters. Then a letter arrives.",
 "Thirty days to build a bridge, save a bakery and say goodbye to Melt Money.",
 "The money is gone. The bridge isn't. And Grandpa Lou has a surprise on the hill.",
]
tags = ["what if", "money", "economics", "worgl", "stamp scrip", "history", "animation", "story", "shorts"]
def ttl(i):
    t = f"{hooks[i]} Part {i + 1} #shorts"
    t2 = f"{hooks[i]} 💸 Part {i + 1} #shorts"
    return t2 if len(t2) <= 60 else t
meta = {}
for i in range(8):
    meta[f"part{i + 1}"] = {
        "title": ttl(i), "short": True,
        "description": f"{blurbs[i]}\nAn original animated \"What if...?\" story by zylo, part {i + 1} of 8.\n\nFollow for a new \"What if...?\" every day.\n\n#whatif #money #history #animation #shorts",
        "tags": tags, "categoryId": "1", "privacy": "public", "madeForKids": False, "syntheticMedia": False}
meta["full"] = {
    "title": "What If Your Money Expired? (Full Story)",
    "description": "In 1932, the town of Wörgl in Austria printed money that lost value if you kept it. Bit copies the idea for Millbrook, and gets it very wrong first.\nAn original animated \"What if...?\" story by zylo: all eight parts in one.\n\n{chapters}\nFollow for a new \"What if...?\" every day.\n\n#whatif #money #history #animation #story",
    "tags": [t for t in tags if t != "shorts"], "categoryId": "1", "privacy": "public", "madeForKids": False, "syntheticMedia": False}
mp = D / "metadata.json"
if mp.exists():
    old = json.loads(mp.read_text())
    for k, v in meta.items():
        if "publishAt" in old.get(k, {}): v["publishAt"] = old[k]["publishAt"]
mp.write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")

(D / "full").mkdir(exist_ok=True)
(D / "full/thumb.json").write_text(json.dumps({
 "text": "MY MONEY IS *MELTING*", "badge": "FULL STORY", "cropY": 880, "set": {"type": "room", "time": "night"},
 "cast": [{"id": "scientist", "x": 0.93, "pose": "panic", "expr": "shocked", "scale": 1.05, "y": 1620, "facing": -1},
          {"id": "hero", "x": 0.72, "pose": "panic", "expr": "shocked", "scale": 1.3, "y": 1760},
          {"id": "bit", "x": 0.56, "expr": "glitch", "scale": 0.55, "y": 1215, "icon": "$"}]}, indent=1) + "\n")

for i, (t, ls) in enumerate(parts):
    spoken = [l for l in ls if not l.get("end")]
    w = sum(len(re.sub(r"[*\"]", "", l["say"]).split()) for l in spoken)
    long_ = [l["say"] for l in spoken if len(l["say"].split()) > 9]
    print(f"part{i + 1} {t!r}: {len(ls)} lines, {w} words", "LONG:" if long_ else "", long_ or "")
for k, v in meta.items():
    print(k, len(v["title"]), v["title"])
