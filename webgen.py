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
