import React from 'react';
import { CalculateMetadataFunction, Composition, Still } from 'remotion';
import { FPS, ZyloLong, ZyloThumbnail, layout } from './ZyloLong';
import type { LongProps, ThumbnailProps } from '../../zylo-shared/types';
import sample from './sample-props.json';

const calculateMetadata: CalculateMetadataFunction<LongProps> = ({ props }) => ({
  durationInFrames: Math.ceil((layout(props).totalSeconds + 1) * FPS),
});

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="ZyloLong"
      component={ZyloLong}
      width={1920}
      height={1080}
      fps={FPS}
      durationInFrames={FPS * 600}
      defaultProps={sample as LongProps}
      calculateMetadata={calculateMetadata}
    />
    <Still
      id="ZyloThumbnail"
      component={ZyloThumbnail}
      width={1280}
      height={720}
      defaultProps={{ text: 'YOUR BRAIN *LIES*', image: 'images/thumb.jpg' } as ThumbnailProps}
    />
  </>
);
