import React from 'react';
import { Easing, interpolate, spring } from 'remotion';
import { brand } from '../brand';
import { INK } from './Character';

const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;

/**
 * Story overlays drawn above the set (not affected by the camera): the props that carry
 * numbers, time and stakes in the reference shorts.
 */
export type UiSpec =
  /** Big digital clock; `to` makes it tick from `text` to `to` over the shot (HH:MM). */
  | { type: 'clock'; text: string; to?: string; color?: string }
  /** Phone notification card sliding in from the top. */
  | { type: 'notify'; app: string; title: string; body?: string; color?: string }
  /** Rubber stamp slammed onto the frame. */
  | { type: 'stamp'; text: string; color?: string }
  /** Paper label with a list that builds item by item (rules, steps, inventory). */
  | { type: 'list'; title?: string; items: string[] }
  /** Named progress bars (race between characters, health, savings). */
  | { type: 'bars'; items: { label: string; value: number; color?: string }[]; tag?: string }
  /** Map with a spreading danger radius. */
  | { type: 'map'; label?: string; radius?: number }
  /** Tilted paper card with a big line of text (DAY 1, $1,000,000, 3 HOURS LATER). */
  | { type: 'card'; text: string; sub?: string; color?: string }
  /** Countdown or count-up number. */
  | { type: 'counter'; from: number; to: number; prefix?: string; suffix?: string; label?: string };

const Paper: React.FC<{ children: React.ReactNode; tilt?: number; style?: React.CSSProperties }> = ({ children, tilt = -2, style }) => (
  <div
    style={{
      background: '#FFF6DF',
      border: `6px solid ${INK}`,
      borderRadius: 18,
      boxShadow: `10px 12px 0 ${INK}`,
      transform: `rotate(${tilt}deg)`,
      ...style,
    }}
  >
    {children}
  </div>
);

const pad = (n: number) => String(n).padStart(2, '0');
const toMin = (hhmm: string) => {
  const [h, m] = hhmm.split(':').map(Number);
  return h * 60 + m;
};

