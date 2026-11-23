// Shared helpers for the serverless functions (files starting with "_" are not routes on Vercel).

const CHANNEL_ID = process.env.YT_CHANNEL_ID || "UCfoc78YxRz1DXNroyI688mA";

// ---------- Storage: Upstash Redis REST (Vercel "Upstash for Redis" / KV integration) ----------
const redisUrl = () => process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
const redisToken = () => process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;

export const hasStore = () => Boolean(redisUrl() && redisToken());

export async function redis(...cmd) {
  if (!hasStore()) return null;
  const r = await fetch(redisUrl(), {
    method: "POST",
    headers: { Authorization: `Bearer ${redisToken()}`, "Content-Type": "application/json" },
    body: JSON.stringify(cmd.map(String)),
  });
  if (!r.ok) throw new Error(`store ${r.status}`);
  return (await r.json()).result;
}

export async function pushItem(list, item) {
  await redis("LPUSH", list, JSON.stringify(item));
  await redis("LTRIM", list, 0, 4999);
}

export async function listItems(list, n = 500) {
  const rows = (await redis("LRANGE", list, 0, n - 1)) || [];
  return rows.map((s) => { try { return JSON.parse(s); } catch { return null; } }).filter(Boolean);
}

// ---------- Optional e-mail notification to the owner (Resend) ----------
export async function notifyOwner(subject, text) {
  const key = process.env.RESEND_API_KEY, to = process.env.OWNER_EMAIL;
  if (!key || !to) return;
  try {
    await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
      body: JSON.stringify({ from: process.env.MAIL_FROM || "zylo <onboarding@resend.dev>", to: [to], subject, text }),
    });
  } catch { /* notification is best-effort */ }
}

// ---------- Request helpers ----------
export async function readJson(req) {
  if (req.body && typeof req.body === "object") return req.body;
  const chunks = [];
  for await (const c of req) chunks.push(c);
  try { return JSON.parse(Buffer.concat(chunks).toString("utf8") || "{}"); } catch { return {}; }
}

export const clean = (s, max) => String(s ?? "").replace(/[\u0000-\u0008\u000B-\u001F]/g, "").trim().slice(0, max);

const hits = new Map(); // simple per-instance rate limit
export function rateLimited(req, limit = 8, windowMs = 10 * 60 * 1000) {
  const ip = String(req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "anon";
  const now = Date.now();
  const arr = (hits.get(ip) || []).filter((t) => now - t < windowMs);
  arr.push(now);
  hits.set(ip, arr);
  return arr.length > limit;
}

// ---------- YouTube Data API (optional, YT_API_KEY): the complete uploads list with view counts ----------
async function fetchAllUploads(key) {
  const uploads = "UU" + CHANNEL_ID.slice(2);
  const out = [];
  let page = "";
  for (let i = 0; i < 20; i++) { // up to 1000 videos
    const u = `https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&maxResults=50&playlistId=${uploads}&key=${key}${page ? `&pageToken=${page}` : ""}`;
    const j = await (await fetch(u)).json();
    if (j.error) throw new Error(j.error.message);
    for (const it of j.items || []) {
      out.push({
        id: it.contentDetails.videoId,
        title: it.snippet.title,
        published: String(it.contentDetails.videoPublishedAt || it.snippet.publishedAt).slice(0, 10),
        description: String(it.snippet.description || "").slice(0, 400),
        views: null,
      });
    }
    if (!j.nextPageToken) break;
    page = j.nextPageToken;
  }
  for (let i = 0; i < out.length; i += 50) {
    const ids = out.slice(i, i + 50).map((v) => v.id).join(",");
    const j = await (await fetch(`https://www.googleapis.com/youtube/v3/videos?part=statistics&id=${ids}&key=${key}`)).json();
    for (const it of j.items || []) {
      const v = out.find((x) => x.id === it.id);
      if (v) v.views = Number(it.statistics?.viewCount) || null;
    }
  }
  return out;
}

// ---------- YouTube: latest 15 channel uploads from the public RSS feed ----------
const decode = (s) => s.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'");

export async function fetchChannelVideos() {
  if (process.env.YT_API_KEY) {
    try { return await fetchAllUploads(process.env.YT_API_KEY); } catch { /* fall back to RSS */ }
  }
  const r =await fetch(`https://www.youtube.com/feeds/videos.xml?channel_id=${CHANNEL_ID}`, {
    headers: { "User-Agent": "zylo-site/1.0" },
  });
  if (!r.ok) throw new Error(`rss ${r.status}`);
  const xml = await r.text();
  return [...xml.matchAll(/<entry>([\s\S]*?)<\/entry>/g)].map(([, e]) => {
    const pick = (re) => (e.match(re) || [])[1] || "";
    return {
      id: pick(/<yt:videoId>([^<]+)<\/yt:videoId>/),
      title: decode(pick(/<title>([^<]*)<\/title>/)),
      published: pick(/<published>([^<]+)<\/published>/).slice(0, 10),
      views: Number(pick(/<media:statistics views="(\d+)"/)) || null,
      description: decode(pick(/<media:description>([\s\S]*?)<\/media:description>/)).slice(0, 400),
    };
  }).filter((v) => v.id);
}
