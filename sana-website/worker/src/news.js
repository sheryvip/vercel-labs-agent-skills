// Tech & AI news aggregator: reads the public RSS/Atom feeds of well-known outlets,
// keeps only the headline, a short summary, the date and a link back to the source.

export const FEEDS = [
  // English
  { id: "mittr", name: "MIT Technology Review", lang: "en", topic: "ai", site: "https://www.technologyreview.com", url: "https://www.technologyreview.com/topic/artificial-intelligence/feed" },
  { id: "verge", name: "The Verge", lang: "en", topic: "ai", site: "https://www.theverge.com", url: "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml" },
  { id: "techcrunch", name: "TechCrunch", lang: "en", topic: "ai", site: "https://techcrunch.com", url: "https://techcrunch.com/category/artificial-intelligence/feed/" },
  { id: "ars", name: "Ars Technica", lang: "en", topic: "ai", site: "https://arstechnica.com", url: "https://arstechnica.com/ai/feed/" },
  { id: "wired", name: "WIRED", lang: "en", topic: "ai", site: "https://www.wired.com", url: "https://www.wired.com/feed/tag/ai/latest/rss" },
  { id: "ieee", name: "IEEE Spectrum", lang: "en", topic: "tech", site: "https://spectrum.ieee.org", url: "https://feeds.feedburner.com/IeeeSpectrum" },
  { id: "bbc", name: "BBC News", lang: "en", topic: "tech", site: "https://www.bbc.com/news/technology", url: "https://feeds.bbci.co.uk/news/technology/rss.xml" },
  // Arabic
  { id: "bbcar", name: "BBC عربي", lang: "ar", topic: "tech", site: "https://www.bbc.com/arabic/science-and-tech", url: "https://feeds.bbci.co.uk/arabic/science-and-tech/rss.xml" },
  { id: "aitnews", name: "البوابة العربية للأخبار التقنية", lang: "ar", topic: "tech", site: "https://aitnews.com", url: "https://aitnews.com/feed/" },
  { id: "techwd", name: "عالم التقنية", lang: "ar", topic: "tech", site: "https://www.tech-wd.com", url: "https://feeds.feedburner.com/tech-wd" },
];

const PER_FEED = 12;
const MAX_ITEMS = 90;
const MAX_AGE_DAYS = 30;
const FETCH_TIMEOUT_MS = 8000;
const AI_RE = /\b(ai|a\.i\.|artificial intelligence|machine learning|deep learning|llms?|chatgpt|openai|anthropic|claude|gemini|deepmind|copilot|neural|robots?|robotics|generative|chatbots?|agents?)\b|ذكاء اصطناعي|الذكاء الاصطناعي|الذكاء الإصطناعي|تعلم الآلة|روبوت|نموذج لغوي|النماذج اللغوية|شات ?جي ?بي ?تي/i;

const ENTITIES = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: " ", hellip: "…", mdash: "—", ndash: "–", rsquo: "’", lsquo: "‘", rdquo: "”", ldquo: "“" };

function decode(s) {
  return s.replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);/gi, (m, e) => {
    if (e[0] === "#") {
      const n = e[1] === "x" || e[1] === "X" ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10);
      return Number.isFinite(n) && n > 0 && n < 0x110000 ? String.fromCodePoint(n) : "";
    }
    return ENTITIES[e.toLowerCase()] ?? m;
  });
}
function unCdata(s) { return s.replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, "$1"); }
function text(s) {
  // Feeds often double-encode HTML: decode once, strip tags, decode again.
  return decode(decode(unCdata(s || "")).replace(/<[^>]*>/g, " ")).replace(/\s+/g, " ").trim();
}
function esc(name) { return name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }
function tag(block, name) {
  const m = block.match(new RegExp(`<${esc(name)}(?:\\s[^>]*)?>([\\s\\S]*?)</${esc(name)}>`, "i"));
  return m ? m[1] : "";
}
function attr(block, tagName, attrName, extra) {
  const re = new RegExp(`<${esc(tagName)}\\b([^>]*)>`, "gi");
  let m;
  while ((m = re.exec(block))) {
    if (extra && !extra.test(m[1])) continue;
    const a = m[1].match(new RegExp(`\\b${esc(attrName)}\\s*=\\s*["']([^"']+)["']`, "i"));
    if (a) return decode(a[1]);
  }
  return "";
}
function httpUrl(u) {
  try { const x = new URL(u.trim()); return x.protocol === "https:" || x.protocol === "http:" ? x.href : ""; } catch { return ""; }
}
function clip(s, n) {
  if (s.length <= n) return s;
  const cut = s.slice(0, n);
  const sp = cut.lastIndexOf(" ");
  return (sp > n * 0.6 ? cut.slice(0, sp) : cut).replace(/[\s,.;:،-]+$/, "") + "…";
}

