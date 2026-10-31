#!/usr/bin/env python3
"""
Build one zylo Short from its episode spec, end to end:
  voiceover + word timings -> music -> AI stills -> Remotion props -> render -> QC.

  scripts/make_short.py episodes/2026-10-30-slug            # runs every stage, skipping ones already done
  scripts/make_short.py episodes/2026-10-30-slug --from props   # redo from a stage: tts|music|images|props|render|qc

episode.json:
{
  "hook": "Your stomach digests itself?", "hookAccent": ["digests"],
  "mood": "mystery", "seed": 4182,
  "lines": [
    {"say": "Six to eight words, one visual each.", "visual": {"type": "image", "prompt": "...", "motion": "in"}},
    {"say": "...", "visual": {"type": "stat", "value": "86 billion", "label": "neurons", "bgPrompt": "..."}},
    {"say": "Follow for one fact a day that changes how you see the world.", "visual": {"type": "cta"}}
  ]
}
A visual shows from its line's first word until the next line starts, so a line of
6-8 words gives the 2-3 second rhythm. The CTA line must be last.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = str(ROOT / '.venv/bin/python')
TEMPLATES = ROOT / 'templates'
STAGES = ['tts', 'music', 'images', 'props', 'render', 'qc']
LEAD = 0.08  # cut to the next visual slightly before its first word lands


def run(cmd: list[str], **kw) -> None:
    print('+', ' '.join(cmd), flush=True)
    subprocess.run(cmd, check=True, **kw)


def narration(ep: dict) -> str:
    return ' '.join(l['say'].strip() for l in ep['lines'])


def stage_tts(d: Path, ep: dict) -> None:
    (d / 'narration.txt').write_text(narration(ep) + '\n')
    run([PY, str(ROOT / 'scripts/tts.py'), '--text-file', str(d / 'narration.txt'), '--out-dir', str(d / 'public/audio')])


def vo(d: Path) -> dict:
    return json.loads((d / 'public/audio/words.json').read_text())


def stage_music(d: Path, ep: dict) -> None:
    run([PY, str(ROOT / 'scripts/music.py'), '--mood', ep.get('mood', 'mystery'), '--seconds', str(vo(d)['seconds'] + 3),
         '--seed', str(ep.get('seed', 1)), '--out', str(d / 'public/audio/music.mp3')])


def image_jobs(d: Path, ep: dict) -> list[tuple[int, str, str]]:
    """(line index, hero key, prompt) -> one image file per prompt, named by line and slot."""
    out = []
    for i, line in enumerate(ep['lines']):
        hero = line.get('hero', {})
        if hero.get('prompt'):
            out.append((i, f'images/{i + 1:02d}.jpg', hero['prompt']))
        for k, pr in enumerate(hero.get('prompts', [])):
            out.append((i, f'images/{i + 1:02d}-{k + 1}.jpg', pr))
    return out


def stage_images(d: Path, ep: dict) -> None:
    jobs = [{'prompt': pr, 'out': str(d / 'public' / rel), 'w': 1080, 'h': 1920, 'seed': ep.get('seed', 1) + n}
            for n, (_, rel, pr) in enumerate(image_jobs(d, ep))]
    (d / 'image-jobs.json').write_text(json.dumps(jobs, indent=1))
    run([PY, str(ROOT / 'scripts/images.py'), '--jobs', str(d / 'image-jobs.json')])


def stage_props(d: Path, ep: dict) -> None:
    v = vo(d)
    words = v['words']
    # Map each line to its first word: the narration is the lines joined by spaces.
    first, idx = [], 0
    for line in ep['lines']:
        first.append(idx)
        idx += len(line['say'].split())
    if idx != len(words):
        sys.exit(f'word count mismatch: lines have {idx}, voiceover has {len(words)}')
    starts = [0.0] + [max(0.0, words[i]['startMs'] / 1000 - LEAD) for i in first[1:]]
    cta_i = len(ep['lines']) - 1
    assert ep['lines'][cta_i].get('cta'), 'last line must be the CTA ({"say": ..., "cta": true})'
    cta_start = starts[cta_i]

    files = {}
    for i, rel, _ in image_jobs(d, ep):
        files.setdefault(i, []).append(rel)

    beats = []
    for i, line in enumerate(ep['lines'][:-1]):
        hero = {k: val for k, val in line['hero'].items() if k not in ('prompt', 'prompts')}
        imgs = files.get(i, [])
        if hero['type'] in ('image', 'card') and 'src' not in hero:
            hero['src'] = imgs[0]
        elif hero['type'] in ('phones', 'filmstrip') and 'srcs' not in hero:
            hero['srcs'] = imgs
        beat = {k: line[k] for k in ('theme', 'headline', 'headlineStyle', 'chips', 'wave') if k in line}
        beat.update({
            'section': line.get('section', 0),
            'hero': hero,
            'start': round(starts[i], 3),
            'end': round(starts[i + 1] if i + 1 < cta_i else cta_start, 3),
        })
        beats.append(beat)

    props = {
        'voiceover': 'audio/voiceover.mp3',
        'voiceoverSeconds': v['seconds'],
        'tailSeconds': 0.4,
        'words': words,
        'music': 'audio/music.mp3',
        'musicVolume': 0.15,
        'sections': max(b['section'] for b in beats) + 1,
        'beats': beats,
        'ctaStart': round(cta_start, 3),
    }
    (d / 'props.json').write_text(json.dumps(props, indent=1))
    spans = [round(b['end'] - b['start'], 1) for b in beats]
    print(f'props: {len(beats)} beats, spans {spans}, CTA at {cta_start:.2f}s, VO {v["seconds"]:.2f}s')


def stage_render(d: Path, ep: dict) -> None:
    (d / 'out').mkdir(exist_ok=True)
    raw = d / 'out/short.raw.mp4'
    run(['npx', 'remotion', 'render', 'zylo-short/src/index.ts', 'ZyloShort', str(raw),
         f'--props={d / "props.json"}', f'--public-dir={d / "public"}', '--codec=h264', '--crf=18',
         '--audio-bitrate=192k', '--log=error'], cwd=TEMPLATES)
    # Final mix to YouTube's -14 LUFS; picture is copied untouched.
    run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(raw), '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1:LRA=11',
         '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(d / 'out/short.mp4')])
    raw.unlink()


def stage_qc(d: Path, ep: dict) -> None:
    run([PY, str(ROOT / 'scripts/check_render.py'), str(d / 'out/short.mp4'), '--props', str(d / 'props.json')])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('episode_dir')
    ap.add_argument('--from', dest='start', choices=STAGES)
    ap.add_argument('--only', choices=STAGES)
    a = ap.parse_args()
    d = Path(a.episode_dir).resolve()
    ep = json.loads((d / 'episode.json').read_text())
    done = {
        'tts': (d / 'public/audio/words.json').exists(),
        'music': (d / 'public/audio/music.mp3').exists(),
        'images': False,  # images.py skips files that already exist
        'props': False,
        'render': False,
        'qc': False,
    }
    stages = [a.only] if a.only else STAGES[STAGES.index(a.start):] if a.start else [s for s in STAGES if not done[s]]
    for s in stages:
        print(f'\n=== {s} ===', flush=True)
        globals()[f'stage_{s}'](d, ep)


if __name__ == '__main__':
    main()
