import React from 'react';
import { CalculateMetadataFunction, Composition } from 'remotion';
import { CastSheet } from './CastSheet';
import { ZyloToon } from './ZyloToon';
import { ThumbProps, ToonThumb, ToonWide, WideProps } from './Wide';
import type { StoryProps } from '../../zylo-shared/toon/types';

const FPS = 30;

// The video ends with the voiceover.
const calculateMetadata: CalculateMetadataFunction<StoryProps> = ({ props }) => ({
  durationInFrames: Math.ceil((props.voiceoverSeconds + (props.tailSeconds ?? 0.8)) * FPS),
});

const sample: StoryProps = {
  voiceover: 'audio/voiceover.mp3',
  voiceoverSeconds: 4,
  words: [],
  lines: [],
  shots: [{ start: 0, end: 4, speaker: 'narrator', set: { type: 'street', time: 'night' }, cast: [{ id: 'hero', x: 0.5 }] }],
  endStart: 3,
};

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="ZyloToon"
      component={ZyloToon}
      width={1080}
      height={1920}
      fps={FPS}
      durationInFrames={FPS * 60}
      defaultProps={sample}
      calculateMetadata={calculateMetadata}
    />
    <Composition
      id="ToonWide"
      component={ToonWide}
      width={1920}
      height={1080}
      fps={FPS}
      durationInFrames={FPS * 10}
      defaultProps={{ video: 'full.mp4', durationSeconds: 10, title: 'What if?', chapters: [{ start: 0, label: 'PART 1', title: 'Start' }] } as WideProps}
      calculateMetadata={({ props }) => ({ durationInFrames: Math.ceil(props.durationSeconds * FPS) })}
    />
    <Composition
      id="ToonThumb"
      component={ToonThumb}
      width={1280}
      height={720}
      fps={FPS}
      durationInFrames={1}
      defaultProps={{ text: 'WHAT IF *THIS*', set: { type: 'casino' }, cast: [{ id: 'heroSuit', x: 0.75, pose: 'cheer', expr: 'grin', scale: 1.6 }] } as ThumbProps}
    />
    <Composition id="CastSheet" component={CastSheet} width={1800} height={1600} fps={30} durationInFrames={90} />
  </>
);
