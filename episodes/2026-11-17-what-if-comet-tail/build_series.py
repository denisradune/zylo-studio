"""Writes series.json + metadata.json + full/thumb.json for "What if Earth flew through a comet's tail today?" (8 parts).
Real basis: Halley's Comet, May 1910 (cyanogen panic, comet pills, papered keyholes, a clouded-out rooftop comet
party, Mark Twain), next return 28 July 2061 — see sources.md. The comet in the story ("Comet Vela") is fiction.
Run: python3 episodes/2026-11-17-what-if-comet-tail/build_series.py"""
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
RD = {"type": "room", "time": "day"}; RN = {"type": "room", "time": "night"}; RK = {"type": "room", "time": "dusk"}
LAB = {"type": "lab"}; SPACE = {"type": "space"}; STORE = {"type": "store"}
SKYN = {"type": "sky", "time": "night"}; SKYK = {"type": "sky", "time": "dusk"}
def news(h): return {"type": "news", "headline": h}
def ph(msgs=None, **kw): return {"type": "phone", "time": "night", "screen": {"title": "TOWN CHAT", "sub": "312 members", "clock": "21:14", "msgs": msgs or [], **kw}}
def lock(clock, *notes): return {"type": "phone", "time": "night", "screen": {"kind": "lock", "clock": clock, "sub": "Friday", "notes": [{"app": a, "text": t} for a, t in notes]}}
CU = {"zoom": 1.1, "y": 0.6}
PUSH = {"zoom": 1.15, "y": .5, "push": .12}
SHAKE = {"zoom": 1.05, "y": .55, "shake": .6}
CLIFF = [{"type": "riser"}, {"type": "hit", "at": .9}]
COMET = [{"type": "comet"}]
COMET_L = [{"type": "comet", "x": 300, "y": 360, "angle": 330, "length": 760}]
INSIDE = [{"type": "comet", "inside": True}]
CLOUDS = [{"type": "clouds"}]
def end(t): return {"speaker": N, "say": t, "end": True}
def recap(t, set_, cast, **kw):
    l = L(N, t, set_, cast, **kw); l["shortOnly"] = True; return l
def town(expr="neutral", pose="idle"):
    return [c("kid", .15, pose=pose, expr=expr, depth=.5), c("friend", .38, pose=pose, expr=expr, depth=.6),
            c("boss", .62, pose="idle", expr=expr, depth=.6), c("scientist", .85, pose=pose, expr=expr, depth=.5)]
def card(t, sub=None, color="#2F7BFF"): return {"type": "card", "text": t, **({"sub": sub} if sub else {}), "color": color}
def masked(x=.5, scale=1.6, **kw): return c("bossMask", x, pose=kw.pop("pose", "panic"), expr="scared", scale=scale, **kw)

p1 = [
 L(N, "What if Earth flew through a *comet's tail* today?", SKYN, [c("hero", .5, pose="point", expr="shocked", scale=1.1, depth=.3)], fx=COMET, camera=PUSH, sfx=[{"type": "riser"}]),
 L(N, "Monday. A new comet lights up the *evening sky*.", SKYK, [], fx=COMET),
 L(N, "Astronomers call it Comet *Vela*. It's beautiful.", SK, town("happy"), fx=COMET_L),
 L(N, "Then the news finds one small *detail*.", news("COMET TAIL: TOXIC GAS"), [c("bit", .8, expr="shocked", scale=.9)], sfx=[{"type": "alarm"}]),
 L(N, "Phones buzz. Every phone. All at *once*.", lock("19:02", ("NEWS", "Comet tail has toxic gas?")), [], sfx=[{"type": "buzz"}, {"type": "ding", "at": .3}]),
 L(N, "The tail contains a poison gas. *Cyanogen*.", LAB, [c("scientist", .5, pose="think", expr="shocked", scale=1.7)]),
 L(N, "And on Friday night, Earth passes *through it*.", SPACE, [], fx=[{"type": "comet", "x": 820, "y": 900, "angle": 180, "length": 900}], ui={"type": "counter", "from": 5, "to": 4, "suffix": " DAYS", "label": "UNTIL THE TAIL"}, sfx=CLIFF),
 L("boss", "Everybody stay calm! *I* am calm!", SD, [c("boss", .5, pose="panic", expr="scared", scale=1.9)], camera=SHAKE),
 L(N, "Mayor Doyle is wearing a *gas mask*.", SD, [masked(.5, 1.9)], ui={"type": "stamp", "text": "CALM?"}, camera=CU),
 L("boss", "It's my *lucky* gas mask.", SD, [masked(.5, 1.9)], camera=CU),
 L("hero", "Bit, how bad is this? *Honestly*.", RN, [c("hero", .3, pose="phone", expr="scared", scale=1.5), c("bit", .74, expr="think", scale=.9)]),
 L("bit", "Honestly? Earth already did this. In *1910*.", RN, [c("bit", .5, expr="smug", scale=1.7)], ui=card("MAY 1910", "HALLEY'S COMET")),
 L("bit", "On May nineteenth, 1910, we flew through Halley's *tail*.", SPACE, [c("bit", .5, expr="happy", scale=1.0)], fx=[{"type": "comet", "x": 700, "y": 700, "angle": 200, "length": 1000}]),
 L("bit", "Scientists found cyanogen in that tail *too*.", news("REAL: 1910, CYANOGEN"), [c("bit", .8, expr="neutral", scale=.9)]),
 L("hero", "And? What *happened*?", RN, [c("hero", .5, pose="shrug", expr="scared", scale=1.9)], camera=CU),
 L("bit", "The planet *panicked*.", news("1910: PLANET PANICS"), [c("bit", .8, expr="glitch", scale=.9)], sfx=[{"type": "glitch"}]),
 L("hero", "The whole *planet*?", RN, [c("hero", .5, pose="panic", expr="shocked", scale=1.9)], camera=SHAKE),
 L(N, "At the door, Grandpa Ezra holds a dusty *box*.", SN, [c("scientist", .5, pose="idle", expr="smug", scale=1.7)], sfx=[{"type": "knock"}]),
 L("scientist", "My grandpa bought these in 1910.", SN, [c("scientist", .5, pose="point", expr="happy", scale=1.9)], camera=CU),
 L(N, "The label says: *comet pills*.", RN, [c("hero", .5, pose="facepalm", expr="shocked", scale=1.6)], ui=card("COMET PILLS", "EST. 1910", "#FF4A3D"), sfx=CLIFF),
 L(N, "Real history. And it's about to *repeat*.", SKYN, [c("hero", .5, pose="idle", expr="scared", scale=1.1, depth=.3)], fx=COMET),
 end("Follow for part two."),
]

