import React from 'react';
import { INK } from './Character';

/**
 * Flat, code-drawn sets in a 1080x1920 canvas. Characters stand on the floor line at
 * FLOOR_Y. Every set takes a time of day and, where it makes sense, a damage level, so
 * one location can carry a whole story arc (calm street -> burning street).
 */

export const W = 1080;
export const H = 1920;
export const FLOOR_Y = 1480;

export type TimeOfDay = 'day' | 'dusk' | 'night';
export type SetName = 'room' | 'street' | 'sky' | 'space' | 'news' | 'store' | 'wasteland' | 'lab' | 'burst';

export type SetSpec = {
  type: SetName;
  time?: TimeOfDay;
  /** 0 = intact, 1 = damaged, 2 = ruined (street, room, store). */
  damage?: number;
  /** burst/news: main colour; news: headline text on the banner. */
  color?: string;
  headline?: string;
};

const SKY: Record<TimeOfDay, [string, string]> = {
  day: ['#7EC8FF', '#D7F0FF'],
  dusk: ['#3B2E6E', '#FF9A5C'],
  night: ['#0B1026', '#1F2D5C'],
};

// Deterministic pseudo-random so the same set always draws the same windows and stars.
const rnd = (i: number) => {
  const x = Math.sin(i * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
};

const Sky: React.FC<{ time: TimeOfDay; t: number; id: string }> = ({ time, t, id }) => (
  <>
    <defs>
      <linearGradient id={`sky-${id}`} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor={SKY[time][0]} />
        <stop offset="1" stopColor={SKY[time][1]} />
      </linearGradient>
    </defs>
    <rect width={W} height={H} fill={`url(#sky-${id})`} />
    {time === 'night' &&
      Array.from({ length: 70 }).map((_, i) => (
        <circle key={i} cx={rnd(i) * W} cy={rnd(i + 99) * H * 0.55} r={rnd(i + 7) * 3 + 1} fill="#FFFFFF" opacity={0.4 + 0.6 * Math.abs(Math.sin(t / 20 + i))} />
      ))}
    {time === 'night' ? (
      <circle cx={820} cy={300} r={70} fill="#F4F1DE" stroke={INK} strokeWidth={6} />
    ) : (
      <circle cx={820} cy={time === 'dusk' ? 820 : 300} r={90} fill={time === 'dusk' ? '#FFC36B' : '#FFE27A'} />
    )}
    {time !== 'night' &&
      [0, 1, 2].map((i) => {
        const x = ((rnd(i) * W + t * (0.4 + i * 0.2)) % (W + 400)) - 200;
        return (
          <g key={i} transform={`translate(${x} ${180 + i * 150})`} opacity={0.9}>
            <ellipse cx={0} cy={0} rx={110} ry={38} fill="#FFFFFF" />
            <ellipse cx={-60} cy={10} rx={70} ry={30} fill="#FFFFFF" />
            <ellipse cx={70} cy={12} rx={80} ry={28} fill="#FFFFFF" />
          </g>
        );
      })}
  </>
);

const Skyline: React.FC<{ y: number; color: string; lit: boolean; seed: number; scale?: number; damage?: number }> = ({ y, color, lit, seed, scale = 1, damage = 0 }) => {
  const blocks = [];
  let x = -20;
  let i = 0;
  while (x < W + 20) {
    const w = (110 + rnd(seed + i) * 120) * scale;
    const h = (260 + rnd(seed + i + 50) * 420) * scale * (damage > 1 ? 0.55 + rnd(i) * 0.3 : 1);
    blocks.push({ x, w, h, i });
    x += w + 8 * scale;
    i++;
  }
  return (
    <g>
      {blocks.map((b) => (
        <g key={b.i}>
          {damage > 1 ? (
            <path
              d={`M ${b.x} ${y} L ${b.x} ${y - b.h} L ${b.x + b.w * 0.3} ${y - b.h + 40} L ${b.x + b.w * 0.55} ${y - b.h - 20} L ${b.x + b.w * 0.8} ${y - b.h + 60} L ${b.x + b.w} ${y - b.h + 10} L ${b.x + b.w} ${y} Z`}
              fill={color}
              stroke={INK}
              strokeWidth={5}
            />
          ) : (
            <rect x={b.x} y={y - b.h} width={b.w} height={b.h} fill={color} stroke={INK} strokeWidth={5} />
          )}
          {Array.from({ length: Math.floor(b.h / (60 * scale)) }).map((_, r) =>
            [0, 1, 2].map((c) => {
              const on = lit ? rnd(seed + b.i * 31 + r * 7 + c) > 0.35 : false;
              const broken = damage > 0 && rnd(b.i * 13 + r * 5 + c) > 0.6;
              return (
                <rect
                  key={`${r}-${c}`}
                  x={b.x + (14 + c * (b.w - 28) / 3) * 1}
                  y={y - b.h + 24 * scale + r * 60 * scale}
                  width={(b.w - 56) / 3}
                  height={30 * scale}
                  fill={broken ? '#1A1A22' : on ? '#FFD86B' : 'rgba(255,255,255,0.18)'}
                  stroke={broken ? INK : 'none'}
                  strokeWidth={3}
                />
              );
            }),
          )}
        </g>
      ))}
    </g>
  );
};

const Fire: React.FC<{ x: number; y: number; s: number; t: number }> = ({ x, y, s, t }) => {
  const f = Math.sin(t / 2.5 + x) * 0.12;
  return (
    <g transform={`translate(${x} ${y}) scale(${s * (1 + f)} ${s * (1 - f)})`}>
      <path d="M 0 0 Q -60 -40 -30 -120 Q -10 -80 0 -170 Q 20 -90 40 -130 Q 70 -40 0 0 Z" fill="#FF6A2B" stroke={INK} strokeWidth={5} />
      <path d="M 0 -6 Q -30 -30 -14 -80 Q 0 -60 6 -110 Q 18 -60 26 -84 Q 40 -30 0 -6 Z" fill="#FFD400" />
    </g>
  );
};

const Smoke: React.FC<{ x: number; y: number; t: number }> = ({ x, y, t }) => (
  <g opacity={0.75}>
    {[0, 1, 2, 3].map((i) => {
      const p = ((t / 40 + i / 4) % 1);
      return <circle key={i} cx={x + Math.sin(p * 6 + i) * 30} cy={y - p * 520} r={50 + p * 90} fill="#4A4652" opacity={1 - p} />;
    })}
  </g>
);

const Room: React.FC<{ time: TimeOfDay; t: number; damage: number }> = ({ time, t, damage }) => (
  <g>
    <rect width={W} height={H} fill={time === 'night' ? '#2C2A44' : '#F2D7A6'} />
    {/* window */}
    <g transform="translate(140 300)">
      <svg width={520} height={560} viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid slice">
        <Sky time={time} t={t} id="room" />
        <Skyline y={H} color={time === 'night' ? '#1E2240' : '#8FA3C7'} lit={time !== 'day'} seed={3} />
      </svg>
      <rect width={520} height={560} fill="none" stroke={INK} strokeWidth={14} />
      <line x1={260} y1={0} x2={260} y2={560} stroke={INK} strokeWidth={10} />
      <line x1={0} y1={280} x2={520} y2={280} stroke={INK} strokeWidth={10} />
      {damage > 0 && <path d="M 300 60 L 360 180 L 330 230 L 420 330 M 360 180 L 450 150" stroke="#FFFFFF" strokeWidth={6} fill="none" />}
    </g>
    {/* poster */}
    <g transform="translate(800 420) rotate(4)">
      <rect width={130} height={175} fill="#FFD400" stroke={INK} strokeWidth={7} />
      <path d="M 34 46 H 96 L 34 130 H 96" fill="none" stroke={INK} strokeWidth={14} strokeLinejoin="round" />
    </g>
    {/* floor */}
    <rect y={FLOOR_Y - 20} width={W} height={H - FLOOR_Y + 20} fill={time === 'night' ? '#3B2F2A' : '#B9835A'} stroke={INK} strokeWidth={8} />
    {/* desk with laptop */}
    <g transform="translate(620 1120)">
      <rect x={0} y={150} width={420} height={36} fill="#8A5A3C" stroke={INK} strokeWidth={8} />
      <rect x={30} y={186} width={30} height={190} fill="#6E4630" stroke={INK} strokeWidth={8} />
      <rect x={360} y={186} width={30} height={190} fill="#6E4630" stroke={INK} strokeWidth={8} />
      <path d="M 120 150 L 150 20 L 330 20 L 300 150 Z" fill="#2B2E3D" stroke={INK} strokeWidth={8} strokeLinejoin="round" />
      <path d="M 162 36 L 316 36 L 292 136 L 140 136 Z" fill={time === 'night' ? '#7FD3FF' : '#BFE8FF'} />
      <rect x={90} y={140} width={260} height={14} rx={6} fill="#3A3E52" stroke={INK} strokeWidth={6} />
    </g>
    {time === 'night' && <ellipse cx={830} cy={1150} rx={220} ry={160} fill="#7FD3FF" opacity={0.1} />}
  </g>
);

const Street: React.FC<{ time: TimeOfDay; t: number; damage: number }> = ({ time, t, damage }) => (
  <g>
    <Sky time={damage > 1 ? 'dusk' : time} t={t} id="street" />
    <Skyline y={1180} color={time === 'night' ? '#252B52' : '#9DB2D6'} lit={time !== 'day'} seed={11} scale={0.7} damage={damage} />
    <Skyline y={1330} color={time === 'night' ? '#343A6B' : '#E6A57E'} lit={time !== 'day'} seed={23} damage={damage} />
    {/* sidewalk + road */}
    <rect y={1330} width={W} height={180} fill="#B8B4AE" stroke={INK} strokeWidth={8} />
    <rect y={1510} width={W} height={H - 1510} fill="#3C3D47" stroke={INK} strokeWidth={8} />
    {[0, 1, 2, 3].map((i) => (
      <rect key={i} x={i * 300 + 40} y={1690} width={170} height={22} rx={8} fill="#F2F2F2" />
    ))}
    {/* lamp post */}
    <g transform="translate(110 900)">
      <rect x={-10} y={0} width={20} height={440} fill="#2E3040" stroke={INK} strokeWidth={6} />
      <path d="M 0 0 Q 0 -40 60 -40" fill="none" stroke={INK} strokeWidth={14} />
      <rect x={40} y={-40} width={70} height={30} rx={10} fill={time === 'day' ? '#DADADA' : '#FFE68A'} stroke={INK} strokeWidth={6} />
      {time !== 'day' && <path d="M 45 -10 L 105 -10 L 160 300 L -10 300 Z" fill="#FFE68A" opacity={0.15} />}
    </g>
    {damage > 0 && (
      <>
        <Smoke x={300} y={1150} t={t} />
        <Smoke x={820} y={1100} t={t + 20} />
        <Fire x={260} y={1335} s={1.1} t={t} />
        <Fire x={860} y={1335} s={0.9} t={t + 5} />
        {/* overturned car */}
        <g transform="translate(560 1560) rotate(-12)">
          <rect x={0} y={0} width={300} height={110} rx={30} fill="#D9443A" stroke={INK} strokeWidth={8} />
          <rect x={50} y={-60} width={180} height={70} rx={20} fill="#D9443A" stroke={INK} strokeWidth={8} />
          <circle cx={70} cy={115} r={34} fill="#2B2B2B" stroke={INK} strokeWidth={8} />
          <circle cx={230} cy={115} r={34} fill="#2B2B2B" stroke={INK} strokeWidth={8} />
        </g>
      </>
    )}
  </g>
);

const SkySet: React.FC<{ time: TimeOfDay; t: number }> = ({ time, t }) => (
  <g>
    <Sky time={time} t={t} id="skyset" />
    <path d={`M 0 1500 Q 270 1400 540 1460 Q 810 1520 1080 1430 L 1080 ${H} L 0 ${H} Z`} fill={time === 'night' ? '#1B2A36' : '#6DBE6A'} stroke={INK} strokeWidth={8} />
    <Skyline y={1520} color={time === 'night' ? '#252B52' : '#9DB2D6'} lit={time !== 'day'} seed={41} scale={0.45} />
    <rect y={1520} width={W} height={H - 1520} fill={time === 'night' ? '#16212B' : '#5AA557'} />
  </g>
);

const Space: React.FC<{ t: number }> = ({ t }) => (
  <g>
    <rect width={W} height={H} fill="#070914" />
    {Array.from({ length: 160 }).map((_, i) => (
      <circle key={i} cx={rnd(i) * W} cy={rnd(i + 300) * H} r={rnd(i + 3) * 2.6 + 0.6} fill="#FFFFFF" opacity={0.3 + 0.7 * Math.abs(Math.sin(t / 25 + i))} />
    ))}
    <g transform={`translate(540 ${2350 - t * 0.15})`}>
      <circle r={900} fill="#2F6BFF" stroke={INK} strokeWidth={10} />
      <path d="M -500 -560 Q -300 -720 -60 -640 Q 60 -560 -60 -470 Q -260 -420 -420 -470 Z" fill="#4CC36B" stroke={INK} strokeWidth={8} />
      <path d="M 200 -760 Q 420 -700 520 -560 Q 380 -500 240 -560 Z" fill="#4CC36B" stroke={INK} strokeWidth={8} />
      <circle r={930} fill="none" stroke="#8FD3FF" strokeWidth={24} opacity={0.35} />
    </g>
  </g>
);

const News: React.FC<{ t: number; color?: string; headline?: string }> = ({ t, color = '#D9443A', headline = 'BREAKING NEWS' }) => (
  <g>
    <rect width={W} height={H} fill="#1B2140" />
    {Array.from({ length: 12 }).map((_, i) => (
      <rect key={i} x={i * 90} y={0} width={46} height={H} fill="#222A52" />
    ))}
    {/* desk */}
    <path d="M 60 1340 L 1020 1340 L 960 1620 L 120 1620 Z" fill="#E9E9EF" stroke={INK} strokeWidth={10} strokeLinejoin="round" />
    <rect x={60} y={1320} width={960} height={40} fill="#C9CAD6" stroke={INK} strokeWidth={8} />
    {/* banner */}
    <g transform="translate(0 1640)">
      <rect width={W} height={110} fill={color} stroke={INK} strokeWidth={8} />
      <text x={40} y={76} fontFamily="ZyloHead" fontWeight={900} fontSize={54} fill="#FFFFFF">
        {headline}
      </text>
      <rect y={110} width={W} height={70} fill="#FFD400" stroke={INK} strokeWidth={8} />
      <text x={W - ((t * 6) % (W + 1400))} y={158} fontFamily="ZyloBody" fontWeight={900} fontSize={36} fill={INK}>
        STAY INDOORS • OFFICIALS URGE CALM • SCIENTISTS BAFFLED • MORE AT 11 •
      </text>
    </g>
    <circle cx={980} cy={120} r={22} fill="#FF3B3B" opacity={Math.sin(t / 5) > 0 ? 1 : 0.3} />
    <text x={900} y={136} textAnchor="end" fontFamily="ZyloBody" fontWeight={900} fontSize={40} fill="#FFFFFF">
      LIVE
    </text>
  </g>
);

const Store: React.FC<{ damage: number }> = ({ damage }) => (
  <g>
    <rect width={W} height={H} fill="#EDEFF3" />
    {[0, 1].map((col) => (
      <g key={col} transform={`translate(${col === 0 ? 40 : 580} 380)`}>
        <rect width={460} height={1000} fill="#C9CED8" stroke={INK} strokeWidth={8} />
        {[0, 1, 2, 3].map((r) => (
          <g key={r}>
            <rect x={0} y={220 + r * 230} width={460} height={20} fill="#8B93A5" stroke={INK} strokeWidth={6} />
            {Array.from({ length: 6 }).map((_, k) => {
              const gone = damage > 0 ? rnd(col * 40 + r * 9 + k) < 0.4 + damage * 0.3 : false;
              const colors = ['#FF6B4A', '#2F6BFF', '#2DBE7E', '#FFD400', '#B05CFF'];
              return gone ? null : (
                <rect
                  key={k}
                  x={16 + k * 74}
                  y={220 + r * 230 - 110 - rnd(k + r) * 40}
                  width={58}
                  height={110 + rnd(k + r) * 40}
                  rx={8}
                  fill={colors[(k + r + col) % colors.length]}
                  stroke={INK}
                  strokeWidth={5}
                />
              );
            })}
          </g>
        ))}
      </g>
    ))}
    <rect y={FLOOR_Y - 20} width={W} height={H - FLOOR_Y + 20} fill="#D5D8DE" stroke={INK} strokeWidth={8} />
  </g>
);

const Wasteland: React.FC<{ t: number }> = ({ t }) => (
  <g>
    <defs>
      <linearGradient id="waste" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#5B3A2E" />
        <stop offset="1" stopColor="#E08A4F" />
      </linearGradient>
    </defs>
    <rect width={W} height={H} fill="url(#waste)" />
    <circle cx={540} cy={700} r={160} fill="#FFB36B" opacity={0.6} />
    <Skyline y={1380} color="#3B2A2A" lit={false} seed={77} scale={0.8} damage={2} />
    <rect y={1370} width={W} height={H - 1370} fill="#8C5A3C" stroke={INK} strokeWidth={8} />
    <Smoke x={200} y={1300} t={t} />
    <Smoke x={900} y={1250} t={t + 13} />
    <Fire x={720} y={1385} s={0.8} t={t} />
  </g>
);

const Lab: React.FC<{ t: number }> = ({ t }) => (
  <g>
    <rect width={W} height={H} fill="#DDE7EE" />
    <rect x={80} y={300} width={600} height={420} rx={10} fill="#FFFFFF" stroke={INK} strokeWidth={10} />
    <path d="M 130 620 L 260 500 L 380 560 L 520 380 L 640 420" fill="none" stroke="#D9443A" strokeWidth={10} strokeLinejoin="round" />
    <text x={130} y={380} fontFamily="ZyloBody" fontWeight={900} fontSize={40} fill={INK}>
      E = mc² ???
    </text>
    {[0, 1].map((i) => (
      <g key={i} transform={`translate(${740 + i * 140} 860)`}>
        <rect x={0} y={0} width={110} height={170} rx={12} fill="#2B2E3D" stroke={INK} strokeWidth={8} />
        <rect x={12} y={14} width={86} height={110} fill={i ? '#7CFFB2' : '#7FD3FF'} opacity={0.6 + 0.4 * Math.abs(Math.sin(t / 10 + i))} />
      </g>
    ))}
    <rect y={FLOOR_Y - 20} width={W} height={H - FLOOR_Y + 20} fill="#AFC0CC" stroke={INK} strokeWidth={8} />
  </g>
);

/** Comic sunburst for "concept" shots (rules, numbers, punchlines). */
const Burst: React.FC<{ color?: string; t: number }> = ({ color = '#FFD400', t }) => (
  <g>
    <rect width={W} height={H} fill={color} />
    <g transform={`translate(540 860) rotate(${t * 0.3})`} opacity={0.18}>
      {Array.from({ length: 18 }).map((_, i) => (
        <path key={i} d="M 0 0 L -120 -1600 L 120 -1600 Z" fill="#FFFFFF" transform={`rotate(${i * 20})`} />
      ))}
    </g>
    <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="11" cy="11" r="3.2" fill="rgba(0,0,0,0.08)" />
    </pattern>
    <rect width={W} height={H} fill="url(#dots)" />
  </g>
);

export const SetPiece: React.FC<{ spec: SetSpec; t: number }> = ({ spec, t }) => {
  const time = spec.time ?? 'day';
  const damage = spec.damage ?? 0;
  switch (spec.type) {
    case 'room':
      return <Room time={time} t={t} damage={damage} />;
    case 'street':
      return <Street time={time} t={t} damage={damage} />;
    case 'sky':
      return <SkySet time={time} t={t} />;
    case 'space':
      return <Space t={t} />;
    case 'news':
      return <News t={t} color={spec.color} headline={spec.headline} />;
    case 'store':
      return <Store damage={damage} />;
    case 'wasteland':
      return <Wasteland t={t} />;
    case 'lab':
      return <Lab t={t} />;
    case 'burst':
      return <Burst color={spec.color} t={t} />;
  }
};

export { Fire, Smoke, rnd };
