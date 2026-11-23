import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  continueRender,
  delayRender,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  Easing,
} from 'remotion';
import { Captions } from '../../zylo-shared/Captions';
import type { Word } from '../../zylo-shared/types';

/* zylo.video tour: a 16:9 walkthrough of the site built from real screenshots.
   Night-indigo stage like the site, a browser window with a camera that zooms to what the voice talks about,
   a cursor that clicks on cue, yellow highlight boxes, and word-by-word captions. Every event is cued
   to a word in the voiceover, so picture and voice stay in sync. */

export const FPS = 30;
export const W = 1920;
export const H = 1080;

const C = {
  night: '#120d2b',
  night2: '#1d1548',
  line: '#30276a',
  violet: '#5b3df5',
  hi: '#FFD600',
  hiInk: '#16112e',
  text: '#f4f1ff',
  muted: '#b5addf',
  display: 'ArchivoBlack, "Arial Black", sans-serif',
  body: 'Archivo, Arial, sans-serif',
};

/* ---------- fonts of the site (Archivo Black + Archivo), loaded from public/fonts ---------- */
const loadSiteFonts = () => {
  if (typeof document === 'undefined') return;
  const h = delayRender('site fonts');
  const faces = [
    new FontFace('ArchivoBlack', `url(${staticFile('fonts/ArchivoBlack-400.woff')})`, { weight: '400' }),
    new FontFace('Archivo', `url(${staticFile('fonts/Archivo-500.woff')})`, { weight: '500' }),
    new FontFace('Archivo', `url(${staticFile('fonts/Archivo-700.woff')})`, { weight: '700' }),
  ];
  Promise.all(faces.map((f) => f.load().then((ff) => document.fonts.add(ff))))
    .then(() => continueRender(h))
    .catch(() => continueRender(h));
};
loadSiteFonts();

/* ---------- props ---------- */
export interface SceneData {
  id: string;
  chapter: string;
  text: string;
  seconds: number;
  words: Word[];
}
export type TourProps = {
  scenes: SceneData[];
  boxes: Record<string, Record<string, Box>>;
  thumbs: string[];
};
interface Box { x: number; y: number; w: number; h: number }

/* ---------- timeline ---------- */
const LEAD: Record<string, number> = { intro: 1.3 };
const TAIL: Record<string, number> = { outro: 3.2, intro: 0.4 };
export const layout = (p: TourProps) => {
  let t = 0;
  const placed = p.scenes.map((s) => {
    const lead = LEAD[s.id] ?? 0.35;
    const dur = lead + s.seconds + (TAIL[s.id] ?? 0.55);
    const r = { ...s, start: t, lead, dur };
    t += dur;
    return r;
  });
  return { scenes: placed, total: t };
};

/** Seconds (relative to the scene's voiceover start) of the n-th word starting with `prefix`. */
const cue = (s: SceneData, prefix: string, n = 1): number => {
  let k = 0;
  for (const w of s.words) {
    const t = w.text.toLowerCase().replace(/[^a-z0-9']/g, '');
    if (t.startsWith(prefix.toLowerCase()) && ++k === n) return w.startMs / 1000;
  }
  throw new Error(`cue "${prefix}"#${n} not found in ${s.id}`);
};

const ease = Easing.bezier(0.45, 0, 0.2, 1);
const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;

/* ---------- background stage ---------- */
const Stage: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: C.night }}>
      <AbsoluteFill
        style={{
          background: `radial-gradient(900px 700px at ${70 + Math.sin(f / 90) * 6}% ${18 + Math.cos(f / 110) * 6}%, rgba(91,61,245,0.42), transparent 70%)`,
        }}
      />
      <AbsoluteFill
        style={{
          backgroundImage: 'radial-gradient(rgba(244,241,255,0.13) 1.3px, transparent 1.6px)',
          backgroundSize: '26px 26px',
          backgroundPosition: `0 ${(-f * 0.3) % 26}px`,
          WebkitMaskImage: 'linear-gradient(180deg, #000, transparent 90%)',
        }}
      />
    </AbsoluteFill>
  );
};

/* ---------- browser window with camera ---------- */
const FRAME_W = 1500;
const SHOT_W = 1600;
const SHOT_H = 900;
const F = FRAME_W / SHOT_W;
const FRAME_H = SHOT_H * F;
const BAR = 42;
const FX = (W - FRAME_W) / 2;
const FY = 34 + BAR;

interface Cam { t: number; zoom: number; cx: number; cy: number; dur?: number }
interface Shot { t: number; src: string; scroll?: boolean }
interface Hi { t: number; box: Box; until?: number; pad?: number }
interface Pt { t: number; x: number; y: number; click?: boolean }

const camAt = (cams: Cam[], t: number) => {
  let cur = cams[0];
  let prev = cams[0];
  for (const c of cams) if (c.t <= t) { prev = cur; cur = c; }
  const idx = cams.indexOf(cur);
  const from = idx > 0 ? cams[idx - 1] : cur;
  const d = cur.dur ?? 0.9;
  const p = ease(Math.min(1, Math.max(0, (t - cur.t) / d)));
  void prev;
  const z = from.zoom + (cur.zoom - from.zoom) * p;
  let cx = from.cx + (cur.cx - from.cx) * p;
  let cy = from.cy + (cur.cy - from.cy) * p;
  const vw = SHOT_W / z / 2;
  const vh = SHOT_H / z / 2;
  cx = Math.min(SHOT_W - vw, Math.max(vw, cx));
  cy = Math.min(SHOT_H - vh, Math.max(vh, cy));
  return { z, cx, cy };
};

/** Maps a point in screenshot CSS px to frame (video) px for the current camera. */
const toScreen = (cam: { z: number; cx: number; cy: number }, x: number, y: number) => ({
  x: FX + (x - (cam.cx - SHOT_W / 2 / cam.z)) * cam.z * F,
  y: FY + (y - (cam.cy - SHOT_H / 2 / cam.z)) * cam.z * F,
});

