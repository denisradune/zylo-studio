import React from 'react';
import { Easing, interpolate } from 'remotion';
import { INK } from './Character';
import { H, rnd, W } from './Backgrounds';

const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;

export type FxSpec =
  /** Fireball streaking from the top corner to (x, y); lands at `hitAt` seconds into the shot. */
  | { type: 'meteor'; x?: number; y?: number; hitAt?: number; size?: number }
  /** White flash + shockwave ring + debris at (x, y), `at` seconds into the shot. */
  | { type: 'impact'; x?: number; y?: number; at?: number }
  | { type: 'moneyRain' }
  | { type: 'rain' }
  | { type: 'snow' }
  | { type: 'alarm' }
  | { type: 'glitch' }
  | { type: 'ufo'; x?: number; beam?: boolean }
  | { type: 'speedLines' }
  | { type: 'vignette'; color?: string }
  /** Northern lights: waving curtains across the top of the sky. `colors` top-to-bottom tints, `y` = lower edge. */
  | { type: 'aurora'; colors?: string[]; y?: number; strength?: number }
  /** An object (phone) flying in an arc from `from` to `to`, starting `at` seconds in, lasting `dur`. */
  | { type: 'throwObj'; from: [number, number]; to: [number, number]; at?: number; dur?: number }
  /** Bright screen glow at (x, y): what the zombies chase. */
  | { type: 'glow'; x: number; y: number; r?: number }
  /** A comet: glowing head at (x, y) with a long two-part tail pointing along `angle` degrees (0 = right).
   *  `inside: true` = Earth is inside the tail: a faint blue-green haze over the whole sky instead. */
  | { type: 'comet'; x?: number; y?: number; angle?: number; length?: number; size?: number; inside?: boolean }
  /** Thick night clouds drifting across the top of the frame (bottom edge at `y`). */
  | { type: 'clouds'; y?: number; color?: string };

/** Camera shake offset for a shot that contains an impact (or `shake: true`). */
export const shakeAt = (t: number, fps: number, startSec: number, strength = 1) => {
  const local = t - startSec * fps;
  if (local < 0) return { x: 0, y: 0 };
  const decay = Math.exp(-local / 12) * 26 * strength;
  return { x: Math.sin(local * 2.7) * decay, y: Math.cos(local * 3.3) * decay };
};

const Meteor: React.FC<{ f: number; fps: number; x: number; y: number; hitAt: number; size: number }> = ({ f, fps, x, y, hitAt, size }) => {
  // Starts just inside the top-right corner so it reads from the first frame of the shot.
  const p = interpolate(f, [0, hitAt * fps], [0, 1], { ...clamp, easing: Easing.in(Easing.poly(1.4)) });
  if (f > hitAt * fps) return null;
  const sx = W - 60;
  const sy = 120;
  const cx = sx + (x - sx) * p;
  const cy = sy + (y - sy) * p;
  const ang = (Math.atan2(y - sy, x - sx) * 180) / Math.PI;
  const s = size * (0.5 + p * 0.8);
  return (
    <g transform={`translate(${cx} ${cy}) rotate(${ang})`}>
      <path d={`M 0 ${-60 * s} L ${-900 * s} 0 L 0 ${60 * s} Z`} fill="#FF8A3D" opacity={0.85} />
      <path d={`M 0 ${-34 * s} L ${-600 * s} 0 L 0 ${34 * s} Z`} fill="#FFD400" />
      <circle r={70 * s} fill="#6B4A3A" stroke={INK} strokeWidth={8} />
      <circle cx={-20 * s} cy={-18 * s} r={16 * s} fill="#4E3428" />
      <circle cx={18 * s} cy={20 * s} r={12 * s} fill="#4E3428" />
    </g>
  );
};

