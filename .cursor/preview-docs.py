#!/usr/bin/env python3
"""Render this repository's Markdown documentation into a browsable static site.

`enumium` is a documentation / architecture repository, so the "application" is
its rendered documentation. This script converts every Markdown file in the repo
into styled, GitHub-flavoured HTML for local preview.

Usage:
    python3 .cursor/preview-docs.py [REPO_ROOT] [OUTPUT_DIR]

Defaults: REPO_ROOT is the repo root (parent of .cursor), OUTPUT_DIR is
.cursor/_site. Run the module afterwards with `python3 -m http.server` from the
output directory to preview the docs in a browser.
"""
import glob
import os
import shutil
import sys

import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(HERE)
OUT = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.join(HERE, "_site")

CSS = """
:root { color-scheme: light dark; }
body { max-width: 820px; margin: 0 auto; padding: 2.5rem 1.5rem 6rem;
  font: 16px/1.65 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  color: #1f2328; background: #ffffff; }
@media (prefers-color-scheme: dark) { body { color:#e6edf3; background:#0d1117; }
  a { color:#4493f8; } code, pre { background:#161b22 !important; }
  .nav { background:#161b22; } h1, h2 { border-color:#30363d; } hr { border-color:#30363d; } }
h1, h2, h3 { line-height: 1.25; margin-top: 1.8rem; }
h1, h2 { border-bottom: 1px solid #d0d7de; padding-bottom: .3em; }
code { background:#f6f8fa; padding:.2em .4em; border-radius:6px; font-size:85%; }
pre { background:#f6f8fa; padding:1rem; border-radius:8px; overflow:auto; }
pre code { background:transparent; padding:0; }
a { color:#0969da; text-decoration:none; }
a:hover { text-decoration:underline; }
hr { border:0; border-top:1px solid #d0d7de; margin:2rem 0; }
.nav { margin-bottom:2rem; padding:.75rem 1rem; background:#f6f8fa; border-radius:8px; }
"""


def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)

    md_files = sorted(
        f for f in glob.glob(os.path.join(REPO, "**", "*.md"), recursive=True)
        if os.sep + ".git" + os.sep not in f and os.sep + "_site" + os.sep not in f
    )

    links = []
    for path in md_files:
        rel = os.path.relpath(path, REPO)
        out_name = rel.replace(os.sep, "__").replace(".md", ".html")
        links.append((rel, out_name))

    nav = "<div class='nav'><strong>Enumium docs preview</strong><br>" + " &middot; ".join(
        f"<a href='{out_name}'>{rel}</a>" for rel, out_name in links
    ) + "</div>"

    md = markdown.Markdown(extensions=["extra", "toc", "sane_lists", "pymdownx.superfences"])
    for path, (rel, out_name) in zip(md_files, links):
        with open(path, encoding="utf-8") as fh:
            md.reset()
            body = md.convert(fh.read())
        page = (
            "<!doctype html><html><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width, initial-scale=1'>"
            f"<title>{rel} — Enumium</title><style>{CSS}</style></head>"
            f"<body>{nav}{body}</body></html>"
        )
        with open(os.path.join(OUT, out_name), "w", encoding="utf-8") as fh:
            fh.write(page)

    if links:
        shutil.copyfile(os.path.join(OUT, links[0][1]), os.path.join(OUT, "index.html"))

    print(f"Rendered {len(md_files)} markdown file(s) from {REPO} to {OUT}")


if __name__ == "__main__":
    build()
