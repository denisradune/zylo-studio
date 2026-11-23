import React from 'react';
import { CalculateMetadataFunction, Composition, Still } from 'remotion';
import { FPS, H, SiteTour, TourThumb, W, layout, type TourProps } from './SiteTour';

const calculateMetadata: CalculateMetadataFunction<TourProps> = ({ props }) => ({
  durationInFrames: Math.ceil(layout(props).total * FPS),
});

const empty: TourProps = { scenes: [], boxes: {}, thumbs: [] };

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="SiteTour" component={SiteTour} width={W} height={H} fps={FPS} durationInFrames={FPS * 10} defaultProps={empty} calculateMetadata={calculateMetadata} />
    <Still id="TourThumb" component={TourThumb} width={1280} height={720} defaultProps={empty} />
  </>
);
