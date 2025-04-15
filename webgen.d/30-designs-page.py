## Responsible for creating designs page's HTML file

import webgen

def stage(data):
    ## Copy asset files
    webgen.cpr(
        webgen.resolveFsPath(data["definitions"]["runtime"]["cwd"], "data", data["config"]["Site"]["DesignsPath"]),
        webgen.resolveFsPath(data["definitions"]["runtime"]["cwd"], data["config"]["Filesystem"]["DestinationDirPath"], "assets", data["config"]["Site"]["DesignsPath"])
    )

    html = webgen.renderTemplate(data["templates"]["page"], {
        "title":       webgen.getWebPageTitle(data["config"]["Site"]["Name"], ["Designs"]),
        "description": "You have it, and I want it, too",
        "navigation": webgen.renderTemplate(data["templates"]["navigation"], {
            "activePage": "designs",
        }),
        "criticalcss": webgen.compileSass(open("../src/styles/critical.scss", "r").read()),
        "css":         "../" + data["definitions"]["filenames"]["css"],
        "class":        "designs content",
        "content":     webgen.renderMarkdown(open("../data/designs.md", "r").read()),
    })
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
