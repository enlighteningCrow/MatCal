from types import SimpleNamespace
from PySide6.QtCore import Qt, Signal, QModelIndex, QPersistentModelIndex, QAbstractTableModel
from PySide6.QtGui import QStandardItem, QStandardItemModel

from typing import Tuple, Union

from db.GlobalSettings import settings

from ui.CommWidg import CommWidgPersistent

from torch import Tensor, tensor, empty


# class NNIntSIM(QAbstractTableModel, CommWidgPersistent):

#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.zeroBased = True
#         settings("indexing").valueChanged.connect(self.setIndexing)
#         self.__data = empty((0, 2), dtype=object)

#     def setIndexing(self, zeroBased: bool):
#         self.zeroBased = zeroBased

#     def setItem(self, row, column, item):
#         if isinstance(item, NNIntSI) or item is None:
#             self.__data[row][column] = item
#         else:
#             raise ValueError("Item must be a NonnegativeIntegerStandardItem")

#     def item(self, row: int, column: int = 0) -> NNIntSI:
#         return self.__data[row][column]

#     def rowCount(self, parent=QModelIndex()):
#         return len(self.__data)

#     def columnCount(self, parent=QModelIndex()):
#         if len(self.__data) > 0:
#             return len(self.__data[0])
#         return 0

#     def data(self, index, role=Qt.DisplayRole):
#         if not index.isValid():
#             return None

#         if role == Qt.DisplayRole or role == Qt.EditRole:
#             row = index.row()
#             col = index.column()
#             item = self.__data[row][col]
#             if item is not None:
#                 return item.getValue()

#         return None

#     def setData(self, index, value, role=Qt.EditRole):
#         if index.isValid() and role == Qt.EditRole:
#             row = index.row()
#             col = index.column()
#             item = self.__data[row][col]
#             if item is not None:
#                 item.setData(value, role)
#                 self.dataChanged.emit(index, index)
#                 return True

#         return False

#     def flags(self, index):
#         if not index.isValid():
#             return Qt.NoItemFlags

#         return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

#     def itemFromIndex(
#         self, index: Union[QModelIndex, QPersistentModelIndex]
#     ) -> NNIntSI:
#         row = index.row()
#         col = index.column()
#         return self.__data[row][col]

#     def saveState(self) -> Tuple[str, SimpleNamespace]:
#         s = SimpleNamespace()
#         # Implement saving state logic here
#         return "NNIntSIM", s

class NNIntSI(QStandardItem):

    valueChanged = Signal(int)

    def __init__(self, value = 0):
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

    def setData(self, value, role = Qt.EditRole):
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


from ui.CommWidg import CommWidgPersistent

class NNIntSIM(QStandardItemModel, CommWidgPersistent):

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

    def __init__(self, parent = None):
        super().__init__()
        # When zeroBased is True, then the index is zero-based.
        # When zeroBased is False, then the index is one-based.
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

    def saveState(self) -> Tuple[str, SimpleNamespace]:
        s = SimpleNamespace()
        # Convert the model data to a Python list
        dlist = []
        for row in range(self.rowCount()):
            row_data = []
            for column in range(self.columnCount()):
                item = self.item(row, column)
                if item is not None:
                    row_data.append(item.getValue())
                else:
                    row_data.append(None)
            dlist.append(row_data)

        s.data_list = dlist
        
        # Return the list as the saved state
        return "NNIntSIM", s

    def loadState(self, state):
        # Clear the current model data
        self.clear()

        # Retrieve the saved data from the state
        dlist = state.dlist

        # Populate the model with the saved data
        for row, row_data in enumerate(dlist):
            for column, value in enumerate(row_data):
                item = NNIntSI(value) if value is not None else None
                self.setItem(row, column, item)

