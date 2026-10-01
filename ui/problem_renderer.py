"""
Render problem text as HTML with math typeset by a bundled copy of MathJax.

Problem files hold the problem's HTML exactly as projecteuler.net serves it
(see tools/import_problems.py), including the same TeX notation ($...$ for
inline math, $$...$$ for display math). Older plain-text problem files are
still supported. MathJax is loaded from the local 'mathjax' folder and images
from 'problems/resources', so no internet connection is needed.
"""

import html
import os
import re

from PyQt6.QtCore import QUrl

# Project root (in a PyInstaller build this is the _internal folder,
# which is where the 'mathjax' and 'problems' data folders are copied to).
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MATHJAX_DIR = os.path.join(BASE_DIR, "mathjax")
PROBLEMS_DIR = os.path.join(BASE_DIR, "problems")

# HTML tags that occasionally appear in plain-text problem files and should be kept
ALLOWED_TAGS = re.compile(r"&lt;(/?)(sup|sub|b|i|em|strong)&gt;", re.IGNORECASE)

# Problem files imported from the website contain block-level HTML
HTML_CONTENT = re.compile(r"<(p|div|table|ul|ol|img|br|blockquote|pre)\b", re.IGNORECASE)

PAGE_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script>
// Same settings as projecteuler.net uses
window.MathJax = {
    startup: {
        pageReady: () => {
            for (const script of document.querySelectorAll('script[type^="math/tex"]')) {
                const math = document.createElement('span');
                math.innerText = script.text;
                script.parentNode.replaceChild(math, script);
            }
            return MathJax.startup.defaultPageReady();
        }
    },
    tex: {
        inlineMath: [['$', '$']],
        displayMath: [['$$', '$$']],
        processEscapes: true
    },
    chtml: { scale: 1.05 },
    options: { enableMenu: false, ignoreHtmlClass: 'text-block' }
};
</script>
<script src="%(mathjax_url)s"></script>
<style>
    html, body {
        margin: 0;
        background-color: %(bg)s;
        color: %(fg)s;
    }
    body {
        padding: %(padding)dpx;
        font-family: %(font_family)s, sans-serif;
        font-size: %(font_size)dpt;
        line-height: 1.5;
        overflow-wrap: break-word;
    }
    .plain {
        white-space: pre-wrap;
    }
    .problem-title {
        font-weight: bold;
        font-size: 1.15em;
    }
    mjx-container[display="true"] {
        margin: 0.6em 0 !important;
    }

    /* Problem HTML from the website (based on projecteuler.net's dark theme) */
    .content p { margin: 0.8em 0; }
    .content a { color: #ad7f63; }
    .content a:hover { color: #fff; }
    .content .center { text-align: center; }
    .content .monospace, .content code, .content pre { font-family: Inconsolata, "Courier New", monospace; }
    .content .monospace { font-size: 1.1em; }
    .content .break_word { word-wrap: break-word; }
    .content .red { color: #f33; }
    .content .smaller { font-size: 90%%; }
    .content .smallest { font-size: 80%%; }
    .content .margin_left { margin-left: 100px; }
    .content table { border-collapse: collapse; margin: 0.6em 0; }
    .content table.center, .content table[align="center"] { margin-left: auto; margin-right: auto; }
    .content .center table { margin-left: auto; margin-right: auto; }
    .content td, .content th { padding: 2px 8px; }
    .content table[border="1"] td, .content table[border="1"] th,
    .content table.grid td, .content table.grid th { border: 1px solid #555; }
    .content img {
        max-width: 95%%;
        object-fit: contain;
        background-color: #fff;
        padding: 10px;
        border: 2px solid #555;
    }
    .content blockquote { margin: 0.8em 2em; }
    .content .tooltip { position: relative; display: inline-block; cursor: help; }
    .content dfn.tooltip, .content strong.tooltip { border-bottom: 1px solid #fff; }
    .content [class*="tooltiptext"] {
        visibility: hidden;
        position: absolute;
        z-index: 1;
        top: 100%%;
        left: 50%%;
        margin: 10px 0 0 -100px;
        width: 200px;
        padding: 5px 10px;
        background-color: #222;
        color: #eee;
        border: 1px solid #555;
        border-radius: 5px;
        font-size: 80%%;
        font-style: normal;
        text-align: center;
    }
    .content .tooltip:hover [class*="tooltiptext"] { visibility: visible; }

    body.tutorial-highlight {
        color: #FFD700;
        font-weight: bold;
    }
    ::-webkit-scrollbar { width: 12px; background: %(bg)s; }
    ::-webkit-scrollbar-thumb { background: #3D3D3D; border-radius: 6px; }
</style>
</head>
<body class="%(body_class)s">
%(body)s
</body>
</html>
"""


def _plain_to_html(text):
    """Escape plain text, keeping its line breaks."""
    escaped = html.escape(text, quote=False)
    return ALLOWED_TAGS.sub(r"<\1\2>", escaped)


def text_to_html(text):
    """Convert problem text into an HTML fragment.

    The first line ("Problem N: Title") becomes a heading. The rest is either
    the problem's HTML from the website, or plain text whose line breaks are
    kept. Plain text added after the HTML (such as the difficulty rating) is
    shown as plain text below it.
    """
    title, _, rest = text.partition("\n")
    if title.startswith("Problem "):
        parts = [f'<div class="problem-title">{html.escape(title, quote=False)}</div>']
    else:
        parts = []
        rest = text

    if HTML_CONTENT.search(rest):
        # Everything after the last tag is plain text appended by the app
        end = rest.rfind(">") + 1
        content, trailer = rest[:end], rest[end:]
        parts.append(f'<div class="content">{content}</div>')
        if trailer.strip():
            parts.append(f'<div class="plain">{_plain_to_html(trailer.strip())}</div>')
    else:
        parts.append(f'<div class="plain">{_plain_to_html(rest)}</div>')

    return "\n".join(parts)


def build_page(text, font_family="Arial", font_size=12, fg="#FFFFFF",
               bg="#000000", padding=10, highlight=False):
    """Build a complete HTML page for the given problem text."""
    return PAGE_TEMPLATE % {
        "body": text_to_html(text),
        "mathjax_url": QUrl.fromLocalFile(
            os.path.join(MATHJAX_DIR, "es5", "tex-chtml-full.js")).toString(),
        "font_family": font_family,
        "font_size": font_size,
        "fg": fg,
        "bg": bg,
        "padding": padding,
        "body_class": "tutorial-highlight" if highlight else "",
    }


def page_base_url():
    """Base URL that the problem's relative image paths resolve against."""
    return QUrl.fromLocalFile(PROBLEMS_DIR + os.sep)
