import os
import re
import sys
from urllib.parse import quote
from urllib.parse import urljoin

import markdown
import pystache

def getText(lyricsFileContents):
    lyricsText = lyricsFileContents
    ## Trim text
    lyricsText = lyricsText.strip()
    ## Add newlines at end of text (unless it’s empty)
    if lyricsText != "":
        lyricsText += "\n\n"
    return lyricsText

def getWebPageLink(target, label, type=0):
    return {
        "href": quote(target),
        "label": label,
        "type": type,
    }

def indent(what="", amount=0):
    indentation = ""
    if amount > 0:
        indentation = "│ " * (amount - 1)
        indentation += "├─" # └
    return indentation + what

def mkdir(*paths):
    os.makedirs(os.path.join(*paths), exist_ok=True)

def mkfile(*paths):
    return open(os.path.join(*paths), "w")

def renderMarkdown(md):
    return markdown.markdown(md)

def renderTemplate(template, data):
    return pystache.render(template, data)

def resolveURL(base, url):
    return urljoin(base, quote(url), allow_fragments=False)
