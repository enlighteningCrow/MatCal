from PySide6.QtCore import QFile


def setTheme(app, settings):
    if settings.value("theme") != "<default>":
        file = QFile(":/themes/" + settings.value("theme") + ".qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            theme = file.readAll().data().decode()
            # print(theme)
            app.setStyleSheet(theme)
