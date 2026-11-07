"""Writes series.json + metadata.json + full/thumb.json for "What if prices dropped every minute you waited?" (8 parts).
Run: python3 episodes/2026-11-07-what-if-prices-dropped/build_series.py"""
import json, re
from pathlib import Path
D = Path(__file__).resolve().parent

def L(sp, say, set_, cast=(), **kw):
    shot = {"set": set_ if isinstance(set_, dict) else {"type": set_}, "cast": list(cast)}
    shot.update(kw)
    return {"speaker": sp, "say": say, "shot": shot}
def c(id_, x=0.5, **kw): return {"id": id_, "x": x, **kw}
N = "narrator"
ST = {"type": "store"}; ST1 = {"type": "store", "damage": 1}; ST2 = {"type": "store", "damage": 2}
SD = {"type": "street", "time": "day"}; SN = {"type": "street", "time": "night"}; SK = {"type": "street", "time": "dusk"}
RN = {"type": "room", "time": "night"}; LAB = {"type": "lab"}
def news(h): return {"type": "news", "headline": h}
def burst(col): return {"type": "burst", "color": col}
CU = {"zoom": 1.1, "y": 0.6}
def end(t): return {"speaker": N, "say": t, "end": True}
def recap(t, set_, cast, **kw):
    l = L(N, t, set_, cast, **kw); l["shortOnly"] = True; return l
def crowd(**kw):
    return [c("friend", .15, pose="idle", expr="neutral", depth=.5), c("boss", .38, pose="phone", expr="neutral", depth=.6),
            c("scientist", .62, pose="idle", expr="neutral", depth=.6), c("soldier", .85, pose="idle", expr="neutral", depth=.5)]
def price(frm, to, label, prefix="$"): return {"type": "counter", "from": frm, "to": to, "prefix": prefix, "label": label}

