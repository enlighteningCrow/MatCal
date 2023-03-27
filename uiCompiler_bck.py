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
        Path(PySide6.__file__).parent / "uic.exe"
    ]
    for uicPath in uicPaths:
        if not uicPath.exists():
            print("uic executable not found at path: \"" + str(uicPath))
            continue
        print("uic executable exists at path: \"" + str(uicPath))
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
    
    a = which("uic")
    if len(a) > 0:
        print("uic executable found in PATH: \"" + str(a))
        for i in glob("*.ui"):
            path = Path(i)
            print(
                "Compiling " + str(path) + " to " +
                str(path.parent / ("ui_" + path.stem + ".py"))
            )
            os.system(
                "uic " + str(path) + " -g python -o " +
                str(path.parent / ("ui_" + path.stem + ".py"))
            )
        return
    a = which("uic.exe")
    if len(a) > 0:
        print("uic executable found in PATH: \"" + str(a))
        for i in glob("*.ui"):
            path = Path(i)
            print(
                "Compiling " + str(path) + " to " +
                str(path.parent / ("ui_" + path.stem + ".py"))
            )
            os.system(
                "uic " + str(path) + " -g python -o " +
                str(path.parent / ("ui_" + path.stem + ".py"))
            )
        return
    print("uic executable not found in PATH")
    sys.exit(1)
