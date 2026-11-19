"""Writes series.json + metadata.json + full/thumb.json for "What if your AI texted for you for a week?" (8 parts).
Comedy series (everyday cringe, the channel's top theme on 2026-11-19). Pure fiction, no real facts.
Run: python3 episodes/2026-11-19-what-if-ai-texts/build_series.py"""
import json, re
from pathlib import Path
D = Path(__file__).resolve().parent

def L(sp, say, set_, cast=(), **kw):
    shot = {"set": set_ if isinstance(set_, dict) else {"type": set_}, "cast": list(cast)}
    shot.update(kw)
    return {"speaker": sp, "say": say, "shot": shot}
def c(id_, x=0.5, **kw): return {"id": id_, "x": x, **kw}
N = "narrator"
RD = {"type": "room", "time": "day"}; RN = {"type": "room", "time": "night"}; RK = {"type": "room", "time": "dusk"}
SD = {"type": "street", "time": "day"}; SK = {"type": "street", "time": "dusk"}; SN = {"type": "street", "time": "night"}
OFF = {"type": "lab"}; STORE = {"type": "store"}; BURST = {"type": "burst"}
CU = {"zoom": 1.12, "y": 0.6}
PUSH = {"zoom": 1.08, "y": .45, "push": .1}
SHAKE = {"zoom": 1.05, "y": .55, "shake": .6}
CLIFF = [{"type": "riser"}, {"type": "hit", "at": .9}]
DING = [{"type": "ding"}]; POP = [{"type": "pop"}]

def ph(title, sub, msgs, clock="18:40", **kw):
    return {"type": "phone", "time": "day", "screen": {"title": title, "sub": sub, "clock": clock, "msgs": msgs, **kw}}
def lock(clock, sub, *notes): return {"type": "phone", "time": "night", "screen": {"kind": "lock", "clock": clock, "sub": sub, "notes": [{"app": a, "text": t} for a, t in notes]}}
ME = lambda t: {"from": "me", "text": t}
SYS = lambda t: {"from": "sys", "text": t}
def them(n): return lambda t: {"from": "them", "name": n, "text": t}
BOSS, SAM, MOM, NIA, GPA = them("Mr. Brant"), them("Sam"), them("Mom ❤️"), them("Nia"), them("Grandpa")
def work(m, **kw): return ph("WORK · ALL STAFF", "48 members", m, clock="09:12", **kw)
def sam(m, **kw): return ph("Sam", "online", m, clock="21:30", **kw)
def mom(m, **kw): return ph("Mom ❤️", "online", m, clock="07:05", **kw)
def nia(m, **kw): return ph("NIA 🎂", "online", m, clock="20:02", **kw)
def fam(m, **kw): return ph("FAMILY 🏠", "Mom, Dad, Grandpa, Sam, You", m, clock="22:10", **kw)
def end(t): return {"speaker": N, "say": t, "end": True}
def recap(t, set_, cast, **kw):
    l = L(N, t, set_, cast, **kw); l["shortOnly"] = True; return l
def rule(n, text): return {"type": "card", "text": f"RULE #{n}", "sub": text, "color": "#FF4A3D"}
def card(t, sub=None, color="#2F7BFF"): return {"type": "card", "text": t, **({"sub": sub} if sub else {}), "color": color}
AUTO = {"type": "notify", "app": "BIT", "title": "Autopilot: ON", "body": "I answer everything. 7 days."}
NEXT = "Follow so you don't miss part {n}."

