import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
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
import type { Chapter, LongProps } from '../../zylo-shared/types';

export const FPS = 30;
const DEFAULT_CARD = 2.5;

type Segment = { kind: 'intro' | 'chapter' | 'outro'; index: number; card: number; body: Omit<Chapter, 'title'>; title?: string };

/** Lays the episode out on one timeline; shared by the component and calculateMetadata. */
export const layout = (p: LongProps) => {
  const card = p.chapterCardSeconds ?? DEFAULT_CARD;
  const segs: Segment[] = [
    { kind: 'intro', index: 0, card: 0, body: p.intro },
    ...p.chapters.map((c, i) => ({ kind: 'chapter' as const, index: i + 1, card, body: c, title: c.title })),
    { kind: 'outro', index: 0, card: 0, body: p.outro },
  ];
  let t = 0;
  const placed = segs.map((s) => {
    const start = t;
    t += s.card + s.body.voiceoverSeconds + 0.5;
    return { ...s, start, end: t };
  });
  return { segments: placed, totalSeconds: t };
};

const ChapterCard: React.FC<{ index: number; title: string; durationInFrames: number }> = ({ index, title, durationInFrames }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 15 } });
  const s2 = spring({ frame: frame - 6, fps, config: { damping: 15 } });
  const out = interpolate(frame, [durationInFrames - 8, durationInFrames], [1, 0], { extrapolateLeft: 'clamp' });
  return (
    <AbsoluteFill style={{ backgroundColor: brand.bg, opacity: out }}>
      <AbsoluteFill style={{ background: 'radial-gradient(circle at 25% 50%, rgba(255,212,0,0.18), rgba(11,11,15,0) 55%)' }} />
      <AbsoluteFill style={{ justifyContent: 'center', paddingLeft: 160 }}>
        <div
          style={{
            fontFamily: brand.body,
            fontWeight: 900,
            fontSize: 44,
            letterSpacing: 10,
            color: brand.accent,
            opacity: s,
            transform: `translateX(${(1 - s) * -80}px)`,
          }}
        >
          CHAPTER {String(index).padStart(2, '0')}
        </div>
        <div style={{ height: 10, width: 220 * s, background: brand.accent, margin: '26px 0 34px' }} />
        <div
          style={{
            fontFamily: brand.display,
            fontSize: 150,
            lineHeight: 1,
            color: brand.text,
            textTransform: 'uppercase',
            maxWidth: 1500,
            opacity: s2,
            transform: `translateX(${(1 - s2) * -120}px)`,
          }}
        >
          {title}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const ChapterTag: React.FC<{ index: number; title: string }> = ({ index, title }) => (
  <div
    style={{
      position: 'absolute',
      top: 44,
      left: 56,
      padding: '10px 22px',
      background: 'rgba(11,11,15,0.75)',
      borderLeft: `8px solid ${brand.accent}`,
      fontFamily: brand.body,
      fontWeight: 900,
      fontSize: 28,
      color: brand.text,
      textTransform: 'uppercase',
      letterSpacing: 2,
    }}
  >
    {String(index).padStart(2, '0')} · {title}
  </div>
);

const Body: React.FC<{ body: Omit<Chapter, 'title'> }> = ({ body }) => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill>
      {body.visuals.map((v, i) => {
        const from = Math.round(v.start * fps);
        const dur = Math.max(1, Math.round(v.end * fps) - from);
        return (
          <Sequence key={i} from={from} durationInFrames={dur} premountFor={fps}>
            <VisualLayer visual={v} durationInFrames={dur} vertical={false} />
          </Sequence>
        );
      })}
      <Captions words={body.words} centerY={0.85} fontSize={72} maxWords={5} maxChars={30} maxWidth={1500} />
      <Audio src={staticFile(body.voiceover)} />
    </AbsoluteFill>
  );
};

export const ZyloLong: React.FC<LongProps> = (props) => {
  const { fps, durationInFrames } = useVideoConfig();
  const { segments } = layout(props);
  const vol = props.musicVolume ?? 0.12;
  return (
    <AbsoluteFill style={{ backgroundColor: brand.bg }}>
      {segments.map((s, i) => {
        const from = Math.round(s.start * fps);
        const cardF = Math.round(s.card * fps);
        const total = Math.round(s.end * fps) - from;
        return (
          <Sequence key={i} from={from} durationInFrames={total}>
            {cardF > 0 && (
              <Sequence durationInFrames={cardF}>
                <ChapterCard index={s.index} title={s.title ?? ''} durationInFrames={cardF} />
              </Sequence>
            )}
            <Sequence from={cardF}>
              <Body body={s.body} />
              {s.kind === 'chapter' && <ChapterTag index={s.index} title={s.title ?? ''} />}
            </Sequence>
          </Sequence>
        );
      })}
      {props.music && (
        <Audio
          src={staticFile(props.music)}
          loop
          volume={(f) =>
            vol * interpolate(f, [0, 15, durationInFrames - 2 * fps, durationInFrames], [0, 1, 1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })
          }
        />
      )}
    </AbsoluteFill>
  );
};

/** 1280x720 thumbnail: bright image on the right, 3-4 heavy words on the left, *accent* word in yellow. */
export const ZyloThumbnail: React.FC<{ text: string; image: string; badge?: string }> = ({ text, image, badge }) => {
  const parts = text.split(/\s+/);
  return (
    <AbsoluteFill style={{ backgroundColor: brand.bg }}>
      <AbsoluteFill style={{ left: 420 }}>
        <Img src={staticFile(image)} style={{ width: '100%', height: '100%', objectFit: 'cover', filter: 'saturate(1.25) contrast(1.1)' }} />
      </AbsoluteFill>
      <AbsoluteFill
        style={{ background: `linear-gradient(90deg, ${brand.bg} 0%, ${brand.bg} 34%, rgba(11,11,15,0.55) 55%, rgba(11,11,15,0) 75%)` }}
      />
      <AbsoluteFill style={{ flexDirection: 'row', flexWrap: 'wrap', alignContent: 'center', gap: '0 26px', paddingLeft: 56, width: 760 }}>
        {parts.map((w, i) => {
          const accent = /^\*.*\*$/.test(w);
          return (
            <div
              key={i}
              style={{
                fontFamily: brand.display,
                fontSize: parts.length > 3 ? 150 : 175,
                lineHeight: 0.98,
                textTransform: 'uppercase',
                color: accent ? brand.bg : brand.text,
                background: accent ? brand.accent : 'transparent',
                padding: accent ? '4px 18px 0' : '0',
                marginBottom: accent ? 10 : 0,
                textShadow: accent ? 'none' : textOutline(5),
                transform: accent ? 'rotate(-2deg)' : 'none',
              }}
            >
              {w.replace(/\*/g, '')}
            </div>
          );
        })}
      </AbsoluteFill>
      {badge && (
        <div
          style={{
            position: 'absolute',
            top: 30,
            right: 30,
            background: brand.accent,
            color: brand.bg,
            fontFamily: brand.display,
            fontSize: 64,
            padding: '6px 24px',
            borderRadius: 12,
          }}
        >
          {badge}
        </div>
      )}
      <div style={{ position: 'absolute', bottom: 0, left: 0, right: 0, height: 14, background: brand.accent }} />
    </AbsoluteFill>
  );
};
