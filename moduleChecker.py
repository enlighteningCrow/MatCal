# failed = pip.main()

import logging
import pip
import pkg_resources as pkg

import sys

# print([i for i in pkg.working_set])
# print(pkg.working_set.__iter__())

# for i in pkg.working_set:
#     print(i.project_name)


def checkModules():
    pkgs = set(i.project_name for i in pkg.working_set)
    packagesList = {"PySide6", "torch", "torchvision", "torchaudio"}
    diff = packagesList.difference(pkgs)
    if len(diff):
        logging.info("Missing packages:", diff)
        accept = input("Missing packages: " + str(diff) +
                       ". Install automatically? (y/n): ")
        if accept == "y":
            pip.main(["install", *diff])
        elif accept == "n":
            print("Please install the missing packages before running MatCal.")
            sys.exit(1)
        else:
            print(
                "Invalid input. Please run install the missing packages before running MatCal.")
            sys.exit(1)
