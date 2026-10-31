import React from 'react';

/**
 * Code-drawn cartoon cast. Every character is a rig of SVG parts, so the same person looks
 * identical in every shot and can blink, emote, gesture and lip-sync to the voice.
 *
 * Coordinates: a 300x620 box with the feet at (150, 600). Mount through <Actor> (Stage.tsx),
 * which places, scales and mirrors the box in the frame.
 */

export const INK = '#16161C';
const STROKE = 7;

export type Pose =
  | 'idle'
  | 'point'
  | 'shrug'
  | 'panic'
  | 'wave'
  | 'phone'
  | 'cheer'
  | 'think'
  | 'zombie'
  | 'run'
  | 'walk'
  | 'facepalm'
  | 'sit';
export type Expr = 'neutral' | 'happy' | 'shocked' | 'scared' | 'angry' | 'sad' | 'smug' | 'sleepy' | 'grin';

export type Look = {
  skin: string;
  hair: string;
  hairStyle: 'messy' | 'short' | 'long' | 'bald' | 'beanie' | 'bun';
  top: string;
  pants: string;
  shoes?: string;
  /** Small yellow Z on the chest (the zylo hero). */
  logo?: boolean;
  beard?: boolean;
  glasses?: boolean;
  zombie?: boolean;
  hat?: string;
};

export const LOOKS: Record<string, Look> = {
  // The recurring zylo hero: blue hoodie with the yellow Z, messy brown hair.
  hero: { skin: '#F5C49C', hair: '#3B2416', hairStyle: 'messy', top: '#2F6BFF', pants: '#262A3D', shoes: '#F4F4F4', logo: true },
  friend: { skin: '#C98B5E', hair: '#141414', hairStyle: 'bun', top: '#FF6B4A', pants: '#2E2E38', shoes: '#141414' },
  boss: { skin: '#F0BE96', hair: '#8C8C8C', hairStyle: 'short', top: '#3A3F4F', pants: '#22242E', shoes: '#141414', glasses: true, beard: true },
  kid: { skin: '#FFD3B0', hair: '#E2A23B', hairStyle: 'short', top: '#2DBE7E', pants: '#3A4A8C', shoes: '#F4F4F4' },
  scientist: { skin: '#E8B08A', hair: '#EDEDED', hairStyle: 'messy', top: '#F2F2F2', pants: '#3B3F52', shoes: '#141414', glasses: true },
  zombie: { skin: '#9CC27A', hair: '#2B2B2B', hairStyle: 'messy', top: '#7A6E66', pants: '#3D3A44', shoes: '#2B2B2B', zombie: true },
  zombie2: { skin: '#A8C98A', hair: '#5A3A22', hairStyle: 'long', top: '#5E7FA8', pants: '#3D3A44', shoes: '#2B2B2B', zombie: true },
  soldier: { skin: '#D9A27A', hair: '#2B2B2B', hairStyle: 'short', top: '#5D6B3A', pants: '#4A5530', shoes: '#2B2B2B', hat: '#4A5530' },
};

const shade = (hex: string, k: number) => {
  const n = parseInt(hex.slice(1), 16);
  const c = (v: number) => Math.max(0, Math.min(255, Math.round(v * k)));
  return `rgb(${c((n >> 16) & 255)},${c((n >> 8) & 255)},${c(n & 255)})`;
};

/** [upper, elbow] outward angles in degrees for the screen-left (L) and screen-right (R) arm. */
type ArmPair = { L: [number, number]; R: [number, number] };

const armPose = (pose: Pose, t: number): ArmPair => {
  const swing = Math.sin(t / 3.2);
  switch (pose) {
    case 'point':
      return { L: [10, -6], R: [98, -4] };
    case 'shrug':
      return { L: [48, -115], R: [48, -115] };
    case 'panic':
      return { L: [150 + swing * 8, 18], R: [150 - swing * 8, 18] };
    case 'wave':
      return { L: [10, -6], R: [140, -40 + swing * 28] };
    case 'phone':
      return { L: [10, -6], R: [22, -142] };
    case 'cheer':
      return { L: [145, -12], R: [145, -12] };
    case 'think':
      return { L: [12, -95], R: [-20, -150] };
    case 'zombie':
      return { L: [82 + swing * 4, -8], R: [86 - swing * 4, -8] };
    case 'run':
      return { L: [30 + swing * 45, -70], R: [30 - swing * 45, -70] };
    case 'walk':
      return { L: [12 + swing * 18, -20], R: [12 - swing * 18, -20] };
    case 'facepalm':
      return { L: [10, -6], R: [-25, -152] };
    case 'sit':
      return { L: [18, -70], R: [18, -70] };
    default:
      return { L: [9 + Math.sin(t / 25) * 2, -6], R: [9 - Math.sin(t / 25) * 2, -6] };
  }
};

