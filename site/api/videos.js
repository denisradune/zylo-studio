// GET /api/videos -> every video on the zylo channel (newest first).
// Merges the live YouTube RSS feed (latest 15 uploads) with videos.json (the full archive),
// so older videos never disappear when they drop out of the feed.
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fetchChannelVideos } from "./_lib.js";

export default async function handler(req, res) {
  let archive = [];
  try {
    archive = JSON.parse(await readFile(path.join(process.cwd(), "videos.json"), "utf8"));
  } catch { /* archive optional */ }

  let live = [];
  try { live = await fetchChannelVideos(); } catch { /* feed down: archive only */ }

  const byId = new Map();
  for (const v of archive) byId.set(v.id, v);
  for (const v of live) byId.set(v.id, { ...byId.get(v.id), ...v });

  const videos = [...byId.values()].sort((a, b) => String(b.published).localeCompare(String(a.published)));
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Cache-Control", "s-maxage=1800, stale-while-revalidate=86400");
  res.status(200).send(JSON.stringify({ updated: new Date().toISOString(), live: live.length > 0, videos }));
}
