import React from 'react';
import { INK } from './Character';

/**
 * Full-frame phone close-up held in a hand — for "everyday cringe" comedy beats (wrong chat, seen by 5,
 * "typing…", lock-screen notifications). Drawn into the same 1080x1920 canvas as the other sets.
 * Keep the content above y≈1230: captions sit at y≈1267.
 *
 * set: {"type": "phone", "time": "night", "screen": {
 *   "kind": "chat" | "lock",
 *   "title": "WORK · ALL STAFF", "sub": "48 members", "clock": "02:13",
 *   "msgs": [{"from": "me" | "them", "name": "Boss", "text": "...", "img": "meme" | "dog" | "bit"}],
 *   "seen": "Seen by 5", "typing": "Boss is typing", "draft": "text in the input bar",
 *   "notes": [{"app": "WORK CHAT", "text": "Boss: My office. Monday."}]   // lock screen
 * }}
 * The LAST message (or note) pops in at the start of the shot, so consecutive shots read as a live chat.
 */

export type PhoneMsg = { from?: 'me' | 'them' | 'sys'; name?: string; text?: string; img?: 'meme' | 'dog' | 'bit' };
export type PhoneScreen = {
  kind?: 'chat' | 'lock';
  title?: string;
  sub?: string;
  clock?: string;
  msgs?: PhoneMsg[];
  seen?: string;
  typing?: string;
  draft?: string;
  notes?: { app?: string; text: string }[];
};

const X0 = 150;
const X1 = 930;
const Y0 = 110;
const SW = X1 - X0;

const wrap = (s: string, max: number): string[] => {
  const out: string[] = [];
  let cur = '';
  for (const w of s.split(/\s+/)) {
    if ((cur + ' ' + w).trim().length > max && cur) {
      out.push(cur);
      cur = w;
    } else cur = (cur + ' ' + w).trim();
  }
  if (cur) out.push(cur);
  return out;
};

const pop = (f: number) => {
  const k = Math.min(1, Math.max(0, f / 7));
  return 0.6 + 0.4 * (1 - Math.pow(1 - k, 3)) + Math.sin(k * Math.PI) * 0.08;
};

const Img: React.FC<{ kind: string; w: number; h: number }> = ({ kind, w, h }) => {
  if (kind === 'dog')
    return (
      <g>
        <rect width={w} height={h} rx={18} fill="#FFE7A8" />
        <g transform={`translate(${w / 2} ${h / 2 + 10})`}>
          <ellipse cx={-70} cy={-30} rx={34} ry={60} fill="#8A5A2B" stroke={INK} strokeWidth={6} transform="rotate(20 -70 -30)" />
          <ellipse cx={70} cy={-30} rx={34} ry={60} fill="#8A5A2B" stroke={INK} strokeWidth={6} transform="rotate(-20 70 -30)" />
          <circle r={78} fill="#D9A066" stroke={INK} strokeWidth={7} />
          <circle cx={-28} cy={-12} r={11} fill={INK} />
          <circle cx={28} cy={-12} r={11} fill={INK} />
          <ellipse cx={0} cy={20} rx={18} ry={13} fill={INK} />
          <path d="M -16 40 Q 0 54 16 40" stroke={INK} strokeWidth={6} fill="none" strokeLinecap="round" />
          <path d="M -40 -84 L 0 -150 L 40 -84 Z" fill="#FF5AA5" stroke={INK} strokeWidth={6} strokeLinejoin="round" />
          <circle cx={0} cy={-152} r={10} fill="#FFD400" stroke={INK} strokeWidth={4} />
        </g>
      </g>
    );
  if (kind === 'bit')
    return (
      <g>
        <rect width={w} height={h} rx={18} fill="#BFE3FF" />
        <g transform={`translate(${w / 2} ${h / 2 + 14})`}>
          <line x1={0} y1={-96} x2={0} y2={-130} stroke={INK} strokeWidth={6} />
          <circle cx={0} cy={-134} r={11} fill="#FFD400" stroke={INK} strokeWidth={4} />
          <rect x={-100} y={-96} width={200} height={170} rx={42} fill="#FFFFFF" stroke={INK} strokeWidth={7} />
          <rect x={-78} y={-74} width={156} height={124} rx={28} fill="#151827" />
          <path d="M -50 -20 Q -34 -40 -18 -20" stroke="#FFD400" strokeWidth={9} fill="none" strokeLinecap="round" />
          <path d="M 18 -20 Q 34 -40 50 -20" stroke="#FFD400" strokeWidth={9} fill="none" strokeLinecap="round" />
          <path d="M -26 14 Q 0 34 26 14" stroke="#FFD400" strokeWidth={8} fill="none" strokeLinecap="round" />
          <path d="M 110 -60 l 14 -24 l 14 24 l -14 24 z" fill="#FFD400" stroke={INK} strokeWidth={4} />
        </g>
      </g>
    );
  // meme: two-panel "expectation / reality" card with a tiny stick boss.
  return (
    <g>
      <rect width={w} height={h} rx={18} fill="#FFFFFF" stroke="#D0D4E0" strokeWidth={4} />
      <rect x={14} y={14} width={w - 28} height={h / 2 - 20} rx={10} fill="#E8F3FF" />
      <rect x={14} y={h / 2 + 6} width={w - 28} height={h / 2 - 20} rx={10} fill="#FFE3E3" />
      <text x={w / 2} y={h / 4 + 6} textAnchor="middle" fontFamily="ZyloHead" fontSize={34} fill={INK}>"QUICK 5 MIN CALL"</text>
      <text x={w / 2} y={(3 * h) / 4 - 2} textAnchor="middle" fontFamily="ZyloHead" fontSize={34} fill="#C0262D">THE CALL: 2 HOURS</text>
      <g transform={`translate(${w - 70} ${(3 * h) / 4 + 30})`}>
        <circle r={22} fill="#FFFFFF" stroke={INK} strokeWidth={5} />
        <line x1={0} y1={0} x2={0} y2={-14} stroke={INK} strokeWidth={4} />
        <line x1={0} y1={0} x2={10} y2={6} stroke={INK} strokeWidth={4} />
      </g>
    </g>
  );
};