p2 = [
 recap("Part two. A comet tail full of *poison gas*.", SKYN, [], fx=COMET),
 L(N, "Tuesday. Bit opens the old 1910 *newspapers*.", LAB, [c("bit", .5, expr="think", scale=1.6)], ui={"type": "list", "title": "1910", "items": ["poison gas?", "end of the world?"]}),
 L("bit", "A famous French astronomer, Camille *Flammarion*, warned...", LAB, [c("bit", .5, expr="neutral", scale=1.6)]),
 L("bit", "...the gas could snuff out *all life*.", news("1910: ALL LIFE IN DANGER?"), [c("bit", .8, expr="shocked", scale=.9)], sfx=[{"type": "boom"}]),
 L("bit", "He didn't even say it was *likely*.", RN, [c("bit", .5, expr="smug", scale=1.6)]),
 L("bit", "Too late. People bought *anti-comet pills*.", STORE, [c("bit", .5, expr="sad", scale=1.4)], ui={"type": "list", "title": "SOLD IN 1910", "items": ["anti-comet pills", "gas masks", "comet umbrellas"]}),
 L("hero", "Comet *umbrellas*?", RN, [c("hero", .5, pose="shrug", expr="shocked", scale=2.0)], camera=CU),
 L("bit", "Very popular. Zero *stars*.", RN, [c("bit", .5, expr="happy", scale=1.7)]),
 L("bit", "Some people papered over their *keyholes*.", RD, [c("kid", .5, pose="point", expr="scared", scale=1.6)]),
 L(N, "Jay's mom tapes the *keyhole*. Just in case.", RD, [c("hero", .5, pose="facepalm", expr="angry", scale=1.7)]),
 L(N, "Now it's 2026. And the town chat *explodes*.", ph([{"from": "them", "name": "Mayor Doyle", "text": "WHERE DO I BUY COMET PILLS"}]), [], sfx=[{"type": "ding"}, {"type": "ding", "at": .3}]),
 L(N, "Somebody already sells them *online*.", ph([{"from": "them", "name": "Mayor Doyle", "text": "WHERE DO I BUY COMET PILLS"}, {"from": "them", "name": "StarSafe Shop", "text": "COMET PILLS. $99. Only 50 left!"}]), [], sfx=[{"type": "ding"}]),
 L(N, "Forty-nine left. *Thirty*. *Twelve*.", ph([{"from": "them", "name": "StarSafe Shop", "text": "COMET PILLS. $99. Only 12 left!"}]), [], ui={"type": "counter", "from": 49, "to": 12, "label": "PILLS LEFT"}),
 L("boss", "I bought two hundred. For the *town*.", SD, [masked(.5, 1.9)], camera=CU, sfx=[{"type": "ring"}]),
 L("friend", "Two hundred? Mayor, they're ninety-nine *dollars*!", SD, [c("friend", .3, pose="point", expr="angry", scale=1.4), masked(.72, 1.4, facing=-1)]),
 L("bit", "And nobody tested a single *pill*.", RN, [c("bit", .5, expr="sad", scale=1.6)]),
 L("boss", "Each. Yes. *Safety first*.", SD, [masked(.5, 1.9)], camera=CU),
 L(N, "Milo opens his piggy bank. Ten *dollars*.", RD, [c("kid", .5, pose="sit", expr="sad", scale=1.7)], ui={"type": "counter", "from": 0, "to": 10, "prefix": "$", "label": "MILO'S SAVINGS"}),
 L("kid", "Is it enough for *one pill*?", RD, [c("kid", .5, pose="idle", expr="sad", scale=1.9)], camera=CU),
 L(N, "Jay looks at Bit. Bit looks at the *website*.", RN, [c("hero", .3, pose="idle", expr="angry", scale=1.4), c("bit", .74, expr="think", scale=.9)]),
 L("bit", "Jay. Something about this shop is *wrong*.", RN, [c("bit", .5, expr="angry", scale=1.8)], sfx=CLIFF, camera=PUSH),
 end("Follow for part three."),
]

