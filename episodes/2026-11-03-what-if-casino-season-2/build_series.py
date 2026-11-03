"""Writes series.json + metadata.json + full/thumb.json for Casino Season 2 (8 parts).
Run: python3 episodes/2026-11-03-what-if-casino-season-2/build_series.py"""
import json, re
from pathlib import Path
D = Path(__file__).resolve().parent

def L(sp, say, set_, cast=(), **kw):
    shot = {"set": set_ if isinstance(set_, dict) else {"type": set_}, "cast": list(cast)}
    shot.update(kw)
    return {"speaker": sp, "say": say, "shot": shot}
def c(id_, x=0.5, **kw): return {"id": id_, "x": x, **kw}
def J(x=0.5, **kw): return {"id": "heroSuit", "voice": "hero", "x": x, **kw}  # Jay in his casino suit
N = "narrator"
CA = {"type": "casino"}; CA1 = {"type": "casino", "damage": 1}; CA2 = {"type": "casino", "damage": 2}
DIN = {"type": "store"}; RN = {"type": "room", "time": "night"}; SN = {"type": "street", "time": "night"}
LAB = {"type": "lab"}
def burst(col): return {"type": "burst", "color": col}
CU = {"zoom": 1.1, "y": 0.6}
def end(t): return {"speaker": N, "say": t, "end": True}
def recap(t, set_, cast, **kw):
    l = L(N, t, set_, cast, **kw); l["shortOnly"] = True; return l

