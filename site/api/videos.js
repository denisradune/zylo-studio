// GET /api/videos -> every video on the zylo channel, newest first.
// See getVideos() in _lib.js for how the sources are merged. Never fails: worst case it returns
// the archive shipped with the site.
import { getVideos } from "./_lib.js";

export default async function handler(req, res) {
  const { videos, live, complete } = await getVideos();
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  // Edge cache: fresh for 15 min, then served stale while refreshing (new uploads appear within ~15 min).
  res.setHeader("Cache-Control", live ? "s-maxage=900, stale-while-revalidate=86400" : "s-maxage=60");
  res.status(200).send(JSON.stringify({ updated: new Date().toISOString(), live, complete, count: videos.length, videos }));
}