p3 = [
 recap("Part three. Everyone is buying ninety-nine dollar *comet pills*.", STORE, [masked(.5, 1.4)]),
 L(N, "Wednesday. Bit traces the StarSafe *Shop*.", LAB, [c("bit", .5, expr="think", scale=1.6)], fx=[{"type": "glitch"}], sfx=[{"type": "glitch"}]),
 L("bit", "The website was made... on *Monday*.", LAB, [c("bit", .5, expr="shocked", scale=1.7)], ui=card("SITE CREATED", "MONDAY, 18:02", "#FF4A3D")),
 L("hero", "One hour after the comet *news*.", RN, [c("hero", .5, pose="think", expr="angry", scale=1.8)], camera=CU),
 L(N, "Nia orders one pill. For *science*.", RD, [c("friend", .5, pose="phone", expr="smug", scale=1.7)], sfx=[{"type": "pop"}]),
 L(N, "It arrives the next morning in a tiny *envelope*.", SD, [c("friend", .5, pose="idle", expr="happy", scale=1.6)], sfx=[{"type": "knock"}]),
 L(N, "Bit scans it. Jay and Nia *lean in*.", LAB, [c("hero", .2, pose="idle", expr="scared", scale=1.1, depth=.3), c("bit", .5, expr="think", scale=1.3), c("friend", .8, pose="idle", expr="scared", scale=1.1, depth=.3, facing=-1)], sfx=[{"type": "tick"}]),
 L("bit", "Ingredients: sugar. Food coloring. And... more *sugar*.", LAB, [c("bit", .5, expr="smug", scale=1.7)], ui={"type": "bars", "items": [{"label": "SUGAR", "value": 0.97, "color": "#FFD400"}, {"label": "COLOR", "value": 0.03, "color": "#FF4A3D"}, {"label": "MAGIC", "value": 0.0}], "tag": "COMET PILL"}),
 L("friend", "A ninety-nine dollar *candy*.", LAB, [c("friend", .5, pose="facepalm", expr="angry", scale=1.8)], camera=CU),
 L("hero", "And the gas? Is the gas *real*?", RN, [c("hero", .5, pose="shrug", expr="scared", scale=1.8)]),
 L(N, "Grandpa Ezra spreads out his old *star charts*.", RK, [c("scientist", .5, pose="point", expr="happy", scale=1.6)], ui=card("COMET VELA", "TAIL: 30 MILLION MILES")),
 L("scientist", "A comet tail is huge. But *thin*.", RK, [c("scientist", .5, pose="think", expr="neutral", scale=1.8)], camera=CU),
 L("scientist", "Flammarion said it: far sparser than a *cloud*.", SKYK, [c("scientist", .5, pose="idle", expr="smug", scale=1.4)], fx=COMET_L),
 L("bit", "Translation: the scary gas is basically *nothing*.", RN, [c("bit", .5, expr="happy", scale=1.7)], ui={"type": "stamp", "text": "HARMLESS", "color": "#2FBF71"}),
 L("hero", "Then we tell everyone. *Tonight*.", RN, [c("hero", .5, pose="point", expr="grin", scale=1.9)], camera=CU),
 L(N, "Jay posts a video. Sugar, sugar, *sugar*.", ph([{"from": "me", "text": "The comet pills are SUGAR. Video ↑"}]), [], sfx=[{"type": "pop"}]),
 L(N, "Three likes. One is his *mom*.", ph([{"from": "me", "text": "The comet pills are SUGAR. Video ↑"}], seen="3 likes"), [], camera={"zoom": 1.06, "y": .5}),
 L(N, "And the shop posts a new *offer*.", ph([{"from": "me", "text": "The comet pills are SUGAR. Video ↑"}, {"from": "them", "name": "StarSafe Shop", "text": "NEW! COMET-PROOF UMBRELLAS. $199"}]), [], sfx=[{"type": "ding"}, {"type": "hit", "at": .5}]),
 L(N, "Mayor Doyle buys *the first one*.", SD, [masked(.5, 1.9)], ui={"type": "stamp", "text": "SOLD"}, sfx=CLIFF, camera=PUSH),
 end("Follow for part four."),
]

