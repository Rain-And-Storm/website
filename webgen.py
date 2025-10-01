#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import importlib.util
import markdown
import os
import pystache
import re
import sass
import shutil
import sys
import urllib.parse

##############################################################################

def buildPath(full_path, current_location, relative=None):
    """
    Resolves the path based on the current location and returns the shortest path if relative is not specified.
    :param full_path: The absolute path to the file (starting from root "/").
    :param current_location: The current directory location (starting from root "/").
    :param relative: Boolean flag to determine if the path should be relative. If None, returns the shortest path.
    :return: The resolved path. Returns the shortest path if relative is None.
    """
    # Normalize the paths to ensure they are in a standard format
    full_path = os.path.normpath(full_path)
    current_location = os.path.normpath(current_location)

    # Compute the relative path
    relative_path = os.path.relpath(full_path, start=current_location)

    # If relative is explicitly specified, return the corresponding path
    if relative is True:
        return relative_path
    elif relative is False:
        return full_path
    else:
        # Compare string lengths of absolute and relative paths, and return the shorter one
        return full_path if len(full_path) <= len(relative_path) else relative_path

def compileSass(scss):
    return sass.compile(string=scss, include_paths=[resolveFsPath(getCwd(), "src", "styles")], output_style='compressed')

def cp(src, dest):
    return shutil.copyfile(src, dest)

def cpr(src, dest):
    return shutil.copytree(src, dest)

def filenameToAnchorTagId(filename):
    noExt = os.path.splitext(filename)[0]
    array = noExt.split("-")
    array.pop(0)
    return '-'.join(array)

def generateNavigationLinks(links, current_location, relative=None):
    navLinks = []
    for link in links:
        navLink = {
            "id": "nav-link__" + (link["destination"].strip("/").replace("/", "__") or "root"),
            "destination": buildPath(link["destination"], current_location, relative),
            "label": link["label"]
        }
        if "children" in link and len(link["children"]) > 0:
            navLink["children"] = generateNavigationLinks(link["children"], current_location, relative)
        if link["destination"] == current_location:
            navLink["active"] = True
        navLinks.append(navLink)
    return navLinks

def getCwd():
    return os.path.dirname(os.path.realpath(__file__))

def getWebPageLink(target, label):
    return {
        "href": urllib.parse.quote(target),
        "label": label,
    }

def getWebPageTitle(siteName, *subtitles):
    title = siteName
    if len(subtitles) > 0:
        title += " → " + " → ".join(*subtitles)
    return title

def mkdir(*paths):
    os.makedirs(os.path.join(*paths), exist_ok=True)

def mkfile(*paths):
    # Ensure the directory path exists
    mkdir(*paths[:-1])
    # Create file
    return open(os.path.join(*paths), "w")

def renderMarkdown(md):
    return markdown.markdown(md, extensions=['tables'])

def renderTemplate(template, data):
    return pystache.render(template, data)

def renderTreeNavigation(links, template):
    result = ""
    for link in links:
        if "children" in link and len(link["children"]) > 0:
            childrenHtml = renderTreeNavigation(link["children"], template)
            link["childrenHtml"] = childrenHtml
    result = renderTemplate(template, links)
    return result

