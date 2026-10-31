import React from 'react';
import { CalculateMetadataFunction, Composition } from 'remotion';
import { ZyloShort } from './ZyloShort';
import type { ShortProps } from '../../zylo-shared/types';
import sample from './sample-props.json';

const FPS = 30;

// The video ends with the voiceover: duration = VO length + a short tail.
const calculateMetadata: CalculateMetadataFunction<ShortProps> = ({ props }) => ({
  durationInFrames: Math.ceil((props.voiceoverSeconds + (props.tailSeconds ?? 0.4)) * FPS),
});

export const RemotionRoot: React.FC = () => (
  <Composition
    id="ZyloShort"
    component={ZyloShort}
    width={1080}
    height={1920}
    fps={FPS}
    durationInFrames={FPS * 45}
    defaultProps={sample as ShortProps}
    calculateMetadata={calculateMetadata}
  />
);
