from typing import Optional
import PySide6.QtCore
from PySide6.QtWidgets import QWidget, QStackedLayout

from ui.easyUI.InputDelegate import InputDelegate

# Cannot inherit from ABC as that will conflict with QT internal implementation
class InputWidget(QWidget):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.sl = QStackedLayout()
        for i in InputDelegate.__subclasses__():
            self.sl.addWidget(i())

        self.setLayout(self.sl)

    def getData(self):
        return self.sl.currentWidget().getData()

    def loadData(self, data):
        self.sl.currentWidget().loadData(data)

    def promptData(self, promptType : str):
        for i in range(self.sl.count()):
            if promptType in type(self.sl.widget(i)).promptTypes():
                self.sl.setCurrentIndex(i)
                return

