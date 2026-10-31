import React, { useMemo } from 'react';
import { AbsoluteFill, Easing, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { getWaveformPortion, useAudioData } from '@remotion/media-utils';
import { brand, Theme } from './brand';
import type { Word } from './types';

/** Fades and un-blurs an element in from `delay` frames. */
export const useBlurIn = (delay = 0, dur = 10) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame - delay, [0, dur], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });
  return { opacity: p, filter: `blur(${(1 - p) * 14}px)`, transform: `translateY(${(1 - p) * 18}px)` };
};

/** Theme surface with a slow-breathing accent glow centred on the hero. */
export const Backdrop: React.FC<{ theme: Theme; glowY?: number }> = ({ theme, glowY = 0.42 }) => {
  const frame = useCurrentFrame();
  const breathe = 1 + Math.sin(frame / 22) * 0.06;
  return (
    <AbsoluteFill style={{ backgroundColor: theme.bg }}>
      <AbsoluteFill
        style={{
          background: `radial-gradient(circle at 50% ${glowY * 100}%, ${theme.glow} 0%, rgba(0,0,0,0) ${38 * breathe}%)`,
        }}
      />
      {/* fine grain so flat fills don't band after YouTube's re-encode */}
      <AbsoluteFill
        style={{
          opacity: 0.06,
          backgroundImage:
            'url("data:image/svg+xml;utf8,<svg xmlns=%27http://www.w3.org/2000/svg%27 width=%27160%27 height=%27160%27><filter id=%27n%27><feTurbulence type=%27fractalNoise%27 baseFrequency=%270.9%27 numOctaves=%272%27/></filter><rect width=%27100%25%27 height=%27100%25%27 filter=%27url(%23n)%27/></svg>")',
        }}
      />
    </AbsoluteFill>
  );
};

/** zylo mark: dark rounded tile with a yellow Z. */
export const LogoMark: React.FC<{ size: number; shine?: boolean }> = ({ size, shine = false }) => {
  const frame = useCurrentFrame();
  const sweep = ((frame % 90) / 90) * 260 - 80;
  return (
    <div
      style={{
        width: size,
        height: size,
        borderRadius: size * 0.27,
        background: 'linear-gradient(145deg, #1E1E26, #0E0E12)',
        border: `${Math.max(2, size / 40)}px solid rgba(255,212,0,0.35)`,
        boxShadow: `0 ${size / 8}px ${size / 3}px rgba(0,0,0,0.45)`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      <span style={{ fontFamily: brand.head, fontWeight: 900, fontSize: size * 0.62, color: brand.accent, lineHeight: 1, marginTop: size * 0.04 }}>
        Z
      </span>
      {shine && (
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background: `linear-gradient(115deg, rgba(255,255,255,0) ${sweep}%, rgba(255,255,255,0.35) ${sweep + 8}%, rgba(255,255,255,0) ${sweep + 16}%)`,
          }}
        />
      )}
    </div>
  );
};

/** Logo + one segment per section; the current one fills as its beats play. */
export const TopBar: React.FC<{ theme: Theme; sections: number; section: number; sectionProgress: number }> = ({
  theme,
  sections,
  section,
  sectionProgress,
}) => (
  <div style={{ position: 'absolute', top: 64, left: 60, right: 60, display: 'flex', alignItems: 'center', gap: 28 }}>
    <LogoMark size={84} />
    <div style={{ flex: 1, display: 'flex', gap: 12 }}>
      {Array.from({ length: sections }).map((_, i) => {
        const fill = i < section ? 1 : i === section ? sectionProgress : 0;
        return (
          <div key={i} style={{ flex: 1, height: 8, borderRadius: 4, background: theme.soft, overflow: 'hidden' }}>
            <div style={{ width: `${fill * 100}%`, height: '100%', background: brand.accent, borderRadius: 4 }} />
          </div>
        );
      })}
    </div>
  </div>
);

/** Headline above the hero. Words un-blur one after another; *accent* words take the accent colour. */
export const Headline: React.FC<{ text: string; theme: Theme; hook?: boolean }> = ({ text, theme, hook = false }) => {
  const frame = useCurrentFrame();
  // Track *accent* spans that cover several words.
  let open = false;
  const words = text.split(/\s+/).map((w) => {
    const starts = w.startsWith('*');
    const ends = /\*[.,!?]*$/.test(w);
    if (starts) open = true;
    const accent = open;
    if (ends) open = false;
    return { text: w.replace(/\*/g, ''), accent };
  });
  const size = hook ? 112 : 64;
  return (
    <div
      style={{
        position: 'absolute',
        top: hook ? 250 : 210,
        left: 70,
        right: 70,
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'center',
        gap: `${hook ? 4 : 2}px ${size * 0.28}px`,
        textAlign: 'center',
      }}
    >
      {words.map((w, i) => {
        // The hook must be fully legible on frame 0 (it is the Shorts cover).
        const delay = hook ? 0 : i * 4;
        const p = hook
          ? 1
          : interpolate(frame - delay, [0, 10], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic) });
        return (
          <span
            key={i}
            style={{
              fontFamily: brand.head,
              fontWeight: 900,
              fontSize: size,
              lineHeight: 1.1,
              textTransform: hook ? 'uppercase' : 'none',
              letterSpacing: hook ? -1 : -0.5,
              color: w.accent ? theme.accentText : theme.text,
              opacity: p,
              filter: `blur(${(1 - p) * 12}px)`,
              display: 'inline-block',
              textShadow: hook ? '0 6px 30px rgba(0,0,0,0.55)' : 'none',
            }}
          >
            {w.text}
          </span>
        );
      })}
    </div>
  );
};

