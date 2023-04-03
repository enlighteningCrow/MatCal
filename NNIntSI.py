from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QStandardItem, QStandardItemModel


class NNIntSI(QStandardItem):

    valueChanged = Signal(int)

    def __init__(self, value = 0):
        super().__init__()
        self.value = value
        self.setData(str(value))
        self.isVisible = True

    def setVisibility(self, show: bool):
        if self.isVisible != show:
            # print("Made", self, ('' if show else 'in') + "visible")
            self.isVisible = show
            self.setFlags(~Qt.ItemIsEditable if show else Qt.ItemIsEditable)
            if show:
                self.setData(0)

    def setData(self, value, role = Qt.EditRole):
        if role == Qt.EditRole:
            oldValue = self.value
            self.value = int(value)
            if oldValue != self.value:
                # self.valueChanged.emit(self.value)
                pass
        super().setData(value, role)

    # def setValue(self, value):
    #     print("setValue called with:", value)
    #     if isinstance(value, int) and value >= 0:
    #         self.setText(str(value))
    #         self.value = value
    #     else:
    #         raise ValueError("Value must be a nonnegative integer")

    # def setText(self, value):
    #     #TODO: Maybe make this also check if it is convertible to an int, raise exception otherwise
    #     #TODO: Make value private
    #     print("setText called with:", value)
    #     super().setText(value)

    def getValue(self):
        # return self.value
        # print(self.text())
        # if self.isEnabled():
        #     assert (self.value == int(self.text()))
        return self.value


class NNIntSIM(QStandardItemModel):

    def __init__(self, parent = None):
        super().__init__(parent)

    def setItem(self, row, column, item):
        if isinstance(item, NNIntSI) or item is None:
            super().setItem(row, column, item)
        else:
            raise ValueError("Item must be a NonnegativeIntegerStandardItem")

    def item(self, row: int, column: int = ...) -> NNIntSI:
        return super().item(row, column)