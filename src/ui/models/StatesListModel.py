import torch
from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt
from PySide6.QtWidgets import QDoubleSpinBox, QMessageBox

import logging

from db.GlobalSettings import settings

from torch import zeros, cat, Tensor
from torch.linalg import solve

from typing import *

from persistent.list import PersistentList as plist


class State:

    def __init__(self, tabName: str, displayString: str, value: dict):
        self.tabName = tabName
        self.displayString = displayString
        self.value = value


class StatesListModel(QAbstractListModel):

    def __init__(self, parent = None):
        super().__init__(parent)
        #TODO: Use the ZODBdata structure for list instead
        self.__states = plist()

    def rowCount(self, parent = QModelIndex()):
        return len(self.__states)

    def data(self, index, role = Qt.DisplayRole):
        assert (isinstance(self.__states[index.row()], State))
        if role == Qt.DisplayRole:
            return self.__states[index.row()].displayString
        # elif role == Qt.EditRole:
        #     return float(self.__results[index.row()])
        return None

    def getState(self, index, role = None):
        assert (isinstance(self.__states[index.row()], State))
        return self.__states[index.row()]

    # def headerData(self, section, orientation, role = Qt.DisplayRole):
    #     if role == Qt.DisplayRole:
    #         if orientation == Qt.Vertical:
    #             return self.__varNamesList[section]
    #         else:
    #             return "Values"
    #     return None