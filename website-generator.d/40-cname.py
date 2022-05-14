## Responsible for creating CNAME file
## This file points GitHub pages website at custom domain

import utils

def stage(data):
    fileHandle = utils.mkfile(
        data["definitions"]["runtime"]["cwd"],
        data["config"]["Filesystem"]["DestinationDirPath"],
        "CNAME",
    )
    fileHandle.write("svcuriouscat.com") # TODO: parse from config
    fileHandle.close()
