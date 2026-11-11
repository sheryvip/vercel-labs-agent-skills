#!/usr/bin/env python3
"""Make a copy of ./site in ./preview whose index.html works as a claude.ai Artifact
(the Artifact host adds its own <html>/<head>/<body>). Not needed for real hosting."""
import os, re, shutil
here = os.path.dirname(os.path.abspath(__file__))
src, dst = os.path.join(here, "site"), os.path.join(here, "preview")
shutil.rmtree(dst, ignore_errors=True); shutil.copytree(src, dst)
p = os.path.join(dst, "index.html"); s = open(p, encoding="utf-8").read()
s = s.replace("<!doctype html>\n", ""); s = re.sub(r"<html[^>]*>\n", "", s); s = s.replace("</html>\n", "")
s = re.sub(r"  <title>.*?</title>\n", "", s, count=1)
s = s.replace("<head>\n", '<title>Sana Technology</title>\n<script>document.documentElement.lang="ar";document.documentElement.dir="rtl";</script>\n', 1)
s = s.replace("</head>\n", ""); s = re.sub(r"<body[^>]*>\n", "", s); s = s.replace("</body>\n", "")
open(p, "w", encoding="utf-8").write(s)
print("Preview ready in", dst)
