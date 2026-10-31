import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { Bit, BitExpr, Expr, Human, LOOKS, Pose } from '../../zylo-shared/toon/Character';

const poses: [string, Pose, Expr][] = [
  ['hero', 'idle', 'neutral'],
  ['hero', 'point', 'happy'],
  ['hero', 'panic', 'scared'],
  ['hero', 'phone', 'shocked'],
  ['hero', 'shrug', 'smug'],
  ['hero', 'think', 'neutral'],
  ['hero', 'run', 'scared'],
  ['hero', 'facepalm', 'sad'],
  ['friend', 'wave', 'grin'],
  ['boss', 'idle', 'angry'],
  ['scientist', 'point', 'shocked'],
  ['zombie', 'zombie', 'neutral'],
];
const bits: BitExpr[] = ['neutral', 'happy', 'shocked', 'angry'];

/** Every pose and face on one page, for reviewing the rigs. */
export const CastSheet: React.FC = () => {
  const t = useCurrentFrame();
  return (
    <AbsoluteFill style={{ backgroundColor: '#EDE9DF' }}>
      <svg viewBox="0 0 1800 1600" width="100%" height="100%">
        {poses.map(([look, pose, expr], i) => (
          <g key={i} transform={`translate(${(i % 6) * 300} ${Math.floor(i / 6) * 640})`}>
            <Human look={LOOKS[look]} pose={pose} expr={expr} talk={i % 3 === 0 ? 0.7 : 0} t={t + i * 7} seed={i} />
          </g>
        ))}
        {bits.map((e, i) => (
          <g key={e} transform={`translate(${i * 300 + 150} 1290) scale(0.9)`}>
            <Bit expr={e} talk={i === 0 ? 0.6 : 0} t={t} icon={i === 3 ? undefined : undefined} />
          </g>
        ))}
        <g transform="translate(1350 1290) scale(0.9)">
          <Bit expr="neutral" talk={0} t={t} icon="$" />
        </g>
      </svg>
    </AbsoluteFill>
  );
};
