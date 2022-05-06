## Responsible for creating CNAME file
## This file points GitHub pages website at custom domain

import webgen

def stage(data):
    fileHandle = webgen.mkfile(
        data["definitions"]["runtime"]["cwd"],
        data["config"]["Filesystem"]["DestinationDirPath"],
        "CNAME",
    )
    fileHandle.write("rainandstorm.com") # TODO: parse from config
    fileHandle.close()
