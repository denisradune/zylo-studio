import React from 'react';
import { AbsoluteFill, Audio, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { brand, themes } from '../../zylo-shared/brand';
import { Backdrop, Chips, Headline, LogoMark, SentenceCaptions, TopBar, Waveform } from '../../zylo-shared/Chrome';
import { HeroLayer } from '../../zylo-shared/Heroes';
import type { Beat, ShortProps } from '../../zylo-shared/types';

const themeOf = (b?: Beat) => themes[b?.theme ?? 'dark'];

/** Fades a beat's own backdrop in over the previous one, so theme switches dissolve. */
const BeatBackdrop: React.FC<{ beat: Beat }> = ({ beat }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 7], [0, 1], { extrapolateRight: 'clamp' });
  return (
    <AbsoluteFill style={{ opacity }}>
      <Backdrop theme={themeOf(beat)} />
    </AbsoluteFill>
  );
};

/** Closing card: shining logo, name, Follow button. The CTA sentence keeps running in the caption pill. */
const CtaCard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 13 } });
  const s2 = spring({ frame: frame - 8, fps, config: { damping: 13 } });
  const theme = themes.dark;
  return (
    <AbsoluteFill style={{ opacity: interpolate(frame, [0, 6], [0, 1], { extrapolateRight: 'clamp' }) }}>
      <Backdrop theme={theme} glowY={0.38} />
      <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', top: -200 }}>
        <div style={{ transform: `scale(${s})` }}>
          <LogoMark size={300} shine />
        </div>
        <div style={{ marginTop: 40, fontFamily: brand.head, fontWeight: 900, fontSize: 96, color: '#FFFFFF', opacity: s2 }}>zylo</div>
        <div style={{ marginTop: 6, fontFamily: brand.body, fontWeight: 700, fontSize: 38, color: theme.muted, opacity: s2 }}>
          one fact a day
        </div>
        <div
          style={{
            marginTop: 44,
            padding: '24px 80px',
            borderRadius: 999,
            background: brand.accent,
            color: brand.bg,
            fontFamily: brand.head,
            fontWeight: 900,
            fontSize: 52,
            transform: `scale(${s2 * (1 + Math.sin(frame / 6) * 0.02)})`,
            boxShadow: '0 20px 60px rgba(255,212,0,0.35)',
          }}
        >
          Follow
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

type Group = { headline: string; hook: boolean; start: number; end: number; theme: Beat['theme'] };

/** Consecutive beats sharing a headline keep one headline on screen instead of re-animating it. */
const headlineGroups = (beats: Beat[]): Group[] => {
  const groups: Group[] = [];
  beats.forEach((b) => {
    if (!b.headline) return;
    const last = groups[groups.length - 1];
    const hook = b.headlineStyle === 'hook';
    if (last && last.headline === b.headline && last.theme === b.theme && Math.abs(last.end - b.start) < 0.3) {
      last.end = b.end;
    } else {
      groups.push({ headline: b.headline, hook, start: b.start, end: b.end, theme: b.theme });
    }
  });
  return groups;
};

export const ZyloShort: React.FC<ShortProps> = (props) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const ctaFrame = Math.round(props.ctaStart * fps);
  const musicVolume = props.musicVolume ?? 0.15;

  const current = props.beats.find((b) => t >= b.start && t < b.end) ?? props.beats[props.beats.length - 1];
  const inCta = frame >= ctaFrame;
  const theme = inCta ? themes.dark : themeOf(current);
  const secBeats = props.beats.filter((b) => b.section === current.section);
  const secStart = secBeats[0]?.start ?? 0;
  const secEnd = secBeats[secBeats.length - 1]?.end ?? 1;
  const secProgress = Math.min(1, Math.max(0, (t - secStart) / (secEnd - secStart)));

  return (
    <AbsoluteFill style={{ backgroundColor: brand.bg }}>
      {props.beats.map((b, i) => {
        const from = Math.round(b.start * fps);
        const dur = Math.max(1, Math.round(b.end * fps) - from);
        const th = themeOf(b);
        return (
          <Sequence key={i} from={from} durationInFrames={dur} premountFor={fps}>
            <BeatBackdrop beat={b} />
            <HeroLayer hero={b.hero} theme={th} dur={dur} />
            {b.chips && <Chips items={b.chips.items} active={b.chips.active} theme={th} top={1255} />}
            {b.wave && <Waveform src={props.voiceover} theme={th} top={1265} />}
          </Sequence>
        );
      })}

      {headlineGroups(props.beats).map((g, i) => {
        const from = Math.round(g.start * fps);
        return (
          <Sequence key={`h${i}`} from={from} durationInFrames={Math.max(1, Math.round(g.end * fps) - from)}>
            <Headline text={g.headline} theme={themes[g.theme ?? 'dark']} hook={g.hook} />
          </Sequence>
        );
      })}

      <Sequence from={ctaFrame}>
        <CtaCard />
      </Sequence>

      <TopBar theme={theme} sections={props.sections} section={inCta ? props.sections - 1 : current.section} sectionProgress={inCta ? 1 : secProgress} />
      <SentenceCaptions words={props.words} theme={theme} centerY={0.78} />

      <Audio src={staticFile(props.voiceover)} />
      {props.music && (
        <Audio
          src={staticFile(props.music)}
          loop
          volume={(f) =>
            musicVolume *
            interpolate(f, [0, 10, durationInFrames - fps, durationInFrames], [0, 1, 1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })
          }
        />
      )}
    </AbsoluteFill>
  );
};
