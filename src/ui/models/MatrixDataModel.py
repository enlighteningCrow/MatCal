import torch
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

import logging

from src.db.GlobalSettings import settings


class MultiDimensionalMatrixException(Exception):

    def __init__(self, message) -> None:
        super().__init__(
            "Provided matrix has " + str(message) +
            " dimensions, more than the maximum allowed: 2"
        )


# TODO: Make the below option self._onXAxis connected to some sort of configuration file/something


class MatrixDataModel(QAbstractTableModel):

    def __init__(self, matrix: torch.Tensor, parent = None):
        super().__init__(parent)
        self.checkMatrixConstraints(matrix)
        # TODO: Check if this matrix set must be moved over to self.setMatrix
        self.__matrix: torch.Tensor = matrix
        self._onYAxis: bool = True
        self.zeroBased = True
        settings("axis").valueChanged.connect(self.setAxis)
        settings("indexing").valueChanged.connect(self.setIndexing)

    # TODO: (Maybe) hook this up to the main menu toolbar actions
    def setAxis(self, onXAxis: bool):
        # self.begin
        # if self.rowCount() > self.columnCount():
        #     self.beginInsertColumns(
        #         QModelIndex(), self.columnCount(), self.rowCount() - 1)
        #     self.beginRemoveRows(
        #         QModelIndex(), self.columnCount(), self.rowCount() - 1)
        self.beginResetModel()
        self._onYAxis = not onXAxis
        self.dataChanged.emit(
            self.index(0, 0),
            self.index(self.rowCount() - 1,
                       self.columnCount() - 1)
        )
        self.endResetModel()

    # TODO: (Maybe) hook this up to the main menu toolbar actions
    def setIndexing(self, zeroBased: bool):
        self.zeroBased = zeroBased

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if role == Qt.DisplayRole:
            return str(section)
        return super().headerData(section, orientation, role)

    def checkMatrixConstraints(self, matrix: torch.Tensor):
        if matrix.dim() > 2:
            raise MultiDimensionalMatrixException(matrix.dim())

    def rowCount(self, parent = QModelIndex()):
        if self.__matrix.dim() == 0:
            return 1
        return self.__matrix.size(0) if self.__matrix.dim(
        ) == 2 or self._onYAxis else 1

    def columnCount(self, parent = QModelIndex()):
        if self.__matrix.dim() == 0:
            return 1
        return self.__matrix.size(1) if self.__matrix.dim(
        ) == 2 else (1 if self._onYAxis else self.__matrix.size(0))

    def data(self, index, role = Qt.DisplayRole):
        if not index.isValid():
            return None

        row, column = index.row(), index.column()

        if role in (Qt.DisplayRole, Qt.EditRole):
            if self.__matrix.dim() == 0:
                return str(self.__matrix.item())
            if self.__matrix.dim() == 1:
                if self._onYAxis:
                    if column == 0:
                        return str(self.__matrix[row].item())
                else:
                    if row == 0:
                        return str(self.__matrix[column].item())
            else:
                return str(self.__matrix[row][column].item())

        return None

    def setData(self, index, value, role = Qt.EditRole):
        if not index.isValid() or role != Qt.EditRole:
            return False

        logging.info(f"Set data to matrix: {self.__matrix}")

        row, column = index.row(), index.column()

        if type(value) is not float:
            value = float(value)

        if self.__matrix.dim() == 0:
            self.__matrix.fill_(value)
            self.dataChanged.emit(index, index)
            return True
        if self.__matrix.dim() == 1:
            if self._onYAxis:
                if column == 0:
                    self.__matrix[row] = value
                    self.dataChanged.emit(index, index)
                    return True
            else:
                if row == 0:
                    self.__matrix[column] = value
                    self.dataChanged.emit(index, index)
                    return True
        else:
            self.__matrix[row][column] = value
            self.dataChanged.emit(index, index)
            return True

        return False

    def flags(self, index):
        flags = super().flags(index)
        if index.isValid():
            flags |= Qt.ItemIsEditable
        return flags

    # def headerData(self, section, orientation, role = Qt.DisplayRole):
    #     if role != Qt.DisplayRole:
    #         return None

    #     if orientation == Qt.Horizontal:
    #         if self.__matrix.dim() == 1 and not self._onXAxis:
    #             return str(section)
    #         else:
    #             return str(section)
    #     else:
    #         if self.__matrix.dim() == 1 and self._onXAxis:
    #             return str(section)
    #         else:
    #             return str(section)

    def setMatrix(self, matrix: torch.Tensor):
        self.checkMatrixConstraints(matrix)
        oldRows = self.rowCount()
        oldCols = self.columnCount()
        self.__matrix = matrix
        newRows = self.rowCount()
        newCols = self.columnCount()

        # Emit signals for row changes
        if oldRows < newRows:
            self.beginInsertRows(QModelIndex(), oldRows, newRows - 1)
            self.endInsertRows()
        elif oldRows > newRows:
            self.beginRemoveRows(QModelIndex(), newRows, oldRows - 1)
            self.endRemoveRows()

        # Emit signals for column changes
        if oldCols < newCols:
            self.beginInsertColumns(QModelIndex(), oldCols, newCols - 1)
            self.endInsertColumns()
        elif oldCols > newCols:
            self.beginRemoveColumns(QModelIndex(), newCols, oldCols - 1)
            self.endRemoveColumns()

        # Emit signal for data changes
        topLeft = self.index(0, 0)
        bottomRight = self.index(newRows - 1, newCols - 1)
        self.dataChanged.emit(topLeft, bottomRight)
