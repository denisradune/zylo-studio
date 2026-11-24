// Shared helpers for the serverless functions (files starting with "_" are not routes on Vercel).
import { readFile } from "node:fs/promises";
import path from "node:path";
import { timingSafeEqual, createHash } from "node:crypto";

export const CHANNEL_ID = process.env.YT_CHANNEL_ID || "UCfoc78YxRz1DXNroyI688mA";

// ---------- Storage: Upstash Redis REST (Vercel "Upstash for Redis" / KV integration) ----------
// The Vercel integration names the variables <PREFIX>_REST_API_URL / _REST_API_TOKEN (prefix KV by default, but the
// owner can pick another one), so fall back to any matching pair.
const anyEnv = (suffix) => Object.keys(process.env).sort().find((k) => k.endsWith(suffix) && !k.includes("READ_ONLY") && process.env[k]);
const redisUrl = () => process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL || process.env[anyEnv("_REST_API_URL")];
const redisToken = () => process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN || process.env[anyEnv("_REST_API_TOKEN")];

export const hasStore = () => Boolean(redisUrl() && redisToken());

export async function redis(...cmd) {
  if (!hasStore()) return null;
  const r = await fetch(redisUrl(), {
    method: "POST",
    headers: { Authorization: `Bearer ${redisToken()}`, "Content-Type": "application/json" },
    body: JSON.stringify(cmd.map(String)),
    signal: AbortSignal.timeout(6000),
  });
  if (!r.ok) throw new Error(`store ${r.status}`);
  return (await r.json()).result;
}

export async function pushItem(list, item) {
  await redis("LPUSH", list, JSON.stringify(item));
  await redis("LTRIM", list, 0, 4999);
}

export async function listItems(list, n = 1000) {
  const rows = (await redis("LRANGE", list, 0, n - 1)) || [];
  return rows.map((s) => { try { return JSON.parse(s); } catch { return null; } }).filter(Boolean);
}

// ---------- Optional e-mail notification to the owner (Resend) ----------
export const hasMail = () => Boolean(process.env.RESEND_API_KEY && process.env.OWNER_EMAIL);

export async function notifyOwner(subject, text) {
  if (!hasMail()) return;
  try {
    await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify({ from: process.env.MAIL_FROM || "zylo <onboarding@resend.dev>", to: [process.env.OWNER_EMAIL], subject, text }),
      signal: AbortSignal.timeout(6000),
    });
  } catch { /* notification is best-effort */ }
}

/** E-mail to anyone (used to tell a viewer their idea became a video). Needs a Resend domain in MAIL_FROM. */
export async function sendMail(to, subject, text) {
  if (!process.env.RESEND_API_KEY || !to) return false;
  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify({ from: process.env.MAIL_FROM || "zylo <onboarding@resend.dev>", to: [to], subject, text }),
      signal: AbortSignal.timeout(6000),
    });
    return r.ok;
  } catch { return false; }
}

// ---------- Admin password (ADMIN_PASSWORD, or the older ADMIN_KEY) ----------
export const adminSecret = () => process.env.ADMIN_PASSWORD || process.env.ADMIN_KEY || "";

export function checkAdmin(given) {
  const secret = adminSecret();
  if (!secret || !given) return false;
  const h = (s) => createHash("sha256").update(String(s)).digest();
  return timingSafeEqual(h(given), h(secret));
}

// ---------- Request helpers ----------
export async function readJson(req) {
  if (req.body && typeof req.body === "object") return req.body;
  if (typeof req.body === "string") { try { return JSON.parse(req.body); } catch { return {}; } }
  const chunks = [];
  for await (const c of req) chunks.push(c);
  try { return JSON.parse(Buffer.concat(chunks).toString("utf8") || "{}"); } catch { return {}; }
}

export const clean = (s, max) => String(s ?? "").replace(/[\u0000-\u0008\u000B-\u001F\u007F]/g, "").trim().slice(0, max);