const Bubble: React.FC<{ m: PhoneMsg; y: number; f: number; live: boolean }> = ({ m, y, f, live }) => {
  if (m.from === 'sys') {
    // centred grey system line: "Bit added Mom to the chat"
    const ls = wrap(m.text ?? '', 30);
    const bw = Math.min(SW - 80, Math.max(...ls.map((l) => l.length)) * 19 + 60);
    const bh = ls.length * 40 + 28;
    const s = live ? pop(f) : 1;
    return (
      <g transform={`translate(540 ${y}) scale(${s}) translate(-540 ${-y})`} opacity={live ? Math.min(1, f / 4) : 1}>
        <rect x={540 - bw / 2} y={y} width={bw} height={bh} rx={bh / 2} fill="#FFF3C4" stroke="#E8D38A" strokeWidth={3} />
        {ls.map((l, i) => (
          <text key={i} x={540} y={y + 46 + i * 40} textAnchor="middle" fontFamily="ZyloBody" fontWeight={800} fontSize={30} fill="#6B5A1E">
            {l}
          </text>
        ))}
      </g>
    );
  }
  const me = m.from !== 'them';
  const lines = m.text ? wrap(m.text, 22) : [];
  const imgW = 470;
  const imgH = m.img ? 300 : 0;
  const nameH = !me && m.name ? 44 : 0;
  const textW = Math.max(...lines.map((l) => l.length), 4) * 25 + 56;
  const bw = m.img ? imgW + 24 : Math.min(SW - 140, textW);
  const bh = nameH + imgH + (m.img && lines.length ? 16 : 0) + lines.length * 52 + (m.img ? 24 : 34);
  const bx = me ? X1 - 30 - bw : X0 + 30;
  const s = live ? pop(f) : 1;
  const ox = me ? bx + bw : bx;
  return (
    <g transform={`translate(${ox} ${y}) scale(${s}) translate(${-ox} ${-y})`} opacity={live ? Math.min(1, f / 4) : 1}>
      <rect x={bx} y={y} width={bw} height={bh} rx={34} fill={me ? '#2F7BFF' : '#ECEEF4'} />
      {nameH > 0 && (
        <text x={bx + 28} y={y + 40} fontFamily="ZyloBody" fontWeight={900} fontSize={30} fill="#E0483B">
          {m.name}
        </text>
      )}
      {m.img && (
        <g transform={`translate(${bx + 12} ${y + 12 + nameH})`}>
          <Img kind={m.img} w={imgW} h={imgH} />
        </g>
      )}
      {lines.map((l, i) => (
        <text key={i} x={bx + 28} y={y + nameH + imgH + (m.img ? 28 : 0) + 58 + i * 52} fontFamily="ZyloBody" fontWeight={800} fontSize={40} fill={me ? '#FFFFFF' : INK}>
          {l}
        </text>
      ))}
    </g>
  );
};