const Arm: React.FC<{ side: 'L' | 'R'; a: [number, number]; look: Look; holdPhone?: boolean }> = ({ side, a, look, holdPhone }) => {
  const sgn = side === 'L' ? 1 : -1;
  const x = side === 'L' ? 92 : 208;
  return (
    <g transform={`translate(${x} 262) rotate(${a[0] * sgn})`}>
      <rect x={-19} y={-6} width={38} height={102} rx={19} fill={look.top} stroke={INK} strokeWidth={STROKE} />
      <g transform={`translate(0 90) rotate(${a[1] * sgn})`}>
        <rect x={-17} y={-8} width={34} height={92} rx={17} fill={shade(look.top, 0.9)} stroke={INK} strokeWidth={STROKE} />
        <circle cx={0} cy={92} r={21} fill={look.skin} stroke={INK} strokeWidth={STROKE} />
        {holdPhone && (
          <g transform="translate(-22 70) rotate(-8)">
            <rect x={0} y={0} width={44} height={74} rx={9} fill="#1D1F2B" stroke={INK} strokeWidth={5} />
            <rect x={6} y={8} width={32} height={52} rx={4} fill="#7FD3FF" />
          </g>
        )}
      </g>
    </g>
  );
};

const Legs: React.FC<{ pose: Pose; t: number; look: Look }> = ({ pose, t, look }) => {
  const moving = pose === 'run' || pose === 'walk';
  const amp = pose === 'run' ? 32 : 16;
  const s = moving ? Math.sin(t / 3.2) * amp : 0;
  if (pose === 'sit') {
    return (
      <g>
        <rect x={98} y={455} width={48} height={60} rx={20} fill={look.pants} stroke={INK} strokeWidth={STROKE} transform="rotate(-80 122 470)" />
        <rect x={154} y={455} width={48} height={60} rx={20} fill={look.pants} stroke={INK} strokeWidth={STROKE} transform="rotate(-80 178 470)" />
      </g>
    );
  }
  const leg = (x: number, ang: number, i: number) => (
    <g key={i} transform={`rotate(${ang} ${x} 470)`}>
      <rect x={x - 25} y={455} width={50} height={130} rx={22} fill={look.pants} stroke={INK} strokeWidth={STROKE} />
      <path d={`M ${x - 32} 600 Q ${x - 32} 570 ${x} 570 Q ${x + 40} 570 ${x + 40} 600 Z`} fill={look.shoes ?? '#F4F4F4'} stroke={INK} strokeWidth={STROKE} strokeLinejoin="round" />
    </g>
  );
  return <g>{[leg(122, s, 0), leg(178, -s, 1)]}</g>;
};

const Hair: React.FC<{ look: Look; layer: 'back' | 'front' }> = ({ look, layer }) => {
  const c = look.hair;
  if (look.hairStyle === 'bald') return null;
  if (look.hairStyle === 'long' && layer === 'back') {
    return <path d="M 52 150 Q 50 60 150 52 Q 250 60 248 150 L 252 262 Q 150 290 48 262 Z" fill={c} stroke={INK} strokeWidth={STROKE} strokeLinejoin="round" />;
  }
  if (look.hairStyle === 'bun' && layer === 'back') {
    return <circle cx={150} cy={44} r={36} fill={c} stroke={INK} strokeWidth={STROKE} />;
  }
  if (layer === 'back') return null;
  switch (look.hairStyle) {
    case 'messy':
      return (
        <path
          d="M 58 140 Q 50 70 105 58 L 112 38 L 132 56 L 150 30 L 166 56 L 192 36 L 196 62 Q 252 80 244 140 Q 220 102 188 104 L 170 88 L 154 106 L 128 92 L 110 108 Q 76 104 58 140 Z"
          fill={c}
          stroke={INK}
          strokeWidth={STROKE}
          strokeLinejoin="round"
        />
      );
    case 'short':
    case 'bun':
      return (
        <path d="M 56 138 Q 52 58 150 54 Q 248 58 244 138 Q 226 96 150 92 Q 74 96 56 138 Z" fill={c} stroke={INK} strokeWidth={STROKE} strokeLinejoin="round" />
      );
    case 'long':
      return <path d="M 56 150 Q 56 62 150 58 Q 244 62 244 150 Q 206 94 150 96 Q 92 96 56 150 Z" fill={c} stroke={INK} strokeWidth={STROKE} strokeLinejoin="round" />;
    case 'beanie':
      return (
        <g>
          <path d="M 54 126 Q 56 40 150 38 Q 244 40 246 126 Z" fill="#20212B" stroke={INK} strokeWidth={STROKE} strokeLinejoin="round" />
          <rect x={46} y={110} width={208} height={34} rx={14} fill="#2D2F3C" stroke={INK} strokeWidth={STROKE} />
        </g>
      );
  }
  return null;
};