p1 = [
 L(N, "What if you played *for* the casino?", CA, [c("owner", .22, pose="idle", expr="smug", depth=.4), J(.55, pose="point", expr="angry", scale=1.5), c("bit", .86, expr="think", depth=.2)], sfx=[{"type": "ding"}, {"type": "hit", "at": .6}], camera={"push": .08}),
 L(N, "Last season, Jay ran a casino. Then lost *it*.", CA2, [J(.5, pose="shrug", expr="sad", scale=1.6)], ui={"type": "stamp", "text": "KEYS RETURNED", "color": "#E0312B"}, sfx=[{"type": "powerdown"}]),
 L(N, "Vance never sold it. Jay never read *the contract*.", CA2, [c("owner", .3, pose="point", expr="grin", scale=1.3), J(.74, pose="facepalm", expr="sad", scale=1.3, facing=-1)]),
 L(N, "Now Jay washes dishes at a *diner*.", DIN, [c("hero", .5, pose="idle", expr="sleepy", scale=1.6)], sfx=[{"type": "whoosh"}], transition="whip"),
 L("bit", "Fun fact. You still owe me *eleven dollars*.", DIN, [c("hero", .28, pose="idle", expr="sad", scale=1.2), c("bit", .75, expr="smug", scale=1.1)], ui={"type": "counter", "from": 0, "to": 11, "prefix": "$", "label": "JAY OWES BIT"}),
 L("hero", "Bit, I'm *broke*. Not now.", DIN, [c("hero", .5, pose="facepalm", expr="sad", scale=1.8)], camera=CU),
 L(N, "Then the bell rings. It's *Lucky Lou*.", DIN, [c("gambler", -.1, moveTo=.5, pose="walk", expr="happy", scale=1.6)], sfx=[{"type": "ding"}]),
 L("gambler", "You gave me my house back. I *owe* you.", DIN, [c("gambler", .5, pose="point", expr="grin", scale=1.8)], camera=CU),
 L(N, "Lou slides a crumpled paper across the *counter*.", DIN, [c("gambler", .3, pose="idle", expr="smug", scale=1.3), c("hero", .72, pose="think", expr="shocked", scale=1.3, facing=-1)], sfx=[{"type": "pop", "at": .5}]),
 L("gambler", "Vance's contract. Read *clause nine*.", DIN, [c("gambler", .5, pose="point", expr="smug", scale=1.9)], camera=CU),
 L("hero", "Bit. Read it. *Slowly*.", DIN, [c("hero", .5, pose="phone", expr="neutral", scale=1.8)], camera=CU),
 L("bit", "Run the house three nights. *Beat the owner*...", LAB, [c("bit", .5, expr="think", scale=1.5)], ui={"type": "card", "text": "CLAUSE 9", "sub": "Run the house 3 nights. Beat the owner.", "color": "#16161C"}, sfx=[{"type": "tick"}, {"type": "tick", "at": .6}], transition="flash"),
 L("bit", "...keeps the house. *Forever*.", LAB, [c("bit", .5, expr="shocked", scale=1.9)], camera=CU, sfx=[{"type": "riser"}]),
 L("hero", "Lou. You just saved my *life*.", DIN, [c("hero", .5, pose="cheer", expr="grin", scale=1.7)]),
 L(N, "That night, Jay walks back into *the casino*.", SN, [J(.5, pose="walk", expr="smug", scale=1.4)], sfx=[{"type": "knock"}], transition="whip"),
 L("owner", "Look who's back. Did you finally *read*?", CA, [c("owner", .5, pose="idle", expr="smug", scale=1.9)], camera=CU),
 L("hero", "Clause nine. Three nights. I'm the *house*.", CA, [J(.5, pose="point", expr="angry", scale=1.9)], camera=CU),
 L("owner", "Then I'm the *player*. And I never lose.", CA, [c("owner", .5, pose="shrug", expr="grin", scale=2.0)], fx=[{"type": "vignette"}], camera={"zoom": 1.15, "y": .5, "push": .1}, sfx=[{"type": "heartbeat"}]),
 L(N, "Vance opens a briefcase. *Ten million dollars*.", CA, [c("owner", .5, pose="cheer", expr="grin", scale=1.4)], fx=[{"type": "moneyRain"}], ui={"type": "counter", "from": 0, "to": 10, "prefix": "$", "suffix": "M", "label": "VANCE'S BANKROLL"}, sfx=[{"type": "hit"}, {"type": "ding", "at": .6}], transition="flash"),
 L("owner", "Night one starts *now*, kid.", CA1, [c("owner", .5, pose="point", expr="smug", scale=2.1)], camera={"zoom": 1.15, "y": .55}, sfx=[{"type": "growl", "at": .6, "volume": .3}]),
 end("Part two drops in two days."),
]
p2 = [
 recap("Part two. Jay is the house. Vance *plays*.", CA, [J(.3, pose="idle", expr="smug", scale=1.3), c("owner", .72, pose="idle", expr="smug", scale=1.3, facing=-1)], sfx=[{"type": "hit"}]),
 L(N, "Night one. Jay puts on the *suit* again.", burst("#FFD400"), [J(.5, pose="cheer", expr="grin", scale=1.7, enter="pop")], sfx=[{"type": "riser"}], transition="flash"),
 L("bit", "Welcome back, boss. I really missed the *chandelier*.", CA, [c("bit", .5, expr="happy", icon="$", scale=1.0)], camera={"zoom": 1.2, "y": .15, "x": .5}, sfx=[{"type": "ding"}]),
 L(N, "Vance ignores the bar and walks straight to *roulette*.", CA, [c("owner", -.1, moveTo=.45, pose="walk", expr="smug", scale=1.5)], sfx=[{"type": "whoosh"}]),
 L("owner", "One thousand dollars. On *red*.", CA, [c("owner", .35, pose="point", expr="smug", scale=1.4), c("dealer", .78, pose="idle", expr="neutral", depth=.3, facing=-1)]),
 L("dealer", "Twenty two. *Black*.", CA, [c("dealer", .5, pose="point", expr="neutral", scale=1.8)], ui={"type": "card", "text": "22", "sub": "BLACK", "color": "#16161C"}, sfx=[{"type": "tick"}, {"type": "ding", "at": .5}]),
 L("owner", "Two thousand. On red.", CA, [c("owner", .5, pose="idle", expr="smug", scale=1.8)], camera=CU),
 L(N, "Black again. Three thousand gone. Vance just *smiles*.", CA, [c("owner", .5, pose="idle", expr="grin", scale=2.0)], fx=[{"type": "vignette"}], camera={"zoom": 1.15, "y": .55}),
 L("owner", "Four thousand. On *red*.", CA, [c("owner", .5, pose="point", expr="smug", scale=1.8)], sfx=[{"type": "tick"}]),
 L("hero", "Bit, why does he keep *doubling*?", CA, [J(.5, pose="think", expr="scared", scale=1.8)], camera=CU),
 L("bit", "It's called the *martingale*. Lose, double, repeat.", LAB, [c("bit", .5, expr="think", scale=1.6)], ui={"type": "list", "title": "MARTINGALE", "items": ["Bet $1K", "Lose? Double it", "Win once: +$1K"]}, sfx=[{"type": "powerup"}], transition="whip"),
 L("bit", "One win pays back *every* loss.", LAB, [c("bit", .5, expr="neutral", scale=1.5)], ui={"type": "bars", "items": [{"label": "LOST", "value": .7, "color": "#FF3B3B"}, {"label": "WIN", "value": .75, "color": "#2DBE7E"}], "tag": "+$1K"}),
 L("bit", "Plus his first thousand, as *profit*.", LAB, [c("bit", .5, expr="smug", scale=1.8)], camera=CU),
 L("hero", "Wait. So he literally can't *lose*?", CA, [J(.5, pose="panic", expr="shocked", scale=1.8)], camera=CU),
 L("bit", "With infinite money? *He can't*.", CA1, [c("bit", .5, expr="sad", scale=1.7)], sfx=[{"type": "powerdown"}]),
 L("hero", "Bit, he brought *ten million* dollars!", CA1, [J(.5, pose="facepalm", expr="scared", scale=1.9)], camera={"zoom": 1.1, "y": .6, "shake": .3}),
 L(N, "Finally, red. Vance wins a thousand. And starts *again*.", CA, [c("owner", .5, pose="cheer", expr="grin", scale=1.6)], sfx=[{"type": "ding"}, {"type": "ding", "at": .5}], transition="flash"),
 L(N, "By midnight, Vance is up *forty thousand*.", CA1, [c("owner", .3, pose="idle", expr="smug", depth=.3), J(.7, pose="idle", expr="sad", scale=1.3, facing=-1)], ui={"type": "counter", "from": 0, "to": 40, "prefix": "+$", "suffix": "K", "label": "VANCE TONIGHT"}, sfx=[{"type": "tick"}]),
 L("owner", "Two more nights, house. Tick tock. *Tick tock*.", CA1, [c("owner", .5, pose="point", expr="grin", scale=2.0)], ui={"type": "clock", "text": "11:58"}, camera=CU, sfx=[{"type": "tick"}, {"type": "tick", "at": .5}]),
 L("hero", "Bit. How do you beat *infinite money*?", CA2, [J(.5, pose="think", expr="angry", scale=1.9)], fx=[{"type": "vignette"}], camera={"zoom": 1.15, "y": .55, "push": .12}, sfx=[{"type": "heartbeat"}]),
 end("Part three drops in two days."),
]
p3 = [
 recap("Part three. Vance's doubling trick can't *lose*.", CA1, [c("owner", .5, pose="idle", expr="smug", scale=1.6)], sfx=[{"type": "hit"}]),
 L("bit", "Nobody has infinite money. Not even *him*.", CA1, [c("bit", .5, expr="smug", scale=1.7)], camera=CU),
 L("bit", "And every real table has a *maximum bet*.", LAB, [c("bit", .5, expr="happy", scale=1.6)], ui={"type": "card", "text": "MAX BET", "sub": "every table has one", "color": "#C8102E"}, sfx=[{"type": "ding"}], transition="whip"),
 L("hero", "A limit? We *forgot* the limit?", CA, [J(.5, pose="shrug", expr="shocked", scale=1.8)], camera=CU),
 L("bit", "You set it to *unlimited*. On day one.", CA, [c("bit", .5, expr="smug", scale=1.8)], camera=CU),
 L("hero", "Of *course* I did.", CA, [J(.5, pose="facepalm", expr="sad", scale=1.9)], camera=CU, sfx=[{"type": "pop"}]),
 L(N, "Jay grabs a marker and writes a *new sign*.", CA, [J(.5, pose="point", expr="smug", scale=1.4)], ui={"type": "card", "text": "MAX BET $100,000", "sub": "house rules", "color": "#16161C"}, sfx=[{"type": "knock"}]),
 L("owner", "Cute sign. It changes *nothing*.", CA, [c("owner", .5, pose="shrug", expr="smug", scale=1.9)], camera=CU),
 L(N, "One thousand on red. Black. Two thousand. *Black*.", CA, [c("dealer", .5, pose="point", expr="neutral", scale=1.5)], sfx=[{"type": "tick"}, {"type": "tick", "at": .5}, {"type": "tick", "at": 1.0}], camera={"push": .1}),
 L(N, "The streak keeps going. Seven blacks. *Eight*.", CA1, [c("owner", .5, pose="idle", expr="scared", scale=1.6)], ui={"type": "counter", "from": 1, "to": 8, "label": "BLACKS IN A ROW"}, fx=[{"type": "vignette"}], sfx=[{"type": "heartbeat"}]),
 L("owner", "Two hundred fifty six thousand. On *red*.", CA1, [c("owner", .5, pose="point", expr="angry", scale=1.9)], camera=CU),
 L("dealer", "Sorry, sir. The limit is *one hundred*.", CA, [c("dealer", .5, pose="shrug", expr="smug", scale=1.8)], ui={"type": "stamp", "text": "OVER LIMIT", "color": "#E0312B"}, sfx=[{"type": "buzz"}]),
 L(N, "The doubling *breaks*. He can't win it back.", burst("#E0312B"), [c("owner", .5, pose="facepalm", expr="shocked", scale=1.7)], sfx=[{"type": "crash"}], transition="flash"),
 L("bit", "Vance is down *two hundred fifty five thousand*.", CA, [c("bit", .5, expr="happy", scale=1.4)], ui={"type": "counter", "from": 0, "to": 255, "prefix": "-$", "suffix": "K", "label": "VANCE"}, sfx=[{"type": "ding"}]),
 L("owner", "You changed the rules *mid-game*!", CA1, [c("owner", .5, pose="panic", expr="angry", scale=1.9)], camera={"zoom": 1.1, "y": .6, "shake": .3}),
 L("hero", "You taught me. Always read *the sign*.", CA, [J(.5, pose="point", expr="grin", scale=1.9)], camera=CU),
 L(N, "Midnight. Night one goes to *the house*.", burst("#FFD400"), [J(.5, pose="cheer", expr="grin", scale=1.6)], ui={"type": "stamp", "text": "NIGHT 1: HOUSE", "color": "#16161C"}, sfx=[{"type": "riser"}, {"type": "hit", "at": .8}]),
 L(N, "Vance closes his briefcase. He's *smiling* again.", CA1, [c("owner", .5, pose="idle", expr="grin", scale=2.0)], fx=[{"type": "vignette"}], camera={"zoom": 1.15, "y": .5}),
 L("owner", "Night two, kid. I'm bringing a *friend*.", CA1, [c("owner", .5, pose="point", expr="smug", scale=2.0)], camera=CU),
 L(N, "Behind the bar, Rosa finds an *envelope*.", CA2, [c("dealer", .5, pose="phone", expr="scared", scale=1.6)], sfx=[{"type": "whoosh"}], transition="whip"),
 L(N, "Inside: cash. And a note. \"*Tilt it.*\"", burst("#16161C"), [], ui={"type": "card", "text": "TILT IT.", "sub": "— V", "color": "#FFF6DF"}, sfx=[{"type": "hit"}, {"type": "heartbeat", "at": .5}]),
 end("Part four drops in two days."),
]
p4 = [
 recap("Part four. Rosa got a *secret envelope*.", CA1, [c("dealer", .5, pose="idle", expr="scared", scale=1.6)], sfx=[{"type": "hit"}]),
 L(N, "Night two. Vance bets on one number. *Seventeen*.", CA, [c("owner", .5, pose="point", expr="smug", scale=1.6)], ui={"type": "card", "text": "17", "sub": "STRAIGHT UP", "color": "#16161C"}, transition="flash"),
 L("dealer", "Seventeen. *Black*.", CA, [c("dealer", .5, pose="idle", expr="sad", scale=1.8, facing=-1)], camera=CU, sfx=[{"type": "ding"}]),
 L(N, "One number pays thirty five to *one*. He wins.", CA, [c("owner", .5, pose="cheer", expr="grin", scale=1.5)], fx=[{"type": "moneyRain"}], sfx=[{"type": "ding"}, {"type": "ding", "at": .5}]),
 L(N, "Seventeen. Then twenty seven. Then seventeen *again*.", CA1, [c("owner", .3, pose="cheer", expr="grin", depth=.3), J(.7, pose="panic", expr="shocked", scale=1.3, facing=-1)], sfx=[{"type": "ding"}, {"type": "ding", "at": .6}, {"type": "ding", "at": 1.2}], camera={"push": .1}),
 L("hero", "That's *impossible*. Right, Bit? Tell me that's impossible.", CA1, [J(.5, pose="shrug", expr="scared", scale=1.8)], camera=CU),
 L("bit", "Not impossible. Just very, very *unlikely*.", CA1, [c("bit", .5, expr="think", scale=1.8)], camera=CU),
 L(N, "Every spin, the vault counter keeps *falling*.", CA1, [], ui={"type": "counter", "from": 900, "to": 300, "prefix": "$", "suffix": "K", "label": "VAULT"}, fx=[{"type": "alarm"}], sfx=[{"type": "alarm", "volume": .3}]),
 L("bit", "Jay, I logged every spin *tonight*.", LAB, [c("bit", .5, expr="neutral", scale=1.6)], sfx=[{"type": "powerup"}], transition="whip"),
 L("bit", "Three numbers hit *five times* too often.", LAB, [c("bit", .78, expr="shocked", scale=.9)], ui={"type": "bars", "items": [{"label": "7", "value": .9, "color": "#FF3B3B"}, {"label": "17", "value": 1.0, "color": "#FF3B3B"}, {"label": "27", "value": .85, "color": "#FF3B3B"}, {"label": "OTHERS", "value": .18, "color": "#2DBE7E"}], "tag": "HITS"}),
 L("bit", "A flawed wheel *favors* some numbers.", LAB, [c("bit", .5, expr="think", scale=1.7)], camera=CU),
 L("bit", "Real players have watched wheels for *ten thousand* spins.", LAB, [c("bit", .5, expr="smug", scale=1.5)], ui={"type": "counter", "from": 0, "to": 10000, "label": "SPINS WATCHED"}, sfx=[{"type": "tick"}]),
 L("hero", "So the wheel itself is *broken*?", CA1, [J(.5, pose="think", expr="angry", scale=1.8)], camera=CU),
 L("bit", "Or someone *broke* it.", CA2, [c("bit", .5, expr="angry", scale=1.9)], fx=[{"type": "vignette"}], camera=CU, sfx=[{"type": "heartbeat"}]),
 L(N, "Jay looks at the dealer. Rosa looks *away*.", CA1, [J(.28, pose="idle", expr="sad", scale=1.4), c("dealer", .74, pose="idle", expr="scared", scale=1.4)]),
 L("hero", "Rosa? Tell me it *wasn't* you.", CA1, [J(.5, pose="point", expr="sad", scale=1.9)], camera=CU),
 L("dealer", "Jay... I didn't want to. I'm *so* sorry.", CA2, [c("dealer", .5, pose="facepalm", expr="sad", scale=1.9)], camera=CU),
 L(N, "The vault is down to *fifty thousand*.", CA2, [], ui={"type": "bars", "items": [{"label": "VAULT", "value": .05, "color": "#FF3B3B"}], "tag": "$50K"}, sfx=[{"type": "powerdown"}]),
 L("owner", "One more spin and the house is *mine*.", CA2, [c("owner", .5, pose="point", expr="grin", scale=2.0)], camera={"zoom": 1.15, "y": .5, "push": .1}),
 L(N, "Vance pushes every single chip he has onto *seventeen*.", burst("#E0312B"), [c("owner", .5, pose="cheer", expr="smug", scale=1.6)], ui={"type": "stamp", "text": "ALL IN: 17", "color": "#16161C"}, sfx=[{"type": "hit"}, {"type": "riser", "at": .4}], transition="flash"),
 end("Part five drops in two days."),
]
p5 = [
 recap("Part five. Vance bet everything on a *tilted wheel*.", CA2, [c("owner", .5, pose="idle", expr="grin", scale=1.6)], sfx=[{"type": "hit"}]),
 L("hero", "Stop the wheel! House rules. *Inspection*.", CA2, [J(.5, pose="point", expr="angry", scale=1.9)], fx=[{"type": "speedLines"}], sfx=[{"type": "whoosh"}], camera={"zoom": 1.1, "y": .6, "shake": .3}),
 L("owner", "You can't stop a *spin*!", CA2, [c("owner", .5, pose="panic", expr="angry", scale=1.9)], camera=CU),
 L("bit", "Your own contract says *he can*.", CA1, [c("bit", .5, expr="smug", scale=1.8)], ui={"type": "card", "text": "CLAUSE 4", "sub": "The house may inspect any table", "color": "#16161C"}, sfx=[{"type": "pop"}]),
 L(N, "Jay lifts the wheel. Under it, a tiny *coin*.", CA1, [J(.5, pose="think", expr="shocked", scale=1.6)], fx=[{"type": "glow", "x": 540, "y": 1200, "r": 300}], sfx=[{"type": "ding"}]),
 L(N, "Stamped with a single letter. *V*.", burst("#16161C"), [], ui={"type": "card", "text": "V", "sub": "under the wheel", "color": "#FFD400"}, sfx=[{"type": "hit"}], transition="flash"),
 L("hero", "Rosa. You were my friend. *Why*?", CA1, [J(.5, pose="idle", expr="sad", scale=1.9)], camera=CU),
 L("dealer", "Vance owns my debt. Forty *thousand*.", CA1, [c("dealer", .5, pose="idle", expr="sad", scale=1.9)], camera=CU),
 L("dealer", "Tilt the wheel, or lose my *apartment*.", RN, [c("dealer", .5, pose="facepalm", expr="sad", scale=1.6)], fx=[{"type": "rain"}, {"type": "vignette"}], transition="whip"),
 L(N, "Jay knows that feeling. He has *been* there.", CA1, [J(.5, pose="idle", expr="sad", scale=2.0)], fx=[{"type": "vignette"}], camera={"zoom": 1.15, "y": .55, "push": .1}, sfx=[{"type": "heartbeat"}]),
 L("hero", "Bit. New wheel. *Perfectly* level.", CA, [J(.35, pose="point", expr="angry", scale=1.4), c("bit", .8, expr="happy", scale=.9)], sfx=[{"type": "engine", "volume": .4}]),
 L(N, "Same bet. Fair wheel. The ball *spins*.", CA, [c("dealer", .5, pose="idle", expr="neutral", scale=1.5)], sfx=[{"type": "tick"}, {"type": "tick", "at": .4}, {"type": "tick", "at": .8}, {"type": "tick", "at": 1.2}], camera={"push": .15}),
 L("dealer", "Four. *Black*.", CA, [c("dealer", .5, pose="point", expr="smug", scale=1.9)], ui={"type": "card", "text": "4", "sub": "BLACK", "color": "#16161C"}, sfx=[{"type": "ding"}], transition="flash"),
 L(N, "Every chip Vance won tonight is *gone*.", CA, [c("owner", .5, pose="facepalm", expr="shocked", scale=1.8)], ui={"type": "stamp", "text": "LOST", "color": "#E0312B"}, sfx=[{"type": "crash"}]),
 L("owner", "Fine. Fine! Night two goes to *the house*.", CA1, [c("owner", .5, pose="shrug", expr="angry", scale=1.9)], camera=CU),
 L("owner", "And Rosa? You're *fired*.", CA1, [c("owner", .5, pose="point", expr="angry", scale=2.0)], camera=CU, sfx=[{"type": "hit"}]),
 L("hero", "She doesn't work for you. She works for *me*.", CA, [c("dealer", .28, pose="idle", expr="shocked", scale=1.3), J(.72, pose="point", expr="smug", scale=1.4, facing=-1)]),
 L("dealer", "Jay... nobody ever stood up for me. *Thank you*.", CA, [c("dealer", .5, pose="idle", expr="happy", scale=1.8)], fx=[{"type": "glow", "x": 540, "y": 1100, "r": 520}]),
 L("owner", "Tomorrow, no wheels. No cards. Just *one coin*.", CA2, [c("owner", .5, pose="idle", expr="grin", scale=2.1)], fx=[{"type": "vignette"}], camera={"zoom": 1.15, "y": .5, "push": .12}, sfx=[{"type": "heartbeat"}]),
 L(N, "One flip. Heads or tails. Winner takes *everything*.", burst("#FFD400"), [], ui={"type": "card", "text": "HEADS OR TAILS", "sub": "winner takes everything", "color": "#16161C"}, sfx=[{"type": "riser"}, {"type": "hit", "at": .9}], transition="flash"),
 end("Part six drops in two days."),
]
p6 = [
 recap("Part six. Tomorrow, one coin decides *everything*.", CA1, [J(.5, pose="think", expr="scared", scale=1.6)], sfx=[{"type": "hit"}]),
 L(N, "Midnight. Jay can't *sleep*.", RN, [c("hero", .5, pose="sit", expr="sleepy", scale=1.5)], ui={"type": "clock", "text": "3:12"}, sfx=[{"type": "tick"}]),
 L("hero", "Bit. A coin flip is *fair*, right?", RN, [c("hero", .5, pose="think", expr="neutral", scale=1.8)], camera=CU),
 L("bit", "Fifty fifty. The fairest bet *there is*.", RN, [c("bit", .5, expr="neutral", scale=1.7)], ui={"type": "bars", "items": [{"label": "HEADS", "value": .5, "color": "#FFD400"}, {"label": "TAILS", "value": .5, "color": "#FFD400"}], "tag": "50/50"}),
 L("hero", "Then why am I *scared*?", RN, [c("hero", .5, pose="idle", expr="scared", scale=1.9)], camera=CU),
 L("bit", "Because you remember *old Jay*.", RN, [c("bit", .5, expr="sad", scale=1.8)], camera=CU),
 L(N, "Old Jay lost ten bets straight. And kept *going*.", CA2, [c("hero", .5, pose="facepalm", expr="sad", scale=1.6)], fx=[{"type": "vignette"}], ui={"type": "counter", "from": 0, "to": 10, "label": "LOSSES IN A ROW"}, transition="whip"),
 L("hero", "I always thought the next one was *due*.", RN, [c("hero", .5, pose="sit", expr="sad", scale=1.8)], camera=CU),
 L("bit", "Monte Carlo, nineteen thirteen. Black hit *twenty six* times.", {"type": "news", "headline": "MONTE CARLO, 1913: BLACK x26"}, [c("bit", .8, expr="think", scale=.9)], ui={"type": "counter", "from": 1, "to": 26, "label": "BLACKS IN A ROW"}, sfx=[{"type": "tick"}, {"type": "tick", "at": .5}, {"type": "tick", "at": 1.0}], transition="flash"),
 L("bit", "People bet against black. They lost *millions*.", {"type": "news", "headline": "GAMBLERS LOSE MILLIONS"}, [c("bit", .5, expr="sad", scale=1.4)], sfx=[{"type": "powerdown"}]),
 L("bit", "A wheel has no *memory*. Neither does a coin.", RN, [c("bit", .5, expr="neutral", scale=1.8)], camera=CU),
 L(N, "Knock knock. It's Lou. And *Rosa*.", RN, [c("gambler", .25, pose="wave", expr="happy", depth=.2), c("dealer", .72, pose="wave", expr="happy", depth=.3)], sfx=[{"type": "knock"}, {"type": "knock", "at": .3}]),
 L("gambler", "I almost lost my house to a *feeling*.", RN, [c("gambler", .5, pose="idle", expr="sad", scale=1.9)], camera=CU),
 L("dealer", "Don't let him turn you into *old Jay*.", RN, [c("dealer", .5, pose="point", expr="angry", scale=1.9)], camera=CU),
 L("hero", "But if I don't flip, I *lose* everything.", RN, [c("hero", .5, pose="shrug", expr="scared", scale=1.9)], camera=CU),
 L("bit", "Jay. Read the contract. *Again*.", RN, [c("bit", .5, expr="smug", scale=1.8)], camera=CU, sfx=[{"type": "pop"}]),
 L(N, "Bit highlights two words. *Three nights*.", LAB, [c("bit", .8, expr="happy", scale=.9)], ui={"type": "card", "text": "CLAUSE 9", "sub": "beat the owner over THREE NIGHTS", "color": "#16161C"}, sfx=[{"type": "ding"}], transition="whip"),
 L("hero", "Not one flip. All three *nights* together.", RN, [c("hero", .5, pose="point", expr="shocked", scale=1.8)], camera=CU),
 L("hero", "Bit. How far ahead *are we*?", RN, [c("hero", .5, pose="think", expr="neutral", scale=1.9)], camera={"zoom": 1.15, "y": .55, "push": .1}, sfx=[{"type": "heartbeat"}]),
 L("bit", "Exactly... *eleven dollars*.", burst("#FFD400"), [c("bit", .5, expr="shocked", scale=2.0, enter="pop")], ui={"type": "counter", "from": 0, "to": 11, "prefix": "+$", "label": "HOUSE AHEAD BY"}, sfx=[{"type": "hit"}, {"type": "riser", "at": .4}], transition="flash"),
 end("Part seven drops in two days."),
]
p7 = [
 recap("Part seven. The house is ahead by *eleven dollars*.", CA1, [c("bit", .5, expr="shocked", scale=1.6)], sfx=[{"type": "hit"}]),
 L(N, "Night three. The whole city came to *watch*.", {"type": "news", "headline": "CASINO SHOWDOWN: NIGHT THREE"}, [c("owner", .25, pose="idle", expr="smug", depth=.3), J(.75, pose="idle", expr="neutral", depth=.3, facing=-1)], sfx=[{"type": "riser"}], transition="flash"),
 L("owner", "Heads or tails, kid. Casino against *everything*.", CA, [c("owner", .5, pose="point", expr="grin", scale=1.9)], camera=CU, sfx=[{"type": "ding"}]),
 L("hero", "*No*.", CA, [J(.5, pose="idle", expr="smug", scale=2.0)], camera={"zoom": 1.15, "y": .55}),
 L("owner", "No?", CA, [c("owner", .5, pose="shrug", expr="shocked", scale=2.0)], camera={"zoom": 1.15, "y": .55}, sfx=[{"type": "pop"}]),
 L("hero", "The house doesn't have to play. You *taught* me.", CA, [J(.5, pose="point", expr="smug", scale=1.8)], camera=CU),
 L(N, "The crowd *boos*. Someone yells \"coward\".", CA1, [c("kid", .2, pose="point", expr="angry", depth=.4), c("friend", .8, pose="point", expr="angry", depth=.4), J(.5, pose="idle", expr="sad", scale=1.3)], sfx=[{"type": "crash", "volume": .4}], camera={"shake": .3}),
 L("owner", "Fine. Then I'll play your *machines*. Every one.", CA1, [c("owner", .5, pose="point", expr="angry", scale=1.9)], camera=CU),
 L(N, "Vance pulls slot after slot after slot. *All night*.", CA, [c("owner", .5, pose="point", expr="angry", scale=1.4)], fx=[{"type": "speedLines"}], sfx=[{"type": "ding"}, {"type": "ding", "at": .4}, {"type": "ding", "at": .8}]),
 L("bit", "Every pull, the house edge earns us *pennies*.", CA, [c("bit", .5, expr="happy", icon="$", scale=1.5)], ui={"type": "counter", "from": 11, "to": 211, "prefix": "+$", "label": "HOUSE AHEAD BY"}, sfx=[{"type": "tick"}]),
 L(N, "Eleven fifty nine. Vance is losing. He's *desperate*.", CA2, [c("owner", .5, pose="panic", expr="scared", scale=1.8)], ui={"type": "clock", "text": "11:59"}, fx=[{"type": "vignette"}], sfx=[{"type": "heartbeat"}]),
 L("owner", "No records? Then no *winner*.", CA2, [c("owner", .5, pose="point", expr="angry", scale=2.0)], camera=CU),
 L(N, "He rips Bit's cable out of the *wall*.", burst("#E0312B"), [c("owner", .3, pose="throw", expr="angry", scale=1.4), c("bit", .75, expr="glitch", scale=1.0)], fx=[{"type": "glitch"}], sfx=[{"type": "crash"}, {"type": "powerdown", "at": .4}], transition="flash"),
 L("bit", "Jay... the ledger... *saving*...", CA2, [c("bit", .5, expr="glitch", scale=1.8)], fx=[{"type": "glitch"}], sfx=[{"type": "glitch"}]),
 L("hero", "Bit! Bit, no! Stay with me!", CA2, [J(.5, pose="panic", expr="scared", scale=1.9)], camera={"zoom": 1.1, "y": .6, "shake": .4}),
 L("bit", "Sending everything to your *phone*.", CA2, [c("bit", .5, expr="sad", scale=1.7)], sfx=[{"type": "powerdown"}]),
 L("bit", "No room left for... *me*.", CA2, [c("bit", .5, expr="sad", scale=2.0)], fx=[{"type": "vignette"}], camera={"zoom": 1.15, "y": .5, "push": .12}),
 L(N, "Then Bit's little screen goes *dark*.", burst("#16161C"), [], sfx=[{"type": "powerdown"}, {"type": "heartbeat", "at": .6}]),
 L(N, "Jay's phone buzzes. Ledger *received*.", CA2, [J(.5, pose="phone", expr="sad", scale=1.6)], ui={"type": "notify", "app": "Bit", "title": "Ledger saved", "body": "House ahead: $211", "color": "#FFD400"}, sfx=[{"type": "buzz"}]),
 L(N, "Midnight. Three nights. The house wins *all three*.", CA, [J(.5, pose="idle", expr="sad", scale=1.5)], ui={"type": "stamp", "text": "HOUSE WINS", "color": "#2DBE7E"}, sfx=[{"type": "ding"}, {"type": "hit", "at": .6}]),
 L(N, "Jay won the casino. But he lost *Bit*.", CA2, [J(.3, pose="idle", expr="sad", scale=1.3), c("bit", .75, expr="sleepy", scale=1.0)], fx=[{"type": "vignette"}], camera={"push": .1}),
 end("The final part drops in two days."),
]
p8 = [
 recap("Part eight. Jay won the casino. But lost *Bit*.", CA2, [c("bit", .5, expr="sleepy", scale=1.6)], sfx=[{"type": "hit"}]),
 L(N, "The casino is Jay's now. *Forever*.", CA, [J(.5, pose="idle", expr="neutral", scale=1.5)], ui={"type": "stamp", "text": "OWNER: JAY", "color": "#16161C"}, sfx=[{"type": "ding"}]),
 L(N, "But Jay isn't celebrating. He's rebooting his *friend*.", RN, [c("hero", .3, pose="sit", expr="sad", scale=1.2), c("bit", .75, expr="sleepy", scale=1.0)], ui={"type": "counter", "from": 0, "to": 100, "suffix": "%", "label": "REBOOT"}, sfx=[{"type": "powerup"}]),
 L("hero", "Bit? It's me. *Jay*.", RN, [c("hero", .5, pose="wave", expr="sad", scale=1.8)], camera=CU),
 L("bit", "Hello. I am Bit. Who is *Jay*?", RN, [c("bit", .5, expr="neutral", scale=1.8)], camera=CU, sfx=[{"type": "ding"}]),
 L(N, "Jay tries everything. He even shows Bit the *chandelier*.", CA, [J(.3, pose="point", expr="happy", scale=1.2), c("bit", .75, expr="neutral", scale=.9)], camera={"zoom": 1.1, "y": .3}),
 L("bit", "That is a *lamp*.", CA, [c("bit", .5, expr="neutral", scale=1.9)], camera=CU, sfx=[{"type": "pop"}]),
 L(N, "Rosa sings. Lou dances badly. Nothing *works*.", CA, [c("dealer", .25, pose="cheer", expr="happy", depth=.3), c("gambler", .75, pose="cheer", expr="grin", depth=.3), c("bit", .5, expr="neutral", scale=1.0)]),
 L("hero", "Bit... remember? I still owe you *eleven dollars*.", RN, [c("hero", .5, pose="idle", expr="sad", scale=1.9)], fx=[{"type": "vignette"}], camera={"zoom": 1.15, "y": .55, "push": .1}, sfx=[{"type": "heartbeat"}]),
 L("bit", "Eleven dollars... You *still* haven't paid me!", RN, [c("bit", .5, expr="angry", scale=2.0, enter="pop")], fx=[{"type": "glow", "x": 540, "y": 1000, "r": 520}], sfx=[{"type": "powerup"}, {"type": "hit", "at": .5}], transition="flash"),
 L("hero", "Bit! You're *back*!", RN, [c("hero", .3, pose="cheer", expr="grin", scale=1.3), c("bit", .75, expr="happy", scale=1.1)]),
 L("bit", "Memory restored. Debt *also* restored.", RN, [c("bit", .5, expr="smug", scale=1.8)], camera=CU),
 L(N, "Next morning, Jay makes *one change*.", CA, [J(.5, pose="think", expr="smug", scale=1.6)], sfx=[{"type": "whoosh"}], transition="whip"),
 L(N, "Chips are free now. Nobody can bet *real money*.", burst("#2DBE7E"), [], ui={"type": "card", "text": "FREE CHIPS", "sub": "no real money. ever.", "color": "#16161C"}, sfx=[{"type": "ding"}, {"type": "pop", "at": .4}]),
 L("hero", "Everybody plays. Everybody laughs. Everybody goes *home*.", CA, [J(.5, pose="cheer", expr="grin", scale=1.6)], fx=[{"type": "moneyRain"}]),
 L(N, "Rosa runs the floor. Lou greets every *guest*.", CA, [c("dealer", .3, pose="wave", expr="happy", scale=1.3), c("gambler", .72, pose="wave", expr="grin", scale=1.3, facing=-1)]),
 L(N, "And the first customer in line? *Mr. Vance*.", CA, [c("owner", -.1, moveTo=.5, pose="walk", expr="smug", scale=1.6)], sfx=[{"type": "whoosh"}, {"type": "hit", "at": .6}]),
 L("owner", "I've got a new system. I *can't* lose.", CA, [c("owner", .5, pose="point", expr="grin", scale=1.9)], camera=CU),
 L("hero", "Sir, the chips are free. *Nobody* loses.", CA, [J(.5, pose="shrug", expr="smug", scale=1.9)], camera=CU),
 L("owner", "Then what's the *point*?", CA, [c("owner", .5, pose="shrug", expr="shocked", scale=2.0)], camera={"zoom": 1.15, "y": .55}),
 L("bit", "*Exactly*.", CA, [J(.3, pose="cheer", expr="grin", scale=1.2), c("bit", .75, expr="smug", scale=1.1)], sfx=[{"type": "ding"}]),
 end("Follow for a new What if every day."),
]
parts = [("Fine Print", p1), ("Doubling", p2), ("Table Limit", p3), ("The Tilted Wheel", p4), ("Rosa", p5),
         ("Old Jay", p6), ("The Flip", p7), ("The House", p8)]

