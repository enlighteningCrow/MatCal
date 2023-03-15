# This Python file uses the following encoding: utf-8

from uiCompiler import compileUi
compileUi()
import os
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from DimensionEditor import DimensionEditor
from MatrixEditor import MatrixEditor


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loader = QUiLoader()
    path = Path(__file__).resolve().parent / "MainWindow.ui"
    ui_file = QFile(path)
    ui_file.open(QFile.ReadOnly)
    widget = loader.load(ui_file)
    editor = MatrixEditor()
    editor.show()
    # widget.show()
    # deditor = DimensionEditor()
    # deditor.show()
    sys.exit(app.exec())
