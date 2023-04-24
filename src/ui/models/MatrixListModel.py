from PySide6.QtCore import QAbstractListModel
from torch import Tensor, zeros
from typing import List, Tuple, Union

from PySide6.QtCore import Qt, QModelIndex

import logging

from bisect import bisect_left

from BTrees.OOBTree import OOBTree


class DuplicateValueError(Exception):

    def __init__(self, name: str) -> None:
        super().__init__(f"Matrix with name {name} already exists in the list.")


class EmptyNameError(Exception):

    def __init__(self) -> None:
        super().__init__("Matrix created with empty name")


class MatrixPair:

    def __init__(self, name: str, matrix: Tensor):
        self.name = name
        self.__matrix = matrix

    @property
    def matrix(self):
        return self.__matrix

    def __lt__(self, other: 'MatrixPair') -> bool:
        return self.name < other.name

    def __str__(self):
        # return self.name + " : " + self.matrix.__str__()
        return self.name


class MatrixListModel(QAbstractListModel):

    def __init__(self, parent = None):
        super().__init__(parent)
        # self.__matrices : List[Matrix]= matrices
        self.__matrices = OOBTree()

    def getMatrixList(self):
        return self.__matrices

    def rowCount(self, parent = QModelIndex()):
        return len(self.__matrices)

    def data(self, index, role = Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < self.rowCount()):
            return None
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self.__matrices[index.row()]
        return None

    def insertRows(self, row, count, parent = QModelIndex()):
        self.beginInsertRows(parent, row, row + count - 1)
        self.__matrices[row : row] = (None for i in range(count))
        self.endInsertRows()
        return True

    def removeRows(self, row, count, parent = QModelIndex()):
        self.beginRemoveRows(parent, row, row + count - 1)
        self.__matrices[row : row + count] = ()
        self.endRemoveRows()
        return True

    def addMatrix(self, matrix: MatrixPair):
        logging.info(f"Before adding matrix: {self.__matrices}")
        assert (type(matrix) is MatrixPair)
        if not len(matrix.name):
            raise EmptyNameError()

        index = bisect_left(self.__matrices, matrix)
        if index < len(self.__matrices
                      ) and matrix.name == self.__matrices[index].name:
            raise DuplicateValueError(matrix.name)
        self.beginInsertRows(QModelIndex(), index, index)
        self.__matrices.insert(index, matrix)
        self.endInsertRows()
        logging.info(f"After adding matrix: {self.__matrices}")
        self.dataChanged.emit(self.index(index), self.index(index))
        # self.__matrices.insert(index, matrix)
        # self.setData(self.index(index), matrix)
        # self.dataChanged.emit(
        #     self.index(index), self.index(self.rowCount() - 1)
        # )
        # self.layoutChanged.emit()

    # def dataPair(self, index: int):
    #     return self.__matrices[index]

    # def setData(self, index: QModelIndex, value, role=Qt.EditRole) -> bool:
    #     if not index.isValid() or role != Qt.EditRole or index.row() >= len(
    #             self.__matrices):
    #         return False
    #     if isinstance(value, MatrixPair):
    #         self.__matrices[index.row()] = value
    #     elif isinstance(value, str):
    #         self.__matrices[index.row()] = MatrixPair(value, zeros(()))
    #     else:
    #         return False
    #     return True

    # def flags(self, index):
    #     flags = super().flags(index)
    #     if index.isValid():
    #         flags |= Qt.ItemIsEditable
    #     return flags
