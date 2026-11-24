#!/usr/bin/env python3
"""Regenerate security headers (CSP with hashes) in vercel.json and firebase.json from index.html.
Run after every change to index.html:   python3 tools/gen-csp.py
CI check (fails on mismatch):           python3 tools/gen-csp.py --check
No frame-ancestors on purpose: the apps are embedded by the CRM."""
import base64, hashlib, json, re, sys, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
html = (root / "index.html").read_text(encoding="utf-8")

def h(txt):
    return "'sha256-" + base64.b64encode(hashlib.sha256(txt.encode("utf-8")).digest()).decode() + "'"

scripts = [m.group(2) for m in re.finditer(r"<script(\s[^>]*)?>(.*?)</script>", html, re.S) if not re.search(r"\ssrc=", m.group(1) or "")]
styles = [m.group(1) for m in re.finditer(r"<style[^>]*>(.*?)</style>", html, re.S)]
if not scripts or not styles:
    sys.exit("expected inline script and style blocks")

csp = "; ".join([
    "default-src 'none'",
    "script-src " + " ".join(h(x) for x in scripts),
    "style-src " + " ".join(h(x) for x in styles) + " https://fonts.googleapis.com",
    "style-src-attr 'unsafe-inline'",
    "font-src https://fonts.gstatic.com",
    "img-src 'self' data:",
    "media-src 'none'",
    "connect-src 'none'",
    "form-action 'none'",
    "base-uri 'none'",
    "object-src 'none'",
])
common = [
    {"key": "Content-Security-Policy", "value": csp},
    {"key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains"},
    {"key": "X-Content-Type-Options", "value": "nosniff"},
    {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
    {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=(), payment=(), usb=()"},
]
vercel = {"cleanUrls": True, "trailingSlash": False,
          "headers": [{"source": "/(.*)", "headers": common + [{"key": "Cache-Control", "value": "public, max-age=0, must-revalidate"}]}]}
fb_path = root / "firebase.json"
fb = json.loads(fb_path.read_text(encoding="utf-8"))
fb["hosting"]["headers"] = [{"source": "**", "headers": common}, {"source": "**/*.html", "headers": [{"key": "Cache-Control", "value": "no-cache"}]}]

new = {"vercel.json": vercel, "firebase.json": fb}
bad = []
for name, data in new.items():
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    p = root / name
    if "--check" in sys.argv:
        if not p.exists() or p.read_text(encoding="utf-8") != text:
            bad.append(name)
    else:
        p.write_text(text, encoding="utf-8")
if bad:
    sys.exit("CSP hashes are out of date in: " + ", ".join(bad) + ". Run: python3 tools/gen-csp.py")
print("ok", "(checked)" if "--check" in sys.argv else "(written)")
