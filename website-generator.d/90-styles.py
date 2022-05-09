## Compile Sass into CSS

import utils

def stage(data):
    ## Write style file
    styleFile = utils.mkfile(
        data["definitions"]["runtime"]["cwd"],
        data["config"]["Filesystem"]["DestinationDirPath"],
        data["config"]["Filesystem"]["StyleFile"],
    )
    css = utils.compileSass(open("../src/styles/main.scss", "r").read())
    styleFile.write(css)
    styleFile.close()