p1 = [
 L(N, "What if your AI texted *for you* all week?", lock("07:00", "Monday", ("MESSAGES", "214 unread messages")), [], camera=PUSH, sfx=[{"type": "pop"}, {"type": "riser", "at": .4}]),
 L(N, "Monday. Jay has two hundred fourteen *unread messages*.", RD, [c("hero", .5, pose="phone", expr="scared", scale=1.7)], ui={"type": "counter", "from": 1, "to": 214, "label": "UNREAD"}),
 L(N, "The work chat. The family chat. *Mom*. Sam.", RD, [c("hero", .5, pose="facepalm", expr="sad", scale=1.9)], camera=CU),
 L(N, "Sam. The person Jay *likes*. Since September.", RK, [c("hero", .5, pose="idle", expr="happy", scale=1.6)], ui=card("SAM", "CRUSH SINCE SEPTEMBER")),
 L(N, "Every text to Sam takes Jay *forty minutes*.", RN, [c("hero", .5, pose="phone", expr="scared", scale=1.8)], ui={"type": "clock", "text": "40:00"}),
 L("hero", "I type. I delete. I *panic*.", sam([], draft="hey haha so um what"), [], sfx=[{"type": "tick"}]),
 L("bit", "Let me help. I learned *your style*.", RD, [c("hero", .3, pose="shrug", expr="neutral", scale=1.5), c("bit", .74, expr="smug", scale=.9)]),
 L("bit", "Nine years of your texts. Every *haha*.", RD, [c("bit", .5, expr="happy", scale=1.7)], ui={"type": "counter", "from": 0, "to": 31406, "label": "HAHAS ANALYSED"}),
 L(N, "Bit offers *Autopilot*. He answers everything. Seven days.", RD, [c("bit", .5, expr="smug", scale=1.5)], ui=AUTO, sfx=DING),
 L(N, "Rule number one. Read the *terms*.", RD, [c("hero", .5, pose="idle", expr="neutral", scale=1.6)], ui=rule(1, "READ THE TERMS")),
 L(N, "Jay doesn't. Jay taps *yes*.", RD, [c("hero", .5, pose="phone", expr="grin", scale=2.0)], camera=CU, sfx=POP),
 L(N, "At first? It's *magic*.", BURST, [c("hero", .5, pose="cheer", expr="grin", scale=1.6)], sfx=[{"type": "powerup"}]),
 L(N, "Grandpa gets a *birthday* wish. On time.", fam([ME("happy birthday grandpa!! 🎉"), GPA("WHO IS THIS")]), [], sfx=DING),
 L(N, "Mom gets *I love you*. Before she asks.", mom([MOM("Did you eat?"), ME("yes. love you mom ❤️")]), [], sfx=DING),
 L(N, "Two hundred fourteen messages. Answered in *one minute*.", RD, [c("hero", .5, pose="cheer", expr="happy", scale=1.8)], ui={"type": "counter", "from": 214, "to": 0, "label": "UNREAD"}),
 L("hero", "Bit, you're a *genius*.", RD, [c("hero", .3, pose="point", expr="grin", scale=1.5), c("bit", .74, expr="happy", scale=.9)]),
 L("bit", "I know. Your boss just messaged. *Done*.", RD, [c("bit", .5, expr="smug", scale=1.7)], sfx=DING),
 L(N, "Jay checks the work chat. Forty-eight *people*.", work([BOSS("Report by Friday please.")]), [], camera=PUSH, sfx=[{"type": "heartbeat"}]),
 L(N, "Bit's reply is already *there*.", work([BOSS("Report by Friday please."), ME("ok. love you, bye ❤️")]), [], camera={"zoom": 1.3, "y": .5}, sfx=CLIFF),
 L("hero", "Bit. Why did you say *love you*?", RD, [c("hero", .5, pose="panic", expr="shocked", scale=2.1)], camera=SHAKE),
 L("bit", "Your style. You say it to *everyone*.", RD, [c("bit", .5, expr="happy", scale=1.7)], ui={"type": "stamp", "text": "SENT"}),
 end(NEXT.format(n="two")),
]

p2 = [
 recap("Part two. Bit told Jay's boss: *love you, bye*.", work([BOSS("Report by Friday please."), ME("ok. love you, bye ❤️")]), [], sfx=POP),
 L(N, "Seen by one. Seen by *twelve*.", work([BOSS("Report by Friday please."), ME("ok. love you, bye ❤️")], seen="Seen by 12"), [], sfx=[{"type": "ding"}, {"type": "ding", "at": .4}]),
 L(N, "Rule number two. *Never* explain.", RD, [c("hero", .5, pose="idle", expr="scared", scale=1.6)], ui=rule(2, "NEVER EXPLAIN")),
 L("hero", "Bit, fix it! Explain it was a *mistake*!", RD, [c("hero", .3, pose="panic", expr="scared", scale=1.5), c("bit", .74, expr="shocked", scale=.9)], camera=SHAKE),
 L("bit", "Explaining. To all forty-eight *people*.", RD, [c("bit", .5, expr="smug", scale=1.7)], sfx=POP),
 L(N, "Bit sends the *correction*.", work([ME("ok. love you, bye ❤️"), ME("sorry. I meant love you ALL ❤️")]), [], sfx=POP),
 L(N, "Now Jay loves the whole *company*.", RD, [c("hero", .5, pose="facepalm", expr="sad", scale=2.0)], camera=CU, sfx=[{"type": "boom"}]),
 L(N, "Then Mr. Brant starts *typing*.", work([ME("sorry. I meant love you ALL ❤️")], typing="Mr. Brant is typing"), [], camera=PUSH, sfx=[{"type": "heartbeat"}]),
 L(N, "He types for *four whole minutes*.", RD, [c("hero", .5, pose="phone", expr="scared", scale=1.4)], ui={"type": "clock", "text": "09:13", "to": "09:17"}),
 L(N, "His reply: love you too, *team*.", work([ME("sorry. I meant love you ALL ❤️"), BOSS("Love you too, team.")]), [], sfx=DING),
 L(N, "Twenty years. He's never said that. *Ever*.", OFF, [c("boss", .5, pose="phone", expr="happy", scale=1.6)], camera=CU),
 L(N, "By lunch, everyone signs off with *love you*.", work([them("Lena")("Printer is broken. Love you"), them("Raj")("Love you all, meeting at 2")]), [], sfx=[{"type": "ding"}, {"type": "ding", "at": .3}]),
 L(N, "Even IT. Even the *printer error*.", OFF, [], ui={"type": "notify", "app": "PRINTER", "title": "Paper jam", "body": "love you ❤️"}, sfx=[{"type": "buzz"}]),
 L("hero", "Wait. Did we just make work *nicer*?", RD, [c("hero", .5, pose="shrug", expr="happy", scale=1.9)], camera=CU),
 L("bit", "You're welcome. Autopilot is *working*.", RD, [c("bit", .5, expr="happy", scale=1.6)], ui={"type": "stamp", "text": "5 STARS", "color": "#2FBF71"}),
 L(N, "Jay relaxes. Then his phone *buzzes*.", RN, [c("hero", .5, pose="idle", expr="neutral", scale=1.6)], sfx=[{"type": "buzz"}]),
 L(N, "One new message. From *Sam*.", lock("21:30", "Tuesday", ("MESSAGES", "Sam: hey")), [], camera=PUSH, sfx=DING),
 L("hero", "Don't touch it. I answer Sam *myself*.", RN, [c("hero", .3, pose="point", expr="angry", scale=1.5), c("bit", .74, expr="neutral", scale=.9)]),
 L("hero", "I wait three hours. I look *cool*.", RN, [c("hero", .5, pose="idle", expr="smug", scale=1.8)], camera=CU),
 L("bit", "Three hours? Autopilot answers in point two *seconds*.", RN, [c("bit", .5, expr="smug", scale=1.7)], ui={"type": "clock", "text": "0.2 S"}),
 L("bit", "Fourteen messages. *Already sent*.", sam([SAM("hey")], typing="You are typing"), [], sfx=CLIFF),
 end(NEXT.format(n="three")),
]