const Cursor: React.FC<{ pts: Pt[]; t: number; cam: { z: number; cx: number; cy: number } }> = ({ pts, t, cam }) => {
  if (!pts.length || t < pts[0].t - 0.4) return null;
  let i = 0;
  while (i < pts.length - 1 && pts[i + 1].t <= t) i++;
  const a = pts[i];
  const b = pts[i + 1];
  let x = a.x;
  let y = a.y;
  if (b) {
    const travel = Math.min(0.8, b.t - a.t);
    const p = ease(Math.min(1, Math.max(0, (t - (b.t - travel)) / travel)));
    x = a.x + (b.x - a.x) * p;
    y = a.y + (b.y - a.y) * p;
  }
  const s = toScreen(cam, x, y);
  const fadeIn = interpolate(t, [pts[0].t - 0.4, pts[0].t - 0.1], [0, 1], clamp);
  const click = pts.filter((p) => p.click && t >= p.t && t < p.t + 0.6).pop();
  const ct = click ? (t - click.t) / 0.6 : 1;
  const press = click ? interpolate(ct, [0, 0.15, 0.4], [1, 0.82, 1], clamp) : 1;
  return (
    <>
      {click && (
        <div
          style={{
            position: 'absolute',
            left: s.x,
            top: s.y,
            width: 120,
            height: 120,
            marginLeft: -60,
            marginTop: -60,
            borderRadius: '50%',
            border: `5px solid ${C.hi}`,
            transform: `scale(${0.2 + ct * 0.9})`,
            opacity: 1 - ct,
          }}
        />
      )}
      <svg
        width={46}
        height={46}
        viewBox="0 0 24 24"
        style={{
          position: 'absolute',
          left: s.x - 7,
          top: s.y - 4,
          opacity: fadeIn,
          transform: `scale(${press})`,
          transformOrigin: '7px 4px',
          filter: 'drop-shadow(0 6px 10px rgba(0,0,0,0.5))',
        }}
      >
        <path d="M4 2.5 L4 19.5 L8.6 15.4 L11.6 22 L14.6 20.7 L11.7 14.2 L18 14.2 Z" fill="#fff" stroke="#120d2b" strokeWidth="1.4" strokeLinejoin="round" />
      </svg>
    </>
  );
};

const Highlight: React.FC<{ h: Hi; t: number; cam: { z: number; cx: number; cy: number } }> = ({ h, t, cam }) => {
  const { fps } = useVideoConfig();
  if (t < h.t || (h.until !== undefined && t > h.until + 0.3)) return null;
  const pad = h.pad ?? 8;
  const a = toScreen(cam, h.box.x - pad, h.box.y - pad);
  const b = toScreen(cam, h.box.x + h.box.w + pad, h.box.y + h.box.h + pad);
  const s = spring({ frame: Math.round((t - h.t) * fps), fps, config: { damping: 14, stiffness: 160 } });
  const out = h.until !== undefined ? interpolate(t, [h.until, h.until + 0.3], [1, 0], clamp) : 1;
  const pulse = 1 + Math.sin((t - h.t) * 5) * 0.012;
  return (
    <div
      style={{
        position: 'absolute',
        left: a.x,
        top: a.y,
        width: b.x - a.x,
        height: b.y - a.y,
        borderRadius: 18,
        border: `5px solid ${C.hi}`,
        boxShadow: `0 0 0 9999px rgba(10,7,28,${0.42 * s * out}), 0 0 40px rgba(255,214,0,0.55)`,
        transform: `scale(${(0.9 + 0.1 * s) * pulse})`,
        opacity: s * out,
      }}
    />
  );
};

