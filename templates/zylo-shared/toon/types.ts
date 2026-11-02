import type { BitExpr, Expr, Pose } from './Character';
import type { SetSpec } from './Backgrounds';
import type { FxSpec } from './Fx';
import type { UiSpec } from './Ui';

export type CastMember = {
  /** A key of LOOKS (hero, friend, boss, zombie, ...) or 'bit' for the AI. */
  id: string;
  /** Horizontal position of the feet, 0..1 of the frame width. */
  x: number;
  scale?: number;
  /** Pushes the actor back (smaller, higher, drawn behind): 0 front .. 1 far. */
  depth?: number;
  pose?: Pose;
  expr?: Expr | BitExpr;
  facing?: 1 | -1;
  gaze?: number;
  /** Bit only: symbol on its screen instead of eyes. */
  icon?: string;
  enter?: 'left' | 'right' | 'pop' | 'none';
  /** Walk/run to this x during the shot. */
  moveTo?: number;
  /** Which speaker name in the script this actor voices (defaults to id). */
  voice?: string;
  /** Raise the actor by this many canvas px (e.g. Bit riding on a car roof). */
  lift?: number;
  /** Car only: body colour. */
  color?: string;
};

export type Shot = {
  start: number;
  end: number;
  speaker: string;
  set: SetSpec;
  cast: CastMember[];
  fx?: FxSpec[];
  ui?: UiSpec;
  camera?: { zoom?: number; x?: number; y?: number; push?: number; shake?: number };
  transition?: 'cut' | 'flash' | 'whip';
  /** Sound effects from brand/sfx, `at` seconds into the shot. */
  sfx?: { type: string; at?: number; volume?: number }[];
};

export type StoryWord = { text: string; startMs: number; endMs: number; line: number; emph?: boolean };

export type StoryProps = {
  voiceover: string;
  voiceoverSeconds: number;
  tailSeconds?: number;
  words: StoryWord[];
  /** Per spoken line: who says it. */
  lines: { speaker: string; start: number; end: number }[];
  /** Display names for speaker tags (narrator gets none). */
  names?: Record<string, string>;
  music?: string;
  musicVolume?: number;
  shots: Shot[];
  /** Second the end card takes over. */
  endStart: number;
  endText?: string;
  endSub?: string;
  /** Series badge shown top-left in a Shorts part, e.g. "PART 2/3". */
  partLabel?: string;
  /** Split-screen Short: story on top (1080x960), an original satisfying loop below. */
  split?: { kind: 'press' | 'sand' | 'marbles'; seed?: number };
  /** Full-length version: a chapter card at the start of each part after the first. */
  chapters?: { start: number; label: string; title: string }[];
};
