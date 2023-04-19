#!/usr/bin/env python3

# This Python file uses the following encoding: utf-8

if True:
    from utils.moduleChecker import checkModules
    checkModules()

    from compilers.uiCompiler import compileUi
    compileUi()
    from generators import themeGenerator
    from generators.rccGenerator import regenerateRcc
    regenerateRcc()
    from compilers.rccCompiler import compileRcc
    compileRcc()
    from generators.projectGenerator import regenerateProject
    regenerateProject()

    from src.ui.MainWindow import MainWindow
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QFile, QSettings
    from PySide6.QtGui import QPixmap
    import sys
    from generated.resources import rcc_resources
    from src.ui.settings import settingEntries
    from src.ui.misc.setTheme import setTheme

# TODO: Make the program have an when run icon, and maybe packaging into executable
# TODO: Make a MatrixList model in MatrixListModel.py
# TODO: Make the matrixlist model capable of saving to/loading from files
# TODO: Make each of the separate matrices capable of saving to/loading from files

# TODO: Make the widget to allow the users to make their own operations, maybe 1 for making more permanent scripts and 1 as a mini-interpreter

if __name__ == "__main__":
    # logging.getLogger().setLevel(logging.DEBUG)
    app = QApplication(sys.argv)
    # loader = QUiLoader()
    # uicPath = Path(__file__).resolve().parent / "MainWindow.ui"
    # ui_file = QFile(uicPath)
    # ui_file.open(QFile.ReadOnly)
    # widget = loader.load(ui_file)
    settings = QSettings()
    for i, j in settingEntries:
        if not settings.contains(i):
            settings.setValue(i, j)
    setTheme(app, settings)
    editor = MainWindow()
    editor.show()
    # widget.show()
    # deditor = MatrixEditor()
    # deditor.show()
    sys.exit(app.exec())

# TODO: Separate components into modules
