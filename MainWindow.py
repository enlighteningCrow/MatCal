#!/usr/bin/env python3

# This Python file uses the following encoding: utf-8

import pip

# failed = pip.main(["install", "PySide6", "torch", "torchvision", "torchaudio"])

from uiCompiler import compileUi

compileUi()

import os
from pathlib import Path
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from ui_MainWindow import Ui_MainWindow

from PySide6.QtGui import QStandardItem, QStandardItemModel

import logging


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        # self.setupUi(self)
        self.matrixList = QStandardItemModel()
        self.__ui.listView.setModel(self.matrixList)
        for i in [QStandardItem("ajsio"), QStandardItem("bsdf09h"),
                  QStandardItem("cjoasidg0")]:
            self.matrixList.appendRow(i)
        # self.


#TODO: (PRIORITY): Try removing the current MatrixEditor.py altogether,
# and replace it with the current MatrixEditor.py. Also consider making
# the matrix editor only pop up when the list is clicked, such that the user
# makes an action to modify an existing matrix in the list or create a new one.

if __name__ == "__main__":
    # logging.getLogger().setLevel(logging.DEBUG)
    app = QApplication(sys.argv)
    # loader = QUiLoader()
    # uicPath = Path(__file__).resolve().parent / "MainWindow.ui"
    # ui_file = QFile(uicPath)
    # ui_file.open(QFile.ReadOnly)
    # widget = loader.load(ui_file)
    editor = MainWindow()
    editor.show()
    # widget.show()
    # deditor = MatrixEditor()
    # deditor.show()
    sys.exit(app.exec())