series = {
 "title": "What If You Played for the Casino? Season 2",
 "rubric": "what-if: money", "mood": "tension", "seed": 4200, "every": 2,
 "sequelOf": "2026-10-31-what-if-casino-boss", "season": 2,
 "names": {"hero": "JAY", "bit": "BIT", "owner": "MR. VANCE", "dealer": "ROSA", "gambler": "LUCKY LOU", "kid": "FAN", "friend": "FAN"},
 "finale": {"text": "THE END", "sub": "Follow for a new What if every day"},
 "parts": [{"title": t, "lines": ls} for t, ls in parts],
}
(D / "series.json").write_text(json.dumps(series, indent=1, ensure_ascii=False) + "\n")

hooks = ["What If You Played for the Casino?", "What If Doubling Always Won?", "What If the Table Had a Limit?",
         "What If the Wheel Was Tilted?", "What If the Dealer Was Bribed?", "What If Black Hit 26 Times?",
         "What If You Refused the Final Bet?", "What If the Casino Was Free?"]
blurbs = [
 "Jay lost the casino. One forgotten clause gives him three nights to win it back for good.",
 "Vance doubles his bet after every loss. With ten million dollars, can he ever lose?",
 "The doubling trick has one weakness, and it is written on a sign.",
 "Seventeen. Twenty seven. Seventeen again. Bit logs every spin and finds the flaw.",
 "Under the wheel: a coin stamped V. And the dealer has a secret.",
 "A coin flip is fair. So why is Jay scared? Monte Carlo, 1913, has the answer.",
 "Night three. Heads or tails, casino against everything. Jay says no.",
 "Jay owns the casino. Bit doesn't remember him. One running joke changes that.",
]
tags = ["what if", "casino", "gambling", "martingale", "roulette", "gambler's fallacy", "animation", "story", "season 2", "shorts"]
def ttl(i):
    t = f"{hooks[i]} Season 2 · Part {i + 1} #shorts"
    t2 = f"{hooks[i]} 🎰 Season 2 · Part {i + 1} #shorts"
    return t2 if len(t2) <= 60 else t
