import React from 'react';
import { CalculateMetadataFunction, Composition } from 'remotion';
import { CastSheet } from './CastSheet';
import { ZyloToon } from './ZyloToon';
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
    <Composition id="CastSheet" component={CastSheet} width={1800} height={1600} fps={30} durationInFrames={90} />
  </>
);
