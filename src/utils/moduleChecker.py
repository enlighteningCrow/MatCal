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
    packagesList = {"PySide6", "torch", "torchvision", "BTrees", "ZODB"}
    diff = packagesList.difference(pkgs)
    if len(diff):
        logging.info(f"Missing packages: {diff}")
        accept = input(
            "Missing packages: " + str(diff) +
            ". Install automatically? (y/n): "
        )
        if accept == "y":
            special_inst = {"torch", "torchvision", "torchaudio"}
            targets = [i for i in diff if i not in special_inst]
            if len(targets):
                pip.main(["install", *targets])
            if len(special_inst.union(diff)):
                # packagesMissingNatural = joinNatural(
                #     *
                # )
                packagesMissing = {i for i in diff if i in special_inst}
                if len(packagesMissing):
                    print(
                        f"Cannot install the following packages automatically: {packagesMissing}. Please install them manually according to this web: https://pytorch.org"
                    )
                    sys.exit(1)
                    # if os.name in ("posix", "nt"):
                    #         pip.main(
                    #             ["install", *[i for i in diff if i in ("torch", "torchvision", "torchaudio")], " --index-url", "https://download.pytorch.org/whl/cu118"])
                    # pip.main(
                    #     ["install", *[i for i in diff if i not in ("torch", "torchvision", "torchaudio")]])
        elif accept == "n":
            print("Please install the missing packages before running MatCal.")
            sys.exit(1)
        else:
            print(
                "Invalid input. Please run install the missing packages before running MatCal."
            )
            sys.exit(1)