const bubbleH = (m: PhoneMsg) => {
  if (m.from === 'sys') return wrap(m.text ?? '', 30).length * 40 + 28;
  const lines = m.text ? wrap(m.text, 22).length : 0;
  return (m.from === 'them' && m.name ? 44 : 0) + (m.img ? 300 : 0) + (m.img && lines ? 16 : 0) + lines * 52 + (m.img ? 24 : 34);
};

const Chat: React.FC<{ s: PhoneScreen; t: number; f: number }> = ({ s, t, f }) => {
  const msgs = s.msgs ?? [];
  // stack from the bottom of the message area up, so the newest message is always visible
  const bottom = s.typing || s.seen ? 1100 : 1180;
  const ys: number[] = [];
  let y = bottom;
  for (let i = msgs.length - 1; i >= 0; i--) {
    y -= bubbleH(msgs[i]);
    ys[i] = y;
    y -= 22;
  }
  return (
    <g>
      <rect x={X0} y={Y0} width={SW} height={1700} fill="#FFFFFF" />
      <g clipPath="url(#phone-msgs)">
        {msgs.map((m, i) => (
          <Bubble key={i} m={m} y={ys[i]} f={f} live={i === msgs.length - 1} />
        ))}
      </g>
      {/* header */}
      <rect x={X0} y={Y0} width={SW} height={260} fill="#F6F7FB" />
      <line x1={X0} y1={Y0 + 260} x2={X1} y2={Y0 + 260} stroke="#D7DAE4" strokeWidth={4} />
      <text x={X0 + 40} y={Y0 + 190} fontFamily="ZyloBody" fontWeight={900} fontSize={60} fill="#2F7BFF">‹</text>
      <circle cx={X0 + 130} cy={Y0 + 172} r={40} fill="#FFD400" stroke={INK} strokeWidth={5} />
      <text x={X0 + 130} y={Y0 + 186} textAnchor="middle" fontFamily="ZyloHead" fontSize={40} fill={INK}>
        {(s.title ?? 'C').trim().charAt(0)}
      </text>
      <text x={X0 + 190} y={Y0 + 168} fontFamily="ZyloBody" fontWeight={900} fontSize={42} fill={INK}>
        {s.title ?? 'Chat'}
      </text>
      {s.sub && (
        <text x={X0 + 190} y={Y0 + 214} fontFamily="ZyloBody" fontWeight={700} fontSize={30} fill="#7A8094">
          {s.sub}
        </text>
      )}
      {s.seen && (
        <text x={X1 - 40} y={1150} textAnchor="end" fontFamily="ZyloBody" fontWeight={800} fontSize={32} fill="#7A8094">
          {s.seen} ✓✓
        </text>
      )}
      {s.typing && (
        <g transform={`translate(${X0 + 30} 1110)`}>
          <rect width={300} height={70} rx={35} fill="#ECEEF4" />
          {[0, 1, 2].map((i) => (
            <circle key={i} cx={56 + i * 40} cy={35} r={12} fill="#7A8094" opacity={0.35 + 0.65 * Math.max(0, Math.sin(t / 4 - i * 0.9))} />
          ))}
          <text x={320} y={48} fontFamily="ZyloBody" fontWeight={800} fontSize={32} fill="#7A8094">
            {s.typing}…
          </text>
        </g>
      )}
      {/* input bar (sits under the captions, which is fine — it is only texture) */}
      <rect x={X0 + 30} y={1600} width={SW - 160} height={90} rx={45} fill="#F0F1F6" stroke="#D7DAE4" strokeWidth={4} />
      <text x={X0 + 70} y={1660} fontFamily="ZyloBody" fontWeight={700} fontSize={34} fill={s.draft ? INK : '#9AA0B2'}>
        {s.draft ? s.draft + (Math.floor(t / 15) % 2 ? '|' : '') : 'Message'}
      </text>
      <circle cx={X1 - 75} cy={1645} r={42} fill="#2F7BFF" />
      <path d={`M ${X1 - 92} ${1645} L ${X1 - 56} ${1645} M ${X1 - 72} ${1628} L ${X1 - 56} ${1645} L ${X1 - 72} ${1662}`} stroke="#FFFFFF" strokeWidth={7} fill="none" strokeLinecap="round" />
    </g>
  );
};

