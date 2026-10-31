#!/usr/bin/env python3
"""
Build one zylo "What if...?" animated story Short from episodes/<slug>/story.json:
  multi-voice VO + word timings -> music -> Remotion props -> render (zylo-toon) -> loudness -> QC.

  scripts/make_story.py episodes/2026-10-31-what-if-meteor
  scripts/make_story.py episodes/... --from props      # stages: tts|music|props|render|qc

story.json:
{
  "title": "What If a Meteor Hit Your City? #shorts", "mood": "tension", "seed": 77,
  "names": {"hero": "JAY", "bit": "BIT"},
  "end": {"text": "PART 2?", "sub": "Follow so you don't miss it"},
  "lines": [
    {"speaker": "narrator", "say": "What if a *meteor* hit your city tonight?",
     "shot": {"set": {"type": "sky", "time": "night"}, "cast": [{"id": "hero", "x": 0.5, "expr": "shocked"}],
              "fx": [{"type": "meteor", "x": 600, "y": 1300, "hitAt": 1.4}], "camera": {"zoom": 1.1}}},
    {"speaker": "hero", "say": "Bit, is that... *coming here*?", "shot": {...}},
    ...
    {"speaker": "narrator", "say": "Follow for part two.", "end": true}
  ]
}
One line = one shot (a line may give "shots": [..] to split its time evenly). *word* = yellow caption word.
The last line must have "end": true; the end card starts with it.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = str(ROOT / '.venv/bin/python')
TEMPLATES = ROOT / 'templates'
STAGES = ['tts', 'music', 'props', 'render', 'qc']
LEAD = 0.06


def run(cmd: list[str], **kw) -> None:
    print('+', ' '.join(cmd), flush=True)
    subprocess.run(cmd, check=True, **kw)


def vo(d: Path) -> dict:
    return json.loads((d / 'public/audio/words.json').read_text())


def stage_tts(d: Path, ep: dict) -> None:
    lines = [{'speaker': l['speaker'], 'text': l['say'], **({'pauseAfter': l['pauseAfter']} if 'pauseAfter' in l else {})} for l in ep['lines']]
    (d / 'lines.json').write_text(json.dumps(lines, indent=1))
    run([PY, str(ROOT / 'scripts/tts.py'), '--lines-json', str(d / 'lines.json'), '--out-dir', str(d / 'public/audio')])


def stage_music(d: Path, ep: dict) -> None:
    run([PY, str(ROOT / 'scripts/music.py'), '--mood', ep.get('mood', 'tension'), '--seconds', str(vo(d)['seconds'] + 3),
         '--seed', str(ep.get('seed', 1)), '--out', str(d / 'public/audio/music.mp3')])


def stage_props(d: Path, ep: dict) -> None:
    v = vo(d)
    spans = v['lines']
    lines = ep['lines']
    if len(spans) != len(lines):
        sys.exit(f'voiceover has {len(spans)} lines, story has {len(lines)}')
    assert lines[-1].get('end'), 'last line must have "end": true'
    starts = [0.0] + [max(0.0, s['start'] - LEAD) for s in spans[1:]]
    end_start = starts[-1]
    shots = []
    for i, line in enumerate(lines[:-1]):
        a, b = starts[i], starts[i + 1]
        parts = line.get('shots') or [line['shot']]
        if len(parts) == 1 and b - a > 3.0 and not line['shot'].get('ui') and not any('moveTo' in c for c in line['shot'].get('cast', [])):
            # Long line: punch in on the same shot halfway, so the picture changes every ~2 s.
            sh = line['shot']
            cam = sh.get('camera', {})
            speaker_x = next((c['x'] for c in sh.get('cast', []) if line['speaker'] in (c['id'], c.get('voice'))), cam.get('x', 0.5))
            punch = {**sh, 'camera': {**cam, 'zoom': round(cam.get('zoom', 1) * 1.3, 2), 'x': speaker_x, 'y': 0.55, 'push': 0.04},
                     'transition': 'cut', 'fx': [e for e in sh.get('fx', []) if e['type'] not in ('meteor', 'impact', 'throwObj')],
                     'sfx': [], 'cast': [{**c, 'enter': 'none'} for c in sh.get('cast', [])]}
            parts = [sh, punch]
        step = (b - a) / len(parts)
        for k, sh in enumerate(parts):
            shots.append({**sh, 'speaker': line['speaker'], 'start': round(a + k * step, 3), 'end': round(a + (k + 1) * step, 3)})
    props = {
        'voiceover': 'audio/voiceover.mp3',
        'voiceoverSeconds': v['seconds'],
        'tailSeconds': 0.8,
        'words': v['words'],
        'lines': spans,
        'names': ep.get('names', {}),
        'music': 'audio/music.mp3',
        'musicVolume': 0.15,
        'shots': shots,
        'endStart': round(end_start, 3),
        'endText': ep.get('end', {}).get('text', 'PART 2?'),
        'endSub': ep.get('end', {}).get('sub', 'Follow so you don’t miss it'),
    }
    if ep.get('partLabel'):
        props['partLabel'] = ep['partLabel']
    if ep.get('chapters'):
        # chapters: [{"line": index of the part's first line, "label": "PART 2", "title": "..."}]
        props['chapters'] = [{'start': round(starts[c['line']], 3), 'label': c['label'], 'title': c['title']} for c in ep['chapters']]
    (d / 'props.json').write_text(json.dumps(props, indent=1))
    print(f'props: {len(shots)} shots, spans {[round(s["end"] - s["start"], 1) for s in shots]}, end card at {end_start:.2f}s, VO {v["seconds"]:.2f}s')


def stage_render(d: Path, ep: dict) -> None:
    (d / 'out').mkdir(exist_ok=True)
    sfx = d / 'public/sfx'
    if not sfx.exists():
        if not (ROOT / 'brand/sfx').exists():
            run([PY, str(ROOT / 'scripts/sfx.py')])
        shutil.copytree(ROOT / 'brand/sfx', sfx)
    raw = d / 'out/short.raw.mp4'
    run(['npx', 'remotion', 'render', 'zylo-toon/src/index.ts', 'ZyloToon', str(raw), f'--props={d / "props.json"}',
         f'--public-dir={d / "public"}', '--codec=h264', '--crf=18', '--audio-bitrate=192k', '--log=error'], cwd=TEMPLATES)
    run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(raw), '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1:LRA=11',
         '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(d / 'out/short.mp4')])
    raw.unlink()


def stage_qc(d: Path, ep: dict) -> None:
    run([PY, str(ROOT / 'scripts/check_render.py'), str(d / 'out/short.mp4'), '--props', str(d / 'props.json'),
         '--min', str(ep.get('minSeconds', 35)), '--max', str(ep.get('maxSeconds', 75))])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('episode_dir')
    ap.add_argument('--from', dest='start', choices=STAGES)
    ap.add_argument('--only', choices=STAGES)
    a = ap.parse_args()
    d = Path(a.episode_dir).resolve()
    ep = json.loads((d / 'story.json').read_text())
    stages = [a.only] if a.only else STAGES[STAGES.index(a.start):] if a.start else STAGES
    for s in stages:
        print(f'\n=== {s} ===', flush=True)
        globals()[f'stage_{s}'](d, ep)


if __name__ == '__main__':
    main()
