#!/usr/bin/env python3

# This Python file uses the following encoding: utf-8

if True:
    from moduleChecker import checkModules
    checkModules()

    from MainWindow import MainWindow
    from PySide6.QtWidgets import QApplication
    import sys

    from compilers.uiCompiler import compileUi
    compileUi()
    from generators.rccGenerator import regenerateRcc
    regenerateRcc()
    from compilers.rccCompiler import compileRcc
    compileRcc()

    import rcc_themes


# TODO: Make the program have an when run icon, and maybe packaging into executable
# TODO: Make a MatrixList model in MatrixListModel.py
# TODO: Make the matirxlist model capable of saving to/loading from files
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
    with open("themes/theme.qss", 'r') as file:
        theme = file.read()
        app.setStyleSheet(theme)
    editor = MainWindow()
    editor.show()
    # widget.show()
    # deditor = MatrixEditor()
    # deditor.show()
    sys.exit(app.exec())

# TODO: Separate components into modules
