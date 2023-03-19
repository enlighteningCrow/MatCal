# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from DimensionEditor import DimensionEditor
from ui_MatrixEditor import Ui_Form


class MatrixEditor(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        # loader = QUiLoader()
        # path = Path(__file__).resolve().parent / "MatrixEditor.ui"
        # ui_file = QFile(path)
        # ui_file.open(QFile.ReadOnly)
        # widget = loader.load(ui_file)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