const Browser: React.FC<{
  t: number;
  shots: Shot[];
  cams: Cam[];
  his?: Hi[];
  cursor?: Pt[];
  enter?: boolean;
  chapterNo?: number;
  chapter?: string;
  extra?: (t: number) => React.ReactNode;
}> = ({ t, shots, cams, his = [], cursor = [], enter, chapterNo, chapter, extra }) => {
  const { fps } = useVideoConfig();
  const cam = camAt(cams, t);
  const inS = enter ? spring({ frame: Math.round(t * fps), fps, config: { damping: 18 } }) : 1;
  let si = 0;
  shots.forEach((s, i) => { if (s.t <= t) si = i; });
  const chapIn = spring({ frame: Math.round(t * fps) - 4, fps, config: { damping: 16 } });
  return (
    <AbsoluteFill style={{ transform: `translateY(${(1 - inS) * 700}px) scale(${0.9 + 0.1 * inS})`, opacity: inS }}>
      <div
        style={{
          position: 'absolute',
          left: FX - 2,
          top: FY - BAR - 2,
          width: FRAME_W + 4,
          height: FRAME_H + BAR + 4,
          borderRadius: 22,
          background: '#0a0720',
          boxShadow: `0 40px 90px -30px rgba(0,0,0,0.85), 0 0 0 2px ${C.line}`,
        }}
      />
      <div style={{ position: 'absolute', left: FX, top: FY - BAR, width: FRAME_W, height: BAR, display: 'flex', alignItems: 'center', gap: 9, paddingLeft: 18 }}>
        {['#ff5f57', '#febc2e', '#28c840'].map((c) => (
          <i key={c} style={{ width: 13, height: 13, borderRadius: 7, background: c, display: 'block' }} />
        ))}
        <div
          style={{
            marginLeft: 22,
            background: '#1a1440',
            color: C.muted,
            fontFamily: C.body,
            fontWeight: 500,
            fontSize: 19,
            padding: '5px 22px',
            borderRadius: 99,
            width: 520,
            textAlign: 'center',
          }}
        >
          <span style={{ color: '#7ee2a8' }}>🔒 </span>zylo.video
        </div>
        {chapter && (
          <div
            style={{
              marginLeft: 'auto',
              marginRight: 16,
              display: 'flex',
              alignItems: 'center',
              gap: 10,
              fontFamily: C.body,
              fontWeight: 700,
              fontSize: 19,
              color: C.text,
              opacity: chapIn,
              transform: `translateX(${(1 - chapIn) * 30}px)`,
            }}
          >
            <span style={{ background: C.hi, color: C.hiInk, borderRadius: 7, padding: '2px 9px', fontFamily: C.display, fontSize: 17 }}>
              {String(chapterNo).padStart(2, '0')}
            </span>
            {chapter}
          </div>
        )}
      </div>
      <div style={{ position: 'absolute', left: FX, top: FY, width: FRAME_W, height: FRAME_H, overflow: 'hidden', borderRadius: '0 0 20px 20px', background: C.night }}>
        <div
          style={{
            position: 'absolute',
            left: 0,
            top: 0,
            width: SHOT_W,
            height: SHOT_H,
            transformOrigin: '0 0',
            transform: `scale(${F * cam.z}) translate(${-(cam.cx - SHOT_W / 2 / cam.z)}px, ${-(cam.cy - SHOT_H / 2 / cam.z)}px)`,
          }}
        >
          {shots.map((s, i) => {
            if (i < si - 1 || i > si) return null;
            const since = t - s.t;
            if (s.scroll && i === si && since < 0.9) {
              const p = ease(Math.max(0, since / 0.9));
              return (
                <React.Fragment key={i}>
                  <Img src={staticFile(`shots/${shots[i - 1].src}.jpg`)} style={{ position: 'absolute', width: SHOT_W, height: SHOT_H, transform: `translateY(${-p * SHOT_H}px)` }} />
                  <Img src={staticFile(`shots/${s.src}.jpg`)} style={{ position: 'absolute', width: SHOT_W, height: SHOT_H, transform: `translateY(${(1 - p) * SHOT_H}px)` }} />
                </React.Fragment>
              );
            }
            const op = i === si ? interpolate(since, [0, 0.12], [shots[si - 1] && !s.scroll ? 0 : 1, 1], clamp) : 1;
            return <Img key={i} src={staticFile(`shots/${s.src}.jpg`)} style={{ position: 'absolute', width: SHOT_W, height: SHOT_H, opacity: op }} />;
          })}
          {extra?.(t)}
        </div>
      </div>
      {his.map((h, i) => <Highlight key={i} h={h} t={t} cam={cam} />)}
      <Cursor pts={cursor} t={t} cam={cam} />
    </AbsoluteFill>
  );
};

/* ---------- helpers ---------- */
const center = (b: Box) => ({ x: b.x + b.w / 2, y: b.y + b.h / 2 });
const camOn = (t: number, b: Box, zoom: number, dur?: number): Cam => ({ t, zoom, cx: b.x + b.w / 2, cy: b.y + b.h / 2, dur });
const FULL = (t: number, dur?: number): Cam => ({ t, zoom: 1, cx: 800, cy: 450, dur });

/* ---------- thumbnail wall for intro/outro ---------- */
const ThumbWall: React.FC<{ thumbs: string[]; dim: number; blur?: number }> = ({ thumbs, dim, blur = 0 }) => {
  const f = useCurrentFrame();
  const cols = 8;
  return (
    <AbsoluteFill style={{ overflow: 'hidden' }}>
      <div style={{ position: 'absolute', left: -260, top: -380, width: W + 520, height: H + 760, transform: 'rotate(-9deg)', display: 'flex', gap: 22, filter: blur ? `blur(${blur}px)` : undefined }}>
        {Array.from({ length: cols }, (_, c) => {
          const dir = c % 2 ? 1 : -1;
          const off = ((f * 0.9 * dir) % 2400) - (dir > 0 ? 2400 : 0);
          return (
            <div key={c} style={{ display: 'flex', flexDirection: 'column', gap: 22, transform: `translateY(${off + c * 70}px)` }}>
              {Array.from({ length: 10 }, (_, r) => {
                const id = thumbs[(c * 7 + r * 3) % thumbs.length];
                return <Img key={r} src={staticFile(`thumbs/${id}.jpg`)} style={{ width: 250, height: 444, objectFit: 'cover', borderRadius: 22, display: 'block' }} />;
              })}
            </div>
          );
        })}
      </div>
      <AbsoluteFill style={{ background: `radial-gradient(ellipse at center, rgba(18,13,43,${dim * 0.75}) 0%, rgba(18,13,43,${dim}) 62%)` }} />
    </AbsoluteFill>
  );
};

const Logo: React.FC<{ size: number; s: number; rot?: number }> = ({ size, s, rot = -3 }) => (
  <div
    style={{
      fontFamily: C.display,
      fontSize: size,
      lineHeight: 1,
      background: C.hi,
      color: C.hiInk,
      padding: `${size * 0.12}px ${size * 0.3}px ${size * 0.16}px`,
      borderRadius: size * 0.2,
      transform: `rotate(${rot}deg) scale(${s})`,
      display: 'inline-block',
      boxShadow: '0 30px 60px -20px rgba(0,0,0,0.6)',
    }}
  >
    zylo
  </div>
);

/* ---------- scenes ---------- */
type SceneProps = { s: SceneData & { lead: number; dur: number }; p: TourProps; no: number };

const useT = (lead: number) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  return f / fps - lead;
};

