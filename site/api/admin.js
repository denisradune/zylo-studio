// POST /api/admin  -> owner-only access to viewer ideas and questions (used by /admin and scripts/ideas.py).
// Auth: {password} in the body, or "Authorization: Bearer <ADMIN_PASSWORD>".
//   {action:"list", redact?:true}                     -> ideas (with review status) and questions; redact drops e-mails
//   {action:"review", id, status, note?, video?}      -> set an idea's status: new | shortlisted | used | rejected
// When an idea is marked "used" with a video link, its author is e-mailed (if they left an address and Resend is set).
import { hasStore, listItems, readJson, rateLimited, checkAdmin, adminSecret, hasMail, redis, clean, sendMail } from "./_lib.js";

const STATUSES = new Set(["new", "shortlisted", "used", "rejected"]);
const ideaId = (i) => i.id || i.at;

async function statuses() {
  const flat = (await redis("HGETALL", "idea:status")) || [];
  const map = {};
  for (let i = 0; i < flat.length; i += 2) { try { map[flat[i]] = JSON.parse(flat[i + 1]); } catch {} }
  return map;
}

export default async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") return res.status(405).json({ error: "method" });
  if (rateLimited(req, 30, 10 * 60 * 1000, "admin:")) return res.status(429).json({ error: "too_many" });
  if (!adminSecret()) return res.status(503).json({ error: "no_password" });
  const body = await readJson(req);
  const bearer = String(req.headers.authorization || "").replace(/^Bearer\s+/i, "");
  if (!checkAdmin(body.password || bearer)) return res.status(401).json({ error: "wrong_password" });
  if (!hasStore()) return res.status(200).json({ storage: false, email: hasMail(), ai: Boolean(process.env.ANTHROPIC_API_KEY), ideas: [], questions: [] });

  try {
    if (body.action === "review") {
      const id = clean(body.id, 40), status = clean(body.status, 20);
      if (!id || !STATUSES.has(status)) return res.status(400).json({ error: "bad_review" });
      const ideas = await listItems("ideas", 5000);
      const idea = ideas.find((i) => ideaId(i) === id);
      if (!idea) return res.status(404).json({ error: "no_idea" });
      const prev = (await statuses())[id] || {};
      const rec = { status, note: clean(body.note, 300), video: clean(body.video, 200), at: new Date().toISOString(), notified: prev.notified || false };
      if (status === "used" && rec.video && idea.email && !rec.notified) {
        rec.notified = await sendMail(idea.email, "Your idea is now a zylo video!",
          `Hi${idea.name ? " " + idea.name : ""}!\n\nYou suggested this on zylo.video:\n"${idea.idea}"\n\nWe made it into a video: ${rec.video}\n\nThanks for the idea!\nzylo · https://zylo.video`);
      }
      await redis("HSET", "idea:status", id, JSON.stringify(rec));
      return res.status(200).json({ ok: true, id, ...rec });
    }

    const [ideas, questions, st] = await Promise.all([listItems("ideas"), listItems("questions"), statuses()]);
    const out = ideas.map((i) => {
      const s = st[ideaId(i)] || { status: "new" };
      const row = { ...i, id: ideaId(i), review: s };
      if (body.redact) delete row.email;
      return row;
    });
    return res.status(200).json({ storage: true, email: hasMail(), ai: Boolean(process.env.ANTHROPIC_API_KEY), ideas: out, questions: body.redact ? [] : questions });
  } catch {
    return res.status(200).json({ storage: true, storeError: true, email: hasMail(), ai: Boolean(process.env.ANTHROPIC_API_KEY), ideas: [], questions: [] });
  }
}
