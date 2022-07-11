## Responsible for creating inspirations page's HTML file

import utils

def stage(data):
    html = utils.renderTemplate(data["templates"]["page"], {
        "title":       "Inspirations " + data["config"]["Site"]["PageTitleSeparator"] + " " + data["config"]["Site"]["Name"],
        "description": "Vessels that inspired SV Curious Cat to be what she is today",
        "logo":        utils.renderTemplate(data["templates"]["link"], {
            "href": "..",
            "content": "Curious Cat",
        }),
        # "navigation":  utils.generateTopBarNavigation(data["config"]["Site"]["DbPath"] + "/"),
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
