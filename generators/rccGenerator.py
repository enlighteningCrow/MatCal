from os import walk


def regenerateRcc():
    fl = open("resources.qrc", 'w')
    prefix = """<RCC>
    <qresource prefix="/">
"""
    suffix = """
    </qresource>
</RCC>"""
    # <file > resources/themes/theme.qss < /file >
    # <file > resources/MatCalIcon.png < /file >
    contents = prefix
    for root, dirs, files in walk("resources"):
        if len(files):
            for i in files:
                contents += "<file>" + root + '/' + i + "</file>"
