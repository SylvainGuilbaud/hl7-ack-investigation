#!/usr/bin/env python3
"""docs/article.md -> docs/article.html, with every relative link rewritten to a GitHub URL.

    python3 tools/article_to_html.py [--repo https://github.com/OWNER/REPO] [--branch main]

 * images  (![..](img/x.png))   -> <repo>/raw/<branch>/docs/img/x.png
 * files   ([..](../test/x.py)) -> <repo>/blob/<branch>/test/x.py
 * folders ([..](traces/))      -> <repo>/tree/<branch>/docs/traces
External links and #anchors are left alone. Needs pandoc.
"""
import argparse, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "article.md"

CSS = """<style>
body{max-width:980px;margin:2rem auto;padding:0 1rem;font:16px/1.55 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;color:#1f2328}
h1,h2,h3{line-height:1.25;margin-top:1.8em}h1,h2{border-bottom:1px solid #d1d9e0;padding-bottom:.3em}
a{color:#0969da;text-decoration:none}a:hover{text-decoration:underline}
code{background:#eff1f3;padding:.15em .35em;border-radius:5px;font-size:88%}
pre{background:#f6f8fa;padding:1em;border-radius:6px;overflow:auto;line-height:1.4}pre code{background:none;padding:0;font-size:85%}
table{border-collapse:collapse;display:block;overflow:auto;margin:1em 0}th,td{border:1px solid #d1d9e0;padding:6px 13px}th{background:#f6f8fa}tr:nth-child(even) td{background:#fafbfc}
blockquote{margin:1em 0;padding:0 1em;color:#59636e;border-left:.25em solid #d1d9e0}
img{max-width:100%}
</style>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="https://github.com/SylvainGuilbaud/hl7-ack-investigation")
    ap.add_argument("--branch", default="main")
    ap.add_argument("--out", default=str(ROOT / "docs" / "article.html"))
    a = ap.parse_args()
    repo = a.repo.rstrip("/")
    stats = {"image": 0, "file": 0, "folder": 0}

    def rewrite(m):
        bang, text, target = m.group(1), m.group(2), m.group(3)
        if re.match(r"^(https?:|mailto:|#)", target):
            return m.group(0)
        path, _, frag = target.partition("#")
        full = (SRC.parent / path).resolve()
        try:
            rel = full.relative_to(ROOT).as_posix()
        except ValueError:
            sys.exit(f"link leaves the repository: {target}")
        if not full.exists():
            sys.exit(f"broken link: {target}")
        if bang:
            kind, url = "image", f"{repo}/raw/{a.branch}/{rel}"
        elif full.is_dir():
            kind, url = "folder", f"{repo}/tree/{a.branch}/{rel}"
        else:
            kind, url = "file", f"{repo}/blob/{a.branch}/{rel}"
        stats[kind] += 1
        return f"{bang}[{text}]({url}{'#' + frag if frag else ''})"

    md = SRC.read_text()
    md = re.sub(r"(!?)\[((?:[^\[\]]|\[[^\]]*\])*)\]\(([^)\s]+)\)", rewrite, md)
    title = md.lstrip().splitlines()[0].lstrip("# ").strip()
    hdr = ROOT / "docs" / ".article_header.html"
    hdr.write_text(CSS)
    try:
        subprocess.run(["pandoc", "-f", "gfm", "-t", "html5", "--standalone", "--metadata", f"title={title}",
                        "--metadata", "lang=en", "-H", str(hdr), "-o", a.out],
                       input=md, text=True, check=True)
    finally:
        hdr.unlink(missing_ok=True)
    # pandoc repeats the title as <h1 class="title"> when --metadata title is set; the article already has its own H1
    html = Path(a.out).read_text()
    html = re.sub(r'<header id="title-block-header">.*?</header>\s*', "", html, flags=re.S)
    Path(a.out).write_text(html)
    print(f"wrote {a.out}: {stats['file']} file links, {stats['folder']} folder links, {stats['image']} images -> {repo} ({a.branch})")


if __name__ == "__main__":
    main()
