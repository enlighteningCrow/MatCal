import os
from pathlib import Path
import sys

from glob import glob
import PySide6
from PySide6.QtCore import QDirIterator

from shutil import which


def compileUi():
    uicPaths = [
        Path(PySide6.__file__).parent / "Qt" / "libexec" / "uic",
        Path(PySide6.__file__).parent / "uic.exe",
        Path("/usr/lib/qt6/uic")
    ]
    uicPath = None
    for uicPathCurrent in uicPaths:
        if not uicPathCurrent.exists():
            print("uic executable not found at path: \"" + str(uicPathCurrent))
            continue
        print("uic executable found at path: \"" + str(uicPathCurrent))
        uicPath = uicPathCurrent
        break
        # for i in glob("*.ui"):
        #     path = Path(i)
        #     print(
        #         "Compiling " + str(path) + " to " +
        #         str(path.parent / ("ui_" + path.stem + ".py"))
        #     )
        #     os.system(
        #         str(uicPath) + " " + str(path) + " -g python -o " +
        #         str(path.parent / ("ui_" + path.stem + ".py"))
        #     )
        # return

    uicPaths = ["uic6", "uic6.exe", "uic", "uic.exe"]
    if uicPath is None:
        for i in uicPaths:
            a = which(i)
            if a is not None:
                print("uic executable found in PATH: \"" + str(a))
                uicPath = Path(a)
                break
    if uicPath is not None:
        for i in glob("*.ui"):
            path = Path(i)
            print(
                "Compiling " + str(path) + " to " +
                str(path.parent / ("ui_" + path.stem + ".py"))
            )
            os.system(
                str(uicPath) + " " + str(path) + " -g python -o " +
                str(path.parent / ("ui_" + path.stem + ".py"))
            )
        return
    print("uic executable not found in PATH")
    sys.exit(1)
