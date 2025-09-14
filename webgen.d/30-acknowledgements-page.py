## Responsible for creating acknowledgements page's HTML file

import webgen

def stage(data):
    None
#     useRelativePaths = data["config"].getboolean("Site", "UseRelativePaths", fallback=None)

#     html = webgen.renderTemplate(data["templates"]["page"], {
#         "title":       webgen.getWebPageTitle(data["config"]["Site"]["Name"], ["Acknowledgements"]),
#         "description": "I would like to thank...",
#         # "navigation": webgen.renderTemplate(data["templates"]["navigation"], {
#         #     "activePage": "acknowledgements",
#         # }),
#         "criticalcss": webgen.compileSass(open("../src/styles/critical.scss", "r").read()),
#         "css":         webgen.buildPath("/" + data["definitions"]["filenames"]["css"], "/acknowledgements/", relative=useRelativePaths),
#         "class":        "acknowledgements content",
#         "content":     webgen.renderMarkdown(open("../data/acknowledgements.md", "r").read()),
#     })
#     htmlFile = webgen.mkfile(
#         data["definitions"]["runtime"]["cwd"],
#         data["config"]["Filesystem"]["DestinationDirPath"],
#         "acknowledgements",
#         data["definitions"]["filenames"]["index"]
#     )
#     htmlFile.write(html)
#     htmlFile.close()

#     ## Add acknowledgements page link to sitemap
#     if data["config"].getboolean("Site", "CreateSitemap", fallback=False):
#         data["sitemap"].append("/acknowledgements/")
