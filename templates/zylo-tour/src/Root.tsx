import React from 'react';
import { CalculateMetadataFunction, Composition, Still } from 'remotion';
import { FPS, H, SiteTour, TourThumb, W, layout, type TourProps } from './SiteTour';
import { TourVertical, VH, VW, vlayout, type VProps } from './TourVertical';

const vMeta: CalculateMetadataFunction<VProps> = ({ props }) => ({ durationInFrames: Math.ceil(vlayout(props).total * FPS) });
const vEmpty: VProps = { scenes: [], boxes: {}, thumbs: [] };

const calculateMetadata: CalculateMetadataFunction<TourProps> = ({ props }) => ({
  durationInFrames: Math.ceil(layout(props).total * FPS),
});

const empty: TourProps = { scenes: [], boxes: {}, thumbs: [] };

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="SiteTour" component={SiteTour} width={W} height={H} fps={FPS} durationInFrames={FPS * 10} defaultProps={empty} calculateMetadata={calculateMetadata} />
    <Composition id="TourVertical" component={TourVertical} width={VW} height={VH} fps={FPS} durationInFrames={FPS * 10} defaultProps={vEmpty} calculateMetadata={vMeta} />
    <Still id="TourThumb" component={TourThumb} width={1280} height={720} defaultProps={empty} />
  </>
);
