#!/usr/bin/env python3
"""
Real "satisfying" footage for the bottom half of split-screen Shorts, from free stock libraries whose licence allows
use in monetised YouTube videos (Pexels, Pixabay). Never clips ripped from other creators.

  scripts/broll.py --out episodes/<slug>/part3/public/broll.mp4 --seconds 62 --seed 7

Needs PEXELS_API_KEY (preferred) or PIXABAY_API_KEY in the environment / .env. Picks clips for a few satisfying
queries, skips clips already used on the channel (brand/broll_used.txt), cuts ~4–7 s from each, crops them to
1080x960, mutes them and concatenates to exactly --seconds. Writes <out>.json with every clip's source URL and
author for the record. Exit code 3 = no key / nothing found (the caller falls back to the drawn loop).
"""
from __future__ import annotations

import argparse
import json
import os
import random
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
USED = ROOT / 'brand/broll_used.txt'
W, H = 1080, 960

QUERIES = [
    'hydraulic press', 'kinetic sand cutting', 'slime', 'soap cutting', 'paint mixing', 'pouring paint',
    'cake decorating', 'pottery wheel', 'satisfying', 'glass blowing', 'chocolate pouring', 'ice cutting',
    'sand art', 'laser cutting', 'honey dripping', 'ink in water', 'woodturning lathe', 'frosting cake',
    'cnc machine', 'dominoes falling', 'pressure washing', 'carving wood', 'cutting fruit', 'molten metal',
]


def load_env() -> None:
    env = ROOT / '.env'
    if env.exists():
        for line in env.read_text().splitlines():
            if '=' in line and not line.lstrip().startswith('#'):
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def get(url: str, headers: dict | None = None) -> dict:
    req = urllib.request.Request(url, headers={'User-Agent': 'zylo-studio/1.0', **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def pexels(query: str, key: str) -> list[dict]:
    q = urllib.parse.urlencode({'query': query, 'per_page': 30, 'size': 'medium'})
    data = get(f'https://api.pexels.com/videos/search?{q}', {'Authorization': key})
    out = []
    for v in data.get('videos', []):
        files = [f for f in v.get('video_files', []) if f.get('file_type') == 'video/mp4' and (f.get('height') or 0) >= 720]
        if not files or v.get('duration', 0) < 6:
            continue
        f = min(files, key=lambda f: abs((f.get('height') or 0) - 1080))
        out.append({'id': f"pexels-{v['id']}", 'url': f['link'], 'page': v.get('url'), 'author': (v.get('user') or {}).get('name'),
                    'duration': v['duration'], 'licence': 'Pexels License', 'query': query})
    return out


def pixabay(query: str, key: str) -> list[dict]:
    q = urllib.parse.urlencode({'key': key, 'q': query, 'per_page': 30, 'safesearch': 'true'})
    data = get(f'https://pixabay.com/api/videos/?{q}')
    out = []
    for v in data.get('hits', []):
        vs = v.get('videos', {})
        f = vs.get('large') if (vs.get('large') or {}).get('url') else vs.get('medium')
        if not f or not f.get('url') or v.get('duration', 0) < 6:
            continue
        out.append({'id': f"pixabay-{v['id']}", 'url': f['url'], 'page': v.get('pageURL'), 'author': v.get('user'),
                    'duration': v['duration'], 'licence': 'Pixabay Content License', 'query': query})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', required=True)
    ap.add_argument('--seconds', type=float, required=True)
    ap.add_argument('--seed', type=int, default=1)
    a = ap.parse_args()
    load_env()
    pk, xk = os.environ.get('PEXELS_API_KEY'), os.environ.get('PIXABAY_API_KEY')
    if not pk and not xk:
        print('no PEXELS_API_KEY / PIXABAY_API_KEY — falling back to the drawn loop', file=sys.stderr)
        sys.exit(3)
    rng = random.Random(a.seed)
    used = set(USED.read_text().split()) if USED.exists() else set()
    queries = QUERIES[:]
    rng.shuffle(queries)

    picked, total = [], 0.0
    for q in queries:
        if total >= a.seconds:
            break
        try:
            cands = pexels(q, pk) if pk else pixabay(q, xk)
        except Exception as e:  # noqa: BLE001
            print(f'search "{q}" failed: {e}', file=sys.stderr)
            continue
        cands = [c for c in cands if c['id'] not in used and c['id'] not in {p['id'] for p in picked}]
        rng.shuffle(cands)
        for c in cands[:2]:
            c['take'] = min(c['duration'] - 1, rng.uniform(4.0, 7.0))
            c['start'] = rng.uniform(0.5, max(0.5, c['duration'] - c['take'] - 0.5))
            picked.append(c)
            total += c['take']
            if total >= a.seconds:
                break
    if total < a.seconds:
        print(f'only found {total:.1f}s of footage', file=sys.stderr)
        sys.exit(3)

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        parts = []
        for i, c in enumerate(picked):
            src = Path(tmp) / f'src{i}.mp4'
            req = urllib.request.Request(c['url'], headers={'User-Agent': 'zylo-studio/1.0'})
            with urllib.request.urlopen(req, timeout=120) as r:
                src.write_bytes(r.read())
            seg = Path(tmp) / f'seg{i}.mp4'
            subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f"{c['start']:.2f}", '-t', f"{c['take']:.2f}", '-i', str(src), '-an',
                            '-vf', f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,setsar=1',
                            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', str(seg)], check=True)
            parts.append(seg)
        lst = Path(tmp) / 'list.txt'
        lst.write_text(''.join(f"file '{p}'\n" for p in parts))
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(lst), '-t', f'{a.seconds:.2f}',
                        '-c', 'copy', str(out)], check=True)
    credits = [{k: c[k] for k in ('id', 'page', 'author', 'licence', 'query')} for c in picked]
    Path(str(out) + '.json').write_text(json.dumps(credits, indent=1))
    with USED.open('a') as f:
        f.write(''.join(c['id'] + '\n' for c in picked))
    print(json.dumps({'out': str(out), 'clips': len(picked), 'queries': sorted({c['query'] for c in picked})}))


if __name__ == '__main__':
    main()
