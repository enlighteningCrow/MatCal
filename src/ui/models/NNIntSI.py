from PySide6.QtCore import Qt, Signal, QModelIndex, QPersistentModelIndex
from PySide6.QtGui import QStandardItem, QStandardItemModel

from typing import Union

from src.db.GlobalSettings import settings


class NNIntSI(QStandardItem):

    valueChanged = Signal(int)

    def __init__(self, value=0):
        super().__init__()
        self.value = value
        self.setData(str(value))
        self.isVisible = True
        self.prev_value = value

    def setVisibility(self, show: bool):
        if self.isVisible != show:
            # logging.info("Made", self, ('' if show else 'in') + "visible")
            self.isVisible = show
            # self.setFlags(~Qt.ItemIsEditable if show else Qt.ItemIsEditable)
            # self.setFlags(~Qt.ItemIsEnabled if show else Qt.ItemIsEnabled)
            # self.setFlags(Qt.)
            if show:
                self.setData(0)
                # self.setFlags(self.flags() | Qt.ItemIsEditable)
                self.setFlags(self.flags() | Qt.ItemIsEnabled)
            else:
                self.setText("-")
                # self.setFlags(self.flags() & ~Qt.ItemIsEditable)
                self.setFlags(self.flags() & ~Qt.ItemIsEnabled)

    def setData(self, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            self.prev_value = self.value
            self.value = int(value)
            # if self.prev_value != self.value:
            #     # self.valueChanged.emit(self.value)
            #     pass

        super().setData(value, role)

    def revertValue(self):
        self.value = self.prev_value
        self.setData(self.value)

    # def setValue(self, value):
    #     logging.info("setValue called with:", value)
    #     if isinstance(value, int) and value >= 0:
    #         self.setText(str(value))
    #         self.value = value
    #     else:
    #         raise ValueError("Value must be a nonnegative integer")

    # def setText(self, value):
    #     #TODO: Maybe make this also check if it is convertible to an int, raise exception otherwise
    #     #TODO: Make value private
    #     logging.info("setText called with:", value)
    #     super().setText(value)

    def getValue(self):
        # return self.value
        # logging.info(self.text())
        # if self.isEnabled():
        #     assert (self.value == int(self.text()))
        return self.value


class NNIntSIM(QStandardItemModel):

    # def headerData(self, section, orientation, role):
    #     # Write the function, with both the vertical and horizontal being an increasing sequence starting from 0
    #     # if orientation == Qt.Horizontal:
    #     #     return section
    #     if orientation == Qt.Vertical:
    #         return str(section)
    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if self.zeroBased and orientation == Qt.Vertical and role == Qt.DisplayRole:
            return str(section)
        return super().headerData(section, orientation, role)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.zeroBased = True
        settings("indexing").valueChanged.connect(self.setIndexing)

    # TODO: (Maybe) hook this up to the main menu toolbar actions
    def setIndexing(self, zeroBased: bool):
        self.zeroBased = zeroBased

    def setItem(self, row, column, item):
        if isinstance(item, NNIntSI) or item is None:
            super().setItem(row, column, item)
        else:
            raise ValueError("Item must be a NonnegativeIntegerStandardItem")

    def item(self, row: int, column: int = 0) -> NNIntSI:
        # if super().item(row, column) is None:
        #     logging.info(
        #         "None in model at row:", row, "with column:", column,
        #         "\nwith model:"
        #     )
        #     for i in range(self.rowCount()):
        #         for j in range(self.columnCount()):
        #             logging.info(super().item(i, j))

        return super().item(row, column)

    def itemFromIndex(
        self, index: Union[QModelIndex, QPersistentModelIndex]
    ) -> NNIntSI:
        return super().itemFromIndex(index)
