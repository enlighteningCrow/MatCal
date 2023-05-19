from os import walk
import logging
from typing import List

import json

from pathlib import Path


def isProjectFile(filename: Path) -> bool:
    return filename.suffix in [".py", ".ui", ".qss", ".qrc"]


def regenerateProject():
    fl = open("MatCal.pyproject", 'w')
    filesList: List[str] = ["main.py"]
    for dir in ["compilers", "designer", "generators", "resources", "src",
                "utils"]:
        for root, dirs, files in walk(dir):
            if len(files):
                for i in files:
                    if isProjectFile(Path(i)):
                        filesList.append(root + '/' + i)
    contents = json.dumps({"files": filesList})
    # print(filesList)
    # print(contents)
    # print(logging.getLogger())
    logging.info(f"Regenerating project contents: {contents}")
    fl.write(contents)
