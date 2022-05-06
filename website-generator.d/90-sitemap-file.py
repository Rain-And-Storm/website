## Creates sitemap.xml

import utils

def stage(data):
    if data["config"].getboolean("Site", "CreateSitemap", fallback=False):
        ## Write sitemap file
        sitemapFile = utils.mkfile(
            data["definitions"]["runtime"]["cwd"],
            data["config"]["Filesystem"]["DestinationDirPath"],
            data["definitions"]["filenames"]["sitemap"],
        )
        xml = utils.renderTemplate(data["templates"]["sitemap"], {
            "links": map(lambda path: utils.resolveURL(data["config"]["Site"]["URL"], path), data["sitemap"]),
        })
        sitemapFile.write(xml)
        sitemapFile.close()
