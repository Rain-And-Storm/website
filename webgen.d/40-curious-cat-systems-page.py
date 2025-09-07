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
    useRelativePaths = data["config"].getboolean("Site", "UseRelativePaths", fallback=None)
    navigationLinks = webgen.generateNavigationLinks(data["definitions"]["runtime"]["navigation"], "/curious-cat/systems/", relative=useRelativePaths)

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
        "title":       webgen.getWebPageTitle(data["config"]["Site"]["Name"], ["Curious Cat", "Systems"]),
        "description": "Detailed description of various systems installed aboard Curious Cat",
        "navigation":  webgen.renderTreeNavigation(navigationLinks, data["templates"]["nav"]) +
            webgen.renderTreeNavigationScript(navigationLinks, "/curious-cat/systems/"),
        "criticalcss": webgen.compileSass(open("../src/styles/critical.scss", "r").read()),
        "css":         webgen.buildPath("/" + data["definitions"]["filenames"]["css"], "/curious-cat/systems/", relative=useRelativePaths),
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
    # Curious comments (TODO: move into scripts.js)
    array = []
    with open("../data/curious-cat/faq.txt", "r") as file:
        for line in file:
            if len(line) > 0:
                array.append(line)
    html += '''<canvas id=\"curious-comments\"></canvas><script>
{

	var lyric = [''' + str.join(",", map(lambda line: "\"" + line.strip() + "\"", array)) + '''];
	var words = {};
	var words_attr = [];
	string_handle(lyric);

	var canvas = document.getElementById('curious-comments');
	canvas.width = window.innerWidth;
	canvas.height = window.innerHeight;

	if (canvas.getContext) {
		var c = canvas.getContext('2d'),
			w = canvas.width,
			h = canvas.height;

		c.strokeStyle = 'red';
		c.fillStyle = 'rgba(125, 125, 125, 0.5)';
		c.lineWidth = 5;

		// constructor
		Word = function(key) {
			this.text = key;
			this.x = Math.random() * w;
			this.y = Math.random() * h;
			this.font = (words[key] * 10) + 'px Arial'
			this.speed = words[key];
			this.speed += Math.random() * (1 - 0.01) + 0.01;
		}
		for (key in words) {
			words_attr.push(new Word(key));
		}
		console.log(words_attr.length);

		function animation() {
			for (var i = 0; i < words_attr.length; i++) {
				c.font = words_attr[i].font;
				c.fillText(words_attr[i].text, words_attr[i].x, words_attr[i].y);
				words_attr[i].width = c.measureText(words_attr[i].text).width;
				c.stroke();
			}
			move();
		}

		function move() {
			for (var i = 0; i < words_attr.length; i++) {
				if (words_attr[i].x > w) {
					words_attr[i].x = -words_attr[i].width;
					words_attr[i].y = Math.random()*h;
				} else {
					words_attr[i].x += words_attr[i].speed;
				}
			}
		}

		setInterval(function() {
			c.clearRect(0, 0, w, h);
			animation();
		}, 24);
	}

	function string_handle(str) {
		var word_array = [];
		var word_count = [];
		for (var i = 0; i < str.length; i++) {
			check = true;
			for (var j = 0; j <= word_array.length; j++) {
				if (str[i] == word_array[j]) {
					word_count[j]++;
					check = false;
					break;
				}
			}
			if (check) {
				word_array.push(str[i]);
				word_count.push(1);
			}
		}
		for (var i = 0; i < word_array.length; i++) {
			words[word_array[i]] = word_count[i];
		}
		return words;
	}

}
</script>'''
    htmlFile.write(html)
    htmlFile.close()

    ## Add systems page link to sitemap
    if data["config"].getboolean("Site", "CreateSitemap", fallback=False):
        data["sitemap"].append("/curious-cat/systems/")
