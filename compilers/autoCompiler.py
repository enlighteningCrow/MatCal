import os
from pathlib import Path
import sys

from glob import glob
import PySide6
from PySide6.QtCore import QDirIterator

from shutil import which

import logging
from typing import List


def getExecutableVariants(name: str):
    return [name, name + ".exe", name + ".bat", name + ".sh", name + ".app"]


def createPath(path: Path):
    if not path.exists():
        # make that path if it does not exist
        for i in range(0, len(path.parts)):
            curPath = Path(*path.parts[0:i + 1])
            if not curPath.exists():
                curPath.mkdir()


def compileAuto(
    compilerName: str,
    compilerNamesFallback: List[str],
    filetype: str,
    resultPrefix: str,
    inputDir: str,
    outputDirPrefix: str = "generated",
    outputDirSuffix: str = ''
):
    compilerPrefixes = [
        Path(PySide6.__file__).parent / "Qt" / "libexec",
        Path(PySide6.__file__).parent,
        Path("/usr/lib/qt6")
    ]
    foundCompilerPath = None
    if not len(outputDirSuffix):
        outputDirSuffix = inputDir
    for prefix in compilerPrefixes:
        for pathCurrent in (
                prefix / i for i in getExecutableVariants(compilerName)):
            if not pathCurrent.exists():
                logging.debug(
                    f"{compilerName} executable not found at path: \"{pathCurrent}\""
                )
            else:
                foundCompilerPath = pathCurrent
                break
        if foundCompilerPath is not None:
            logging.info(
                f"{compilerName} executable found at path: \"{foundCompilerPath}\""
            )
            break
        # for i in glob("*.ui"):
        #     path = Path(i)
        #     logging.info(
        #         "Compiling " + str(path) + " to " +
        #         str(path.parent / ("ui_" + path.stem + ".py"))
        #     )
        #     os.system(
        #         str(uicPath) + " " + str(path) + " -g python -o " +
        #         str(path.parent / ("ui_" + path.stem + ".py"))
        #     )
        # return

    if foundCompilerPath is None:
        for name in compilerNamesFallback:
            for i in getExecutableVariants(name):
                a = which(i)
                if a is not None:
                    logging.info(
                        f"{compilerName} executable found in PATH: \"{a}\""
                    )
                    foundCompilerPath = Path(a)
                    break
    if foundCompilerPath is not None:
        for i in (file for file in os.listdir(inputDir)
                  if file.endswith('.' + filetype)):
            path = Path(i)
            createPath(path.parent/outputDirPrefix / outputDirSuffix)
            output = str(
                path.parent / outputDirPrefix / outputDirSuffix /
                (resultPrefix + "_" + path.stem + ".py")
            )
            logging.info(f"Compiling {inputDir / path} to {output}")
            # print(str(foundCompilerPath) + " " + str(inputDir / path) + " -g python -o " + output)
            os.system(
                # str(foundCompilerPath) + " " + str(inputDir / path) + " -g python -o " + output
                f"{foundCompilerPath} {inputDir / path} -g python -o {output}"
            )
        return
    logging.warning(f"{compilerName} executable not found in PATH")
    sys.exit(1)
