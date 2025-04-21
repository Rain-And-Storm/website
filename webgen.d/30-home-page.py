## Responsible for creating landing page’s HTML file

import webgen

def stage(data):
    useRelativePaths = data["config"].getboolean("Site", "UseRelativePaths", fallback=None)
    navigationLinks = webgen.generateNavigationLinks(data["definitions"]["runtime"]["navigation"], "/", relative=useRelativePaths)

    html = webgen.renderTemplate(data["templates"]["page"], {
        "title":       data["config"]["Site"]["Name"],
        "description": "Open source for open waters",
        "navigation":  webgen.renderTreeNavigation(navigationLinks, data["templates"]["nav"]) +
            webgen.renderTreeNavigationScript(navigationLinks, "/"),
        "criticalcss": webgen.compileSass(open("../src/styles/critical.scss", "r").read()),
        "css":         webgen.buildPath("/" + data["definitions"]["filenames"]["css"], "/", relative=useRelativePaths),
        "class":        "home content",
        "content":     webgen.renderMarkdown(open("../data/home.md", "r").read()),
    })
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
