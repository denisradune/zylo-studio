// GET /api/status -> which optional services are connected (booleans only, no secrets).
import { hasStore, hasMail, adminSecret } from "./_lib.js";

export default function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  res.status(200).json({
    ok: true,
    storage: hasStore(),
    ai: Boolean(process.env.ANTHROPIC_API_KEY),
    email: hasMail(),
    admin: Boolean(adminSecret()),
    youtubeApiKey: Boolean(process.env.YT_API_KEY),
  });
}
