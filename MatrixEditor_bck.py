# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from DimensionEditor import DimensionEditor
from ui_MatrixEditor import MatrixEditor


class MatrixEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = Path(__file__).resolve().parent / "MatrixEditor.ui"
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        # self.ui = loader.load(ui_file, self)
        self.ui = MatrixEditor()
        print(type(self.ui.widget))
        ui_file.close()

