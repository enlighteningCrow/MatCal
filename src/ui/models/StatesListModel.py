import torch
from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt
from PySide6.QtWidgets import QDoubleSpinBox, QMessageBox

import logging

from db.GlobalSettings import settings

from torch import zeros, cat, Tensor
from torch.linalg import solve

from typing import *


class State:

    def __init__(self, tabName: str, displayString: str, value: dict):
        self.tabName = tabName
        self.displayString = displayString
        self.value = value


class StatesListModel(QAbstractListModel):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.__states = List[State]

    def rowCount(self, parent = QModelIndex()):
        return self.__results.size(0)

    def data(self, index, role = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(float(self.__results[index.row()]))
        elif role == Qt.EditRole:
            return float(self.__results[index.row()])
        return None

    def calculate(self, varNamesList: List[str], equations: Tensor):
        try:
            self.__varNamesList = varNamesList[:]
            assert (equations.dim() == 2)
            assert (equations.size(0) == equations.size(1) - 1)
            self.beginResetModel()
            self.__results = solve(equations[:, :-1], equations[:, -1])
            self.endResetModel()
            self.headerDataChanged.emit(Qt.Vertical, 0, self.rowCount() - 1)
        except RuntimeError as e:
            QMessageBox.critical(
                self.__parent, "Error", "The equations are invalid: " + str(e)
            )

    def getResults(self):
        return self.__results

    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Vertical:
                return self.__varNamesList[section]
            else:
                return "Values"
        return None