type Sentence = { words: Word[]; startMs: number; endMs: number };

const toSentences = (words: Word[]): Sentence[] => {
  const out: Sentence[] = [];
  let cur: Word[] = [];
  const flush = () => {
    if (cur.length) out.push({ words: cur, startMs: cur[0].startMs, endMs: cur[cur.length - 1].endMs });
    cur = [];
  };
  words.forEach((w) => {
    cur.push(w);
    const end = /[.!?…]["')]*$/.test(w.text);
    const softBreak = /[,;:—]$/.test(w.text) && cur.length >= 7;
    if (end || softBreak || cur.length >= 13) flush();
  });
  flush();
  out.forEach((s, i) => {
    const next = out[i + 1];
    s.endMs = next ? next.startMs : s.endMs + 600;
  });
  return out;
};

/** Whole phrase in a pill: spoken words solid, the current word in accent, upcoming words dim. */
export const SentenceCaptions: React.FC<{ words: Word[]; theme: Theme; centerY?: number }> = ({ words, theme, centerY = 0.78 }) => {
  const frame = useCurrentFrame();
  const { fps, height } = useVideoConfig();
  const sentences = useMemo(() => toSentences(words), [words]);
  const t = (frame / fps) * 1000;
  const s = sentences.find((x) => t >= x.startMs - 120 && t < x.endMs);
  if (!s) return null;
  const appear = interpolate(t - (s.startMs - 120), [0, 140], [0, 1], { extrapolateRight: 'clamp' });
  return (
    <div
      style={{
        position: 'absolute',
        left: 0,
        right: 0,
        top: height * centerY,
        transform: 'translateY(-50%)',
        display: 'flex',
        justifyContent: 'center',
      }}
    >
    <div
      style={{
        transform: `scale(${0.96 + 0.04 * appear})`,
        opacity: appear,
        maxWidth: 940,
        padding: '22px 36px',
        borderRadius: 30,
        background: theme.pill,
        border: '2px solid rgba(255,255,255,0.08)',
        boxShadow: '0 18px 50px rgba(0,0,0,0.35)',
        textAlign: 'center',
        fontFamily: brand.body,
        fontWeight: 700,
        fontSize: 50,
        lineHeight: 1.28,
      }}
    >
      {s.words.map((w, i) => {
        const next = s.words[i + 1];
        const current = t >= w.startMs && t < (next ? next.startMs : s.endMs);
        const spoken = t >= w.startMs;
        return (
          <span key={i} style={{ color: current ? brand.accent : spoken ? theme.pillText : theme.pillMuted }}>
            {w.text}
            {i < s.words.length - 1 ? ' ' : ''}
          </span>
        );
      })}
    </div>
    </div>
  );
};

/** Scrolling voice waveform with a fixed playhead: the bars are the real VO envelope. */
export const Waveform: React.FC<{ src: string; theme: Theme; top: number }> = ({ src, theme, top }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const audio = useAudioData(staticFile(src));
  const enter = useBlurIn(0, 10);
  if (!audio) return null;
  const window = 4; // seconds visible
  const bars = 56;
  const t = frame / fps;
  const start = t - window / 2;
  const portion = getWaveformPortion({
    audioData: audio,
    startTimeInSeconds: Math.max(0, start),
    durationInSeconds: window,
    numberOfSamples: bars,
  });
  const pad = start < 0 ? Math.round((-start / window) * bars) : 0;
  const vals = [...Array(pad).fill(0), ...portion.map((p) => p.amplitude)].slice(0, bars);
  return (
    <div style={{ position: 'absolute', top, left: 120, right: 120, height: 90, display: 'flex', alignItems: 'center', gap: 6, ...enter }}>
      {vals.map((v, i) => (
        <div
          key={i}
          style={{
            flex: 1,
            height: `${Math.max(8, Math.min(1, v * 3.2) * 100)}%`,
            borderRadius: 3,
            background: i < bars / 2 ? theme.text : theme.muted,
            opacity: i < bars / 2 ? 0.85 : 0.6,
          }}
        />
      ))}
      <div style={{ position: 'absolute', left: '50%', top: -16, bottom: -16, width: 5, borderRadius: 3, background: brand.accent }} />
    </div>
  );
};

/** Row of small chips; the active one lifts and gets an accent ring. */
export const Chips: React.FC<{ items: string[]; active: number; theme: Theme; top: number }> = ({ items, active, theme, top }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <div style={{ position: 'absolute', top, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 20 }}>
      {items.map((it, i) => {
        const s = spring({ frame: frame - i * 3, fps, config: { damping: 14 } });
        const on = i === active;
        return (
          <div
            key={i}
            style={{
              minWidth: 92,
              height: 92,
              padding: '0 22px',
              borderRadius: 24,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              background: on ? theme.card : theme.soft,
              border: `3px solid ${on ? brand.accent : 'transparent'}`,
              boxShadow: on ? '0 10px 30px rgba(255,212,0,0.25)' : 'none',
              transform: `scale(${(on ? 1.08 : 1) * s})`,
              fontFamily: brand.body,
              fontWeight: 900,
              fontSize: 40,
              color: on ? theme.text : theme.muted,
            }}
          >
            {it}
          </div>
        );
      })}
    </div>
  );
};
