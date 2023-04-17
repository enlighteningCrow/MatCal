# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QWidget, QSpinBox
from torch import Tensor

from PySide6.QtCore import Signal
from typing import Tuple


# TODO: Make it hide the curIndex if the frameEditor is set to this dimension
class DIndexEditor(QWidget):
    sizeChange = Signal()
    curIndChange = Signal()

    def __init__(
        #TODO: Look at removing this tensor from the initializer arguments
        self,
        tensor: Tensor,
        dimension: int,
        parent: 'MatrixEditor' = None
    ):
        super().__init__(parent)
        # self.tensor = tensor
        self.dimension = dimension
        self.curInd = QSpinBox(parent)
        self.dimSize = QSpinBox(parent)
        self.curInd.setValue(0)
        self.dimSize.setValue(1)
        self.dimSize.setMaximum(1_000_000_000)
        # self.setSizePolicy(sp)

    def getWidgets(self) -> Tuple[QSpinBox, QSpinBox]:
        return self.curInd, self.dimSize

    # def dimLabelName(self):
    #     return str(self.dimension)
    # return "Dimension #" + str(dimension)

    # def updateDimensionSize(self):
    #     logging.info(self.tensor.shape[self.dimension])

    def hideCurInd(self):
        self.curInd.hide()

    def showCurInd(self):
        self.curInd.show()

    def getCurInd(self) -> int:
        return self.curInd.value()

    def setCurInd(self, val: int):
        self.curInd.setValue(val)
