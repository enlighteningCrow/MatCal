from PySide6.QtWidgets import *
# from torch import Tensor

# Cannot inherit from ABC as that will conflict with QT internal implementation
class OutputDelegate(): 
    # @abstractmethod
    def displayTypes():
        return {}

    def showData(self, data):
        self.data = data
        assert(type(self.data).__name__ in type(self).displayTypes())

class LineOutputDelegate(OutputDelegate, QLineEdit):
    def __init__(self) -> None:
        super().__init__()

    def displayTypes():
        return {"int", "float", "complex", "str", "bool", "bytes", "bytearray"}

    def showData(self, data):
        OutputDelegate.showData(self, data)
        self.setText(str(data))
    
class MatrixOutputDelegate(OutputDelegate, QTableWidget):
    def __init__(self) -> None:
        super().__init__()

    def displayTypes():
        return {"Tensor"}

    def showData(self, data):
        assert(data.dim() <= 2)
        OutputDelegate.showData(self, data)
        self.setRowCount(data.shape[0])
        self.setColumnCount(data.shape[1])
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                self.setItem(i, j, QTableWidgetItem(str(data[i, j].item())))

        
class IntegerBinaryOutputDelegate(OutputDelegate, QLineEdit):
    def __init__(self) -> None:
        super().__init__()

    def displayTypes():
        return {"binary"}

    def showData(self, data):
        OutputDelegate.showData(self, data)
        self.setText(bin(data)[2:])