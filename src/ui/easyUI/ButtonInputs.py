from typing import Any, Optional
import PySide6.QtCore

from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QLineEdit, QApplication

from PySide6.QtCore import QPropertyAnimation

from PySide6 import QtCore, QtGui

from typing import List

class ButtonInputs(QWidget):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)

        self.gridLayout = QGridLayout(self)
        self.setLayout(self.gridLayout)
        self.allButtons = None
        self.inputLine = None

        self.numberButtons : List[Optional[QPushButton]] = None


    def onInitDone(self):

        for i in self.allButtons:
            i.setFocusPolicy(QtCore.Qt.FocusPolicy(QtCore.Qt.NoFocus))


    def getLineInput(self) -> QLineEdit:
        return self.inputLine

    def setInputLine(self, inputLine):
        self.inputLine = inputLine
        
    class Input:
        def __init__(self, eventArguments, outerClass : 'ButtonInputs') -> None:
            self.__outerClass = outerClass
            self.__eventArguments = eventArguments

        def getEvent(self):
            return QtGui.QKeyEvent(*self.__eventArguments)

        def __call__(self, outerClass : Optional['ButtonInputs'] = None) -> Any:
            if outerClass is None:
                outerClass = self.__outerClass
            QtCore.QCoreApplication.postEvent(outerClass, self.getEvent())

    def aHide(self):
        a = QPropertyAnimation(self, b"maximumHeight")
        a.setDuration(1000)
        a.setStartValue(10000)
        a.setEndValue(0)
        a.start()

    def aShow(self):
        a = QPropertyAnimation(self, b"maximumHeight")
        a.setDuration(1000)
        a.setStartValue(0)
        a.setEndValue(10000)
        a.start()

