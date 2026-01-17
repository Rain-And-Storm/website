## Responsible for creating Curious Cat's main page’s HTML file

import webgen

def stage(data):
    useRelativePaths = data["config"].getboolean("Site", "UseRelativePaths", fallback=None)
    navigationLinks = webgen.generateNavigationLinks(data["definitions"]["runtime"]["navigation"], "/curious-cat/", relative=useRelativePaths)

    html = webgen.renderTemplate(data["templates"]["page"], {
        "title":       webgen.getWebPageTitle(data["config"]["Site"]["Name"], ["Curious Cat"]),
        "description": "You wouldn't download a boat",
        "navigation":  webgen.renderTreeNavigation(navigationLinks, data["templates"]["nav"]) +
            webgen.renderTreeNavigationScript(navigationLinks, "/curious-cat/"),
        "criticalcss": webgen.compileSass(open("../src/styles/critical.scss", "r").read()),
        "css":         webgen.buildPath("/" + data["definitions"]["filenames"]["css"], "/curious-cat/", relative=useRelativePaths),
        # "style":       '''
        # ''',
        "class":        "curious-cat main content",
        "content":     webgen.renderMarkdown(open("../data/curious-cat/main.md", "r").read()),
    })
    htmlFile = webgen.mkfile(
        data["definitions"]["runtime"]["cwd"],
        data["config"]["Filesystem"]["DestinationDirPath"],
        "curious-cat",
        data["definitions"]["filenames"]["index"]
    )
    # Curious comments (TODO: move into scripts.js)
    array = []
    with open("../data/curious-cat/faq.txt", "r") as file:
        for line in file:
            if len(line) > 0:
                array.append(line)
    html += '''<canvas id=\"curious-comments\"></canvas><script>
window.onload = function(argument) {

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

    ## Add home page link to sitemap
    if data["config"].getboolean("Site", "CreateSitemap", fallback=False):
        data["sitemap"].append("/curious-cat/")
