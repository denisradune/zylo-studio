import React from 'react';
import { Easing, interpolate, spring } from 'remotion';
import { SCREEN } from './Den';

/**
 * What the desk monitor shows in a tips shot (shot.screen). Crisp vector UI, dark theme,
 * yellow accent. Everything animates in over the shot (f = local frame).
 *
 *  {"kind": "stat", "label": "VIEWS", "value": 127346, "sub": "217 subscribers"}
 *  {"kind": "chat", "from": "hero", "text": "write me a viral script", "reply": 3}   reply = gray lines, or a string
 *  {"kind": "prompts", "text": "write me a viral video", "n": 3}                     same prompt -> same boring result
 *  {"kind": "step", "n": 1, "text": "Here is my topic..."}
 *  {"kind": "cards", "n": 10, "mark": "?", "pick": 4}
 *  {"kind": "slots", "title": "30-SECOND SCRIPT", "items": [{"icon": "hook", "label": "HOOK"}, ...]}
 *  {"kind": "videos", "title": "VIDEOS ON THIS TOPIC", "items": [{"views": "2.8M", "ok": true}, ...]}
 *  {"kind": "compare", "bad": "write a viral video", "good": "find 10 problems..."}
 *  {"kind": "list", "title": "CHECKLIST", "items": ["...", "..."]}
 *  {"kind": "title", "text": "STEP 2", "sub": "..."}
 */
export type MonitorIcon = 'hook' | 'lines' | 'question' | 'check' | 'cross' | 'play' | 'star' | 'clock' | 'money' | 'bolt' | 'chat' | 'search';
export type MonitorScreen =
  | { kind: 'stat'; label: string; value: number; prefix?: string; suffix?: string; sub?: string }
  | { kind: 'chat'; from?: 'hero' | 'bit'; text: string; reply?: number | string }
  | { kind: 'prompts'; text: string; n?: number }
  | { kind: 'step'; n: number; text?: string }
  | { kind: 'cards'; n?: number; mark?: string; pick?: number }
  | { kind: 'slots'; title?: string; items: { icon: MonitorIcon; label: string }[] }
  | { kind: 'videos'; title?: string; items: { views: string; ok?: boolean }[] }
  | { kind: 'compare'; bad: string; good: string }
  | { kind: 'list'; title?: string; items: string[] }
  | { kind: 'title'; text: string; sub?: string };

const Y = '#FFD400';
const BG = '#16161F';
const PANEL = '#22222E';
const TXT = '#F4F4F8';
const DIM = '#7C7C92';
const RED = '#FF4A3D';
const GREEN = '#2FBF71';
const FONT = 'ZyloBody';
const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;

/** Word-wrap into lines of at most `max` characters. */
const wrap = (s: string, max: number) => {
  const out: string[] = [];
  let cur = '';
  s.split(/\s+/).forEach((w) => {
    if ((cur + ' ' + w).trim().length > max) {
      if (cur) out.push(cur);
      cur = w;
    } else cur = (cur + ' ' + w).trim();
  });
  if (cur) out.push(cur);
  return out;
};