def renderTreeNavigationScript(links, current_location):
    if len(links) < 1:
        return "";

    return """
<script src="//unpkg.com/leader-line@1.0.8/leader-line.min.js"></script>
<script>

setTimeout(() => {
    const lineOptions = {
        color: 'lightblue',
        size: 2,
        path: 'magnet',
        dash: {
            animation: true
        },
        endPlug: 'behind',
    };

    new LeaderLine(
        document.getElementById('nav-link__root'),
        document.getElementById('nav-link__designs'),
        lineOptions
    );

    new LeaderLine(
        document.getElementById('nav-link__root'),
        document.getElementById('nav-link__software'),
        lineOptions
    );

/*
    new LeaderLine(
        document.getElementById('nav-link__root'),
        document.getElementById('nav-link__acknowledgements'),
        lineOptions
    );
*/

    new LeaderLine(
        document.getElementById('nav-link__root'),
        document.getElementById('nav-link__curious-cat'),
        lineOptions
    );

    new LeaderLine(
        document.getElementById('nav-link__curious-cat'),
        document.getElementById('nav-link__curious-cat__gallery'),
        lineOptions
    );

    new LeaderLine(
        document.getElementById('nav-link__curious-cat'),
        document.getElementById('nav-link__curious-cat__inspirations'),
        lineOptions
    );

    new LeaderLine(
        document.getElementById('nav-link__curious-cat'),
        document.getElementById('nav-link__curious-cat__systems'),
        lineOptions
    );
}, 0);

</script>"""

def resolveFsPath(*additionalPath):
    return os.path.join(os.path.sep.join(additionalPath[:320000]))

def resolveURL(base, url):
    return urllib.parse.urljoin(base, urllib.parse.quote(url), allow_fragments=False)

##############################################################################

if __name__ == "__main__":
    ## Global constants
    definitions = {
        "runtime": {
            "cwd": getCwd(),
            "navigation": [
                {
                    "destination": "/",
                    "label": "Rain And Storm",
                    "children": [
                        {
                            "destination": "/designs/",
                            "label": "Designs"
                        },
                        {
                            "destination": "/software/",
                            "label": "Software"
                        },
                        {
                            "destination": "/curious-cat/",
                            "label": "Curious Cat",
                            "children": [
                                {
                                    "destination": "/curious-cat/gallery/",
                                    "label": "Gallery"
                                },
                                {
                                    "destination": "/curious-cat/inspirations/",
                                    "label": "Inspirations"
                                },
                                {
                                    "destination": "/curious-cat/systems/",
                                    "label": "Equipment"
                                }
                            ]
                        },
                    ]
                }
            ]
        },
        "filenames": {
            "index":    "index.html",
            "notfound": "404.html",
            "css":      "_.css",
            "sitemap":  "sitemap.xml",
        },
    }

    ## Config
    config = configparser.ConfigParser()
    configFile = os.path.join(definitions["runtime"]["cwd"], "config.ini")
    if os.path.isfile(configFile):
        config.read(configFile)
    else:
        print("Error: config.ini does not exist")
        exit()

    ## Function for optimizing template code
    def shrinkwrapTemplate(markup):
        return re.sub(r"\n\s*", "", markup)

    ## Function for reading and optimizing template code
    def getTemplateContents(templateFileName):
        if templateFileName == "sitemap.mustache":
            return open(os.path.join(templatesPath, templateFileName), "r").read()
        else:
            return shrinkwrapTemplate(open(os.path.join(templatesPath, templateFileName), "r").read())

    ## Read and store template files
    templates = {}
    templatesPath = os.path.join(definitions["runtime"]["cwd"], "src", "templates")
    templatesFileNames = next(os.walk(templatesPath))[2]
    for templateFileName in templatesFileNames:
        (templateName, _) = os.path.splitext(templateFileName)
        templates[templateName] = getTemplateContents(templateFileName)

    ## Compose data to be consumed by build stages
    data = {
        "definitions": definitions,
        "config": config,
        "templates": templates,
    }
    if data["config"].getboolean("Site", "CreateSitemap", fallback=False):
        data["sitemap"] = []

    ## Load and execute build stages one-by-one
    buildStagesDirectory = os.path.join(definitions["runtime"]["cwd"], os.path.splitext(os.path.basename(__file__))[0] + ".d")
    for buildStageFilename in sorted(os.listdir(buildStagesDirectory), key=str.lower):
        if buildStageFilename.endswith(".py"):
            spec = importlib.util.spec_from_file_location(buildStageFilename, os.path.join(buildStagesDirectory, buildStageFilename))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            buildStageMainFn = getattr(module, "stage")
            buildStageMainFn(data)
