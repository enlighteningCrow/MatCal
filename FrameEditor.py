# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QGridLayout,
    QHBoxLayout,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

# In case you are reading this, there is NO ML or DL or any sort of AI in here; this is used solely for matrix calculations
from torch import Tensor, tensor


class FrameEditor(QWidget):

    def __init__(self, mat: Tensor, parent = None):
        super().__init__(parent)
        self.matrix = mat
        self.spinboxes = []
        self.gl = QGridLayout(self)
        self.updateBindings()

    def updateBindings(self):
        shape = self.matrix.shape
        assert (len(shape) <= 2)
        if len(shape) < 2:
            shape = (self.matrix.shape[0], 1)
        shapem = shape[0]
        shapen = shape[1]
        counterI = 0
        for i in self.spinboxes[: shapen]:
            while len(i) < shapem:
                i.append(QDoubleSpinBox(self))
                self.gl.addWidget(i[-1], len(i) - 1, counterI)
            while len(i) > shapem:
                wid = i.pop()
                wid.setParent(None)
                self.gl.removeWidget(wid)
                counterI += 1
        for i in self.spinboxes[shapen :]:
            for j in i:
                wid = i.pop()
                wid.setParent(None)
                self.gl.removeWidget(wid)
        self.spinboxes = self.spinboxes[: shapen]
        while len(self.spinboxes) < shapem:
            self.spinboxes.append([QDoubleSpinBox(self) for i in range(shapen)])
            for i in range(shapen):
                self.gl.addWidget(
                    self.spinboxes[-1][i], i,
                    len(self.spinboxes) - 1
                )

    def updateMatrix(self, matrix: Tensor):
        # self.matrix.copy_(matrix)
        self.matrix = matrix
        self.updateBindings()