const Intro: React.FC<SceneProps> = ({ s, p }) => {
  const t = useT(s.lead);
  const { fps } = useVideoConfig();
  const fr = (x: number) => Math.round((t - x) * fps);
  const logo = spring({ frame: fr(-1.1), fps, config: { damping: 11, stiffness: 120 } });
  const url = 'zylo.video';
  const typeAt = cue(s, 'zylo', 2);
  const chars = Math.floor(interpolate(t, [typeAt, typeAt + 0.9], [0, url.length], clamp));
  const sub = spring({ frame: fr(cue(s, 'everything')), fps, config: { damping: 16 } });
  const urlIn = spring({ frame: fr(typeAt - 0.2), fps, config: { damping: 15 } });
  const out = interpolate(t, [s.seconds + 0.05, s.seconds + 0.4], [1, 0], clamp);
  return (
    <AbsoluteFill style={{ opacity: out }}>
      <ThumbWall thumbs={p.thumbs} dim={interpolate(t, [-1.3, 0.5], [0.55, 0.86], clamp)} />
      <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 34, paddingBottom: 90 }}>
        <Logo size={150} s={logo} />
        <div style={{ height: 120, display: 'flex', alignItems: 'center', opacity: urlIn, transform: `translateY(${(1 - urlIn) * 30}px)` }}>
          <span style={{ fontFamily: C.display, fontSize: 124, color: C.text, letterSpacing: -3 }}>
            {url.slice(0, chars)}
            <span style={{ display: 'inline-block', width: 8, height: 100, marginLeft: 8, background: C.hi, verticalAlign: '-8px', opacity: Math.floor(t * 2.5) % 2 || chars < url.length ? 1 : 0 }} />
          </span>
        </div>
        <div
          style={{
            fontFamily: C.body,
            fontWeight: 700,
            fontSize: 34,
            letterSpacing: 8,
            textTransform: 'uppercase',
            color: C.muted,
            opacity: sub,
            transform: `translateY(${(1 - sub) * 20}px)`,
          }}
        >
          The full tour · everything you can do
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const HeroScene: React.FC<SceneProps> = ({ s, p, no }) => {
  const t = useT(s.lead);
  const b = p.boxes.hero_0;
  const first = cue(s, 'one');
  const realStarts = s.words.filter((w) => w.startMs / 1000 >= first - 0.01).slice(0, 11).map((w) => w.startMs / 1000);
  const shots: Shot[] = [{ t: -1, src: 'hero_0' }, ...realStarts.map((x, i) => ({ t: x, src: `hero_${i + 1}` }))];
  return (
    <Browser
      t={t}
      enter
      chapterNo={no}
      chapter={s.chapter}
      shots={shots}
      cams={[FULL(-1), camOn(cue(s, 'slogan'), b.h1, 1.55, 1.4), camOn(first - 0.2, b.h1, 1.75, 1.2)]}
      his={[{ t: cue(s, 'slogan') + 0.4, box: b.h1, until: first - 0.3, pad: 14 }]}
    />
  );
};

