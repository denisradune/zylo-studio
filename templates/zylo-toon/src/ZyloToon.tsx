import React, { useMemo } from 'react';
import { AbsoluteFill, Audio, Easing, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { brand } from '../../zylo-shared/brand';
import { LogoMark } from '../../zylo-shared/Chrome';
import { FLOOR_Y, H, SetPiece, W } from '../../zylo-shared/toon/Backgrounds';
import { Bit, BitExpr, Car, Expr, Human, INK, LOOKS, Pose } from '../../zylo-shared/toon/Character';
import { FxLayer, shakeAt } from '../../zylo-shared/toon/Fx';
import type { CastMember, Shot, StoryProps, StoryWord } from '../../zylo-shared/toon/types';
import { UiLayer } from '../../zylo-shared/toon/Ui';
import { SatisfyingPanel } from '../../zylo-shared/toon/Satisfying';

/** Split-screen: the top half shows this window of the 1080x1920 scene (heads to floor). */
const SPLIT_Y = 510;
const HALF = 960;
/** UI overlays (counters, cards, notifications) are scaled into the top half. */
const UI_SPLIT = 0.68;

const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;

/** Mouth openness for `voice` at absolute time t (seconds): flaps on its words, closed between. */
const talkFor = (voice: string, t: number, words: StoryWord[], lines: StoryProps['lines'], frame: number) => {
  const ms = t * 1000;
  const w = words.find((x) => ms >= x.startMs && ms < x.endMs);
  if (!w || lines[w.line]?.speaker !== voice) return 0;
  return 0.35 + 0.65 * Math.abs(Math.sin(frame * 0.95));
};

const Actor: React.FC<{ m: CastMember; f: number; dur: number; t: number; frame: number; words: StoryWord[]; lines: StoryProps['lines']; fps: number }> = ({
  m,
  f,
  dur,
  t,
  frame,
  words,
  lines,
  fps,
}) => {
  const depth = m.depth ?? 0;
  const scale = (m.scale ?? 1.35) * (1 - depth * 0.55);
  const lift = depth * 260 + (m.lift ?? 0);
  let x = m.x;
  let pose: Pose = (m.pose as Pose) ?? 'idle';
  if (m.moveTo !== undefined) {
    x = interpolate(f, [0, dur], [m.x, m.moveTo], { ...clamp, easing: Easing.inOut(Easing.sin) });
    if (!m.pose) pose = 'walk';
  }
  let enterDx = 0;
  let pop = 1;
  if (m.enter === 'left' || m.enter === 'right') {
    const p = interpolate(f, [0, 14], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
    enterDx = (1 - p) * (m.enter === 'left' ? -700 : 700);
  } else if (m.enter === 'pop') {
    pop = spring({ frame: f, fps, config: { damping: 11, stiffness: 160 } });
  }
  const talk = talkFor(m.voice ?? m.id, t, words, lines, frame);
  const facing = m.facing ?? 1;
  const cx = x * W + enterDx;
  const footY = FLOOR_Y - lift;
  const body =
    m.id === 'car' ? (
      <Car color={m.color} t={frame} moving={m.moveTo !== undefined} />
    ) : m.id === 'bit' ? (
      <Bit expr={(m.expr as BitExpr) ?? 'neutral'} talk={talk} t={frame} icon={m.icon} seed={3} />
    ) : (
      <Human look={LOOKS[m.id] ?? LOOKS.hero} pose={pose} expr={(m.expr as Expr) ?? 'neutral'} talk={talk} t={frame} gaze={m.gaze ?? 0} seed={Math.abs(Math.round(m.x * 97))} />
    );
  return (
    <g transform={`translate(${cx} ${footY}) scale(${scale * pop * facing} ${scale * pop}) translate(-150 -600)`} opacity={1 - depth * 0.15}>
      {body}
    </g>
  );
};

const ShotView: React.FC<{ shot: Shot; dur: number; words: StoryWord[]; lines: StoryProps['lines']; split?: boolean }> = ({ shot, dur, words, lines, split }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = shot.start + f / fps;
  const frame = Math.round(shot.start * fps) + f;
  const cam = shot.camera ?? {};
  const zoom0 = cam.zoom ?? 1;
  const zoom = zoom0 * interpolate(f, [0, dur], [1, 1 + (cam.push ?? 0.05)], clamp);
  const fx = cam.x ?? 0.5;
  const fy = cam.y ?? 0.55;
  const impacts = (shot.fx ?? []).filter((e) => e.type === 'impact').map((e) => (e.type === 'impact' ? e.at ?? 0 : 0));
  const meteorHits = (shot.fx ?? []).filter((e) => e.type === 'meteor').map((e) => (e.type === 'meteor' ? e.hitAt ?? 1.2 : 0));
  const shakes = [...impacts, ...meteorHits, ...(cam.shake !== undefined ? [cam.shake] : [])];
  const sh = shakes.reduce((acc, s0) => {
    const o = shakeAt(f, fps, s0);
    return { x: acc.x + o.x, y: acc.y + o.y };
  }, { x: 0, y: 0 });
  const ordered = [...shot.cast].sort((a, b) => (b.depth ?? 0) - (a.depth ?? 0));
  // Split-screen: slide the 960-px window so the tallest character's head (after camera zoom) stays in view.
  let winY = SPLIT_Y;
  if (split && shot.cast.length) {
    const zEnd = zoom0 * (1 + (cam.push ?? 0.05));
    const heads = shot.cast.map((m) => {
      const depth = m.depth ?? 0;
      const sc = (m.scale ?? 1.35) * (1 - depth * 0.55);
      const top = FLOOR_Y - depth * 260 - (m.lift ?? 0) - (m.id === 'bit' ? 430 : 600) * sc;
      return fy * H + (top - fy * H) * Math.max(zoom0, zEnd);
    });
    winY = Math.max(0, Math.min(SPLIT_Y, Math.min(...heads) - 70));
  }

  const tr = shot.transition ?? 'cut';
  const flash = tr === 'flash' ? interpolate(f, [0, 6], [1, 0], clamp) : 0;
  const whip = tr === 'whip' ? interpolate(f, [0, 6], [1, 0], { ...clamp, easing: Easing.out(Easing.cubic) }) : 0;

  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      <AbsoluteFill style={{ transform: `translateX(${whip * -160}px)`, filter: whip > 0.05 ? `blur(${whip * 18}px)` : undefined }}>
        <svg viewBox={split ? `0 ${winY} ${W} ${HALF}` : `0 0 ${W} ${H}`} width="100%" height="100%">
          <g transform={`translate(${sh.x} ${sh.y}) translate(${fx * W} ${fy * H}) scale(${zoom}) translate(${-fx * W} ${-fy * H})`}>
            <SetPiece spec={shot.set} t={frame} />
            {ordered.map((m, i) => (
              <Actor key={i} m={m} f={f} dur={dur} t={t} frame={frame} words={words} lines={lines} fps={fps} />
            ))}
            <FxLayer fx={shot.fx ?? []} f={f} fps={fps} />
          </g>
        </svg>
      </AbsoluteFill>
      {shot.ui &&
        (split ? (
          <div style={{ position: 'absolute', left: (W - W * UI_SPLIT) / 2, top: 20, width: W, height: H, transform: `scale(${UI_SPLIT})`, transformOrigin: 'top left' }}>
            <UiLayer ui={shot.ui} f={f} fps={fps} dur={dur} />
          </div>
        ) : (
          <UiLayer ui={shot.ui} f={f} fps={fps} dur={dur} />
        ))}
      {flash > 0 && <AbsoluteFill style={{ backgroundColor: '#FFFFFF', opacity: flash }} />}
    </AbsoluteFill>
  );
};

type Page = { words: StoryWord[]; start: number; end: number };

/** 2-4 word pages; a page never spans two speakers or a sentence end. */
const pages = (words: StoryWord[]): Page[] => {
  const out: Page[] = [];
  let cur: StoryWord[] = [];
  const flush = () => {
    if (cur.length) out.push({ words: cur, start: cur[0].startMs, end: cur[cur.length - 1].endMs });
    cur = [];
  };
  words.forEach((w, i) => {
    const prev = cur[cur.length - 1];
    if (prev && (prev.line !== w.line || cur.length >= 4 || /[.!?…,]$/.test(prev.text) || cur.map((x) => x.text).join(' ').length > 22)) flush();
    cur.push(w);
    if (i === words.length - 1) flush();
  });
  out.forEach((p, i) => {
    const n = out[i + 1];
    p.end = n ? Math.min(n.start, p.end + 700) : p.end + 600;
  });
  return out;
};

const StoryCaptions: React.FC<{ words: StoryWord[]; lines: StoryProps['lines']; names: Record<string, string>; hideFrom: number; split?: boolean }> = ({ words, lines, names, hideFrom, split }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ps = useMemo(() => pages(words), [words]);
  const ms = (frame / fps) * 1000;
  if (ms >= hideFrom * 1000) return null;
  const p = ps.find((x) => ms >= x.start && ms < x.end);
  if (!p) return null;
  const speaker = lines[p.words[0].line]?.speaker;
  const name = speaker && speaker !== 'narrator' ? names[speaker] ?? speaker.toUpperCase() : null;
  return (
    <div style={{ position: 'absolute', left: 60, right: 60, top: split ? 600 : H * 0.66, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      {name && (
        <div
          style={{
            marginBottom: 14,
            padding: '6px 18px',
            borderRadius: 10,
            background: speaker === 'bit' ? '#FFD400' : '#FFFFFF',
            border: `5px solid ${INK}`,
            fontFamily: brand.body,
            fontWeight: 900,
            fontSize: 30,
            letterSpacing: 2,
            color: INK,
          }}
        >
          {name}
        </div>
      )}
      <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '0 22px', maxWidth: 940 }}>
        {p.words.map((w, i) => {
          const shown = ms >= w.startMs - 40;
          const k = interpolate(ms - w.startMs, [-40, 80], [0.6, 1], clamp);
          return (
            <span
              key={i}
              style={{
                fontFamily: brand.head,
                fontWeight: 900,
                fontSize: split ? 66 : 78,
                lineHeight: 1.12,
                textTransform: 'uppercase',
                color: w.emph ? '#FFD400' : '#FFFFFF',
                WebkitTextStroke: `14px ${INK}`,
                paintOrder: 'stroke fill',
                opacity: shown ? 1 : 0,
                transform: `scale(${shown ? k : 0.6})`,
                display: 'inline-block',
                textShadow: `0 8px 0 ${INK}`,
              }}
            >
              {w.text}
            </span>
          );
        })}
      </div>
    </div>
  );
};

const EndCard: React.FC<{ text: string; sub: string }> = ({ text, sub }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: f, fps, config: { damping: 12 } });
  const s2 = spring({ frame: f - 8, fps, config: { damping: 12 } });
  return (
    <AbsoluteFill style={{ backgroundColor: '#0E0E14', alignItems: 'center', justifyContent: 'center' }}>
      <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%" style={{ position: 'absolute' }}>
        <g transform={`translate(540 860) rotate(${f * 0.4})`} opacity={0.12}>
          {Array.from({ length: 18 }).map((_, i) => (
            <path key={i} d="M 0 0 L -110 -1500 L 110 -1500 Z" fill="#FFD400" transform={`rotate(${i * 20})`} />
          ))}
        </g>
      </svg>
      <div style={{ transform: `scale(${s})`, marginTop: -260 }}>
        <LogoMark size={220} shine />
      </div>
      <div
        style={{
          marginTop: 50,
          fontFamily: brand.head,
          fontWeight: 900,
          fontSize: 120,
          color: '#FFD400',
          WebkitTextStroke: `10px ${INK}`,
          paintOrder: 'stroke fill',
          transform: `scale(${s2})`,
          textAlign: 'center',
          lineHeight: 1,
        }}
      >
        {text}
      </div>
      <div style={{ marginTop: 26, fontFamily: brand.body, fontWeight: 900, fontSize: 46, color: '#FFFFFF', opacity: s2, textAlign: 'center', maxWidth: 900 }}>{sub}</div>
    </AbsoluteFill>
  );
};

