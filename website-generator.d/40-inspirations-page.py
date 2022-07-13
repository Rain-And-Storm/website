## Responsible for creating inspirations page's HTML file

import utils

def stage(data):
    html = utils.renderTemplate(data["templates"]["page"], {
        "title":       utils.generatePageTitle("Inspirations", data),
        "description": "Vessels that inspired Curious Cat to be what she is today",
        "logo":        utils.renderTemplate(data["templates"]["link"], {
            "href": "..",
            "content": "Curious Cat",
        }),
        "navigation":  utils.generateNavigation(),
        "criticalcss": utils.compileSass(open("../src/styles/critical.scss", "r").read()),
        "css":         "../" + data["definitions"]["filenames"]["css"],
        "name":        "inspirations",
        "content":     utils.renderMarkdown(open("../data/inspirations.md", "r").read()),
    })
    htmlFile = utils.mkfile(
        data["definitions"]["runtime"]["cwd"],
        data["config"]["Filesystem"]["DestinationDirPath"],
        "inspirations",
        data["definitions"]["filenames"]["index"]
    )
    htmlFile.write(html)
    htmlFile.close()
    ## Add inspiration page link to sitemap
    if data["config"].getboolean("Site", "CreateSitemap", fallback=False):
        data["sitemap"].append("/inspirations/")
