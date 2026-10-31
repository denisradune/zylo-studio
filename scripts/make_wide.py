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

    # One transparent panel still per chapter, then a single ffmpeg pass:
    # blurred low-res copy as background + the cut centred + the panel of the current chapter.
    panels = []
    for i in range(len(chapters)):
        pj = full / f'wide-panel-{i}.json'
        pj.write_text(json.dumps({'title': series['title'], 'chapters': chapters, 'current': i}))
        png = out / f'wide-panel-{i}.png'
        run(['npx', 'remotion', 'still', 'zylo-toon/src/index.ts', 'WidePanel', str(png), f'--props={pj}', '--image-format=png', '--log=error'], cwd=TPL)
        pj.unlink()
        panels.append(png)
    ends = [c['start'] for c in chapters[1:]] + [dur + 1]
    fc = ['[0:v]split=2[a][b]',
          '[a]scale=270:480,crop=270:152:0:164,boxblur=8:2,scale=1920:1080,eq=brightness=-0.22:saturation=1.3[bg]',
          '[b]scale=608:1080[fg]',
          '[bg][fg]overlay=656:0[v0]']
    for i, (c, e) in enumerate(zip(chapters, ends)):
        fc.append(f"[v{i}][{i + 1}:v]overlay=0:0:enable='between(t,{c['start']},{e})'[v{i + 1}]")
    cmd = ['ffmpeg', '-loglevel', 'error', '-y', '-i', str(out / 'short.mp4')]
    for png in panels:
        cmd += ['-loop', '1', '-i', str(png)]
    cmd += ['-filter_complex', ';'.join(fc), '-map', f'[v{len(chapters)}]', '-map', '0:a', '-t', f'{dur:.3f}',
            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-r', '30',
            '-c:a', 'copy', '-movflags', '+faststart', str(out / 'wide.mp4')]
    run(cmd)
    for png in panels:
        png.unlink()

    lines = [f"{stamp(c['start'])} {c['label'].title()} · {c['title']}" for c in chapters]
    (full / 'chapters.txt').write_text('\n'.join(lines) + '\n')
    print('\n'.join(lines))
    print(json.dumps({'wide': str(out / 'wide.mp4'), 'seconds': round(dur, 2)}))


if __name__ == '__main__':
    main()
