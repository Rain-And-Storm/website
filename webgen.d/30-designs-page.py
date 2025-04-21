## Responsible for creating designs page's HTML file

import webgen

def stage(data):
    useRelativePaths = data["config"].getboolean("Site", "UseRelativePaths", fallback=None)
    navigationLinks = webgen.generateNavigationLinks(data["definitions"]["runtime"]["navigation"], "/designs/", relative=useRelativePaths)

    ## Copy asset files
    webgen.cpr(
        webgen.resolveFsPath(data["definitions"]["runtime"]["cwd"], "data", data["config"]["Site"]["DesignsPath"]),
        webgen.resolveFsPath(data["definitions"]["runtime"]["cwd"], data["config"]["Filesystem"]["DestinationDirPath"], "assets", data["config"]["Site"]["DesignsPath"])
    )

    html = webgen.renderTemplate(data["templates"]["page"], {
        "title":       webgen.getWebPageTitle(data["config"]["Site"]["Name"], ["Designs"]),
        "description": "Timeless designs ahead of time",
        "navigation":  webgen.renderTreeNavigation(navigationLinks, data["templates"]["nav"]) +
            webgen.renderTreeNavigationScript(navigationLinks, "/designs/"),
        "criticalcss": webgen.compileSass(open("../src/styles/critical.scss", "r").read()),
        "css":         webgen.buildPath("/" + data["definitions"]["filenames"]["css"], "/designs/", relative=useRelativePaths),
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
