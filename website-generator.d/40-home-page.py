## Responsible for creating landing page's HTML file

import utils

def stage(data):
    html = utils.renderTemplate(data["templates"]["page"], {
        "title":       utils.generatePageTitle("", data),
        "description": "Curious Cat lives!",
        "logo":        utils.renderTemplate(data["templates"]["link"], {
            "href": ".",
            "content": "Curious Cat",
        }),
        "navigation":  utils.generateNavigation(),
        "criticalcss": utils.compileSass(open("../src/styles/critical.scss", "r").read()),
        "css":         data["definitions"]["filenames"]["css"],
        "name":        "home",
        "content":     utils.renderMarkdown(open("../data/home.md", "r").read()),
    })
    htmlFile = utils.mkfile(
        data["definitions"]["runtime"]["cwd"],
        data["config"]["Filesystem"]["DestinationDirPath"],
        data["definitions"]["filenames"]["index"]
    )
    htmlFile.write(html)
    htmlFile.close()
    ## Add home page link to sitemap
    if data["config"].getboolean("Site", "CreateSitemap", fallback=False):
        data["sitemap"].append("/")