p4 = [
 recap("Part four. The pills are *sugar*. Nobody listens.", RN, [c("hero", .5, pose="facepalm", expr="angry", scale=1.7)]),
 L(N, "Thursday. Main Street looks like a *movie*.", SD, town("scared"), fx=[{"type": "vignette"}]),
 L(N, "Gas masks. Umbrellas. Tape on every *keyhole*.", SD, [c("kid", .2, pose="idle", expr="scared", scale=1.1, depth=.3), masked(.5, 1.2), c("friend", .8, pose="idle", expr="neutral", scale=1.1, depth=.3)]),
 L("boss", "Citizens! Pills at noon. Umbrellas at *one*!", SD, [masked(.5, 1.9)], camera=CU, sfx=[{"type": "siren", "volume": 0.4}]),
 L("friend", "Mayor, it's a scam. Bit *tested* the pills.", SD, [c("friend", .3, pose="point", expr="angry", scale=1.4), masked(.72, 1.4, facing=-1)]),
 L("boss", "A robot told you? On the *internet*?", SD, [masked(.5, 1.9)], camera=CU),
 L("bit", "Excuse me. I am a *very* serious robot.", SD, [c("bit", .5, expr="angry", scale=1.6)]),
 L(N, "Bit's screen shows a smiley face. Not *helping*.", SD, [c("bit", .5, expr="happy", scale=1.8)], camera=CU, sfx=[{"type": "pop"}]),
 L(N, "Then Grandpa Ezra steps onto the *bench*.", SD, [c("scientist", .5, pose="wave", expr="neutral", scale=1.7)]),
 L("scientist", "In 1910, everyone was scared like you. *Everyone*.", SD, [c("scientist", .5, pose="point", expr="sad", scale=1.9)], camera=CU),
 L("scientist", "And Earth flew through that tail. And *nothing* happened.", SPACE, [c("scientist", .5, pose="idle", expr="happy", scale=.9)], fx=[{"type": "comet", "x": 700, "y": 700, "angle": 200, "length": 1000}]),
 L("scientist", "The only thing people lost was *money*.", SD, [c("scientist", .5, pose="shrug", expr="smug", scale=1.8)]),
 L(N, "The crowd laughs. One mask comes *off*.", SD, town("happy"), sfx=[{"type": "ding"}]),
 L(N, "Then *ten*.", SD, town("grin", "cheer"), sfx=[{"type": "powerup"}]),
 L(N, "Mayor Doyle keeps his on. *Just in case*.", SD, [masked(.5, 1.9)], camera=CU),
 L(N, "That night the shop page shows: *closed*.", ph([{"from": "them", "name": "StarSafe Shop", "text": "Store closed. Thank you for your trust!"}]), [], ui={"type": "stamp", "text": "GONE"}, sfx=[{"type": "powerdown"}]),
 L("friend", "They ran. With everyone's *money*.", RN, [c("friend", .5, pose="facepalm", expr="angry", scale=1.8)]),
 L("bit", "Not everyone's. I kept the *receipts*.", RN, [c("bit", .5, expr="smug", scale=1.8)], camera=CU, ui=card("REFUNDS", "312 ORDERS SAVED", "#2FBF71")),
 L(N, "But Grandpa Ezra isn't *smiling*.", RK, [c("scientist", .5, pose="idle", expr="sad", scale=1.8)], sfx=CLIFF, camera=PUSH),
 end("Follow for part five."),
]

p5 = [
 recap("Part five. Scam over. But Grandpa is *sad*.", RK, [c("scientist", .5, pose="idle", expr="sad", scale=1.6)]),
 L(N, "Jay finds Ezra on the porch, looking *up*.", SK, [c("hero", .3, pose="idle", expr="neutral", scale=1.3), c("scientist", .7, pose="sit", expr="sad", scale=1.3, facing=-1)], fx=COMET_L),
 L("hero", "Grandpa, the comet is harmless. Why so *sad*?", SK, [c("hero", .5, pose="shrug", expr="sad", scale=1.8)], camera=CU),
 L("scientist", "Because I've never actually *seen* one.", SK, [c("scientist", .5, pose="sit", expr="sad", scale=1.8)], camera=CU),
 L(N, "He opens a photo. A boy on a *roof*.", RK, [c("scientist", .5, pose="idle", expr="sad", scale=1.5)], ui=card("MY GRANDPA", "MAY 1910")),
 L("scientist", "My grandpa saw Halley's Comet in *1910*.", RK, [c("scientist", .5, pose="point", expr="happy", scale=1.7)]),
 L("scientist", "He said: it's back in 1986. Watch for *me*.", RK, [c("scientist", .5, pose="idle", expr="sad", scale=1.8)], camera=CU),
 L(N, "In 1986, Ezra was working nights. Clouds. *Missed it*.", SN, [c("scientist", .5, pose="facepalm", expr="sad", scale=1.4)], fx=CLOUDS),
 L("bit", "Halley comes back in *2061*. July twenty-eighth.", SPACE, [c("bit", .5, expr="neutral", scale=1.0)], ui={"type": "counter", "from": 2026, "to": 2061, "label": "NEXT HALLEY"}),
 L("scientist", "I'll be a hundred and twelve. I'm not *waiting*.", RK, [c("scientist", .5, pose="shrug", expr="smug", scale=1.8)], camera=CU),
 L("bit", "Fun fact. Mark Twain was born with Halley's *Comet*.", LAB, [c("bit", .5, expr="happy", scale=1.6)], ui=card("1835", "MARK TWAIN IS BORN")),
 L("bit", "He said he'd leave with it. He *did*.", LAB, [c("bit", .5, expr="neutral", scale=1.6)], ui=card("1910", "HALLEY RETURNS")),
 L("hero", "Bit. That is the *opposite* of fun.", SK, [c("hero", .5, pose="facepalm", expr="angry", scale=1.9)], camera=CU),
 L("scientist", "Ha! I like him. *This* comet is my chance.", SK, [c("scientist", .5, pose="cheer", expr="grin", scale=1.8)], fx=COMET_L),
 L(N, "Friday night. Biggest show of the *century*.", SKYN, [], fx=COMET),
 L(N, "Jay promises. Front row. The best *roof* in town.", SN, [c("hero", .3, pose="point", expr="grin", scale=1.3), c("scientist", .7, pose="idle", expr="happy", scale=1.3, facing=-1)]),
 L(N, "Then Bit checks the *weather*.", RN, [c("bit", .5, expr="think", scale=1.6)], sfx=[{"type": "tick"}]),
 L("bit", "Friday night: clouds. A hundred *percent*.", RN, [c("bit", .5, expr="sad", scale=1.8)], ui={"type": "counter", "from": 0, "to": 100, "suffix": "%", "label": "CLOUDS FRIDAY"}, sfx=CLIFF, camera=PUSH),
 end("Follow for part six."),
]

