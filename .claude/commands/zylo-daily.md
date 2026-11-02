---
description: Fully automatic day — read the stats, every 2nd day invent a new ~7-minute "What if...?" series (8 parts), render, schedule, upload what is due, log, push
---

# /zylo-daily

Runs unattended once a day (scheduled task) in the standing session "zylo producer (daily)". Only ONE session runs this per day — never start it in a second session in parallel (on 2026-11-01 that uploaded 3 duplicates). `publish_series.py upload` also skips titles already on the channel. Nobody reviews the result before it goes out, so do the QC yourself
and never skip it. Follow CLAUDE.md and `/zylo-story` (story, line and shot rules). Report to the owner in Russian.

## 0. Workspace
```bash
git fetch origin claude/magical-newton-hmla9z && git checkout claude/magical-newton-hmla9z && git pull --ff-only origin claude/magical-newton-hmla9z
bash scripts/setup.sh
python3 scripts/youtube_upload.py --check     # must print "expected": true, else stop and report
.venv/bin/python scripts/publish_series.py status
```

## 0b. Format and rhythm (the owner's choice)
- Every story is **~7 minutes, told in detail**: 8 parts of ~55–70 s (130–160 spoken words, 20–24 lines each).
  Parts go out **every 2 days**; the full story (16:9, chapters) the day after the last part.
- A **new series starts every 2 days**: if any series' part 1 goes out today or went out yesterday (see
  `publish_series.py status` / metadata `publishAt` of part 1s — this includes backlog/owner-scheduled series), today
  is an **upload day** — skip step 1a–2 for a new series and instead
  (a) run the stats, (b) upload what is due, (c) if time allows, write the next backlog story (below).
  9 uploads per series every 2 days ≈ 4.5 uploads/day, inside YouTube's default quota (~6/day).
- **Backlog** (`episodes/<date>-what-if-<slug>/` with `"startOn"` in series.json, already scheduled): holiday
  specials prepared ahead (e.g. `2026-11-01-what-if-ai-santa`, Christmas). They publish on their own dates via
  `upload`; leave them alone except to fix problems. When a holiday is 3–6 weeks away and nothing is prepared,
  an upload day is a good day to write one (same rules, `"startOn"`, then `publish_series.py schedule … --start <startOn>`).

