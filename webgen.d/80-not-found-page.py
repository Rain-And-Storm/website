## Creates 404 page

import webgen

def stage(data):
    html = webgen.renderTemplate(data["templates"]["page"], {
        "title":       "Rain And Storm → Page Not Found",
        "description": "Error 404: page not found",
        ## Since we don't know the depth of this page relative to the root,
        ## we have to assume the db directory is located in the root of this web resource
        # "navigation":  webgen.generateTopBarNavigation("/" + data["config"].get("Site", "DbPath")),
        "name":        "error",
        # "content":     webgen.renderTemplate(data["templates"]["not-found-page-contents"]),
    })
    notFoundFile = webgen.mkfile(
        data["definitions"]["runtime"]["cwd"],
        data["config"].get("Filesystem", "DestinationDirPath"),
        data["definitions"]["filenames"]["notfound"],
    )
    notFoundFile.write(html)
    notFoundFile.close()