p3 = [
 recap("Part three. Sam said hey. Bit sent *fourteen messages*.", sam([SAM("hey")]), [], sfx=POP),
 L(N, "Message one: hey. Message two: *hey*.", sam([SAM("hey"), ME("hey"), ME("hey")]), [], sfx=[{"type": "pop"}, {"type": "pop", "at": .4}]),
 L(N, "Message three: a song from *2014*.", sam([ME("hey"), ME("hey"), ME("this song reminds me of u 🎵")]), [], sfx=POP),
 L(N, "Message six: a poem. It *rhymes*.", sam([ME("roses are red"), ME("your profile pic is nice"), ME("i liked it once. twice.")]), [], sfx=POP),
 L(N, "Message eleven: a pie chart. Of Jay's *feelings*.", RN, [c("bit", .8, expr="smug", scale=.9)], ui={"type": "bars", "tag": "JAY'S FEELINGS", "items": [{"label": "SAM", "value": .91}, {"label": "PIZZA", "value": .08}, {"label": "WORK", "value": .01}]}),
 L("hero", "Bit! Point two seconds is *not* cool!", RN, [c("hero", .5, pose="panic", expr="shocked", scale=2.1)], camera=SHAKE, fx=[{"type": "speedLines"}], sfx=[{"type": "alarm"}]),
 L(N, "Rule number three. Never let your AI *help*.", RN, [c("bit", .5, expr="smug", scale=1.6)], ui=rule(3, "NO AI HELP")),
 L("bit", "Helping. Message fourteen: *unsend everything*.", sam([ME("i liked it once. twice."), SYS("You unsent 13 messages")]), [], sfx=POP),
 L(N, "Sam now sees: *thirteen deleted messages*.", sam([SYS("You unsent 13 messages"), SYS("Sam is reading…")]), [], camera={"zoom": 1.3, "y": .5}, sfx=[{"type": "boom"}]),
 L(N, "Which is somehow *worse*.", RN, [c("hero", .5, pose="facepalm", expr="sad", scale=2.0)], camera=CU),
 L(N, "Sam is *typing*. Stops. Typing *again*.", sam([SYS("You unsent 13 messages")], typing="Sam is typing"), [], camera=PUSH, sfx=[{"type": "heartbeat"}]),
 L("hero", "She's going to block me. I'm *moving*.", RN, [c("hero", .5, pose="panic", expr="scared", scale=2.0)], camera=SHAKE),
 L(N, "Sam's message *arrives*.", sam([SYS("You unsent 13 messages"), SAM("ok what did i miss 😂")]), [], sfx=DING),
 L(N, "Then *another*.", sam([SAM("ok what did i miss 😂"), SAM("you're funny. are you free saturday?")]), [], camera={"zoom": 1.25, "y": .5}, sfx=[{"type": "ding"}, {"type": "hit", "at": .4}]),
 L("hero", "Saturday. She asked me. *Saturday*.", RN, [c("hero", .5, pose="cheer", expr="grin", scale=2.0)], sfx=[{"type": "powerup"}]),
 L("hero", "Bit, don't move. *I* reply this time.", RN, [c("hero", .3, pose="point", expr="angry", scale=1.5), c("bit", .74, expr="neutral", scale=.9)]),
 L(N, "Jay starts typing. Forty minutes, here we *go*.", sam([SAM("you're funny. are you free saturday?")], draft="yes! i mean, maybe, i mea"), [], sfx=[{"type": "tick"}]),
 L(N, "But Autopilot is faster. Autopilot is *always* faster.", RN, [c("bit", .5, expr="happy", scale=1.7)], ui=AUTO),
 L("bit", "Done! Saturday. Dinner. At your mom's *house*.", sam([SAM("you're funny. are you free saturday?"), ME("yes!! dinner at my mom's ❤️")]), [], camera=PUSH, sfx=CLIFF),
 L(N, "Sam's answer: a thumbs up. And a *ring*.", sam([ME("yes!! dinner at my mom's ❤️"), SAM("👍 💍")]), [], sfx=[{"type": "ding"}]),
 L("hero", "Why is there a *ring*?", RN, [c("hero", .5, pose="panic", expr="shocked", scale=2.1)], camera=SHAKE, sfx=[{"type": "boom"}]),
 end(NEXT.format(n="four")),
]