const StatsScene: React.FC<SceneProps> = ({ s, p, no }) => {
  const t = useT(s.lead);
  const b = p.boxes.hero_0;
  const front = b.phones;
  const tap = cue(s, 'tap');
  return (
    <Browser
      t={t}
      chapterNo={no}
      chapter={s.chapter}
      shots={[{ t: -1, src: 'hero_0' }]}
      cams={[camOn(-1, b.h1, 1.75), camOn(cue(s, 'glance') - 0.6, { ...b.stats, y: b.stats.y - 160, h: 260 }, 1.9, 1.1), camOn(cue(s, 'stack') - 0.6, front, 1.45, 1.1)]}
      his={[
        { t: cue(s, 'many'), box: { ...b.stats, w: 120, h: 70 }, until: cue(s, 'when') - 0.15 },
        { t: cue(s, 'when'), box: { ...b.stats, x: b.stats.x + 160, w: 240, h: 70 }, until: cue(s, 'and') - 0.15 },
        { t: cue(s, 'views') - 0.4, box: { ...b.stats, x: b.stats.x + 420, w: 160, h: 70 }, until: cue(s, 'on') - 0.3 },
        { t: cue(s, 'phones'), box: front, pad: 12 },
      ]}
      cursor={[
        { t: cue(s, 'phones'), x: front.x + front.w + 120, y: front.y + front.h - 40 },
        { t: tap, x: front.x + front.w * 0.82, y: front.y + 75, click: true },
      ]}
      extra={(tt) =>
        tt > tap ? (
          <div style={{ position: 'absolute', left: front.x + 7, top: front.y + 7, width: front.w - 14, height: front.h - 14, borderRadius: 24, overflow: 'hidden', opacity: interpolate(tt, [tap + 0.15, tap + 0.45], [0, 1], clamp) }}>
            <Img src={staticFile(`thumbs/${p.thumbs[0]}.jpg`)} style={{ width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${1 + (tt - tap) * 0.03})` }} />
            <div style={{ position: 'absolute', left: 14, right: 14, bottom: 16, height: 5, borderRadius: 5, background: 'rgba(255,255,255,0.3)' }}>
              <div style={{ width: `${Math.min(100, (tt - tap) * 22)}%`, height: '100%', background: '#ff2e4d', borderRadius: 5 }} />
            </div>
          </div>
        ) : null
      }
    />
  );
};

const ArchiveScene: React.FC<SceneProps> = ({ s, p, no }) => {
  const t = useT(s.lead);
  const b = p.boxes.archive;
  return (
    <Browser
      t={t}
      chapterNo={no}
      chapter={s.chapter}
      shots={[{ t: -1, src: 'hero_0' }, { t: cue(s, 'scroll') + 0.15, src: 'archive', scroll: true }]}
      cams={[FULL(-1, 0.6), camOn(cue(s, 'every') - 0.3, b.head, 1.55, 1), FULL(cue(s, 'when') - 0.2, 1), camOn(cue(s, 'appears') - 0.3, b.firstThumb, 2.0, 1.1)]}
      his={[
        { t: cue(s, 'every'), box: b.head, until: cue(s, 'when') - 0.3, pad: 12 },
        { t: cue(s, 'appears'), box: b.firstThumb, pad: 6 },
      ]}
    />
  );
};

const CardsScene: React.FC<SceneProps> = ({ s, p, no }) => {
  const t = useT(s.lead);
  const b = p.boxes.cards;
  const card = b.first;
  return (
    <Browser
      t={t}
      chapterNo={no}
      chapter={s.chapter}
      shots={[{ t: -1, src: 'cards' }]}
      cams={[FULL(-1), camOn(0, card, 2.25, 1.1), camOn(cue(s, 'newest') - 0.3, { ...card, y: card.y + 40, h: 160 }, 2.5, 0.9), camOn(cue(s, 'longer') - 0.3, b.long, 2.6, 1)]}
      his={[
        { t: cue(s, 'cover'), box: { ...card, h: card.w * 16 / 9 }, until: cue(s, 'title') - 0.1, pad: 4 },
        { t: cue(s, 'title'), box: b.title, until: cue(s, 'date') - 0.1, pad: 5 },
        { t: cue(s, 'date'), box: b.date, until: cue(s, 'number') - 0.1, pad: 5 },
        { t: cue(s, 'number'), box: b.views, until: cue(s, 'newest') - 0.2, pad: 5 },
        { t: cue(s, 'yellow'), box: b.newtag, until: cue(s, 'longer') - 0.2, pad: 5 },
        { t: cue(s, 'full'), box: b.long, pad: 5 },
      ]}
    />
  );
};

const FiltersScene: React.FC<SceneProps> = ({ s, p, no }) => {
  const t = useT(s.lead);
  const b = p.boxes.filters_all;
  const chip = (k: string) => p.boxes.filters_all[k] ?? b.chips;
  const hist = chip('history');
  const histT = cue(s, 'history');
  const x0 = b.chips.x;
  const segs = [
    [cue(s, 'weird'), chip('science')],
    [cue(s, 'psychology'), chip('mind')],
    [cue(s, 'money'), chip('money')],
  ] as const;
  return (
    <Browser
      t={t}
      chapterNo={no}
      chapter={s.chapter}
      shots={[{ t: -1, src: 'filters_all' }, { t: histT + 0.25, src: 'filters_history' }]}
      cams={[FULL(-1), camOn(cue(s, 'pick') - 0.4, { ...b.chips, w: b.chips.w }, 1.9, 1), FULL(histT + 0.6, 1.1)]}
      his={[
        { t: cue(s, 'rubric'), box: b.chips, until: cue(s, 'weird') - 0.15, pad: 8 },
        ...segs.map(([tt, box], i) => ({ t: tt, box, until: (segs[i + 1]?.[0] ?? histT) - 0.15, pad: 5 })),
        { t: histT, box: hist, until: histT + 0.6, pad: 5 },
      ]}
      cursor={[
        { t: cue(s, 'weird') - 0.2, x: x0 + 150, y: b.chips.y + 70 },
        { t: histT, x: hist.x + hist.w / 2, y: hist.y + hist.h / 2, click: true },
      ]}
    />
  );
};

const SearchScene: React.FC<SceneProps> = ({ s, p, no }) => {
  const t = useT(s.lead);
  const b = p.boxes.search_zombie;
  const typeT = cue(s, 'zombie');
  const sortT = cue(s, 'sort');
  const moreT = cue(s, 'load');
  const mb = p.boxes.more.more;
  const q = b.q;
  return (
    <Browser
      t={t}
      chapterNo={no}
      chapter={s.chapter}
      shots={[
        { t: -1, src: 'filters_all' },
        { t: typeT + 0.55, src: 'search_zombie' },
        { t: sortT + 0.4, src: 'sort_views' },
        { t: moreT - 0.1, src: 'more', scroll: true },
      ]}
      cams={[camOn(-1, q, 2.4, 0.01), camOn(cue(s, 'every') - 0.2, { x: 800, y: 560, w: 1, h: 1 }, 1.15, 1.1), camOn(sortT - 0.3, p.boxes.sort_views.sort, 2.2, 0.9), FULL(cue(s, 'most') + 0.2, 0.9), camOn(moreT + 0.4, mb, 1.8, 1)]}
      his={[
        { t: cue(s, 'search'), box: q, until: cue(s, 'every') - 0.2, pad: 4 },
        { t: sortT, box: p.boxes.sort_views.sort, until: cue(s, 'most') + 0.3, pad: 5 },
        { t: moreT + 0.5, box: mb, pad: 6 },
      ]}
      cursor={[
        { t: cue(s, 'search'), x: q.x + 40, y: q.y + q.h / 2, click: true },
        { t: sortT, x: p.boxes.sort_views.sort.x + 60, y: p.boxes.sort_views.sort.y + 26, click: true },
        { t: moreT + 0.9, x: mb.x + mb.w / 2, y: mb.y + mb.h / 2, click: true },
      ]}
      extra={(tt) => {
        if (tt < cue(s, 'type') || tt > typeT + 0.55) return null;
        const n = Math.floor(interpolate(tt, [cue(s, 'type') + 0.1, typeT + 0.45], [0, 6], clamp));
        return (
          <div style={{ position: 'absolute', left: q.x + 43, top: q.y + 2, height: q.h - 4, width: q.w - 60, background: '#171137', display: 'flex', alignItems: 'center', fontFamily: C.body, fontWeight: 500, fontSize: 16, color: C.text }}>
            {'zombie'.slice(0, n)}
            <span style={{ width: 2, height: 20, background: C.text, marginLeft: 1 }} />
          </div>
        );
      }}
    />
  );
};

const PlayerScene: React.FC<SceneProps> = ({ s, p, no }) => {
  const t = useT(s.lead);
  const card = p.boxes.player_before.card;
  const pl = p.boxes.player.player;
  const open = p.boxes.player.open;
  const tap = cue(s, 'tap') + 0.35;
  return (
    <Browser
      t={t}
      chapterNo={no}
      chapter={s.chapter}
      shots={[{ t: -1, src: 'player_before' }, { t: tap + 0.25, src: 'player' }]}
      cams={[camOn(-1, card, 1.6, 0.01), FULL(tap + 0.3, 0.8), camOn(cue(s, 'one') - 0.3, open, 2.1, 0.9)]}
      his={[{ t: cue(s, 'one'), box: open, pad: 6 }]}
      cursor={[
        { t: -0.2, x: card.x + card.w + 60, y: card.y + card.h * 0.75 },
        { t: tap, x: card.x + card.w / 2, y: card.y + card.h / 2, click: true },
        { t: cue(s, 'one') + 0.1, x: open.x + open.w / 2, y: open.y + open.h / 2, click: true },
      ]}
      extra={(tt) =>
        tt > tap + 0.25 ? (
          <div style={{ position: 'absolute', left: pl.x, top: pl.y, width: pl.w, height: pl.h, borderRadius: 22, overflow: 'hidden', background: '#000' }}>
            <Img src={staticFile('thumbs/C3nffxC5ZKM.jpg')} style={{ width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${1.02 + (tt - tap) * 0.02})` }} />
            <div style={{ position: 'absolute', left: 0, right: 0, bottom: 0, height: 90, background: 'linear-gradient(180deg, transparent, rgba(0,0,0,0.7))' }} />
            <div style={{ position: 'absolute', left: 16, right: 16, bottom: 18, height: 4, borderRadius: 4, background: 'rgba(255,255,255,0.3)' }}>
              <div style={{ width: `${Math.min(100, (tt - tap) * 9)}%`, height: '100%', background: '#ff2e4d', borderRadius: 4 }} />
            </div>
          </div>
        ) : null
      }
    />
  );
};

