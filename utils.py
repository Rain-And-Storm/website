import os
import re
import shutil
import sys
from urllib.parse import quote, urljoin

import markdown
import pystache
import sass

def compileSass(scss):
    return sass.compile(string=scss, include_paths=[resolveFsPath(getCwd(), "src", "styles")], output_style='compressed')

def cpr(src, dest):
    return shutil.copytree(src, dest)

def filenameToAnchorTagId(filename):
    noExt = os.path.splitext(filename)[0]
    array = noExt.split("-")
    array.pop(0)
    return '-'.join(array)

def generatePageTitle(name, data):
    if len(name) > 0:
        return name + " " + data["config"]["Site"]["PageTitleSeparator"] + " " + data["config"]["Site"]["Name"]
    else:
        return data["config"]["Site"]["Name"]

def generateNavigation():
    links = []
    links.append(getWebPageLink("/captains-log/", "Captain’s log"))
    links.append(getWebPageLink("/inspirations/", "Inspirations"))
    return links

def getCwd():
    return os.path.dirname(os.path.realpath(__file__))

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
    return markdown.markdown(md, extensions=['tables'])

def renderTemplate(template, data):
    return pystache.render(template, data)

def resolveFsPath(*additionalPath):
    return os.path.join(os.path.sep.join(additionalPath[:320000]))

def resolveURL(base, url):
    return urljoin(base, quote(url), allow_fragments=False)
