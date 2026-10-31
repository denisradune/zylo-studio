import React from 'react';
import {
  AbsoluteFill,
  Img,
  OffthreadVideo,
  Easing,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import { brand, textOutline } from './brand';
import type { KenBurns, Visual } from './types';

const FADE = 6; // frames of cross-fade in and out of every visual

/** Fade + tiny zoom punch at the cut, so every 2-3s change reads as deliberate. */
const CutIn: React.FC<{ children: React.ReactNode; durationInFrames: number }> = ({ children, durationInFrames }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, FADE, durationInFrames - 1, durationInFrames + FADE], [0, 1, 1, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const punch = interpolate(frame, [0, FADE + 2], [1.06, 1], {
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });
  return <AbsoluteFill style={{ opacity, transform: `scale(${punch})` }}>{children}</AbsoluteFill>;
};

const kenBurns = (motion: KenBurns, p: number) => {
  const z = (a: number, b: number) => a + (b - a) * p;
  switch (motion) {
    case 'in':
      return `scale(${z(1.04, 1.18)})`;
    case 'out':
      return `scale(${z(1.2, 1.05)})`;
    case 'left':
      return `scale(1.16) translateX(${z(3, -3)}%)`;
    case 'right':
      return `scale(1.16) translateX(${z(-3, 3)}%)`;
    case 'up':
      return `scale(1.16) translateY(${z(3, -3)}%)`;
    case 'down':
      return `scale(1.16) translateY(${z(-3, 3)}%)`;
  }
};

/** Darkens edges so captions and overlays stay readable on any image. */
export const Vignette: React.FC<{ strength?: number }> = ({ strength = 1 }) => (
  <AbsoluteFill
    style={{
      background: `linear-gradient(180deg, rgba(0,0,0,${0.55 * strength}) 0%, rgba(0,0,0,0) 30%, rgba(0,0,0,0) 55%, rgba(0,0,0,${0.75 * strength}) 100%)`,
    }}
  />
);

const ImageLayer: React.FC<{ src: string; motion: KenBurns; durationInFrames: number; dim?: number }> = ({
  src,
  motion,
  durationInFrames,
  dim = 0,
}) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, durationInFrames], [0, 1], { extrapolateRight: 'clamp' });
  return (
    <AbsoluteFill style={{ overflow: 'hidden', backgroundColor: brand.bg }}>
      <Img
        src={staticFile(src)}
        style={{ width: '100%', height: '100%', objectFit: 'cover', transform: kenBurns(motion, p) }}
      />
      {dim > 0 && <AbsoluteFill style={{ backgroundColor: `rgba(11,11,15,${dim})` }} />}
    </AbsoluteFill>
  );
};

/** Brand backdrop for infographics: dark field, soft yellow glow, slow drifting grid. */
const InfoBackdrop: React.FC<{ bgSrc?: string; durationInFrames: number }> = ({ bgSrc, durationInFrames }) => {
  const frame = useCurrentFrame();
  if (bgSrc) return <ImageLayer src={bgSrc} motion="in" durationInFrames={durationInFrames} dim={0.72} />;
  return (
    <AbsoluteFill style={{ backgroundColor: brand.bg }}>
      <AbsoluteFill
        style={{
          backgroundImage:
            'linear-gradient(rgba(255,255,255,0.05) 2px, transparent 2px), linear-gradient(90deg, rgba(255,255,255,0.05) 2px, transparent 2px)',
          backgroundSize: '90px 90px',
          backgroundPosition: `0 ${frame * 0.6}px`,
        }}
      />
      <AbsoluteFill
        style={{ background: `radial-gradient(circle at 50% 42%, rgba(255,212,0,0.22) 0%, rgba(11,11,15,0) 55%)` }}
      />
    </AbsoluteFill>
  );
};

