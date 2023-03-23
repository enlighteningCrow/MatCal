# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QWidget
from ui_DIndexEditor import Ui_Form
from torch import Tensor

from PySide6.QtCore import Signal


# TODO: Make it hide the curIndex if the frameEditor is set to this dimension
class DIndexEditor(QWidget):
    instances = 0
    sizeChange = Signal()
    curIndChange = Signal()

    def __init__(
        self, tensor: Tensor, dimension: int, parent: 'DimensionEditor' = None
    ):
        super().__init__(parent)
        self.tensor = tensor
        self.instances += 1
        self.dimension = dimension
        self.__ui = Ui_Form()
        self.__ui.setupUi(self)
        self.__ui.curInd.setValue(0)
        self.__ui.dimSize.setValue(1)
        sp = self.__ui.curInd.sizePolicy()
        sp.setRetainSizeWhenHidden(True)
        self.__ui.curInd.setSizePolicy(sp)
        # self.setSizePolicy(sp)
        self.updateDimension()

    def __del__(self):
        self.instances -= 1

    def dimLabelName(self):
        return str(self.dimension)
        # return "Dimension #" + str(dimension)

    def updateDimension(self):
        self.__ui.dimInd.setText(self.dimLabelName())
        self.__ui.curInd.setValue(0)

    def updateDimensionSize(self):
        print(self.tensor.shape[self.dimension])

    def hideCurInd(self):
        self.__ui.curInd.hide()

    def showCurInd(self):
        self.__ui.curInd.show()

    def getCurInd(self) -> int:
        return self.__ui.curInd.value()

    def setCurInd(self, val: int):
        self.__ui.curInd.setValue(val)
