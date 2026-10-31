import React from 'react';
import { AbsoluteFill, Easing, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { brand, Theme } from './brand';
import type { Hero, KenBurns } from './types';

const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;

/** Spring entrance (rise, un-blur, slight 3D tilt) and a quick blur-out before the cut. */
const Enter: React.FC<{ children: React.ReactNode; dur: number; tilt?: number; centerY?: number }> = ({
  children,
  dur,
  tilt = 14,
  centerY = 0.46,
}) => {
  const frame = useCurrentFrame();
  const { fps, height } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 16, stiffness: 110 } });
  const out = interpolate(frame, [dur - 6, dur], [0, 1], clamp);
  const blur = (1 - s) * 18 + out * 16;
  return (
    <AbsoluteFill style={{ perspective: 1800 }}>
      <div
        style={{
          position: 'absolute',
          left: '50%',
          top: height * centerY,
          transform: `translate(-50%, -50%) translateY(${(1 - s) * 90}px) rotateX(${(1 - s) * tilt}deg) scale(${(0.86 + 0.14 * s) * (1 - out * 0.05)})`,
          opacity: Math.min(1, s * 1.4) * (1 - out),
          filter: `blur(${blur}px)`,
        }}
      >
        {children}
      </div>
    </AbsoluteFill>
  );
};

const kenBurns = (motion: KenBurns, p: number) => {
  const z = (a: number, b: number) => a + (b - a) * p;
  switch (motion) {
    case 'in':
      return `scale(${z(1.04, 1.16)})`;
    case 'out':
      return `scale(${z(1.18, 1.04)})`;
    case 'left':
      return `scale(1.14) translateX(${z(3, -3)}%)`;
    case 'right':
      return `scale(1.14) translateX(${z(-3, 3)}%)`;
    case 'up':
      return `scale(1.14) translateY(${z(3, -3)}%)`;
    case 'down':
      return `scale(1.14) translateY(${z(-3, 3)}%)`;
  }
};

const Photo: React.FC<{ src: string; motion?: KenBurns; dur: number; style?: React.CSSProperties }> = ({ src, motion = 'in', dur, style }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, dur], [0, 1], clamp);
  return (
    <div style={{ overflow: 'hidden', ...style }}>
      <Img src={staticFile(src)} style={{ width: '100%', height: '100%', objectFit: 'cover', transform: kenBurns(motion, p) }} />
    </div>
  );
};

/** Browser chrome strip with traffic dots and a URL pill. */
const WindowBar: React.FC<{ url?: string; theme: Theme }> = ({ url, theme }) => (
  <div style={{ height: 64, display: 'flex', alignItems: 'center', gap: 10, padding: '0 22px', background: theme.card }}>
    {[0, 1, 2].map((i) => (
      <div key={i} style={{ width: 13, height: 13, borderRadius: 7, background: theme.muted }} />
    ))}
    {url && (
      <div
        style={{
          marginLeft: 14,
          padding: '8px 18px',
          borderRadius: 14,
          background: theme.soft,
          fontFamily: brand.body,
          fontWeight: 600,
          fontSize: 24,
          color: theme.text,
          opacity: 0.85,
          display: 'flex',
          alignItems: 'center',
          gap: 10,
        }}
      >
        <span style={{ fontSize: 20 }}>🔒</span>
        {url}
      </div>
    )}
  </div>
);

const cardShell = (theme: Theme, w: number): React.CSSProperties => ({
  width: w,
  borderRadius: 40,
  overflow: 'hidden',
  background: theme.card,
  border: `2px solid ${theme.cardBorder}`,
  boxShadow: '0 40px 90px rgba(0,0,0,0.45)',
});

