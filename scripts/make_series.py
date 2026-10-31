#!/usr/bin/env python3
"""
One long "What if...?" story -> N Shorts parts + one full-length video.

  scripts/make_series.py episodes/2026-10-31-what-if-zombies            # all parts, then the full cut
  scripts/make_series.py episodes/... --parts 2 --from props           # just part 2, from a stage
  scripts/make_series.py episodes/... --full-only

series.json:
{
  "title": "...", "mood": "tension", "seed": 31, "names": {...},
  "parts": [
    {"title": "The Notification", "lines": [ ...story lines..., {"speaker": "narrator", "say": "...", "end": true}]},
    {"title": "Turn Me Off", "lines": [ {"speaker": "narrator", "say": "Part two. <recap>", ...}, ..., end line ]},
    ...
  ],
  "finale": {"text": "SEASON 2?", "sub": "Follow for what's in the cloud"}
}
A line with "shortOnly": true (the "Part two. <recap>" openers) is left out of the full cut.
Each part becomes episodes/<slug>/part<N>/ (story.json -> out/short.mp4, badge "PART N/total").
The full cut (episodes/<slug>/full/) drops every part's closing line except the last and puts a chapter
card where each later part begins.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = str(ROOT / '.venv/bin/python')


def build(d: Path, story: dict, start: str | None) -> None:
    d.mkdir(parents=True, exist_ok=True)
    (d / 'story.json').write_text(json.dumps(story, indent=1))
    cmd = [PY, str(ROOT / 'scripts/make_story.py'), str(d)]
    if start:
        cmd += ['--from', start]
    print(f'\n##### {d.name} #####', flush=True)
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('series_dir')
    ap.add_argument('--parts', help='comma-separated part numbers (default: all)')
    ap.add_argument('--full-only', action='store_true')
    ap.add_argument('--no-full', action='store_true')
    ap.add_argument('--from', dest='start')
    a = ap.parse_args()
    root = Path(a.series_dir).resolve()
    s = json.loads((root / 'series.json').read_text())
    parts = s['parts']
    n = len(parts)
    base = {k: s[k] for k in ('mood', 'names') if k in s}

    if not a.full_only:
        wanted = [int(x) for x in a.parts.split(',')] if a.parts else range(1, n + 1)
        for i in wanted:
            p = parts[i - 1]
            last = i == n
            story = {
                **base,
                'title': f"{s['title']} (Part {i})",
                'seed': s.get('seed', 1) + i,
                'partLabel': f'PART {i}/{n}',
                'end': s.get('finale') if last else {'text': f'PART {i + 1}', 'sub': 'Follow — it drops tomorrow' if s.get('every', 2) == 1 else f"Follow — it drops in {s.get('every', 2)} days"},
                'lines': p['lines'],
                'minSeconds': 35,
                'maxSeconds': 90,
            }
            build(root / f'part{i}', story, a.start)

    if not a.no_full:
        lines, chapters = [], []
        for i, p in enumerate(parts, 1):
            body = p['lines'] if i == n else p['lines'][:-1]
            # "Part two. Last time…" recaps only make sense in the Shorts; the full story plays straight through.
            body = [l for l in body if not l.get('shortOnly')]
            if i > 1:
                chapters.append({'line': len(lines), 'label': f'PART {i}', 'title': p['title']})
            lines += body
        story = {
            **base,
            'title': s['title'],
            'seed': s.get('seed', 1),
            'end': s.get('finale'),
            'lines': lines,
            'chapters': chapters,
            'minSeconds': 90,
            'maxSeconds': 600,
        }
        build(root / 'full', story, a.start)


if __name__ == '__main__':
    main()
