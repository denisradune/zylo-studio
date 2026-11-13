import React from 'react';
import { AbsoluteFill, Easing, OffthreadVideo, interpolate, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { brand } from '../../zylo-shared/brand';
import { LogoMark } from '../../zylo-shared/Chrome';
import { FLOOR_Y, SetPiece, SetSpec, W } from '../../zylo-shared/toon/Backgrounds';
import { Bit, BitExpr, Expr, Human, INK, LOOKS, Pose } from '../../zylo-shared/toon/Character';
import { FxLayer, FxSpec } from '../../zylo-shared/toon/Fx';

export type WideChapter = { start: number; label: string; title: string };
export type WideProps = {
  /** The vertical full cut (1080x1920), relative to the public dir. */
  video: string;
  durationSeconds: number;
  title: string;
  chapters: WideChapter[];
};

const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;
const VW = 608; // 1080 * 9/16 -> the vertical cut at full height

/**
 * The vertical full story as a regular 16:9 video: blurred copy behind, the cut in the middle,
 * the title on the left and the chapter list on the right (current chapter highlighted).
 */
export const ToonWide: React.FC<WideProps> = ({ video, title, chapters }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  let cur = 0;
  chapters.forEach((c, i) => {
    if (t >= c.start) cur = i;
  });
  const since = t - chapters[cur].start;
  const tagIn = interpolate(since, [0, 0.4], [0, 1], { ...clamp, easing: Easing.out(Easing.back(2)) });
  const words = title.replace(/^What if\s*/i, '').split(/\s+/);
  return (
    <AbsoluteFill style={{ backgroundColor: brand.bg }}>
      <AbsoluteFill style={{ filter: 'blur(42px) brightness(0.32) saturate(1.3)', transform: 'scale(1.15)' }}>
        <OffthreadVideo src={staticFile(video)} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
      </AbsoluteFill>
      <AbsoluteFill style={{ background: 'radial-gradient(ellipse at center, rgba(11,11,15,0) 30%, rgba(11,11,15,0.75) 100%)' }} />

      {/* left: brand + title */}
      <div style={{ position: 'absolute', left: 70, top: 70, display: 'flex', alignItems: 'center', gap: 18 }}>
        <LogoMark size={64} />
        <div style={{ fontFamily: brand.head, fontWeight: 900, fontSize: 44, color: brand.text }}>zylo</div>
      </div>
      <div style={{ position: 'absolute', left: 70, top: 300, width: 520 }}>
        <div style={{ fontFamily: brand.display, fontSize: 64, color: brand.accent, letterSpacing: 2 }}>WHAT IF...</div>
        <div style={{ fontFamily: brand.display, fontSize: words.join(' ').length > 34 ? 72 : 86, lineHeight: 1.02, color: brand.text, textTransform: 'uppercase', marginTop: 8 }}>
          {words.join(' ')}
        </div>
        <div style={{ marginTop: 34, width: 90, height: 10, background: brand.accent, borderRadius: 5 }} />
        <div style={{ marginTop: 26, fontFamily: brand.body, fontWeight: 700, fontSize: 28, color: brand.textDim }}>An original animated story</div>
      </div>

      {/* centre: the vertical cut */}
      <div style={{ position: 'absolute', left: (1920 - VW) / 2 - 8, top: 0, width: VW + 16, height: 1080, background: brand.accent }} />
      <div style={{ position: 'absolute', left: (1920 - VW) / 2, top: 0, width: VW, height: 1080, overflow: 'hidden', background: '#000' }}>
        <OffthreadVideo src={staticFile(video)} style={{ width: VW, height: 1080 }} />
      </div>

      {/* right: chapters */}
      <div style={{ position: 'absolute', left: 1330, top: 300, width: 520 }}>
        <div
          style={{
            display: 'inline-block',
            background: brand.accent,
            color: brand.bg,
            fontFamily: brand.display,
            fontSize: 56,
            padding: '6px 22px 0',
            borderRadius: 10,
            transform: `scale(${tagIn}) rotate(-2deg)`,
            transformOrigin: 'left center',
          }}
        >
          {chapters[cur].label}
        </div>
        <div style={{ fontFamily: brand.display, fontSize: 64, color: brand.text, textTransform: 'uppercase', marginTop: 14, lineHeight: 1.05, opacity: tagIn }}>
          {chapters[cur].title}
        </div>
        <div style={{ marginTop: 44, display: 'flex', flexDirection: 'column', gap: 16 }}>
          {chapters.map((c, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 16, opacity: i === cur ? 1 : 0.45 }}>
              <div style={{ width: 16, height: 16, borderRadius: 8, background: i === cur ? brand.accent : 'transparent', border: `3px solid ${brand.accent}` }} />
              <div style={{ fontFamily: brand.body, fontWeight: 900, fontSize: 30, color: brand.text }}>
                {c.label} · {c.title}
              </div>
            </div>
          ))}
        </div>
      </div>
      <div style={{ position: 'absolute', left: 0, right: 0, bottom: 0, height: 10, background: brand.accent }} />
    </AbsoluteFill>
  );
};

