import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import { brand, textOutline } from '../../zylo-shared/brand';
import { Captions } from '../../zylo-shared/Captions';
import { VisualLayer } from '../../zylo-shared/Visuals';
import type { ShortProps } from '../../zylo-shared/types';

const HOOK_END = 1.5; // seconds the hook text owns the top third

const Hook: React.FC<{ text: string; accent?: string[] }> = ({ text, accent = [] }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const acc = new Set(accent.map((a) => a.toLowerCase()));
  // Fully legible on frame 0: frame 0 is the Shorts cover in the feed.
  const settle = interpolate(frame, [0, 8], [1.08, 1], { extrapolateRight: 'clamp' });
  const out = interpolate(frame, [HOOK_END * fps - 6, HOOK_END * fps + 4], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return (
    <AbsoluteFill style={{ opacity: out }}>
      <div
        style={{
          position: 'absolute',
          top: 230,
          left: 60,
          right: 60,
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          gap: '0 26px',
          transform: `scale(${settle})`,
        }}
      >
        {text.split(/\s+/).map((w, i) => (
          <span
            key={i}
            style={{
              fontFamily: brand.display,
              fontSize: 132,
              lineHeight: 1.04,
              textTransform: 'uppercase',
              color: acc.has(w.toLowerCase().replace(/[^a-z0-9%$?]/g, '').replace(/\?$/, '')) ? brand.accent : brand.text,
              textShadow: textOutline(6),
            }}
          >
            {w}
          </span>
        ))}
      </div>
    </AbsoluteFill>
  );
};

const ProgressBar: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  return (
    <div style={{ position: 'absolute', top: 0, left: 0, height: 10, width: `${(frame / durationInFrames) * 100}%`, background: brand.accent }} />
  );
};

/** Closing card: brand wordmark + the CTA sentence lit word by word in sync with the VO. */
const CtaCard: React.FC<{ words: ShortProps['words']; ctaStartMs: number }> = ({ words, ctaStartMs }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 14 } });
  const t = (frame / fps) * 1000 + ctaStartMs;
  const ctaWords = words.filter((w) => w.startMs >= ctaStartMs - 150);
  return (
    <AbsoluteFill style={{ backgroundColor: brand.bg, opacity: interpolate(frame, [0, 6], [0, 1], { extrapolateRight: 'clamp' }) }}>
      <AbsoluteFill style={{ background: 'radial-gradient(circle at 50% 40%, rgba(255,212,0,0.25), rgba(11,11,15,0) 60%)' }} />
      <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', padding: 80, top: -80 }}>
        <div
          style={{
            fontFamily: brand.display,
            fontSize: 220,
            letterSpacing: 6,
            color: brand.accent,
            transform: `scale(${0.7 + 0.3 * s})`,
            lineHeight: 1,
          }}
        >
          ZYLO
        </div>
        <div
          style={{
            marginTop: 40,
            padding: '22px 64px',
            borderRadius: 999,
            background: brand.accent,
            color: brand.bg,
            fontFamily: brand.body,
            fontWeight: 900,
            fontSize: 64,
            letterSpacing: 2,
            transform: `scale(${s})`,
          }}
        >
          FOLLOW
        </div>
        <div style={{ marginTop: 60, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '0 20px', maxWidth: 920 }}>
          {ctaWords.map((w, i) => {
            const spoken = t >= w.startMs;
            return (
              <span
                key={i}
                style={{
                  fontFamily: brand.display,
                  fontSize: 84,
                  lineHeight: 1.15,
                  textTransform: 'uppercase',
                  color: spoken ? brand.text : 'rgba(255,255,255,0.28)',
                }}
              >
                {w.text}
              </span>
            );
          })}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const ZyloShort: React.FC<ShortProps> = (props) => {
  const { fps, durationInFrames } = useVideoConfig();
  const ctaFrame = Math.round(props.ctaStart * fps);
  const musicVolume = props.musicVolume ?? 0.15;

  return (
    <AbsoluteFill style={{ backgroundColor: brand.bg }}>
      {props.visuals.map((v, i) => {
        const from = Math.round(v.start * fps);
        const dur = Math.max(1, Math.round(v.end * fps) - from);
        return (
          <Sequence key={i} from={from} durationInFrames={dur} premountFor={fps}>
            <VisualLayer visual={v} durationInFrames={dur} vertical />
          </Sequence>
        );
      })}

      <Sequence durationInFrames={Math.round((HOOK_END + 0.4) * fps)}>
        <Hook text={props.hook} accent={props.hookAccent} />
      </Sequence>

      <Captions words={props.words} centerY={0.78} hideFromMs={props.ctaStart * 1000} />

      <Sequence from={ctaFrame}>
        <CtaCard words={props.words} ctaStartMs={props.ctaStart * 1000} />
      </Sequence>

      <ProgressBar />

      <Audio src={staticFile(props.voiceover)} />
      {props.music && (
        <Audio
          src={staticFile(props.music)}
          loop
          volume={(f) =>
            musicVolume *
            interpolate(f, [0, 10, durationInFrames - fps, durationInFrames], [0, 1, 1, 0], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            })
          }
        />
      )}
    </AbsoluteFill>
  );
};
