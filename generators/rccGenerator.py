# from os import walk
import logging
import os

from pathlib import Path
from utils.chdir import chdir


def regenerateRcc():
    fl = open("resources/resources.qrc", 'w')
    prefix = """<RCC>
    <qresource prefix="">
"""
    suffix = """    </qresource>
</RCC>"""
    # <file > resources/themes/theme.qss < /file >
    # <file > resources/MatCalIcon.png < /file >
    contents = prefix
    # os.curren
    with chdir("resources"):
        for root, dirs, files in os.walk("."):
            # print(root, dirs, files)
            if len(files):
                for i in files:
                    if not i.endswith(".qrc"):
                        contents += 8 * ' ' + "<file>" + \
                            (root + '/')[2:] + i + "</file>\n"
        contents += suffix
        logging.info("Regenerating resources.qrc contents:")
        logging.info(contents)
        fl.write(contents)