- **Split-screen Shorts** (owner's choice, 2026-11-02): every part is rendered with the story in the top half and
  an original code-drawn satisfying loop in the bottom half (`templates/zylo-shared/toon/Satisfying.tsx`: press /
  sand / marbles, rotating per part — make_series does it automatically). **Preferred:** real satisfying stock
  footage from Pexels/Pixabay (licence allows monetised YouTube use) via `scripts/broll.py`, used automatically by
  make_story when `PEXELS_API_KEY` or `PIXABAY_API_KEY` is set; commit `brand/broll_used.txt` and each part's
  `broll.json` (clip sources). Never use other creators' footage
  (press videos, Minecraft parkour, Subway Surfers…) — that is reused content and gets the channel demonetised. When
  looking at frames, check the top half too: heads, captions and UI must sit inside it. The 16:9 full story is not split.

## 1. Read the audience (every day, before choosing anything)
```bash
.venv/bin/python scripts/channel_stats.py     # -> stats/<date>.md + stats/latest.md (commit them)
```
Read the report and the previous days' reports (`stats/*.md`). It compares every public video age-fairly
(views/day over the first week vs the median of its group), flags **HIT** (≥ 2× median) and **FLOP** (≤ 0.4×),
ranks series and themes, shows how many part-1 viewers come back for later parts, and lists **promised seasons
still owed**. Write 3–5 lines of conclusions at the top of today's `research.md`: what the audience clearly likes
(topic, hook style, characters, title wording), what to stop doing.

## 1a. Decide what today's series is — in this order
1. **A promise is due → keep it.** If a series promised a next season (finale "SEASON 2?", last line "Follow for
   season two" …) and its last part has aired, today's series is that sequel. Several owed → the best performer
   first; never leave a promise unkept more than 5 days after its finale.
2. **A HIT → more of it.** If a recent video/series is a HIT and nothing followed up on it in the last 3 days, make
   its sequel (if the story allows) or a new premise in the same theme/angle that made it work.
3. **Otherwise → today's best trend** (below), steered by the theme ranking (more of the top themes, fewer flops).
Keep a mix: at most 3 days in a row on one theme, so the channel keeps testing new ideas.

**Sequels**: `series.json` gets `"sequelOf": "<slug of season 1>"`, `"season": 2`, same cast/world/names; part 1
opens with a one-line recap ("Last season: …") and pays off the cliffhanger. Titles "… Season 2 · Part 1 #shorts".
**Promises are obligations**: only end a series with a next-season tease (finale "SEASON 2?" / "follow for season
two") when its theme is at or above the median in the stats or it is itself a sequel of a HIT; otherwise end with
a closed twist and "Follow for a new What if every day."

## 1b. Pick a trending topic yourself (when 1a says trend)
1. **What is hot right now.** Run several WebSearch queries in one go (use `extended` mode for at least one):
   today's viral/trending topics and memes, what's trending on YouTube Shorts / TikTok this week, upcoming holidays
   and events in the next 2–3 weeks (a series runs ~16 days), big tech/AI/science/pop-culture news, new movie/game
   releases people are talking about. Note 5–8 candidate hooks with why each is hot (link + date).
2. **What works on our channel.** `python3 scripts/youtube_upload.py --stats --days 14` — which themes, hooks and
   titles got the most views; lean toward what wins, drop what flops.
3. **Choose** the candidate that is (a) trending now or tied to an upcoming date, (b) turns into a strong
   "What if...?" with a twist, (c) never used in `log.md` / `episodes/*/series.json`, (d) a different theme from
   yesterday (disaster/survival · money/power · AI/Bit gone weird · sci-fi twist · everyday-life absurd · holiday/event).
   Fiction only: never real people, brands, logos or events presented as real; riff on the *idea* of the trend
   (e.g. "what if a new phone update…", not a named company). Skip tragedies, politics, and anything that would
   exploit a real disaster.
4. Write the reasoning to `episodes/<slug>/research.md` (audience conclusions, candidates, links, stats you used,
   why this one won — or which promise/hit it follows up).
## 1c. Write the series
- Titles/tags/hashtags use the words people are searching for this trend (from your research).
- `episodes/<YYYY-MM-DD>-what-if-<slug>/series.json`: **8 parts** (~55–70 s, 130–160 words, 20–24 lines ≤ 9 words
  each). Tell it **in detail**, not as a summary: set the scene, show why characters act (motive, fear, wish), let
  dialogue carry the story, give every part a real development + its own cliffhanger. Across the 8 parts: setup and
  the rule of the world (1–2), escalation and a running joke (2–4), a big loss/turn (4–5), the emotional reason under
  it all (6), climax with a cost (7), payoff and a final twist (8). Parts 2+ open with a recap line marked
  `"shortOnly": true` ("Part two. <recap>") — it is cut from the full story so the 7-minute version plays straight.
  Reference: `episodes/2026-11-01-what-if-ai-santa/` (series built by its `build_series.py`).
- Vary sets, cast, poses, UI and sfx from the last series. A new location may need a new set in
  `templates/zylo-shared/toon/Backgrounds.tsx` (see `casino`) or new looks in `Character.tsx` (see `heroSuit`).
- Any real-world fact in the story must be verified by WebSearch first and saved with quotes in `sources.md`;
  cut anything disputed.
- `metadata.json`: `part1..part8` (title ≤ 60 chars incl. " #shorts", starts "What If", 2-line description + CTA +
  4–5 hashtags, `short: true`) and `full` (title "... (Full Story)", no #shorts, description containing the literal
  `{chapters}` line, which is filled in at upload). `categoryId "1"`, `madeForKids false`, `syntheticMedia false`.
- `full/thumb.json`: ToonThumb props — ≤ 5 words with one `*accent*` word, a set, 2–3 big expressive characters on
  the right (see `episodes/2026-10-31-what-if-casino-boss/full/thumb.json`).

## 2. Build and look
```bash
.venv/bin/python scripts/make_series.py episodes/<slug>        # parts + vertical full cut
.venv/bin/python scripts/make_wide.py episodes/<slug>          # 16:9 full story + thumbnail + chapters.txt
```
Make a contact sheet per part (12 frames) and Read it; Read `full/out/thumb.png` and one frame of
`full/out/wide.mp4`. Fix anything unreadable, cropped, overlapping or off-model and re-run from `--from props`.

## 3. Schedule + upload
```bash
.venv/bin/python scripts/publish_series.py schedule episodes/<slug> --start <today YYYY-MM-DD>
.venv/bin/python scripts/publish_series.py upload
```
`schedule` puts a part every 2 days at a free slot; `upload` (every day, also on upload days) takes everything due in
the next 3 days across all series, oldest first, re-renders whatever is missing (renders don't survive between
sessions), publishes immediately when a slot already passed, writes `uploads.json` + `log.md`, and stops cleanly at
the quota — tomorrow's run continues.

## 4. Save
Commit (`stats/`, `episodes/<slug>`, `uploads.json`s, `log.md`, any template changes) and push to
`claude/magical-newton-hmla9z`. Finish with a short Russian summary: what the stats showed (hits/flops), why today's topic, premise, links + publish times, anything left
for tomorrow.
