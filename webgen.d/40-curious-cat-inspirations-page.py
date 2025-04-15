## Responsible for creating Curious Cat's inspirations page's HTML file

import webgen

def stage(data):
    ## Copy asset files
    webgen.cpr(
        webgen.resolveFsPath(data["definitions"]["runtime"]["cwd"], "data", "curious-cat", "inspirations"),
        webgen.resolveFsPath(data["definitions"]["runtime"]["cwd"], data["config"]["Filesystem"]["DestinationDirPath"], "assets", "curious-cat", data["config"]["Site"]["InspirationsPath"])
    )

    html = webgen.renderTemplate(data["templates"]["page"], {
        "title":       webgen.getWebPageTitle(data["config"]["Site"]["Name"], ["Curious Cat", "Inspirations"]),
        "description": "Vessels that have inspired Curious Cat to be what she is today",
        "navigation": webgen.renderTemplate(data["templates"]["navigation"], {
            "activePage": "curious-cat/inspirations",
        }),
        "criticalcss": webgen.compileSass(open("../src/styles/critical.scss", "r").read()),
        "css":         "../../" + data["definitions"]["filenames"]["css"],
        "class":        "curious-cat inspirations content",
        "content":     webgen.renderMarkdown(open("../data/curious-cat/inspirations.md", "r").read()),
    })
    htmlFile = webgen.mkfile(
        data["definitions"]["runtime"]["cwd"],
        data["config"]["Filesystem"]["DestinationDirPath"],
        "curious-cat",
        data["config"]["Site"]["InspirationsPath"],
        data["definitions"]["filenames"]["index"]
    )
    htmlFile.write(html)
    htmlFile.close()

    ## Add inspiration page link to sitemap
    if data["config"].getboolean("Site", "CreateSitemap", fallback=False):
        data["sitemap"].append("/curious-cat/" + data["config"]["Site"]["InspirationsPath"] + "/")
