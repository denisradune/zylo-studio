import React from 'react';
import { interpolate, Easing } from 'remotion';
import { INK } from './Character';
import { rnd } from './Backgrounds';

/**
 * Code-drawn "satisfying" loops for the bottom half of split-screen Shorts (1080x960). Original animation —
 * never footage from other creators. Kinds rotate per part so consecutive Shorts look different.
 */
export type SatisfyingKind = 'press' | 'sand' | 'marbles';
export const SAT_W = 1080;
export const SAT_H = 960;

const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;
const COLORS = ['#FF4D6D', '#FFD400', '#2DBE7E', '#2F6BFF', '#B05CFF', '#FF8A3D', '#3FD0E0'];

const Hazard: React.FC<{ x: number; y: number; w: number; h: number; id: string }> = ({ x, y, w, h, id }) => (
  <g>
    <defs>
      <pattern id={`hz-${id}`} width="60" height="60" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
        <rect width="30" height="60" fill="#FFD400" />
        <rect x="30" width="30" height="60" fill={INK} />
      </pattern>
    </defs>
    <rect x={x} y={y} width={w} height={h} fill={`url(#hz-${id})`} stroke={INK} strokeWidth={8} />
  </g>
);

/** Hydraulic press: the head comes down, the object squashes and splats, the head goes back up. */
const Press: React.FC<{ f: number; fps: number; seed: number }> = ({ f, fps, seed }) => {
  const T = Math.round(2.8 * fps);
  const cycle = Math.floor(f / T);
  const p = (f % T) / T;
  const baseTop = 720;
  const objH = 230;
  const objTop = baseTop - objH;
  const down = interpolate(p, [0, 0.38], [0, 1], { ...clamp, easing: Easing.in(Easing.cubic) });
  const squash = interpolate(p, [0.38, 0.55], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const up = interpolate(p, [0.66, 1], [0, 1], { ...clamp, easing: Easing.inOut(Easing.sin) });
  const headBottomRest = 170;
  const headBottomContact = objTop;
  const headBottomCrushed = baseTop - objH * 0.12;
  let headBottom = headBottomRest + (headBottomContact - headBottomRest) * down;
  if (p >= 0.38) headBottom = headBottomContact + (headBottomCrushed - headBottomContact) * squash;
  if (p >= 0.66) headBottom = headBottomCrushed + (headBottomRest - headBottomCrushed) * up;
  const crushed = Math.max(0.12, Math.min(1, (baseTop - Math.max(headBottom, objTop)) / objH));
  const k = (1 - crushed) / 0.88; // 0 intact -> 1 flat
  const kind = Math.floor(rnd(cycle * 7 + seed) * 4);
  const c1 = COLORS[(cycle + seed) % COLORS.length];
  const c2 = COLORS[(cycle + seed + 3) % COLORS.length];
  const sx = 1 + k * 0.9;
  const h = objH * crushed;
  const w = 260 * sx;
  const left = 540 - w / 2;
  const top = baseTop - h;
  const splat = p > 0.42 && p < 0.9 ? interpolate(p, [0.42, 0.6], [0, 1], clamp) : p >= 0.9 ? 1 : 0;
  return (
    <g>
      <rect width={SAT_W} height={SAT_H} fill="#C9CED8" />
      <rect y={SAT_H - 260} width={SAT_W} height={260} fill="#B3B9C6" />
      {/* object */}
      {kind === 0 &&
        [0, 1, 2].map((i) => (
          <rect key={i} x={left} y={top + (h / 3) * i} width={w} height={h / 3} rx={14} fill={COLORS[(cycle + i + seed) % COLORS.length]} stroke={INK} strokeWidth={7} />
        ))}
      {kind === 1 && <ellipse cx={540} cy={baseTop - h / 2} rx={w / 2} ry={h / 2} fill={c1} stroke={INK} strokeWidth={8} />}
      {kind === 2 && (
        <g>
          <rect x={left} y={top} width={w} height={h} rx={30} fill={c1} stroke={INK} strokeWidth={8} opacity={0.92} />
          <rect x={left + 24} y={top + 14} width={w * 0.25} height={Math.max(8, h * 0.4)} rx={12} fill="#FFFFFF" opacity={0.45} />
        </g>
      )}
      {kind === 3 && (
        <g>
          <rect x={left} y={top} width={w} height={h} rx={18} fill="#D9DDE4" stroke={INK} strokeWidth={8} />
          <rect x={left} y={top + h * 0.3} width={w} height={h * 0.4} fill={c2} stroke={INK} strokeWidth={6} />
        </g>
      )}
      {/* splats */}
      {splat > 0 &&
        Array.from({ length: 10 }).map((_, i) => {
          const dir = i % 2 ? 1 : -1;
          const dist = 120 + rnd(cycle * 31 + i) * 260;
          const x = 540 + dir * (w / 2 + dist * splat * 0.6);
          const y = baseTop - 20 - rnd(i + cycle) * 60 * (1 - splat) + splat * 10;
          return <circle key={i} cx={x} cy={y} r={10 + rnd(i * 3 + cycle) * 16} fill={i % 3 ? c1 : c2} stroke={INK} strokeWidth={4} opacity={1 - Math.max(0, (p - 0.85) * 6)} />;
        })}
      {/* base */}
      <Hazard x={300} y={baseTop} w={480} h={110} id="base" />
      <rect x={260} y={baseTop + 110} width={560} height={60} rx={10} fill="#3A3F4F" stroke={INK} strokeWidth={8} />
      {/* head */}
      <rect x={470} y={-20} width={140} height={headBottom - 120} fill="#5A6070" stroke={INK} strokeWidth={8} />
      <rect x={340} y={headBottom - 150} width={400} height={50} rx={8} fill="#3A3F4F" stroke={INK} strokeWidth={8} />
      <Hazard x={360} y={headBottom - 100} w={360} h={100} id="head" />
    </g>
  );
};

/** Kinetic sand: a striped block slides under a knife; each slice peels off and falls. */
const Sand: React.FC<{ f: number; fps: number; seed: number }> = ({ f, fps, seed }) => {
  const T = Math.round(1.1 * fps);
  const n = Math.floor(f / T);
  const p = (f % T) / T;
  const layers = [0, 1, 2, 3].map((i) => COLORS[(i * 2 + seed) % COLORS.length]);
  const knifeY = interpolate(p, [0, 0.35, 0.55, 1], [210, 640, 640, 210], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const blockTop = 330;
  const blockH = 330;
  const sliceW = 70;
  const fall = interpolate(p, [0.4, 1], [0, 1], { ...clamp, easing: Easing.in(Easing.quad) });
  const Block = ({ x, w, clip }: { x: number; w: number; clip?: string }) => (
    <g clipPath={clip}>
      {layers.map((c, i) => (
        <rect key={i} x={x} y={blockTop + (blockH / 4) * i} width={w} height={blockH / 4 + 1} fill={c} />
      ))}
      {Array.from({ length: 40 }).map((_, i) => (
        <circle key={i} cx={x + rnd(i + n) * w} cy={blockTop + rnd(i * 3) * blockH} r={2.5} fill="#FFFFFF" opacity={0.35} />
      ))}
      <rect x={x} y={blockTop} width={w} height={blockH} fill="none" stroke={INK} strokeWidth={7} />
    </g>
  );
  return (
    <g>
      <rect width={SAT_W} height={SAT_H} fill="#F3E3D3" />
      <rect y={blockTop + blockH} width={SAT_W} height={SAT_H - blockTop - blockH} fill="#E2CDB8" stroke={INK} strokeWidth={6} />
      {/* main block, sliding left one slice per cycle */}
      <Block x={540 - 20} w={520} />
      {/* the slice being cut, tipping over and falling */}
      <g transform={`translate(${540 - 20 - sliceW} 0) rotate(${-70 * fall} ${sliceW} ${blockTop + blockH}) translate(${-fall * 60} ${fall * 40})`}>
        <Block x={0} w={sliceW} />
      </g>
      {/* earlier slices piled up */}
      {Array.from({ length: Math.min(n, 6) }).map((_, i) => (
        <g key={i} transform={`translate(${120 + i * 54} ${blockTop + blockH - 40}) rotate(-90)`}>
          {layers.map((c, j) => (
            <rect key={j} x={0} y={j * 18} width={sliceW} height={18} fill={c} stroke={INK} strokeWidth={3} />
          ))}
        </g>
      ))}
      {/* knife */}
      <g transform={`translate(${540 - 20 - 6} ${knifeY - 420})`}>
        <path d="M 0 0 L 22 0 L 22 400 L 0 440 Z" fill="#E6EAF0" stroke={INK} strokeWidth={6} />
        <rect x={-10} y={-120} width={42} height={130} rx={10} fill="#2F2F3A" stroke={INK} strokeWidth={6} />
      </g>
    </g>
  );
};

/** Marbles drop through a peg board and land in coloured cups. */
const Marbles: React.FC<{ f: number; fps: number; seed: number }> = ({ f, fps, seed }) => {
  const rows = 7;
  const pegs: [number, number][] = [];
  for (let r = 0; r < rows; r++) for (let c = 0; c <= r + 3; c++) pegs.push([540 + (c - (r + 3) / 2) * 92, 150 + r * 82]);
  const balls = Array.from({ length: 9 }).map((_, i) => {
    const life = Math.round(2.6 * fps);
    const start = i * Math.round(0.3 * fps);
    const local = (f - start) % (life + Math.round(0.1 * fps));
    const id = Math.floor((f - start) / (life + Math.round(0.1 * fps))) * 9 + i;
    if (f < start || local > life) return null;
    const t = local / life;
    // zig-zag down the board: one random left/right step per row
    let x = 540;
    const steps = rows + 1;
    const pos = t * steps;
    const row = Math.min(steps - 1, Math.floor(pos));
    for (let r = 0; r < row; r++) x += (rnd(id * 13 + r + seed) < 0.5 ? -1 : 1) * 46;
    const next = x + (rnd(id * 13 + row + seed) < 0.5 ? -1 : 1) * 46;
    const fr = pos - row;
    const bx = x + (next - x) * Easing.inOut(Easing.sin)(fr);
    const by = 90 + pos * 82 - Math.sin(fr * Math.PI) * 26;
    return <circle key={i} cx={bx} cy={Math.min(by, 830)} r={22} fill={COLORS[(id + seed) % COLORS.length]} stroke={INK} strokeWidth={5} />;
  });
  return (
    <g>
      <rect width={SAT_W} height={SAT_H} fill="#1E2340" />
      {pegs.map(([x, y], i) => (
        <circle key={i} cx={x} cy={y} r={12} fill="#FFFFFF" stroke={INK} strokeWidth={4} />
      ))}
      {balls}
      {Array.from({ length: 9 }).map((_, i) => (
        <g key={i}>
          <rect x={540 + (i - 4) * 110 - 50} y={820} width={100} height={140} rx={10} fill={COLORS[(i + seed) % COLORS.length]} stroke={INK} strokeWidth={6} />
          <rect x={540 + (i - 4) * 110 - 50} y={820} width={100} height={22} fill="#FFFFFF" opacity={0.3} />
        </g>
      ))}
    </g>
  );
};

export const SatisfyingPanel: React.FC<{ kind: SatisfyingKind; f: number; fps: number; seed?: number }> = ({ kind, f, fps, seed = 0 }) => (
  <svg viewBox={`0 0 ${SAT_W} ${SAT_H}`} width="100%" height="100%">
    {kind === 'press' && (
      <g>
        <rect width={SAT_W} height={SAT_H} fill="#C9CED8" />
        <g transform="translate(540 600) scale(1.3) translate(-540 -600)">
          <Press f={f} fps={fps} seed={seed} />
        </g>
      </g>
    )}
    {kind === 'sand' && (
      <g transform="translate(540 700) scale(1.2) translate(-540 -700)">
        <Sand f={f} fps={fps} seed={seed} />
      </g>
    )}
    {kind === 'marbles' && (
      <g>
        <rect width={SAT_W} height={SAT_H} fill="#1E2340" />
        <g transform="translate(540 960) scale(1.18) translate(-540 -960)">
          <Marbles f={f} fps={fps} seed={seed} />
        </g>
      </g>
    )}
  </svg>
);
