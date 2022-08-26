## Responsible for creating logbook pages' HTML files

import datetime
import os
import re

import utils

def formatLogbookPageDate(logbookPage):
    return datetime.datetime(int(logbookPage["year"]), int(logbookPage["month"]), int(logbookPage["day"])).strftime("%d.%m.%Y")

def stage(data):
    # 
    # Schema for logbookPage:
    #  - year: string
    #  - month: string
    #  - day: string
    #  - records: dict
    #  - prevPage: logbookPage
    #  - nextPage: logbookPage
    #
    logbookPages = []

    #
    # Loop through logbook years
    #
    logbookPath = os.path.join(
        data["definitions"]["runtime"]["cwd"],
        "data",
        "logbook",
    )
    logbookPath = os.path.abspath(logbookPath)
    years = sorted(next(os.walk(logbookPath))[1])
    for year in years:
        logbookYearPath = os.path.join(
            logbookPath,
            year,
        )
        ## Loop through logbook years → months
        months = sorted(next(os.walk(logbookYearPath))[1])
        for month in months:
            logbookYearMonthPath = os.path.join(
                logbookYearPath,
                month,
            )
            ## Loop through logbook years → months → days
            days = sorted(next(os.walk(logbookYearMonthPath))[1])
            for day in days:
                logbookYearMonthDayPath = os.path.join(
                    logbookYearMonthPath,
                    day,
                )
                logbookPageData = {
                    "year": year,
                    "month": month,
                    "day": day,
                    "records": {},
                }
                if (len(logbookPages) > 0):
                    logbookPageData["prevPage"] = logbookPages[-1]
                    logbookPages[-1]["nextPage"] = logbookPageData
                logbookPages.append(logbookPageData)
                ## Loop through logbook years → months → days → records
                records = sorted(next(os.walk(logbookYearMonthDayPath))[2], key=str.lower)
                for recordFileName in records:
                    ## Skip system files
                    if recordFileName == '.DS_Store':
                        continue
                    logbookYearMonthDayRecordPath = os.path.join(
                        logbookYearMonthDayPath,
                        recordFileName,
                    )
                    logbookPages[-1]["records"][recordFileName] = open(os.path.join(data["definitions"]["runtime"]["cwd"], "data", "logbook", year, month, day, recordFileName), "r").read()

    #
    # Create captain's log HTML pages out of Markdown files
    #
    for logbookPage in logbookPages:
        formattedDate = formatLogbookPageDate(logbookPage)
        records = logbookPage["records"]
        recordsHtml = "<h1>Captain’s log<br />Dateline: " + formattedDate + "</h1>"
        for recordFileName in records:
            # Add ID anchor
            recordsHtml += "<a id=\"" + utils.filenameToAnchorTagId(recordFileName) + "\"></a>"
            # Render the logbook entry
            recordsHtml += utils.renderMarkdown(records[recordFileName])
        prevLinkHtml = ""
        if "prevPage" in logbookPage:
            prevRecords = logbookPage["prevPage"]["records"]
            prevRecordsHtml = "<h1>Captain’s log<br />Dateline: " + formatLogbookPageDate(logbookPage["prevPage"]) + "</h1>"
            for recordFileName in prevRecords:
                prevRecordsHtml += utils.renderMarkdown(prevRecords[recordFileName])
            # Strip off all anchor tags
            prevRecordsHtml = re.sub('<(?:a[^>]*>|/a>)', '', prevRecordsHtml)
            prevLinkHtml = utils.renderTemplate(data["templates"]["link"], {
                "href": "../../../" + logbookPage["prevPage"]["year"] + "/" + logbookPage["prevPage"]["month"] + "/" + logbookPage["prevPage"]["day"] + "/",
                "class": "content",
                "content": prevRecordsHtml
            })
        nextLinkHtml = ""
        if "nextPage" in logbookPage:
            nextRecords = logbookPage["nextPage"]["records"]
            nextRecordsHtml = "<h1>Captain’s log<br />Dateline: " + formatLogbookPageDate(logbookPage["nextPage"]) + "</h1>"
            for recordFileName in nextRecords:
                nextRecordsHtml += utils.renderMarkdown(nextRecords[recordFileName])
            nextRecordsHtml = re.sub('<(?:a[^>]*>|/a>)', '', nextRecordsHtml)
            nextLinkHtml = utils.renderTemplate(data["templates"]["link"], {
                "href": "../../../" + logbookPage["nextPage"]["year"] + "/" + logbookPage["nextPage"]["month"] + "/" + logbookPage["nextPage"]["day"] + "/",
                "class": "content",
                "content": nextRecordsHtml
            })
        html = utils.renderTemplate(data["templates"]["page"], {
            "title":       utils.generatePageTitle("Captain’s log, " + formattedDate, data),
            "description": "Captain’s log, " + formattedDate,
            "logo":        utils.renderTemplate(data["templates"]["link"], {
                "href": "../../../..",
                "content": "Curious Cat",
            }),
            "navigation":  utils.generateNavigation(),
            "criticalcss": utils.compileSass(open("../src/styles/critical.scss", "r").read()),
            "css":         "../../../../" + data["definitions"]["filenames"]["css"],
            "name":        "logbook",
            "content":     utils.renderTemplate(data["templates"]["logbook-page"], {
                "date": formattedDate,
                "prevLink": prevLinkHtml,
                "content": recordsHtml,
                "nextLink": nextLinkHtml,
            })
        })
        htmlFile = utils.mkfile(
            data["definitions"]["runtime"]["cwd"],
            data["config"]["Filesystem"]["DestinationDirPath"],
            data["config"]["Site"]["CaptainsLogPath"],
            logbookPage["year"],
            logbookPage["month"],
            logbookPage["day"],
            data["definitions"]["filenames"]["index"]
        )
        htmlFile.write(html)
        htmlFile.close()
        ## Copy asset files
        if os.path.isdir(os.path.join(data["definitions"]["runtime"]["cwd"], "data", "logbook", logbookPage['year'], logbookPage['month'], logbookPage['day'], "assets")):
            utils.cpr(
                os.path.join(data["definitions"]["runtime"]["cwd"], "data", "logbook", logbookPage['year'], logbookPage['month'], logbookPage['day'], "assets"),
                os.path.join(data["definitions"]["runtime"]["cwd"], data["config"]["Filesystem"]["DestinationDirPath"], data["config"]["Site"]["CaptainsLogPath"], logbookPage['year'], logbookPage['month'], logbookPage['day'], "assets")
            )
        ## Add this logbook page's link to sitemap
        if data["config"].getboolean("Site", "CreateSitemap", fallback=False):
            data["sitemap"].append("/" + data["config"]["Site"]["CaptainsLogPath"] + "/" + logbookPage["year"] + "/" + logbookPage["month"] + "/" + logbookPage["day"] + "/")

    #
    # Generate latest captain's log page
    #
    logbookPage = logbookPages[-1]
    formattedDate = formatLogbookPageDate(logbookPage)
    records = logbookPage["records"]
    recordsHtml = "<h1>Captain’s log<br />Dateline: " + formattedDate + "</h1>"
    for recordFileName in records:
        # Add ID anchor
        recordsHtml += "<a id=\"" + utils.filenameToAnchorTagId(recordFileName) + "\"></a>"
        # Render the logbook entry
        recordsHtml += utils.renderMarkdown(records[recordFileName])
    prevLinkHtml = ""
    if "prevPage" in logbookPage:
        prevRecords = logbookPage["prevPage"]["records"]
        prevRecordsHtml = "<h1>Captain’s log<br />Dateline: " + formatLogbookPageDate(logbookPage["prevPage"]) + "</h1>"
        for recordFileName in prevRecords:
            prevRecordsHtml += utils.renderMarkdown(prevRecords[recordFileName])
        # Strip off all anchor tags
        prevRecordsHtml = re.sub('<(?:a[^>]*>|/a>)', '', prevRecordsHtml)
        prevLinkHtml = utils.renderTemplate(data["templates"]["link"], {
            "href": "./" + logbookPage["prevPage"]["year"] + "/" + logbookPage["prevPage"]["month"] + "/" + logbookPage["prevPage"]["day"] + "/",
            "class": "content",
            "content": prevRecordsHtml
        })
    html = utils.renderTemplate(data["templates"]["page"], {
        "title":       utils.generatePageTitle("Captain’s log, " + formattedDate, data),
        "description": "Captain’s log, " + formattedDate,
        "logo":        utils.renderTemplate(data["templates"]["link"], {
            "href": "..",
            "content": "Curious Cat",
        }),
        "navigation":  utils.generateNavigation(),
        "criticalcss": utils.compileSass(open("../src/styles/critical.scss", "r").read()),
        "css":         "../" + data["definitions"]["filenames"]["css"],
        "name":        "logbook",
        "content":     utils.renderTemplate(data["templates"]["logbook-page"], {
            "date": formattedDate,
            "prevLink": prevLinkHtml,
            "content": recordsHtml
        })
    })
    htmlFile = utils.mkfile(
        data["definitions"]["runtime"]["cwd"],
        data["config"]["Filesystem"]["DestinationDirPath"],
        data["config"]["Site"]["CaptainsLogPath"],
        data["definitions"]["filenames"]["index"]
    )
    htmlFile.write(html)
    htmlFile.close()
    ## Copy asset files
    if os.path.isdir(os.path.join(data["definitions"]["runtime"]["cwd"], "data", "logbook", logbookPage['year'], logbookPage['month'], logbookPage['day'], "assets")):
        utils.cpr(
            os.path.join(data["definitions"]["runtime"]["cwd"], "data", "logbook", logbookPage['year'], logbookPage['month'], logbookPage['day'], "assets"),
            os.path.join(data["definitions"]["runtime"]["cwd"], data["config"]["Filesystem"]["DestinationDirPath"], data["config"]["Site"]["CaptainsLogPath"], "assets")
        )
    ## Add latest logbook page link to sitemap
    if data["config"].getboolean("Site", "CreateSitemap", fallback=False):
        data["sitemap"].append("/" + data["config"]["Site"]["CaptainsLogPath"] + "/")
