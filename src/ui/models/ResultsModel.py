import torch
from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt
from PySide6.QtWidgets import QDoubleSpinBox, QMessageBox

import logging

from db.GlobalSettings import settings

from torch import zeros, cat, Tensor
from torch.linalg import solve

from typing import *

from ui.CommWidg import CommWidgPersistent

from types import SimpleNamespace


class ResultsModel(QAbstractListModel, CommWidgPersistent):

    def __init__(self, parent = None):
        super().__init__()
        self.__parent = parent
        self.__varNamesList: List[str] = []
        self.__results = zeros(0)
        self.__saveDisabled = False

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

    def getDisplayStringForState(self, state: SimpleNamespace):
        return ", ".join(
            [
                self.__varNamesList[i] + " = " + str(float(state.results[i]))
                for i in range(len(
                    # self.__varNamesList
                    state.results
                    ))
            ]
        )

    def saveState(self):
        if self.__saveDisabled:
            return None
        # self.
        # return self.__varNamesList, self.__results
        s = SimpleNamespace()
        s.varNamesList = self.__varNamesList[:]
        s.results = self.__results.clone()
        return self.getDisplayStringForState(s), s

    def loadState(self, state: SimpleNamespace):
        # return super().loadState(state)
        self.beginResetModel()
        self.__varNamesList = state.varNamesList[:]
        self.__results = state.results.clone()
        # self.headerDataChanged.emit(Qt.Vertical, 0, self.rowCount() - 1)
        # self.dataChanged.emit(QModelIndex(), QModelIndex())
        self.endResetModel()

    def disableSaving(self):
        self.__saveDisabled = True

    def enableSaving(self):
        self.__saveDisabled = False