type Face = { browL: number; browR: number; browY: number; eye: 'open' | 'wide' | 'happy' | 'half' | 'closed'; mouth: string; sweat?: boolean };

const FACES: Record<Expr, Face> = {
  neutral: { browL: 0, browR: 0, browY: 0, eye: 'open', mouth: 'M 128 206 Q 150 216 172 206' },
  happy: { browL: -6, browR: 6, browY: -6, eye: 'happy', mouth: 'M 120 198 Q 150 236 180 198 Z' },
  grin: { browL: -4, browR: 4, browY: -4, eye: 'open', mouth: 'M 116 198 Q 150 240 184 198 Z' },
  shocked: { browL: -12, browR: 12, browY: -16, eye: 'wide', mouth: 'O' },
  scared: { browL: 16, browR: -16, browY: -12, eye: 'wide', mouth: 'M 124 214 Q 133 202 142 214 Q 150 224 158 214 Q 167 202 176 214', sweat: true },
  angry: { browL: -20, browR: 20, browY: 6, eye: 'open', mouth: 'M 126 214 Q 150 202 174 214' },
  sad: { browL: 14, browR: -14, browY: -4, eye: 'open', mouth: 'M 128 216 Q 150 202 172 216' },
  smug: { browL: -4, browR: 12, browY: 0, eye: 'half', mouth: 'M 128 208 Q 158 218 176 200' },
  sleepy: { browL: 0, browR: 0, browY: 4, eye: 'closed', mouth: 'M 138 210 Q 150 214 162 210' },
};

const Eyes: React.FC<{ face: Face; blink: number; gaze: number; zombie?: boolean; skin: string }> = ({ face, blink, gaze, zombie, skin }) => {
  const eyes = [114, 186];
  if (face.eye === 'happy' || face.eye === 'closed') {
    return (
      <g fill="none" stroke={INK} strokeWidth={STROKE} strokeLinecap="round">
        {eyes.map((x) =>
          face.eye === 'happy' ? <path key={x} d={`M ${x - 14} 156 Q ${x} 138 ${x + 14} 156`} /> : <path key={x} d={`M ${x - 14} 152 Q ${x} 160 ${x + 14} 152`} />,
        )}
      </g>
    );
  }
  const wide = face.eye === 'wide';
  const rx = wide ? 19 : 15;
  const ry = (wide ? 24 : 19) * (1 - blink) + 1.5;
  return (
    <g>
      {eyes.map((x) => (
        <g key={x}>
          <ellipse cx={x} cy={150} rx={rx} ry={ry} fill="#FFFFFF" stroke={INK} strokeWidth={5} />
          {blink < 0.6 && (
            <circle cx={x + gaze * 6} cy={152} r={zombie ? 5 : wide ? 7 : 9} fill={zombie ? '#C0392B' : INK} />
          )}
          {face.eye === 'half' && <rect x={x - rx - 3} y={128} width={rx * 2 + 6} height={20} fill={skin} />}
          {face.eye === 'half' && <path d={`M ${x - rx} 148 L ${x + rx} 148`} stroke={INK} strokeWidth={6} strokeLinecap="round" />}
        </g>
      ))}
    </g>
  );
};

