import torch
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtWidgets import QDoubleSpinBox, QMessageBox

import logging

from db.GlobalSettings import settings

from torch import zeros, cat

from typing import *

from ui.CommWidg import CommWidgPersistent


class MultiDimensionalMatrixException(Exception):

    def __init__(self, message) -> None:
        super().__init__(
            "Provided matrix has " + str(message) +
            " dimensions, more than the maximum allowed: 2"
        )


# TODO: Make the below option self._onXAxis connected to some sort of configuration file/something

# class EquationSolverModel(QAbstractTableModel):

#     def __init__(self, unknownsCount: int = 0, parent = None):
#         super().__init__(parent)
#         # self.unknownsCount = unknownsCount
#         self.updateUnknownsCount(unknownsCount)

#     def updateUnknownsCount(self, unknownsCount: int):
#         self.unknownsCount = unknownsCount
#         self.resize

from PySide6.QtCore import Qt, QModelIndex, QAbstractTableModel
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QStyledItemDelegate, QLineEdit, QWidget

from math import inf

class EquationDelegate(QStyledItemDelegate):

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.__parent = parent

    def createEditor(self, parent, option, index):
        editor = QDoubleSpinBox(parent)
        editor.setMinimum(-inf)
        editor.setMaximum(inf)
        return editor

    def setEditorData(self, editor: QDoubleSpinBox, index):
        value = index.model().data(index, Qt.EditRole)
        editor.setValue(float(value))
        # editor.setText(value)

    def setModelData(self, editor: QDoubleSpinBox, model, index):
        try:
            # value = float(editor.text())
            value = editor.value()
            model.setData(index, value, Qt.EditRole)
        except ValueError as e:
            # Show the error dialogue
            QMessageBox.critical(
                self.__parent, "Error", "Please enter a valid number"
            )

from types import SimpleNamespace

class EquationSolverModel(QAbstractTableModel, CommWidgPersistent):

    def __init__(self, unknownsCount: int = 0, parent = None):
        super().__init__()
        self.__varNamesList: List[str] = []
        self.__equations = zeros((unknownsCount, unknownsCount + 1))
        self.__unknownsCount = unknownsCount
        self.setUnknownsCount(unknownsCount)
        self.__saveDisabled = False

    def setUnknownsCount(self, unknownsCount: int):
        # self.equations.res
        self.__unknownsCount = unknownsCount
        n = self.__equations.size(0)
        assert (len(self.__varNamesList) == unknownsCount)
        assert (self.__equations.size(0) == self.__equations.size(1) - 1)
        if unknownsCount > n:
            self.beginInsertColumns(QModelIndex(), n, unknownsCount - 1)
            self.beginInsertRows(QModelIndex(), n, unknownsCount - 1)
            # Fill in the new columns and rows with zeros
            self.__equations = cat(
                (
                    cat(
                        (self.__equations, zeros((n, unknownsCount - n))),
                        dim = 1
                    ), zeros((unknownsCount - n, unknownsCount + 1))
                ),
                dim = 0
            )
            self.endInsertRows()
            self.endInsertColumns()
        elif unknownsCount < n:
            self.beginRemoveColumns(QModelIndex(), unknownsCount, n - 1)
            self.beginRemoveRows(QModelIndex(), unknownsCount, n - 1)
            self.__equations = self.__equations[: unknownsCount, :
                                                unknownsCount + 1]
            self.endRemoveRows()
            self.endRemoveColumns()

    def rowCount(self, parent = QModelIndex()):
        # Assert that the tensor is 2D and square (n x n)
        assert (self.__equations.dim() == 2)
        assert (self.__equations.size(0) == self.__equations.size(1) - 1)
        return self.__equations.size(0)

    def columnCount(self, parent = QModelIndex()):
        # Assert that the tensor is 2D and square (n x n)
        assert (self.__equations.dim() == 2)
        assert (self.__equations.size(1) - 1 == self.__equations.size(0))
        return self.__equations.size(1)

    def data(self, index, role = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(float(self.__equations[index.row()][index.column()]))
        elif role == Qt.EditRole:
            return float(self.__equations[index.row()][index.column()])
        return None

    def setData(self, index, value, role = Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            self.__equations[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, [role])
            return True
        return False

    def setVarNamesList(self, ib: QModelIndex, ie: QModelIndex):
        # for i in range(ib.row(), ie.row() + 1):
        #     self.varNamesList[i] = ib.data(Qt.EditRole)
        # ib = ib.sibling(ib.row() + 1, ib.column())
        # self.varNamesList = [
        #     ib.model().data(ib.model().index(i), Qt.EditRole)
        #     for i in range(ib.row(),
        #                    ie.row() + 1)
        # ]
        if ib.model() is None:
            return
        # self.varNamesList = ib.model().getVarNamesList()[:]
        for i in range(ib.row(), ie.row() + 1):
            self.__varNamesList[i] = ib.data(Qt.EditRole)
        ib = ib.sibling(ib.row() + 1, ib.column())
        self.headerDataChanged.emit(
            Qt.Horizontal, min(self.rowCount(), ib.row()),
            min(self.rowCount(), ie.row())
        )

    if 0 != 0:
        from VariableNamesListModel import VariableNamesListModel

    def insertVarNamesList(self, mod: 'VariableNamesListModel', a: int, b: int):
        if mod is None:
            return
        self.__varNamesList = self.__varNamesList[: a] + [
            mod.data(mod.index(i), Qt.EditRole) for i in range(a, b + 1)
        ] + self.__varNamesList[b + 1 :]

    def removeVarNamesList(self, a: int, b: int):
        self.__varNamesList = self.__varNamesList[: a] + self.__varNamesList[
            b + 1 :]

    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section < self.__unknownsCount:
                    if section < len(self.__varNamesList):
                        return self.__varNamesList[section]
                    return f"X{section+1}"
                elif section == self.__unknownsCount:
                    return "Result"
            elif orientation == Qt.Vertical:
                return f"Equation {section+1}"
        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return super().flags(index) | Qt.ItemIsEditable

    def getEquations(self):
        return self.__equations

    def getDisplayStringForState(self, state: SimpleNamespace):
    # def linear_equations_to_string(variables, equations):
        n = len(state.varNamesList)
        result = []

        for i in range(n):
            equation_str = []
            for j in range(n):
                coefficient = state.equations[i][j].item()
                variable = state.varNamesList[j]
                equation_str.append(f"{coefficient}*{variable}")
            
            constant = state.equations[i][-1].item()
            # equation_str.append(f"= {constant}")
            
            result.append(" + ".join(equation_str) + f" = {constant}")
        
        return " ; ".join(result)

    def saveState(self):
        if self.__saveDisabled:
            return None
        s = SimpleNamespace()
        s.unknownsCount = self.__unknownsCount
        s.varNamesList = self.__varNamesList[:]
        s.equations = self.__equations.clone()
        return "Equation Solver: " + self.getDisplayStringForState(s), s

    def loadState(self, state: SimpleNamespace):
        self.beginResetModel()
        self.__unknownsCount = state.unknownsCount
        self.__varNamesList = state.varNamesList[:]
        self.__equations = state.equations.clone()
        # self.dataChanged.emit(
        #     self.index(0, 0), self.index(self.rowCount() - 1,
        #                                     self.columnCount() - 1)
        # )
        # self.headerDataChanged.emit(Qt.Horizontal, 0, self.columnCount() - 1)
        # self.headerDataChanged.emit(Qt.Vertical, 0, self.rowCount() - 1)
        self.endResetModel()

    def disableSaving(self):
        self.__saveDisabled = True

    def enableSaving(self):
        self.__saveDisabled = False


