# This Python file uses the following encoding: utf-8
from typing import Tuple
from PySide6.QtWidgets import (
    QTableView,
    QVBoxLayout,
    QWidget,
)

# In case you are reading this, there is NO ML or DL or any sort of AI in here; this is used solely for matrix calculations
from torch import Tensor, empty

from ui.models.MatrixDataModel import MatrixDataModel

from ui.delegates.DoubleSpinBoxDelegate import DoubleSpinBoxDelegate

import logging


from ui.CommWidg import CommWidgPersistent

from types import SimpleNamespace

class FrameEditor(QWidget, CommWidgPersistent):

    def __init__(self, parent = None, mat: Tensor = empty((0, 0))):
        self.initialized = False
        super().__init__()
        self.vblo = QVBoxLayout(self)
        self.tableView = QTableView(self)
        self.matrixModel = MatrixDataModel(mat, self)
        self.tableView.setModel(self.matrixModel)
        self.vblo.addWidget(self.tableView)
        self.initialized = True

    def updateMatrix(self, matrix: Tensor):
        logging.info(matrix)
        self.matrixModel.setMatrix(matrix)

    def getDisplayStringForState(self, state: SimpleNamespace):
        return str(state.matrix)

    def saveState(self) -> Tuple[str, SimpleNamespace]:
        s = SimpleNamespace()
        s.matrix = self.matrixModel.getMatrix()
        return self.getDisplayStringForState(s), s

    def loadState(self, state: SimpleNamespace):
        self.matrixModel.setMatrix(state.matrix)

    def getMatrix(self) -> Tensor:
        return self.matrixModel.getMatrix()