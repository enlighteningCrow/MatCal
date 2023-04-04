# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSpinBox,
    QTableView,
    QVBoxLayout,
    QWidget,
)

# In case you are reading this, there is NO ML or DL or any sort of AI in here; this is used solely for matrix calculations
from torch import Tensor, tensor

from typing import List
from math import inf

from MatrixModel import MatrixTableModel

# class MatrixModel(QAbstract)


# TODO: Maybe rename to MatrixView
class FrameEditor(QWidget):

    def __init__(self, mat: Tensor, parent = None):
        self.initialized = False
        super().__init__(parent)
        # self.dimensionEditor = dimensionEditor
        # self.matrix = mat
        # self.spinboxes: List[QDoubleSpinBox] = []
        # self.glOuter = QGridLayout(self)
        # self.scrArea = QScrollArea(self)
        # self.gl = QGridLayout(self.scrArea)
        # self.glOuter.addWidget(self.scrArea, 1, 2, 1, 2)
        self.vblo = QVBoxLayout(self)
        self.tableView = QTableView(self)
        self.matrixModel = MatrixTableModel(mat, parent = self)
        self.tableView.setModel(self.matrixModel)
        self.vblo.addWidget(self.tableView)
        # self.updateBindings()
        self.initialized = True

    # def updateBindings(self):

    def updateMatrix(self, matrix: Tensor):
        # self.matrix.copy_(matrix)
        # self.matrix = matrix
        # self.updateBindings()
        print(matrix)
        self.matrixModel.setMatrix(matrix)
