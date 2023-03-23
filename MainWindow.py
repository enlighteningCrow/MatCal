# This Python file uses the following encoding: utf-8

from ui_MainWindow import Ui_MainWindow
from MatrixEditor import MatrixEditor
from DimensionEditor import DimensionEditor
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
import sys
from pathlib import Path
import os
import pip

# failed = pip.main(["install", "PySide6", "torch", "torchvision", "torchaudio"])

from uiCompiler import compileUi

compileUi()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loader = QUiLoader()
    path = Path(__file__).resolve().parent / "MainWindow.ui"
    ui_file = QFile(path)
    ui_file.open(QFile.ReadOnly)
    widget = loader.load(ui_file)
    editor = MainWindow()
    editor.show()
    # widget.show()
    # deditor = DimensionEditor()
    # deditor.show()
    sys.exit(app.exec())