export const Icon: React.FC<{ kind: MonitorIcon; x: number; y: number; s?: number; color?: string }> = ({ kind, x, y, s = 1, color = Y }) => {
  const sw = 14;
  const p = { fill: 'none', stroke: color, strokeWidth: sw, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const };
  let g: React.ReactNode;
  switch (kind) {
    case 'hook':
      g = <path d="M 10 -50 L 10 20 Q 10 50 -18 50 Q -46 50 -46 22 M -46 22 L -30 34" {...p} />;
      break;
    case 'lines':
      g = (
        <g>
          {[-30, 0, 30].map((dy, i) => (
            <line key={i} x1={-44} y1={dy} x2={i === 2 ? 14 : 44} y2={dy} {...p} />
          ))}
        </g>
      );
      break;
    case 'question':
      g = (
        <g>
          <path d="M -26 -24 Q -26 -52 0 -52 Q 28 -52 28 -26 Q 28 -6 0 4 L 0 18" {...p} />
          <circle cx={0} cy={44} r={9} fill={color} />
        </g>
      );
      break;
    case 'check':
      g = <path d="M -40 2 L -12 30 L 42 -30" {...p} />;
      break;
    case 'cross':
      g = <path d="M -34 -34 L 34 34 M 34 -34 L -34 34" {...p} />;
      break;
    case 'play':
      g = <path d="M -24 -38 L 36 0 L -24 38 Z" fill={color} stroke={color} strokeWidth={8} strokeLinejoin="round" />;
      break;
    case 'star':
      g = <path d="M 0 -48 L 14 -14 L 50 -12 L 22 10 L 32 46 L 0 26 L -32 46 L -22 10 L -50 -12 L -14 -14 Z" fill={color} />;
      break;
    case 'clock':
      g = (
        <g>
          <circle cx={0} cy={0} r={44} {...p} />
          <path d="M 0 -24 L 0 0 L 18 12" {...p} />
        </g>
      );
      break;
    case 'money':
      g = <text x={0} y={30} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={96} fill={color}>$</text>;
      break;
    case 'bolt':
      g = <path d="M 10 -52 L -30 8 L 0 8 L -10 52 L 30 -8 L 0 -8 Z" fill={color} />;
      break;
    case 'chat':
      g = <path d="M -44 -34 H 44 V 22 H -6 L -26 42 L -24 22 H -44 Z" {...p} />;
      break;
    case 'search':
      g = (
        <g>
          <circle cx={-8} cy={-8} r={30} {...p} />
          <line x1={14} y1={14} x2={42} y2={42} {...p} />
        </g>
      );
      break;
  }
  return <g transform={`translate(${x} ${y}) scale(${s})`}>{g}</g>;
};

const Avatar: React.FC<{ x: number; y: number; who: 'hero' | 'bit' | number }> = ({ x, y, who }) => {
  const col = who === 'bit' ? Y : who === 'hero' ? '#2F6BFF' : ['#2F6BFF', '#2FBF71', '#B05AD9', '#FF6B4A'][who % 4];
  return (
    <g transform={`translate(${x} ${y})`}>
      <circle r={34} fill={col} />
      {who === 'bit' ? (
        <g>
          <rect x={-20} y={-14} width={40} height={28} rx={6} fill="#16161F" />
          <rect x={-12} y={-8} width={7} height={14} rx={3} fill={Y} />
          <rect x={5} y={-8} width={7} height={14} rx={3} fill={Y} />
        </g>
      ) : (
        <g fill="#F4F4F8">
          <circle cx={0} cy={-8} r={12} />
          <path d="M -22 24 Q 0 -4 22 24 Z" />
        </g>
      )}
    </g>
  );
};

const Bubble: React.FC<{ x: number; y: number; w: number; text: string; shown: number; size?: number; dark?: boolean; caret?: boolean }> = ({ x, y, w, text, shown, size = 38, dark, caret }) => {
  const max = Math.floor((w - 50) / (size * 0.56));
  const vis = text.slice(0, Math.round(shown * text.length));
  const ls = wrap(vis || ' ', max);
  const full = wrap(text, max);
  const h = 34 + full.length * size * 1.22;
  return (
    <g>
      <rect x={x} y={y} width={w} height={h} rx={18} fill={dark ? PANEL : '#F4F4F8'} />
      {ls.map((l, i) => (
        <text key={i} x={x + 24} y={y + 14 + size + i * size * 1.22} fontFamily={FONT} fontWeight={800} fontSize={size} fill={dark ? TXT : '#16161F'}>
          {l}
          {caret && i === ls.length - 1 && shown < 1 ? '|' : ''}
        </text>
      ))}
    </g>
  );
};

const Card: React.FC<{ cx: number; cy: number; a: number; mark: string; lit: number; dark?: number }> = ({ cx, cy, a, mark, lit, dark = 0 }) => (
  <g transform={`translate(${cx} ${cy}) rotate(${a})`} opacity={1 - dark * 0.55}>
    <rect x={-42} y={-62} width={84} height={124} rx={12} fill={lit > 0.5 ? '#F4F4F8' : Y} stroke="#16161F" strokeWidth={6} />
    <text x={0} y={22} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={64} fill={mark === '!' ? RED : '#16161F'}>
      {mark}
    </text>
  </g>
);

