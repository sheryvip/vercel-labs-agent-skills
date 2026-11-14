// Saves a news snapshot to site/news.json (fallback shown until the Worker is live).
// Usage: node scripts/snapshot.mjs
import { writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { collectNews } from "../src/news.js";

const out = fileURLToPath(new URL("../../site/news.json", import.meta.url));
const data = await collectNews(fetch);
writeFileSync(out, JSON.stringify(data));
for (const s of data.sources) console.error(`${s.ok ? "OK  " : "FAIL"} ${s.name}: ${s.count}${s.error ? " (" + s.error + ")" : ""}`);
console.error(`${data.items.length} items -> ${out}`);
