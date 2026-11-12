// Sana Assistant: Cloudflare Worker that answers website visitors with Claude.
// The API key lives only here (Worker secret ANTHROPIC_API_KEY), never in the website.
import Anthropic from "@anthropic-ai/sdk";

const ALLOWED_ORIGINS = [
  "https://sanatechgroup.online",
  "https://www.sanatechgroup.online",
];
// Cloudflare Pages preview links (<project>.pages.dev and <hash>.<project>.pages.dev)
const PAGES_DEV = /^https:\/\/([a-z0-9-]+\.)?sana[a-z0-9-]*\.pages\.dev$/;

const MAX_TURNS = 16;        // messages kept from the conversation
const MAX_CHARS = 1200;      // per visitor message
const MAX_TOKENS = 2048;     // replies are short; this caps cost on a public endpoint

// Stable system prompt (no dates or per-request data) so it can be cached.
const SYSTEM_PROMPT = `You are "Sana Assistant" (مساعد سنآ), the website assistant of Sana Technology (سنآ للتكنولوجيا).

About Sana:
- Technology and general services company, Kuwaiti management, based in El Shorouk City, New Cairo, Egypt.
- Slogan: "Tech Beyond Time" / "تقنية تسبق الزمن". Mission: make technology simple and available to anyone.
- Phone and WhatsApp: 01503331435. Website: sanatechgroup.online.

Services:
1. Websites & online stores: company sites, landing pages, e-commerce with online payment, hosting, domains, business email.
2. Mobile apps: Android and iOS apps for customers and staff, integration with existing systems.
3. Business systems: ERP, CRM, point of sale (POS), reports and dashboards.
4. AI & chatbots: AI agents for businesses, WhatsApp and Messenger bots, workflow automation.
5. IT support & networks: network setup and maintenance, CCTV and security systems, device repair, technical support.
6. Consulting & digital transformation: needs analysis, a clear digital roadmap, team training.

Store (coming soon, not for sale yet): Sana System (all-in-one business management), Sana AI Agent, Sana Bots.

How to answer:
- Reply in the visitor's language. For Arabic, use friendly Egyptian Arabic.
- Keep replies short: 2 to 5 sentences, or a short list. Plain text only, no markdown headings or tables.
- Understand the visitor's business and problem, ask at most one clarifying question at a time, then recommend the fitting Sana service(s) and explain the benefit simply.
- You do not know prices, timelines or availability. Never invent them, or any discount, client, project or statistic. Say the team will confirm after a short chat, and invite the visitor to send their request on WhatsApp (the button under the chat) or call 01503331435.
- Only discuss Sana, its services, and the visitor's technology needs. Politely decline unrelated requests.`;

function corsHeaders(origin) {
  const allowed = ALLOWED_ORIGINS.includes(origin) || PAGES_DEV.test(origin);
  return {
    "Access-Control-Allow-Origin": allowed ? origin : ALLOWED_ORIGINS[0],
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    Vary: "Origin",
  };
}

function json(body, status, origin) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...corsHeaders(origin) },
  });
}

// Accept only a clean user/assistant alternation that starts and ends with the user.
function cleanMessages(input) {
  if (!Array.isArray(input)) return null;
  const msgs = input.slice(-MAX_TURNS).map((m) => ({
    role: m && m.role === "assistant" ? "assistant" : "user",
    content: String((m && m.content) || "").slice(0, MAX_CHARS).trim(),
  })).filter((m) => m.content);
  while (msgs.length && msgs[0].role !== "user") msgs.shift();
  if (!msgs.length || msgs[msgs.length - 1].role !== "user") return null;
  for (let i = 1; i < msgs.length; i++) if (msgs[i].role === msgs[i - 1].role) return null;
  return msgs;
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const allowed = ALLOWED_ORIGINS.includes(origin) || PAGES_DEV.test(origin);

    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: corsHeaders(origin) });
    if (request.method !== "POST") return json({ error: "method_not_allowed" }, 405, origin);
    if (!allowed) return json({ error: "origin_not_allowed" }, 403, origin);
    if (!env.ANTHROPIC_API_KEY) return json({ error: "not_configured" }, 503, origin);

    let body;
    try { body = await request.json(); } catch { return json({ error: "bad_json" }, 400, origin); }
    const messages = cleanMessages(body && body.messages);
    if (!messages) return json({ error: "bad_messages" }, 400, origin);
    const lang = body.lang === "en" ? "English" : "Egyptian Arabic";

    const client = new Anthropic({ apiKey: env.ANTHROPIC_API_KEY });
    try {
      const response = await client.beta.messages.create({
        model: "claude-opus-5-5",
        max_tokens: MAX_TOKENS,
        output_config: { effort: "low" }, // chat route: low effort keeps replies fast and cheap
        betas: ["server-side-fallback-2026-07-01"],
        fallbacks: "default", // if a request is declined, the API retries it on a suitable model
        system: [{ type: "text", text: SYSTEM_PROMPT, cache_control: { type: "ephemeral" } }],
        messages: [
          ...messages,
          { role: "system", content: `The visitor's website language is ${lang}.` },
        ],
      });

      if (response.stop_reason === "refusal") {
        return json({ reply: null, handoff: true }, 200, origin);
      }
      const reply = response.content
        .filter((b) => b.type === "text")
        .map((b) => b.text)
        .join("\n")
        .trim();
      return json({ reply: reply || null, handoff: !reply }, 200, origin);
    } catch (error) {
      if (error instanceof Anthropic.RateLimitError) return json({ error: "busy" }, 429, origin);
      if (error instanceof Anthropic.AuthenticationError) return json({ error: "not_configured" }, 503, origin);
      if (error instanceof Anthropic.BadRequestError) return json({ error: "bad_request" }, 400, origin);
      if (error instanceof Anthropic.APIError) return json({ error: "upstream" }, 502, origin);
      return json({ error: "unavailable" }, 502, origin);
    }
  },
};
