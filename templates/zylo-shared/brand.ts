import { continueRender, delayRender } from 'remotion';
import antonUrl from './fonts/Anton-Regular.woff2';
import interBlackUrl from './fonts/Inter-Black.ttf';
import interBoldUrl from './fonts/Inter-Bold.ttf';
import interSemiUrl from './fonts/Inter-SemiBold.woff2';
import unbounded800Url from './fonts/Unbounded-800.woff2';
import unbounded900Url from './fonts/Unbounded-900.woff2';

// Fonts ship inside the template, so renders never depend on a font CDN.
const loadFonts = () => {
  if (typeof document === 'undefined') return;
  const handle = delayRender('zylo fonts');
  const faces = [
    new FontFace('ZyloDisplay', `url(${antonUrl})`, { weight: '400' }),
    new FontFace('ZyloHead', `url(${unbounded800Url})`, { weight: '800' }),
    new FontFace('ZyloHead', `url(${unbounded900Url})`, { weight: '900' }),
    new FontFace('ZyloBody', `url(${interSemiUrl})`, { weight: '600' }),
    new FontFace('ZyloBody', `url(${interBoldUrl})`, { weight: '700' }),
    new FontFace('ZyloBody', `url(${interBlackUrl})`, { weight: '900' }),
  ];
  Promise.all(faces.map((f) => f.load().then((ff) => document.fonts.add(ff)))).then(() => continueRender(handle));
};
loadFonts();

// zylo brand: dark background, one yellow accent, heavy type.
export const brand = {
  bg: '#0B0B0F',
  bgSoft: '#16161D',
  accent: '#FFD400',
  text: '#FFFFFF',
  textDim: 'rgba(255,255,255,0.72)',
  stroke: '#000000',
  display: 'ZyloDisplay, Impact, sans-serif',
  head: 'ZyloHead, Arial Black, sans-serif',
  body: 'ZyloBody, Arial, sans-serif',
};

export type ThemeName = 'dark' | 'light';

/** Two surfaces the shorts alternate between; the accent stays yellow on both. */
export const themes = {
  dark: {
    bg: '#0B0B0F',
    glow: 'rgba(255,212,0,0.20)',
    text: '#FFFFFF',
    muted: 'rgba(255,255,255,0.38)',
    soft: 'rgba(255,255,255,0.08)',
    card: '#17171E',
    cardBorder: 'rgba(255,255,255,0.10)',
    accentText: '#FFD400',
    pill: 'rgba(16,16,22,0.88)',
    pillText: '#FFFFFF',
    pillMuted: 'rgba(255,255,255,0.36)',
  },
  light: {
    bg: '#F1F0EA',
    glow: 'rgba(255,212,0,0.45)',
    text: '#111114',
    muted: 'rgba(17,17,20,0.35)',
    soft: 'rgba(17,17,20,0.07)',
    card: '#FFFFFF',
    cardBorder: 'rgba(17,17,20,0.08)',
    // Yellow text on a light page fails contrast; the light theme accents with a darker gold.
    accentText: '#B88A00',
    pill: 'rgba(22,22,28,0.92)',
    pillText: '#FFFFFF',
    pillMuted: 'rgba(255,255,255,0.40)',
  },
} as const;

export type Theme = (typeof themes)[ThemeName];

export const CTA_LINE = 'Follow for one fact a day that changes how you see the world.';

// Thick legible outline for text over busy imagery.
export const textOutline = (px: number, color = brand.stroke) =>
  [
    `${px}px ${px}px 0 ${color}`,
    `-${px}px ${px}px 0 ${color}`,
    `${px}px -${px}px 0 ${color}`,
    `-${px}px -${px}px 0 ${color}`,
    `0 ${px * 2}px ${px * 4}px rgba(0,0,0,0.6)`,
  ].join(', ');
