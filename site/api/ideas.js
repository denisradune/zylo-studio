// POST /api/ideas  {idea, name?, email?, website(honeypot)}  -> saves a video idea from a viewer
// GET  /api/ideas?key=ADMIN_KEY                              -> owner-only list (used by /admin)
import { hasStore, pushItem, listItems, notifyOwner, readJson, clean, rateLimited } from "./_lib.js";

export default async function handler(req, res) {
  if (req.method === "GET") {
    if (!process.env.ADMIN_KEY || req.query.key !== process.env.ADMIN_KEY) return res.status(401).json({ error: "Wrong admin key." });
    const [ideas, questions] = hasStore() ? await Promise.all([listItems("ideas"), listItems("questions")]) : [[], []];
    return res.status(200).json({ storage: hasStore(), ideas, questions });
  }
  if (req.method !== "POST") return res.status(405).json({ error: "Use POST." });
  if (rateLimited(req)) return res.status(429).json({ error: "Too many ideas at once. Try again in a few minutes." });

  const body = await readJson(req);
  if (body.website) return res.status(200).json({ ok: true }); // bot filled the hidden field
  const idea = clean(body.idea, 600);
  if (idea.length < 8) return res.status(400).json({ error: "Describe the idea in at least a few words." });

  const item = {
    idea,
    topic: clean(body.topic, 40),
    name: clean(body.name, 60),
    email: clean(body.email, 120),
    at: new Date().toISOString(),
  };
  if (!hasStore() && !process.env.RESEND_API_KEY) {
    return res.status(503).json({ error: "Idea inbox is not connected yet. Please try again later." });
  }
  try {
    if (hasStore()) await pushItem("ideas", item);
    await notifyOwner(`New zylo idea: ${idea.slice(0, 60)}`, `${idea}\n\nTopic: ${item.topic}\nFrom: ${item.name} ${item.email}`);
  } catch {
    return res.status(500).json({ error: "Could not save the idea. Please try again." });
  }
  return res.status(200).json({ ok: true });
}
