"""
Render problem text as HTML with math typeset by a bundled copy of MathJax.

Problem files contain the same TeX notation that projecteuler.net uses
($...$ for inline math, $$...$$ for display math). MathJax is loaded from
the local 'mathjax' folder, so no internet connection is needed.
"""

import html
import os
import re

from PyQt6.QtCore import QUrl

# Project root (in a PyInstaller build this is the _internal folder,
# which is where the 'mathjax' data folder is copied to).
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MATHJAX_DIR = os.path.join(BASE_DIR, "mathjax")

# HTML tags that occasionally appear in problem files and should be kept
ALLOWED_TAGS = re.compile(r"&lt;(/?)(sup|sub|b|i|em|strong)&gt;", re.IGNORECASE)

PAGE_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script>
window.MathJax = {
    tex: {
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
    },
    chtml: { scale: 1.05 },
    options: { enableMenu: false }
};
</script>
<script src="es5/tex-chtml-full.js"></script>
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
    }
    .problem {
        white-space: pre-wrap;
        overflow-wrap: break-word;
    }
    .problem-title {
        font-weight: bold;
        font-size: 1.15em;
    }
    mjx-container[display="true"] {
        margin: 0.6em 0 !important;
    }
    body.tutorial-highlight {
        color: #FFD700;
        font-weight: bold;
    }
    ::-webkit-scrollbar { width: 12px; background: %(bg)s; }
    ::-webkit-scrollbar-thumb { background: #3D3D3D; border-radius: 6px; }
</style>
</head>
<body class="%(body_class)s">
<div class="problem">%(body)s</div>
</body>
</html>
"""


def text_to_html(text):
    """Convert plain problem text into an HTML fragment.

    Line breaks are preserved by the 'white-space: pre-wrap' style, so the
    text is kept in one block and math that spans lines still works.
    """
    escaped = html.escape(text, quote=False)
    escaped = ALLOWED_TAGS.sub(r"<\1\2>", escaped)

    # Make the "Problem N: Title" line stand out
    lines = escaped.split("\n", 1)
    if lines[0].startswith("Problem "):
        title = f'<span class="problem-title">{lines[0]}</span>'
        escaped = title + ("\n" + lines[1] if len(lines) > 1 else "")

    return escaped


def build_page(text, font_family="Arial", font_size=12, fg="#FFFFFF",
               bg="#000000", padding=10, highlight=False):
    """Build a complete HTML page for the given plain problem text."""
    return PAGE_TEMPLATE % {
        "body": text_to_html(text),
        "font_family": font_family,
        "font_size": font_size,
        "fg": fg,
        "bg": bg,
        "padding": padding,
        "body_class": "tutorial-highlight" if highlight else "",
    }


def mathjax_base_url():
    """Base URL that the page's relative MathJax script path resolves against."""
    return QUrl.fromLocalFile(MATHJAX_DIR + os.sep)