/** Series badge: which part of the story this Short is. */
const PartBadge: React.FC<{ label: string; hideFrom: number }> = ({ label, hideFrom }) => {
  const f = useCurrentFrame();
  if (f >= hideFrom) return null;
  return (
    <div
      style={{
        position: 'absolute',
        top: 70,
        left: 56,
        display: 'flex',
        alignItems: 'center',
        gap: 14,
        padding: '10px 22px 10px 12px',
        borderRadius: 18,
        background: '#FFD400',
        border: `5px solid ${INK}`,
        boxShadow: `6px 6px 0 ${INK}`,
        fontFamily: brand.head,
        fontWeight: 900,
        fontSize: 38,
        color: INK,
      }}
    >
      <LogoMark size={52} />
      {label}
    </div>
  );
};

/** Full-length version: a punchy card announcing each new part. */
const ChapterCard: React.FC<{ label: string; title: string }> = ({ label, title }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: f, fps, config: { damping: 12 } });
  const out = interpolate(f, [38, 48], [1, 0], clamp);
  return (
    <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', opacity: out, background: 'rgba(14,14,20,0.55)' }}>
      <div
        style={{
          transform: `rotate(-3deg) scale(${0.5 + 0.5 * s})`,
          padding: '26px 60px',
          background: '#FFD400',
          border: `8px solid ${INK}`,
          boxShadow: `12px 12px 0 ${INK}`,
          borderRadius: 22,
          textAlign: 'center',
          marginTop: -300,
        }}
      >
        <div style={{ fontFamily: brand.head, fontWeight: 900, fontSize: 120, color: INK, lineHeight: 1 }}>{label}</div>
        <div style={{ fontFamily: brand.body, fontWeight: 900, fontSize: 48, color: INK, marginTop: 10 }}>{title}</div>
      </div>
    </AbsoluteFill>
  );
};

