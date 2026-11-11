#!/bin/bash

# Company Website Scaffolder
# Usage: ./scaffold.sh <output-dir> [config.json]
# Returns: JSON with siteDir, files, placeholders

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$SCRIPT_DIR/../template"
OUT_DIR="$1"
CONFIG="$2"

if [ -z "$OUT_DIR" ]; then
    echo "Usage: scaffold.sh <output-dir> [config.json]" >&2
    exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: python3 is required" >&2
    exit 1
fi

if [ -n "$CONFIG" ] && [ ! -f "$CONFIG" ]; then
    echo "Error: config file not found: $CONFIG" >&2
    exit 1
fi

if [ -d "$OUT_DIR" ] && [ -n "$(ls -A "$OUT_DIR" 2>/dev/null)" ]; then
    echo "Error: output-dir is not empty: $OUT_DIR" >&2
    exit 1
fi

TMP_DIR=$(mktemp -d)
cleanup() { rm -rf "$TMP_DIR"; }
trap cleanup EXIT

echo "Copying template..." >&2
cp -R "$TEMPLATE_DIR/." "$TMP_DIR/"

echo "Filling in company details..." >&2
python3 - "$TMP_DIR" "$CONFIG" <<'PY'
import html, json, os, sys

site_dir, config_path = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else ""
cfg = {}
if config_path:
    with open(config_path, encoding="utf-8") as f:
        cfg = json.load(f)

def get(key, fallback):
    v = cfg.get(key)
    return str(v).strip() if v not in (None, "") else fallback

name = get("name", "[ADD Company name]")
lang = get("defaultLang", "ar").lower()
lang = "en" if lang.startswith("en") else "ar"
site_url = get("siteUrl", "https://example.com").rstrip("/")
values = {
    "NAME": name,
    "NAME_AR": get("nameAr", name),
    "TAGLINE": get("tagline", "[ADD Short tagline]"),
    "TAGLINE_AR": get("taglineAr", get("tagline", "[ADD شعار قصير]")),
    "PRIMARY_COLOR": get("primaryColor", "#0f766e"),
    "PHONE": get("phone", "[ADD phone]"),
    "WHATSAPP": "".join(c for c in get("whatsapp", "") if c.isdigit()) or "[ADD whatsapp]",
    "EMAIL": get("email", "[ADD email]"),
    "ADDRESS": get("address", "[ADD address]"),
    "ADDRESS_AR": get("addressAr", get("address", "[ADD العنوان]")),
    "DEFAULT_LANG": lang,
    "DIR": "rtl" if lang == "ar" else "ltr",
    "SITE_URL": site_url,
    "INITIAL": (name.strip("[")[:1] or "C").upper(),
}

count = 0
for dirpath, _, files in os.walk(site_dir):
    for fn in files:
        path = os.path.join(dirpath, fn)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        for k, v in values.items():
            text = text.replace("{{" + k + "}}", html.escape(v, quote=True))
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        count += 1
print(f"Filled {count} files", file=sys.stderr)
PY

mkdir -p "$OUT_DIR"
cp -R "$TMP_DIR/." "$OUT_DIR/"
SITE_DIR="$(cd "$OUT_DIR" && pwd)"

echo "Site created at $SITE_DIR" >&2

python3 - "$SITE_DIR" <<'PY'
import json, os, re, sys
site = sys.argv[1]
found, files = set(), 0
for dirpath, _, names in os.walk(site):
    for fn in names:
        files += 1
        with open(os.path.join(dirpath, fn), encoding="utf-8") as f:
            found.update(re.findall(r"\[ADD [^\]]+\]", f.read()))
print(json.dumps({"siteDir": site, "files": files, "placeholders": sorted(found)}, ensure_ascii=False))
PY
