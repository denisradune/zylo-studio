import React from 'react';
import { INK } from './Character';

/**
 * "Den": the cosy night studio of the tips format (owner's reference 2026-11-19).
 * A wall-sized window onto a lit night city, a wooden desk, a big monitor (its screen is
 * drawn by Monitor.tsx on top of this set), a plant and a desk lamp.
 * view 'close' = only the window wall behind a face close-up.
 */

export const DW = 1080;
export const DH = 1920;
/** The monitor's screen rectangle in canvas px (Monitor.tsx draws into it). */
export const SCREEN = { x: 112, y: 300, w: 856, h: 560 };
/** Top surface of the desk. */
export const DESK_Y = 1330;

const rnd = (i: number) => {
  const x = Math.sin(i * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
};

const City: React.FC<{ t: number; y0: number }> = ({ t, y0 }) => {
  const rows: React.ReactNode[] = [];
  // three layers of blocks, far (dark) to near (brighter)
  const layers = [
    { base: y0 + 520, col: '#16204A', win: '#3D63C9', seed: 5, s: 0.7 },
    { base: y0 + 760, col: '#1C2A5E', win: '#F2B84B', seed: 17, s: 1 },
    { base: y0 + 1000, col: '#22336E', win: '#FFC85A', seed: 29, s: 1.25 },
  ];
  layers.forEach((L, li) => {
    let x = -30;
    let i = 0;
    while (x < DW + 30) {
      const w = (90 + rnd(L.seed + i) * 110) * L.s;
      const h = (240 + rnd(L.seed + i + 40) * 380) * L.s;
      const top = L.base - h;
      rows.push(<rect key={`b${li}-${i}`} x={x} y={top} width={w} height={h + 400} fill={L.col} />);
      const cols = Math.max(2, Math.floor(w / (28 * L.s)));
      const rws = Math.floor(h / (40 * L.s));
      for (let r = 0; r < rws; r++)
        for (let c = 0; c < cols; c++) {
          const k = L.seed * 1000 + i * 97 + r * 13 + c;
          const on = rnd(k) > 0.55;
          if (!on) continue;
          const flick = rnd(k + 3) > 0.97 ? 0.5 + 0.5 * Math.sin(t / 9 + k) : 1;
          rows.push(
            <rect key={`w${li}-${i}-${r}-${c}`} x={x + 8 * L.s + c * (w - 16 * L.s) / cols} y={top + 16 * L.s + r * 40 * L.s} width={12 * L.s} height={16 * L.s} fill={rnd(k + 9) > 0.8 ? '#7FD3FF' : L.win} opacity={flick} />,
          );
        }
      // rooftop beacon
      if (rnd(L.seed + i + 77) > 0.7) rows.push(<rect key={`r${li}-${i}`} x={x + w / 2 - 5} y={top - 22} width={10} height={14} fill="#FF4A3D" opacity={0.5 + 0.5 * Math.sin(t / 12 + i)} />);
      x += w + 10 * L.s;
      i++;
    }
  });
  return <g>{rows}</g>;
};

const Window: React.FC<{ t: number; close?: boolean }> = ({ t, close }) => (
  <g>
    <defs>
      <linearGradient id="den-sky" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#070B22" />
        <stop offset="1" stopColor="#1B2C6B" />
      </linearGradient>
    </defs>
    <rect width={DW} height={DH} fill="url(#den-sky)" />
    {Array.from({ length: 50 }).map((_, i) => (
      <rect key={i} x={rnd(i) * DW} y={rnd(i + 99) * 520} width={4} height={4} fill="#FFFFFF" opacity={0.3 + 0.6 * Math.abs(Math.sin(t / 25 + i))} />
    ))}
    <City t={t} y0={close ? 260 : 120} />
    {/* window frame: thick wooden mullions */}
    {[0, 360, 720, 1080].map((x) => (
      <rect key={x} x={x - 22} y={0} width={44} height={DH} fill="#3A2416" />
    ))}
    <rect x={0} y={close ? 760 : 620} width={DW} height={34} fill="#3A2416" />
    <rect x={0} y={0} width={DW} height={DH} fill="#0A0E2A" opacity={0.12} />
  </g>
);

const Plant: React.FC<{ x: number; y: number; t: number }> = ({ x, y, t }) => {
  const sway = Math.sin(t / 30) * 2;
  const leaves = [
    [-150, -420, -30], [-90, -520, -12], [10, -560, 8], [110, -470, 28], [160, -360, 48], [-190, -300, -55], [70, -380, 18], [-40, -330, -20],
  ];
  return (
    <g transform={`translate(${x} ${y})`}>
      {leaves.map(([lx, ly, a], i) => (
        <g key={i} transform={`rotate(${a + sway})`}>
          <line x1={0} y1={-40} x2={lx * 0.6} y2={ly * 0.6} stroke="#2F6B2A" strokeWidth={10} />
          <path d={`M ${lx * 0.55} ${ly * 0.55} Q ${lx - 60} ${ly + 40} ${lx} ${ly - 40} Q ${lx + 60} ${ly + 40} ${lx * 0.55} ${ly * 0.55} Z`} fill={i % 2 ? '#3FA34D' : '#2E8A3E'} stroke="#173F1B" strokeWidth={6} />
          <path d={`M ${lx * 0.6} ${ly * 0.6} L ${lx} ${ly - 20}`} stroke="#6FD06A" strokeWidth={4} opacity={0.7} />
        </g>
      ))}
      <path d="M -95 -60 L 95 -60 L 75 70 L -75 70 Z" fill="#C8693A" stroke={INK} strokeWidth={8} strokeLinejoin="round" />
      <rect x={-105} y={-78} width={210} height={30} rx={6} fill="#DB7C47" stroke={INK} strokeWidth={8} />
    </g>
  );
};

const Lamp: React.FC<{ x: number; y: number }> = ({ x, y }) => (
  <g transform={`translate(${x} ${y})`}>
    <path d="M -10 0 L 260 0 L 520 230 L -260 230 Z" transform="translate(70 -150) rotate(28)" fill="#FFC46B" opacity={0.12} />
    <line x1={0} y1={0} x2={60} y2={-200} stroke="#2A2A33" strokeWidth={14} />
    <line x1={60} y1={-200} x2={150} y2={-250} stroke="#2A2A33" strokeWidth={14} />
    <path d="M 120 -290 L 210 -250 L 175 -195 Z" fill="#E8A13A" stroke={INK} strokeWidth={7} strokeLinejoin="round" />
    <circle cx={175} cy={-215} r={14} fill="#FFF3C4" />
    <ellipse cx={0} cy={6} rx={60} ry={14} fill="#2A2A33" stroke={INK} strokeWidth={6} />
  </g>
);

export const DenSet: React.FC<{ t: number; view?: 'wide' | 'close' | 'screen' }> = ({ t, view = 'wide' }) => {
  if (view === 'close') return <Window t={t} close />;
  const m = SCREEN;
  return (
    <g>
      <Window t={t} />
      {/* wall/sill under the window */}
      <rect x={0} y={1180} width={DW} height={160} fill="#2B1A12" />
      <Plant x={930} y={1300} t={t} />
      {/* monitor */}
      <rect x={m.x - 34} y={m.y - 34} width={m.w + 68} height={m.h + 68} rx={22} fill="#1A1A22" stroke={INK} strokeWidth={8} />
      <rect x={m.x - 12} y={m.y - 12} width={m.w + 24} height={m.h + 24} rx={10} fill="#0D0D13" />
      <rect x={m.x} y={m.y} width={m.w} height={m.h} rx={6} fill="#16161F" />
      <rect x={490} y={m.y + m.h + 34} width={100} height={DESK_Y - (m.y + m.h + 34)} fill="#24242E" stroke={INK} strokeWidth={7} />
      <ellipse cx={540} cy={DESK_Y + 4} rx={170} ry={26} fill="#24242E" stroke={INK} strokeWidth={7} />
      {/* screen glow */}
      <ellipse cx={540} cy={DESK_Y + 40} rx={560} ry={120} fill="#7FB3FF" opacity={0.08} />
      {/* desk */}
      <rect x={-20} y={DESK_Y} width={DW + 40} height={70} fill="#C1712F" stroke={INK} strokeWidth={8} />
      <rect x={-20} y={DESK_Y + 8} width={DW + 40} height={12} fill="#DE8C45" />
      <rect x={-20} y={DESK_Y + 70} width={DW + 40} height={DH - DESK_Y} fill="#8E4B22" stroke={INK} strokeWidth={8} />
      {[0, 1, 2, 3, 4, 5].map((i) => (
        <line key={i} x1={-20} y1={DESK_Y + 150 + i * 80} x2={DW + 20} y2={DESK_Y + 150 + i * 80} stroke="#7A3F1C" strokeWidth={6} />
      ))}
      <Lamp x={70} y={DESK_Y} />
      {/* mug */}
      <g transform={`translate(840 ${DESK_Y - 4})`}>
        <rect x={-36} y={-80} width={72} height={80} rx={10} fill="#F2F2F2" stroke={INK} strokeWidth={7} />
        <path d="M 36 -60 Q 66 -52 36 -22" fill="none" stroke={INK} strokeWidth={8} />
        <rect x={-36} y={-60} width={72} height={16} fill="#FFD400" />
        {[0, 1].map((i) => (
          <path key={i} d={`M ${-10 + i * 20} -96 q 10 -20 0 -40 q -10 -20 0 -40`} fill="none" stroke="#FFFFFF" strokeWidth={5} opacity={0.25 + 0.2 * Math.sin(t / 10 + i)} />
        ))}
      </g>
    </g>
  );
};

/**
 * Chunky-pixel look over vector art: sample one pixel per BLOCK and dilate it to a block.
 * Applied to the set and cast; monitor graphics and captions stay crisp.
 */
export const PIXEL = 6;
export const PixelFilter: React.FC<{ id?: string; size?: number }> = ({ id = 'px', size = PIXEL }) => (
  <filter id={id} x={0} y={0} width={DW} height={DH} filterUnits="userSpaceOnUse" primitiveUnits="userSpaceOnUse">
    <feFlood x={size / 2} y={size / 2} width={1} height={1} />
    <feComposite width={size} height={size} />
    <feTile result="grid" />
    <feComposite in="SourceGraphic" in2="grid" operator="in" />
    <feMorphology operator="dilate" radius={size / 2} />
  </filter>
);
