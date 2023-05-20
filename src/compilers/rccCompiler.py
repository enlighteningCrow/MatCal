from src.compilers.autoCompiler import compileAuto


def compileRcc():
    return compileAuto(
        "rcc", ["rcc6", "rcc", "pyside6-rcc", "pyside2-rcc"], "qrc", "rcc",
        "resources"
    )