p1 = [
 L(N, "What if prices dropped *every minute* you waited?", ST, [c("hero", .3, pose="point", expr="grin", scale=1.3), c("bit", .78, expr="happy", icon="$", scale=1.0)], ui=price(100, 1, "EVERY MINUTE"), sfx=[{"type": "tick"}, {"type": "tick", "at": .4}, {"type": "hit", "at": .8}], camera={"push": .08}),
 L(N, "Jay just inherited his grandma's toy shop. *Penny's*.", ST, [c("hero", .5, pose="idle", expr="neutral", scale=1.5)], ui={"type": "card", "text": "PENNY'S TOYS", "sub": "since 1961", "color": "#FFD400"}),
 L(N, "It's tiny. It's dusty. And it's *empty*.", ST1, [c("hero", .5, pose="shrug", expr="sad", scale=1.6)], sfx=[{"type": "powerdown"}]),
 L("bit", "Rent is due Monday. *Nine thousand* dollars.", ST1, [c("bit", .5, expr="sad", scale=1.4)], ui={"type": "bars", "items": [{"label": "RENT", "value": 1.0, "color": "#FF3B3B"}, {"label": "CASH", "value": .03, "color": "#2DBE7E"}], "tag": "$9,000"}),
 L("hero", "Bit, I have *two hundred* dollars.", ST1, [c("hero", .5, pose="facepalm", expr="sad", scale=1.9)], camera=CU),
 L("bit", "Then we need Black Friday. And a *crazy idea*.", LAB, [c("bit", .5, expr="think", scale=1.7)], transition="whip", sfx=[{"type": "powerup"}]),
 L("bit", "Boston, nineteen oh nine. A store with *falling prices*.", news("BOSTON 1909: THE BARGAIN BASEMENT"), [c("bit", .8, expr="smug", scale=.9)], transition="flash"),
 L("bit", "Unsold after twelve days? Twenty five percent *off*.", LAB, [c("bit", .78, expr="happy", scale=.9)], ui={"type": "list", "title": "AUTOMATIC MARKDOWN", "items": ["12 days: -25%", "6 more: -50%", "6 more: -75%"]}),
 L("bit", "Still unsold? It went to *charity*.", LAB, [c("bit", .5, expr="happy", scale=1.7)], ui={"type": "stamp", "text": "TO CHARITY", "color": "#2DBE7E"}, sfx=[{"type": "ding"}]),
 L("hero", "Days are too slow. What about... *minutes*?", ST, [c("hero", .5, pose="think", expr="grin", scale=1.8)], camera=CU),
 L(N, "So they invent *the Drop*.", burst("#FFD400"), [c("bit", .5, expr="happy", scale=1.8, enter="pop")], ui={"type": "card", "text": "THE DROP", "sub": "every price falls every minute", "color": "#16161C"}, sfx=[{"type": "riser"}, {"type": "hit", "at": .8}], transition="flash"),
 L(N, "Mia, his best friend, prints *five hundred* flyers.", SD, [c("friend", .5, pose="cheer", expr="grin", scale=1.6)], ui={"type": "counter", "from": 0, "to": 500, "label": "FLYERS"}, sfx=[{"type": "pop"}]),
 L("friend", "Black Friday. Six a.m. Prices fall *till midnight*.", SD, [c("friend", .5, pose="point", expr="happy", scale=1.9)], camera=CU),
 L(N, "Friday morning, the line wraps around the *block*.", SD, crowd(), sfx=[{"type": "whoosh"}], transition="whip"),
 L(N, "Six o'clock. The doors open. The clock *starts*.", ST, crowd(), ui={"type": "clock", "text": "05:59", "to": "06:00"}, sfx=[{"type": "ring"}]),
 L(N, "Every price tag in the store starts *falling*.", ST, [c("bit", .5, expr="happy", icon="$", scale=1.4)], ui=price(40, 39, "ROBOT TOY"), sfx=[{"type": "tick"}, {"type": "tick", "at": .5}]),
 L("hero", "Okay, everyone. Go! *Buy things*!", ST, [c("hero", .5, pose="cheer", expr="grin", scale=1.8)], camera=CU),
 L(N, "But nobody moves. Not *one* person.", ST, crowd(), fx=[{"type": "vignette"}], sfx=[{"type": "heartbeat"}], camera={"push": .1}),
 L("bit", "Jay... they're not shopping. They're *waiting*.", ST, [c("bit", .5, expr="shocked", scale=2.0)], camera={"zoom": 1.15, "y": .5, "push": .12}, sfx=[{"type": "riser"}, {"type": "hit", "at": .9}]),
 end("Part two drops in two days."),
]
p2 = [
 recap("Part two. Prices are falling. Nobody is *buying*.", ST, crowd(), sfx=[{"type": "hit"}]),
 L(N, "Seven a.m. Everything is ten percent *off*.", ST, crowd(), ui={"type": "clock", "text": "07:00"}, sfx=[{"type": "tick"}]),
 L(N, "Nine a.m. Thirty percent. Still *nothing*.", ST, crowd(), ui={"type": "clock", "text": "09:00"}, fx=[{"type": "vignette"}], sfx=[{"type": "tick"}]),
 L("hero", "Bit, why is nobody *buying*?", ST, [c("hero", .5, pose="shrug", expr="scared", scale=1.9)], camera=CU),
 L("bit", "It's a *Dutch auction*. You built one by accident.", LAB, [c("bit", .5, expr="think", scale=1.6)], transition="whip", sfx=[{"type": "powerup"}]),
 L("bit", "Price starts high. Falls until someone *says yes*.", LAB, [c("bit", .78, expr="neutral", scale=.9)], ui=price(100, 20, "DUTCH AUCTION")),
 L("bit", "Dutch flower markets sell flowers with a *falling clock*.", news("FLOWER AUCTION: THE PRICE CLOCK"), [c("bit", .8, expr="happy", scale=.9)], ui={"type": "clock", "text": "10:00", "to": "09:30"}, transition="flash"),
 L("bit", "Wait too long, and someone else *takes it*.", LAB, [c("bit", .5, expr="smug", scale=1.8)], camera=CU),
 L(N, "In the corner, a kid stares at a *robot*.", ST, [c("kid", .5, pose="idle", expr="happy", scale=1.6)], sfx=[{"type": "ding"}]),
 L("kid", "I'm Theo. My sister turns seven *on Sunday*.", ST, [c("kid", .5, pose="point", expr="happy", scale=1.9)], camera=CU),
 L(N, "The robot costs forty dollars. Theo has *twelve*.", ST, [c("kid", .5, pose="shrug", expr="sad", scale=1.6)], ui={"type": "bars", "items": [{"label": "ROBOT", "value": 1.0, "color": "#FF3B3B"}, {"label": "THEO", "value": .3, "color": "#2DBE7E"}], "tag": "$12"}),
 L("bit", "At this speed, it hits twelve at *two p.m.*", ST, [c("bit", .5, expr="think", scale=1.7)], ui={"type": "clock", "text": "14:00"}),
 L("kid", "Then I'll wait. I'm *very* good at waiting.", ST, [c("kid", .5, pose="sit", expr="smug", scale=1.8)], camera=CU),
 L(N, "Mia picks up the ugliest sweater in the *shop*.", ST, [c("friend", .5, pose="idle", expr="grin", scale=1.6)], ui={"type": "card", "text": "UGLY SWEATER", "sub": "$40 and falling", "color": "#2DBE7E"}),
 L("friend", "Forty bucks? Hmm. *Not yet*.", ST, [c("friend", .5, pose="think", expr="smug", scale=1.9)], camera=CU, sfx=[{"type": "pop"}]),
 L(N, "By the door, a man in sunglasses *smiles*.", ST, [c("gambler", .5, pose="phone", expr="smug", scale=1.6)], fx=[{"type": "vignette"}], sfx=[{"type": "heartbeat"}]),
 L("bit", "Jay. That man has been inside *since midnight*.", ST, [c("bit", .5, expr="angry", scale=1.8)], camera=CU),
 L("hero", "We opened at six. How is that *possible*?", ST, [c("hero", .5, pose="panic", expr="shocked", scale=1.9)], camera={"zoom": 1.1, "y": .6, "shake": .3}),
 L("bit", "Not in the store. In our *website*.", ST1, [c("bit", .5, expr="shocked", scale=2.0)], fx=[{"type": "glitch"}], camera={"zoom": 1.15, "y": .5, "push": .12}, sfx=[{"type": "glitch"}, {"type": "hit", "at": .7}]),
 end("Part three drops in two days."),
]
p3 = [
 recap("Part three. A stranger is hiding in *our website*.", ST1, [c("gambler", .5, pose="phone", expr="smug", scale=1.6)], sfx=[{"type": "hit"}]),
 L(N, "His name is Flip. He flips toys *for money*.", ST, [c("gambler", .5, pose="wave", expr="grin", scale=1.7)], ui={"type": "card", "text": "FLIP", "sub": "buy cheap. sell triple.", "color": "#16161C"}),
 L("gambler", "I buy low. I sell high. It's called *business*.", ST, [c("gambler", .5, pose="point", expr="smug", scale=1.9)], camera=CU),
 L("bit", "His bot has four hundred toys *in its cart*.", LAB, [c("bit", .78, expr="angry", scale=.9)], ui={"type": "counter", "from": 0, "to": 400, "label": "ITEMS IN FLIP'S CART"}, transition="whip", sfx=[{"type": "alarm", "volume": .3}]),
 L("hero", "Every toy in the shop? At *what price*?", ST, [c("hero", .5, pose="shrug", expr="scared", scale=1.9)], camera=CU),
 L("bit", "The lowest price the Drop allows. *One cent*.", ST1, [c("bit", .5, expr="sad", scale=1.8)], ui={"type": "stamp", "text": "$0.01", "color": "#E0312B"}, sfx=[{"type": "hit"}]),
 L("hero", "Four hundred toys for four dollars? Stop *the Drop*!", ST1, [c("hero", .5, pose="panic", expr="angry", scale=1.9)], camera={"zoom": 1.1, "y": .6, "shake": .3}),
 L("friend", "Jay, five hundred flyers said *until midnight*.", ST, [c("friend", .5, pose="point", expr="scared", scale=1.8)], camera=CU),
 L(N, "Jay looks at the crowd. They look *back*.", ST, crowd(), fx=[{"type": "vignette"}], sfx=[{"type": "heartbeat"}]),
 L("hero", "If I stop now, they'll tear it *apart*.", ST, [c("hero", .5, pose="facepalm", expr="sad", scale=1.9)], camera=CU),
 L("gambler", "Relax, kid. I'm a *patient* man.", ST, [c("gambler", .5, pose="idle", expr="smug", scale=2.0)], camera={"zoom": 1.15, "y": .55}),
 L(N, "Noon. Prices are sixty percent off. Still *no sales*.", ST, crowd(), ui={"type": "clock", "text": "12:00"}, sfx=[{"type": "tick"}, {"type": "tick", "at": .5}]),
 L(N, "The robot toy falls to *sixteen dollars*.", ST, [c("kid", .5, pose="idle", expr="happy", scale=1.6)], ui=price(20, 16, "ROBOT TOY")),
 L("kid", "Sixteen. Almost. I have twelve. *Almost*.", ST, [c("kid", .5, pose="point", expr="happy", scale=1.9)], camera=CU),
 L(N, "Mia checks her sweater. Twenty dollars. *Not yet*.", ST, [c("friend", .5, pose="think", expr="smug", scale=1.7)], sfx=[{"type": "pop"}]),
 L("bit", "Jay. Flip's bot just picked *the robot*.", ST1, [c("bit", .5, expr="shocked", scale=1.8)], camera=CU, sfx=[{"type": "buzz"}]),
 L("hero", "Theo. The bot wants your robot. Buy it *now*.", ST, [c("hero", .5, pose="point", expr="scared", scale=1.9)], camera=CU),
 L("kid", "I only have twelve. I *can't*.", ST1, [c("kid", .5, pose="shrug", expr="sad", scale=1.9)], fx=[{"type": "vignette"}], camera=CU),
 L(N, "Somewhere, a computer counts down to *one cent*.", burst("#E0312B"), [], ui={"type": "clock", "text": "14:58", "to": "14:59"}, sfx=[{"type": "tick"}, {"type": "riser", "at": .3}, {"type": "hit", "at": .9}], transition="flash"),
 end("Part four drops in two days."),
]
p4 = [
 recap("Part four. Flip's bot waits for *one cent*.", ST1, [c("gambler", .5, pose="phone", expr="smug", scale=1.6)], sfx=[{"type": "hit"}]),
 L(N, "Two p.m. The robot hits *twelve dollars*.", ST, [c("kid", .5, pose="cheer", expr="grin", scale=1.6)], ui=price(13, 12, "ROBOT TOY"), sfx=[{"type": "ding"}]),
 L("kid", "Twelve! I have twelve! I'm *buying* it!", ST, [c("kid", .5, pose="run", expr="grin", scale=1.8)], fx=[{"type": "speedLines"}], sfx=[{"type": "whoosh"}]),
 L(N, "Theo runs to the counter. His coins *spill*.", ST, [c("kid", .5, pose="panic", expr="shocked", scale=1.7)], sfx=[{"type": "crash", "volume": .4}]),
 L(N, "He counts. Ten. Eleven. One coin is *missing*.", ST1, [c("kid", .5, pose="think", expr="scared", scale=1.9)], ui={"type": "counter", "from": 1, "to": 11, "prefix": "$", "label": "THEO COUNTS"}, sfx=[{"type": "tick"}, {"type": "tick", "at": .5}]),
 L("hero", "Bit, can't we just give him *one dollar*?", ST1, [c("hero", .5, pose="point", expr="scared", scale=1.8)], camera=CU),
 L("bit", "The Drop is automatic. Three. Two. *One*.", ST1, [c("bit", .5, expr="sad", scale=1.8)], ui={"type": "clock", "text": "14:59", "to": "15:00"}, sfx=[{"type": "tick"}, {"type": "tick", "at": .4}, {"type": "tick", "at": .8}]),
 L(N, "Three p.m. Every price hits *one cent*.", burst("#E0312B"), [], ui={"type": "stamp", "text": "$0.01", "color": "#16161C"}, sfx=[{"type": "hit"}], transition="flash"),
 L(N, "In one second, Flip's bot buys *everything*.", ST2, [c("gambler", .5, pose="cheer", expr="grin", scale=1.6)], ui={"type": "counter", "from": 0, "to": 400, "label": "SOLD TO FLIP"}, fx=[{"type": "glitch"}], sfx=[{"type": "buzz"}, {"type": "glitch", "at": .4}]),
 L(N, "The robot. The puzzles. Even Mia's *ugly sweater*.", ST2, [c("friend", .5, pose="facepalm", expr="shocked", scale=1.7)], ui={"type": "stamp", "text": "SOLD", "color": "#E0312B"}, sfx=[{"type": "pop"}]),
 L("friend", "It was going to be *ten bucks*!", ST2, [c("friend", .5, pose="panic", expr="angry", scale=1.9)], camera={"zoom": 1.1, "y": .6, "shake": .3}),
 L(N, "The crowd shuffles out. The shop is *silent*.", ST2, [c("hero", .5, pose="idle", expr="sad", scale=1.5)], fx=[{"type": "vignette"}], sfx=[{"type": "powerdown"}]),
 L("bit", "Total sales today. Four dollars. And *zero cents*.", ST2, [c("bit", .5, expr="sad", scale=1.6)], ui={"type": "bars", "items": [{"label": "RENT", "value": 1.0, "color": "#FF3B3B"}, {"label": "SALES", "value": .01, "color": "#2DBE7E"}], "tag": "$4"}),
 L(N, "Theo stands at the counter. *Eleven dollars* in hand.", ST2, [c("kid", .5, pose="idle", expr="sad", scale=1.8)], camera={"zoom": 1.15, "y": .55, "push": .1}),
 L("kid", "It's okay. Robots are for *babies* anyway.", ST2, [c("kid", .5, pose="shrug", expr="sad", scale=1.9)], camera=CU, sfx=[{"type": "heartbeat"}]),
 L("hero", "Theo, wait. I'm *so* sorry.", ST2, [c("hero", .5, pose="wave", expr="sad", scale=1.9)], camera=CU),
 L(N, "The door chimes. Flip walks out *whistling*.", SK, [c("gambler", .5, pose="walk", expr="smug", scale=1.6)], sfx=[{"type": "ding"}]),
 L("gambler", "Thanks for the sale. Want them back? *Triple price*.", SK, [c("gambler", .5, pose="point", expr="grin", scale=2.0)], camera={"zoom": 1.15, "y": .5, "push": .12}, sfx=[{"type": "riser"}, {"type": "hit", "at": .9}]),
 end("Part five drops in two days."),
]
p5 = [
 recap("Part five. Flip bought everything for *four dollars*.", ST2, [c("gambler", .5, pose="cheer", expr="grin", scale=1.6)], sfx=[{"type": "hit"}]),
 L(N, "Five p.m. Flip's toys are *online*.", RN, [c("hero", .5, pose="phone", expr="sad", scale=1.5)], ui={"type": "notify", "app": "FlipDeals", "title": "Robot toy", "body": "$120. Only one left!", "color": "#FF3B3B"}, sfx=[{"type": "buzz"}]),
 L("hero", "A hundred twenty dollars. For *Theo's* robot.", RN, [c("hero", .5, pose="facepalm", expr="angry", scale=1.9)], camera=CU),
 L("friend", "And my sweater. Ninety *nine* dollars!", RN, [c("friend", .5, pose="phone", expr="angry", scale=1.9)], camera=CU, sfx=[{"type": "pop"}]),
 L(N, "Jay drops into Grandma's old chair. Something *crinkles*.", RN, [c("hero", .5, pose="sit", expr="sad", scale=1.6)], sfx=[{"type": "whoosh"}]),
 L(N, "A shoebox. Old price tags. And a *note*.", RN, [c("hero", .5, pose="think", expr="shocked", scale=1.6)], ui={"type": "card", "text": "A fair price", "sub": "makes two people happy. — Penny", "color": "#FFF6DF"}, transition="flash"),
 L("hero", "Two people. Today I made *one*. Flip.", RN, [c("hero", .5, pose="idle", expr="sad", scale=1.9)], fx=[{"type": "vignette"}], camera={"zoom": 1.15, "y": .55, "push": .1}, sfx=[{"type": "heartbeat"}]),
 L("bit", "Jay. Can I read the flyer *again*?", RN, [c("bit", .5, expr="think", scale=1.8)], camera=CU),
 L("friend", "I made those flyers. They're *perfect*.", RN, [c("friend", .5, pose="cheer", expr="smug", scale=1.8)], camera=CU),
 L("bit", "Tiny print, bottom corner. Mia, did you *write* this?", LAB, [c("bit", .78, expr="shocked", scale=.9)], ui={"type": "card", "text": "IN-STORE PICKUP ONLY", "sub": "by midnight, or the order is cancelled", "color": "#16161C"}, transition="whip", sfx=[{"type": "ding"}]),
 L("friend", "Grandma Penny's rule. I copied it from *her sign*.", RN, [c("friend", .5, pose="shrug", expr="happy", scale=1.8)], camera=CU),
 L(N, "Flip's four hundred toys are still on *our shelf*.", ST2, [c("hero", .5, pose="point", expr="grin", scale=1.6)], sfx=[{"type": "hit"}]),
 L("hero", "He has to come and get them. *Before midnight*.", ST2, [c("hero", .5, pose="cheer", expr="grin", scale=1.9)], ui={"type": "clock", "text": "17:05", "to": "23:59"}, camera=CU),
 L("bit", "And his bot used four hundred *accounts*.", LAB, [c("bit", .5, expr="smug", scale=1.7)], ui={"type": "counter", "from": 0, "to": 400, "label": "ACCOUNTS"}),
 L(N, "Flip's phone buzzes. *Pickup reminder*.", SK, [c("gambler", .5, pose="phone", expr="shocked", scale=1.8)], ui={"type": "notify", "app": "Penny's", "title": "Pickup reminder", "body": "400 orders. Pick up by midnight.", "color": "#FFD400"}, sfx=[{"type": "buzz"}]),
 L("gambler", "Pickup? Who reads the *fine print*?", SK, [c("gambler", .5, pose="facepalm", expr="angry", scale=1.9)], camera=CU),
 L(N, "Eleven p.m. A rumble outside the *shop*.", SN, [c("car", -.2, moveTo=.5, color="#555E72", scale=1.3)], ui={"type": "clock", "text": "23:00"}, sfx=[{"type": "engine"}], transition="whip"),
 L(N, "Flip is back. A truck. And *four hundred people*.", SN, crowd() + [c("gambler", .5, pose="point", expr="grin", scale=1.3)], fx=[{"type": "vignette"}], sfx=[{"type": "riser"}, {"type": "hit", "at": .9}]),
 end("Part six drops in two days."),
]
p6 = [
 recap("Part six. Flip came back with *four hundred* people.", SN, crowd() + [c("gambler", .5, pose="point", expr="grin", scale=1.3)], sfx=[{"type": "hit"}]),
 L("gambler", "Four hundred orders. Four hundred people. *Pay up*.", SN, [c("gambler", .5, pose="cheer", expr="smug", scale=1.8)], camera=CU),
 L("hero", "Bit... can he *do* that?", ST2, [c("hero", .5, pose="shrug", expr="scared", scale=1.9)], camera=CU),
 L("bit", "Every order needs the account holder's *ID*.", ST2, [c("bit", .5, expr="think", scale=1.8)], ui={"type": "card", "text": "SHOW ID", "sub": "name must match the order", "color": "#16161C"}),
 L(N, "The first stranger steps up. Jay checks the *name*.", ST2, [c("scientist", .5, pose="idle", expr="neutral", scale=1.6)], sfx=[{"type": "tick"}]),
 L("hero", "Order one. Name on the account... *F. Lipp*.", ST2, [c("hero", .5, pose="phone", expr="smug", scale=1.8)], camera=CU),
 L("bit", "Order two. *F. Lipp*. Order three. *F. Lipp*.", LAB, [c("bit", .78, expr="smug", scale=.9)], ui={"type": "list", "title": "ORDERS", "items": ["#1 F. LIPP", "#2 F. LIPP", "#3 F. LIPP"]}, sfx=[{"type": "tick"}, {"type": "tick", "at": .4}, {"type": "tick", "at": .8}]),
 L(N, "All four hundred accounts. *Same name*.", burst("#FFD400"), [], ui={"type": "counter", "from": 1, "to": 400, "label": "F. LIPP"}, sfx=[{"type": "hit"}], transition="flash"),
 L("friend", "And only one F. Lipp is *standing here*.", ST2, [c("friend", .5, pose="point", expr="grin", scale=1.9)], camera=CU),
 L(N, "The hired crowd shrugs and walks *home*.", SN, crowd(), sfx=[{"type": "whoosh"}]),
 L("gambler", "Fine! One item. I take the *robot*.", ST2, [c("gambler", .5, pose="point", expr="angry", scale=1.9)], camera=CU),
 L(N, "Midnight. Three hundred ninety nine orders *cancelled*.", ST1, [], ui={"type": "stamp", "text": "CANCELLED", "color": "#E0312B"}, sfx=[{"type": "ring"}, {"type": "hit", "at": .5}]),
 L(N, "Flip walks out with one robot. For *one cent*.", SN, [c("gambler", .5, pose="walk", expr="smug", scale=1.6)], fx=[{"type": "vignette"}]),
 L(N, "Jay sits alone among three hundred ninety nine *toys*.", RN, [c("hero", .5, pose="sit", expr="sad", scale=1.5)], fx=[{"type": "vignette"}], sfx=[{"type": "heartbeat"}]),
 L("hero", "I saved the toys. But I lost *Theo's* robot.", RN, [c("hero", .5, pose="idle", expr="sad", scale=1.9)], camera=CU),
 L("bit", "Grandma Penny would have hated the *Drop*, wouldn't she?", RN, [c("bit", .5, expr="sad", scale=1.8)], camera=CU),
 L("hero", "No. She'd hate that *nobody* won.", RN, [c("hero", .5, pose="think", expr="neutral", scale=1.9)], camera=CU),
 L("hero", "Bit. Tomorrow we run it again. *One change*.", RN, [c("hero", .5, pose="point", expr="angry", scale=1.9)], camera={"zoom": 1.15, "y": .55, "push": .1}),
 L(N, "Jay writes it on a card in Grandma's *handwriting*.", burst("#16161C"), [], ui={"type": "card", "text": "ONE OF EACH.", "sub": "in person. no bots. ever.", "color": "#FFF6DF"}, sfx=[{"type": "riser"}, {"type": "hit", "at": .9}]),
 end("Part seven drops in two days."),
]
p7 = [
 recap("Part seven. The Drop runs again. *One of each*.", ST, [c("hero", .5, pose="point", expr="angry", scale=1.6)], sfx=[{"type": "hit"}]),
 L(N, "Saturday, six a.m. The crowd is *back*.", SD, crowd(), ui={"type": "clock", "text": "06:00"}, sfx=[{"type": "ring"}], transition="whip"),
 L("hero", "New rule. Every toy is the *only one*.", ST, [c("hero", .5, pose="point", expr="grin", scale=1.9)], camera=CU),
 L(N, "The prices start falling. And *this time*...", ST, crowd(), ui=price(40, 36, "EVERY TOY"), sfx=[{"type": "tick"}, {"type": "tick", "at": .5}]),
 L(N, "a man grabs a train set at *thirty dollars*.", ST, [c("soldier", .5, pose="cheer", expr="grin", scale=1.6)], sfx=[{"type": "ding"}]),
 L("soldier", "I'm not risking it. My son *loves* trains.", ST, [c("soldier", .5, pose="point", expr="happy", scale=1.9)], camera=CU),
 L("bit", "Falling clock rule. Whoever wants it most *buys first*.", ST, [c("bit", .5, expr="happy", scale=1.7)]),
 L(N, "Puzzles. Dolls. Kites. One by one, *everything* sells.", ST, crowd(), fx=[{"type": "moneyRain"}], ui={"type": "counter", "from": 4, "to": 8200, "prefix": "$", "label": "SALES"}, sfx=[{"type": "ding"}, {"type": "ding", "at": .4}, {"type": "ding", "at": .8}]),
 L(N, "Mia guards her sweater. Twenty dollars. *Still not yet*.", ST, [c("friend", .5, pose="idle", expr="smug", scale=1.7)], sfx=[{"type": "pop"}]),
 L(N, "Then the door opens. It's *Theo*.", ST, [c("kid", .5, pose="walk", expr="sad", scale=1.6)], sfx=[{"type": "ding"}]),
 L(N, "Behind him, Flip. With the robot. *A hundred twenty*.", ST, [c("kid", .28, pose="idle", expr="sad", scale=1.3), c("gambler", .72, pose="point", expr="smug", scale=1.4, facing=-1)], fx=[{"type": "vignette"}], sfx=[{"type": "heartbeat"}]),
 L("gambler", "Kid followed me for blocks. Market price. *Take it*.", ST, [c("gambler", .5, pose="shrug", expr="grin", scale=1.9)], camera=CU),
 L("hero", "Flip. What did you pay for that? *One cent*.", ST, [c("hero", .5, pose="point", expr="angry", scale=1.9)], camera=CU),
 L("hero", "I'll buy it back. Forty dollars. *Original price*.", ST, [c("hero", .5, pose="idle", expr="angry", scale=1.9)], ui={"type": "card", "text": "$40", "sub": "a fair price", "color": "#FFD400"}),
 L("gambler", "Forty times four thousand. Deal, *sucker*.", ST, [c("gambler", .5, pose="cheer", expr="grin", scale=1.9)], sfx=[{"type": "ding"}]),
 L(N, "Jay gives Theo the robot. Theo pays *eleven dollars*.", ST, [c("hero", .3, pose="idle", expr="happy", scale=1.3), c("kid", .72, pose="cheer", expr="grin", scale=1.3, facing=-1)], fx=[{"type": "glow", "x": 540, "y": 1100, "r": 520}]),
 L(N, "Closing time. Jay counts the *register*.", ST, [c("bit", .5, expr="think", scale=1.6)], ui={"type": "bars", "items": [{"label": "RENT", "value": 1.0, "color": "#FF3B3B"}, {"label": "CASH", "value": .996, "color": "#2DBE7E"}], "tag": "$8,960"}),
 L("bit", "Eight thousand nine hundred sixty. We're short *forty dollars*.", ST, [c("bit", .5, expr="sad", scale=2.0)], fx=[{"type": "vignette"}], camera={"zoom": 1.15, "y": .5, "push": .12}, sfx=[{"type": "powerdown"}, {"type": "hit", "at": .8}]),
 end("The final part drops in two days."),
]
p8 = [
 recap("Part eight. The shop is short exactly *forty dollars*.", ST, [c("hero", .5, pose="facepalm", expr="sad", scale=1.6)], sfx=[{"type": "hit"}]),
 L("hero", "Forty dollars. The price of *one robot*.", ST, [c("hero", .5, pose="sit", expr="sad", scale=1.8)], camera=CU),
 L("bit", "Rent is due Monday. Nothing is left *to sell*.", ST1, [c("bit", .5, expr="sad", scale=1.7)], ui={"type": "clock", "text": "21:58"}, sfx=[{"type": "tick"}]),
 L(N, "Well... *almost* nothing.", ST, [c("friend", .5, pose="idle", expr="neutral", scale=1.6)], sfx=[{"type": "pop"}]),
 L(N, "On the last rack, the ugly sweater. *One cent*.", ST, [], ui={"type": "card", "text": "UGLY SWEATER", "sub": "$0.01", "color": "#2DBE7E"}, sfx=[{"type": "ding"}]),
 L("friend", "One cent. I finally *won*.", ST, [c("friend", .5, pose="cheer", expr="grin", scale=1.9)], camera=CU),
 L(N, "Mia takes it. And slaps down *forty dollars*.", ST, [c("friend", .5, pose="point", expr="smug", scale=1.7)], ui={"type": "counter", "from": 0, "to": 40, "prefix": "$", "label": "MIA PAYS"}, sfx=[{"type": "hit"}]),
 L("hero", "Mia, the price is *one cent*!", ST, [c("hero", .5, pose="shrug", expr="shocked", scale=1.9)], camera=CU),
 L("friend", "Fair price. It makes *two* people happy.", ST, [c("friend", .5, pose="idle", expr="happy", scale=1.9)], fx=[{"type": "glow", "x": 540, "y": 1000, "r": 520}], camera=CU),
 L(N, "Nine thousand dollars. The rent is *paid*.", burst("#2DBE7E"), [], ui={"type": "stamp", "text": "RENT PAID", "color": "#16161C"}, sfx=[{"type": "riser"}, {"type": "hit", "at": .7}], transition="flash"),
 L(N, "Sunday, a photo arrives. Theo's sister. And a *robot*.", RN, [c("hero", .5, pose="phone", expr="happy", scale=1.6)], ui={"type": "notify", "app": "Theo", "title": "She LOVES it", "body": "best birthday ever!!", "color": "#2DBE7E"}, sfx=[{"type": "buzz"}]),
 L(N, "And Flip? His toys are gone. *Zero sales*.", SK, [c("gambler", .5, pose="phone", expr="sad", scale=1.7)], ui={"type": "notify", "app": "FlipDeals", "title": "0 sales today", "color": "#FF3B3B"}, sfx=[{"type": "powerdown"}]),
 L("gambler", "Who pays triple when the Drop is *next door*?", SK, [c("gambler", .5, pose="facepalm", expr="angry", scale=1.9)], camera=CU),
 L(N, "Monday morning. One last item in the *sale bin*.", ST, [c("hero", .5, pose="think", expr="shocked", scale=1.6)], sfx=[{"type": "whoosh"}], transition="whip"),
 L(N, "It's Bit. With a price tag on his *head*.", ST, [c("bit", .5, expr="smug", scale=1.8)], ui=price(1000000, 999999, "BIT")),
 L("bit", "One million dollars. Falling every minute. *Act fast*.", ST, [c("bit", .5, expr="happy", icon="$", scale=1.9)], camera=CU),
 L("hero", "Bit, get out. You're *not for sale*.", ST, [c("hero", .5, pose="point", expr="grin", scale=1.9)], camera=CU),
 L("bit", "Correct. I'm *priceless*.", ST, [c("hero", .3, pose="cheer", expr="grin", scale=1.2), c("bit", .75, expr="smug", scale=1.1)], sfx=[{"type": "ding"}]),
 end("Follow for a new What if every day."),
]
parts = [("The Drop", p1), ("The Standoff", p2), ("Flip", p3), ("One Cent", p4), ("Fine Print", p5),
         ("F. Lipp", p6), ("One of Each", p7), ("A Fair Price", p8)]

