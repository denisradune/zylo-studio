#!/usr/bin/env python3
"""
Voiceover + word timings for a zylo episode, fully local (no API keys).

Voice: the brand voice in brand/voice.json (Kokoro-82M, Apache-2.0, via ONNX).
Each sentence is synthesised whole, so intonation stays natural. Word times are
then recovered by DTW: the same voice reads every word on its own, the isolated
words are concatenated, and MFCC dynamic time warping maps their boundaries onto
the sentence audio. Same voice on both sides, so the alignment is tight.

Usage:
  scripts/tts.py --text-file episode/narration.txt --out-dir episode/public/audio
Writes voiceover.mp3, voiceover.wav and words.json ({seconds, words:[{text,startMs,endMs}]}).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

ROOT = Path(__file__).resolve().parent.parent
SR = 24000
HOP = 240  # 10 ms
PAUSE = {'.': 0.30, '!': 0.30, '?': 0.38, '…': 0.40}


def load_voice():
    cfg = json.loads((ROOT / 'brand/voice.json').read_text())
    k = Kokoro(str(ROOT / '.models/kokoro-v1.0.onnx'), str(ROOT / '.models/voices-v1.0.bin'))
    style = np.load(ROOT / cfg['style_file'])
    return k, style, cfg


def speaker_voice(k, speaker: str):
    """(style, cfg) for a story speaker, from brand/voices.json."""
    table = json.loads((ROOT / 'brand/voices.json').read_text())
    cfg = table.get(speaker) or table['narrator']
    style = np.load(ROOT / cfg['style_file']) if 'style_file' in cfg else k.get_voice_style(cfg['voice'])
    return style, cfg


def robot(y: np.ndarray) -> np.ndarray:
    """Bit's voice tint: light phaser + very short slap echo, same length as the input."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        a, b = Path(d) / 'a.wav', Path(d) / 'b.wav'
        sf.write(a, y, SR)
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(a), '-af',
                        'aphaser=in_gain=0.8:out_gain=0.9:delay=2.5:decay=0.45:speed=0.9,aecho=0.85:0.5:9:0.25',
                        '-ar', str(SR), str(b)], check=True)
        out, _ = sf.read(b, dtype='float32')
    return out[: len(y)] if len(out) >= len(y) else np.pad(out, (0, len(y) - len(out)))


def say(k, style, cfg, text: str, speed: float) -> np.ndarray:
    audio, sr = k.create(text, voice=style, speed=speed, lang=cfg['lang'])
    assert sr == SR
    return audio.astype(np.float32)


def sentences(text: str) -> list[str]:
    text = re.sub(r'\s+', ' ', text.strip())
    return [s for s in re.split(r'(?<=[.!?…])\s+', text) if s]


def spoken(word: str) -> str:
    """What the model should read for one caption word ('part?' -> 'part', '$1.2' stays)."""
    return re.sub(r'^[^\w$£€%]+|[^\w%]+$', '', word) or word


def mfcc(y: np.ndarray) -> np.ndarray:
    m = librosa.feature.mfcc(y=y, sr=SR, n_mfcc=20, hop_length=HOP, n_fft=1024)
    return (m - m.mean(axis=1, keepdims=True)) / (m.std(axis=1, keepdims=True) + 1e-6)


