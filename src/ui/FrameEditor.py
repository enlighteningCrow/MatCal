# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import (
    QTableView,
    QVBoxLayout,
    QWidget,
)

# In case you are reading this, there is NO ML or DL or any sort of AI in here; this is used solely for matrix calculations
from torch import Tensor

from src.ui.models.MatrixDataModel import MatrixDataModel

from src.ui.delegates.DoubleSpinBoxDelegate import DoubleSpinBoxDelegate

import logging

# class MatrixModel(QAbstract)


# TODO: Maybe rename to MatrixView
class FrameEditor(QWidget):

    def __init__(self, mat: Tensor, parent=None):
        self.initialized = False
        super().__init__(parent)
        # self.matrix = mat
        # self.spinboxes: List[QDoubleSpinBox] = []
        # self.glOuter = QGridLayout(self)
        # self.scrArea = QScrollArea(self)
        # self.gl = QGridLayout(self.scrArea)
        # self.glOuter.addWidget(self.scrArea, 1, 2, 1, 2)
        self.vblo = QVBoxLayout(self)
        self.tableView = QTableView(self)
        self.matrixModel = MatrixDataModel(mat, self)
        self.tableView.setModel(self.matrixModel)
        self.vblo.addWidget(self.tableView)
        # self.updateBindings()
        self.initialized = True

    # def updateBindings(self):

    def updateMatrix(self, matrix: Tensor):
        # self.matrix.copy_(matrix)
        # self.matrix = matrix
        # self.updateBindings()
        logging.info(matrix)
        self.matrixModel.setMatrix(matrix)
        # self.tableView.resizeColumnsToContents()
        # self.tableView.resizeRowsToContents()