const hits = new Map(); // simple per-instance rate limit
export function rateLimited(req, limit = 8, windowMs = 10 * 60 * 1000, bucket = "") {
  const ip = String(req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "anon";
  const key = bucket + ip, now = Date.now();
  const arr = (hits.get(key) || []).filter((t) => now - t < windowMs);
  arr.push(now);
  hits.set(key, arr);
  return arr.length > limit;
}

// ======================================================================================
// Videos. Several sources are merged so the archive is complete and survives any one of
// them being down:
//   1. videos.json            — full archive shipped with the site (exact dates)
//   2. Redis "videos" hash     — every video the site has ever seen (if storage is connected)
//   3. YouTube Data API        — complete list with views (only if YT_API_KEY is set)
//   4. Channel uploads list    — complete list, titles and views, no key needed
//   5. Channel RSS feed        — latest 15 uploads with exact dates and descriptions
//   6. Per-video page data     — exact date + description for videos still missing one
// ======================================================================================

const decode = (s) => s.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'");

async function fetchRss() {
  const r = await fetch(`https://www.youtube.com/feeds/videos.xml?channel_id=${CHANNEL_ID}`, {
    headers: { "User-Agent": "zylo-site/1.0" }, signal: AbortSignal.timeout(7000),
  });
  if (!r.ok) throw new Error(`rss ${r.status}`);
  const xml = await r.text();
  return [...xml.matchAll(/<entry>([\s\S]*?)<\/entry>/g)].map(([, e]) => {
    const pick = (re) => (e.match(re) || [])[1] || "";
    const views = pick(/<media:statistics views="(\d+)"/);
    return {
      id: pick(/<yt:videoId>([^<]+)<\/yt:videoId>/),
      title: decode(pick(/<title>([^<]*)<\/title>/)),
      published: pick(/<published>([^<]+)<\/published>/).slice(0, 10),
      views: views === "" ? null : Number(views),
      description: decode(pick(/<media:description>([\s\S]*?)<\/media:description>/)).slice(0, 400),
    };
  }).filter((v) => v.id);
}

// YouTube's own web client endpoints (public, no key).
const YT_CTX = { client: { clientName: "WEB", clientVersion: "2.20251101.00.00", hl: "en", gl: "US" } };
async function yti(endpoint, body) {
  const r = await fetch(`https://www.youtube.com/youtubei/v1/${endpoint}?prettyPrint=false`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "Accept-Language": "en-US,en" },
    body: JSON.stringify({ context: YT_CTX, ...body }),
    signal: AbortSignal.timeout(8000),
  });
  if (!r.ok) throw new Error(`yt ${endpoint} ${r.status}`);
  return r.json();
}
function walk(o, f) {
  if (!o || typeof o !== "object") return;
  f(o);
  for (const k in o) walk(o[k], f);
}
export function parseViews(s) {
  s = String(s || "");
  if (/no views/i.test(s)) return 0;
  const m = s.replace(/,/g, "").match(/([\d.]+)\s*([KMB])?\s*views?/i);
  if (!m) return null;
  return Math.round(parseFloat(m[1]) * ({ K: 1e3, M: 1e6, B: 1e9 }[(m[2] || "").toUpperCase()] || 1));
}
function agoToDate(s) {
  const m = String(s || "").match(/(\d+)\s*(second|minute|hour|day|week|month|year)s?\s+ago/i);
  if (!m) return null;
  const unit = { second: 1e3, minute: 6e4, hour: 36e5, day: 864e5, week: 6048e5, month: 2592e6, year: 31536e6 }[m[2].toLowerCase()];
  return new Date(Date.now() - Number(m[1]) * unit).toISOString().slice(0, 10);
}

// Complete uploads list (Shorts and long videos), newest first.
async function fetchUploads() {
  let j = await yti("browse", { browseId: "VLUU" + CHANNEL_ID.slice(2) });
  const out = [];
  for (let page = 0; page < 40 && j; page++) {
    let cont = null;
    walk(j, (o) => {
      if (o.lockupViewModel) {
        const l = o.lockupViewModel, m = l.metadata?.lockupMetadataViewModel;
        const parts = [];
        walk(m?.metadata, (x) => { if (x.metadataParts) for (const p of x.metadataParts) if (p.text?.content) parts.push(p.text.content); });
        let duration = "";
        walk(l.contentImage, (x) => { if (x.thumbnailBadgeViewModel?.text && /^\d+:\d\d/.test(x.thumbnailBadgeViewModel.text)) duration = x.thumbnailBadgeViewModel.text; });
        if (l.contentId && m?.title?.content) {
          out.push({
            id: l.contentId,
            title: m.title.content,
            views: parts.map(parseViews).find((n) => n != null) ?? null,
            approx: parts.map(agoToDate).find(Boolean) || null,
            duration,
          });
        }
      }
      if (o.continuationCommand?.token) cont = o.continuationCommand.token;
    });
    if (!cont) return { list: out, complete: true };
    try { j = await yti("browse", { continuation: cont }); } catch { return { list: out, complete: false }; }
  }
  return { list: out, complete: false };
}

