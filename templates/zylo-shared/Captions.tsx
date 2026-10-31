import React, { useMemo } from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import { brand, textOutline } from './brand';
import type { Word } from './types';

interface Page {
  words: Word[];
  startMs: number;
  endMs: number;
}

const SENTENCE_END = /[.!?…]["')\]]*$/;

/** Groups words into short pages: break on sentence end, a pause, or the word/char limits. */
const paginate = (words: Word[], maxWords: number, maxChars: number, pauseMs = 450): Page[] => {
  const pages: Page[] = [];
  let cur: Word[] = [];
  const flush = () => {
    if (cur.length) pages.push({ words: cur, startMs: cur[0].startMs, endMs: cur[cur.length - 1].endMs });
    cur = [];
  };
  for (const w of words) {
    const prev = cur[cur.length - 1];
    const chars = cur.map((c) => c.text).join(' ').length + w.text.length + 1;
    if (
      prev &&
      (cur.length >= maxWords ||
        chars > maxChars ||
        SENTENCE_END.test(prev.text) ||
        (/[,;:—]$/.test(prev.text) && cur.length >= 2) ||
        w.startMs - prev.endMs > pauseMs)
    ) {
      flush();
    }
    cur.push(w);
  }
  flush();
  // Hold each page until the next one starts, so captions never flicker off mid-sentence.
  pages.forEach((p, i) => {
    const next = pages[i + 1];
    p.endMs = next ? Math.min(next.startMs, p.endMs + 900) : p.endMs + 500;
  });
  return pages;
};

/**
 * Word-by-word karaoke captions. The current word is painted in the brand yellow
 * and nudged up in scale. `centerY` is the vertical centre of the caption line as a
 * fraction of frame height (0.78 for Shorts). `offsetMs` shifts word times when the
 * words are timed relative to a VO that starts later than the composition.
 */
export const Captions: React.FC<{
  words: Word[];
  centerY?: number;
  fontSize?: number;
  maxWords?: number;
  maxChars?: number;
  maxWidth?: number;
  offsetMs?: number;
  hideFromMs?: number;
}> = ({ words, centerY = 0.78, fontSize = 92, maxWords = 3, maxChars = 18, maxWidth = 940, offsetMs = 0, hideFromMs }) => {
  const frame = useCurrentFrame();
  const { fps, height } = useVideoConfig();
  const pages = useMemo(() => paginate(words, maxWords, maxChars), [words, maxWords, maxChars]);
  const t = (frame / fps) * 1000 - offsetMs;
  if (hideFromMs !== undefined && t + offsetMs >= hideFromMs) return null;
  const page = pages.find((p) => t >= p.startMs && t < p.endMs);
  if (!page) return null;

  const popIn = interpolate(t - page.startMs, [0, 90], [0.85, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ pointerEvents: 'none' }}>
      <div
        style={{
          position: 'absolute',
          left: '50%',
          top: height * centerY,
          transform: `translate(-50%, -50%) scale(${popIn})`,
          width: maxWidth,
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          alignItems: 'center',
          gap: `0 ${fontSize * 0.36}px`,
          textAlign: 'center',
        }}
      >
        {page.words.map((w, i) => {
          const active = t >= w.startMs && t < (page.words[i + 1]?.startMs ?? page.endMs);
          return (
            <span
              key={`${w.startMs}-${i}`}
              style={{
                fontFamily: brand.display,
                fontSize,
                lineHeight: 1.12,
                textTransform: 'uppercase',
                color: active ? brand.accent : brand.text,
                transform: `scale(${active ? 1.1 : 1})`,
                display: 'inline-block',
                textShadow: textOutline(Math.max(3, Math.round(fontSize / 18))),
              }}
            >
              {w.text}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
