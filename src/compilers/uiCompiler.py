from .autoCompiler import compileAuto
from pathlib import Path


def compileUi():
    return compileAuto(
        "uic", ["uic6", "uic", "pyside6-uic", "pyside2-uic"], "ui", "ui",
        Path("src/designer"), Path("src/generated")
    )