const Card: React.FC<{ h: Extract<Hero, { type: 'card' }>; theme: Theme; dur: number }> = ({ h, theme, dur }) => {
  const badge = useCurrentFrame() > 10;
  return (
    <div style={cardShell(theme, 800)}>
      <WindowBar url={h.url} theme={theme} />
      <Photo src={h.src} dur={dur} style={{ width: 800, height: 560 }} />
      <div
        style={{
          padding: '34px 40px 38px',
          background: `linear-gradient(180deg, ${theme.card} 0%, rgba(255,212,0,0.22) 160%)`,
          textAlign: 'center',
        }}
      >
        <div style={{ fontFamily: brand.head, fontWeight: 900, fontSize: 54, color: theme.text, lineHeight: 1.1 }}>{h.title}</div>
        {h.badge && (
          <div
            style={{
              display: 'inline-block',
              marginTop: 18,
              padding: '8px 22px',
              borderRadius: 999,
              background: theme.soft,
              fontFamily: brand.body,
              fontWeight: 700,
              fontSize: 28,
              color: theme.text,
              opacity: badge ? 1 : 0,
            }}
          >
            <span style={{ color: brand.accent }}>★</span> {h.badge}
          </div>
        )}
      </div>
    </div>
  );
};

/** A page from the source: title, meta and placeholder text lines, one swept with a highlighter. */
const Source: React.FC<{ h: Extract<Hero, { type: 'source' }>; theme: Theme; dur: number }> = ({ h, theme, dur }) => {
  const frame = useCurrentFrame();
  const mark = interpolate(frame, [12, Math.min(dur - 8, 40)], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const lines = [0.92, 0.84, 0.97, 0.7, 0.88, 0.6];
  return (
    <div style={cardShell(theme, 820)}>
      <WindowBar url={h.url} theme={theme} />
      <div style={{ padding: '44px 50px 54px', background: theme.card }}>
        <div style={{ fontFamily: brand.body, fontWeight: 900, fontSize: 46, lineHeight: 1.2, color: theme.text }}>{h.title}</div>
        {h.meta && (
          <div style={{ marginTop: 16, fontFamily: brand.body, fontWeight: 600, fontSize: 30, color: theme.muted }}>{h.meta}</div>
        )}
        <div style={{ marginTop: 36, display: 'flex', flexDirection: 'column', gap: 18 }}>
          {lines.map((w, i) => (
            <div key={i} style={{ position: 'relative', height: 20, width: `${w * 100}%`, borderRadius: 10, background: theme.soft }}>
              {i === 2 && (
                <div
                  style={{
                    position: 'absolute',
                    left: -8,
                    top: -10,
                    bottom: -10,
                    width: `calc(${mark * 100}% + 16px)`,
                    borderRadius: 8,
                    background: 'rgba(255,212,0,0.55)',
                  }}
                />
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

/** Leading number counts up; prefix/suffix kept ("$1.2 trillion", "37%"). */
const countUp = (value: string, p: number) => {
  const m = value.match(/^([^0-9]*)([0-9][0-9,]*\.?[0-9]*)(.*)$/);
  if (!m) return value;
  const [, pre, num, post] = m;
  const target = parseFloat(num.replace(/,/g, ''));
  const decimals = num.includes('.') ? num.split('.')[1].length : 0;
  const shown = (target * p).toLocaleString('en-US', { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
  return `${pre}${num.includes(',') ? shown : shown.replace(/,/g, '')}${post}`;
};

const Tile: React.FC<{ h: Extract<Hero, { type: 'tile' }>; theme: Theme }> = ({ h, theme }) => {
  const frame = useCurrentFrame();
  const sweep = interpolate(frame, [8, 30], [-60, 160], clamp);
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <div
        style={{
          width: 440,
          height: 440,
          borderRadius: 100,
          position: 'relative',
          overflow: 'hidden',
          background: 'linear-gradient(150deg, #6E5A00 0%, #3B3000 55%, #241D00 100%)',
          border: '3px solid rgba(255,212,0,0.45)',
          boxShadow: '0 40px 100px rgba(255,212,0,0.25), inset 0 2px 0 rgba(255,255,255,0.25)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <span
          style={{
            fontFamily: brand.head,
            fontWeight: 900,
            fontSize: h.value.length <= 2 ? 270 : h.value.length === 3 ? 190 : h.value.length <= 5 ? 108 : 88,
            lineHeight: 1,
            background: 'linear-gradient(180deg, #FFFFFF 30%, #FFE680 100%)',
            WebkitBackgroundClip: 'text',
            color: 'transparent',
          }}
        >
          {h.value}
        </span>
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background: `linear-gradient(115deg, rgba(255,255,255,0) ${sweep}%, rgba(255,255,255,0.45) ${sweep + 10}%, rgba(255,255,255,0) ${sweep + 22}%)`,
          }}
        />
      </div>
      {h.label && (
        <div style={{ marginTop: 44, fontFamily: brand.body, fontWeight: 700, fontSize: 52, color: theme.text, textAlign: 'center', maxWidth: 860 }}>
          {h.label}
        </div>
      )}
    </div>
  );
};

const Counter: React.FC<{ h: Extract<Hero, { type: 'counter' }>; theme: Theme; dur: number }> = ({ h, theme, dur }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, Math.min(dur * 0.6, 36)], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: 960 }}>
      <div
        style={{
          fontFamily: brand.head,
          fontWeight: 900,
          fontSize: h.value.length > 6 ? 170 : 250,
          lineHeight: 1,
          letterSpacing: -6,
          color: theme.accentText,
          textShadow: '0 20px 80px rgba(255,212,0,0.35)',
        }}
      >
        {countUp(h.value, p)}
      </div>
      <div style={{ marginTop: 28, fontFamily: brand.body, fontWeight: 900, fontSize: 56, color: theme.text, textAlign: 'center' }}>{h.label}</div>
      {h.sub && <div style={{ marginTop: 14, fontFamily: brand.body, fontWeight: 600, fontSize: 32, color: theme.muted }}>{h.sub}</div>}
    </div>
  );
};

const Phones: React.FC<{ h: Extract<Hero, { type: 'phones' }>; theme: Theme; dur: number }> = ({ h, theme, dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const fan = spring({ frame: frame - 4, fps, config: { damping: 15 } });
  const labels = h.labels ?? [];
  const active = labels.length ? Math.min(labels.length - 1, Math.floor((frame / Math.max(1, dur - 8)) * labels.length)) : -1;
  const phone = (src: string, i: number) => {
    const side = i - 1;
    return (
      <div
        key={i}
        style={{
          position: 'absolute',
          left: '50%',
          top: '50%',
          width: 360,
          height: 720,
          borderRadius: 56,
          overflow: 'hidden',
          border: `3px solid ${theme.cardBorder}`,
          background: theme.card,
          boxShadow: '0 40px 90px rgba(0,0,0,0.5)',
          transform: `translate(-50%, -50%) translateX(${side * 270 * fan}px) translateZ(${side === 0 ? 0 : -160}px) rotateY(${-side * 24 * fan}deg) rotateZ(${side * 4 * fan}deg)`,
          zIndex: side === 0 ? 2 : 1,
        }}
      >
        <Photo src={src} dur={dur} motion={side === 0 ? 'in' : 'out'} style={{ width: '100%', height: '100%' }} />
        {side === 0 && labels.length > 0 && (
          <div
            style={{
              position: 'absolute',
              left: 0,
              right: 0,
              bottom: 0,
              padding: '120px 26px 44px',
              background: 'linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.85) 45%)',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: 12,
            }}
          >
            {labels.map((l, j) => (
              <div
                key={j}
                style={{
                  padding: '8px 22px',
                  borderRadius: 14,
                  fontFamily: brand.body,
                  fontWeight: 900,
                  fontSize: 34,
                  color: j === active ? brand.bg : '#FFFFFF',
                  background: j === active ? brand.accent : 'transparent',
                  opacity: j <= active ? 1 : 0.45,
                }}
              >
                {l}
              </div>
            ))}
          </div>
        )}
      </div>
    );
  };
  const srcs = h.srcs.length >= 3 ? h.srcs.slice(0, 3) : [h.srcs[0], h.srcs[0], h.srcs[0]];
  return (
    <div style={{ width: 1080, height: 820, position: 'relative', transformStyle: 'preserve-3d' }}>
      {[0, 2, 1].map((i) => phone(srcs[i], i))}
    </div>
  );
};

const Filmstrip: React.FC<{ h: Extract<Hero, { type: 'filmstrip' }>; theme: Theme; dur: number }> = ({ h, dur }) => {
  const frame = useCurrentFrame();
  const x = interpolate(frame, [0, dur], [0, -420]);
  const frames = [...h.srcs, ...h.srcs, ...h.srcs].slice(0, 8);
  const holes = (
    <div style={{ display: 'flex', gap: 22, padding: '0 14px' }}>
      {Array.from({ length: 48 }).map((_, i) => (
        <div key={i} style={{ width: 26, height: 18, borderRadius: 4, background: '#F1F0EA' }} />
      ))}
    </div>
  );
  return (
    <div style={{ width: 1500, transform: 'rotate(-7deg)' }}>
      <div style={{ background: '#0B0B0F', padding: '16px 0', borderRadius: 10, boxShadow: '0 40px 90px rgba(0,0,0,0.5)', overflow: 'hidden' }}>
        <div style={{ transform: `translateX(${x}px)` }}>
          {holes}
          <div style={{ display: 'flex', gap: 16, padding: '14px 14px' }}>
            {frames.map((s, i) => (
              <Img key={i} src={staticFile(s)} style={{ width: 300, height: 400, objectFit: 'cover', borderRadius: 8, flexShrink: 0 }} />
            ))}
          </div>
          {holes}
        </div>
      </div>
    </div>
  );
};

const Checklist: React.FC<{ h: Extract<Hero, { type: 'checklist' }>; theme: Theme; dur: number }> = ({ h, theme, dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const step = Math.max(8, (dur - 10) / h.items.length);
  return (
    <div style={{ width: 820, display: 'flex', flexDirection: 'column', gap: 26 }}>
      {h.items.map((it, i) => {
        const s = spring({ frame: frame - i * step, fps, config: { damping: 15 } });
        const checked = frame > i * step + 6;
        return (
          <div
            key={i}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 28,
              padding: '28px 36px',
              borderRadius: 30,
              background: theme.card,
              border: `2px solid ${checked ? 'rgba(255,212,0,0.5)' : theme.cardBorder}`,
              boxShadow: '0 20px 50px rgba(0,0,0,0.25)',
              opacity: s,
              transform: `translateX(${(1 - s) * -80}px)`,
            }}
          >
            <div
              style={{
                width: 54,
                height: 54,
                borderRadius: 27,
                border: `4px solid ${checked ? brand.accent : theme.muted}`,
                background: checked ? brand.accent : 'transparent',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 32,
                fontWeight: 900,
                color: brand.bg,
              }}
            >
              {checked ? '✓' : ''}
            </div>
            <div style={{ fontFamily: brand.body, fontWeight: 900, fontSize: 48, color: theme.text }}>{it}</div>
          </div>
        );
      })}
    </div>
  );
};

const Chart: React.FC<{ h: Extract<Hero, { type: 'chart' }>; theme: Theme; dur: number }> = ({ h, theme, dur }) => {
  const frame = useCurrentFrame();
  const W = 860;
  const H = 520;
  const max = Math.max(...h.points);
  const min = Math.min(...h.points);
  const pts = h.points.map((v, i) => [40 + (i / (h.points.length - 1)) * (W - 80), H - 40 - ((v - min) / (max - min || 1)) * (H - 120)]);
  const len = pts.reduce((a, p, i) => (i ? a + Math.hypot(p[0] - pts[i - 1][0], p[1] - pts[i - 1][1]) : 0), 0);
  const draw = interpolate(frame, [4, Math.min(dur - 6, 40)], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const last = pts[pts.length - 1];
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <svg width={W} height={H}>
        {[0.25, 0.5, 0.75].map((g) => (
          <line key={g} x1={0} x2={W} y1={H * g} y2={H * g} stroke={theme.soft} strokeWidth={3} />
        ))}
        <polyline
          points={pts.map((p) => p.join(',')).join(' ')}
          fill="none"
          stroke={brand.accent}
          strokeWidth={10}
          strokeLinejoin="round"
          strokeLinecap="round"
          strokeDasharray={len}
          strokeDashoffset={len * (1 - draw)}
        />
        {pts.map((p, i) => (
          <circle key={i} cx={p[0]} cy={p[1]} r={14} fill={theme.bg} stroke={brand.accent} strokeWidth={6} opacity={draw >= i / (pts.length - 1) ? 1 : 0} />
        ))}
        {h.highlight && draw > 0.98 && (
          <text x={last[0]} y={last[1] - 40} textAnchor="end" fontFamily="ZyloHead" fontWeight={900} fontSize={64} fill={theme.accentText}>
            {h.highlight}
          </text>
        )}
      </svg>
      <div style={{ marginTop: 20, fontFamily: brand.body, fontWeight: 900, fontSize: 48, color: theme.text }}>{h.label}</div>
    </div>
  );
};

const Compare: React.FC<{ h: Extract<Hero, { type: 'compare' }>; theme: Theme }> = ({ h, theme }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const b = spring({ frame: frame - 10, fps, config: { damping: 14 } });
  const box = (side: { value: string; label: string }, accent: boolean, s: number) => (
    <div
      style={{
        width: 820,
        padding: '40px 30px',
        borderRadius: 40,
        background: accent ? 'linear-gradient(150deg, #6E5A00, #2C2400)' : theme.card,
        border: `2px solid ${accent ? 'rgba(255,212,0,0.5)' : theme.cardBorder}`,
        textAlign: 'center',
        opacity: s,
        transform: `translateY(${(1 - s) * 50}px)`,
      }}
    >
      <div style={{ fontFamily: brand.head, fontWeight: 900, fontSize: 130, lineHeight: 1, color: accent ? '#FFFFFF' : theme.text }}>{side.value}</div>
      <div style={{ marginTop: 14, fontFamily: brand.body, fontWeight: 700, fontSize: 40, color: accent ? '#FFE680' : theme.muted }}>{side.label}</div>
    </div>
  );
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 22 }}>
      {box(h.left, false, 1)}
      <div style={{ fontFamily: brand.head, fontWeight: 900, fontSize: 48, color: theme.muted, opacity: b }}>vs</div>
      {box(h.right, true, b)}
    </div>
  );
};

const FullBleed: React.FC<{ h: Extract<Hero, { type: 'image' }>; dur: number }> = ({ h, dur }) => {
  const frame = useCurrentFrame();
  const fade = interpolate(frame, [0, 6, dur - 4, dur], [0, 1, 1, 0.6], clamp);
  return (
    <AbsoluteFill style={{ opacity: fade }}>
      <Photo src={h.src} motion={h.motion} dur={dur} style={{ width: '100%', height: '100%' }} />
      <AbsoluteFill
        style={{ background: 'linear-gradient(180deg, rgba(11,11,15,0.85) 0%, rgba(11,11,15,0.15) 38%, rgba(11,11,15,0.2) 60%, rgba(11,11,15,0.9) 100%)' }}
      />
    </AbsoluteFill>
  );
};

/** Hero for one beat. Mount inside a <Sequence> spanning the beat. */
export const HeroLayer: React.FC<{ hero: Hero; theme: Theme; dur: number }> = ({ hero, theme, dur }) => {
  switch (hero.type) {
    case 'image':
      return <FullBleed h={hero} dur={dur} />;
    case 'card':
      return (
        <Enter dur={dur} centerY={0.47}>
          <Card h={hero} theme={theme} dur={dur} />
        </Enter>
      );
    case 'source':
      return (
        <Enter dur={dur} centerY={0.47}>
          <Source h={hero} theme={theme} dur={dur} />
        </Enter>
      );
    case 'tile':
      return (
        <Enter dur={dur} tilt={0} centerY={0.46}>
          <Tile h={hero} theme={theme} />
        </Enter>
      );
    case 'counter':
      return (
        <Enter dur={dur} tilt={0} centerY={0.45}>
          <Counter h={hero} theme={theme} dur={dur} />
        </Enter>
      );
    case 'phones':
      return (
        <Enter dur={dur} tilt={8} centerY={0.47}>
          <Phones h={hero} theme={theme} dur={dur} />
        </Enter>
      );
    case 'filmstrip':
      return (
        <Enter dur={dur} tilt={0} centerY={0.47}>
          <Filmstrip h={hero} theme={theme} dur={dur} />
        </Enter>
      );
    case 'checklist':
      return (
        <Enter dur={dur} tilt={0} centerY={0.47}>
          <Checklist h={hero} theme={theme} dur={dur} />
        </Enter>
      );
    case 'chart':
      return (
        <Enter dur={dur} tilt={10} centerY={0.47}>
          <Chart h={hero} theme={theme} dur={dur} />
        </Enter>
      );
    case 'compare':
      return (
        <Enter dur={dur} tilt={0} centerY={0.47}>
          <Compare h={hero} theme={theme} />
        </Enter>
      );
  }
};
