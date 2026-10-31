#!/usr/bin/env python3
"""
zylo sound-effects library, synthesised from scratch (no samples, no licences).

  scripts/sfx.py                 # (re)builds brand/sfx/*.wav
  scripts/sfx.py --list

Each effect is short, mono, 44.1 kHz and peak-normalised; the story template places them per
shot ({"type": "boom", "at": 1.2}) and mixes them under the voice.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'brand/sfx'
SR = 44100
rng = np.random.default_rng(7)


def t(sec: float) -> np.ndarray:
    return np.arange(int(sec * SR)) / SR


def noise(sec: float) -> np.ndarray:
    return rng.standard_normal(int(sec * SR))


def band(x: np.ndarray, lo: float, hi: float) -> np.ndarray:
    b, a = butter(2, [lo / (SR / 2), hi / (SR / 2)], btype='band')
    return lfilter(b, a, x)


def low(x: np.ndarray, hz: float) -> np.ndarray:
    b, a = butter(2, hz / (SR / 2), btype='low')
    return lfilter(b, a, x)


def env(n: int, attack: float, release: float) -> np.ndarray:
    a = np.minimum(1, np.arange(n) / max(1, attack * SR))
    r = np.exp(-np.arange(n) / max(1, release * SR))
    return a * r


def whoosh() -> np.ndarray:
    d = 0.7
    x = noise(d)
    out = np.zeros_like(x)
    # sweep a band-pass up then down by processing short blocks
    blocks = 40
    n = len(x) // blocks
    for i in range(blocks):
        p = i / blocks
        c = 300 + 2600 * np.sin(np.pi * p)
        out[i * n:(i + 1) * n] = band(x[i * n:(i + 1) * n], c * 0.7, c * 1.3)
    return out * np.sin(np.pi * np.linspace(0, 1, len(out))) ** 2


def boom() -> np.ndarray:
    d = 2.2
    tt = t(d)
    sub = np.sin(2 * np.pi * (38 + 60 * np.exp(-tt * 6)) * tt) * np.exp(-tt * 1.6)
    crack = low(noise(d), 1800) * np.exp(-tt * 5)
    rumble = low(noise(d), 120) * np.exp(-tt * 1.1) * 3
    return sub * 1.0 + crack * 0.5 + rumble * 0.6


def hit() -> np.ndarray:
    d = 0.5
    tt = t(d)
    return np.sin(2 * np.pi * (70 + 120 * np.exp(-tt * 25)) * tt) * np.exp(-tt * 9) + low(noise(d), 3000) * np.exp(-tt * 30) * 0.4


def alarm() -> np.ndarray:
    d = 2.0
    tt = t(d)
    f = 650 + 350 * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 1.5 * tt)))
    ph = np.cumsum(2 * np.pi * f / SR)
    return np.sign(np.sin(ph)) * 0.35 + np.sin(ph) * 0.3


def siren() -> np.ndarray:
    d = 3.0
    tt = t(d)
    f = 700 + 400 * np.sin(2 * np.pi * 0.5 * tt)
    return np.sin(np.cumsum(2 * np.pi * f / SR)) * 0.6


def buzz() -> np.ndarray:
    d = 1.1
    tt = t(d)
    gate = ((tt % 0.5) < 0.32).astype(float)
    return np.sin(2 * np.pi * 160 * tt) * np.sign(np.sin(2 * np.pi * 40 * tt)) * gate * 0.7


def ring() -> np.ndarray:
    notes = [988, 1319, 1175, 1568, 988, 1319]
    out = []
    for f in notes:
        tt = t(0.14)
        out.append((np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)) * env(len(tt), 0.005, 0.08))
    one = np.concatenate(out + [np.zeros(int(0.15 * SR))])
    return np.concatenate([one, one])


def ding() -> np.ndarray:
    tt = t(1.0)
    return (np.sin(2 * np.pi * 1320 * tt) + 0.5 * np.sin(2 * np.pi * 1980 * tt)) * np.exp(-tt * 5)


def pop() -> np.ndarray:
    tt = t(0.18)
    return np.sin(2 * np.pi * (500 + 900 * np.exp(-tt * 40)) * tt) * np.exp(-tt * 28)


def riser() -> np.ndarray:
    d = 2.0
    tt = t(d)
    f = 200 * (2 ** (tt * 2.2))
    tone = np.sin(np.cumsum(2 * np.pi * f / SR)) * 0.35
    air = band(noise(d), 2000, 7000) * (tt / d) * 0.6
    return (tone + air) * (tt / d) ** 1.5


def glitch() -> np.ndarray:
    d = 0.6
    out = np.zeros(int(d * SR))
    pos = 0
    while pos < len(out):
        n = int(rng.uniform(0.01, 0.06) * SR)
        f = rng.uniform(200, 3000)
        seg = np.sign(np.sin(2 * np.pi * f * np.arange(n) / SR)) if rng.random() > 0.4 else rng.standard_normal(n)
        out[pos:pos + n] = seg[: len(out) - pos] * rng.uniform(0.2, 0.8)
        pos += n
    return out


def growl() -> np.ndarray:
    d = 1.6
    tt = t(d)
    f = 70 + 15 * np.sin(2 * np.pi * 3 * tt) + 10 * rng.standard_normal(len(tt)).cumsum() / SR
    voice = np.sign(np.sin(np.cumsum(2 * np.pi * f / SR)))
    rasp = band(noise(d), 300, 1400)
    return low(voice * 0.6 + rasp * 0.8, 1500) * np.sin(np.pi * np.linspace(0, 1, len(tt)))


def crash() -> np.ndarray:
    d = 1.2
    tt = t(d)
    shards = np.zeros(len(tt))
    for _ in range(40):
        s = int(rng.uniform(0, 0.5) * SR)
        f = rng.uniform(2500, 7000)
        n = int(0.15 * SR)
        k = np.arange(min(n, len(tt) - s))
        shards[s:s + len(k)] += np.sin(2 * np.pi * f * k / SR) * np.exp(-k / (0.03 * SR)) * rng.uniform(0.2, 0.6)
    return shards + low(noise(d), 2500) * np.exp(-tt * 6) * 0.8


def heartbeat() -> np.ndarray:
    out = []
    for _ in range(2):
        for gap in (0.18, 0.62):
            tt = t(0.16)
            out.append(np.sin(2 * np.pi * 55 * tt) * np.exp(-tt * 22))
            out.append(np.zeros(int(gap * SR)))
    return np.concatenate(out) * 1.4


def engine() -> np.ndarray:
    d = 2.5
    tt = t(d)
    f = 45 + 40 * np.minimum(1, tt / 1.2)
    return low(np.sign(np.sin(np.cumsum(2 * np.pi * f / SR))) + 0.4 * noise(d), 400) * np.minimum(1, tt * 4)


def tick() -> np.ndarray:
    out = []
    for i in range(4):
        tt = t(0.05)
        out.append(band(noise(0.05), 2000, 6000) * np.exp(-tt * 120))
        out.append(np.zeros(int(0.45 * SR)))
    return np.concatenate(out)


def powerdown() -> np.ndarray:
    d = 1.4
    tt = t(d)
    f = 900 * np.exp(-tt * 2.5) + 40
    return np.sin(np.cumsum(2 * np.pi * f / SR)) * np.exp(-tt * 1.5) * 0.7


def powerup() -> np.ndarray:
    return powerdown()[::-1].copy()


def knock() -> np.ndarray:
    out = []
    for gap in (0.18, 0.18, 0.5):
        out.append(hit()[: int(0.2 * SR)] * 0.9)
        out.append(np.zeros(int(gap * SR)))
    return np.concatenate(out)


LIB = {f.__name__: f for f in (whoosh, boom, hit, alarm, siren, buzz, ring, ding, pop, riser, glitch, growl, crash,
                                heartbeat, engine, tick, powerdown, powerup, knock)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--list', action='store_true')
    a = ap.parse_args()
    if a.list:
        print(' '.join(LIB))
        return
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in LIB.items():
        y = fn().astype(np.float32)
        y = y / (np.abs(y).max() + 1e-9) * 0.9
        fade = min(len(y), int(0.01 * SR))
        y[-fade:] *= np.linspace(1, 0, fade)
        sf.write(OUT / f'{name}.wav', y, SR)
    print(f'{len(LIB)} effects -> {OUT}')


if __name__ == '__main__':
    main()
