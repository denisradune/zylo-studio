#!/usr/bin/env python3
"""
Schedule and upload "What if...?" series without anyone touching them.

  scripts/publish_series.py schedule episodes/<slug> --start 2026-11-01      # slot picked from the date
  scripts/publish_series.py upload                                          # everything not uploaded yet, all series
  scripts/publish_series.py upload episodes/<slug> --max 3
  scripts/publish_series.py status

Schedule (Asia/Jerusalem): part i goes out on start + (i-1) days at the series' slot; the full story
(16:9, regular video) the day after the last part at FULL_AT. With 4-part series started every day the
slots never collide: the slot rotates with the date through SLOTS.

State lives in git so a fresh session can continue: episodes/<slug>/uploads.json {key: {id, url, publishAt}}.
`upload` renders whatever is missing (make_series / make_wide), fills {chapters} in the full description,
publishes immediately when a scheduled time has already passed, appends a log.md row, and stops cleanly
when the YouTube daily quota (10,000 units ~ 6 uploads) runs out — the next run picks up the rest.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import youtube_upload as yu  # noqa: E402

TZ = ZoneInfo('Asia/Jerusalem')
SLOTS = ['13:00', '15:00', '17:00', '19:00']
FULL_AT = '21:00'
PY = str(ROOT / '.venv/bin/python')


def slot_for(day: dt.date) -> str:
    # 2026-11-01 -> 13:00, then 15:00, 17:00, 19:00, 13:00 ...
    return SLOTS[(day - dt.date(2026, 11, 1)).days % len(SLOTS)]


def at(day: dt.date, hhmm: str) -> str:
    h, m = map(int, hhmm.split(':'))
    return dt.datetime(day.year, day.month, day.day, h, m, tzinfo=TZ).astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def load(p: Path, default):
    return json.loads(p.read_text()) if p.exists() else default


def part_keys(meta: dict) -> list[str]:
    return sorted((k for k in meta if k.startswith('part')), key=lambda k: int(k[4:]))


def schedule(d: Path, start: dt.date, slot: str | None) -> None:
    meta = json.loads((d / 'metadata.json').read_text())
    slot = slot or slot_for(start)
    keys = part_keys(meta)
    for i, k in enumerate(keys):
        meta[k]['publishAt'] = at(start + dt.timedelta(days=i), slot)
    if 'full' in meta:
        meta['full']['publishAt'] = at(start + dt.timedelta(days=len(keys)), FULL_AT)
    (d / 'metadata.json').write_text(json.dumps(meta, indent=1, ensure_ascii=False) + '\n')
    for k in keys + (['full'] if 'full' in meta else []):
        print(k, meta[k]['publishAt'])


def video_for(d: Path, key: str) -> tuple[Path, Path | None]:
    if key == 'full':
        return d / 'full/out/wide.mp4', d / 'full/out/thumb.png'
    return d / key / 'out/short.mp4', None


def ensure_rendered(d: Path, key: str) -> None:
    video, _ = video_for(d, key)
    if video.exists():
        return
    if key == 'full':
        if not (d / 'full/out/short.mp4').exists():
            subprocess.run([PY, str(ROOT / 'scripts/make_series.py'), str(d), '--full-only'], check=True)
        subprocess.run([PY, str(ROOT / 'scripts/make_wide.py'), str(d)], check=True)
    else:
        subprocess.run([PY, str(ROOT / 'scripts/make_series.py'), str(d), '--parts', key[4:], '--no-full'], check=True)


def log_row(d: Path, meta: dict, key: str, res: dict) -> None:
    log = ROOT / 'log.md'
    rows = [l for l in log.read_text().splitlines() if l.startswith('| ') and l[2:3].isdigit()]
    n = len(rows) + 1
    m = meta[key]
    when = (m.get('publishAt') or dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%MZ'))[:10]
    series = load(d / 'series.json', {})
    rubric = series.get('rubric', 'what-if')
    label = f'{rubric} ({key})'
    src = 'sources.md' if (d / 'sources.md').exists() else 'original fiction'
    with log.open('a') as f:
        f.write(f"| {n} | {when} | {m['title']} | {label} | {src} | {res['url']} |\n")


def upload(dirs: list[Path], max_n: int | None) -> int:
    items = []
    now = dt.datetime.now(dt.timezone.utc)
    for d in dirs:
        meta = load(d / 'metadata.json', {})
        done = load(d / 'uploads.json', {})
        for k in part_keys(meta) + (['full'] if 'full' in meta else []):
            if k not in done and meta[k].get('publishAt'):
                items.append((meta[k]['publishAt'], d, k))
    items.sort()
    count = 0
    for publish_at, d, k in items:
        if max_n is not None and count >= max_n:
            break
        meta = json.loads((d / 'metadata.json').read_text())
        m = dict(meta[k])
        if dt.datetime.fromisoformat(publish_at.replace('Z', '+00:00')) < now + dt.timedelta(minutes=20):
            m['publishAt'] = None  # its slot has passed: go public right away
        if '{chapters}' in m['description']:
            ch = d / 'full/chapters.txt'
            ensure_rendered(d, k)
            m['description'] = m['description'].replace('{chapters}', ch.read_text() if ch.exists() else '')
        ensure_rendered(d, k)
        video, thumb = video_for(d, k)
        print(f'uploading {d.name}/{k} -> {m.get("publishAt") or "now"}', flush=True)
        try:
            res = yu.upload(video, m, thumb if thumb and thumb.exists() else None)
        except Exception as e:  # noqa: BLE001
            if any(s in str(e).lower() for s in ('quota', 'uploadlimit')):
                print(f'YouTube daily quota used up; {len(items) - count} item(s) left for the next run')
                return count
            raise
        done = load(d / 'uploads.json', {})
        done[k] = {'id': res['id'], 'url': res['url'], 'publishAt': m.get('publishAt')}
        (d / 'uploads.json').write_text(json.dumps(done, indent=1) + '\n')
        log_row(d, meta, k, res)
        print(json.dumps(res), flush=True)
        count += 1
    return count


def series_dirs() -> list[Path]:
    return sorted(p.parent for p in (ROOT / 'episodes').glob('*/series.json'))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('schedule')
    s.add_argument('series_dir')
    s.add_argument('--start', required=True)
    s.add_argument('--slot')
    u = sub.add_parser('upload')
    u.add_argument('series_dir', nargs='*')
    u.add_argument('--max', type=int)
    sub.add_parser('status')
    a = ap.parse_args()
    yu.load_env()
    if a.cmd == 'schedule':
        schedule(Path(a.series_dir).resolve(), dt.date.fromisoformat(a.start), a.slot)
    elif a.cmd == 'upload':
        dirs = [Path(x).resolve() for x in a.series_dir] or series_dirs()
        print(f'{upload(dirs, a.max)} uploaded')
    else:
        for d in series_dirs():
            meta = load(d / 'metadata.json', {})
            done = load(d / 'uploads.json', {})
            for k in part_keys(meta) + (['full'] if 'full' in meta else []):
                print(f"{d.name:40} {k:6} {meta[k].get('publishAt') or '-':22} {done.get(k, {}).get('url', 'pending')}")


if __name__ == '__main__':
    main()
