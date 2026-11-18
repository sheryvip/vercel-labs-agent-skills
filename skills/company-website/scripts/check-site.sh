#!/bin/bash

# Company Website Checker
# Usage: ./check-site.sh [site-dir]
# Checks SEO, accessibility basics, broken internal links and leftover placeholders.
# Returns: JSON summary {errors, warnings, files}; exits 1 when errors are found.

set -e

SITE_DIR="${1:-.}"

if [ ! -d "$SITE_DIR" ]; then
    echo "Error: directory not found: $SITE_DIR" >&2
    exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: python3 is required" >&2
    exit 1
fi

echo "Checking $SITE_DIR ..." >&2

python3 - "$SITE_DIR" <<'PY'
import json, os, re, sys
from html.parser import HTMLParser

site = os.path.abspath(sys.argv[1])
errors = warnings = 0

def report(level, rel, msg, line=None):
    global errors, warnings
    if level == "ERROR":
        errors += 1
    else:
        warnings += 1
    where = f" (line {line})" if line else ""
    print(f"{level:<5} {rel}: {msg}{where}", file=sys.stderr)

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.html_attrs, self.ids, self.links = {}, set(), []
        self.title, self.in_title = "", False
        self.meta, self.imgs, self.h1 = {}, [], 0
        self.labels_for, self.inputs, self.label_depth = set(), [], 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        line = self.getpos()[0]
        if "id" in a: self.ids.add(a["id"])
        if tag == "html": self.html_attrs = a
        elif tag == "title": self.in_title = True
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key: self.meta[key] = a.get("content", "")
        elif tag == "img": self.imgs.append((a, line))
        elif tag == "h1": self.h1 += 1
        elif tag == "label":
            self.label_depth += 1
            if a.get("for"): self.labels_for.add(a["for"])
        elif tag in ("input", "textarea", "select") and a.get("type") not in ("hidden", "submit", "button"):
            if self.label_depth == 0:  # a field nested inside <label> is already labelled
                self.inputs.append((a, line))
        for attr in ("href", "src"):
            if a.get(attr): self.links.append((a[attr], line))
    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
        elif tag == "label" and self.label_depth: self.label_depth -= 1
    def handle_data(self, data):
        if self.in_title: self.title += data

html_files, all_files = [], 0
for dirpath, dirs, names in os.walk(site):
    dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", ".vercel")]
    for fn in names:
        all_files += 1
        if fn.endswith(".html"):
            html_files.append(os.path.join(dirpath, fn))

if not os.path.exists(os.path.join(site, "index.html")):
    report("ERROR", ".", "index.html is missing")

for path in html_files:
    rel = os.path.relpath(path, site)
    with open(path, encoding="utf-8") as f:
        src = f.read()
    p = Page(); p.feed(src)

    if not p.html_attrs.get("lang"): report("ERROR", rel, "<html> missing lang attribute")
    if p.html_attrs.get("lang", "").startswith("ar") and p.html_attrs.get("dir") != "rtl":
        report("WARN", rel, 'Arabic page should have dir="rtl"')
    t = p.title.strip()
    if not t: report("ERROR", rel, "missing <title>")
    elif len(t) > 65: report("WARN", rel, f"title is long ({len(t)} chars, aim for <= 60)")
    if "viewport" not in p.meta: report("ERROR", rel, "missing viewport meta tag")
    if rel != "404.html":
        d = p.meta.get("description", "")
        if not d: report("ERROR", rel, "missing meta description")
        elif len(d) > 170: report("WARN", rel, f"meta description is long ({len(d)} chars)")
        if p.h1 != 1: report("WARN", rel, f"page should have exactly one <h1> (found {p.h1})")

    for a, line in p.imgs:
        if "alt" not in a: report("ERROR", rel, "<img> missing alt text", line)
        if not (a.get("width") and a.get("height")): report("WARN", rel, "<img> missing width/height (layout shift)", line)

    for a, line in p.inputs:
        if a.get("id") not in p.labels_for and not a.get("aria-label"):
            report("ERROR", rel, f"form field '{a.get('name', '?')}' has no <label>", line)

    for target, line in p.links:
        if target.startswith(("http:", "https:", "mailto:", "tel:", "data:", "//", "javascript:")):
            continue
        if target.startswith("#"):
            if len(target) > 1 and target[1:] not in p.ids:
                report("ERROR", rel, f"anchor link to missing id: {target}", line)
            continue
        clean = target.split("#")[0].split("?")[0]
        if not clean: continue
        base = site if clean.startswith("/") else os.path.dirname(path)
        fp = os.path.normpath(os.path.join(base, clean.lstrip("/")))
        if not (os.path.exists(fp) or os.path.exists(fp + ".html") or os.path.exists(os.path.join(fp, "index.html"))):
            report("ERROR", rel, f"broken link: {target}", line)

for dirpath, dirs, names in os.walk(site):
    dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", ".vercel")]
    for fn in names:
        if not fn.endswith((".html", ".xml", ".txt", ".css", ".js", ".svg")): continue
        path = os.path.join(dirpath, fn); rel = os.path.relpath(path, site)
        with open(path, encoding="utf-8", errors="ignore") as f:
            src = f.read()
        if re.search(r"\{\{[A-Z_]+\}\}", src): report("ERROR", rel, "unfilled template variable {{...}}")
        for ph in sorted(set(re.findall(r"\[ADD [^\]]+\]", src))):
            report("WARN", rel, f"placeholder text remains: {ph}")
        if "example.com" in src: report("WARN", rel, "uses example.com: set the real siteUrl/email")

print(json.dumps({"errors": errors, "warnings": warnings, "files": len(html_files)}))
sys.exit(1 if errors else 0)
PY
