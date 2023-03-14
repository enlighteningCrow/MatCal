import os
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from glob import glob

app = QApplication(sys.argv)
loader = QUiLoader()
for i in glob("*.ui"):
    path = Path(i).resolve()
    file = QFile(path)
    file.open(QFile.ReadOnly)
    w = loader.load(file)
    w.show()
    sys.exit(app.exec())
    # print(path)