export const Human: React.FC<{
  look: Look;
  pose: Pose;
  expr: Expr;
  /** Mouth openness 0..1 while this character speaks. */
  talk: number;
  t: number;
  gaze?: number;
  seed?: number;
}> = ({ look, pose, expr, talk, t, gaze = 0, seed = 0 }) => {
  const face = FACES[expr];
  const arms = armPose(pose, t);
  // Blink every ~3.3 s, staggered per character so a crowd doesn't blink in unison.
  const cyc = (t + seed * 37) % 100;
  const blink = cyc < 2 ? cyc / 2 : cyc < 4 ? (4 - cyc) / 2 : 0;
  const bob = pose === 'run' ? Math.abs(Math.sin(t / 3.2)) * -14 : pose === 'walk' ? Math.abs(Math.sin(t / 3.2)) * -6 : Math.sin(t / 18) * 2.5;
  const headTilt = pose === 'zombie' ? 9 + Math.sin(t / 9) * 3 : pose === 'think' ? -6 : pose === 'facepalm' ? 8 : 0;
  const lean = pose === 'run' ? 8 : pose === 'zombie' ? 4 : 0;
  const skinFace = look.skin;
  const mouthOpen = expr === 'sleepy' ? 0 : talk;

  const mouth =
    face.mouth === 'O' || mouthOpen > 0.15 ? (
      <ellipse
        cx={150}
        cy={210}
        rx={face.mouth === 'O' ? 15 + mouthOpen * 4 : 16 + mouthOpen * 6}
        ry={face.mouth === 'O' ? 19 + mouthOpen * 4 : 4 + mouthOpen * 15}
        fill="#5A1E25"
        stroke={INK}
        strokeWidth={5}
      />
    ) : face.mouth.endsWith('Z') ? (
      <path d={face.mouth} fill="#5A1E25" stroke={INK} strokeWidth={5} strokeLinejoin="round" />
    ) : (
      <path d={face.mouth} fill="none" stroke={INK} strokeWidth={6} strokeLinecap="round" />
    );

  return (
    <g transform={`translate(0 ${bob}) rotate(${lean} 150 600)`}>
      <Legs pose={pose} t={t} look={look} />
      <Arm side="L" a={arms.L} look={look} />
      {/* torso */}
      <path
        d="M 82 470 L 88 290 Q 92 244 150 242 Q 208 244 212 290 L 218 470 Q 150 486 82 470 Z"
        fill={look.top}
        stroke={INK}
        strokeWidth={STROKE}
        strokeLinejoin="round"
      />
      <path d="M 104 410 Q 150 424 196 410" fill="none" stroke={shade(look.top, 0.72)} strokeWidth={5} strokeLinecap="round" />
      {look.zombie && <path d="M 120 440 L 132 420 L 146 444 L 160 418 L 172 446" fill="none" stroke={INK} strokeWidth={5} strokeLinejoin="round" />}
      {look.logo && (
        <g transform="translate(150 340)">
          <rect x={-24} y={-24} width={48} height={48} rx={12} fill="#16161C" />
          <path d="M -12 -12 H 12 L -12 12 H 12" fill="none" stroke="#FFD400" strokeWidth={7} strokeLinejoin="round" strokeLinecap="round" />
        </g>
      )}
      <Arm side="R" a={arms.R} look={look} holdPhone={pose === 'phone'} />
      {/* head */}
      <g transform={`rotate(${headTilt} 150 230)`}>
        <Hair look={look} layer="back" />
        <rect x={130} y={214} width={40} height={40} fill={skinFace} stroke={INK} strokeWidth={STROKE} />
        <circle cx={58} cy={160} r={18} fill={skinFace} stroke={INK} strokeWidth={STROKE} />
        <circle cx={242} cy={160} r={18} fill={skinFace} stroke={INK} strokeWidth={STROKE} />
        <ellipse cx={150} cy={150} rx={94} ry={100} fill={skinFace} stroke={INK} strokeWidth={STROKE} />
        {look.zombie && <path d="M 196 96 L 210 112 M 204 96 L 202 116" stroke="#6E8F52" strokeWidth={5} strokeLinecap="round" />}
        <Hair look={look} layer="front" />
        {look.hat && <path d="M 50 118 Q 54 40 150 38 Q 246 40 250 118 L 270 124 L 30 124 Z" fill={look.hat} stroke={INK} strokeWidth={STROKE} strokeLinejoin="round" />}
        <g transform={`translate(0 ${face.browY})`} stroke={INK} strokeWidth={8} strokeLinecap="round">
          <line x1={98} y1={122} x2={130} y2={122} transform={`rotate(${face.browL} 114 122)`} />
          <line x1={170} y1={122} x2={202} y2={122} transform={`rotate(${face.browR} 186 122)`} />
        </g>
        <Eyes face={face} blink={blink} gaze={gaze} zombie={look.zombie} skin={skinFace} />
        {look.glasses && (
          <g fill="none" stroke={INK} strokeWidth={6}>
            <circle cx={114} cy={150} r={27} />
            <circle cx={186} cy={150} r={27} />
            <line x1={141} y1={150} x2={159} y2={150} />
          </g>
        )}
        <circle cx={96} cy={186} r={11} fill="#FF8A8A" opacity={look.zombie ? 0 : 0.45} />
        <circle cx={204} cy={186} r={11} fill="#FF8A8A" opacity={look.zombie ? 0 : 0.45} />
        {look.beard && <path d="M 80 180 Q 86 250 150 254 Q 214 250 220 180 Q 196 236 150 234 Q 104 236 80 180 Z" fill={look.hair} stroke={INK} strokeWidth={5} />}
        {mouth}
        {face.sweat && <path d="M 236 108 Q 250 130 242 140 Q 230 140 230 128 Q 230 118 236 108 Z" fill="#8FD3FF" stroke={INK} strokeWidth={4} />}
      </g>
    </g>
  );
};