// Exact publish date and description of one video.
export async function fetchVideoDetails(id) {
  const j = await yti("next", { videoId: id });
  let date = "", description = "", views = null;
  walk(j, (o) => {
    if (o.videoPrimaryInfoRenderer) {
      date = o.videoPrimaryInfoRenderer.dateText?.simpleText || date;
      views = parseViews(o.videoPrimaryInfoRenderer.viewCount?.videoViewCountRenderer?.viewCount?.simpleText) ?? views;
    }
    if (o.videoSecondaryInfoRenderer?.attributedDescription?.content) description = o.videoSecondaryInfoRenderer.attributedDescription.content;
  });
  const m = date.match(/([A-Z][a-z]{2,8}\.? \d{1,2}, \d{4})/);
  const d = m ? new Date(`${m[1]} 12:00 UTC`) : null;
  return {
    published: d && !isNaN(d) ? d.toISOString().slice(0, 10) : null,
    description: description.slice(0, 400),
    views,
  };
}

// YouTube Data API (optional, YT_API_KEY): complete list with exact dates and view counts.
async function fetchAllUploadsApi(key) {
  const uploads = "UU" + CHANNEL_ID.slice(2);
  const out = [];
  let page = "";
  for (let i = 0; i < 20; i++) {
    const u = `https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&maxResults=50&playlistId=${uploads}&key=${key}${page ? `&pageToken=${page}` : ""}`;
    const j = await (await fetch(u, { signal: AbortSignal.timeout(8000) })).json();
    if (j.error) throw new Error(j.error.message);
    for (const it of j.items || []) {
      out.push({
        id: it.contentDetails.videoId,
        title: it.snippet.title,
        published: String(it.contentDetails.videoPublishedAt || it.snippet.publishedAt).slice(0, 10),
        description: String(it.snippet.description || "").slice(0, 400),
      });
    }
    if (!j.nextPageToken) break;
    page = j.nextPageToken;
  }
  for (let i = 0; i < out.length; i += 50) {
    const ids = out.slice(i, i + 50).map((v) => v.id).join(",");
    const j = await (await fetch(`https://www.googleapis.com/youtube/v3/videos?part=statistics&id=${ids}&key=${key}`, { signal: AbortSignal.timeout(8000) })).json();
    for (const it of j.items || []) {
      const v = out.find((x) => x.id === it.id);
      if (v) v.views = Number(it.statistics?.viewCount) || 0;
    }
  }
  return out;
}

async function readArchive() {
  try { return JSON.parse(await readFile(path.join(process.cwd(), "videos.json"), "utf8")); } catch { return []; }
}
async function readStoredVideos() {
  try {
    const flat = (await redis("HGETALL", "videos")) || [];
    const out = [];
    for (let i = 0; i < flat.length; i += 2) { try { out.push(JSON.parse(flat[i + 1])); } catch {} }
    return out;
  } catch { return []; }
}