def align(k, style, cfg, sent_audio: np.ndarray, words: list[str], speed: float) -> list[tuple[float, float]]:
    """Return (start, end) seconds for each word inside sent_audio."""
    pieces, bounds, pos = [], [], 0
    for w in words:
        a = say(k, style, cfg, spoken(w), speed)
        a, _ = librosa.effects.trim(a, top_db=35)
        pieces.append(a)
        bounds.append(pos)
        pos += len(a)
    ref = np.concatenate(pieces)
    # Trim the sentence's own edge silence for the DTW, then shift back.
    _, (s0, s1) = librosa.effects.trim(sent_audio, top_db=35)
    core = sent_audio[s0:s1]
    _, path = librosa.sequence.dtw(X=mfcc(ref), Y=mfcc(core), metric='cosine')
    path = path[::-1]
    ref_to_core = {}
    for r, c in path:
        ref_to_core.setdefault(r, []).append(c)
    n_ref = mfcc(ref).shape[1]

    def map_sample(sample: int) -> float:
        f = min(n_ref - 1, sample // HOP)
        cs = ref_to_core.get(f)
        while cs is None and f > 0:
            f -= 1
            cs = ref_to_core.get(f)
        return (s0 + int(np.median(cs)) * HOP) / SR

    starts = [map_sample(b) for b in bounds]
    starts[0] = s0 / SR
    out = []
    for i, st in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else s1 / SR
        out.append((st, max(end, st + 0.06)))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--text-file')
    ap.add_argument('--lines-json', help='story mode: [{"speaker": "hero", "text": "..."}]; *word* marks caption emphasis')
    ap.add_argument('--out-dir', required=True)
    ap.add_argument('--speed', type=float, default=None, help='override brand speed (1.0 = natural)')
    args = ap.parse_args()

    k, style, cfg = load_voice()
    speed = args.speed or cfg.get('speed', 1.0)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    if args.lines_json:
        return story(k, json.loads(Path(args.lines_json).read_text()), out)

    lead = np.zeros(int(0.12 * SR), dtype=np.float32)
    track, words, t = [lead], [], len(lead) / SR
    for s in sentences(Path(args.text_file).read_text()):
        audio = say(k, style, cfg, s, speed)
        _, (a0, a1) = librosa.effects.trim(audio, top_db=40)
        pad = int(0.04 * SR)
        audio = audio[max(0, a0 - pad): a1 + pad]
        toks = s.split(' ')
        for tok, (a, b) in zip(toks, align(k, style, cfg, audio, toks, speed)):
            words.append({'text': tok, 'startMs': round((t + a) * 1000), 'endMs': round((t + b) * 1000)})
        track.append(audio)
        t += len(audio) / SR
        gap = np.zeros(int(PAUSE.get(s[-1], 0.25) * SR), dtype=np.float32)
        track.append(gap)
        t += len(gap) / SR

    y = np.concatenate(track[:-1])  # no pause after the last sentence
    y = y / max(1e-6, np.abs(y).max()) * 0.89
    sf.write(out / 'voiceover.wav', y, SR)
    # Loudness-normalise for speech (-16 LUFS leaves room for the music bed).
    subprocess.run(
        ['ffmpeg', '-loglevel', 'error', '-y', '-i', str(out / 'voiceover.wav'),
         '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '44100', '-b:a', '192k', str(out / 'voiceover.mp3')],
        check=True,
    )
    seconds = len(y) / SR
    (out / 'words.json').write_text(json.dumps({'seconds': round(seconds, 3), 'words': words}, indent=1))
    wpm = len(words) / seconds * 60
    print(json.dumps({'seconds': round(seconds, 2), 'words': len(words), 'wpm': round(wpm)}))


def story(k, lines: list[dict], out: Path) -> None:
    """Multi-voice VO: each line in its speaker's voice, words tagged with line index and emphasis."""
    lead = np.zeros(int(0.10 * SR), dtype=np.float32)
    track, words, spans, t = [lead], [], [], len(lead) / SR
    for li, line in enumerate(lines):
        style, cfg = speaker_voice(k, line['speaker'])
        line_start = t
        sents = sentences(line['text'])
        for si, s in enumerate(sents):
            toks = s.split(' ')
            clean = ' '.join(x.replace('*', '') for x in toks)
            audio = say(k, style, cfg, clean, cfg.get('speed', 1.0))
            _, (a0, a1) = librosa.effects.trim(audio, top_db=40)
            pad = int(0.04 * SR)
            audio = audio[max(0, a0 - pad): a1 + pad]
            plain = [x.replace('*', '') for x in toks]
            for tok, (a, b) in zip(toks, align(k, style, cfg, audio, plain, cfg.get('speed', 1.0))):
                words.append({'text': tok.replace('*', ''), 'startMs': round((t + a) * 1000), 'endMs': round((t + b) * 1000),
                              'line': li, 'emph': tok.startswith('*') or tok.rstrip('.,!?…').endswith('*')})
            if cfg.get('fx') == 'robot':
                audio = robot(audio)
            track.append(audio)
            t += len(audio) / SR
            if si < len(sents) - 1:
                gap = np.zeros(int(PAUSE.get(s[-1], 0.25) * 0.8 * SR), dtype=np.float32)
                track.append(gap)
                t += len(gap) / SR
        spans.append({'speaker': line['speaker'], 'start': round(line_start, 3), 'end': round(t, 3)})
        gap = np.zeros(int(float(line.get('pauseAfter', 0.22)) * SR), dtype=np.float32)
        track.append(gap)
        t += len(gap) / SR
    y = np.concatenate(track[:-1])
    y = y / max(1e-6, np.abs(y).max()) * 0.89
    sf.write(out / 'voiceover.wav', y, SR)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(out / 'voiceover.wav'), '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11',
                    '-ar', '44100', '-b:a', '192k', str(out / 'voiceover.mp3')], check=True)
    seconds = len(y) / SR
    (out / 'words.json').write_text(json.dumps({'seconds': round(seconds, 3), 'words': words, 'lines': spans}, indent=1))
    print(json.dumps({'seconds': round(seconds, 2), 'words': len(words), 'lines': len(spans), 'wpm': round(len(words) / seconds * 60)}))


if __name__ == '__main__':
    main()
