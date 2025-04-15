## Copies favicon.ico over

import os
import shutil

def stage(data):
    sourcePath = os.path.join(
        data["definitions"]["runtime"]["cwd"],
        "data",
        "assets",
        "favicon.ico",
    )
    destinationPath = os.path.join(
        data["definitions"]["runtime"]["cwd"],
        data["config"]["Filesystem"]["DestinationDirPath"],
    )
    if os.path.isfile(sourcePath):
        shutil.copy(sourcePath, destinationPath)
