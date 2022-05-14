## Responsible for creating landing page HTML file

import utils

def stage(data):
    homePathWebPageLink = utils.getWebPageLink(".", "Home")
    html = utils.renderTemplate(data["templates"]["page"], {
        "title":       data["config"]["Site"]["Name"],
        "description": "Sailing blog of SV Curious Cat",
        "logo":        utils.renderTemplate(data["templates"]["link"], {
            "href": ".",
            "content": "Curious Cat",
        }),
        # "navigation":  utils.generateTopBarNavigation(data["config"]["Site"]["DbPath"] + "/"),
        "css":         data["definitions"]["filenames"]["css"],
        "name":        "home",
        "content":     utils.renderMarkdown(open("../data/about.md", "r").read()),
    })
    homepageFile = utils.mkfile(
        data["definitions"]["runtime"]["cwd"],
        data["config"]["Filesystem"]["DestinationDirPath"],
        data["definitions"]["filenames"]["index"]
    )
    homepageFile.write(html)
    homepageFile.close()
    ## Add home page link to sitemap
    if data["config"].getboolean("Site", "CreateSitemap", fallback=False):
        data["sitemap"].append("/")
