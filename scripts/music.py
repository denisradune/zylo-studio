#!/usr/bin/env python3
"""
Original background music bed, synthesised locally (no samples, no licences to track).

Each mood fixes the harmonic colour, tempo range and instrumentation; the seed picks
key, progression, tempo and arpeggio pattern, so every episode gets its own track.

  scripts/music.py --mood mystery --seconds 50 --seed 1234 --out episode/public/audio/music.mp3
Moods: mystery, wonder, tension, tech, space, warm
"""
from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

SR = 44100

MOODS = {
    #           scale intervals         progressions (scale degrees)                    bpm       arp  kick  brightness
    'mystery': ([0, 2, 3, 5, 7, 8, 10], [[0, 5, 2, 6], [0, 3, 5, 4], [0, 6, 5, 6]], (72, 86), True, True, 0.35),
    'wonder': ([0, 2, 4, 6, 7, 9, 11], [[0, 4, 5, 3], [0, 5, 3, 4], [3, 4, 0, 5]], (88, 104), True, False, 0.6),
    'tension': ([0, 1, 3, 5, 7, 8, 10], [[0, 0, 1, 0], [0, 5, 1, 0], [0, 3, 1, 5]], (96, 112), True, True, 0.3),
    'tech': ([0, 2, 3, 5, 7, 9, 10], [[0, 3, 4, 3], [0, 6, 3, 4], [0, 4, 6, 3]], (108, 124), True, True, 0.7),
    'space': ([0, 2, 4, 7, 9, 11, 14], [[0, 3, 0, 4], [0, 5, 3, 0], [5, 3, 0, 0]], (60, 72), False, False, 0.45),
    'warm': ([0, 2, 4, 5, 7, 9, 11], [[0, 5, 3, 4], [0, 3, 4, 0], [5, 3, 0, 4]], (80, 96), True, False, 0.5),
}


def hz(midi: float) -> float:
    return 440.0 * 2 ** ((midi - 69) / 12)


def lowpass(x: np.ndarray, cutoff: float) -> np.ndarray:
    from scipy.signal import lfilter

    a = np.exp(-2 * np.pi * cutoff / SR)
    return lfilter([1 - a], [1, -a], x)


def saw(f: float, n: int, rng: np.random.Generator) -> np.ndarray:
    t = np.arange(n) / SR
    ph = rng.random()
    return 2 * ((f * t + ph) % 1.0) - 1


def pad(freqs: list[float], n: int, bright: float, rng) -> np.ndarray:
    out = np.zeros(n)
    for f in freqs:
        for det in (-0.08, 0.0, 0.08):
            out += saw(f * 2 ** (det / 12), n, rng)
    out = lowpass(out, 500 + 1800 * bright)
    env = np.minimum(1, np.arange(n) / (0.6 * SR)) * np.minimum(1, (n - np.arange(n)) / (0.4 * SR))
    return out * env / (3 * len(freqs))


def pluck(f: float, n: int, bright: float) -> np.ndarray:
    t = np.arange(n) / SR
    tone = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) + 0.12 * np.sin(6 * np.pi * f * t) * bright
    return tone * np.exp(-t * 7)


def kick(n: int) -> np.ndarray:
    t = np.arange(n) / SR
    f = 50 + 70 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def reverb(x: np.ndarray, seconds: float, rng) -> np.ndarray:
    from scipy.signal import fftconvolve

    n = int(seconds * SR)
    ir = rng.standard_normal(n) * np.exp(-np.arange(n) / (SR * seconds / 5))
    ir[0] = 1
    wet = fftconvolve(x, ir)[: len(x)]
    return 0.7 * x + 0.3 * wet / (np.abs(wet).max() + 1e-9) * np.abs(x).max()


def render(mood: str, seconds: float, seed: int) -> np.ndarray:
    scale, progs, (lo, hi), use_arp, use_kick, bright = MOODS[mood]
    rng = np.random.default_rng(seed)
    root = 45 + int(rng.integers(0, 8))  # A2..E3
    bpm = float(rng.integers(lo, hi + 1))
    prog = progs[int(rng.integers(len(progs)))]
    beat = 60 / bpm
    bar = int(4 * beat * SR)
    total = int(seconds * SR) + SR
    out = np.zeros(total + bar)
    arp_pattern = rng.permutation([0, 1, 2, 3, 2, 1, 4, 2])
    n_bars = total // bar + 1

    def chord(deg: int) -> list[float]:
        notes = [scale[(deg + i) % 7] + 12 * ((deg + i) // 7) for i in (0, 2, 4)]
        return [root + 12 + n for n in notes]

    for b in range(n_bars):
        deg = prog[b % len(prog)]
        c = chord(deg)
        s = b * bar
        out[s : s + bar] += 0.55 * pad([hz(m) for m in c], bar, bright, rng)
        bass = np.sin(2 * np.pi * hz(root + scale[deg % 7] - 12 * (scale[deg % 7] > 7)) * np.arange(bar) / SR)
        out[s : s + bar] += 0.22 * bass * np.minimum(1, np.arange(bar) / 2000) * np.minimum(1, (bar - np.arange(bar)) / 4000)
        if use_arp and b >= 1:
            step = int(beat / 2 * SR)
            for i in range(8):
                note = (c + [c[0] + 12, c[1] + 12])[arp_pattern[i] % 5] + 12
                p = pluck(hz(note), step * 2, bright)
                st = s + i * step
                out[st : st + len(p)] += 0.10 * p[: len(out) - st]
        if use_kick and b >= 2:
            for i in range(4):
                k = kick(int(0.4 * SR))
                st = s + int(i * beat * SR)
                out[st : st + len(k)] += 0.25 * k[: len(out) - st]

    out = reverb(out[:total], 2.5 if mood in ('space', 'mystery') else 1.6, rng)
    stereo = np.stack([out, np.roll(out, int(0.012 * SR))], axis=1)
    return stereo / (np.abs(stereo).max() + 1e-9) * 0.8


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--mood', choices=MOODS, required=True)
    ap.add_argument('--seconds', type=float, required=True)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    y = render(a.mood, a.seconds, a.seed)
    with tempfile.TemporaryDirectory() as d:
        wav = Path(d) / 'm.wav'
        sf.write(wav, y, SR)
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(wav), '-af', 'loudnorm=I=-18:TP=-2',
                        '-ar', '44100', '-b:a', '192k', a.out], check=True)
    print(a.out)


if __name__ == '__main__':
    main()
