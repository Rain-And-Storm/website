## Compile Sass into CSS

import os

import webgen

def stage(data):
    css = ""
    ## Read and compile Sass
    for filename in os.listdir(os.path.join(data["definitions"]["runtime"]["cwd"], "src", "styles")):
        if filename.endswith(".scss") and not filename.startswith("_") and filename != "critical.scss":
            with open(os.path.join(data["definitions"]["runtime"]["cwd"], "src", "styles", filename), 'r') as file:
                css = css + webgen.compileSass(file.read())
    ## Write style file
    styleFile = webgen.mkfile(
        data["definitions"]["runtime"]["cwd"],
        data["config"]["Filesystem"]["DestinationDirPath"],
        data["config"]["Filesystem"]["StyleFile"]
    )
    styleFile.write(css)
    styleFile.close()
