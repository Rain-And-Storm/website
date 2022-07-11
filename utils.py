import os
import re
import sys
from urllib.parse import quote
from urllib.parse import urljoin

import markdown
import pystache
from scss import Scss

SCSS = Scss()

def compileSass(scss):
    return SCSS.compile(scss)

def getWebPageLink(target, label, type=0):
    return {
        "href": quote(target),
        "label": label,
        "type": type,
    }

def mkdir(*paths):
    os.makedirs(os.path.join(*paths), exist_ok=True)

def mkfile(*paths):
    # Ensure directory exists
    mkdir(*paths[:-1])
    # Create file
    return open(os.path.join(*paths), "w")

def renderMarkdown(md):
    return markdown.markdown(md)

def renderTemplate(template, data):
    return pystache.render(template, data)

def resolveURL(base, url):
    return urljoin(base, quote(url), allow_fragments=False)