meta = {}
for i in range(8):
    meta[f"part{i + 1}"] = {
        "title": ttl(i), "short": True,
        "description": f"{blurbs[i]}\nAn original animated \"What if...?\" story by zylo, season 2, part {i + 1} of 8.\n\nFollow for a new \"What if...?\" every day.\n\n#whatif #casino #gambling #animation #shorts",
        "tags": tags, "categoryId": "1", "privacy": "public", "madeForKids": False, "syntheticMedia": False}
meta["full"] = {
    "title": "What If You Played for the Casino? Season 2 (Full Story)",
    "description": "Jay lost the casino. A forgotten clause gives him three nights to beat the man who tricked him, playing as the house.\nAn original animated \"What if...?\" story by zylo: all eight parts of season two in one.\n\n{chapters}\nFollow for a new \"What if...?\" every day.\n\n#whatif #casino #gambling #animation #story",
    "tags": [t for t in tags if t != "shorts"], "categoryId": "1", "privacy": "public", "madeForKids": False, "syntheticMedia": False}
mp = D / "metadata.json"
if mp.exists():  # keep publishAt set by publish_series.py schedule
    old = json.loads(mp.read_text())
    for k, v in meta.items():
        if "publishAt" in old.get(k, {}): v["publishAt"] = old[k]["publishAt"]
mp.write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")

(D / "full").mkdir(exist_ok=True)
(D / "full/thumb.json").write_text(json.dumps({
 "text": "ONE COIN. *EVERYTHING*.", "badge": "FULL STORY", "cropY": 880, "set": {"type": "casino"},
 "cast": [{"id": "owner", "x": 0.93, "pose": "point", "expr": "grin", "scale": 1.05, "y": 1620, "facing": -1},
          {"id": "heroSuit", "x": 0.72, "pose": "idle", "expr": "shocked", "scale": 1.3, "y": 1760},
          {"id": "bit", "x": 0.58, "expr": "shocked", "scale": 0.55, "y": 1215, "icon": "$"}]}, indent=1) + "\n")

# self-check: words per part, line length, titles
for i, (t, ls) in enumerate(parts):
    spoken = [l for l in ls if not l.get("end")]
    w = sum(len(re.sub(r"[*\"]", "", l["say"]).split()) for l in spoken)
    long_ = [l["say"] for l in spoken if len(l["say"].split()) > 9]
    print(f"part{i + 1} {t!r}: {len(ls)} lines, {w} words", "LONG:" if long_ else "", long_ or "")
for k, v in meta.items():
    print(k, len(v["title"]), v["title"])
