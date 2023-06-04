from PySide6.QtWidgets import *
from torch import *

from ui.easyUI.MatrixEditor import MatrixEditor
from src.ui.easyUI.ButtonInputs import ButtonInputs

# Cannot inherit from ABC as that will conflict with QT internal implementation
class InputDelegate(): 
    # @abstractmethod
    def promptTypes():
        return {}

    def getData(self):
        # assert(type(self.data) in self.promptTypes())
        return None
        # return self.data

    def loadData(self, data):
        pass

class IntInputDelegate(InputDelegate, QSpinBox):
    def __init__(self, parent = None, keypadParent = None) -> None:
        QSpinBox.__init__(self, parent)
        self.setMaximum(999999999)
        self.setMinimum(-999999999)
        self.inputKeypad = ButtonInputs(keypadParent)

    def promptTypes():
        return {"int"}

    def getData(self):
        super().getData()
        return self.value()

    def loadData(self, data):
        self.setValue(data)
    
class MatrixInputDelegate(InputDelegate, MatrixEditor):
    def __init__(self, parent = None) -> None:
        MatrixEditor.__init__(self, parent)
        self.setTitle("Matrix Input")

    def promptTypes():
        return {"Tensor"}

    def getData(self):
        super().getData()
        return self.getMatrix()

    def loadData(self, data):
        self.updateMatrix(data.clone())

        
class FloatInputDelegate(InputDelegate, QDoubleSpinBox):
    def __init__(self, parent = None) -> None:
        QDoubleSpinBox.__init__(self, parent)
        self.setMaximum(999999999)
        self.setMinimum(-999999999)

    def promptTypes():
        return {"float"}

    def getData(self):
        super().getData()
        return self.value()

    def loadData(self, data):
        self.setValue(data)

class BinaryInputDelegate(InputDelegate, QLineEdit):
    def __init__(self, parent = None) -> None:
        QLineEdit.__init__(self, parent)

    def promptTypes():
        return {"binary"}

    def getData(self):
        super().getData()
        return int(self.text(), 2)

    def loadData(self, data):
        self.setText(bin(data)[2:])

# class HexInputDelegate(InputDelegate, )