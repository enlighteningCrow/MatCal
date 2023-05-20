from src.compilers.autoCompiler import compileAuto


def compileUi():
    return compileAuto("uic", ["uic6", "uic", "pyside6-uic", "pyside2-uic"], "ui", "ui", "designer")