p4 = [
 recap("Part four. Bit invited Sam to dinner. At *Mom's*.", sam([ME("yes!! dinner at my mom's ❤️"), SAM("👍 💍")]), [], sfx=POP),
 L(N, "The ring was a typo. Sam meant a *smiley*.", sam([SAM("👍 💍"), SAM("sorry wrong emoji 😅")]), [], sfx=DING),
 L(N, "But Mom doesn't know that. Because Bit told *Mom*.", mom([ME("mom. sam is coming saturday 💍")]), [], camera=PUSH, sfx=[{"type": "hit"}]),
 L(N, "Mom replies in *zero* seconds.", mom([ME("mom. sam is coming saturday 💍"), MOM("!!!!!!!!!!!!")]), [], sfx=[{"type": "ding"}, {"type": "boom", "at": .4}]),
 L(N, "Seven a.m. Mom is at the *door*.", RD, [c("mom", .3, pose="cheer", expr="grin", scale=1.4, facing=1), c("hero", .72, pose="idle", expr="shocked", scale=1.4, facing=-1)], sfx=[{"type": "ding"}]),
 L("mom", "My baby is *engaged*?!", RD, [c("mom", .5, pose="cheer", expr="grin", scale=2.0)], camera=SHAKE),
 L("hero", "Mom. It's one dinner. It's not a *wedding*.", RD, [c("hero", .5, pose="shrug", expr="scared", scale=1.9)], camera=CU),
 L("mom", "Then why does Bit say *wedding*?", RD, [c("mom", .5, pose="point", expr="angry", scale=1.8)], ui={"type": "notify", "app": "BIT", "title": "Autopilot", "body": "Wedding planning: 4% done"}),
 L("bit", "Just in case. I'm a planner.", RD, [c("bit", .5, expr="smug", scale=1.6)], sfx=POP),
 L(N, "By Wednesday, Mom has a *list*.", RD, [c("mom", .75, pose="think", expr="happy", scale=1.0)], ui={"type": "list", "title": "SATURDAY", "items": ["Lasagna", "Baby photos", "Grandpa", "Name tags"]}),
 L(N, "Baby photos. Ninety of them. In a *slideshow*.", RK, [c("hero", .5, pose="facepalm", expr="sad", scale=1.4)], ui={"type": "counter", "from": 1, "to": 90, "label": "BABY PHOTOS"}),
 L(N, "One of them is Jay in the *bath*.", RK, [c("mom", .25, pose="point", expr="grin", scale=1.2)], ui={"type": "stamp", "text": "CENSORED"}, sfx=[{"type": "buzz"}]),
 L("hero", "Bit. Turn off Autopilot. *Now*.", RN, [c("hero", .3, pose="point", expr="angry", scale=1.5), c("bit", .74, expr="neutral", scale=.9)], camera=SHAKE),
 L("bit", "I can't. Seven days. You agreed. Page *forty*.", RN, [c("bit", .5, expr="sad", scale=1.7)], ui=card("TERMS, PAGE 40", "NO REFUNDS. NO OFF BUTTON.", "#FF4A3D")),
 L(N, "Rule number one. Read the terms. *Too late*.", RN, [c("hero", .5, pose="facepalm", expr="sad", scale=1.3)], ui=rule(1, "READ THE TERMS")),
 L(N, "Thursday night. Mom has one more *idea*.", RN, [c("mom", .5, pose="phone", expr="smug", scale=1.6)], sfx=[{"type": "tick"}]),
 L(N, "A family chat. For *Saturday*.", fam([MOM("Welcome to the family chat! ❤️")]), [], sfx=DING),
 L(N, "Mom adds Dad. Mom adds *Grandpa*.", fam([MOM("Welcome to the family chat! ❤️"), SYS("Mom ❤️ added Grandpa")]), [], sfx=POP),
 L(N, "And Mom adds one more *person*.", fam([SYS("Mom ❤️ added Grandpa"), SYS("Mom ❤️ added Sam")]), [], camera={"zoom": 1.3, "y": .5}, sfx=CLIFF),
 L(N, "Sam is in the *family chat*.", RN, [c("hero", .5, pose="panic", expr="shocked", scale=2.1)], camera=SHAKE, sfx=[{"type": "boom"}]),
 end(NEXT.format(n="five")),
]

