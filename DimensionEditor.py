# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QSpinBox, QVBoxLayout, QWidget, QHBoxLayout

from FrameEditor import FrameEditor
from DIndexEditor import DIndexEditor
import torch

from typing import List


# TODO: Use a stackedwidget or something to swap between with 0 dimensions (1 lineedit), 1 dimension (1 row/column of lineedit), 2 dimensions (matrix of lineedits), 3+ dimensions (matrix of lineedits in selectable dimensions for columns and rows, with other dimensions selected with the spinboxes)
class DimensionEditor(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.hl = QHBoxLayout(self)
        self.vl = QVBoxLayout(self)
        self.hl.addLayout(self.vl)
        self.dimensions = 0
        self.dindEditors: List[DIndexEditor] = []
        print("DimensionEditor")
        self.matrix = torch.empty(())
        self.frameEditor = FrameEditor(self.matrix, self)
        self.hl.addWidget(self.frameEditor)
        self.dim0 = None
        self.dim1 = None
        # self.hl0 = QHBoxLayout(self)
        # self.hl0 = QHBoxLayout(self)

    def getCurrentFrame(self):
        currentFrame = tuple()
        for i, j in enumerate(self.dindEditors):
            if self.dim0 is not None and self.dim0 == i or self.dim1 is not None and self.dim1 == i:
                currentFrame += tuple([slice(None, None)])
            else:
                currentFrame += tuple([j.getCurInd()])
        print(currentFrame)
        return currentFrame

    def updateFrameMatrix(self, empty: bool = False):
        # mat = self.
        if empty:
            self.frameEditor.updateMatrix(torch.empty(()))
        else:
            print(self.getCurrentFrame())
            self.frameEditor.updateMatrix(self.matrix[self.getCurrentFrame()])

    def incrementDimensions(self):
        print("inc")
        self.dimensions += 1
        # # print([self.vl.itemAt(i) for i in range(self.vl.count())], self.dindEditors)
        # if self.dimensions > 2:
        #     self.dindEditors.append(QSpinBox(self))
        #     self.vl.addWidget(self.dindEditors[-1])
        # else:
        #     pass
        # # self.
        self.matrix = self.matrix.reshape(self.matrix.shape + tuple([1]))
        self.dindEditors.append(
            DIndexEditor(self.matrix, self.dimensions, self)
        )
        self.vl.addWidget(self.dindEditors[-1])
        self.updateFrameMatrix()
        # print([self.vl.itemAt(i) for i in range(self.vl.count())], self.dindEditors)

    def decrementDimensions(self):
        print("dec")
        assert (max(0, self.dimensions) == len(self.dindEditors))
        # if self.dimensions <= 2:
        #     # if self.dimensions == 2:
        #     pass
        # else:
        #     # print([self.vl.itemAt(i) for i in range(self.vl.count())], self.dindEditors)
        #     self.vl.removeWidget(self.dindEditors[-1])
        #     self.dindEditors.pop(-1).setParent(None)
        #     # print([self.vl.itemAt(i) for i in range(self.vl.count())], self.dindEditors)
        self.matrix = self.matrix.reshape(self.matrix.shape[:-1])
        self.vl.removeWidget(self.dindEditors[-1])
        self.dindEditors.pop(-1).setParent(None)
        self.dimensions -= 1
        self.updateFrameMatrix()

    def changeDimensions(self, num):
        currentDimensions = self.dimensions
        while self.dimensions != num:
            self.incrementDimensions(
            ) if self.dimensions < num else self.decrementDimensions()
            # if self.dimensions < 2:
            #     self.frameEditor.updateMatrix(self.matrix)
        self.frameEditor.updateDimensionsCount(num)
        self.frameEditor.updateBindings()

    def updateDimensions(self, dim0, dim1):
        # self.dindEditors[dim0].hideCurInd()
        # self.dindEditors[dim1].hideCurInd()
        self.dim0 = dim0
        self.dim1 = dim1
        if dim0 == dim1:
            self.updateFrameMatrix(True)
