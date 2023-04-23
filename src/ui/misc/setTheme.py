from PySide6.QtCore import QFile


def setTheme(app, theme):
    if theme != "<default>":
        file = QFile(":/themes/" + theme + ".qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            theme = file.readAll().data().decode()
            # print(theme)
            app.setStyleSheet(theme)
    else:
        app.setStyleSheet("")
