## Responsible for creating designs page's HTML file

import os
from PIL import Image

import webgen

def stage(data):
    useRelativePaths = data["config"].getboolean("Site", "UseRelativePaths", fallback=None)
    navigationLinks = webgen.generateNavigationLinks(data["definitions"]["runtime"]["navigation"], "/designs/", relative=useRelativePaths)

    ## Loop through design folders
    designsSourcePath = os.path.join(
        data["definitions"]["runtime"]["cwd"],
        "data",
        "designs.d",
    )
    designs = []
    designsSourcePath = os.path.abspath(designsSourcePath)
    designsDirNames = sorted(next(os.walk(designsSourcePath))[1])
    for designDirName in designsDirNames:
        designDirPath = os.path.join(designsSourcePath, designDirName)

        if not os.path.isdir(designDirPath) or not os.path.isfile(os.path.join(designDirPath, "README.md")):
            continue

        designs.append({
            "images": [],
            "description": webgen.renderMarkdown(open(os.path.join(designDirPath, "README.md"), "r").read())
        })

        ## Loop through files within each design's directory
        designFiles = sorted(next(os.walk(designDirPath))[2])
        for designFileName in designFiles:
            if designFileName.startswith(".") or not designFileName.endswith(".webp"):
                continue
            designAndImageFilePath = designDirName + "/" + designFileName
            designAndImageThumbFilePath = designDirName + "/thumb_" + designFileName
            ## Create thumbnail
            image = Image.open("../data/designs.d/" + designDirName + "/" + designFileName)
            image.thumbnail((640, 640))
            webgen.mkdir(data["definitions"]["runtime"]["cwd"], data["config"]["Filesystem"]["DestinationDirPath"], "designs", designDirName)
            image.save(webgen.resolveFsPath(data["definitions"]["runtime"]["cwd"], data["config"]["Filesystem"]["DestinationDirPath"], "designs", designAndImageThumbFilePath))
            ## Append to array of designs
            designs[-1]["images"].append({ "orig": "../../designs/" + designAndImageFilePath, "thumb": "../../designs/" + designAndImageThumbFilePath })
    designsHtml = webgen.renderTemplate(data["templates"]["items"], {
        "items": designs
    })
    ## Generate HTML contents out of template
    html = webgen.renderTemplate(data["templates"]["page"], {
        "title":       webgen.getWebPageTitle(data["config"]["Site"]["Name"], ["Designs"]),
        "description": "Timeless designs ahead of their time",
        "navigation":  webgen.renderTreeNavigation(navigationLinks, data["templates"]["nav"]) +
            webgen.renderTreeNavigationScript(navigationLinks, "/designs/"),
        "criticalcss": webgen.compileSass(open("../src/styles/critical.scss", "r").read()),
        "css":         webgen.buildPath("/" + data["definitions"]["filenames"]["css"], "/designs/", relative=useRelativePaths),
        "class":       "designs content",
        "content":     designsHtml + "<hr />" + webgen.renderMarkdown(open("../data/designs.d/README.md", "r").read()),
    })

    ## Create HTML file
    htmlFile = webgen.mkfile(
        data["definitions"]["runtime"]["cwd"],
        data["config"]["Filesystem"]["DestinationDirPath"],
        data["config"]["Site"]["DesignsPath"],
        data["definitions"]["filenames"]["index"]
    )
    htmlFile.write(html)
    htmlFile.close()

    ## Add designs page link to sitemap
    if data["config"].getboolean("Site", "CreateSitemap", fallback=False):
        data["sitemap"].append("/" + data["config"]["Site"]["DesignsPath"] + "/")
