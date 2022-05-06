## Responsible for creating Curious Cat's main page’s HTML file

import webgen

def stage(data):
    html = webgen.renderTemplate(data["templates"]["page"], {
        "title":       "Rain And Storm → Curious Cat",
        "description": "Curious Cat lives!",
        "navigation": webgen.renderTemplate(data["templates"]["navigation"], {
            "activePage": "curious-cat",
        }),
        "criticalcss": webgen.compileSass(open("../src/styles/critical.scss", "r").read()),
        "css":         "../" + data["definitions"]["filenames"]["css"],
        "class":        "curious-cat main content",
        "content":     webgen.renderMarkdown(open("../data/curious-cat/main.md", "r").read()),
    })
    htmlFile = webgen.mkfile(
        data["definitions"]["runtime"]["cwd"],
        data["config"]["Filesystem"]["DestinationDirPath"],
        "curious-cat",
        data["definitions"]["filenames"]["index"]
    )
    htmlFile.write(html)
    htmlFile.close()

    ## Add home page link to sitemap
    if data["config"].getboolean("Site", "CreateSitemap", fallback=False):
        data["sitemap"].append("/curious-cat/")