const SuggestScene: React.FC<SceneProps> = ({ s, p, no }) => {
  const t = useT(s.lead);
  const e = p.boxes.suggest_empty;
  const f = p.boxes.suggest_filled;
  const write = cue(s, 'write');
  return (
    <Browser
      t={t}
      chapterNo={no}
      chapter={s.chapter}
      shots={[{ t: -1, src: 'suggest_empty' }, { t: write + 0.6, src: 'suggest_filled' }]}
      cams={[FULL(-1), camOn(cue(s, 'got') - 0.3, e.panel, 1.45, 1.1), camOn(cue(s, 'leave') - 0.4, { ...f.name, y: f.name.y + 40, h: 60 }, 1.7, 1), camOn(cue(s, 'we') - 0.3, e.panel, 1.4, 1)]}
      his={[
        { t: write, box: f.idea, until: cue(s, 'pick') - 0.15, pad: 5 },
        { t: cue(s, 'pick'), box: f.topic, until: cue(s, 'leave') - 0.15, pad: 5 },
        { t: cue(s, 'leave'), box: { x: f.topic.x, y: f.name.y - 34, w: f.name.x + f.name.w - f.topic.x, h: f.email.y + f.email.h - f.name.y + 34 }, until: cue(s, 'we') - 0.2, pad: 8 },
        { t: cue(s, 'best'), box: f.send, pad: 6 },
      ]}
      cursor={[
        { t: write - 0.2, x: f.idea.x + 60, y: f.idea.y + 40, click: true },
        { t: cue(s, 'pick') + 0.1, x: f.topic.x + 80, y: f.topic.y + f.topic.h / 2, click: true },
        { t: cue(s, 'best') + 0.2, x: f.send.x + f.send.w / 2, y: f.send.y + f.send.h / 2 },
      ]}
      extra={(tt) => {
        if (tt < write || tt > write + 0.6) return null;
        const txt = 'What if the Moon disappeared for one night?';
        const n = Math.floor(interpolate(tt, [write, write + 0.55], [0, txt.length], clamp));
        return (
          <div style={{ position: 'absolute', left: f.idea.x + 14, top: f.idea.y + 12, width: f.idea.w - 28, height: 40, background: '#171137', fontFamily: C.body, fontSize: 16, color: C.text, fontWeight: 500 }}>
            {txt.slice(0, n)}
          </div>
        );
      }}
    />
  );
};

const AskScene: React.FC<SceneProps> = ({ s, p, no }) => {
  const t = useT(s.lead);
  const e = p.boxes.ask_empty;
  const typed = p.boxes.ask_typed;
  const typeT = cue(s, 'type');
  return (
    <Browser
      t={t}
      chapterNo={no}
      chapter={s.chapter}
      shots={[{ t: -1, src: 'ask_empty' }, { t: typeT + 0.7, src: 'ask_typed' }]}
      cams={[FULL(-1), camOn(cue(s, 'ask') - 0.3, e.panel, 1.45, 1.1), camOn(cue(s, 'tap') - 0.3, e.samples, 1.9, 0.9), camOn(cue(s, 'you') - 0.3, { ...typed.q, w: typed.q.w + 120 }, 1.9, 0.9)]}
      his={[
        { t: typeT, box: typed.q, until: cue(s, 'tap') - 0.2, pad: 5 },
        { t: cue(s, 'examples') - 0.2, box: e.samples, until: cue(s, 'you') - 0.2, pad: 8 },
        { t: cue(s, 'short'), box: typed.ask, pad: 6 },
      ]}
      cursor={[
        { t: typeT - 0.2, x: typed.q.x + 60, y: typed.q.y + typed.q.h / 2, click: true },
        { t: cue(s, 'examples'), x: e.samples.x + 90, y: e.samples.y + 16 },
        { t: cue(s, 'short') + 0.1, x: typed.ask.x + typed.ask.w / 2, y: typed.ask.y + typed.ask.h / 2 },
      ]}
      extra={(tt) => {
        if (tt < typeT || tt > typeT + 0.7) return null;
        const txt = 'Why was Krakatoa so loud?';
        const n = Math.floor(interpolate(tt, [typeT, typeT + 0.6], [0, txt.length], clamp));
        return (
          <div style={{ position: 'absolute', left: typed.q.x + 18, top: typed.q.y + 3, height: typed.q.h - 6, width: typed.q.w - 30, background: '#1d1548', display: 'flex', alignItems: 'center', fontFamily: C.body, fontSize: 16, color: C.text, fontWeight: 500 }}>
            {txt.slice(0, n)}
          </div>
        );
      }}
    />
  );
};