/**
 * The 16:9 frame around the vertical cut as one transparent still per chapter (title left, chapter list right,
 * yellow rails). make_wide.py lays it over a blurred copy + the cut with ffmpeg, which is far faster than
 * decoding the video twice per frame in the browser.
 */
export const WidePanel: React.FC<{ title: string; chapters: WideChapter[]; current: number }> = ({ title, chapters, current }) => {
  const words = title.replace(/^What if\s*/i, '');
  const c = chapters[current] ?? chapters[0];
  return (
    <AbsoluteFill style={{ backgroundColor: 'transparent' }}>
      <div style={{ position: 'absolute', left: 0, top: 0, width: (1920 - VW) / 2 - 8, height: 1080, background: 'linear-gradient(90deg, rgba(11,11,15,0.85), rgba(11,11,15,0.35))' }} />
      <div style={{ position: 'absolute', right: 0, top: 0, width: (1920 - VW) / 2 - 8, height: 1080, background: 'linear-gradient(270deg, rgba(11,11,15,0.85), rgba(11,11,15,0.35))' }} />
      <div style={{ position: 'absolute', left: 70, top: 70, display: 'flex', alignItems: 'center', gap: 18 }}>
        <LogoMark size={64} />
        <div style={{ fontFamily: brand.head, fontWeight: 900, fontSize: 44, color: brand.text }}>zylo</div>
      </div>
      <div style={{ position: 'absolute', left: 70, top: 290, width: 520 }}>
        <div style={{ fontFamily: brand.display, fontSize: 64, color: brand.accent, letterSpacing: 2 }}>WHAT IF...</div>
        <div style={{ fontFamily: brand.display, fontSize: words.length > 34 ? 72 : 86, lineHeight: 1.02, color: brand.text, textTransform: 'uppercase', marginTop: 8 }}>{words}</div>
        <div style={{ marginTop: 34, width: 90, height: 10, background: brand.accent, borderRadius: 5 }} />
        <div style={{ marginTop: 26, fontFamily: brand.body, fontWeight: 700, fontSize: 28, color: brand.textDim }}>An original animated story</div>
      </div>
      <div style={{ position: 'absolute', left: (1920 - VW) / 2 - 8, top: 0, width: 8, height: 1080, background: brand.accent }} />
      <div style={{ position: 'absolute', left: (1920 + VW) / 2, top: 0, width: 8, height: 1080, background: brand.accent }} />
      <div style={{ position: 'absolute', left: 1330, top: 290, width: 520 }}>
        <div style={{ display: 'inline-block', background: brand.accent, color: brand.bg, fontFamily: brand.display, fontSize: 56, padding: '6px 22px 0', borderRadius: 10, transform: 'rotate(-2deg)' }}>{c.label}</div>
        <div style={{ fontFamily: brand.display, fontSize: 64, color: brand.text, textTransform: 'uppercase', marginTop: 14, lineHeight: 1.05 }}>{c.title}</div>
        <div style={{ marginTop: 44, display: 'flex', flexDirection: 'column', gap: 16 }}>
          {chapters.map((x, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 16, opacity: i === current ? 1 : 0.5 }}>
              <div style={{ width: 16, height: 16, borderRadius: 8, background: i === current ? brand.accent : 'transparent', border: `3px solid ${brand.accent}` }} />
              <div style={{ fontFamily: brand.body, fontWeight: 900, fontSize: 30, color: brand.text }}>{x.label} · {x.title}</div>
            </div>
          ))}
        </div>
      </div>
      <div style={{ position: 'absolute', left: 0, right: 0, bottom: 0, height: 10, background: brand.accent }} />
    </AbsoluteFill>
  );
};

