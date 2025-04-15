## Responsible for creating HTML files related to Curious Cat's gallery and copying over picture files

import os
from PIL import Image

import webgen

def stage(data):
    #
    # Loop through gallery albums
    #
    gallerySourcePath = os.path.join(
        data["definitions"]["runtime"]["cwd"],
        "data",
        "curious-cat",
        "gallery",
    )
    galleryTemplateAlbums = []
    gallerySourcePath = os.path.abspath(gallerySourcePath)
    albumNames = sorted(next(os.walk(gallerySourcePath))[1], reverse=True)
    for albumName in albumNames:
        galleryTemplateAlbums.append({"name": albumName, "pictures": []})
        galleryDataAlbumPath = os.path.join(
            gallerySourcePath,
            albumName,
        )
        ## Loop through gallery album → pictures
        pictures = sorted(next(os.walk(galleryDataAlbumPath))[2])
        if len(pictures) > 1:
            for fileName in pictures:
                if fileName.startswith("."):
                    continue
                albumAndFilePath = albumName + "/" + fileName
                albumAndThumbFilePath = albumName + "/thumb_" + fileName
                ## Create thumbnail
                image = Image.open("../data/curious-cat/gallery/" + albumName + "/" + fileName)
                image.thumbnail((640, 640))
                webgen.mkdir(data["definitions"]["runtime"]["cwd"], data["config"]["Filesystem"]["DestinationDirPath"], "assets", "curious-cat", "gallery", albumName)
                image.save(webgen.resolveFsPath(data["definitions"]["runtime"]["cwd"], data["config"]["Filesystem"]["DestinationDirPath"], "assets", "curious-cat", "gallery", albumAndThumbFilePath))
                ## Append to array of albums
                galleryTemplateAlbums[-1]["pictures"].append({ "orig": "../../assets/curious-cat/gallery/" + albumAndFilePath, "thumb": "../../assets/curious-cat/gallery/" + albumAndThumbFilePath })
                ## Copy original asset file
                webgen.cp(
                    webgen.resolveFsPath(data["definitions"]["runtime"]["cwd"], "data", "curious-cat", "gallery", albumAndFilePath),
                    webgen.resolveFsPath(data["definitions"]["runtime"]["cwd"], data["config"]["Filesystem"]["DestinationDirPath"], "assets", "curious-cat", "gallery", albumAndFilePath)
                )
        else:
            ## Omit empty albums
            galleryTemplateAlbums.pop()
    pageHTML = webgen.renderTemplate(data["templates"]["gallery"], {
        "albums": galleryTemplateAlbums
    })
    ## Generate HTML contents out of template
    html = webgen.renderTemplate(data["templates"]["page"], {
        "title":       webgen.getWebPageTitle(data["config"]["Site"]["Name"], ["Curious Cat", "Gallery"]),
        "description": "Pictures of Curious Cat, old and new",
        "navigation": webgen.renderTemplate(data["templates"]["navigation"], {
            "activePage": "curious-cat/gallery",
        }),
        "criticalcss": webgen.compileSass(open("../src/styles/critical.scss", "r").read()),
        "css":         "../../" + data["definitions"]["filenames"]["css"],
        "class":        "curious-cat gallery content",
        "content":     pageHTML,
    })
    ## Create new HTML file
    htmlFile = webgen.mkfile(
        data["definitions"]["runtime"]["cwd"],
        data["config"]["Filesystem"]["DestinationDirPath"],
        "curious-cat",
        "gallery",
        data["definitions"]["filenames"]["index"]
    )
    htmlFile.write(html)
    htmlFile.close()

    ## Add home page link to sitemap
    if data["config"].getboolean("Site", "CreateSitemap", fallback=False):
        data["sitemap"].append("/curious-cat/gallery/")
