## Responsible for creating Curious Cat's systems page’s HTML file

import os

import yaml

import webgen

blankPixel = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="

# CA: 🇨🇦
# DE: 🇩🇪
# IT: 🇮🇹
# NL: 🇳🇱
# UK: 🇬🇧
# US: 🇺🇸

connections = []

def printSystemHtml(systemName, systemDataItem):
    id = systemName.replace(" ", "_") + "__" + systemDataItem["what"].replace(" ", "_")
    # Print system component's title
    title: str = str(systemDataItem["name"] if "name" in systemDataItem else systemDataItem["what"])
    output = "<div id=\"" + id + "\">"
    output += "<h3>" + title + "</h3>"
    output += "<a href=" + (systemDataItem["link"] if "link" in systemDataItem else "javascript:void(0)") + "><img src=" + (systemDataItem["image"] if "image" in systemDataItem else blankPixel) + " alt=" + title + " /></a>"
    output += "<ul>"
    for systemKey, systemValue in systemDataItem.items():
        if systemKey == "connected_to":
            connections.append([id, systemName.replace(" ", "_") + "__" + systemValue.replace(" ", "_")])
        else:
            # Print properties of the system
            if systemKey not in ["what", "name", "image", "link"]:
                value: str = str(systemValue) if (isinstance(systemValue, str) or isinstance(systemValue, int)) else ", ".join(systemValue)
                output += "<li>" + systemKey.replace("_", " ").title() + ": " + value + " </li>"
    output += "</ul>"
    output += "</div>"
    return output

def stage(data):
    ## Copy asset files
    webgen.cpr(
        webgen.resolveFsPath(data["definitions"]["runtime"]["cwd"], "data", "curious-cat", data["config"]["Site"]["SystemsPath"]),
        webgen.resolveFsPath(data["definitions"]["runtime"]["cwd"], data["config"]["Filesystem"]["DestinationDirPath"], "assets", "curious-cat", data["config"]["Site"]["SystemsPath"])
    )

    #
    # Parse systems YAML and header Markdown files
    #
    systemsSourcePath = os.path.join(
        data["definitions"]["runtime"]["cwd"],
        "data",
        "curious-cat",
        "systems.yaml",
    )
    pageHtml = ""
    systemsSourcePath = os.path.abspath(systemsSourcePath)

    with open(systemsSourcePath, "r") as stream:
        try:
            # print(yaml.safe_load(stream))
            systemsObject = yaml.safe_load(stream)
            for systemName, systemData in systemsObject.items():
                pageHtml += "<fieldset>"
                pageHtml += "<legend><h2>" + systemName.title() + "</h2></legend>"
                for systemDataItem in systemData:
                    if systemDataItem["what"] == "separator":
                        pageHtml += "<hr />"
                    else:
                        pageHtml += printSystemHtml(systemName, systemDataItem)
                pageHtml += "</fieldset>"
                pageHtml += "<br />"
        except yaml.YAMLError as exception:
            pageHtml = "Error: " + str(exception)

    html = webgen.renderTemplate(data["templates"]["page"], {
        "title":       "Rain And Storm → Curious Cat → Systems",
        "description": "Detailed description of various systems installed aboard SV Curious Cat",
        "navigation": webgen.renderTemplate(data["templates"]["navigation"], {
            "activePage": "curious-cat/systems",
        }),
        "criticalcss": webgen.compileSass(open("../src/styles/critical.scss", "r").read()),
        "css":         "../../" + data["definitions"]["filenames"]["css"],
        "class":       "curious-cat systems content",
        "content":     pageHtml,
    })
    # html += "<script src=\"https://cdnjs.cloudflare.com/ajax/libs/leader-line/1.0.7/leader-line.min.js\"></script>"
    html += "<script>"
    for c in connections:
        html += "new LeaderLine(document.getElementById('" + c[0] +"'),document.getElementById('" + c[1] +"'), { color: 'green', dash: { animation: true }, path: 'straight' });"
    html += "</script>"
    htmlFile = webgen.mkfile(
        data["definitions"]["runtime"]["cwd"],
        data["config"]["Filesystem"]["DestinationDirPath"],
        "curious-cat",
        data["config"]["Site"]["SystemsPath"],
        data["definitions"]["filenames"]["index"]
    )
    htmlFile.write(html)
    htmlFile.close()

    ## Add systems page link to sitemap
    if data["config"].getboolean("Site", "CreateSitemap", fallback=False):
        data["sitemap"].append("/curious-cat/systems/")
