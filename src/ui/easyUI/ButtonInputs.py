from typing import Any, Optional
import PySide6.QtCore
# from generated.designer.ui_ButtonInputs import Ui_Form

from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QLineEdit, QApplication

from PySide6.QtCore import QPropertyAnimation

from PySide6 import QtCore, QtGui

from typing import List

# from ui.easyUI.AllInOneCalculator import AllInOneCalculator

# class inputActivated()

class ButtonInputs(QWidget):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)

        self.gridLayout = QGridLayout(self)
        self.setLayout(self.gridLayout)
        self.allButtons = None
        self.inputLine = None

        self.numberButtons : List[Optional[QPushButton]] = None

        # self.inputLine = QLineEdit(self)


    def onInitDone(self):

        for i in self.allButtons:
            i.setFocusPolicy(QtCore.Qt.FocusPolicy(QtCore.Qt.NoFocus))

        # gridLayout.addWidget(self.inputLine, 4, 0, 1, 3)


    #TODO: Set the self.inputLine to external later, while removing the line to construct it above.
    def getLineInput(self) -> QLineEdit:
        return self.inputLine

    def setInputLine(self, inputLine):
        self.inputLine = inputLine
        
        # self.__ui = Ui_Form()
        # self.__ui.setupUi(self)

    # class Input:
    #     def getEvent()
    class Input:
        def __init__(self, eventArguments, outerClass : 'ButtonInputs') -> None:
            # self.number = number
            self.__outerClass = outerClass
            # self.eventFactory = eventFactory
            # self.getEvent = eventFactory
            self.__eventArguments = eventArguments

        def getEvent(self):
            return QtGui.QKeyEvent(*self.__eventArguments)

        # def getEvent(self):
        #     return QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_0 + self.number, QtCore.Qt.NoModifier, chr(ord('0') + self.number))

        def __call__(self, outerClass : Optional['ButtonInputs'] = None) -> Any:
            if outerClass is None:
                outerClass = self.__outerClass
            QtCore.QCoreApplication.postEvent(outerClass, self.getEvent())

    # def addInput(self, number : int):
    #     assert(0 <= number < 10)
    #     # self.__ui.lineEdit.
    #     for 
    #     QtCore.QCoreApplication.postEvent(self.__ui.lineEdit, )

    def aHide(self):
        a = QPropertyAnimation(self, b"maximumHeight")
        # a = QPropertyAnimation(self, b"height")
        # a = QPropertyAnimation(self)
        # a.setProperty()
        a.setDuration(1000)
        # a.setStartValue(self.maximumHeight())
        a.setStartValue(10000)
        # a.setStartValue(self.height())
        a.setEndValue(0)

        # a.setDuration

        a.start()
        # l = QLineEdit()
        # l.maxim
        # self.setMaximumHeight(100)

    def aShow(self):
        a = QPropertyAnimation(self, b"maximumHeight")
        # a = QPropertyAnimation(self, b"height")
        a.setDuration(1000)
        # a.setStartValue(self.maximumHeight())
        a.setStartValue(0)
        # a.setStartValue(self.height())
        a.setEndValue(10000)

        a.start()
        # self.setMaximumHeight(1000)

