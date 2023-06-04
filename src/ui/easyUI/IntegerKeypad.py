from ui.easyUI.ButtonInputs import ButtonInputs
from PySide6.QtWidgets import QPushButton
from PySide6 import QtCore

class IntegerKeypad(ButtonInputs):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.allButtons = [None for i in range(10)]
        self.numberButtons = [None for i in range(10)]

        for i in range(1, 10):
            self.numberButtons[i] = QPushButton(str(i), self)
            self.allButtons[i] = self.numberButtons[i]
            self.gridLayout.addWidget(self.numberButtons[i], (i - 1) // 3, (i - 1) % 3)

        self.numberButtons[0] = QPushButton(str(0), self)
        self.allButtons[0] = self.numberButtons[0]
        self.gridLayout.addWidget(self.numberButtons[0], 3, 1)
        for i in range(len(self.numberButtons)):
            self.numberButtons[i].clicked.connect(self.Input((QtCore.QEvent.KeyPress, QtCore.Qt.Key_0 + i, QtCore.Qt.NoModifier, chr(ord('0') + i)), self.getLineInput()))

        self.buttonLeftCursor = QPushButton('<', self)
        self.buttonRightCursor = QPushButton('>', self)
        self.allButtons.append(self.buttonLeftCursor)
        self.allButtons.append(self.buttonRightCursor)

        self.buttonLeftCursor.clicked.connect(self.Input((QtCore.QEvent.KeyPress, QtCore.Qt.Key_Left, QtCore.Qt.NoModifier, 'Left'), self.getLineInput()))
        self.buttonRightCursor.clicked.connect(self.Input((QtCore.QEvent.KeyPress, QtCore.Qt.Key_Right, QtCore.Qt.NoModifier, 'Right'), self.getLineInput()))

        self.gridLayout.addWidget(self.buttonLeftCursor, 3, 0)
        self.gridLayout.addWidget(self.buttonRightCursor, 3, 2)

        self.backspaceButton = QPushButton("Backspace", self)
        self.allButtons.append(self.backspaceButton)

        self.backspaceButton.clicked.connect(self.Input((QtCore.QEvent.KeyPress, QtCore.Qt.Key_Backspace, QtCore.Qt.NoModifier, 'Backspace'), self.getLineInput()))

        self.gridLayout.addWidget(self.backspaceButton, 0, 3)

        self.onInitDone()
