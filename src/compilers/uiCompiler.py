from .autoCompiler import compileAuto
from pathlib import Path


def compileUi():
    compileAuto(
        "uic", ["uic6", "uic", "pyside6-uic", "pyside2-uic"], "ui", "ui",
        Path("src/designer"), Path("src/generated")
    )
    compileAuto(
        "uic", ["uic6", "uic", "pyside6-uic", "pyside2-uic"], "ui", "ui",
        Path("src/designer/easyUI"), Path("src/generated"), Path("designer/easyUI")
    )