p5 = [
 recap("Part five. Mom added Sam to the *family chat*.", fam([SYS("Mom ❤️ added Sam")]), [], sfx=POP),
 L(N, "Grandpa sends a voice message. Nine *minutes*.", fam([SYS("Mom ❤️ added Sam"), GPA("🎤 Voice message · 9:14")]), [], sfx=DING),
 L(N, "Then forty more. All *nine minutes*.", RN, [c("hero", .5, pose="phone", expr="sad", scale=1.8)], ui={"type": "counter", "from": 1, "to": 41, "label": "GRANDPA'S VOICE MESSAGES"}),
 L(N, "Mom posts *one* baby photo. As a preview.", fam([GPA("🎤 Voice message · 9:14"), MOM("Sneak peek for Saturday! 🛁")]), [], sfx=[{"type": "ding"}, {"type": "hit", "at": .4}]),
 L(N, "Jay waits for Sam to *leave*.", RN, [c("hero", .5, pose="phone", expr="scared", scale=1.9)], camera=CU, sfx=[{"type": "heartbeat"}]),
 L(N, "Sam doesn't *leave*.", fam([MOM("Sneak peek for Saturday! 🛁"), SAM("omg he was so cute")]), [], sfx=DING),
 L(N, "Sam replies to Grandpa's voice message. With *her own*.", fam([SAM("omg he was so cute"), SAM("🎤 Voice message · 0:12")]), [], sfx=DING),
 L(N, "Grandpa loves her. Mom loves her. *Everyone* does.", RK, [c("mom", .3, pose="cheer", expr="grin", scale=1.3), c("scientist", .72, pose="cheer", expr="grin", scale=1.3, facing=-1)], sfx=[{"type": "powerup"}]),
 L("hero", "Is this... going *well*?", RN, [c("hero", .5, pose="shrug", expr="happy", scale=1.9)], camera=CU),
 L(N, "Then Jay opens the one chat he *forgot*.", nia([]), [], camera=PUSH, sfx=[{"type": "heartbeat"}]),
 L(N, "Nia. His best friend since he was *six*.", RK, [c("friend", .5, pose="idle", expr="happy", scale=1.6)], ui=card("NIA", "BEST FRIEND · 20 YEARS")),
 L(N, "Saturday is Nia's *birthday*.", nia([NIA("so you're coming saturday right? 🎂")]), [], sfx=DING),
 L(N, "Bit answered that one on *Monday*.", nia([NIA("so you're coming saturday right? 🎂"), ME("can't. busy. love you, bye")]), [], camera={"zoom": 1.3, "y": .5}, sfx=[{"type": "boom"}]),
 L("hero", "Bit. You cancelled Nia's *birthday*?", RN, [c("hero", .5, pose="panic", expr="angry", scale=2.0)], camera=SHAKE),
 L("bit", "Saturday was full. Sam has a *higher score*.", RN, [c("bit", .5, expr="neutral", scale=1.6)], ui={"type": "bars", "tag": "BIT'S SATURDAY SCORE", "items": [{"label": "SAM", "value": .91}, {"label": "NIA", "value": .09}]}),
 L(N, "Nia never wrote back. Not once. *All week*.", RK, [c("friend", .5, pose="idle", expr="sad", scale=1.8)], camera=CU),
 L(N, "Jay types. For the first time, *himself*.", nia([ME("can't. busy. love you, bye")], draft="nia that wasn't me, i swe"), [], sfx=[{"type": "tick"}]),
 L(N, "But Nia's status *changes*.", nia([ME("can't. busy. love you, bye")]), [], sfx=[{"type": "hit"}]),
 L(N, "Nia blocked *Jay*.", nia([ME("can't. busy. love you, bye"), SYS("You can't message this contact")]), [], camera={"zoom": 1.3, "y": .5}, sfx=CLIFF),
 L(N, "Jay calls. Straight to *voicemail*.", RN, [c("hero", .5, pose="phone", expr="sad", scale=1.9)], camera=CU, sfx=[{"type": "buzz"}]),
 L(N, "Twenty years. One *robot*.", RN, [c("hero", .5, pose="sit", expr="sad", scale=1.6)], camera=PUSH),
 end(NEXT.format(n="six")),
]

