import torch

from PySide6.QtWidgets import QWidget, QStackedLayout

from ui.easyUI.OutputDelegate import OutputDelegate

from typing import Optional

# Cannot inherit from ABC as that will conflict with QT internal implementation
class OutputWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.sl = QStackedLayout()
        for i in OutputDelegate.__subclasses__():
            self.sl.addWidget(i())

        self.setLayout(self.sl)
        self.data = None

    def showData(self, data, dataType : Optional[str] = None):
        self.data = data
        if dataType is None:
            dataType = type(data).__name__

        for i in range(self.sl.count()):
            if dataType in type(self.sl.widget(i)).displayTypes():
                self.sl.setCurrentIndex(i)
                self.sl.widget(i).showData(data)
                return

    def getData(self):
        return self.data