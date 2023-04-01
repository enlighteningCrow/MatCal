# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

# In case you are reading this, there is NO ML or DL or any sort of AI in here; this is used solely for matrix calculations
from torch import Tensor, tensor

from typing import List
from math import inf


class Binding:

    def __init__(self, frame: 'FrameEditor', index: tuple):
        self.frame = frame
        self.index = index
        self.prevValue = None

    def __call__(self, value, firstCall = False):
        self.frame.matrix[self.index[: len(self.matrix.shape)]] = value


# TODO: Maybe rename to MatrixView
class FrameEditor(QWidget):

    def __init__(
        self,
        mat: Tensor,
        dimensionEditor: 'DimensionEditor',
        dimensions,
        parent = None
    ):
        self.initialized = False
        super().__init__(parent if parent is not None else dimensionEditor)
        # self.dimensionEditor = dimensionEditor
        self.matrix = mat
        self.spinboxes: List[QDoubleSpinBox] = []
        self.glOuter = QGridLayout(self)
        self.scrArea = QScrollArea(self)
        self.gl = QGridLayout(self.scrArea)
        self.glOuter.addWidget(self.scrArea, 1, 2, 1, 2)
        # self.xDimLabel = QLabel("Dimension X:", self)
        # self.yDimLabel = QLabel("Dimension Y:", self)
        # self.xDimSpin = QSpinBox(self)
        # self.xDimSpin.valueChanged.connect(self.updateDimensions)
        # self.yDimSpin = QSpinBox(self)
        # self.yDimSpin.valueChanged.connect(self.updateDimensions)
        # self.glOuter.addWidget(self.xDimLabel, 0, 2)
        # self.glOuter.addWidget(self.yDimLabel, 1, 0)
        # self.glOuter.addWidget(self.xDimSpin, 0, 3)
        # self.glOuter.addWidget(self.yDimSpin, 1, 1)
        # self.dimX
        # self.glOuter.addWidget(self.gl, 0, 1)
        self.updateBindings()
        # self.updateDimensionsCount(dimensions)
        self.initialized = True

    def updateBindings(self):
        shape = self.matrix.shape
        assert (len(shape) <= 2)
        if len(shape) == 1:
            shape = (self.matrix.shape[0], 1)
        elif len(shape) == 0:
            shape = (1, 1)
        shapem = shape[0]
        shapen = shape[1]
        counterI = 0
        for i in self.spinboxes[: shapen]:
            while len(i) < shapem:
                i.append(QDoubleSpinBox(self))
                i[-1].valueChanged.connect(
                    Binding(self, (counterI, len(i) - 1))
                )
                i[-1].setMaximum(inf)
                i[-1].setMinimum(-inf)
                self.gl.addWidget(i[-1], len(i) - 1, counterI)
            while len(i) > shapem:
                wid = i.pop()
                wid.disconnect()
                wid.setParent(None)
                self.gl.removeWidget(wid)
                counterI += 1
        for i in self.spinboxes[shapen :]:
            for j in i:
                wid = i.pop()
                wid.disconnect()
                wid.setParent(None)
                self.gl.removeWidget(wid)
        self.spinboxes = self.spinboxes[: shapen]
        while len(self.spinboxes) < shapem:
            self.spinboxes.append([QDoubleSpinBox(self) for i in range(shapen)])
            for i in range(shapen):
                self.spinboxes[-1][i].valueChanged.connect(
                    Binding(self, (len(self.spinboxes) - 1, i))
                )
                self.spinboxes[-1][i].setMaximum(inf)
                self.spinboxes[-1][i].setMinimum(-inf)
                self.gl.addWidget(
                    self.spinboxes[-1][i], i,
                    len(self.spinboxes) - 1
                )

    def updateMatrix(self, matrix: Tensor):
        # self.matrix.copy_(matrix)
        self.matrix = matrix
        self.updateBindings()