export const MonitorLayer: React.FC<{ screen: MonitorScreen; f: number; fps: number; dur: number }> = ({ screen, f, fps, dur }) => {
  const { x: X, y: Y0, w: Wd, h: Hd } = SCREEN;
  const cx = X + Wd / 2;
  const pop = (d = 0) => spring({ frame: f - d, fps, config: { damping: 13, stiffness: 170 } });
  const lin = (a: number, b: number) => interpolate(f, [a, b], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const head = (t: string) => (
    <text x={cx} y={Y0 + 74} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={44} letterSpacing={2} fill={TXT}>
      {t}
    </text>
  );
  let body: React.ReactNode = null;
  switch (screen.kind) {
    case 'stat': {
      const v = Math.round(screen.value * lin(0, Math.min(dur * 0.7, 40)));
      body = (
        <g>
          <g transform={`translate(${X + 70} ${Y0 + 110})`} opacity={pop()}>
            <rect width={200} height={320} rx={16} fill={PANEL} stroke={Y} strokeWidth={6} />
            <Icon kind="play" x={100} y={160} s={1.3} />
          </g>
          <text x={X + 320} y={Y0 + 170} fontFamily={FONT} fontWeight={900} fontSize={44} letterSpacing={3} fill={TXT}>
            {screen.label}
          </text>
          <text x={X + 316} y={Y0 + 300} fontFamily={FONT} fontWeight={900} fontSize={screen.value >= 1e6 ? 110 : 128} fill={Y}>
            {(screen.prefix ?? '') + v.toLocaleString('en-US') + (screen.suffix ?? '')}
          </text>
          {screen.sub && (
            <g opacity={pop(10)}>
              <rect x={X + 316} y={Y0 + 350} width={460} height={90} rx={14} fill="none" stroke={TXT} strokeWidth={6} />
              <text x={X + 546} y={Y0 + 410} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={42} fill={TXT}>
                {screen.sub}
              </text>
            </g>
          )}
        </g>
      );
      break;
    }
    case 'chat': {
      const typed = lin(0, Math.max(10, dur * 0.55));
      const rp = pop(Math.round(dur * 0.6));
      body = (
        <g>
          <Avatar x={X + 70} y={Y0 + 80} who={screen.from ?? 'hero'} />
          <Bubble x={X + 120} y={Y0 + 40} w={Wd - 160} text={screen.text} shown={typed} caret />
          {screen.reply !== undefined && (
            <g opacity={rp} transform={`translate(0 ${(1 - rp) * 30})`}>
              <Avatar x={X + 70} y={Y0 + 330} who="bit" />
              {typeof screen.reply === 'string' ? (
                <Bubble x={X + 120} y={Y0 + 290} w={Wd - 160} text={screen.reply} shown={1} dark size={34} />
              ) : (
                Array.from({ length: screen.reply }).map((_, i) => <rect key={i} x={X + 130} y={Y0 + 300 + i * 50} width={(Wd - 200) * (i === (screen.reply as number) - 1 ? 0.55 : 1)} height={26} rx={13} fill={DIM} opacity={0.6} />)
              )}
            </g>
          )}
        </g>
      );
      break;
    }
    case 'prompts': {
      const n = screen.n ?? 3;
      body = (
        <g>
          {Array.from({ length: n }).map((_, i) => {
            const p = pop(i * 8);
            const y = Y0 + 50 + i * 170;
            return (
              <g key={i} opacity={p} transform={`translate(${(1 - p) * -40} 0)`}>
                <Avatar x={X + 70} y={y + 50} who={i} />
                <Bubble x={X + 120} y={y} w={420} text={screen.text} shown={1} size={32} />
                <path d={`M ${X + 570} ${y + 50} L ${X + 620} ${y + 50} M ${X + 604} ${y + 34} L ${X + 622} ${y + 50} L ${X + 604} ${y + 66}`} fill="none" stroke={TXT} strokeWidth={8} strokeLinecap="round" />
                <rect x={X + 650} y={y + 4} width={160} height={110} rx={10} fill={DIM} />
                {[0, 1, 2, 3].map((k) => (
                  <rect key={k} x={X + 668} y={y + 22 + k * 22} width={k === 3 ? 70 : 124} height={10} rx={5} fill="#B9B9CC" />
                ))}
              </g>
            );
          })}
        </g>
      );
      break;
    }
    case 'step': {
      const p = pop(screen.text ? 12 : 0);
      body = (
        <g>
          {screen.text && (
            <g>
              <Avatar x={X + 70} y={Y0 + 80} who="hero" />
              <Bubble x={X + 120} y={Y0 + 40} w={Wd - 160} text={screen.text} shown={lin(0, Math.max(12, dur * 0.6))} caret size={36} />
            </g>
          )}
          <g transform={`translate(${cx} ${Y0 + (screen.text ? 400 : Hd / 2)}) rotate(-3) scale(${p})`}>
            <rect x={-200} y={-70} width={400} height={140} rx={22} fill={Y} stroke="#16161F" strokeWidth={8} />
            <rect x={-200} y={52} width={400} height={18} rx={9} fill="#C9A800" />
            <text x={0} y={30} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={84} fill="#16161F">
              STEP {screen.n}
            </text>
          </g>
        </g>
      );
      break;
    }
    case 'cards': {
      const n = screen.n ?? 10;
      const spread = lin(0, 18);
      body = (
        <g>
          {Array.from({ length: n }).map((_, i) => {
            const k = (i - (n - 1) / 2) / ((n - 1) / 2 || 1);
            const a = k * 34 * spread;
            const picked = screen.pick === i;
            const up = picked ? lin(24, 40) : 0;
            const r = 520;
            const px = cx + Math.sin((a * Math.PI) / 180) * r;
            const py = Y0 + Hd * 0.62 + r - Math.cos((a * Math.PI) / 180) * r - up * 170;
            return <Card key={i} cx={px} cy={py} a={a * (1 - up)} mark={screen.mark ?? '?'} lit={picked ? up : 0} dark={screen.pick !== undefined && !picked ? up : 0} />;
          })}
        </g>
      );
      break;
    }
    case 'slots': {
      const items = screen.items;
      const n = items.length;
      const bw = Math.min(230, (Wd - 80 - (n - 1) * 24) / n);
      const total = n * bw + (n - 1) * 24;
      const fill = (i: number) => lin((i * dur) / (n + 0.5), (i * dur) / (n + 0.5) + 10);
      body = (
        <g>
          {head(screen.title ?? 'SCRIPT')}
          {items.map((it, i) => {
            const x = cx - total / 2 + i * (bw + 24);
            const p = fill(i);
            return (
              <g key={i}>
                <rect x={x} y={Y0 + 120} width={bw} height={290} rx={16} fill={PANEL} stroke={p > 0.5 ? Y : DIM} strokeWidth={6} strokeDasharray={p > 0.5 ? undefined : '18 14'} />
                <circle cx={x + 36} cy={Y0 + 156} r={24} fill={p > 0.5 ? Y : DIM} />
                <text x={x + 36} y={Y0 + 168} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={32} fill="#16161F">
                  {i + 1}
                </text>
                <g opacity={p} transform={`translate(0 ${(1 - p) * 20})`}>
                  <Icon kind={it.icon} x={x + bw / 2} y={Y0 + 260} s={1.1} />
                  <text x={x + bw / 2} y={Y0 + 380} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={30} fill={TXT}>
                    {it.label}
                  </text>
                </g>
              </g>
            );
          })}
          <rect x={cx - total / 2} y={Y0 + 450} width={total} height={22} rx={11} fill={PANEL} />
          <rect x={cx - total / 2} y={Y0 + 450} width={total * lin(0, dur)} height={22} rx={11} fill={Y} />
        </g>
      );
      break;
    }
    case 'videos': {
      const items = screen.items;
      const n = items.length;
      const bw = Math.min(230, (Wd - 80 - (n - 1) * 30) / n);
      const total = n * bw + (n - 1) * 30;
      const cols = ['#2F4FBF', '#6B3FB0', '#8A4A3A', '#2F7F6B'];
      body = (
        <g>
          {head(screen.title ?? 'VIDEOS ON THIS TOPIC')}
          {items.map((it, i) => {
            const x = cx - total / 2 + i * (bw + 30);
            const p = pop(i * 7);
            const ok = it.ok === undefined ? undefined : lin(16 + i * 7, 26 + i * 7);
            return (
              <g key={i} opacity={p} transform={`translate(0 ${(1 - p) * 30})`}>
                <rect x={x} y={Y0 + 120} width={bw} height={260} rx={14} fill={cols[i % 4]} />
                <Icon kind="play" x={x + bw / 2} y={Y0 + 250} s={1.1} color="#F4F4F8" />
                {ok !== undefined && (
                  <g opacity={ok}>
                    <circle cx={x + bw - 30} cy={Y0 + 350} r={26} fill={it.ok ? GREEN : RED} />
                    <Icon kind={it.ok ? 'check' : 'cross'} x={x + bw - 30} y={Y0 + 350} s={0.38} color="#F4F4F8" />
                  </g>
                )}
                <text x={x + bw / 2} y={Y0 + 450} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={46} fill={Y}>
                  {it.views}
                </text>
              </g>
            );
          })}
        </g>
      );
      break;
    }
    case 'compare': {
      const p1 = pop(0);
      const p2 = pop(Math.round(dur * 0.4));
      const col = (x: number, title: string, text: string, good: boolean, p: number) => (
        <g opacity={p} transform={`translate(0 ${(1 - p) * 30})`}>
          <rect x={x} y={Y0 + 40} width={(Wd - 90) / 2} height={Hd - 80} rx={18} fill={PANEL} stroke={good ? GREEN : RED} strokeWidth={7} />
          <circle cx={x + 60} cy={Y0 + 104} r={32} fill={good ? GREEN : RED} />
          <Icon kind={good ? 'check' : 'cross'} x={x + 60} y={Y0 + 104} s={0.45} color="#F4F4F8" />
          <text x={x + 110} y={Y0 + 120} fontFamily={FONT} fontWeight={900} fontSize={42} fill={good ? GREEN : RED}>
            {title}
          </text>
          {wrap(text, 17).map((l, i) => (
            <text key={i} x={x + 34} y={Y0 + 210 + i * 52} fontFamily={FONT} fontWeight={800} fontSize={40} fill={TXT}>
              {l}
            </text>
          ))}
        </g>
      );
      body = (
        <g>
          {col(X + 30, 'WRONG', screen.bad, false, p1)}
          {col(X + 60 + (Wd - 90) / 2, 'RIGHT', screen.good, true, p2)}
        </g>
      );
      break;
    }
    case 'list': {
      body = (
        <g>
          {head(screen.title ?? 'CHECKLIST')}
          {screen.items.map((it, i) => {
            const p = lin(6 + i * 12, 16 + i * 12);
            const y = Y0 + 150 + i * 92;
            return (
              <g key={i} opacity={0.35 + 0.65 * p}>
                <rect x={X + 60} y={y - 40} width={60} height={60} rx={12} fill={p > 0.5 ? Y : 'none'} stroke={Y} strokeWidth={6} />
                {p > 0.5 && <Icon kind="check" x={X + 90} y={y - 10} s={0.5} color="#16161F" />}
                <text x={X + 150} y={y + 6} fontFamily={FONT} fontWeight={900} fontSize={44} fill={TXT}>
                  {it}
                </text>
              </g>
            );
          })}
        </g>
      );
      break;
    }
    case 'title': {
      const p = pop();
      body = (
        <g transform={`translate(${cx} ${Y0 + Hd / 2}) scale(${p})`}>
          {wrap(screen.text, 14).map((l, i, a) => (
            <text key={i} x={0} y={(i - (a.length - 1) / 2) * 104 + (screen.sub ? -20 : 30)} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={96} fill={Y}>
              {l}
            </text>
          ))}
          {screen.sub && (
            <text x={0} y={wrap(screen.text, 14).length * 52 + 60} textAnchor="middle" fontFamily={FONT} fontWeight={800} fontSize={42} fill={TXT}>
              {screen.sub}
            </text>
          )}
        </g>
      );
      break;
    }
  }
  return (
    <g>
      <defs>
        <clipPath id="monitor-clip">
          <rect x={X} y={Y0} width={Wd} height={Hd} rx={6} />
        </clipPath>
      </defs>
      <g clipPath="url(#monitor-clip)">
        <rect x={X} y={Y0} width={Wd} height={Hd} fill={BG} />
        {body}
        {/* scanline sheen */}
        <rect x={X} y={Y0} width={Wd} height={Hd} fill="url(#monitor-sheen)" opacity={0.5} />
      </g>
      <defs>
        <linearGradient id="monitor-sheen" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#FFFFFF" stopOpacity={0.06} />
          <stop offset="0.5" stopColor="#FFFFFF" stopOpacity={0} />
        </linearGradient>
      </defs>
    </g>
  );
};