p6 = [
 recap("Part six. Grandpa's last chance. Then: *clouds*.", SN, [c("scientist", .5, pose="idle", expr="sad", scale=1.5)], fx=CLOUDS),
 L("bit", "This happened in 1910 too. In *Brooklyn*.", RN, [c("bit", .5, expr="neutral", scale=1.6)], ui=card("1910", "A ROOFTOP COMET PARTY")),
 L("bit", "A lady threw a comet party for thirteen *guests*.", SN, town("happy", "cheer")),
 L("bit", "Telescope on the roof. And then? *Clouds*.", SN, town("sad"), fx=CLOUDS, sfx=[{"type": "powerdown"}]),
 L("friend", "So we need to get *above* the clouds.", RN, [c("friend", .5, pose="think", expr="neutral", scale=1.8)], camera=CU),
 L("hero", "A plane? A *mountain*?", RN, [c("hero", .5, pose="shrug", expr="scared", scale=1.9)]),
 L(N, "Milo raises his hand. Shy. *Hopeful*.", RD, [c("kid", .5, pose="wave", expr="happy", scale=1.8)]),
 L("kid", "Bit can *fly*. A little.", RD, [c("kid", .5, pose="point", expr="grin", scale=1.9)], camera=CU),
 L(N, "Everyone turns to *Bit*.", RN, [c("bit", .5, expr="shocked", scale=1.7)], sfx=[{"type": "hit"}], camera=PUSH),
 L("bit", "I float. Three feet. Above a *sofa*.", RN, [c("bit", .5, expr="sad", scale=1.7)], ui={"type": "counter", "from": 0, "to": 3, "suffix": " FT", "label": "BIT'S RECORD"}),
 L("hero", "The clouds start at six thousand *feet*.", RN, [c("hero", .5, pose="point", expr="neutral", scale=1.8)], ui={"type": "counter", "from": 0, "to": 6000, "suffix": " FT", "label": "CLOUD BASE"}),
 L(N, "So they build *a balloon*.", RD, [c("hero", .2, pose="idle", expr="grin", scale=1.1, depth=.3), c("bit", .5, expr="happy", scale=1.2), c("friend", .8, pose="idle", expr="grin", scale=1.1, depth=.3, facing=-1)], sfx=[{"type": "pop"}]),
 L(N, "Party balloons. Fifty-two of them. All *helium*.", SD, [c("kid", .5, pose="cheer", expr="grin", scale=1.6)], ui={"type": "counter", "from": 0, "to": 52, "label": "BALLOONS"}),
 L(N, "Bit gets a camera. A *live stream*.", LAB, [c("bit", .5, expr="smug", scale=1.6)], ui={"type": "notify", "app": "ZYLO LIVE", "title": "Bit is going live", "body": "Above the clouds"}),
 L(N, "Grandpa Ezra gets a tablet. And the *roof*.", SN, [c("scientist", .5, pose="sit", expr="happy", scale=1.6)], fx=CLOUDS),
 L(N, "Friday, eleven p.m. One hour until *the tail*.", SN, town("neutral"), fx=CLOUDS, ui={"type": "clock", "text": "23:00", "to": "23:01"}),
 L("bit", "If my battery hits zero up there... I *fall*.", SN, [c("bit", .5, expr="sad", scale=1.8)], ui={"type": "counter", "from": 100, "to": 100, "suffix": "%", "label": "BATTERY"}, camera=CU),
 L("hero", "Then we'll *catch* you. Go!", SN, [c("hero", .5, pose="point", expr="grin", scale=1.9)], camera=CU),
 L(N, "Bit lets go of Jay's hand. And *rises*.", SKYN, [c("bit", .5, expr="happy", scale=.9, lift=420)], fx=CLOUDS, sfx=CLIFF, camera=PUSH),
 end("Follow for part seven."),
]

