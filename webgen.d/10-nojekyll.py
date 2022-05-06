## Responsible for creating empty .nojekyll file
## This file tells GitHub pages to not treat this site as a Jekyll project

import webgen

def stage(data):
    fileHandle = webgen.mkfile(
        data["definitions"]["runtime"]["cwd"],
        data["config"]["Filesystem"]["DestinationDirPath"],
        ".nojekyll",
    )
    fileHandle.close()
