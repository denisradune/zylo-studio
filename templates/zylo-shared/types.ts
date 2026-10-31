// Props shared by the zylo compositions. Everything an episode needs lives in one
// JSON file passed with `--props`; media paths are relative to the episode's
// public dir (`--public-dir`).

/** One spoken word, in the @remotion/captions `Caption` shape (ms, relative to the VO). */
export type Word = {
  text: string;
  startMs: number;
  endMs: number;
}

export type KenBurns = 'in' | 'out' | 'left' | 'right' | 'up' | 'down';

type BaseVisual = {
  /** Seconds from the start of the composition (or chapter body, in zylo-long). */
  start: number;
  end: number;
}

export type Visual =
  | (BaseVisual & { type: 'image'; src: string; motion?: KenBurns })
  | (BaseVisual & { type: 'video'; src: string; playbackRate?: number })
  /** Animated infographic: big number that counts up, with a label. */
  | (BaseVisual & { type: 'stat'; value: string; label: string; sub?: string; bgSrc?: string })
  /** Two numbers side by side, the second one in the accent colour. */
  | (BaseVisual & {
      type: 'compare';
      left: { value: string; label: string };
      right: { value: string; label: string };
      bgSrc?: string;
    })
  /** Animated horizontal bars, values relative to the largest. */
  | (BaseVisual & { type: 'bars'; title: string; items: { label: string; value: number; display?: string }[] })
  /** Kinetic statement card (words pop in one by one); `accent` words go yellow. */
  | (BaseVisual & { type: 'text'; text: string; accent?: string[]; bgSrc?: string });

/** The single hero object a beat puts centre-screen. Image paths are relative to the public dir. */
export type Hero =
  /** Full-bleed photo with Ken Burns, darkened so the headline reads. */
  | { type: 'image'; src: string; motion?: KenBurns }
  /** Floating browser-style card: image on top, title band below; `url` shows the source domain. */
  | { type: 'card'; src: string; url?: string; title: string; badge?: string }
  /** Text-only source card: the paper or page a fact comes from. */
  | { type: 'source'; url: string; title: string; meta?: string }
  /** Glossy tile with a big number or symbol and a light sweep. */
  | { type: 'tile'; value: string; label?: string }
  /** Giant number that counts up, with a label underneath. */
  | { type: 'counter'; value: string; label: string; sub?: string }
  /** Three phone-like cards fanned in 3D; the middle one lists `labels`, lighting them in turn. */
  | { type: 'phones'; srcs: string[]; labels?: string[] }
  /** Horizontal film strip of frames sliding past. */
  | { type: 'filmstrip'; srcs: string[] }
  /** Items tick on one by one. */
  | { type: 'checklist'; items: string[] }
  /** Line chart that draws itself; values are relative. */
  | { type: 'chart'; points: number[]; label: string; highlight?: string }
  | { type: 'compare'; left: { value: string; label: string }; right: { value: string; label: string } };

export type Beat = {
  start: number;
  end: number;
  /** Progress-bar segment this beat belongs to (0-based). */
  section: number;
  theme?: 'dark' | 'light';
  /** Headline above the hero; wrap accent words in *asterisks*. Consecutive beats with the same headline keep it on screen. */
  headline?: string;
  /** 'hook' = huge three-tone title for the opening beat. */
  headlineStyle?: 'hook' | 'normal';
  hero: Hero;
  /** Row of small chips under the hero, one highlighted (lists, steps). */
  chips?: { items: string[]; active: number };
  /** Voice waveform with a playhead under the hero. */
  wave?: boolean;
};

export type ShortProps = {
  voiceover: string;
  /** Exact VO length in seconds; the video ends with it (+ tailSeconds). */
  voiceoverSeconds: number;
  tailSeconds?: number;
  words: Word[];
  music?: string;
  musicVolume?: number;
  sections: number;
  beats: Beat[];
  /** Second the CTA card takes over (normally the start of the CTA sentence). */
  ctaStart: number;
};

export type Chapter = {
  title: string;
  /** Chapter VO (relative path) and its words, timed relative to that file. */
  voiceover: string;
  voiceoverSeconds: number;
  words: Word[];
  /** Visual times are relative to the start of the chapter body (after the title card). */
  visuals: Visual[];
}

export type LongProps = {
  title: string;
  /** Cold open: hook VO over visuals, no title card. */
  intro: Omit<Chapter, 'title'>;
  chapters: Chapter[];
  outro: Omit<Chapter, 'title'>;
  music?: string;
  musicVolume?: number;
  /** Seconds of chapter title card before each chapter's narration. */
  chapterCardSeconds?: number;
}

export type ThumbnailProps = {
  /** 3-4 punchy words; wrap the accent word(s) in *asterisks*. */
  text: string;
  image: string;
  /** Small badge in the corner, e.g. "TOP 10" or a number. Optional. */
  badge?: string;
}