p7 = [
 recap("Part seven. Bit rises toward the *clouds*.", SKYN, [c("bit", .5, expr="happy", scale=.9)], fx=CLOUDS),
 L(N, "Two thousand feet. The town is a little *map*.", SKYN, [c("bit", .5, expr="shocked", scale=1.0)], ui={"type": "counter", "from": 900, "to": 2000, "suffix": " FT", "label": "BIT'S ALTITUDE"}),
 L("bit", "This is *higher* than the sofa.", SKYN, [c("bit", .5, expr="shocked", scale=1.6)], camera=CU),
 L(N, "Four thousand feet. Cold. The camera *fogs*.", SKYN, [c("bit", .5, expr="sad", scale=1.4)], fx=[{"type": "snow"}], ui={"type": "counter", "from": 2000, "to": 4000, "suffix": " FT", "label": "BIT'S ALTITUDE"}),
 L(N, "On the roof, the tablet shows *gray*.", SN, [c("scientist", .5, pose="sit", expr="sad", scale=1.6)], fx=CLOUDS),
 L(N, "Inside the cloud, Bit sees *nothing*.", {"type": "sky", "time": "night"}, [c("bit", .5, expr="sad", scale=1.3)], fx=[{"type": "clouds", "y": 2000}], sfx=[{"type": "buzz"}]),
 L(N, "Battery: thirty *percent*.", SKYN, [c("bit", .5, expr="sad", scale=1.6)], fx=[{"type": "clouds", "y": 2000}], ui={"type": "counter", "from": 41, "to": 30, "suffix": "%", "label": "BATTERY"}),
 L("bit", "Hello, cloud. You are very *wet*.", SKYN, [c("bit", .5, expr="sad", scale=1.7)], fx=[{"type": "clouds", "y": 2000}], camera=CU),
 L("hero", "Bit, come back! It's not *worth* it!", SN, [c("hero", .5, pose="panic", expr="scared", scale=1.9)], camera=SHAKE),
 L(N, "Ezra grips the tablet. *Please*.", SN, [c("scientist", .5, pose="sit", expr="scared", scale=1.8)], fx=CLOUDS, camera=CU),
 L("bit", "Ezra waited forty years. I can wait *one cloud*.", SKYN, [c("bit", .5, expr="angry", scale=1.7)], fx=[{"type": "clouds", "y": 2000}]),
 L(N, "Five thousand. Five thousand five *hundred*.", SKYN, [c("bit", .5, expr="neutral", scale=1.3)], fx=[{"type": "clouds", "y": 2000}], ui={"type": "counter", "from": 5000, "to": 5500, "suffix": " FT", "label": "BIT'S ALTITUDE"}),
 L(N, "A balloon *pops*.", SKYN, [c("bit", .5, expr="shocked", scale=1.6)], fx=[{"type": "clouds", "y": 2000}], sfx=[{"type": "pop"}, {"type": "hit", "at": .2}], camera=SHAKE),
 L(N, "Then *two more*.", SKYN, [c("bit", .5, expr="shocked", scale=1.8)], fx=[{"type": "clouds", "y": 2000}], sfx=[{"type": "pop"}, {"type": "pop", "at": .3}], camera=SHAKE),
 L(N, "Bit starts to *sink*.", SKYN, [c("bit", .5, expr="sad", scale=1.3, lift=0)], fx=[{"type": "clouds", "y": 2000}], sfx=[{"type": "powerdown"}]),
 L("friend", "Come on, Bit. Come *on*.", SN, [c("friend", .5, pose="idle", expr="scared", scale=1.8)], fx=CLOUDS, camera=CU),
 L(N, "Milo grabs Jay's phone. Types *fast*.", RN, [c("kid", .5, pose="phone", expr="angry", scale=1.8)], sfx=[{"type": "tick"}]),
 L("kid", "Bit! Drop the *camera case*! It's heavy!", RN, [c("kid", .5, pose="point", expr="angry", scale=1.9)], camera=CU),
 L(N, "Bit drops it. Bit *rises*.", SKYN, [c("bit", .5, expr="happy", scale=1.3, lift=380)], fx=[{"type": "clouds", "y": 2000}], sfx=[{"type": "whoosh"}, {"type": "powerup", "at": .3}]),
 L(N, "Six thousand feet. Battery: nine *percent*.", SKYN, [c("bit", .5, expr="neutral", scale=1.4)], fx=[{"type": "clouds", "y": 2000}], ui={"type": "counter", "from": 15, "to": 9, "suffix": "%", "label": "BATTERY"}),
 L(N, "Eleven fifty-nine. Then the cloud *opens*.", SKYN, [c("bit", .5, expr="shocked", scale=1.0)], ui={"type": "clock", "text": "23:59"}, sfx=[{"type": "riser"}]),
 L(N, "And the signal *dies*.", SN, [c("scientist", .5, pose="sit", expr="shocked", scale=1.8)], fx=CLOUDS + [{"type": "glitch"}], sfx=[{"type": "glitch"}, {"type": "hit", "at": .5}], camera=PUSH),
 end("Follow for the final part."),
]