export type BitExpr = 'neutral' | 'happy' | 'shocked' | 'angry' | 'sad' | 'think' | 'glitch' | 'smug';

/**
 * Bit, the zylo AI: a floating white monitor with a dark screen face, yellow eyes and an
 * antenna. `icon` swaps the eyes for a symbol on screen ($, !, ?, ♥, %, ...).
 */
export const Bit: React.FC<{ expr: BitExpr; talk: number; t: number; icon?: string; seed?: number }> = ({ expr, talk, t, icon, seed = 0 }) => {
  const hover = Math.sin(t / 14) * 10;
  const cyc = (t + seed * 29) % 110;
  const blink = cyc < 3 ? 1 : 0;
  const eyeColor = '#FFD400';
  const glitch = expr === 'glitch' ? Math.sin(t * 2.3) * 6 : 0;
  const eye = (x: number, i: number) => {
    switch (expr) {
      case 'happy':
        return <path key={i} d={`M ${x - 18} 190 Q ${x} 168 ${x + 18} 190`} fill="none" stroke={eyeColor} strokeWidth={10} strokeLinecap="round" />;
      case 'shocked':
        return <circle key={i} cx={x} cy={182} r={22} fill="none" stroke={eyeColor} strokeWidth={9} />;
      case 'angry':
        return <path key={i} d={i ? `M ${x - 18} 170 L ${x + 18} 186 L ${x + 18} 200 L ${x - 18} 200 Z` : `M ${x - 18} 186 L ${x + 18} 170 L ${x + 18} 200 L ${x - 18} 200 Z`} fill={eyeColor} />;
      case 'sad':
        return <path key={i} d={i ? `M ${x - 18} 172 L ${x + 18} 182 L ${x + 18} 198 L ${x - 18} 198 Z` : `M ${x - 18} 182 L ${x + 18} 172 L ${x + 18} 198 L ${x - 18} 198 Z`} fill={eyeColor} opacity={0.85} />;
      case 'think':
        return i ? <rect key={i} x={x - 16} y={182} width={32} height={10} rx={5} fill={eyeColor} /> : <rect key={i} x={x - 14} y={164} width={28} height={36} rx={10} fill={eyeColor} />;
      case 'smug':
        return <rect key={i} x={x - 16} y={180} width={32} height={14} rx={6} fill={eyeColor} />;
      default:
        return <rect key={i} x={x - 14} y={blink ? 182 : 162} width={28} height={blink ? 6 : 40} rx={10} fill={eyeColor} />;
    }
  };
  return (
    <g transform={`translate(${glitch} ${hover})`}>
      {/* shadow on the ground */}
      <ellipse cx={150} cy={590 - hover} rx={70 - hover} ry={12} fill="rgba(0,0,0,0.18)" />
      {/* antenna */}
      <line x1={150} y1={92} x2={150} y2={52} stroke={INK} strokeWidth={STROKE} />
      <circle cx={150} cy={44} r={15 + (talk > 0.2 ? 3 : 0)} fill={eyeColor} stroke={INK} strokeWidth={6} />
      {/* shell */}
      <rect x={40} y={92} width={220} height={190} rx={56} fill="#F3F3F7" stroke={INK} strokeWidth={STROKE} />
      <rect x={62} y={114} width={176} height={146} rx={38} fill="#14161F" stroke={INK} strokeWidth={5} />
      {icon ? (
        <text x={150} y={214} textAnchor="middle" fontFamily="ZyloHead" fontWeight={900} fontSize={92} fill={eyeColor}>
          {icon}
        </text>
      ) : (
        <>
          {[118, 182].map((x, i) => eye(x, i))}
          <rect x={150 - 14 - talk * 16} y={224 - talk * 6} width={28 + talk * 32} height={8 + talk * 14} rx={6} fill={eyeColor} opacity={0.9} />
        </>
      )}
      {/* little floating hands */}
      <circle cx={24} cy={230 + Math.sin(t / 10) * 8} r={20} fill="#F3F3F7" stroke={INK} strokeWidth={6} />
      <circle cx={276} cy={230 - Math.sin(t / 10) * 8} r={20} fill="#F3F3F7" stroke={INK} strokeWidth={6} />
      {/* body stub */}
      <path d="M 110 282 Q 150 330 190 282" fill="#E2E2EA" stroke={INK} strokeWidth={6} />
    </g>
  );
};
