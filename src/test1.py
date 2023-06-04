from typing import Any, Optional
import PySide6.QtCore
# from generated.designer.ui_ButtonInputs import Ui_Form

from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QLineEdit, QApplication

from PySide6 import QtCore, QtGui

from typing import List

# class inputActivated()

class ButtonInputs(QWidget):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)

        gridLayout = QGridLayout(self)
        self.setLayout(gridLayout)
        self.numberButtons : List[Optional[QPushButton]] = [None for i in range(10)]
        self.allButtons = [None for i in range(12)]

        self.inputLine = QLineEdit(self)

        for i in range(1, 10):
            self.numberButtons[i] = QPushButton(str(i), self)
            self.allButtons[i] = self.numberButtons[i]
            gridLayout.addWidget(self.numberButtons[i], (i - 1) // 3, (i - 1) % 3)

        self.numberButtons[0] = QPushButton(str(0), self)
        self.allButtons[0] = self.numberButtons[0]
        gridLayout.addWidget(self.numberButtons[0], 3, 1)
        for i in range(len(self.numberButtons)):
            self.numberButtons[i].clicked.connect(self.Input((QtCore.QEvent.KeyPress, QtCore.Qt.Key_0 + i, QtCore.Qt.NoModifier, chr(ord('0') + i)), self.getLineInput()))

        self.buttonLeftCursor = QPushButton('<', self)
        self.buttonRightCursor = QPushButton('>', self)
        self.allButtons[10] = self.buttonLeftCursor
        self.allButtons[11] = self.buttonRightCursor

        self.buttonLeftCursor.clicked.connect(self.Input((QtCore.QEvent.KeyPress, QtCore.Qt.Key_Left, QtCore.Qt.NoModifier, 'Left'), self.getLineInput()))
        self.buttonRightCursor.clicked.connect(self.Input((QtCore.QEvent.KeyPress, QtCore.Qt.Key_Right, QtCore.Qt.NoModifier, 'Right'), self.getLineInput()))

        for i in self.allButtons:
            i.setFocusPolicy(QtCore.Qt.FocusPolicy(QtCore.Qt.NoFocus))

        gridLayout.addWidget(self.buttonLeftCursor, 3, 0)
        gridLayout.addWidget(self.buttonRightCursor, 3, 2)

        gridLayout.addWidget(self.inputLine, 4, 0, 1, 3)


    #TODO: Set the self.inputLine to external later, while removing the line to construct it above.
    def getLineInput(self):
        return self.inputLine

        
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

if __name__ == '__main__':
    a = QApplication()
    bi = ButtonInputs()
    bi.show()
    a.exec()