p8 = [
 recap("Final part. Bit broke through. Then the signal *died*.", SN, [c("scientist", .5, pose="sit", expr="sad", scale=1.6)], fx=CLOUDS),
 L(N, "The roof is silent. Ezra holds the *tablet*.", SN, [c("scientist", .5, pose="sit", expr="sad", scale=1.8)], fx=CLOUDS, camera=CU),
 L(N, "Three seconds. *Four*.", SN, town("sad"), fx=CLOUDS, sfx=[{"type": "heartbeat"}]),
 L(N, "Then the screen *lights up*.", SKYN, [], fx=[{"type": "comet", "x": 560, "y": 520, "angle": 205, "length": 1100, "size": 1.3}], sfx=[{"type": "riser"}, {"type": "ding", "at": .6}]),
 L(N, "Above the clouds: Comet Vela. Huge. *Glowing*.", SKYN, [c("bit", .5, expr="happy", scale=.8, depth=.4)], fx=[{"type": "comet", "x": 560, "y": 520, "angle": 205, "length": 1100, "size": 1.3}], camera=PUSH),
 L(N, "Grandpa Ezra doesn't say a *word*.", SN, [c("scientist", .5, pose="sit", expr="happy", scale=1.9)], fx=CLOUDS, camera=CU),
 L("scientist", "Grandpa... I'm *watching* it.", SN, [c("scientist", .5, pose="idle", expr="happy", scale=1.9)], camera=CU),
 L("scientist", "It's more beautiful than Grandpa *said*.", SN, [c("scientist", .5, pose="cheer", expr="grin", scale=1.8)], fx=COMET_L),
 L(N, "Midnight. Earth slides into the *tail*.", SPACE, [], fx=[{"type": "comet", "x": 820, "y": 900, "angle": 180, "length": 900}], ui={"type": "clock", "text": "00:00"}),
 L(N, "The whole town *holds its breath*.", SN, town("scared"), fx=INSIDE),
 L(N, "And nothing happens. *Exactly* like 1910.", SN, town("grin", "cheer"), fx=INSIDE, sfx=[{"type": "powerup"}], ui={"type": "stamp", "text": "STILL ALIVE", "color": "#2FBF71"}),
 L(N, "Battery: two percent. Bit *drifts down*.", SKYN, [c("bit", .5, expr="sad", scale=1.3, lift=60)], fx=INSIDE, ui={"type": "counter", "from": 4, "to": 2, "suffix": "%", "label": "BATTERY"}, sfx=[{"type": "powerdown"}]),
 L(N, "Right into Milo's *arms*.", SN, [c("kid", .4, pose="cheer", expr="grin", scale=1.6), c("bit", .62, expr="happy", scale=.7)], sfx=[{"type": "pop"}]),
 L("bit", "Told you. Very *serious* robot.", SN, [c("bit", .5, expr="smug", scale=1.7)], camera=CU),
 L(N, "Ezra hugs Bit. Then Jay. Then the *mayor*.", SN, [c("scientist", .3, pose="cheer", expr="grin", scale=1.4), masked(.72, 1.4, facing=-1)]),
 L(N, "Mayor Doyle finally takes off the *mask*.", SN, [c("boss", .5, pose="idle", expr="happy", scale=1.9)], camera=CU),
 L(N, "Under it, he's wearing *another* one.", SN, [masked(.5, 1.9)], camera=CU, sfx=[{"type": "ding"}]),
 L(N, "In 1910, everyone survived the tail. Even pill *buyers*.", news("REAL: 1910, ALL FINE"), [c("bit", .8, expr="happy", scale=.9)]),
 L(N, "Somewhere, a sugar pill rolls under a *sofa*.", RD, [], ui={"type": "stamp", "text": "$99", "color": "#FF4A3D"}, sfx=[{"type": "tick"}]),
 L("kid", "Halley comes back in 2061. I'll be *forty-four*.", RD, [c("kid", .5, pose="point", expr="grin", scale=1.9)], ui=card("JULY 28, 2061", "HALLEY RETURNS")),
 L("kid", "I'll watch it. For *Grandpa*.", SKYN, [c("kid", .5, pose="idle", expr="happy", scale=1.1, depth=.3)], fx=COMET),
 end("Follow for a new What if every day."),
]

parts = [("The Tail", p1), ("Comet Pills", p2), ("Sugar", p3), ("Masks Off", p4),
         ("Grandpa's Comet", p5), ("Clouds", p6), ("Above the Clouds", p7), ("The Glow", p8)]

