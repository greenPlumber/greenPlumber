#!/usr/bin/env python3
"""Renders README.md into a local HTML page that mimics GitHub's profile view.

    python3 tools/preview.py [--open]

Loads the SVGs through <img> tags exactly as GitHub does, so the SMIL
animations actually run, and uses GitHub's own font stacks and colours so the
box-drawing alignment can be checked in the font it will really be read in.
The light/dark toggle exists to confirm the self-contained dark art holds up
in both GitHub themes.
"""

import html
import os
import re
import sys
import webbrowser

CSS = """
:root { color-scheme: dark; }
body {
  margin: 0; background: #0d1117; color: #e6edf3;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans",
               Helvetica, Arial, sans-serif;
  font-size: 16px; line-height: 1.5;
}
body.light { background: #ffffff; color: #1f2328; }
.page { max-width: 1012px; margin: 0 auto; padding: 24px 32px 64px; }
.frame {
  border: 1px solid #30363d; border-radius: 6px; padding: 32px; margin-top: 16px;
}
body.light .frame { border-color: #d1d9e0; }
pre {
  background: #161b22; border: 1px solid #30363d; border-radius: 6px;
  padding: 16px; overflow-x: auto; line-height: 1.45; font-size: 12px;
}
body.light pre { background: #f6f8fa; border-color: #d1d9e0; }
pre, code {
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas,
               "Liberation Mono", monospace;
}
blockquote {
  margin: 16px 0; padding: 0 1em; border-left: .25em solid #30363d; color: #8d96a0;
}
body.light blockquote { border-left-color: #d1d9e0; color: #59636e; }
img { max-width: 100%; }
sub { color: #8d96a0; font-size: 12px; }
.bar {
  display: flex; gap: 12px; align-items: center; font-size: 13px; color: #8d96a0;
  border-bottom: 1px solid #30363d; padding-bottom: 12px;
}
button {
  font: inherit; padding: 4px 12px; border-radius: 6px; cursor: pointer;
  border: 1px solid #30363d; background: #21262d; color: #e6edf3;
}
body.light button { background: #f6f8fa; color: #1f2328; border-color: #d1d9e0; }
"""

JS = """
const b = document.body, t = document.getElementById('t');
t.onclick = () => {
  b.classList.toggle('light');
  const dark = !b.classList.contains('light');
  document.documentElement.style.colorScheme = dark ? 'dark' : 'light';
  t.textContent = dark ? 'Switch to light theme' : 'Switch to dark theme';
};
"""


def render(md, asset_prefix):
    """Handles exactly the constructs the generated README uses: raw HTML
    blocks, fenced code, blockquotes and **bold**."""
    out, i, lines = [], 0, md.split("\n")
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            body, i = [], i + 1
            while i < len(lines) and not lines[i].startswith("```"):
                body.append(lines[i])
                i += 1
            out.append("<pre><code>" + html.escape("\n".join(body)) + "</code></pre>")
        elif line.startswith(">"):
            body = []
            while i < len(lines) and lines[i].startswith(">"):
                body.append(lines[i].lstrip(">").strip())
                i += 1
            text = "<br>".join(body).replace("<br><br>", "</p><p>")
            out.append("<blockquote><p>" + text + "</p></blockquote>")
            continue
        else:
            out.append(line)
        i += 1

    doc = "\n".join(out)
    doc = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", doc)
    # Relative wherever possible: file:// sub-resources are blocked when the
    # page is served over http, which is what VS Code's Live Preview does.
    if asset_prefix:
        doc = doc.replace('src="assets/', f'src="{asset_prefix}assets/')
    return doc


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(here)
    md = open(os.path.join(repo, "README.md"), encoding="utf-8").read()

    out = os.environ.get("PREVIEW_OUT") or os.path.join(repo, "preview.html")
    rel = os.path.relpath(repo, os.path.dirname(os.path.abspath(out)))
    prefix = "" if rel == "." else rel.replace(os.sep, "/") + "/"

    page = (
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<title>greenPlumber - README preview</title>"
        f"<style>{CSS}</style></head><body><div class='page'>"
        "<div class='bar'><button id='t'>Switch to light theme</button>"
        "<span>local preview &middot; animations run here exactly as on GitHub</span></div>"
        f"<div class='frame'>{render(md, prefix)}</div>"
        f"</div><script>{JS}</script></body></html>"
    )

    with open(out, "w", encoding="utf-8") as fh:
        fh.write(page)
    print(f"wrote {out}")
    if "--open" in sys.argv:
        webbrowser.open("file://" + out)


if __name__ == "__main__":
    main()
