from PySide6.QtWidgets import QWidget

from typing import Tuple

from generated.designer.easyUI.ui_MatrixEditor import Ui_Form

from ui.CommWidg import CommWidgPersistent

from types import SimpleNamespace

import torch

class MatrixEditor(QWidget, CommWidgPersistent):
    def __init__(self, parent = None):
        QWidget.__init__(self)
        self.__ui = Ui_Form()
        self.__ui.setupUi(self)
        print(type(self.__ui.frameEditor))
        self.__ui.frameEditor.updateMatrix(torch.empty((0, 0)))

    def increaseRows(self):
        print("increaseRows")
        newMatrix = torch.cat((self.__ui.frameEditor.getMatrix(), torch.zeros((1, self.__ui.frameEditor.getMatrix().shape[1]))))
        self.__ui.frameEditor.updateMatrix(newMatrix)

    def increaseColumns(self):
        print("increaseColumns")
        newMatrix = torch.cat((self.__ui.frameEditor.getMatrix(), torch.zeros((self.__ui.frameEditor.getMatrix().shape[0], 1))), dim = 1)
        self.__ui.frameEditor.updateMatrix(newMatrix)

    def decreaseRows(self):
        print("decreaseRows")
        newMatrix = self.__ui.frameEditor.getMatrix()[:-1, :]
        self.__ui.frameEditor.updateMatrix(newMatrix)

    def decreaseColumns(self):
        print("decreaseColumns")
        newMatrix = self.__ui.frameEditor.getMatrix()[:, :-1]
        self.__ui.frameEditor.updateMatrix(newMatrix)

    def setTitle(self, name : str):
        self.__ui.groupBox.setTitle(name)

    def saveState(self) -> Tuple[str, SimpleNamespace]:
        return self.__ui.frameEditor.saveState()

    def loadState(self, state: SimpleNamespace):
        return self.__ui.frameEditor.loadState(state)

    def disableSaving(self):
        return self.__ui.frameEditor.disableSaving()

    def enableSaving(self):
        return self.__ui.frameEditor.enableSaving()

    def getMatrix(self):
        return self.__ui.frameEditor.getMatrix()

    def updateMatrix(self, matrix):
        return self.__ui.frameEditor.updateMatrix(matrix)