series = {
 "title": "What If Prices Dropped Every Minute You Waited?",
 "rubric": "what-if: money", "mood": "warm", "seed": 5300, "every": 2,
 "names": {"hero": "JAY", "bit": "BIT", "friend": "MIA", "kid": "THEO", "gambler": "FLIP", "soldier": "DAD", "boss": "SHOPPER", "scientist": "SHOPPER"},
 "finale": {"text": "THE END", "sub": "Follow for a new What if every day"},
 "parts": [{"title": t, "lines": ls} for t, ls in parts],
}
(D / "series.json").write_text(json.dumps(series, indent=1, ensure_ascii=False) + "\n")

hooks = ["What If Prices Dropped Every Minute?", "What If Nobody Wanted to Buy First?", "What If a Bot Waited for One Cent?",
         "What If a Bot Bought Everything for $4?", "What If the Fine Print Saved You?", "What If 400 Orders Had One Name?",
         "What If Every Toy Was the Only One?", "What If the Price Was One Cent?"]
blurbs = [
 "Jay's grandma's toy shop needs $9,000 by Monday. His Black Friday idea: every price falls every minute.",
 "The prices keep falling and nobody buys. Jay built a Dutch auction by accident.",
 "A reseller's bot has 400 toys in its cart, waiting for one cent.",
 "Three p.m. Every price hits one cent. In one second, the bot buys the whole shop.",
 "Grandma Penny's old rule is hiding in the fine print of Mia's flyer.",
 "Flip brings 400 people to pick up 400 orders. Every order has the same name.",
 "The Drop runs again with one change. And Flip walks in holding the robot.",
 "The shop is $40 short. The last item on the rack costs one cent.",
]
tags = ["what if", "black friday", "black friday deals", "dutch auction", "sale", "money", "animation", "story", "shorts"]
def ttl(i):
    t = f"{hooks[i]} Part {i + 1} #shorts"
    t2 = f"{hooks[i]} 🛒 Part {i + 1} #shorts"
    return t2 if len(t2) <= 60 else t
