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

def generatePageTitle(name, data):
    if len(name) > 0:
        return name + " " + data["config"]["Site"]["PageTitleSeparator"] + " " + data["config"]["Site"]["Name"]
    else:
        return data["config"]["Site"]["Name"]

def generateNavigation():
    links = []
    links.append(getWebPageLink("/logbook/", "Captain’s log"))
    links.append(getWebPageLink("/inspirations/", "Inspirations"))
    return links

def getWebPageLink(target, label):
    return {
        "href": quote(target),
        "label": label,
    }

def mkdir(*paths):
    os.makedirs(os.path.join(*paths), exist_ok=True)

def mkfile(*paths):
    # Ensure the directory path exists
    mkdir(*paths[:-1])
    # Create file
    return open(os.path.join(*paths), "w")

def renderMarkdown(md):
    return markdown.markdown(md)

def renderTemplate(template, data):
    return pystache.render(template, data)

def resolveURL(base, url):
    return urljoin(base, quote(url), allow_fragments=False)