const Impact: React.FC<{ f: number; fps: number; x: number; y: number; at: number }> = ({ f, fps, x, y, at }) => {
  const local = f - at * fps;
  if (local < 0) return null;
  const flash = interpolate(local, [0, 2, 12], [0, 1, 0], clamp);
  const ring = interpolate(local, [0, 26], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  return (
    <g>
      <circle cx={x} cy={y} r={ring * 1400} fill="none" stroke="#FFFFFF" strokeWidth={60 * (1 - ring) + 4} opacity={1 - ring} />
      <circle cx={x} cy={y} r={ring * 520} fill="#FFB347" opacity={(1 - ring) * 0.8} />
      {Array.from({ length: 16 }).map((_, i) => {
        const a = (i / 16) * Math.PI * 2 + rnd(i);
        const d = ring * (300 + rnd(i + 4) * 600);
        return (
          <rect
            key={i}
            x={x + Math.cos(a) * d}
            y={y + Math.sin(a) * d - ring * 200 + ring * ring * 400}
            width={26 + rnd(i) * 30}
            height={20 + rnd(i + 1) * 24}
            fill="#5A4636"
            stroke={INK}
            strokeWidth={4}
            transform={`rotate(${local * 12 + i * 30} ${x + Math.cos(a) * d} ${y + Math.sin(a) * d})`}
            opacity={1 - ring * 0.6}
          />
        );
      })}
      <rect width={W} height={H} fill="#FFFFFF" opacity={flash} />
    </g>
  );
};

const MoneyRain: React.FC<{ f: number }> = ({ f }) => (
  <g>
    {Array.from({ length: 26 }).map((_, i) => {
      const y = ((f * (6 + rnd(i) * 6) + rnd(i + 9) * H) % (H + 200)) - 200;
      const x = rnd(i + 3) * W + Math.sin(f / 10 + i) * 40;
      return (
        <g key={i} transform={`translate(${x} ${y}) rotate(${Math.sin(f / 8 + i) * 40})`}>
          <rect x={-60} y={-30} width={120} height={60} rx={6} fill="#5DBB63" stroke={INK} strokeWidth={5} />
          <circle r={18} fill="#8FD694" stroke={INK} strokeWidth={4} />
          <text y={9} textAnchor="middle" fontFamily="ZyloHead" fontWeight={900} fontSize={24} fill={INK}>
            $
          </text>
        </g>
      );
    })}
  </g>
);

const Precip: React.FC<{ f: number; kind: 'rain' | 'snow' }> = ({ f, kind }) => (
  <g>
    {Array.from({ length: kind === 'rain' ? 90 : 70 }).map((_, i) => {
      const speed = kind === 'rain' ? 38 : 4 + rnd(i) * 3;
      const y = ((f * speed + rnd(i) * H) % H);
      const x = (rnd(i + 5) * W + (kind === 'snow' ? Math.sin(f / 15 + i) * 30 : -y * 0.15)) % W;
      return kind === 'rain' ? (
        <line key={i} x1={x} y1={y} x2={x - 10} y2={y + 60} stroke="#A9C8FF" strokeWidth={4} opacity={0.7} />
      ) : (
        <circle key={i} cx={x} cy={y} r={4 + rnd(i) * 6} fill="#FFFFFF" opacity={0.9} />
      );
    })}
  </g>
);

const Ufo: React.FC<{ f: number; x: number; beam: boolean }> = ({ f, x, beam }) => {
  const y = 520 + Math.sin(f / 12) * 20;
  return (
    <g transform={`translate(${x} ${y})`}>
      {beam && <path d="M -70 30 L 70 30 L 300 1100 L -300 1100 Z" fill="#B6FF7A" opacity={0.25 + 0.1 * Math.sin(f / 3)} />}
      <ellipse cx={0} cy={0} rx={220} ry={60} fill="#B9C2D0" stroke={INK} strokeWidth={8} />
      <path d="M -100 -20 Q 0 -150 100 -20 Z" fill="#8FE3FF" stroke={INK} strokeWidth={8} />
      {[-140, -70, 0, 70, 140].map((dx, i) => (
        <circle key={dx} cx={dx} cy={14} r={14} fill={(Math.floor(f / 5) + i) % 2 ? '#FFD400' : '#FF6B4A'} stroke={INK} strokeWidth={4} />
      ))}
    </g>
  );
};

export const FxLayer: React.FC<{ fx: FxSpec[]; f: number; fps: number }> = ({ fx, f, fps }) => (
  <g>
    {fx.map((e, i) => {
      switch (e.type) {
        case 'meteor':
          return <Meteor key={i} f={f} fps={fps} x={e.x ?? 560} y={e.y ?? 1300} hitAt={e.hitAt ?? 1.2} size={e.size ?? 1} />;
        case 'impact':
          return <Impact key={i} f={f} fps={fps} x={e.x ?? 560} y={e.y ?? 1300} at={e.at ?? 0} />;
        case 'moneyRain':
          return <MoneyRain key={i} f={f} />;
        case 'rain':
          return <Precip key={i} f={f} kind="rain" />;
        case 'snow':
          return <Precip key={i} f={f} kind="snow" />;
        case 'aurora': {
          const cols = e.colors ?? ['#3DFFB0', '#2FD3FF', '#C04BFF'];
          const base = e.y ?? 760;
          return (
            <g key={i} style={{ mixBlendMode: 'screen' }} opacity={e.strength ?? 0.8}>
              <defs>
                {cols.map((c, k) => (
                  <linearGradient key={k} id={`aur${i}_${k}`} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0" stopColor={c} stopOpacity={0} />
                    <stop offset="0.75" stopColor={c} stopOpacity={0.75} />
                    <stop offset="1" stopColor={c} stopOpacity={0} />
                  </linearGradient>
                ))}
              </defs>
              {cols.map((_, k) => {
                const pts: string[] = [];
                const yb = base - k * 140;
                for (let x = -40; x <= W + 40; x += 40) {
                  const w = Math.sin(x / 170 + f / 22 + k * 1.7) * 60 + Math.sin(x / 63 - f / 15 + k) * 22;
                  pts.push(`${x},${yb + w}`);
                }
                const top = pts.map((pt) => {
                  const [x, y] = pt.split(',').map(Number);
                  return `${x},${y - 420 - Math.sin(x / 90 + f / 30 + k) * 50}`;
                }).reverse();
                return <polygon key={k} points={[...pts, ...top].join(' ')} fill={`url(#aur${i}_${k})`} />;
              })}
            </g>
          );
        }
        case 'alarm':
          return <rect key={i} width={W} height={H} fill="#FF2D2D" opacity={0.18 + 0.14 * Math.sin(f / 4)} />;
        case 'glitch':
          return (
            <g key={i} opacity={f % 9 < 3 ? 1 : 0}>
              {[0, 1, 2].map((k) => (
                <rect key={k} x={0} y={rnd(Math.floor(f / 3) + k) * H} width={W} height={20 + rnd(f + k) * 60} fill={k ? '#2FFFE0' : '#FF2D8A'} opacity={0.45} />
              ))}
            </g>
          );
        case 'ufo':
          return <Ufo key={i} f={f} x={e.x ?? 540} beam={e.beam ?? true} />;
        case 'speedLines':
          return (
            <g key={i} opacity={0.5}>
              {Array.from({ length: 30 }).map((_, k) => {
                const a = (k / 30) * Math.PI * 2;
                const r0 = 520 + ((f * 20 + k * 40) % 200);
                return (
                  <line key={k} x1={540 + Math.cos(a) * r0} y1={900 + Math.sin(a) * r0} x2={540 + Math.cos(a) * 1500} y2={900 + Math.sin(a) * 1500} stroke="#FFFFFF" strokeWidth={6 + (k % 3) * 4} />
                );
              })}
            </g>
          );
        case 'throwObj': {
          const st = (e.at ?? 0) * fps;
          const p = interpolate(f, [st, st + (e.dur ?? 0.8) * fps], [0, 1], clamp);
          if (f < st || p >= 1) return null;
          const x = e.from[0] + (e.to[0] - e.from[0]) * p;
          const y = e.from[1] + (e.to[1] - e.from[1]) * p - Math.sin(Math.PI * p) * 420;
          return (
            <g key={i} transform={`translate(${x} ${y}) rotate(${p * 900})`}>
              <rect x={-26} y={-44} width={52} height={88} rx={10} fill="#1D1F2B" stroke={INK} strokeWidth={6} />
              <rect x={-18} y={-34} width={36} height={62} rx={4} fill="#7FD3FF" />
            </g>
          );
        }
        case 'glow':
          return (
            <g key={i}>
              <defs>
                <radialGradient id={`glow${i}`}>
                  <stop offset="0" stopColor="rgba(255,240,170,0.9)" />
                  <stop offset="1" stopColor="rgba(255,212,0,0)" />
                </radialGradient>
              </defs>
              <circle cx={e.x} cy={e.y} r={(e.r ?? 260) * (1 + Math.sin(f / 4) * 0.05)} fill={`url(#glow${i})`} />
            </g>
          );
        case 'comet': {
          if (e.inside) {
            return (
              <g key={i}>
                <defs>
                  <linearGradient id={`haze${i}`} x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0" stopColor="rgba(120,255,220,0.42)" />
                    <stop offset="0.5" stopColor="rgba(90,170,255,0.22)" />
                    <stop offset="1" stopColor="rgba(120,255,220,0)" />
                  </linearGradient>
                </defs>
                <rect width={W} height={H} fill={`url(#haze${i})`} opacity={0.75 + 0.25 * Math.sin(f / 9)} />
                {Array.from({ length: 26 }).map((_, k) => (
                  <line key={k} x1={(rnd(k + 40) * 1.6 - 0.3) * W + f * 2} y1={rnd(k + 70) * H * 0.6 - 200} x2={(rnd(k + 40) * 1.6 - 0.3) * W + f * 2 + 420} y2={rnd(k + 70) * H * 0.6 + 120} stroke="#CFFFF1" strokeWidth={3} opacity={0.25} strokeLinecap="round" />
                ))}
              </g>
            );
          }
          const cx = e.x ?? 760;
          const cy = e.y ?? 420;
          const ang = e.angle ?? 205;
          const len = (e.length ?? 900) * (1 + Math.sin(f / 14) * 0.02);
          const sz = e.size ?? 1;
          return (
            <g key={i} transform={`translate(${cx} ${cy}) rotate(${ang})`}>
              <defs>
                <linearGradient id={`ion${i}`} x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0" stopColor="rgba(140,220,255,0.95)" />
                  <stop offset="1" stopColor="rgba(140,220,255,0)" />
                </linearGradient>
                <linearGradient id={`dust${i}`} x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0" stopColor="rgba(255,244,200,0.9)" />
                  <stop offset="1" stopColor="rgba(255,244,200,0)" />
                </linearGradient>
                <radialGradient id={`coma${i}`}>
                  <stop offset="0" stopColor="#FFFFFF" />
                  <stop offset="0.4" stopColor="rgba(200,255,250,0.9)" />
                  <stop offset="1" stopColor="rgba(140,220,255,0)" />
                </radialGradient>
              </defs>
              <path d={`M 0 ${-34 * sz} L ${len} ${-110 * sz} L ${len} ${110 * sz} L 0 ${34 * sz} Z`} fill={`url(#dust${i})`} transform="rotate(-7)" />
              <path d={`M 0 ${-18 * sz} L ${len * 1.15} ${-40 * sz} L ${len * 1.15} ${40 * sz} L 0 ${18 * sz} Z`} fill={`url(#ion${i})`} />
              <circle r={90 * sz * (1 + Math.sin(f / 6) * 0.05)} fill={`url(#coma${i})`} />
              <circle r={22 * sz} fill="#FFFFFF" />
            </g>
          );
        }
        case 'clouds': {
          const base = e.y ?? 700;
          const col = e.color ?? '#3A4166';
          return (
            <g key={i}>
              <rect x={0} y={0} width={W} height={base - 120} fill={col} opacity={0.92} />
              {Array.from({ length: 9 }).map((_, k) => (
                <circle key={k} cx={((k * 160 + f * 1.2) % (W + 320)) - 160} cy={base - 120 + rnd(k + 5) * 60} r={130 + rnd(k + 9) * 70} fill={col} opacity={0.97} />
              ))}
            </g>
          );
        }
        case 'vignette':
          return (
            <g key={i}>
              <defs>
                <radialGradient id="vig">
                  <stop offset="0.55" stopColor="rgba(0,0,0,0)" />
                  <stop offset="1" stopColor={e.color ?? 'rgba(0,0,0,0.7)'} />
                </radialGradient>
              </defs>
              <rect width={W} height={H} fill="url(#vig)" />
            </g>
          );
      }
      return null;
    })}
  </g>
);
