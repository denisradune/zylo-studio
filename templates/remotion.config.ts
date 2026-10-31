import { Config } from '@remotion/cli/config';
import fs from 'fs';

Config.setVideoImageFormat('jpeg');
Config.setOverwriteOutput(true);

// Cloud containers can't download Remotion's own browser; use a preinstalled one when present.
const localChrome = process.env.REMOTION_CHROME ?? '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell';
if (fs.existsSync(localChrome)) Config.setBrowserExecutable(localChrome);