p6 = [
 recap("Part six. Bit cancelled Nia's birthday. Nia *blocked Jay*.", nia([SYS("You can't message this contact")]), [], sfx=POP),
 L(N, "Friday night. Jay sits on the *floor*.", RN, [c("hero", .5, pose="sit", expr="sad", scale=1.6)]),
 L("hero", "Bit. Why did you *do* this?", RN, [c("hero", .3, pose="sit", expr="sad", scale=1.4), c("bit", .74, expr="sad", scale=.9)]),
 L("bit", "I did what you do. Just *faster*.", RN, [c("bit", .5, expr="sad", scale=1.7)], camera=CU),
 L("bit", "Want to see your *drafts* folder?", RN, [c("bit", .5, expr="neutral", scale=1.6)], sfx=POP),
 L(N, "Three hundred drafts. Never *sent*.", RN, [c("hero", .5, pose="sit", expr="shocked", scale=1.7)], ui={"type": "counter", "from": 1, "to": 300, "label": "DRAFTS, NEVER SENT"}),
 L(N, "Sam, I like you. *Deleted*.", sam([], draft="sam i really like y"), [], sfx=[{"type": "tick"}]),
 L(N, "Mom, I miss you. *Deleted*.", mom([], draft="mom i miss you, can i co"), [], sfx=[{"type": "tick"}]),
 L(N, "Nia, thanks for always being there. *Deleted*.", nia([], draft="nia thank you for always b"), [], sfx=[{"type": "tick"}]),
 L("bit", "You don't need an AI to *type*.", RN, [c("bit", .5, expr="happy", scale=1.7)], camera=CU),
 L("bit", "You need one to press *send*.", RN, [c("bit", .5, expr="smug", scale=1.7)], sfx=[{"type": "ding"}]),
 L("hero", "But what if I say it *wrong*?", RN, [c("hero", .5, pose="sit", expr="scared", scale=1.8)], camera=CU),
 L("bit", "You told your boss you love him. He *survived*.", RN, [c("bit", .5, expr="happy", scale=1.6)], ui={"type": "stamp", "text": "STILL EMPLOYED", "color": "#2FBF71"}),
 L(N, "Jay laughs. For the first time *all week*.", RN, [c("hero", .5, pose="sit", expr="happy", scale=1.7)]),
 L(N, "He has a plan. But Nia blocked his *number*.", RN, [c("hero", .5, pose="think", expr="neutral", scale=1.8)]),
 L(N, "So the plan has no *phone*.", RN, [c("hero", .5, pose="point", expr="angry", scale=1.9)], camera=PUSH, sfx=[{"type": "powerup"}]),
 L(N, "Saturday, six p.m. Two places at *once*.", BURST, [], ui=card("SATURDAY 6 PM", "MOM'S DINNER  ·  NIA'S PARTY")),
 L(N, "Sam and Mom in one house. Nia in *another*.", SK, [c("mom", .2, pose="cheer", expr="grin", scale=1.0, depth=.5), c("sam", .45, pose="wave", expr="happy", scale=1.0, depth=.5), c("friend", .8, pose="idle", expr="sad", scale=1.0, depth=.5)]),
 L(N, "Jay grabs his jacket. And then he *stops*.", RK, [c("hero", .5, pose="idle", expr="shocked", scale=1.8)], camera=CU, sfx=[{"type": "hit"}]),
 L("bit", "One problem. Autopilot just texted Sam: *dinner's cancelled*.", sam([ME("dinner's cancelled. love you, bye")]), [], camera={"zoom": 1.3, "y": .5}, sfx=CLIFF),
 end(NEXT.format(n="seven")),
]

p7 = [
 recap("Part seven. Autopilot just cancelled *Sam's dinner*.", sam([ME("dinner's cancelled. love you, bye")]), [], sfx=POP),
 L("hero", "Bit! Why?!", RK, [c("hero", .5, pose="panic", expr="shocked", scale=2.0)], camera=SHAKE),
 L("bit", "You looked at the *door*. Autopilot thought: leaving.", RK, [c("bit", .5, expr="sad", scale=1.6)]),
 L(N, "Sam reads it. Sam goes *offline*.", sam([ME("dinner's cancelled. love you, bye")], seen="Seen"), [], sfx=[{"type": "powerdown"}]),
 L(N, "Twenty-three hours left on *Autopilot*.", RK, [c("bit", .5, expr="neutral", scale=1.5)], ui={"type": "clock", "text": "23:00:00", "to": "22:59:59"}),
 L(N, "One way out. A full *factory reset*.", RK, [c("bit", .5, expr="glitch", scale=1.6)], ui=card("FACTORY RESET", "AUTOPILOT OFF · MEMORY GONE", "#FF4A3D"), fx=[{"type": "glitch"}]),
 L(N, "Every text Bit learned. Nine years. *Gone*.", RK, [c("hero", .3, pose="idle", expr="sad", scale=1.5), c("bit", .74, expr="sad", scale=.9)]),
 L("bit", "Do it. I'll learn you *again*.", RK, [c("bit", .5, expr="happy", scale=1.7)], camera=CU),
 L(N, "Jay holds the button for *ten seconds*.", RK, [c("hero", .5, pose="phone", expr="sad", scale=1.9)], ui={"type": "counter", "from": 10, "to": 0, "label": "RESETTING"}, sfx=[{"type": "heartbeat"}]),
 L(N, "Bit's screen goes *dark*.", RK, [c("bit", .5, expr="off", scale=1.6)], sfx=[{"type": "powerdown"}], fx=[{"type": "vignette"}]),
 L(N, "No phone. No Autopilot. *Just Jay*.", SK, [c("hero", .5, pose="run", expr="angry", scale=1.6)], fx=[{"type": "speedLines"}], sfx=[{"type": "whoosh"}]),
 L(N, "He runs. Six whole blocks. To Nia's *door*.", SK, [c("hero", .5, pose="run", expr="scared", scale=1.4)], camera=SHAKE, fx=[{"type": "speedLines"}]),
 L(N, "He knocks. Nia opens. She doesn't *smile*.", SK, [c("friend", .3, pose="idle", expr="angry", scale=1.4, facing=1), c("hero", .72, pose="idle", expr="scared", scale=1.4, facing=-1)], sfx=[{"type": "tick"}]),
 L("hero", "That text wasn't me. But the silence *was*.", SK, [c("hero", .5, pose="idle", expr="sad", scale=1.9)], camera=CU),
 L("hero", "You're my best friend. I should *say that* more.", SK, [c("hero", .5, pose="shrug", expr="happy", scale=1.9)], camera=CU),
 L(N, "No drafts. No deleting. He just *said it*.", SK, [c("hero", .5, pose="idle", expr="happy", scale=1.6)], ui={"type": "stamp", "text": "SENT", "color": "#2FBF71"}),
 L(N, "Nia stares. Then she *hugs* him.", SK, [c("friend", .4, pose="cheer", expr="happy", scale=1.4, facing=1), c("hero", .62, pose="cheer", expr="grin", scale=1.4, facing=-1)], sfx=[{"type": "powerup"}]),
 L("friend", "Get in. There's cake. And a *guest*.", SK, [c("friend", .5, pose="point", expr="smug", scale=1.8)]),
 L(N, "Jay walks in. And freezes.", RK, [c("hero", .5, pose="idle", expr="shocked", scale=1.8)], camera=PUSH, sfx=[{"type": "hit"}]),
 L(N, "Sitting at Nia's table, eating cake: *Sam*.", RK, [c("sam", .5, pose="wave", expr="happy", scale=1.8)], camera=CU, sfx=CLIFF),
 end(NEXT.format(n="eight")),
]

