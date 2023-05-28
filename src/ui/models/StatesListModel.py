import torch
from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt
from PySide6.QtWidgets import QDoubleSpinBox, QMessageBox

import logging

from db.GlobalSettings import settings

from torch import zeros, cat, Tensor
from torch.linalg import solve

from typing import *

from persistent.list import PersistentList as plist

from persistent import Persistent

from types import SimpleNamespace

from ui.CommWidg import CommWidgPersistent

class State(Persistent):

    # def __init__(self, tabName: str, displayString: str, value: dict):
        # self.tabName = tabName
        # self.displayString = displayString
        # self.value = value

    # def __init__(self, tab : CommWidgPersistent, displayString: str, value: SimpleNamespace):
    def __init__(self, tabName : str, displayString: str, value: SimpleNamespace):
        self.tabName = tabName
        self.displayString = displayString
        self.value = value



class StatesListModel(QAbstractListModel):

    def __init__(self, states : plist, parent = None):
        super().__init__(parent)
        #TODO: Use the ZODBdata structure for list instead
        self.__states = states

    def rowCount(self, parent = QModelIndex()):
        return len(self.__states)

    def data(self, index, role = Qt.DisplayRole):
        assert (isinstance(self.__states[index.row()], State))
        if role == Qt.DisplayRole:
            return self.__states[index.row()].displayString
        # elif role == Qt.EditRole:
        #     return float(self.__results[index.row()])
        return None

    def getState(self, index, role = None) -> State:
        assert (isinstance(self.__states[index.row()], State))
        return self.__states[index.row()]

    # def insertState(self, tabName : CommWidgPersistent, displayString : str, state: SimpleNamespace):
    def insertState(self, tabName : str, displayString : str, state: SimpleNamespace):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.__states.append(State(tabName, displayString, state))
        self.endInsertRows()

    def clear(self):
        self.beginResetModel()
        self.__states.clear()
        self.endResetModel()

    # def headerData(self, section, orientation, role = Qt.DisplayRole):
    #     if role == Qt.DisplayRole:
    #         if orientation == Qt.Vertical:
    #             return self.__varNamesList[section]
    #         else:
    #             return "Values"
    #     return None