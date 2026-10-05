# /// script
# requires-python = ">=3.11"
# dependencies = ["markdown-it-py>=3", "pygments>=2.17"]
# ///
"""Build the nossaifd site from README.md, GUIDE.md and the pages in docs/.

    uv run docs/build.py            writes docs/_site
    uv run docs/build.py --serve    and serves it at http://127.0.0.1:8000 to look at

GUIDE.md and README.md stay at the top of the repository, because people and models read them there. The
build reads them from there, so each text has one source. Links between the files are written as file names,
so they also work on GitHub, and the build turns them into links between pages.
"""

import argparse
import functools
import html
import http.server
import re
import shutil
from pathlib import Path

from markdown_it import MarkdownIt
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

DOCS = Path(__file__).resolve().parent
ROOT = DOCS.parent
OUT = DOCS / "_site"
REPO = "https://github.com/rahuldave/nossaifd"

# The pages, in the order of the sidebar: the source file, the page it becomes, the title in the sidebar.
PAGES = [
    (ROOT / "README.md", "index.html", "Overview"),
    (ROOT / "GUIDE.md", "guide.html", "The guide"),
    (DOCS / "checker.md", "checker.html", "The checker"),
]
# Links in the sources that point to other files: a page of the site, or the file on GitHub.
LINKS = {"README.md": "index.html", "GUIDE.md": "guide.html", "../GUIDE.md": "guide.html", "../README.md": "index.html",
         "checker.md": "checker.html", "docs/checker.md": "checker.html", "check.py": f"{REPO}/blob/main/check.py",
         "../check.py": f"{REPO}/blob/main/check.py", "LICENSE": f"{REPO}/blob/main/LICENSE"}


def code_block(
    code: str,  # The text inside a fence
    language: str,  # The fence's language, or empty
    attrs: str,  # Unused fence attributes
) -> str:  # Highlighted HTML, or empty to let markdown-it escape it plainly
    "Highlight a fenced block with Pygments when it names a language that Pygments knows."
    try:
        lexer = get_lexer_by_name(language) if language else None
    except ClassNotFound:
        lexer = None
    return highlight(code, lexer, HtmlFormatter(nowrap=True)) if lexer else ""


def slug(
    text: str,  # The text of a heading
) -> str:  # An id for it
    "Make an id from a heading, as GitHub does: lower case, words joined by hyphens."
    text = re.sub(r"<[^>]+>", "", html.unescape(text)).lower()
    return re.sub(r"[^\w\- ]", "", text).strip().replace(" ", "-")


def render(
    text: str,  # The Markdown of a page
) -> tuple[str, str, list[tuple[str, str]]]:  # Its title, its HTML, and its sections as (id, title)
    "Turn one page into HTML: tables, highlighted code, ids on headings, links between pages."
    md = MarkdownIt("commonmark", {"html": True, "highlight": code_block}).enable("table")
    body = md.render(text)

    def link(match: re.Match) -> str:  # The link, pointed at a page of the site where there is one
        target, fragment = match.group(1), match.group(2) or ""
        return f'href="{LINKS.get(target, target)}{fragment}"'

    body = re.sub(r'href="([\w./\-]+?)(#[^"]*)?"', link, body)
    body = re.sub(r"<(h[23])>(.*?)</\1>", lambda m: f'<{m.group(1)} id="{slug(m.group(2))}"><a class="anchor" href="#{slug(m.group(2))}">{m.group(2)}</a></{m.group(1)}>', body)
    body = body.replace("<pre><code", '<pre class="hl"><code')
    sections = [(m.group(1), re.sub(r"<[^>]+>", "", m.group(2))) for m in re.finditer(r'<h2 id="([^"]+)"><a class="anchor"[^>]*>(.*?)</a></h2>', body)]
    found = re.search(r"<h1>(.*?)</h1>", body)
    return (re.sub(r"<[^>]+>", "", found.group(1)) if found else "nossaifd"), body, sections


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="icon" href="data:,">
<link rel="stylesheet" href="site.css">
</head>
<body>
<header class="top"><a class="brand" href="index.html">nossaifd</a><span class="tag">not so shitty AI first drafts</span>
<a class="gh" href="{repo}">GitHub</a></header>
<div class="wrap">
<nav class="side" aria-label="Pages"><ul>{nav}</ul></nav>
<main>{body}<footer class="pager">{pager}</footer></main>
</div>
</body>
</html>
"""


def build() -> int:  # How many pages were written
    "Write every page and the stylesheet to docs/_site."
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    css = (DOCS / "site.css").read_text(encoding="utf-8")
    light = HtmlFormatter(style="friendly").get_style_defs(".hl")
    dark = "@media (prefers-color-scheme: dark) {\n" + HtmlFormatter(style="github-dark").get_style_defs(".hl") + "\n}"
    (OUT / "site.css").write_text(css + "\n/* code, from Pygments */\n" + light + "\n" + dark + "\n", encoding="utf-8")
    for index, (source, out, label) in enumerate(PAGES):
        title, body, sections = render(source.read_text(encoding="utf-8"))
        nav = ""
        for _, other, other_label in PAGES:
            here = other == out
            nav += f'<li><a href="{other}"{" aria-current=page" if here else ""}>{html.escape(other_label)}</a>'
            if here and len(sections) > 2:
                # A long page lists its sections under its name, so the reader can jump to one.
                nav += "<ul>" + "".join(f'<li><a href="#{id_}">{html.escape(name)}</a></li>' for id_, name in sections) + "</ul>"
            nav += "</li>"
        before = PAGES[index - 1] if index > 0 else None
        after = PAGES[index + 1] if index + 1 < len(PAGES) else None
        pager = (f'<a class="prev" href="{before[1]}">&larr; {html.escape(before[2])}</a>' if before else "<span></span>") + \
                (f'<a class="next" href="{after[1]}">{html.escape(after[2])} &rarr;</a>' if after else "<span></span>")
        page_title = "nossaifd" if out == "index.html" else f"{title} | nossaifd"
        (OUT / out).write_text(TEMPLATE.format(title=html.escape(page_title), nav=nav, body=body, pager=pager, repo=REPO), encoding="utf-8")
    return len(PAGES)


def main() -> None:
    "Build the site, and serve it if asked."
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--serve", action="store_true", help="serve the built site at http://127.0.0.1:8000")
    args = parser.parse_args()
    print(f"build: wrote {build()} pages to {OUT}")
    if args.serve:
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
        print("build: serving at http://127.0.0.1:8000 (Ctrl+C to stop)")
        http.server.ThreadingHTTPServer(("127.0.0.1", 8000), handler).serve_forever()


if __name__ == "__main__":
    main()