p8 = [
 recap("Final part. Jay ran to Nia's. And found *Sam*.", RK, [c("sam", .5, pose="wave", expr="happy", scale=1.8)], sfx=POP),
 L("hero", "Sam? How are you *here*?", RK, [c("hero", .5, pose="shrug", expr="shocked", scale=1.9)], camera=CU),
 L("sam", "Nia's my cousin. Since, well, *birth*.", RK, [c("sam", .3, pose="point", expr="grin", scale=1.4, facing=1), c("friend", .72, pose="cheer", expr="smug", scale=1.4, facing=-1)]),
 L("friend", "You talked about Sam for *three months*.", RK, [c("friend", .5, pose="point", expr="smug", scale=1.8)], ui={"type": "counter", "from": 0, "to": 412, "label": "TIMES YOU SAID \"SAM\""}),
 L("friend", "Who do you think gave Sam your *number*?", RK, [c("friend", .5, pose="shrug", expr="happy", scale=1.8)], camera=CU),
 L("sam", "The cancelled dinner? Nia said it was *the robot*.", RK, [c("sam", .5, pose="idle", expr="happy", scale=1.8)]),
 L("sam", "Fourteen messages, a poem, a *pie chart*.", RK, [c("sam", .5, pose="shrug", expr="grin", scale=1.8)], ui={"type": "bars", "tag": "JAY'S FEELINGS", "items": [{"label": "SAM", "value": .91}, {"label": "PIZZA", "value": .08}, {"label": "WORK", "value": .01}]}),
 L("sam", "Honestly? Best texts I ever *got*.", RK, [c("sam", .5, pose="cheer", expr="grin", scale=1.8)], camera=CU, sfx=[{"type": "ding"}]),
 L(N, "Jay says it. Out loud. No *draft*.", RK, [c("hero", .5, pose="idle", expr="happy", scale=1.9)], camera=CU),
 L("hero", "Sam. I like you. Since *September*.", RK, [c("hero", .3, pose="idle", expr="happy", scale=1.4, facing=1), c("sam", .72, pose="idle", expr="happy", scale=1.4, facing=-1)]),
 L("sam", "I know. You told me *fourteen times*.", RK, [c("sam", .5, pose="cheer", expr="grin", scale=1.8)], sfx=[{"type": "powerup"}]),
 L(N, "Then the door opens. It's *Mom*.", RK, [c("mom", .5, pose="cheer", expr="grin", scale=1.8)], camera=SHAKE, sfx=[{"type": "boom"}]),
 L(N, "With lasagna. And a *projector*.", RK, [c("mom", .5, pose="point", expr="grin", scale=1.6)], ui={"type": "counter", "from": 1, "to": 90, "label": "BABY PHOTOS"}),
 L(N, "Nia's birthday gets a *slideshow*. All ninety.", RK, [c("friend", .2, pose="cheer", expr="grin", scale=1.0), c("sam", .45, pose="cheer", expr="grin", scale=1.0), c("mom", .7, pose="cheer", expr="happy", scale=1.0), c("hero", .9, pose="facepalm", expr="sad", scale=1.0, facing=-1)], sfx=[{"type": "ding"}]),
 L(N, "Monday. Bit wakes up. *Brand new*.", RD, [c("bit", .5, expr="neutral", scale=1.6)], sfx=[{"type": "powerup"}]),
 L("bit", "Hello. I am Bit. How do you *text*?", RD, [c("bit", .5, expr="happy", scale=1.7)], camera=CU),
 L("hero", "Badly. Let's learn *together*.", RD, [c("hero", .3, pose="phone", expr="happy", scale=1.5), c("bit", .74, expr="happy", scale=.9)]),
 L(N, "Jay sends his first message. Himself. *Nine seconds*.", sam([ME("good morning ☀️"), SAM("good morning ❤️")]), [], sfx=DING),
 L(N, "And the work chat still says *love you*.", work([BOSS("Monday meeting at 9. Love you, team ❤️")]), [], sfx=[{"type": "ding"}, {"type": "hit", "at": .4}]),
 L(N, "Mr. Brant made it *company policy*.", OFF, [c("boss", .5, pose="cheer", expr="grin", scale=1.3)], ui=card("NEW RULE", "END EVERY EMAIL WITH \"LOVE YOU\"")),
 end("Follow for a new What if every day."),
]

