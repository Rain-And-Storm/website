## Responsible for creating landing page’s HTML file

import os
from PIL import Image

import webgen

def stage(data):
    useRelativePaths = data["config"].getboolean("Site", "UseRelativePaths", fallback=None)
    navigationLinks = webgen.generateNavigationLinks(data["definitions"]["runtime"]["navigation"], "/", relative=useRelativePaths)

    ## Render acknowledgements
    designsSourcePath = os.path.join(
        data["definitions"]["runtime"]["cwd"],
        "data",
        "acknowledgements.d",
    )
    acknowledgements = []
    designsSourcePath = os.path.abspath(designsSourcePath)
    designsDirNames = sorted(next(os.walk(designsSourcePath))[1])
    for designDirName in designsDirNames:
        designDirPath = os.path.join(designsSourcePath, designDirName)

        if not os.path.isdir(designDirPath) or not os.path.isfile(os.path.join(designDirPath, "README.md")):
            continue

        acknowledgements.append({
            "images": [],
            "description": webgen.renderMarkdown(open(os.path.join(designDirPath, "README.md"), "r").read())
        })

        ## Loop through files within each acknowledgement's directory
        designFiles = sorted(next(os.walk(designDirPath))[2])
        for designFileName in designFiles:
            if designFileName.startswith(".") or not designFileName.endswith(".webp"):
                continue
            designAndImageFilePath = designDirName + "/" + designFileName
            designAndImageThumbFilePath = designDirName + "/thumb_" + designFileName
            ## Create thumbnail
            image = Image.open("../data/acknowledgements.d/" + designDirName + "/" + designFileName)
            image.thumbnail((640, 640))
            webgen.mkdir(data["definitions"]["runtime"]["cwd"], data["config"]["Filesystem"]["DestinationDirPath"], "acknowledgements", designDirName)
            image.save(webgen.resolveFsPath(data["definitions"]["runtime"]["cwd"], data["config"]["Filesystem"]["DestinationDirPath"], "acknowledgements", designAndImageThumbFilePath))
            ## Append to array of acknowledgements
            acknowledgements[-1]["images"].append({ "orig": "../../acknowledgements/" + designAndImageFilePath, "thumb": "../../acknowledgements/" + designAndImageThumbFilePath })
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
