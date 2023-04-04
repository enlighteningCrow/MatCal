# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QSpinBox, QVBoxLayout, QWidget, QHBoxLayout, QLabel

from FrameEditor_bck2 import FrameEditor
from DIndexEditor import DIndexEditor
import torch

from typing import List

# from ui_DIndexLabels import Ui_Form
from ui_DimensionEditor import Ui_Form

# TODO: Use a stackedwidget or something to swap between with 0 dimensions (1 lineedit), 1 dimension (1 row/column of lineedit), 2 dimensions (matrix of lineedits), 3+ dimensions (matrix of lineedits in selectable dimensions for columns and rows, with other dimensions selected with the spinboxes)


class Binding:

    def __init__(self, dimEdit: 'DimensionEditor', dim: int) -> None:
        self.dimEdit = dimEdit
        self.dim = dim

    def updateSize(self, val: int) -> None:
        # TODO: Make this change the dimensions
        if val < self.dimEdit.matrix.shape[self.dim]:
            self.dimEdit.matrix = self.dimEdit.matrix[(
                (slice(None, None) if i != self.dim else slice(None, val))
                for i in range(self.dim)
            )]
        elif val < self.dimEdit.matrix.shape[self.dim]:
            shape = list(self.dimEdit.matrix.shape)
            shape[self.dim] = self.dimEdit.matrix.shape[self.dim] - val
            self.dimEdit.matrix = torch.cat(
                (
                    self.dimEdit.matrix,
                    torch.ones(shape, device = self.dimEdit.matrix.device)
                ), self.dim
            )

    def __call__(self, val: int) -> None:
        return self.updateSize(val)


class DimensionEditor(QWidget):

    def __init__(self, parent: 'MatrixEditor' = None):
        super().__init__(parent)
        self.hl = QHBoxLayout(self)
        self.vl = QVBoxLayout(self)
        self.hl.addLayout(self.vl)
        self.dimensions = 0
        self.dindEditors: List[DIndexEditor] = []
        print("DimensionEditor")
        self.matrix = torch.zeros(())
        self.frameEditor = FrameEditor(
            self.matrix, self, parent.getDimensions()
        )
        self.hl.addWidget(self.frameEditor)
        self.dim0 = None
        self.dim1 = None
        # self.hl0 = QHBoxLayout(self)
        # self.hl0 = QHBoxLayout(self)

        # self.widg = QWidget(self)
        # self.widg_hl = QHBoxLayout(self.widg)
        # self.widg_DimensionLabel = QLabel("Dimension #", self.widg)
        # self.widg_DimensionSize = QLabel("Dimension Size")
        # self.widg_CurrentIndex = QLabel("Current Index")
        # self.widg_hl.addWidget(self.widg_DimensionLabel)
        # self.widg_hl.addWidget(self.widg_DimensionSize)
        # self.widg_hl.addWidget(self.widg_CurrentIndex)

        self.widg = QWidget(self)
        self.labelsUi = Ui_Form()
        self.labelsUi.setupUi(self.widg)
        self.vl.addWidget(self.widg)
        self.changeDimensions(parent.getDimensions())

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
            self.frameEditor.updateMatrix(torch.zeros(()))
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
        print(f"shape: {self.matrix.shape}; matrix: {self.matrix}")
        self.matrix = self.matrix.reshape(self.matrix.shape + tuple([1]))
        b = Binding(self, len(self.dindEditors))
        self.dindEditors.append(
            DIndexEditor(self.matrix, self.dimensions, self)
        )
        self.dindEditors[-1].sizeChange.connect(b)
        self.dindEditors[-1].curIndChange.connect(self.updateFrameMatrix)
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

    def changeDimensions(self, dim):
        currentDimensions = self.dimensions
        while self.dimensions != dim:
            self.incrementDimensions(
            ) if self.dimensions < dim else self.decrementDimensions()
            # if self.dimensions < 2:
            #     self.frameEditor.updateMatrix(self.matrix)
        self.frameEditor.updateDimensionsCount(dim)
        self.frameEditor.updateBindings()

    def updateDimensions(self, dim0, dim1):
        # self.dindEditors[dim0].hideCurInd()
        # self.dindEditors[dim1].hideCurInd()
        self.dim0 = dim0
        self.dim1 = dim1
        self.updateFrameMatrix(dim0 == dim1)
