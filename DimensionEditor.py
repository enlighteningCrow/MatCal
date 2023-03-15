# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QSpinBox, QVBoxLayout, QWidget, QHBoxLayout

from FrameEditor import FrameEditor
import torch


# TODO: Use a stackedwidget or something to swap between with 0 dimensions (1 lineedit), 1 dimension (1 row/column of lineedit), 2 dimensions (matrix of lineedits), 3+ dimensions (matrix of lineedits in selectable dimensions for columns and rows, with other dimensions selected with the spinboxes)
class DimensionEditor(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.hl = QHBoxLayout(self)
        self.vl = QVBoxLayout(self)
        self.hl.addLayout(self.vl)
        self.dimensions = 0
        self.dimIndSpins = []
        print("DimensionEditor")
        self.matrix = torch.tensor([0])
        self.frameEditor = FrameEditor(self.matrix, self)
        self.hl.addWidget(self.frameEditor)
        # self.hl0 = QHBoxLayout(self)
        # self.hl0 = QHBoxLayout(self)

    def updateFrameMatrix(self):
        self.frameEditor.updateMatrix()

    def incrementDimensions(self):
        print("inc")
        self.dimensions += 1
        # print([self.vl.itemAt(i) for i in range(self.vl.count())], self.dimIndSpins)
        if self.dimensions > 2:
            self.dimIndSpins.append(QSpinBox(self))
            self.vl.addWidget(self.dimIndSpins[-1])
        else:
            pass
        self.updateFrameMatrix()
        # print([self.vl.itemAt(i) for i in range(self.vl.count())], self.dimIndSpins)

    def decrementDimensions(self):
        print("dec")
        assert ((self.dimensions - 2 <= 0) == (len(self.dimIndSpins) <= 0))
        if self.dimensions <= 2:
            # if self.dimensions == 2:
            pass
        else:
            # print([self.vl.itemAt(i) for i in range(self.vl.count())], self.dimIndSpins)
            self.vl.removeWidget(self.dimIndSpins[-1])
            self.dimIndSpins.pop(-1).setParent(None)
            # print([self.vl.itemAt(i) for i in range(self.vl.count())], self.dimIndSpins)
        self.dimensions -= 1

    def changeDimensions(self, num):
        while self.dimensions != num:
            self.incrementDimensions(
            ) if self.dimensions < num else self.decrementDimensions()
