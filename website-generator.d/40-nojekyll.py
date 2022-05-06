## Responsible for creating empty .nojekyll file
## This file tells GitHub pages to not treat this site as a Jekyll project

import utils

def stage(data):
    fileHandle = utils.mkfile(
        data["definitions"]["runtime"]["cwd"],
        data["config"]["Filesystem"]["DestinationDirPath"],
        ".nojekyll",
    )
    fileHandle.close()