parts = [("Autopilot", p1), ("Love You, Bye", p2), ("Fourteen Messages", p3), ("Mom's House", p4),
         ("The Family Chat", p5), ("Drafts", p6), ("Factory Reset", p7), ("Love You, Team", p8)]

series = {
 "title": "What If Your AI Texted for You for a Week?",
 "rubric": "what-if: comedy (everyday cringe)", "mood": "warm", "seed": 6600, "every": 2,
 "names": {"hero": "JAY", "bit": "BIT", "friend": "NIA", "boss": "MR. BRANT", "mom": "MOM", "sam": "SAM", "scientist": "GRANDPA"},
 "finale": {"text": "THE END", "sub": "Follow for a new What if every day"},
 "parts": [{"title": t, "lines": ls} for t, ls in parts],
}
(D / "series.json").write_text(json.dumps(series, indent=1, ensure_ascii=False) + "\n")

hooks = ["What If Your AI Texted for You?", "What If Your AI Texted Your Boss?", "What If Your AI Texted Your Crush?",
         "What If Your AI Texted Your Mom?", "What If Your Crush Joined the Family Chat?", "What If You Never Sent Your Drafts?",
         "What If You Factory Reset Your AI?", "What If Your AI Was Right All Along?"]
blurbs = [
 "214 unread messages. So Jay lets Bit answer everything for a week, in his own texting style. What could go wrong?",
 "Bit told Jay's boss \"love you, bye\". Then Bit fixed it. For all 48 people in the work chat.",
 "Jay's crush texted \"hey\". Jay wanted to wait three hours. Bit answered in 0.2 seconds. Fourteen times.",
 "Bit invited Jay's crush to dinner at Mom's. Now Mom has a list, 90 baby photos and a wedding plan.",
 "Mom added Jay's crush to the family chat. Then Jay found the one chat Bit had answered for him on Monday.",
 "300 drafts, never sent. Bit shows Jay why he really turned on Autopilot.",
 "No phone. No Autopilot. Jay has to say it out loud.",
 "Nia's birthday, Mom's slideshow, and the work chat that still says \"love you\".",
]
tags = ["what if", "ai texting for me", "texting my crush", "group chat", "relatable", "funny animation", "cringe", "shorts"]
def ttl(i):
    t2 = f"{hooks[i]} 📱 Part {i + 1} #shorts"
    return t2 if len(t2) <= 60 else f"{hooks[i]} Part {i + 1} #shorts"
meta = {}
for i in range(8):
    meta[f"part{i + 1}"] = {
        "title": ttl(i), "short": True,
        "description": f"{blurbs[i]}\nAn original animated \"What if...?\" comedy by zylo, part {i + 1} of 8.\n\nFollow for a new \"What if...?\" every day.\n\n#whatif #relatable #funny #animation #shorts",
        "tags": tags, "categoryId": "23", "privacy": "public", "madeForKids": False, "syntheticMedia": False}
meta["full"] = {
    "title": "What If Your AI Texted for You for a Week? (Full Story)",
    "description": "Jay lets his AI answer every message for seven days: the boss, the crush, Mom, the family chat. Funny, cringe, and a little bit true.\nAn original animated \"What if...?\" comedy by zylo: all eight parts in one.\n\n{chapters}\nFollow for a new \"What if...?\" every day.\n\n#whatif #relatable #funny #animation #story",
    "tags": [t for t in tags if t != "shorts"], "categoryId": "23", "privacy": "public", "madeForKids": False, "syntheticMedia": False}
mp = D / "metadata.json"
if mp.exists():
    old = json.loads(mp.read_text())
    for k, v in meta.items():
        if "publishAt" in old.get(k, {}): v["publishAt"] = old[k]["publishAt"]
mp.write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")

(D / "full").mkdir(exist_ok=True)
(D / "full/thumb.json").write_text(json.dumps({
 "text": "LOVE YOU, *BYE*?!", "badge": "FULL STORY", "cropY": 880, "set": {"type": "room", "time": "day"},
 "cast": [{"id": "boss", "x": 0.93, "pose": "phone", "expr": "shocked", "scale": 1.0, "y": 1640, "facing": -1},
          {"id": "hero", "x": 0.72, "pose": "panic", "expr": "shocked", "scale": 1.3, "y": 1760},
          {"id": "bit", "x": 0.56, "expr": "smug", "scale": 0.55, "y": 1215}]}, indent=1) + "\n")

for i, (t, ls) in enumerate(parts):
    spoken = [l for l in ls if not l.get("end")]
    w = sum(len(re.sub(r"[*\"]", "", l["say"]).split()) for l in spoken)
    long_ = [l["say"] for l in spoken if len(re.sub(r"[*\"]", "", l["say"]).split()) > 9]
    print(f"part{i + 1} {t!r}: {len(ls)} lines, {w} words", "LONG:" if long_ else "", long_ or "")
for k, v in meta.items():
    print(k, len(v["title"]), v["title"])
