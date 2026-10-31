---
description: Write, animate, QC and publish today's zylo "What if...?" animated story Short
---

# /zylo-story

Make today's zylo Short: an original, fictional **"What if...?"** story, animated in the code-drawn 2D
style (`templates/zylo-toon`). Follow CLAUDE.md. Ask only when blocked by accounts, keys or payment.
`$ARGUMENTS` may force a premise or theme.

## 1. Premise
- Rotate themes (check `log.md`, never two days running): disaster/survival (meteor, zombies, blackout,
  flood, aliens) · money (a billion in 30 days, the last dollar on Earth) · AI/Claude-style assistant gone weird
  (our AI is **Bit**, never another company's mascot) · science-fiction twists (gravity off, time loop).
- Check trends with WebSearch (holidays, news, viral topics) and lean the premise into one when it fits.
- Never repeat a premise from `log.md`. Fiction is fine; don't present invented events as real news about real
  people, places or companies.

## 2. Format: one story, several parts
Write ONE long story (2.5–4 min) as a series: `episodes/<YYYY-MM-DD>-what-if-<slug>/series.json`
(`parts[]`, each with `title` and `lines`, plus `finale`). Each part is a 45–60 s Short with its own arc:
- part 1 opens with the "What if...?" hook; parts 2+ open with "Part two. <one-line recap>";
- every part ends on a cliffhanger line, then its closing line (`"end": true`);
- the story needs real turns: a rule of the world, a cost, a betrayal or sacrifice, a twist, one running joke.
Build with `scripts/make_series.py episodes/<slug>`: part<N>/out/short.mp4 (badge "PART N/total") and
full/out/short.mp4 (chapter cards, only the final closing line). Publish one part per day; the full cut goes
out as the Sunday long video. Put titles/descriptions for every part and the full cut in `metadata.json`.
Every shot should carry sound: add `sfx` (whoosh boom hit alarm siren buzz ring ding pop riser glitch growl
crash heartbeat engine tick powerdown powerup knock) on hits, reveals, phones, transitions.

## 2b. Line and shot rules
- 85–130 spoken words, 35–60 s. Line 1 = the "What if...?" hook (≤ 9 words). Escalate every 2–3 lines,
  one comic beat in the middle, a twist near the end, cliffhanger, last line `{"speaker":"narrator",
  "say":"Follow for part two.","end":true}` (vary the wording).
- Mix narrator lines with dialogue (`hero` = Jay, `bit` = Bit, plus `friend`, `boss`, `scientist`, `kid`,
  `soldier`, `zombie`). Lines ≤ 9 words so every shot is 1.2–3 s. Mark 1–2 key words per line with *asterisks*.
- Each line gets a `shot`: `set` (room | street | sky | space | news | store | wasteland | lab | burst; `time`
  day|dusk|night; `damage` 0–2; news `headline`; burst `color`), `cast` (id, x 0–1, pose, expr, scale,
  depth, facing, enter left|right|pop, moveTo, icon for Bit), optional `fx` (meteor, impact, moneyRain, rain,
  snow, alarm, glitch, ufo, speedLines, vignette), `ui` (clock, notify, stamp, list, bars, map, card, counter),
  `camera` (zoom, x, y, push, shake), `transition` (cut | flash | whip).
- Poses: idle point shrug panic wave phone cheer think zombie run walk facepalm sit.
  Expressions: neutral happy grin shocked scared angry sad smug sleepy (Bit: neutral happy shocked angry sad think glitch smug).
- Vary sets, framing and transitions from the last episodes; the speaking character should usually be in frame.

## 3. Build
```bash
.venv/bin/python scripts/make_story.py episodes/<slug>
```

## 4. Look at it
Extract frames at 0.8 s, every shot change and the end; Read them. Check the hook is legible on frame 0,
captions sit inside the frame, the speaker is visible, nothing overlaps badly. Fix `story.json` and re-run
`--from props` (visual) or from `tts` (text changes).

## 5. Metadata, upload, log
As in `/zylo-short` steps 6–8: title ≤ 60 chars with " #shorts" (starts "What If..."), description 2 lines +
CTA + 4–5 hashtags, `syntheticMedia: false` (stylised cartoon, no realistic people). Upload with
`scripts/youtube_upload.py`, append to `log.md`, commit and push.
