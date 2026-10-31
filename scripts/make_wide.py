#!/usr/bin/env python3
"""
The full cut of a series as a regular (non-Shorts) 16:9 YouTube video, plus its thumbnail.

  scripts/make_wide.py episodes/2026-10-31-what-if-zombies

Needs episodes/<slug>/full/out/short.mp4 (from make_series.py) and full/props.json.
Writes:
  full/out/wide.mp4      1920x1080: the vertical cut centred, blurred copy behind, title + chapter list
  full/out/thumb.png     1280x720 cartoon thumbnail from full/thumb.json (ToonThumb props), if present
  full/chapters.txt      YouTube chapter lines ("0:00 Part 1 · The Notification") for the description
A 16:9 frame keeps YouTube from filing the full story under Shorts.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TPL = ROOT / 'templates'


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print('+', ' '.join(cmd), flush=True)
    subprocess.run(cmd, check=True, cwd=cwd)


def stamp(sec: float) -> str:
    s = int(sec)
    return f'{s // 60}:{s % 60:02d}'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('series_dir')
    ap.add_argument('--thumb-only', action='store_true')
    a = ap.parse_args()
    root = Path(a.series_dir).resolve()
    full = root / 'full'
    series = json.loads((root / 'series.json').read_text())
    out = full / 'out'
    out.mkdir(parents=True, exist_ok=True)

    thumb = full / 'thumb.json'
    if thumb.exists():
        run(['npx', 'remotion', 'still', 'zylo-toon/src/index.ts', 'ToonThumb', str(out / 'thumb.png'), f'--props={thumb}', '--log=error'], cwd=TPL)
    if a.thumb_only:
        return

    props = json.loads((full / 'props.json').read_text())
    parts = series['parts']
    chapters = [{'start': 0, 'label': 'PART 1', 'title': parts[0]['title']}] + props.get('chapters', [])
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(out / 'short.mp4')],
                               capture_output=True, text=True, check=True).stdout)

    pub = full / 'wide-public'
    pub.mkdir(exist_ok=True)
    shutil.copy(out / 'short.mp4', pub / 'full.mp4')
    wprops = {'video': 'full.mp4', 'durationSeconds': round(dur, 3), 'title': series['title'], 'chapters': chapters}
    (full / 'wide-props.json').write_text(json.dumps(wprops, indent=1))
    run(['npx', 'remotion', 'render', 'zylo-toon/src/index.ts', 'ToonWide', str(out / 'wide.mp4'), f'--props={full / "wide-props.json"}',
         f'--public-dir={pub}', '--codec=h264', '--crf=18', '--audio-bitrate=192k', '--log=error'], cwd=TPL)
    shutil.rmtree(pub)

    lines = [f"{stamp(c['start'])} {c['label'].title()} · {c['title']}" for c in chapters]
    (full / 'chapters.txt').write_text('\n'.join(lines) + '\n')
    print('\n'.join(lines))
    print(json.dumps({'wide': str(out / 'wide.mp4'), 'seconds': round(dur, 2)}))


if __name__ == '__main__':
    main()
