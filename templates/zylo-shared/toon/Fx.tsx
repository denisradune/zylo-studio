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
  | { type: 'vignette'; color?: string };

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