export const UiLayer: React.FC<{ ui: UiSpec; f: number; fps: number; dur: number }> = ({ ui, f, fps, dur }) => {
  const s = spring({ frame: f, fps, config: { damping: 13, stiffness: 140 } });
  const pop = { transform: `scale(${0.6 + 0.4 * s})`, opacity: Math.min(1, s * 1.5) };
  const wrap = (top: number, node: React.ReactNode) => (
    <div style={{ position: 'absolute', top, left: 0, right: 0, display: 'flex', justifyContent: 'center' }}>{node}</div>
  );
  switch (ui.type) {
    case 'clock': {
      let text = ui.text;
      if (ui.to) {
        const a = toMin(ui.text);
        const b = toMin(ui.to);
        const m = Math.round(a + (b - a) * interpolate(f, [4, dur - 6], [0, 1], clamp));
        text = `${pad(Math.floor(m / 60) % 24)}:${pad(m % 60)}`;
      }
      return wrap(
        260,
        <div
          style={{
            ...pop,
            padding: '18px 44px',
            background: '#0D0D12',
            border: `6px solid ${INK}`,
            borderRadius: 24,
            fontFamily: 'ui-monospace, Menlo, monospace',
            fontWeight: 900,
            fontSize: 150,
            letterSpacing: 8,
            color: ui.color ?? '#FF3B3B',
            textShadow: `0 0 30px ${ui.color ?? '#FF3B3B'}`,
          }}
        >
          {text}
        </div>,
      );
    }
    case 'notify': {
      const y = interpolate(s, [0, 1], [-260, 0]);
      return (
        <div style={{ position: 'absolute', top: 230 + y, left: 70, right: 70 }}>
          <div
            style={{
              display: 'flex',
              gap: 26,
              alignItems: 'center',
              padding: '28px 32px',
              background: '#FFFFFF',
              border: `6px solid ${INK}`,
              borderRadius: 34,
              boxShadow: `0 14px 0 ${INK}`,
            }}
          >
            <div
              style={{
                width: 92,
                height: 92,
                borderRadius: 24,
                background: ui.color ?? '#2F6BFF',
                border: `5px solid ${INK}`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontFamily: brand.head,
                fontWeight: 900,
                fontSize: 48,
                color: '#FFFFFF',
              }}
            >
              {ui.app.slice(0, 1)}
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ fontFamily: brand.body, fontWeight: 700, fontSize: 28, color: '#6B6F80' }}>{ui.app} · now</div>
              <div style={{ fontFamily: brand.body, fontWeight: 900, fontSize: 44, color: INK, lineHeight: 1.15 }}>{ui.title}</div>
              {ui.body && <div style={{ fontFamily: brand.body, fontWeight: 600, fontSize: 34, color: '#3C4050', marginTop: 4 }}>{ui.body}</div>}
            </div>
          </div>
        </div>
      );
    }
    case 'stamp': {
      const slam = interpolate(f, [6, 12], [2.4, 1], { ...clamp, easing: Easing.in(Easing.quad) });
      return wrap(
        620,
        <div
          style={{
            opacity: f >= 6 ? 1 : 0,
            transform: `rotate(-12deg) scale(${slam})`,
            padding: '16px 40px',
            border: `12px solid ${ui.color ?? '#E0312B'}`,
            borderRadius: 18,
            fontFamily: brand.head,
            fontWeight: 900,
            fontSize: 110,
            color: ui.color ?? '#E0312B',
            letterSpacing: 4,
            background: 'rgba(255,255,255,0.15)',
          }}
        >
          {ui.text}
        </div>,
      );
    }
    case 'list': {
      const step = Math.max(6, (dur - 10) / ui.items.length);
      return wrap(
        230,
        <div style={{ width: 900, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 22 }}>
          {ui.title && (
            <div style={{ fontFamily: brand.head, fontWeight: 900, fontSize: 64, color: '#FFD400', textShadow: `5px 5px 0 ${INK}`, ...pop }}>{ui.title}</div>
          )}
          {ui.items.map((it, i) => {
            const k = spring({ frame: f - i * step, fps, config: { damping: 14 } });
            return (
              <Paper key={i} tilt={i % 2 ? 1.2 : -1.2} style={{ width: 860, opacity: k, transform: `translateX(${(1 - k) * 120}px) rotate(${i % 2 ? 1.2 : -1.2}deg)` }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 22, padding: '20px 28px' }}>
                  <div
                    style={{
                      width: 64,
                      height: 64,
                      borderRadius: 32,
                      background: ['#2F6BFF', '#FF6B4A', '#2DBE7E', '#E0312B', '#B05CFF'][i % 5],
                      border: `5px solid ${INK}`,
                      color: '#FFFFFF',
                      fontFamily: brand.head,
                      fontWeight: 900,
                      fontSize: 34,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                    }}
                  >
                    {i + 1}
                  </div>
                  <div style={{ fontFamily: brand.body, fontWeight: 900, fontSize: 42, color: INK }}>{it}</div>
                </div>
              </Paper>
            );
          })}
        </div>,
      );
    }
    case 'bars': {
      const grow = interpolate(f, [4, Math.min(dur - 4, 30)], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
      return (
        <div style={{ position: 'absolute', top: 210, left: 60, right: 60, ...pop }}>
          <div style={{ background: '#16161C', border: `6px solid ${INK}`, borderRadius: 24, padding: '24px 28px', position: 'relative' }}>
            {ui.tag && (
              <div
                style={{
                  position: 'absolute',
                  top: -34,
                  right: 24,
                  background: '#E0312B',
                  color: '#FFFFFF',
                  fontFamily: brand.head,
                  fontWeight: 900,
                  fontSize: 32,
                  padding: '6px 20px',
                  borderRadius: 12,
                  border: `5px solid ${INK}`,
                }}
              >
                {ui.tag}
              </div>
            )}
            {ui.items.map((b, i) => (
              <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 18, marginTop: i ? 16 : 0 }}>
                <div style={{ width: 170, fontFamily: brand.body, fontWeight: 900, fontSize: 32, color: b.color ?? '#FFD400' }}>{b.label}</div>
                <div style={{ flex: 1, height: 34, borderRadius: 10, background: '#2C2D38', overflow: 'hidden' }}>
                  <div style={{ width: `${b.value * grow * 100}%`, height: '100%', background: b.color ?? '#FFD400', borderRadius: 10 }} />
                </div>
                <div style={{ width: 90, textAlign: 'right', fontFamily: brand.body, fontWeight: 900, fontSize: 30, color: '#FFFFFF' }}>{Math.round(b.value * grow * 100)}%</div>
              </div>
            ))}
          </div>
        </div>
      );
    }
    case 'map': {
      const r = interpolate(f, [6, dur], [0.05, ui.radius ?? 0.8], { ...clamp, easing: Easing.out(Easing.cubic) });
      return wrap(
        250,
        <Paper tilt={-1.5} style={{ width: 860, height: 700, overflow: 'hidden', position: 'relative', background: '#BFE3F2', ...pop }}>
          <svg viewBox="0 0 860 700" width="100%" height="100%">
            <path d="M 80 120 Q 260 40 420 130 Q 600 80 760 200 Q 820 380 700 520 Q 520 640 330 600 Q 120 560 90 380 Z" fill="#9ED37E" stroke={INK} strokeWidth={6} />
            <path d="M 200 200 L 640 460 M 260 520 L 600 160 M 120 330 L 760 330" stroke="#FFFFFF" strokeWidth={10} opacity={0.7} />
            <circle cx={430} cy={340} r={r * 420} fill="#E0312B" opacity={0.35} stroke="#E0312B" strokeWidth={6} />
            <circle cx={430} cy={340} r={16} fill="#E0312B" stroke={INK} strokeWidth={5} />
          </svg>
          {ui.label && (
            <div style={{ position: 'absolute', bottom: 22, left: 0, right: 0, textAlign: 'center', fontFamily: brand.head, fontWeight: 900, fontSize: 46, color: INK }}>
              {ui.label}
            </div>
          )}
        </Paper>,
      );
    }
    case 'card': {
      // Readable on any card colour: light text on dark cards.
      const hex = (ui.color ?? '#FFF6DF').replace('#', '');
      const lum = (0.299 * parseInt(hex.slice(0, 2), 16) + 0.587 * parseInt(hex.slice(2, 4), 16) + 0.114 * parseInt(hex.slice(4, 6), 16)) / 255;
      const dark = lum < 0.5;
      return wrap(
        330,
        <Paper tilt={-3} style={{ padding: '30px 54px', textAlign: 'center', background: ui.color ?? '#FFF6DF', ...pop, transform: `rotate(-3deg) scale(${0.6 + 0.4 * s})` }}>
          <div style={{ fontFamily: brand.head, fontWeight: 900, fontSize: ui.text.length > 14 ? 72 : ui.text.length > 10 ? 84 : 120, color: dark ? '#FFFFFF' : INK, lineHeight: 1.05 }}>{ui.text}</div>
          {ui.sub && <div style={{ marginTop: 10, fontFamily: brand.body, fontWeight: 900, fontSize: 40, color: dark ? '#FFD400' : '#E0312B' }}>{ui.sub}</div>}
        </Paper>,
      );
    }
    case 'counter': {
      const p = interpolate(f, [2, Math.max(8, dur - 8)], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
      const dec = Number.isInteger(ui.from) && Number.isInteger(ui.to) ? 0 : 1;
      const v = Number((ui.from + (ui.to - ui.from) * p).toFixed(dec));
      return wrap(
        280,
        <div style={{ textAlign: 'center', ...pop }}>
          <div style={{ fontFamily: brand.head, fontWeight: 900, fontSize: 150, color: '#FFD400', WebkitTextStroke: `6px ${INK}`, textShadow: `8px 8px 0 ${INK}` }}>
            {ui.prefix ?? ''}
            {v.toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec })}
            {ui.suffix ?? ''}
          </div>
          {ui.label && <div style={{ fontFamily: brand.body, fontWeight: 900, fontSize: 48, color: '#FFFFFF', textShadow: `4px 4px 0 ${INK}` }}>{ui.label}</div>}
        </div>,
      );
    }
  }
};