const FaqScene: React.FC<SceneProps> = ({ s, p, no }) => {
  const t = useT(s.lead);
  const b = p.boxes.faq;
  return (
    <Browser
      t={t}
      chapterNo={no}
      chapter={s.chapter}
      shots={[{ t: -1, src: 'faq' }]}
      cams={[FULL(-1), camOn(cue(s, 'faq') - 0.3, b.qa, 1.3, 1.2), camOn(cue(s, 'check') - 0.3, b.open, 1.8, 0.9)]}
      his={[
        { t: cue(s, 'often'), box: { ...b.qa, h: 70 }, until: cue(s, 'check') - 0.2, pad: 4 },
        { t: cue(s, 'check'), box: b.open, until: cue(s, 'videos') - 0.2, pad: 4 },
        { t: cue(s, 'videos'), box: { ...b.qa, y: b.qa.y + b.qa.h - 70, h: 70 }, pad: 4 },
      ]}
    />
  );
};

const Phone: React.FC<{ src: string; alt: string; mix: number; x: number; s: number; rot: number }> = ({ src, alt, mix, x, s, rot }) => {
  const w = 360;
  const h = w * (844 / 390);
  return (
    <div
      style={{
        position: 'absolute',
        left: W / 2 + x - (w + 24) / 2,
        top: 96,
        width: w + 24,
        height: h + 24,
        padding: 12,
        borderRadius: 58,
        background: '#05030f',
        boxShadow: `0 50px 90px -30px rgba(0,0,0,0.85), inset 0 0 0 2px #3a3170`,
        transform: `translateY(${(1 - s) * 500}px) rotate(${rot}deg)`,
        opacity: s,
      }}
    >
      <div style={{ position: 'relative', width: w, height: h, borderRadius: 46, overflow: 'hidden' }}>
        <Img src={staticFile(`shots/${src}.jpg`)} style={{ position: 'absolute', width: '100%', height: '100%' }} />
        <Img src={staticFile(`shots/${alt}.jpg`)} style={{ position: 'absolute', width: '100%', height: '100%', clipPath: `inset(0 0 ${100 - mix * 100}% 0)` }} />
      </div>
    </div>
  );
};

const MobileScene: React.FC<SceneProps> = ({ s, no }) => {
  const t = useT(s.lead);
  const { fps } = useVideoConfig();
  const sp = (d: number) => spring({ frame: Math.round((t - d) * fps), fps, config: { damping: 16 } });
  const lightT = cue(s, 'light');
  const mix = ease(interpolate(t, [lightT - 0.1, lightT + 0.6], [0, 1], clamp));
  const back = interpolate(t, [cue(s, 'dark') - 0.2, cue(s, 'dark') + 0.6], [0, 1], clamp);
  const chap = spring({ frame: Math.round(t * fps), fps, config: { damping: 16 } });
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: `linear-gradient(90deg, rgba(244,242,251,${0.1 * mix}), transparent)`, opacity: back }} />
      <div style={{ position: 'absolute', left: 80, top: 60, display: 'flex', gap: 12, alignItems: 'center', fontFamily: C.body, fontWeight: 700, fontSize: 24, color: C.text, opacity: chap }}>
        <span style={{ background: C.hi, color: C.hiInk, borderRadius: 8, padding: '3px 11px', fontFamily: C.display, fontSize: 22 }}>{String(no).padStart(2, '0')}</span>
        {s.chapter}
      </div>
      <Phone src="m_dark_hero" alt="m_light_hero" mix={mix} x={-440} s={sp(-0.3)} rot={-4} />
      <Phone src="m_dark_grid" alt="m_light_grid" mix={mix} x={0} s={sp(-0.15)} rot={0} />
      <Phone src="m_dark_ask" alt="m_light_ask" mix={mix} x={440} s={sp(0)} rot={4} />
    </AbsoluteFill>
  );
};