meta = {}
for i in range(8):
    meta[f"part{i + 1}"] = {
        "title": ttl(i), "short": True,
        "description": f"{blurbs[i]}\nAn original animated \"What if...?\" story by zylo, part {i + 1} of 8.\n\nFollow for a new \"What if...?\" every day.\n\n#whatif #blackfriday #sale #animation #shorts",
        "tags": tags, "categoryId": "1", "privacy": "public", "madeForKids": False, "syntheticMedia": False}
meta["full"] = {
    "title": "What If Prices Dropped Every Minute You Waited? (Full Story)",
    "description": "Jay's grandma's toy shop needs $9,000 by Monday. His Black Friday idea: every price falls every minute until someone buys. Then a bot shows up.\nAn original animated \"What if...?\" story by zylo: all eight parts in one.\n\n{chapters}\nFollow for a new \"What if...?\" every day.\n\n#whatif #blackfriday #sale #animation #story",
    "tags": [t for t in tags if t != "shorts"], "categoryId": "1", "privacy": "public", "madeForKids": False, "syntheticMedia": False}
mp = D / "metadata.json"
if mp.exists():
    old = json.loads(mp.read_text())
    for k, v in meta.items():
        if "publishAt" in old.get(k, {}): v["publishAt"] = old[k]["publishAt"]
mp.write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")

(D / "full").mkdir(exist_ok=True)
(D / "full/thumb.json").write_text(json.dumps({
 "text": "EVERYTHING FOR *ONE CENT*", "badge": "FULL STORY", "cropY": 880, "set": {"type": "store"},
 "cast": [{"id": "gambler", "x": 0.93, "pose": "phone", "expr": "grin", "scale": 1.05, "y": 1620, "facing": -1},
          {"id": "hero", "x": 0.72, "pose": "panic", "expr": "shocked", "scale": 1.3, "y": 1760},
          {"id": "bit", "x": 0.56, "expr": "shocked", "scale": 0.55, "y": 1215, "icon": "$"}]}, indent=1) + "\n")

for i, (t, ls) in enumerate(parts):
    spoken = [l for l in ls if not l.get("end")]
    w = sum(len(re.sub(r"[*\"]", "", l["say"]).split()) for l in spoken)
    long_ = [l["say"] for l in spoken if len(l["say"].split()) > 9]
    print(f"part{i + 1} {t!r}: {len(ls)} lines, {w} words", "LONG:" if long_ else "", long_ or "")
for k, v in meta.items():
    print(k, len(v["title"]), v["title"])