export type ThumbActor = { id: string; pose?: string; expr?: string; x: number; y?: number; scale?: number; facing?: number; icon?: string };
export type ThumbProps = {
  /** Thumbnail text; *word* gets the yellow block. */
  text: string;
  set: SetSpec;
  /** Top of the 16:9 window into the 1080x1920 set (default: frames the floor). */
  cropY?: number;
  cast: ThumbActor[];
  badge?: string;
  /** Optional background effects (e.g. aurora), drawn over the set, under the cast. */
  fx?: FxSpec[];
};

/** 1280x720 cartoon thumbnail: a cropped set, big characters on the right, big text on the left. */
export const ToonThumb: React.FC<ThumbProps> = ({ text, set, cropY, cast, badge, fx }) => {
  const h = (W * 9) / 16;
  const y0 = cropY ?? FLOOR_Y - h + 140;
  const parts = text.split(/\s+/);
  return (
    <AbsoluteFill style={{ backgroundColor: brand.bg }}>
      <svg viewBox={`0 ${y0} ${W} ${h}`} width="100%" height="100%" preserveAspectRatio="xMidYMid slice">
        <SetPiece spec={set} t={0} />
        {fx && fx.length ? <FxLayer fx={fx} f={40} fps={30} /> : null}
        <rect x={0} y={y0} width={W} height={h} fill="url(#thumb-shade)" />
        <defs>
          <linearGradient id="thumb-shade" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0" stopColor="#0B0B0F" stopOpacity={0.92} />
            <stop offset="0.42" stopColor="#0B0B0F" stopOpacity={0.6} />
            <stop offset="0.62" stopColor="#0B0B0F" stopOpacity={0} />
          </linearGradient>
        </defs>
        {cast.map((m, i) => {
          const s = m.scale ?? 1.4;
          const f = m.facing ?? 1;
          const body =
            m.id === 'bit' ? (
              <Bit expr={(m.expr as BitExpr) ?? 'neutral'} talk={0} t={0} icon={m.icon} />
            ) : (
              <Human look={LOOKS[m.id] ?? LOOKS.hero} pose={(m.pose as Pose) ?? 'idle'} expr={(m.expr as Expr) ?? 'neutral'} talk={m.expr === 'shocked' ? 0.8 : 0} t={0} seed={i} />
            );
          return (
            <g key={i} transform={`translate(${m.x * W} ${m.y ?? FLOOR_Y}) scale(${s * f} ${s}) translate(-150 -600)`}>
              {body}
            </g>
          );
        })}
      </svg>
      <AbsoluteFill style={{ flexDirection: 'row', flexWrap: 'wrap', alignContent: 'center', gap: '0 22px', padding: '0 0 0 50px', width: 640 }}>
        {parts.map((w, i) => {
          const accent = /^\*.*\*$/.test(w);
          return (
            <div
              key={i}
              style={{
                fontFamily: brand.display,
                fontSize: parts.length > 5 ? 112 : 130,
                lineHeight: 1.0,
                textTransform: 'uppercase',
                color: accent ? brand.bg : brand.text,
                background: accent ? brand.accent : 'transparent',
                padding: accent ? '4px 16px 0' : 0,
                margin: accent ? '6px 0 10px' : 0,
                transform: accent ? 'rotate(-2deg)' : 'none',
                WebkitTextStroke: accent ? undefined : `4px ${INK}`,
                textShadow: accent ? 'none' : `6px 6px 0 ${INK}`,
              }}
            >
              {w.replace(/\*/g, '')}
            </div>
          );
        })}
      </AbsoluteFill>
      {badge && (
        <div style={{ position: 'absolute', top: 28, left: 50, background: brand.accent, color: brand.bg, fontFamily: brand.display, fontSize: 48, padding: '4px 20px 0', borderRadius: 10 }}>
          {badge}
        </div>
      )}
      <div style={{ position: 'absolute', top: 30, right: 34 }}>
        <LogoMark size={70} />
      </div>
      <div style={{ position: 'absolute', bottom: 0, left: 0, right: 0, height: 12, background: brand.accent }} />
    </AbsoluteFill>
  );
};
