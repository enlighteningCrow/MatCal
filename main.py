#!/usr/bin/env python3

# This Python file uses the following encoding: utf-8

# failed = pip.main(["install", "PySide6", "torch", "torchvision", "torchaudio"])

from uiCompiler import compileUi

compileUi()

import sys
from PySide6.QtWidgets import QApplication

from MainWindow import MainWindow

#TODO: Make the program have an when run icon, and maybe packaging into executable
#TODO: Make a MatrixList model in MatrixListModel.py
#TODO: Make the matirxlist model capable of saving to/loading from files
#TODO: Make each of the separate matrices capable of saving to/loading from files

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