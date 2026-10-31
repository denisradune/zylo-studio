#!/usr/bin/env python3
"""
AI stills for an episode. Every image prompt gets the zylo look appended
(cinematic, dark, one warm-yellow highlight, no text, no real people).

Providers, picked automatically in this order:
  1. toolkit FLUX.2 (Modal/RunPod) when MODAL_FLUX2_ENDPOINT_URL or RUNPOD_FLUX2_ENDPOINT_ID is set
  2. Pollinations (FLUX, free, no key) otherwise

  scripts/images.py --jobs jobs.json            # [{"prompt": "...", "out": ".../01.jpg", "w":1080, "h":1920, "seed": 1}]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLKIT = Path(os.environ.get('TOOLKIT_DIR', ROOT.parent / 'digitalsamba/claude-code-video-toolkit'))

STYLE = (
    'cinematic, dramatic low-key lighting, deep dark background, single warm golden-yellow accent light, '
    'high detail, sharp focus, rich contrast, editorial science illustration, '
    'no text, no letters, no watermark, no logos'
)


def via_pollinations(prompt: str, out: Path, w: int, h: int, seed: int) -> None:
    q = urllib.parse.quote(f'{prompt}. {STYLE}')
    url = f'https://image.pollinations.ai/prompt/{q}?width={w}&height={h}&model=flux&nologo=true&seed={seed}'
    last = None
    for attempt in range(6):
        try:
            with urllib.request.urlopen(url, timeout=180) as r:
                data = r.read()
            if len(data) < 10_000:
                raise RuntimeError(f'suspiciously small image ({len(data)} bytes)')
            out.write_bytes(data)
            return
        except Exception as e:  # noqa: BLE001 - retry any transport failure
            last = e
            # Free tier: one image per 45 s per IP (HTTP 402 FREE_LIMIT).
            time.sleep(47 if getattr(e, 'code', None) == 402 else 4 * (attempt + 1))
    raise RuntimeError(f'pollinations failed for {out.name}: {last}')


def via_toolkit_flux(prompt: str, out: Path, w: int, h: int, seed: int) -> None:
    cloud = 'modal' if os.environ.get('MODAL_FLUX2_ENDPOINT_URL') else 'runpod'
    subprocess.run(
        ['uv', 'run', 'tools/flux2.py', '--prompt', f'{prompt}. {STYLE}', '--width', str(w), '--height', str(h),
         '--seed', str(seed), '--cloud', cloud, '--no-open', '--output', str(out.resolve())],
        cwd=TOOLKIT, check=True,
    )


def generate(job: dict) -> str:
    out = Path(job['out'])
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and out.stat().st_size > 10_000:
        return f'skip {out.name}'
    fn = via_toolkit_flux if (os.environ.get('MODAL_FLUX2_ENDPOINT_URL') or os.environ.get('RUNPOD_FLUX2_ENDPOINT_ID')) else via_pollinations
    fn(job['prompt'], out, job.get('w', 1080), job.get('h', 1920), job.get('seed', 1))
    return f'ok {out.name}'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--jobs', required=True)
    ap.add_argument('--parallel', type=int, default=3)
    jobs = json.loads(Path(ap.parse_args().jobs).read_text())
    toolkit = os.environ.get('MODAL_FLUX2_ENDPOINT_URL') or os.environ.get('RUNPOD_FLUX2_ENDPOINT_ID')
    if toolkit:
        with ThreadPoolExecutor(ap.parse_args().parallel) as ex:
            for msg in ex.map(generate, jobs):
                print(msg, flush=True)
        return
    for i, job in enumerate(jobs):
        msg = generate(job)
        print(msg, flush=True)
        if msg.startswith('ok') and i + 1 < len(jobs):
            time.sleep(46)  # stay under the free-tier rate limit


if __name__ == '__main__':
    sys.exit(main())