series = {
 "title": "What If Earth Flew Through a Comet's Tail Today?",
 "rubric": "what-if: disaster (real history)", "mood": "wonder", "seed": 6300, "every": 2,
 "names": {"hero": "JAY", "bit": "BIT", "friend": "NIA", "boss": "MAYOR DOYLE", "scientist": "GRANDPA EZRA", "kid": "MILO"},
 "finale": {"text": "THE END", "sub": "Follow for a new What if every day"},
 "parts": [{"title": t, "lines": ls} for t, ls in parts],
}
(D / "series.json").write_text(json.dumps(series, indent=1, ensure_ascii=False) + "\n")

hooks = ["What If Earth Flew Through a Comet's Tail?", "What If Everyone Bought Comet Pills?", "What If the Comet Pills Were Fake?",
         "What If a Whole Town Panicked?", "What If You Never Saw a Comet?", "What If Clouds Ruined the Comet?",
         "What If Your AI Flew Above the Clouds?", "What If the Comet Tail Hit at Midnight?"]
blurbs = [
 "A new comet's tail holds poison gas, and Earth passes through it on Friday. In May 1910, Earth flew through Halley's Comet's tail.",
 "In 1910 people bought anti-comet pills, gas masks and comet umbrellas. Today an online shop sells $99 comet pills.",
 "Bit tests a $99 comet pill. Grandpa Ezra explains why a comet tail is huge but incredibly thin.",
 "Main Street is full of gas masks and taped keyholes, until Grandpa Ezra tells the town what really happened in 1910.",
 "Grandpa Ezra has never seen a comet. Halley's Comet comes back on July 28, 2061, and clouds are coming on Friday.",
 "In 1910, a rooftop comet party in Brooklyn got clouded out. So Jay, Nia and Milo send Bit up on 52 balloons.",
 "Bit climbs into the clouds on a dying battery while Grandpa Ezra watches a gray screen.",
 "Midnight: Earth slides into the comet's tail. In 1910, everybody survived it. Even the pill buyers.",
]
tags = ["what if", "halley's comet", "comet tail", "1910 comet panic", "comet pills", "animation", "story", "shorts"]
def ttl(i):
    t = f"{hooks[i]} Part {i + 1} #shorts"
    t2 = f"{hooks[i]} ☄️ Part {i + 1} #shorts"
    return t2 if len(t2) <= 60 else t
meta = {}
for i in range(8):
    meta[f"part{i + 1}"] = {
        "title": ttl(i), "short": True,
        "description": f"{blurbs[i]}\nAn original animated \"What if...?\" story by zylo, part {i + 1} of 8.\n\nFollow for a new \"What if...?\" every day.\n\n#whatif #halleyscomet #comet #animation #shorts",
        "tags": tags, "categoryId": "1", "privacy": "public", "madeForKids": False, "syntheticMedia": False}
meta["full"] = {
    "title": "What If Earth Flew Through a Comet Tail Today? (Full Story)",
    "description": "In May 1910, Earth flew through the tail of Halley's Comet. Its gas made headlines, people bought anti-comet pills, and nothing happened. What if it happened today?\nAn original animated \"What if...?\" story by zylo: all eight parts in one.\n\n{chapters}\nFollow for a new \"What if...?\" every day.\n\n#whatif #halleyscomet #comet #animation #story",
    "tags": [t for t in tags if t != "shorts"], "categoryId": "1", "privacy": "public", "madeForKids": False, "syntheticMedia": False}
mp = D / "metadata.json"
if mp.exists():
    old = json.loads(mp.read_text())
    for k, v in meta.items():
        if "publishAt" in old.get(k, {}): v["publishAt"] = old[k]["publishAt"]
mp.write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")

(D / "full").mkdir(exist_ok=True)
(D / "full/thumb.json").write_text(json.dumps({
 "text": "COMET *PILLS*?!", "badge": "FULL STORY", "cropY": 880, "set": {"type": "street", "time": "night"},
 "fx": [{"type": "comet", "x": 640, "y": 1000, "angle": 200, "length": 700}],
 "cast": [{"id": "boss", "x": 0.93, "pose": "panic", "expr": "scared", "scale": 1.0, "y": 1640, "facing": -1},
          {"id": "hero", "x": 0.72, "pose": "point", "expr": "shocked", "scale": 1.3, "y": 1760},
          {"id": "bit", "x": 0.56, "expr": "shocked", "scale": 0.55, "y": 1215}]}, indent=1) + "\n")

for i, (t, ls) in enumerate(parts):
    spoken = [l for l in ls if not l.get("end")]
    w = sum(len(re.sub(r"[*\"]", "", l["say"]).split()) for l in spoken)
    long_ = [l["say"] for l in spoken if len(re.sub(r"[*\"]", "", l["say"]).split()) > 9]
    print(f"part{i + 1} {t!r}: {len(ls)} lines, {w} words", "LONG:" if long_ else "", long_ or "")
for k, v in meta.items():
    print(k, len(v["title"]), v["title"])
