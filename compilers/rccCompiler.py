from compilers.autoCompiler import compileAuto

from os import walk


def compileRcc():
    return compileAuto("rcc", ["rcc6", "rcc", "pyside6-rcc", "pyside2-rcc"], "qrc", "rcc")
