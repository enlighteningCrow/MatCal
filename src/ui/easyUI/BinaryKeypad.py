from ui.easyUI.ButtonInputs import ButtonInputs
from PySide6.QtWidgets import QPushButton
from PySide6 import QtCore

class BinaryKeypad(ButtonInputs):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.allButtons = [None for i in range(2)]
        self.numberButtons = [None for i in range(2)]

        for i in range(2):
            self.numberButtons[i] = QPushButton(str(i), self)
            self.allButtons[i] = self.numberButtons[i]
            self.gridLayout.addWidget(self.numberButtons[i], 0, i)

        for i in range(len(self.numberButtons)):
            self.numberButtons[i].clicked.connect(self.Input((QtCore.QEvent.KeyPress, QtCore.Qt.Key_0 + i, QtCore.Qt.NoModifier, chr(ord('0') + i)), self.getLineInput()))

        self.buttonLeftCursor = QPushButton('<', self)
        self.buttonRightCursor = QPushButton('>', self)
        self.allButtons.append(self.buttonLeftCursor)
        self.allButtons.append(self.buttonRightCursor)

        self.buttonLeftCursor.clicked.connect(self.Input((QtCore.QEvent.KeyPress, QtCore.Qt.Key_Left, QtCore.Qt.NoModifier, 'Left'), self.getLineInput()))
        self.buttonRightCursor.clicked.connect(self.Input((QtCore.QEvent.KeyPress, QtCore.Qt.Key_Right, QtCore.Qt.NoModifier, 'Right'), self.getLineInput()))

        self.gridLayout.addWidget(self.buttonLeftCursor, 1, 0)
        self.gridLayout.addWidget(self.buttonRightCursor, 1, 1)

        self.backspaceButton = QPushButton("Backspace", self)
        self.allButtons.append(self.backspaceButton)

        self.backspaceButton.clicked.connect(self.Input((QtCore.QEvent.KeyPress, QtCore.Qt.Key_Backspace, QtCore.Qt.NoModifier, 'Backspace'), self.getLineInput()))

        self.gridLayout.addWidget(self.backspaceButton, 0, 2)

        self.onInitDone()
