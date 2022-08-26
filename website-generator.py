#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import importlib.util
import os
import re

import utils

## Global constants
definitions = {
    "runtime": {
        "cwd": utils.getCwd(),
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
