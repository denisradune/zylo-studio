import React from 'react';
import { AbsoluteFill, Audio, Easing, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { Captions } from '../../zylo-shared/Captions';
import type { Word } from '../../zylo-shared/types';
import './SiteTour';

/* 9:16 cut of the zylo.video tour for TikTok / Shorts. One big phone shows real mobile screenshots of the
   site; a camera zooms inside the screen, finger taps land on cue words, captions sit below the phone. */

export const VW = 1080;
export const VH = 1920;
const FPS = 30;

const C = {
  night: '#120d2b', night2: '#1d1548', line: '#30276a', hi: '#FFD600', hiInk: '#16112e', text: '#f4f1ff', muted: '#b5addf',
  display: 'ArchivoBlack, "Arial Black", sans-serif', body: 'Archivo, Arial, sans-serif',
};

interface Box { x: number; y: number; w: number; h: number }
export interface VScene { id: string; text: string; seconds: number; words: Word[] }
export type VProps = { scenes: VScene[]; boxes: Record<string, Record<string, Box>>; thumbs: string[] };

const LEAD: Record<string, number> = { vhook: 0.15 };
const TAIL: Record<string, number> = { voutro: 2.2 };
export const vlayout = (p: VProps) => {
  let t = 0;
  const scenes = p.scenes.map((s) => {
    const lead = LEAD[s.id] ?? 0.2;
    const dur = lead + s.seconds + (TAIL[s.id] ?? 0.35);
    const r = { ...s, start: t, lead, dur };
    t += dur;
    return r;
  });
  return { scenes, total: t };
};

const cue = (s: VScene, prefix: string, n = 1) => {
  let k = 0;
  for (const w of s.words) {
    const t = w.text.toLowerCase().replace(/[^a-z0-9']/g, '');
    if (t.startsWith(prefix) && ++k === n) return w.startMs / 1000;
  }
  throw new Error(`cue ${prefix}#${n} missing in ${s.id}`);
};

const ease = Easing.bezier(0.45, 0, 0.2, 1);
const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;

/* phone geometry: screenshots are 390 x 844 CSS px */
const SW = 390;
const SH = 844;
const SCR_H = 1200;
const K = SCR_H / SH;
const SCR_W = SW * K;
const SX = (VW - SCR_W) / 2;
const SY = 132;

interface Cam { t: number; zoom: number; cx: number; cy: number; dur?: number }
interface Shot { t: number; src: string; scroll?: boolean }
interface Hi { t: number; box: Box; until?: number; pad?: number }
interface Tap { t: number; x: number; y: number }

const camAt = (cams: Cam[], t: number) => {
  let i = 0;
  cams.forEach((c, j) => { if (c.t <= t) i = j; });
  const cur = cams[i];
  const from = cams[Math.max(0, i - 1)];
  const p = ease(Math.min(1, Math.max(0, (t - cur.t) / (cur.dur ?? 0.7))));
  const z = from.zoom + (cur.zoom - from.zoom) * p;
  const vw = SW / z / 2;
  const vh = SH / z / 2;
  const cx = Math.min(SW - vw, Math.max(vw, from.cx + (cur.cx - from.cx) * p));
  const cy = Math.min(SH - vh, Math.max(vh, from.cy + (cur.cy - from.cy) * p));
  return { z, cx, cy };
};
const toScreen = (c: { z: number; cx: number; cy: number }, x: number, y: number) => ({
  x: SX + (x - (c.cx - SW / 2 / c.z)) * c.z * K,
  y: SY + (y - (c.cy - SH / 2 / c.z)) * c.z * K,
});
const FULL = (t: number, dur?: number): Cam => ({ t, zoom: 1, cx: SW / 2, cy: SH / 2, dur });
const on = (t: number, b: Box, zoom: number, dur?: number): Cam => ({ t, zoom, cx: b.x + b.w / 2, cy: b.y + b.h / 2, dur });
const mid = (b: Box) => ({ x: b.x + b.w / 2, y: b.y + b.h / 2 });

const Phone: React.FC<{
  t: number; shots: Shot[]; cams: Cam[]; his?: Hi[]; taps?: Tap[]; enter?: boolean; extra?: (t: number) => React.ReactNode; dir?: string;
}> = ({ t, shots, cams, his = [], taps = [], enter, extra, dir = 'mshots' }) => {
  const { fps } = useVideoConfig();
  const cam = camAt(cams, t);
  const inS = enter ? spring({ frame: Math.round((t + 0.15) * fps), fps, config: { damping: 15, stiffness: 140 } }) : 1;
  let si = 0;
  shots.forEach((s, i) => { if (s.t <= t) si = i; });
  return (
    <AbsoluteFill style={{ transform: `translateY(${(1 - inS) * 900}px) rotate(${(1 - inS) * 8}deg)` }}>
      <div style={{ position: 'absolute', left: SX - 16, top: SY - 16, width: SCR_W + 32, height: SCR_H + 32, borderRadius: 76, background: '#05030f', boxShadow: `0 60px 120px -40px rgba(0,0,0,0.9), inset 0 0 0 3px #3a3170` }} />
      <div style={{ position: 'absolute', left: SX, top: SY, width: SCR_W, height: SCR_H, borderRadius: 62, overflow: 'hidden', background: C.night }}>
        <div style={{ position: 'absolute', width: SW, height: SH, transformOrigin: '0 0', transform: `scale(${K * cam.z}) translate(${-(cam.cx - SW / 2 / cam.z)}px, ${-(cam.cy - SH / 2 / cam.z)}px)` }}>
          {shots.map((s, i) => {
            if (i < si - 1 || i > si) return null;
            const since = t - s.t;
            const img = (src: string, style: React.CSSProperties) => <Img src={staticFile(`${dir}/${src}.jpg`)} style={{ position: 'absolute', width: SW, height: SH, ...style }} />;
            if (s.scroll && i === si && since < 0.7) {
              const p = ease(Math.max(0, since / 0.7));
              return <React.Fragment key={i}>{img(shots[i - 1].src, { transform: `translateY(${-p * SH}px)` })}{img(s.src, { transform: `translateY(${(1 - p) * SH}px)` })}</React.Fragment>;
            }
            return <React.Fragment key={i}>{img(s.src, { opacity: i === si && shots[si - 1] && !s.scroll ? interpolate(since, [0, 0.1], [0, 1], clamp) : 1 })}</React.Fragment>;
          })}
          {extra?.(t)}
        </div>
      </div>
      {his.map((h, i) => {
        if (t < h.t || (h.until !== undefined && t > h.until + 0.25)) return null;
        const pad = h.pad ?? 5;
        const a = toScreen(cam, h.box.x - pad, h.box.y - pad);
        const b = toScreen(cam, h.box.x + h.box.w + pad, h.box.y + h.box.h + pad);
        const s = spring({ frame: Math.round((t - h.t) * fps), fps, config: { damping: 14, stiffness: 170 } });
        const out = h.until !== undefined ? interpolate(t, [h.until, h.until + 0.25], [1, 0], clamp) : 1;
        return <div key={i} style={{ position: 'absolute', left: a.x, top: a.y, width: b.x - a.x, height: b.y - a.y, borderRadius: 22, border: `7px solid ${C.hi}`, boxShadow: '0 0 50px rgba(255,214,0,0.6)', transform: `scale(${0.9 + 0.1 * s})`, opacity: s * out }} />;
      })}
      {taps.map((tp, i) => {
        const d = t - tp.t;
        if (d < -0.35 || d > 0.7) return null;
        const p = toScreen(cam, tp.x, tp.y);
        const appear = interpolate(d, [-0.35, -0.1], [0, 1], clamp) * interpolate(d, [0.4, 0.7], [1, 0], clamp);
        const press = interpolate(d, [-0.05, 0.05, 0.25], [1, 0.75, 1], clamp);
        const ring = Math.max(0, d) / 0.6;
        return (
          <React.Fragment key={i}>
            <div style={{ position: 'absolute', left: p.x - 46, top: p.y - 46, width: 92, height: 92, borderRadius: 46, background: 'rgba(255,255,255,0.85)', boxShadow: '0 8px 24px rgba(0,0,0,0.45)', opacity: appear, transform: `scale(${press})` }} />
            {d >= 0 && <div style={{ position: 'absolute', left: p.x - 80, top: p.y - 80, width: 160, height: 160, borderRadius: 80, border: `7px solid ${C.hi}`, transform: `scale(${0.3 + ring})`, opacity: 1 - ring }} />}
          </React.Fragment>
        );
      })}
    </AbsoluteFill>
  );
};

type SP = { s: VScene & { lead: number; dur: number }; p: VProps };
const useT = (lead: number) => useCurrentFrame() / useVideoConfig().fps - lead;

const Sticker: React.FC<{ show: number; t: number }> = ({ show, t }) => {
  const { fps } = useVideoConfig();
  const s = spring({ frame: Math.round((t - show) * fps), fps, config: { damping: 10, stiffness: 150 } });
  return (
    <div style={{ position: 'absolute', left: 0, right: 0, top: SY + SCR_H - 40, display: 'flex', justifyContent: 'center', opacity: s }}>
      <div style={{ fontFamily: C.display, fontSize: 92, background: C.hi, color: C.hiInk, padding: '6px 34px 14px', borderRadius: 22, transform: `rotate(-4deg) scale(${s})`, boxShadow: '0 24px 60px rgba(0,0,0,0.55)' }}>zylo.video</div>
    </div>
  );
};

const Hook: React.FC<SP> = ({ s, p }) => {
  const t = useT(s.lead);
  const b = p.boxes.archive;
  const url = cue(s, 'zylo', 2);
  return (
    <AbsoluteFill>
      <Phone t={t} enter shots={[{ t: -1, src: 'archive' }]} cams={[FULL(-1), on(cue(s, 'place') - 0.2, b.head, 1.1, 0.6), FULL(url - 0.5, 0.7)]} his={[{ t: cue(s, 'every'), box: b.head, until: url - 0.6, pad: 6 }]} />
      <Sticker show={url} t={t} />
    </AbsoluteFill>
  );
};

const Hero: React.FC<SP> = ({ s, p }) => {
  const t = useT(s.lead);
  const b = p.boxes.hero_0;
  const first = cue(s, 'one');
  const starts = s.words.filter((w) => w.startMs / 1000 >= first - 0.01).slice(0, 11).map((w) => w.startMs / 1000);
  return <Phone t={t} shots={[{ t: -1, src: 'hero_0' }, ...starts.map((x, i) => ({ t: x, src: `hero_${i + 1}` }))]} cams={[FULL(-1), on(cue(s, 'slogan') - 0.2, b.h1, 1.06, 0.8)]} his={[{ t: cue(s, 'slogan'), box: b.h1, until: first - 0.25, pad: 6 }]} />;
};

const Archive: React.FC<SP> = ({ s, p }) => {
  const t = useT(s.lead);
  const g = p.boxes.grid;
  return (
    <Phone t={t} shots={[{ t: -1, src: 'hero_11' }, { t: cue(s, 'scroll') + 0.1, src: 'grid', scroll: true }]} cams={[FULL(-1), on(cue(s, 'new') - 0.2, g.first, 1.5, 0.6)]}
      his={[{ t: cue(s, 'every'), box: { ...g.first, w: g.second.x + g.second.w - g.first.x }, until: cue(s, 'new') - 0.1, pad: 5 }, { t: cue(s, 'new') + 0.1, box: g.newtag, pad: 4 }]} />
  );
};

const Find: React.FC<SP> = ({ s, p }) => {
  const t = useT(s.lead);
  const c = p.boxes.chips;
  const pick = cue(s, 'rubric');
  const search = cue(s, 'search');
  const z = cue(s, 'zombie');
  return (
    <Phone t={t} shots={[{ t: -1, src: 'chips' }, { t: pick + 0.25, src: 'chips_history' }, { t: z + 0.45, src: 'search' }]}
      cams={[on(-1, c.chips, 1.08), on(search - 0.1, c.q, 1.1, 0.5), FULL(z + 0.4, 0.6)]}
      his={[{ t: pick, box: c.history, until: search - 0.15, pad: 4 }, { t: cue(s, 'every') - 0.1, box: { x: 8, y: 130, w: 374, h: 330 }, pad: 2 }]}
      taps={[{ t: pick, ...mid(c.history) }, { t: search + 0.1, ...mid(c.q) }]}
      extra={(tt) => {
        if (tt < search + 0.2 || tt > z + 0.45) return null;
        const n = Math.floor(interpolate(tt, [cue(s, 'type'), z + 0.35], [0, 6], clamp));
        return <div style={{ position: 'absolute', left: c.q.x + 40, top: c.q.y + 2, width: c.q.w - 56, height: c.q.h - 4, background: '#171137', display: 'flex', alignItems: 'center', fontFamily: C.body, fontWeight: 500, fontSize: 15, color: C.text }}>{'zombie'.slice(0, n)}<span style={{ width: 2, height: 18, background: C.text, marginLeft: 1 }} /></div>;
      }} />
  );
};

const Player: React.FC<SP> = ({ s, p }) => {
  const t = useT(s.lead);
  const card = p.boxes.player_before.card;
  const pl = p.boxes.player.player;
  const tap = cue(s, 'tap') + 0.25;
  return (
    <Phone t={t} shots={[{ t: -1, src: 'player_before' }, { t: tap + 0.2, src: 'player' }]} cams={[on(-1, card, 1.3), FULL(tap + 0.2, 0.5)]} taps={[{ t: tap, ...mid(card) }]}
      extra={(tt) => tt > tap + 0.2 ? (
        <div style={{ position: 'absolute', left: pl.x, top: pl.y, width: pl.w, height: pl.h, borderRadius: 22, overflow: 'hidden', background: '#000' }}>
          <Img src={staticFile('thumbs/C3nffxC5ZKM.jpg')} style={{ width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${1.02 + (tt - tap) * 0.03})` }} />
          <div style={{ position: 'absolute', left: 12, right: 12, bottom: 14, height: 4, borderRadius: 4, background: 'rgba(255,255,255,0.3)' }}><div style={{ width: `${Math.min(100, (tt - tap) * 14)}%`, height: '100%', background: '#ff2e4d', borderRadius: 4 }} /></div>
        </div>) : null} />
  );
};

const Suggest: React.FC<SP> = ({ s, p }) => {
  const t = useT(s.lead);
  const b = p.boxes.suggest;
  return (
    <Phone t={t} shots={[{ t: -1, src: 'suggest' }]} cams={[on(-1, b.idea, 1.08), on(cue(s, 'best') - 0.3, b.send, 1.08, 0.6)]}
      his={[{ t: cue(s, 'idea'), box: b.idea, until: cue(s, 'send') - 0.1, pad: 4 }, { t: cue(s, 'send'), box: b.topic, until: cue(s, 'best') - 0.2, pad: 4 }, { t: cue(s, 'best'), box: b.send, pad: 4 }]}
      taps={[{ t: cue(s, 'best') + 0.45, ...mid(b.send) }]} />
  );
};

const Ask: React.FC<SP> = ({ s, p }) => {
  const t = useT(s.lead);
  const b = p.boxes.ask;
  return (
    <Phone t={t} shots={[{ t: -1, src: 'ask' }]} cams={[FULL(-1), on(cue(s, 'ask') - 0.2, { ...b.q, h: b.ask.y + b.ask.h - b.q.y }, 1.1, 0.6), on(cue(s, 'short') - 0.2, b.samples, 1.08, 0.6)]}
      his={[{ t: cue(s, 'ask'), box: b.q, until: cue(s, 'get') - 0.1, pad: 4 }, { t: cue(s, 'short'), box: b.samples, pad: 6 }]}
      taps={[{ t: cue(s, 'get'), ...mid(b.ask) }]} />
  );
};

const Theme: React.FC<SP> = ({ s }) => {
  const t = useT(s.lead);
  const lt = cue(s, 'light');
  const mix = ease(interpolate(t, [cue(s, 'dark'), lt + 0.3], [0, 1], clamp));
  return (
    <Phone t={t} shots={[{ t: -1, src: 'dark_grid' }]} cams={[FULL(-1)]}
      extra={() => <Img src={staticFile('mshots/light_grid.jpg')} style={{ position: 'absolute', width: SW, height: SH, clipPath: `inset(0 0 ${100 - mix * 100}% 0)` }} />} />
  );
};

const Outro: React.FC<SP> = ({ s, p }) => {
  const t = useT(s.lead);
  const { fps } = useVideoConfig();
  const sp = (d: number, damping = 14) => spring({ frame: Math.round((t - d) * fps), fps, config: { damping } });
  const follow = cue(s, 'follow');
  const clicked = t > follow + 0.3;
  const k = sp(follow - 0.2, 11);
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ overflow: 'hidden', opacity: 0.35 }}>
        <div style={{ position: 'absolute', left: -200, top: -300, width: VW + 400, display: 'flex', flexWrap: 'wrap', gap: 20, transform: `rotate(-8deg) translateY(${-f * 1.2}px)` }}>
          {Array.from({ length: 30 }, (_, i) => <Img key={i} src={staticFile(`thumbs/${p.thumbs[i % p.thumbs.length]}.jpg`)} style={{ width: 250, height: 444, objectFit: 'cover', borderRadius: 24 }} />)}
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{ background: 'radial-gradient(ellipse at 50% 42%, rgba(18,13,43,0.55), rgba(18,13,43,0.96) 70%)' }} />
      <AbsoluteFill style={{ alignItems: 'center', paddingTop: 470, flexDirection: 'column', gap: 40 }}>
        <div style={{ fontFamily: C.display, fontSize: 150, background: C.hi, color: C.hiInk, padding: '10px 46px 22px', borderRadius: 32, transform: `rotate(-4deg) scale(${sp(-0.1, 10)})` }}>zylo</div>
        <div style={{ fontFamily: C.display, fontSize: 120, color: C.text, letterSpacing: -3, opacity: sp(0.2) }}>.video</div>
        <div style={{ marginTop: 50, transform: `scale(${k * (t > follow && t < follow + 0.35 ? 0.92 : 1)})`, opacity: k, background: clicked ? '#2b2066' : C.hi, color: clicked ? C.text : C.hiInk, fontFamily: C.body, fontWeight: 800, fontSize: 64, padding: '28px 70px', borderRadius: 99, boxShadow: clicked ? 'none' : '0 20px 60px -10px rgba(255,214,0,0.6)' }}>
          {clicked ? 'Following ✓' : '+ Follow'}
        </div>
        <div style={{ fontFamily: C.body, fontWeight: 700, fontSize: 40, letterSpacing: 6, textTransform: 'uppercase', color: C.muted, opacity: sp(cue(s, 'every')), textAlign: 'center', width: 900 }}>A new “What if…?” every day</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const MAP: Record<string, React.FC<SP>> = { vhook: Hook, vhero: Hero, varchive: Archive, vfind: Find, vplayer: Player, vsuggest: Suggest, vask: Ask, vtheme: Theme, voutro: Outro };

export const TourVertical: React.FC<VProps> = (p) => {
  const frame = useCurrentFrame();
  const { scenes, total } = vlayout(p);
  const music = interpolate(frame, [0, 10, (total - 1.5) * FPS, total * FPS], [0.1, 0.15, 0.15, 0], clamp);
  return (
    <AbsoluteFill style={{ background: C.night }}>
      <AbsoluteFill style={{ background: `radial-gradient(900px 900px at 75% ${15 + Math.sin(frame / 80) * 5}%, rgba(91,61,245,0.45), transparent 70%)` }} />
      <AbsoluteFill style={{ backgroundImage: 'radial-gradient(rgba(244,241,255,0.12) 2px, transparent 2.4px)', backgroundSize: '36px 36px', WebkitMaskImage: 'linear-gradient(180deg,#000,transparent 80%)' }} />
      <Audio src={staticFile('audio/music.mp3')} volume={music} />
      {scenes.map((s) => {
        const Comp = MAP[s.id];
        return (
          <Sequence key={s.id} from={Math.round(s.start * FPS)} durationInFrames={Math.round(s.dur * FPS)} name={s.id}>
            <Comp s={s} p={p} />
            <Sequence from={Math.round(s.lead * FPS)}><Audio src={staticFile(`vaudio/${s.id}/voiceover.mp3`)} /></Sequence>
            <Captions words={s.words} offsetMs={s.lead * 1000} centerY={s.id === "voutro" ? 0.86 : 0.775} fontSize={92} maxWords={3} maxChars={18} maxWidth={940} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
