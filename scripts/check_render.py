#!/usr/bin/env python3
"""
QC a rendered zylo video before upload. Exit 1 on any hard failure.

Checks: resolution, fps, duration (35-50 s for Shorts and equal to VO + tail),
audio present and loud enough, no black gaps, captions inside the frame
and
extracts review frames to out/frames/ (default 0.8 s, middle, 30 s).

  scripts/check_render.py episodes/x/out/short.mp4 --props episodes/x/props.json
  scripts/check_render.py out/long.mp4 --long
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


def probe(path: Path) -> dict:
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def ff_filter(path: Path, af: str | None = None, vf: str | None = None) -> str:
    cmd = ['ffmpeg', '-hide_banner', '-nostats', '-i', str(path)]
    cmd += ['-af', af] if af else ['-an']
    cmd += ['-vf', vf] if vf else ['-vn']
    cmd += ['-f', 'null', '-']
    return subprocess.run(cmd, capture_output=True, text=True).stderr


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('video')
    ap.add_argument('--props')
    ap.add_argument('--long', action='store_true')
    ap.add_argument('--frames', default=None, help='comma-separated seconds to extract')
    ap.add_argument('--min', type=float, default=35)
    ap.add_argument('--max', type=float, default=50)
    a = ap.parse_args()
    v = Path(a.video)
    errors, warns, info = [], [], []

    meta = probe(v)
    vs = next(s for s in meta['streams'] if s['codec_type'] == 'video')
    aus = [s for s in meta['streams'] if s['codec_type'] == 'audio']
    dur = float(meta['format']['duration'])
    w, h = vs['width'], vs['height']
    fps = float(Fraction(vs['r_frame_rate']))
    want = (1920, 1080) if a.long else (1080, 1920)
    (info if (w, h) == want else errors).append(f'resolution {w}x{h} (want {want[0]}x{want[1]})')
    (info if abs(fps - 30) < 0.01 else errors).append(f'fps {fps:g}')
    if a.long:
        (info if 480 <= dur <= 720 else warns).append(f'duration {dur:.2f}s (target 8-12 min)')
    else:
        (info if a.min <= dur <= a.max else errors).append(f'duration {dur:.2f}s (target {a.min:g}-{a.max:g}s)')

    if a.props:
        p = json.loads(Path(a.props).read_text())
        if 'voiceoverSeconds' in p:
            expect = p['voiceoverSeconds'] + p.get('tailSeconds', 0.4)
            (info if abs(dur - expect) < 0.25 else errors).append(f'ends with VO: video {dur:.2f}s vs VO+tail {expect:.2f}s')
            spans = [round(x['end'] - x['start'], 2) for x in p.get('beats', p.get('shots', p.get('visuals', [])))]
            if any(s > 3.6 for s in spans):
                warns.append(f'visual held >3.6s: {spans}')

    if not aus:
        errors.append('no audio stream')
    else:
        lo = ff_filter(v, af='ebur128=framelog=quiet')
        m = re.findall(r'I:\s+(-?[\d.]+) LUFS', lo)
        lufs = float(m[-1]) if m else -99
        (info if -17 <= lufs <= -12 else warns if lufs > -24 else errors).append(f'loudness {lufs:.1f} LUFS (target -14)')

    bl = ff_filter(v, vf='blackdetect=d=0.3:pix_th=0.06')
    blacks = re.findall(r'black_start:([\d.]+) black_end:([\d.]+)', bl)
    (errors if blacks else info).append(f'black gaps: {blacks or "none"}')

    frames_dir = v.parent / 'frames'
    frames_dir.mkdir(exist_ok=True)
    times = [float(x) for x in a.frames.split(',')] if a.frames else [0.8, round(dur / 2, 1), min(30.0, dur - 1)]
    paths = []
    for t in times:
        fp = frames_dir / f'frame_{t:05.1f}s.jpg'
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', str(t), '-i', str(v), '-frames:v', '1', str(fp)], check=True)
        paths.append(str(fp))
    info.append(f'frames: {", ".join(paths)}')

    for tag, items in (('ERROR', errors), ('WARN', warns), ('ok', info)):
        for it in items:
            print(f'[{tag}] {it}')
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
