from .autoCompiler import compileAuto

from pathlib import Path


def compileRcc():
    return compileAuto(
        "rcc", ["rcc6", "rcc", "pyside6-rcc", "pyside2-rcc"], "qrc", "rcc",
        Path("resources"), Path("src/generated")
    )
