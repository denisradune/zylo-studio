// POST /api/ideas {idea, topic?, name?, email?, website (honeypot), t (ms the form was open)}
// Saves a video idea from a viewer. The owner reads them at /admin (and by e-mail if Resend is set).
import { randomBytes } from "node:crypto";
import { hasStore, hasMail, pushItem, notifyOwner, readJson, clean, rateLimited } from "./_lib.js";

const TOPICS = new Set(["science", "mind", "money", "history", "other"]);

export default async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") return res.status(405).json({ error: "Use POST." });
  if (rateLimited(req, 6, 10 * 60 * 1000, "idea:")) return res.status(429).json({ error: "Too many ideas at once. Try again in a few minutes." });

  const body = await readJson(req);
  // Bots: hidden field filled, form sent faster than a human can type, or a wall of links.
  const idea = clean(body.idea, 600);
  const tooFast = Number(body.t) > 0 && Number(body.t) < 2500;
  if (body.website || tooFast || (idea.match(/https?:\/\//g) || []).length > 2) return res.status(200).json({ ok: true });
  if (idea.length < 8) return res.status(400).json({ error: "Describe the idea in at least a few words." });

  const email = clean(body.email, 120);
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return res.status(400).json({ error: "That email doesn't look right. Fix it or leave it empty." });
  const topic = clean(body.topic, 20);
  const item = { id: randomBytes(6).toString("hex"), idea, topic: TOPICS.has(topic) ? topic : "other", name: clean(body.name, 60), email, at: new Date().toISOString() };

  if (!hasStore() && !hasMail()) {
    return res.status(503).json({ error: "The idea inbox is offline right now. Please try again later." });
  }
  let saved = false;
  if (hasStore()) { try { await pushItem("ideas", item); saved = true; } catch { /* try e-mail below */ } }
  if (hasMail()) {
    await notifyOwner(`New zylo idea: ${idea.slice(0, 60)}`, `${idea}\n\nTopic: ${item.topic}\nFrom: ${item.name || "-"} ${item.email || ""}\nAt: ${item.at}`);
    saved = true;
  }
  if (!saved) return res.status(503).json({ error: "Couldn't save your idea right now. Please try again in a minute." });
  return res.status(200).json({ ok: true });
}