// Rubric of a video: first by the series hashtag, then by words in the title. First match wins.
const RUBRIC_TAGS = [
  ["science", /#(seaslug|science|cordyceps|zombies?|biology|body|health|animals?)\b/i],
  ["history", /#(krakatoa|volcano|solarstorm|northernlights|halleyscomet|comet|space|astronomy|history)\b/i],
  ["mind", /#(relatable|funny|casino|gambling|psychology|brain|mind)\b/i],
  ["money", /#(money|blackfriday|sale|ai|chatgpt|aitips|christmas|santa|tech|business|economy)\b/i],
];
const RUBRIC_WORDS = [
  ["science", /zombie|sea slug|fungus|sunlight|virus|\bbody\b|\bblood\b|\bsleep\b/i],
  ["mind", /casino|gambl|crush|group chat|meme|voice message|\bbet\b|psycholog|\bbrain\b|habit/i],
  ["history", /krakatoa|volcano|solar|comet|telegraph|planet|moon|mars|space|ancient|histor|century/i],
  ["money", /money|price|cent\b|\$|\bai\b|santa|christmas|\bbots?\b|robot|bank|business|tech/i],
];
export function rubricOf(v) {
  const title = String(v.title || ""), text = `${title} ${v.description || ""}`;
  for (const [k, re] of RUBRIC_TAGS) if (re.test(text)) return k;
  for (const [k, re] of RUBRIC_WORDS) if (re.test(title)) return k;
  return "science";
}

let memo = null;
const MEMO_MS = 10 * 60 * 1000;

// Returns { videos, live, complete } — videos newest first. Never throws.
export async function getVideos({ fresh = false } = {}) {
  if (!fresh && memo && Date.now() - memo.at < MEMO_MS) return memo.data;

  const byId = new Map();
  const merge = (v, { exactDate = true } = {}) => {
    if (!v || !v.id) return;
    const o = byId.get(v.id) || { id: v.id };
    for (const [k, x] of Object.entries(v)) {
      if (x == null || x === "" || k === "approx") continue;
      if (k === "published" && !exactDate) continue;
      o[k] = x;
    }
    if (v.approx && !o.published) o.approx = v.approx;
    byId.set(v.id, o);
  };

  const [archive, stored] = await Promise.all([readArchive(), readStoredVideos()]);
  archive.forEach((v) => merge(v));
  stored.forEach((v) => merge(v));

  const apiKey = process.env.YT_API_KEY;
  const [api, uploads, rss] = await Promise.allSettled([
    apiKey ? fetchAllUploadsApi(apiKey) : Promise.reject(new Error("no key")),
    fetchUploads(),
    fetchRss(),
  ]);
  if (uploads.status === "fulfilled") uploads.value.list.forEach((v) => merge(v, { exactDate: false }));
  if (rss.status === "fulfilled") rss.value.forEach((v) => merge(v.views == null ? { ...v, views: undefined } : v));
  if (api.status === "fulfilled") api.value.forEach((v) => merge(v));

  // Drop videos that were deleted or made private on YouTube, when we have an authoritative list.
  const authoritative = api.status === "fulfilled" && api.value.length ? api.value
    : uploads.status === "fulfilled" && uploads.value.complete && uploads.value.list.length ? uploads.value.list : null;
  if (authoritative) {
    const keep = new Set([...authoritative.map((v) => v.id), ...(rss.status === "fulfilled" ? rss.value.map((v) => v.id) : [])]);
    for (const id of [...byId.keys()]) if (!keep.has(id)) byId.delete(id);
  }

  // Fill in exact dates for videos that only have an estimate (new uploads that left the RSS window).
  const missing = [...byId.values()].filter((v) => !v.published).slice(0, 15);
  await Promise.allSettled(missing.map(async (v) => {
    const d = await fetchVideoDetails(v.id);
    if (d.published) { v.published = d.published; delete v.approx; }
    if (d.description && !v.description) v.description = d.description;
  }));
  for (const v of byId.values()) if (!v.published && v.approx) { v.published = v.approx; v.estimated = true; }
  for (const v of byId.values()) { delete v.approx; v.pillar = rubricOf(v); }

  const videos = [...byId.values()].filter((v) => v.published).sort((a, b) => String(b.published).localeCompare(String(a.published)));
  const live = [api, uploads, rss].some((r) => r.status === "fulfilled");

  // Remember everything we have seen, so the archive survives YouTube outages.
  if (hasStore() && live) {
    try {
      const args = [];
      for (const v of videos) if (!v.estimated) args.push(v.id, JSON.stringify(v));
      if (args.length) await redis("HSET", "videos", ...args);
    } catch { /* best-effort */ }
  }

  const data = { videos, live, complete: Boolean(authoritative) };
  if (videos.length) memo = { at: Date.now(), data };
  return data;
}
