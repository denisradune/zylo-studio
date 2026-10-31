---
description: Fully automatic day — invent a new "What if...?" series, render it, schedule every part + the full story, upload, log, push
---

# /zylo-daily

Runs unattended once a day (scheduled task). Nobody reviews the result before it goes out, so do the QC yourself
and never skip it. Follow CLAUDE.md and `/zylo-story` (story, line and shot rules). Report to the owner in Russian.

## 0. Workspace
```bash
git fetch origin claude/magical-newton-hmla9z && git checkout claude/magical-newton-hmla9z && git pull --ff-only origin claude/magical-newton-hmla9z
bash scripts/setup.sh
python3 scripts/youtube_upload.py --check     # must print "expected": true, else stop and report
.venv/bin/python scripts/publish_series.py status
```

## 1. New series (one per day)
- Premise: a fresh "What if...?" never used in `log.md` / `episodes/*/series.json`; rotate themes so two days running
  never share one (disaster/survival · money/power · AI/Bit gone weird · sci-fi twist · everyday-life absurd).
  Check WebSearch for today's trends/holidays and lean in when it fits. Fiction only; no real people/companies.
- `episodes/<YYYY-MM-DD>-what-if-<slug>/series.json`: **4 parts** (45–60 s each, own arc, cliffhanger, parts 2+ open
  with "Part two. <recap>"), one running joke, a rule of the world, a cost, a twist; `finale` card on the last part.
  4 parts + 1 full = 5 uploads/day, which fits YouTube's default quota (~6 uploads/day). If the quota is ever
  raised, more parts per series are fine.
- Vary sets, cast, poses, UI and sfx from the last series. A new location may need a new set in
  `templates/zylo-shared/toon/Backgrounds.tsx` (see `casino`) or new looks in `Character.tsx` (see `heroSuit`).
- Any real-world fact in the story must be verified by WebSearch first and saved with quotes in `sources.md`;
  cut anything disputed.
- `metadata.json`: `part1..part4` (title ≤ 60 chars incl. " #shorts", starts "What If", 2-line description + CTA +
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
`upload` handles every series still pending (oldest first, re-rendering missing files), publishes immediately when a
slot already passed, writes `uploads.json` + `log.md`, and stops cleanly at the quota — tomorrow's run continues.

## 4. Save
Commit (`episodes/<slug>`, `uploads.json`s, `log.md`, any template changes) and push to
`claude/magical-newton-hmla9z`. Finish with a short Russian summary: premise, links + publish times, anything left
for tomorrow.