export const ZyloToon: React.FC<StoryProps> = (props) => {
  const { fps, durationInFrames } = useVideoConfig();
  const frame = useCurrentFrame();
  const endFrame = Math.round(props.endStart * fps);
  const vol = props.musicVolume ?? 0.15;
  const split = !!props.split;
  const shotsLayer = props.shots.map((s, i) => {
    const from = Math.round(s.start * fps);
    const dur = Math.max(1, Math.round(s.end * fps) - from);
    return (
      <Sequence key={i} from={from} durationInFrames={dur}>
        <ShotView shot={s} dur={dur} words={props.words} lines={props.lines} split={split} />
        {(s.sfx ?? []).map((e, k) => (
          <Sequence key={k} from={Math.round((e.at ?? 0) * fps)} layout="none">
            <Audio src={staticFile(`sfx/${e.type}.wav`)} volume={e.volume ?? 0.55} />
          </Sequence>
        ))}
      </Sequence>
    );
  });
  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      {split ? (
        <>
          <div style={{ position: 'absolute', left: 0, top: 0, width: W, height: HALF, overflow: 'hidden' }}>{shotsLayer}</div>
          <div style={{ position: 'absolute', left: 0, top: HALF, width: W, height: HALF, overflow: 'hidden' }}>
            <SatisfyingPanel kind={props.split!.kind} f={frame} fps={fps} seed={props.split!.seed ?? 0} />
          </div>
          <div style={{ position: 'absolute', left: 0, top: HALF - 4, width: W, height: 8, background: INK }} />
        </>
      ) : (
        shotsLayer
      )}
      <Sequence from={endFrame}>
        <EndCard text={props.endText ?? 'PART 2?'} sub={props.endSub ?? 'Follow so you don’t miss it'} />
      </Sequence>
      {props.chapters?.map((c, i) => (
        <Sequence key={`c${i}`} from={Math.round(c.start * fps)} durationInFrames={Math.round(1.6 * fps)}>
          <ChapterCard label={c.label} title={c.title} />
        </Sequence>
      ))}
      {props.partLabel && <PartBadge label={props.partLabel} hideFrom={endFrame} />}
      <StoryCaptions words={props.words} lines={props.lines} names={props.names ?? {}} hideFrom={props.endStart + 99} split={split} />
      <Audio src={staticFile(props.voiceover)} />
      {props.music && (
        <Audio
          src={staticFile(props.music)}
          loop
          volume={(fr) => vol * interpolate(fr, [0, 10, durationInFrames - fps, durationInFrames], [0, 1, 1, 0], clamp)}
        />
      )}
    </AbsoluteFill>
  );
};
