## Responsible for creating landing page’s HTML file

import os
import re

from PIL import Image

import webgen

def extract_first_h1(html):
    pattern = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.I | re.S)
    matches = pattern.findall(html)
    return matches[0] if matches else None

def remove_first_h1(html):
    pattern = re.compile(r"<h1\b[^>]*>.*?</h1\s*>", re.I | re.S)
    m = pattern.search(html)
    if not m:
        return html
    start, end = m.span()
    return html[:start] + html[end:]

def stage(data):
    useRelativePaths = data["config"].getboolean("Site", "UseRelativePaths", fallback=None)
    navigationLinks = webgen.generateNavigationLinks(data["definitions"]["runtime"]["navigation"], "/", relative=useRelativePaths)

    ## Render acknowledgements
    acknowledgementsSourcePath = os.path.join(
        data["definitions"]["runtime"]["cwd"],
        "data",
        "acknowledgements.d",
    )
    acknowledgements = []
    acknowledgementsSourcePath = os.path.abspath(acknowledgementsSourcePath)
    acknowledgementsDirNames = sorted(next(os.walk(acknowledgementsSourcePath))[1])
    for acknowledgementDirName in acknowledgementsDirNames:
        acknowledgementDirPath = os.path.join(acknowledgementsSourcePath, acknowledgementDirName)

        if not os.path.isdir(acknowledgementDirPath) or not os.path.isfile(os.path.join(acknowledgementDirPath, "README.md")):
            continue

        html = webgen.renderMarkdown(open(os.path.join(acknowledgementDirPath, "README.md"), "r").read())

        acknowledgements.append({
            "title": extract_first_h1(html),
            "images": [],
            "description": remove_first_h1(html)
        })

        ## Loop through files within each acknowledgement's directory
        acknowledgementFiles = sorted(next(os.walk(acknowledgementDirPath))[2])
        for acknowledgementFileName in acknowledgementFiles:
            if acknowledgementFileName.startswith(".") or not acknowledgementFileName.endswith((".webp", ".jpg", ".jpeg", ".png", ".svg", ".avif")):
                continue
            acknowledgementAndImageFilePath = acknowledgementDirName + "/" + acknowledgementFileName
            acknowledgementAndImageThumbFilePath = acknowledgementDirName + "/thumb_" + acknowledgementFileName
            ## Create thumbnail
            if acknowledgementFileName.endswith((".webp", ".jpg", ".jpeg", ".png")):
                image = Image.open("../data/acknowledgements.d/" + acknowledgementAndImageFilePath)
                image.thumbnail((640, 640))
                webgen.mkdir(data["definitions"]["runtime"]["cwd"], data["config"]["Filesystem"]["DestinationDirPath"], "acknowledgements", acknowledgementDirName)
                image.save(webgen.resolveFsPath(data["definitions"]["runtime"]["cwd"], data["config"]["Filesystem"]["DestinationDirPath"], "acknowledgements", acknowledgementAndImageThumbFilePath))
            else:
                webgen.cp(
                    webgen.resolveFsPath(data["definitions"]["runtime"]["cwd"], "data", "acknowledgements.d", acknowledgementAndImageFilePath),
                    webgen.resolveFsPath(data["definitions"]["runtime"]["cwd"], data["config"]["Filesystem"]["DestinationDirPath"], "acknowledgements", acknowledgementAndImageThumbFilePath)
                )
            ## Append to array of acknowledgement's images
            acknowledgements[-1]["images"].append({ "orig": "../../acknowledgements/" + acknowledgementAndImageFilePath, "thumb": "../../acknowledgements/" + acknowledgementAndImageThumbFilePath })
            # acknowledgements[-1]["description"] += "<img src=\"" + acknowledgements[-1]["images"][0]['thumb'] + "\" />"
    acknowledgementsHtml = webgen.renderTemplate(data["templates"]["items"], {
        "items": acknowledgements
    })

    ## Render homepage template
    html = webgen.renderTemplate(data["templates"]["page"], {
        "title":       data["config"]["Site"]["Name"],
        "description": "Open source for open waters",
        "navigation":  webgen.renderTreeNavigation(navigationLinks, data["templates"]["nav"]) +
            webgen.renderTreeNavigationScript(navigationLinks, "/"),
        "criticalcss": webgen.compileSass(open("../src/styles/critical.scss", "r").read()),
        "css":         webgen.buildPath("/" + data["definitions"]["filenames"]["css"], "/", relative=useRelativePaths),
        "class":        "home content",
        "content":     webgen.renderMarkdown(open("../data/home.md", "r").read()) + "<h1>Acknowledgements</h1>" + acknowledgementsHtml,
    })

    ## Create HTML file
    htmlFile = webgen.mkfile(
        data["definitions"]["runtime"]["cwd"],
        data["config"]["Filesystem"]["DestinationDirPath"],
        data["definitions"]["filenames"]["index"]
    )
    htmlFile.write(html)
    htmlFile.close()

    ## Add home page link to sitemap
    if data["config"].getboolean("Site", "CreateSitemap", fallback=False):
        data["sitemap"].append("/")