export function parseFeed(xml, feed) {
  const blocks = xml.match(/<item[\s>][\s\S]*?<\/item>/gi) || xml.match(/<entry[\s>][\s\S]*?<\/entry>/gi) || [];
  const out = [];
  for (const b of blocks.slice(0, PER_FEED * 2)) {
    const title = clip(text(tag(b, "title")), 200);
    let link = httpUrl(text(tag(b, "link")));
    if (!link) link = httpUrl(attr(b, "link", "href", /rel\s*=\s*["']alternate["']/i) || attr(b, "link", "href"));
    if (!title || !link) continue;
    const rawDate = text(tag(b, "pubDate") || tag(b, "published") || tag(b, "updated") || tag(b, "dc:date"));
    const t = Date.parse(rawDate);
    const body = tag(b, "description") || tag(b, "summary") || tag(b, "content") || tag(b, "content:encoded");
    const summary = clip(text(body), 230);
    let image = attr(b, "media:thumbnail", "url") || attr(b, "media:content", "url", /medium\s*=\s*["']image["']|type\s*=\s*["']image/i)
      || attr(b, "media:content", "url") || attr(b, "enclosure", "url", /type\s*=\s*["']image/i);
    if (!image) {
      const html = decode(unCdata(tag(b, "content:encoded") || body));
      const im = html.match(/<img\b[^>]*\bsrc\s*=\s*["']([^"']+)["']/i);
      if (im) image = im[1];
    }
    image = httpUrl(image).replace(/^http:/, "https:");
    out.push({
      title, link, summary: summary === title ? "" : summary,
      date: Number.isFinite(t) ? new Date(t).toISOString() : null,
      image: image || null,
      source: feed.id, lang: feed.lang,
      ai: feed.topic === "ai" || AI_RE.test(title + " " + summary),
    });
    if (out.length >= PER_FEED) break;
  }
  return out;
}

async function fetchFeed(feed, fetchImpl) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), FETCH_TIMEOUT_MS);
  try {
    const r = await fetchImpl(feed.url, {
      signal: ctrl.signal,
      headers: { "User-Agent": "SanaNewsBot/1.0 (+https://sanatechgroup.online)", Accept: "application/rss+xml, application/atom+xml, application/xml, text/xml;q=0.9, */*;q=0.5" },
    });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const xml = await r.text();
    return parseFeed(xml.slice(0, 3_000_000), feed);
  } finally {
    clearTimeout(timer);
  }
}

export async function collectNews(fetchImpl = fetch, now = Date.now()) {
  const results = await Promise.allSettled(FEEDS.map((f) => fetchFeed(f, fetchImpl)));
  const seen = new Set();
  const items = [];
  const sources = FEEDS.map((f, i) => {
    const r = results[i];
    const list = r.status === "fulfilled" ? r.value : [];
    for (const it of list) {
      if (it.date && now - Date.parse(it.date) > MAX_AGE_DAYS * 864e5) continue;
      const key = it.title.toLowerCase().replace(/[^\p{L}\p{N}]+/gu, " ").trim();
      if (seen.has(key) || seen.has(it.link)) continue;
      seen.add(key); seen.add(it.link);
      items.push(it);
    }
    return { id: f.id, name: f.name, lang: f.lang, site: f.site, ok: r.status === "fulfilled" && list.length > 0, count: list.length,
      error: r.status === "rejected" ? String(r.reason && r.reason.message || r.reason).slice(0, 120) : undefined };
  });
  items.sort((a, b) => (b.date ? Date.parse(b.date) : 0) - (a.date ? Date.parse(a.date) : 0));
  return { updated: new Date(now).toISOString(), sources, items: items.slice(0, MAX_ITEMS) };
}
