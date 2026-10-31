import { continueRender, delayRender } from 'remotion';
import antonUrl from './fonts/Anton-Regular.woff2';
import interBlackUrl from './fonts/Inter-Black.ttf';
import interBoldUrl from './fonts/Inter-Bold.ttf';

// Fonts ship inside the template, so renders never depend on a font CDN.
const loadFonts = () => {
  if (typeof document === 'undefined') return;
  const handle = delayRender('zylo fonts');
  const faces = [
    new FontFace('ZyloDisplay', `url(${antonUrl})`, { weight: '400' }),
    new FontFace('ZyloBody', `url(${interBoldUrl})`, { weight: '700' }),
    new FontFace('ZyloBody', `url(${interBlackUrl})`, { weight: '900' }),
  ];
  Promise.all(faces.map((f) => f.load().then((ff) => document.fonts.add(ff)))).then(() => continueRender(handle));
};
loadFonts();

// zylo brand: dark background, one yellow accent, heavy condensed type.
export const brand = {
  bg: '#0B0B0F',
  bgSoft: '#16161D',
  accent: '#FFD400',
  text: '#FFFFFF',
  textDim: 'rgba(255,255,255,0.72)',
  stroke: '#000000',
  display: 'ZyloDisplay, Impact, sans-serif',
  body: 'ZyloBody, Arial Black, sans-serif',
};

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
