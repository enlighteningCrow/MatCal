#!/usr/bin/env python3

# This Python file uses the following encoding: utf-8

if True:
    from src.utils.moduleChecker import checkModules
    checkModules()

    from src.compilers.uiCompiler import compileUi
    compileUi()
    # regenerateRcc()
    # compileRcc()
    from src.generators.projectGenerator import regenerateProject
    regenerateProject()

    from src.ui.MainWindow import MainWindow
    from PySide6.QtWidgets import QApplication
    import sys
    from src.db.settings import settingEntries
    from src.ui.misc.setTheme import setTheme
    from src.db.GlobalSettings import settings, gsettings

    from src.db.Storage import onExit

    import logging

# TODO: Make the program have an when run icon, and maybe packaging into executable
# TODO: Make a MatrixList model in MatrixListModel.py
# TODO: Make the matrixlist model capable of saving to/loading from files
# TODO: Make each of the separate matrices capable of saving to/loading from files

# TODO: Make the widget to allow the users to make their own operations, maybe 1 for making more permanent scripts and 1 as a mini-interpreter

# TODO: (PRIORITY) Consider moving everything source-related to src (except ignored and resources)
# TODO: (PRIORITY) Consider rebranding this to a Tensor Calculator instead of Matrix Calculator

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.WARN)
    app = QApplication(sys.argv)
    # loader = QUiLoader()
    # uicPath = Path(__file__).resolve().parent / "MainWindow.ui"
    # ui_file = QFile(uicPath)
    # ui_file.open(QFile.ReadOnly)
    # widget = loader.load(ui_file)
    # settings = QSettings()
    # gsettings().clear()
    for i, j in settingEntries.items():
        if not gsettings().contains(i):
            settings(i).set(j)
    theme = settings("theme")
    theme.valueChanged.connect(lambda x: setTheme(app, x))
    theme.update()
    mainWindow = MainWindow()
    mainWindow.show()
    # widget.show()
    # deditor = MatrixEditor()
    # deditor.show()
    exitCode = app.exec()
    onExit()
    sys.exit(exitCode)

# TODO: Separate components into modules

# TODO: Check why the themes (qss) still regenerate despite commenting out

# TODO: (PROCEDURE) Make the main window show a stackwidget first to let the user enter the logging in screen.
# Store the account details (username, password (hashed), account type) into the ZODB.
# Then make the user authenticate and select from the account type which

# --Fix the auto compiler to look at the correct location
#TODO: Move the main.py into the src directory