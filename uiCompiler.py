import os
from pathlib import Path
import sys

from glob import glob
import PySide6


def compileUi():
    uicPath = Path(PySide6.__file__).parent / "Qt" / "libexec" / "uic"
    if not uicPath.exists():
        print("uic executable not found at path: \"" + str(uicPath))
        sys.exit(1)
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
