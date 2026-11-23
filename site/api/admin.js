// POST /api/admin {password} -> owner-only: all viewer ideas and questions (used by /admin).
import { hasStore, listItems, readJson, rateLimited, checkAdmin, adminSecret, hasMail } from "./_lib.js";

export default async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") return res.status(405).json({ error: "method" });
  if (rateLimited(req, 10, 10 * 60 * 1000, "admin:")) return res.status(429).json({ error: "too_many" });
  if (!adminSecret()) return res.status(503).json({ error: "no_password" });
  const body = await readJson(req);
  if (!checkAdmin(body.password)) return res.status(401).json({ error: "wrong_password" });

  let ideas = [], questions = [], storeError = false;
  if (hasStore()) {
    try { [ideas, questions] = await Promise.all([listItems("ideas"), listItems("questions")]); }
    catch { storeError = true; }
  }
  return res.status(200).json({
    storage: hasStore(), storeError, email: hasMail(), ai: Boolean(process.env.ANTHROPIC_API_KEY),
    ideas, questions,
  });
}