const Lock: React.FC<{ s: PhoneScreen; time: string; f: number }> = ({ s, time, f }) => {
  const notes = s.notes ?? [];
  const night = time === 'night';
  return (
    <g>
      <defs>
        <linearGradient id="lock-bg" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor={night ? '#1B1F4A' : '#4D7BFF'} />
          <stop offset="1" stopColor={night ? '#4B2A6E' : '#A6C8FF'} />
        </linearGradient>
      </defs>
      <rect x={X0} y={Y0} width={SW} height={1700} fill="url(#lock-bg)" />
      <text x={540} y={470} textAnchor="middle" fontFamily="ZyloHead" fontSize={190} fill="#FFFFFF">
        {s.clock ?? '02:13'}
      </text>
      <text x={540} y={545} textAnchor="middle" fontFamily="ZyloBody" fontWeight={800} fontSize={40} fill="#FFFFFF" opacity={0.8}>
        {s.sub ?? 'Monday'}
      </text>
      {notes.map((n, i) => {
        const live = i === notes.length - 1;
        const y = 640 + i * 190;
        const sc = live ? pop(f) : 1;
        return (
          <g key={i} transform={`translate(540 ${y + 80}) scale(${sc}) translate(-540 ${-(y + 80)})`} opacity={live ? Math.min(1, f / 4) : 1}>
            <rect x={X0 + 30} y={y} width={SW - 60} height={165} rx={36} fill="#FFFFFF" opacity={0.93} />
            <rect x={X0 + 60} y={y + 30} width={56} height={56} rx={14} fill="#2FBF71" />
            <text x={X0 + 140} y={y + 70} fontFamily="ZyloBody" fontWeight={900} fontSize={30} fill="#7A8094">
              {n.app ?? 'MESSAGES'} · now
            </text>
            <text x={X0 + 60} y={y + 132} fontFamily="ZyloBody" fontWeight={900} fontSize={40} fill={INK}>
              {n.text}
            </text>
          </g>
        );
      })}
    </g>
  );
};

export const PhoneSet: React.FC<{ screen?: PhoneScreen; time: string; t: number; f: number }> = ({ screen = {}, time, t, f }) => {
  const night = time === 'night';
  return (
    <g>
      {/* blurred room behind the phone */}
      <rect width={1080} height={1920} fill={night ? '#141832' : '#E9D9B8'} />
      <circle cx={180} cy={300} r={260} fill={night ? '#22285A' : '#F5E8CC'} />
      <circle cx={940} cy={1500} r={340} fill={night ? '#1C2148' : '#DCC79F'} />
      {night && <rect width={1080} height={1920} fill="#4D6BFF" opacity={0.06 + 0.02 * Math.sin(t / 9)} />}
      <defs>
        <clipPath id="phone-screen">
          <rect x={X0} y={Y0} width={SW} height={1700} rx={70} />
        </clipPath>
        <clipPath id="phone-msgs">
          <rect x={X0} y={Y0 + 260} width={SW} height={1000} />
        </clipPath>
      </defs>
      {/* body */}
      <rect x={X0 - 34} y={Y0 - 34} width={SW + 68} height={1768} rx={100} fill="#20232E" stroke={INK} strokeWidth={10} />
      <g clipPath="url(#phone-screen)">
        {screen.kind === 'lock' ? <Lock s={screen} time={time} f={f} /> : <Chat s={screen} t={t} f={f} />}
        {/* status bar */}
        <text x={X0 + 70} y={Y0 + 70} fontFamily="ZyloBody" fontWeight={900} fontSize={34} fill={screen.kind === 'lock' ? '#FFFFFF' : INK}>
          {screen.clock ?? '02:13'}
        </text>
        <rect x={X1 - 120} y={Y0 + 44} width={64} height={30} rx={8} fill="none" stroke={screen.kind === 'lock' ? '#FFFFFF' : INK} strokeWidth={4} />
        <rect x={X1 - 115} y={Y0 + 49} width={30} height={20} rx={4} fill={screen.kind === 'lock' ? '#FFFFFF' : INK} />
      </g>
      <rect x={430} y={Y0 + 22} width={220} height={56} rx={28} fill="#0B0C12" />
      {/* hand: fingers on the left edge, thumb hovering bottom right */}
      {[0, 1, 2].map((i) => (
        <rect key={i} x={X0 - 92} y={1180 + i * 130} width={110} height={100} rx={48} fill="#F2C29A" stroke={INK} strokeWidth={8} />
      ))}
      <path d={`M 1080 1920 L 1080 1480 Q 1000 1440 930 1500 L 820 1640 Q 790 1700 840 1730 L 900 1760 L 900 1920 Z`} fill="#F2C29A" stroke={INK} strokeWidth={8} strokeLinejoin="round" />
      <path d="M 1080 1920 L 1080 1700 Q 1000 1720 960 1920 Z" fill="#2F7BFF" stroke={INK} strokeWidth={8} />
    </g>
  );
};