const Outro: React.FC<SceneProps> = ({ s, p }) => {
  const t = useT(s.lead);
  const { fps } = useVideoConfig();
  const sp = (d: number, damping = 15) => spring({ frame: Math.round((t - d) * fps), fps, config: { damping } });
  const items: [string, number][] = [
    ['Watch every video', cue(s, 'watch')],
    ['Suggest the next one', cue(s, 'suggest')],
    ['Ask anything', cue(s, 'ask')],
  ];
  const subT = cue(s, 'subscribe');
  const sub = sp(cue(s, 'hit') - 0.3, 12);
  const clicked = t > subT + 0.25;
  const btnX = W / 2;
  const btnY = 760;
  const cur = interpolate(t, [subT - 0.9, subT], [0, 1], clamp);
  const click = t >= subT && t < subT + 0.6 ? (t - subT) / 0.6 : -1;
  return (
    <AbsoluteFill>
      <ThumbWall thumbs={p.thumbs} dim={0.88} blur={3} />
      <AbsoluteFill style={{ alignItems: 'center', paddingTop: 120, flexDirection: 'column', gap: 30 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 30, transform: `scale(${0.9 + 0.1 * sp(-0.2)})`, opacity: sp(-0.2) }}>
          <Logo size={110} s={1} />
          <span style={{ fontFamily: C.display, fontSize: 120, color: C.text, letterSpacing: -3 }}>.video</span>
        </div>
        <div style={{ display: 'flex', gap: 22, marginTop: 20 }}>
          {items.map(([label, at], i) => {
            const k = sp(at - 0.1);
            return (
              <div
                key={label}
                style={{
                  fontFamily: C.body,
                  fontWeight: 700,
                  fontSize: 36,
                  color: C.text,
                  background: C.night2,
                  border: `2px solid ${C.line}`,
                  borderRadius: 99,
                  padding: '16px 30px',
                  display: 'flex',
                  gap: 14,
                  alignItems: 'center',
                  opacity: k,
                  transform: `translateY(${(1 - k) * 40}px)`,
                }}
              >
                <span style={{ fontFamily: C.display, color: C.hi }}>{String(i + 1).padStart(2, '0')}</span>
                {label}
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
      <div
        style={{
          position: 'absolute',
          left: btnX,
          top: btnY,
          transform: `translate(-50%,-50%) scale(${sub * (click >= 0 ? interpolate(click, [0, 0.15, 0.4], [1, 0.92, 1], clamp) : 1)})`,
          opacity: sub,
          display: 'flex',
          alignItems: 'center',
          gap: 18,
          background: clicked ? '#2b2066' : C.hi,
          color: clicked ? C.text : C.hiInk,
          fontFamily: C.body,
          fontWeight: 800,
          fontSize: 46,
          padding: '26px 56px',
          borderRadius: 99,
          boxShadow: clicked ? 'none' : '0 20px 60px -10px rgba(255,214,0,0.55)',
        }}
      >
        <svg width="52" height="52" viewBox="0 0 24 24"><path fill={clicked ? C.text : '#16112e'} d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12a31 31 0 0 0 .5 4.8 3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .5-4.8 31 31 0 0 0-.5-4.8ZM9.7 15.1V8.9l5.8 3.1-5.8 3.1Z" /></svg>
        {clicked ? 'Subscribed' : 'Subscribe'}
      </div>
      {click >= 0 && (
        <div style={{ position: 'absolute', left: btnX + 120 - 70, top: btnY - 70, width: 140, height: 140, borderRadius: '50%', border: `6px solid ${C.hi}`, transform: `scale(${0.2 + click})`, opacity: 1 - click }} />
      )}
      {cur > 0 && (
        <svg width={56} height={56} viewBox="0 0 24 24" style={{ position: 'absolute', left: interpolate(cur, [0, 1], [btnX + 420, btnX + 112]), top: interpolate(cur, [0, 1], [btnY + 230, btnY - 6]), filter: 'drop-shadow(0 6px 10px rgba(0,0,0,0.5))' }}>
          <path d="M4 2.5 L4 19.5 L8.6 15.4 L11.6 22 L14.6 20.7 L11.7 14.2 L18 14.2 Z" fill="#fff" stroke="#120d2b" strokeWidth="1.4" strokeLinejoin="round" />
        </svg>
      )}
      <div style={{ position: 'absolute', left: 0, right: 0, top: 880, textAlign: 'center', fontFamily: C.body, fontWeight: 700, fontSize: 28, letterSpacing: 7, textTransform: 'uppercase', color: C.muted, opacity: sp(cue(s, 'see')) }}>
        A new “What if…?” every day
      </div>
    </AbsoluteFill>
  );
};

const SCENES: Record<string, React.FC<SceneProps>> = {
  intro: Intro,
  hero: HeroScene,
  stats: StatsScene,
  archive: ArchiveScene,
  cards: CardsScene,
  filters: FiltersScene,
  search: SearchScene,
  player: PlayerScene,
  suggest: SuggestScene,
  ask: AskScene,
  faq: FaqScene,
  mobile: MobileScene,
  outro: Outro,
};

export const SiteTour: React.FC<TourProps> = (p) => {
  const { fps } = useVideoConfig();
  const frame = useCurrentFrame();
  const { scenes, total } = layout(p);
  const chapters = [...new Set(scenes.map((s) => s.chapter).filter(Boolean))];
  const musicVol = interpolate(frame, [0, fps * 1.2, (total - 2.5) * fps, total * fps], [0, 0.16, 0.16, 0], clamp);
  return (
    <AbsoluteFill style={{ background: C.night }}>
      <Stage />
      <Audio src={staticFile('audio/music.mp3')} volume={musicVol} />
      {scenes.map((s) => {
        const Comp = SCENES[s.id];
        const from = Math.round(s.start * fps);
        const dur = Math.round(s.dur * fps);
        return (
          <Sequence key={s.id} from={from} durationInFrames={dur} name={s.id}>
            <Comp s={s} p={p} no={chapters.indexOf(s.chapter) + 1} />
            <Sequence from={Math.round(s.lead * fps)} name={`${s.id} vo`}>
              <Audio src={staticFile(`audio/${s.id}/voiceover.mp3`)} />
            </Sequence>
            <Captions words={s.words} offsetMs={s.lead * 1000} centerY={0.94} fontSize={56} maxWords={6} maxChars={36} maxWidth={1700} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

/* ---------- thumbnail (1280x720) ---------- */
export const TourThumb: React.FC<TourProps> = (p) => (
  <AbsoluteFill style={{ background: C.night }}>
    <ThumbWall thumbs={p.thumbs} dim={0.5} />
    <AbsoluteFill style={{ background: 'linear-gradient(90deg, rgba(18,13,43,0.97) 0%, rgba(18,13,43,0.88) 52%, rgba(18,13,43,0.2) 100%)' }} />
    <div style={{ position: 'absolute', left: 64, top: 70, display: 'flex', flexDirection: 'column', alignItems: 'flex-start', gap: 26 }}>
      <Logo size={78} s={1} />
      <div style={{ fontFamily: C.display, fontSize: 112, lineHeight: 0.98, color: C.text, letterSpacing: -3, width: 760 }}>
        EVERY VIDEO, <span style={{ background: C.hi, color: C.hiInk, padding: '0 14px', borderRadius: 14 }}>ONE</span> SITE
      </div>
      <div style={{ fontFamily: C.display, fontSize: 54, color: C.hi, letterSpacing: -1 }}>zylo.video</div>
    </div>
    <div style={{ position: 'absolute', right: 70, top: 70, width: 330, height: 586, borderRadius: 40, padding: 10, background: '#05030f', transform: 'rotate(5deg)', boxShadow: '0 30px 60px rgba(0,0,0,0.6), inset 0 0 0 2px #3a3170' }}>
      <Img src={staticFile('shots/m_dark_hero.jpg')} style={{ width: '100%', height: '100%', borderRadius: 32, objectFit: 'cover', objectPosition: 'top' }} />
    </div>
  </AbsoluteFill>
);
