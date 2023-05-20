from pathlib import Path
from PySide6.QtCore import QDir

THEME_DIR = ":/themes/"


def getThemes():
    # return [QDir(themeDir).dirName() for themeDir in QDir(THEME_DIR).entryList(QDir.Dirs | QDir.NoDotAndDotDot)]
    # return QDir(THEME_DIR).entryList(QDir.NoDotAndDotDot)
    li = ["<default>"]
    li.extend(Path(i).stem for i in QDir(THEME_DIR).entryList())
    return li
