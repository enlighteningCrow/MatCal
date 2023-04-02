from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel


class NNIntSI(QStandardItem):

    def __init__(self, value = 0):
        super().__init__()
        self.setValue(value)
        self.value = value

    def setValue(self, value):
        print("setValue called with:", value)
        if isinstance(value, int) and value >= 0:
            self.setText(str(value))
            self.value = value
        else:
            raise ValueError("Value must be a nonnegative integer")

    def setText(self, value):
        #TODO: Maybe make this also check if it is convertible to an int, raise exception otherwise
        #TODO: Make value private
        print("setText called with:", value)
        super().setText(value)

    def getValue(self):
        return self.value


class NNIntSIM(QStandardItemModel):

    def __init__(self, parent = None):
        super().__init__(parent)

    def setItem(self, row, column, item):
        if isinstance(item, NNIntSI):
            super().setItem(row, column, item)
        else:
            raise ValueError("Item must be a NonnegativeIntegerStandardItem")

    def item(self, row: int, column: int = ...) -> NNIntSI:
        return super().item(row, column)