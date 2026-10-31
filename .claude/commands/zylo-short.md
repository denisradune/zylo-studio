---
description: Research, produce, QC and publish today's zylo Short end to end
---

# /zylo-short

Produce and publish today's Short for zylo. Follow CLAUDE.md. Work without asking unless blocked
by accounts, keys or payment. Arguments (optional): `$ARGUMENTS` — a topic or rubric to force.

## 0. Prep
- If `.venv`, `.models` or `templates/node_modules` is missing: `bash scripts/setup.sh`.
- Date = today in Asia/Jerusalem. Read `log.md`: last rubric used, all past topics.

## 1. Topic
- Next rubric in rotation (1→2→3→4→1), unless `$ARGUMENTS` says otherwise.
- WebSearch (standard; several queries in one turn) for what is trending today: holidays/observances,
  news, viral science/tech/history stories. Pick a topic inside the rubric with a strong "wait, really?" core.
- Reject anything already in `log.md` (same subject, not just same title).

## 2. Verify facts
- WebSearch every claim you plan to use; prefer primary sources (papers, agencies, museums, filings).
- Write `episodes/<YYYY-MM-DD>-<slug>/sources.md`: each source with URL and the quoted fact it supports.
- Drop any claim you could not confirm.

## 3. Script → episode.json
- 95–120 words incl. CTA; hook 0–3 s, promise 3–15 s, one idea with facts 15–40 s, CTA last.
- Lines of 5–8 words; each line is one **beat** (a cut every 2–3 s). Per line set:
  `section` (0..3, one progress segment per story block), `theme` (`dark`/`light`, alternate blocks),
  `headline` (2–5 words, accent words in *asterisks*; repeat it on consecutive lines to hold it),
  first line `headlineStyle: "hook"`, and one `hero`:
  `image` (full-bleed, `prompt`, `motion`), `card` (`prompt`, `title`, `badge`, `url` of the source domain),
  `source` (`url`, paper `title`, `meta`), `tile` (`value` ≤ 5 chars, `label`), `counter` (`value`, `label`, `sub`),
  `phones` (`prompts`×3 or `srcs`, optional `labels`), `filmstrip` (`prompts`), `checklist` (`items`),
  `chart` (`points`, `label`, `highlight`), `compare` (`left`/`right`). Optional `chips`, `wave`.
  Last line: `{"say": "Follow for one fact a day that changes how you see the world.", "cta": true}`.
  Vary hero types and order between episodes; show a `source` or `url` card for the key fact.
  Image prompts: concrete subject, no realistic people, no fake real-world events.
- Pick `mood` (mystery|wonder|tension|tech|space|warm) and a new `seed`.
- Also write `title` in episode.json.

## 4. Build
```bash
.venv/bin/python scripts/make_short.py episodes/<slug>
```
If QC fails (duration outside 35–50 s → adjust words; caption overflow → shorten long words/lines), fix and
re-run from the right stage with `--from`.

## 5. Look at it
Read `out/frames/*.jpg` yourself (0.8 s hook, middle, 30 s). Check: hook legible, captions inside frame and on
the right word, visual matches the line, nothing blank. Also extract 2–3 more frames at cut points if in doubt.
Fix and re-render if anything is off.

## 6. Metadata → `episodes/<slug>/metadata.json`
```json
{"title": "<= 60 chars incl. #shorts, keyword early", "short": true,
 "description": "Line 1 with keyword.\nLine 2.\n\nFollow for one fact a day that changes how you see the world.\n\n#shorts #facts #science #...",
 "tags": ["..."], "categoryId": "28", "privacy": "public", "madeForKids": false, "syntheticMedia": false}
```
Set `publishAt` to today 17:00 Asia/Jerusalem in UTC if it is still before that time; otherwise publish now.

## 7. Upload
```bash
.venv/bin/python scripts/youtube_upload.py --video episodes/<slug>/out/short.mp4 --meta episodes/<slug>/metadata.json
```
If credentials are missing, stop here and report (the video stays ready to upload).

## 8. Log and save
- Append to `log.md`: `| N | date | title | rubric | sources (short) | link |`.
- `git add -A && git commit -m "Short #N: <title>" && git push` (media is gitignored; episode.json,
  sources.md, metadata.json, props.json are kept).
- Report: title, link, duration, the three frames.