/** Counts the leading number of `value` up from zero, keeping prefix/suffix ("$1.2 trillion", "37%"). */
const countUp = (value: string, p: number) => {
  const m = value.match(/^([^0-9]*)([0-9][0-9,]*\.?[0-9]*)(.*)$/);
  if (!m) return value;
  const [, pre, num, post] = m;
  const target = parseFloat(num.replace(/,/g, ''));
  const decimals = num.includes('.') ? num.split('.')[1].length : 0;
  const cur = target * p;
  const shown = cur.toLocaleString('en-US', { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
  return `${pre}${num.includes(',') || target >= 10000 ? shown : shown.replace(/,/g, '')}${post}`;
};

const useLocalSpring = (delay = 0) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return spring({ frame: frame - delay, fps, config: { damping: 14, stiffness: 120 } });
};

const Stat: React.FC<{ v: Extract<Visual, { type: 'stat' }>; durationInFrames: number; scale: number }> = ({
  v,
  durationInFrames,
  scale,
}) => {
  const frame = useCurrentFrame();
  const pop = useLocalSpring(0);
  const labelIn = useLocalSpring(8);
  const p = interpolate(frame, [0, Math.min(durationInFrames * 0.6, 40)], [0, 1], {
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });
  return (
    <AbsoluteFill>
      <InfoBackdrop bgSrc={v.bgSrc} durationInFrames={durationInFrames} />
      <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', padding: 80 * scale, top: -120 * scale }}>
        <div
          style={{
            fontFamily: brand.display,
            fontSize: 230 * scale,
            lineHeight: 1,
            color: brand.accent,
            transform: `scale(${0.6 + 0.4 * pop})`,
            textShadow: textOutline(4 * scale),
            textAlign: 'center',
          }}
        >
          {countUp(v.value, p)}
        </div>
        <div
          style={{
            marginTop: 30 * scale,
            fontFamily: brand.body,
            fontWeight: 900,
            fontSize: 64 * scale,
            color: brand.text,
            textTransform: 'uppercase',
            textAlign: 'center',
            opacity: labelIn,
            transform: `translateY(${(1 - labelIn) * 40}px)`,
            textShadow: textOutline(3 * scale),
          }}
        >
          {v.label}
        </div>
        {v.sub && (
          <div
            style={{
              marginTop: 18 * scale,
              fontFamily: brand.body,
              fontWeight: 700,
              fontSize: 40 * scale,
              color: brand.textDim,
              textAlign: 'center',
              opacity: labelIn,
            }}
          >
            {v.sub}
          </div>
        )}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const Compare: React.FC<{ v: Extract<Visual, { type: 'compare' }>; durationInFrames: number; scale: number; vertical: boolean }> = ({
  v,
  durationInFrames,
  scale,
  vertical,
}) => {
  const a = useLocalSpring(0);
  const b = useLocalSpring(12);
  const box = (side: { value: string; label: string }, s: number, accent: boolean) => (
    <div
      style={{
        flex: vertical ? '0 0 auto' : 1,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        opacity: s,
        transform: `translateY(${(1 - s) * 60}px)`,
      }}
    >
      <div
        style={{
          fontFamily: brand.display,
          fontSize: (vertical ? 150 : 170) * scale,
          lineHeight: 1,
          color: accent ? brand.accent : brand.text,
          textShadow: textOutline(4 * scale),
        }}
      >
        {side.value}
      </div>
      <div
        style={{
          marginTop: 16 * scale,
          fontFamily: brand.body,
          fontWeight: 900,
          fontSize: 46 * scale,
          color: brand.text,
          textTransform: 'uppercase',
          textAlign: 'center',
          textShadow: textOutline(2 * scale),
        }}
      >
        {side.label}
      </div>
    </div>
  );
  return (
    <AbsoluteFill>
      <InfoBackdrop bgSrc={v.bgSrc} durationInFrames={durationInFrames} />
      <AbsoluteFill
        style={{
          flexDirection: vertical ? 'column' : 'row',
          alignItems: 'center',
          justifyContent: 'center',
          gap: (vertical ? 24 : 70) * scale,
          padding: 80 * scale,
          top: vertical ? -260 : 0,
        }}
      >
        {box(v.left, a, false)}
        <div style={{ fontFamily: brand.display, fontSize: 90 * scale, color: brand.textDim, opacity: b }}>VS</div>
        {box(v.right, b, true)}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const Bars: React.FC<{ v: Extract<Visual, { type: 'bars' }>; durationInFrames: number; scale: number }> = ({
  v,
  durationInFrames,
  scale,
}) => {
  const frame = useCurrentFrame();
  const max = Math.max(...v.items.map((i) => i.value));
  return (
    <AbsoluteFill>
      <InfoBackdrop durationInFrames={durationInFrames} />
      <AbsoluteFill style={{ justifyContent: 'center', padding: 90 * scale, top: -120 * scale }}>
        <div
          style={{
            fontFamily: brand.display,
            fontSize: 96 * scale,
            color: brand.text,
            marginBottom: 50 * scale,
            textTransform: 'uppercase',
          }}
        >
          {v.title}
        </div>
        {v.items.map((it, i) => {
          const grow = interpolate(frame, [i * 6, i * 6 + 24], [0, it.value / max], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.out(Easing.cubic),
          });
          const top = it.value === max;
          return (
            <div key={it.label} style={{ marginBottom: 34 * scale }}>
              <div
                style={{
                  fontFamily: brand.body,
                  fontWeight: 900,
                  fontSize: 42 * scale,
                  color: brand.text,
                  marginBottom: 10 * scale,
                  display: 'flex',
                  justifyContent: 'space-between',
                }}
              >
                <span>{it.label}</span>
                <span style={{ color: top ? brand.accent : brand.textDim }}>{it.display ?? it.value}</span>
              </div>
              <div style={{ height: 46 * scale, background: 'rgba(255,255,255,0.08)', borderRadius: 10 }}>
                <div
                  style={{
                    height: '100%',
                    width: `${grow * 100}%`,
                    borderRadius: 10,
                    background: top ? brand.accent : 'rgba(255,255,255,0.55)',
                  }}
                />
              </div>
            </div>
          );
        })}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const KineticText: React.FC<{ v: Extract<Visual, { type: 'text' }>; durationInFrames: number; scale: number }> = ({
  v,
  durationInFrames,
  scale,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const accent = new Set((v.accent ?? []).map((w) => w.toLowerCase()));
  const words = v.text.split(/\s+/);
  return (
    <AbsoluteFill>
      <InfoBackdrop bgSrc={v.bgSrc} durationInFrames={durationInFrames} />
      <AbsoluteFill
        style={{
          alignItems: 'center',
          justifyContent: 'center',
          padding: 90 * scale,
          top: -140 * scale,
          flexDirection: 'row',
          flexWrap: 'wrap',
          alignContent: 'center',
          gap: `${10 * scale}px ${26 * scale}px`,
        }}
      >
        {words.map((w, i) => {
          const s = spring({ frame: frame - i * 3, fps, config: { damping: 12, stiffness: 160 } });
          const isAccent = accent.has(w.toLowerCase().replace(/[^a-z0-9%$]/g, ''));
          return (
            <span
              key={i}
              style={{
                fontFamily: brand.display,
                fontSize: 128 * scale,
                lineHeight: 1.05,
                textTransform: 'uppercase',
                color: isAccent ? brand.accent : brand.text,
                opacity: s,
                transform: `scale(${0.5 + 0.5 * s})`,
                display: 'inline-block',
                textShadow: textOutline(4 * scale),
              }}
            >
              {w}
            </span>
          );
        })}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/** Renders one visual; mount inside a <Sequence> whose duration is the visual's span. */
export const VisualLayer: React.FC<{ visual: Visual; durationInFrames: number; vertical: boolean }> = ({
  visual,
  durationInFrames,
  vertical,
}) => {
  const scale = vertical ? 1 : 0.8;
  let body: React.ReactNode;
  switch (visual.type) {
    case 'image':
      body = (
        <>
          <ImageLayer src={visual.src} motion={visual.motion ?? 'in'} durationInFrames={durationInFrames} />
          <Vignette />
        </>
      );
      break;
    case 'video':
      body = (
        <>
          <AbsoluteFill style={{ backgroundColor: brand.bg }}>
            <OffthreadVideo
              src={staticFile(visual.src)}
              muted
              playbackRate={visual.playbackRate ?? 1}
              style={{ width: '100%', height: '100%', objectFit: 'cover' }}
            />
          </AbsoluteFill>
          <Vignette />
        </>
      );
      break;
    case 'stat':
      body = <Stat v={visual} durationInFrames={durationInFrames} scale={scale} />;
      break;
    case 'compare':
      body = <Compare v={visual} durationInFrames={durationInFrames} scale={scale} vertical={vertical} />;
      break;
    case 'bars':
      body = <Bars v={visual} durationInFrames={durationInFrames} scale={scale} />;
      break;
    case 'text':
      body = <KineticText v={visual} durationInFrames={durationInFrames} scale={scale} />;
      break;
  }
  return <CutIn durationInFrames={durationInFrames}>{body}</CutIn>;
};
