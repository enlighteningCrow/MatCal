import torch
from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt, Signal

from typing import *

import logging

from db.GlobalSettings import settings

from PySide6.QtWidgets import QStyledItemDelegate, QLineEdit, QTableView, QSpinBox, QMessageBox, QWidget

from ui.CommWidg import CommWidgPersistent


class VariableDelegate(QStyledItemDelegate):

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.__parent = parent

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        editor.setText(value)

    def setModelData(self, editor, model, index):
        try:
            value = editor.text()
            if value in model.getVarNamesList():
                raise ValueError("Duplicate variable name")
            model.setData(index, value, Qt.EditRole)
        except ValueError as e:
            # Show the error dialogue
            QMessageBox.critical(
                self.__parent, "Error",
                "The variable name is invalid: " + str(e)
            )

from types import SimpleNamespace


class VariableNamesListModel(QAbstractListModel, CommWidgPersistent):
    #

    # # TODO: Make this signal, and connect it to the setVarNamesList in equation solver in the designer
    # varListChanged = Signal(list)

    def __init__(self, unknownsCount: int = 0, parent = None):
        # QAbstractListModel.__init__(self, parent=parent)
        # CommWidgPersistent.__init__(self)
        super().__init__()
        self.names = []
        self.__saveDisabled = False

    def setUnknownsCount(self, unknownsCount: int):
        self.size = unknownsCount
        if unknownsCount > len(self.names):
            self.beginInsertRows(
                QModelIndex(), len(self.names), unknownsCount - 1
            )
            oldLength = len(self.names)

            def sgbody(num: int):
                res = ""
                while num >= 0:
                    remainder = num % 26
                    res += chr(remainder + ord('a'))
                    num = num // 26 - 1
                    if num < 0:
                        break
                return res[::-1]

            def sgen():
                count = 0
                while True:
                    yield (sgbody(count))
                    count += 1

            for i in sgen():
                if len(self.names) >= unknownsCount:
                    break
                if i not in self.names:
                    self.names.append(i)
            self.endInsertRows()
            # self.dataChanged.emit(
            #     self.index(oldLength), self.index(unknownsCount - 1),
            #     [Qt.EditRole]
            # )
        elif unknownsCount < len(self.names):
            self.beginRemoveRows(
                QModelIndex(), unknownsCount,
                len(self.names) - 1
            )
            oldLength = len(self.names)
            while len(self.names) > unknownsCount:
                self.names.pop(unknownsCount)
            self.endRemoveRows()

    def getVarNamesList(self):
        return self.names

    def rowCount(self, parent = QModelIndex()):
        return len(self.names)

    def data(self, index, role = Qt.DisplayRole):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self.names[index.row()]
        return None

    def setData(self, index, value, role = Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            self.names[index.row()
                      ] = value if type(value) is str else str(value)
            self.dataChanged.emit(index, index, [role])
            return True
        return False

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return super().flags(index) | Qt.ItemIsEditable

    # def addObservee(self, observee):
    #     self.varListChanged.connect(observee.setVarNamesList)

    def getDisplayStringForState(self, state: SimpleNamespace):
        return str(state.names)


    def saveState(self):
        if self.__saveDisabled:
            return None
        s = SimpleNamespace()
        s.names = self.names[:]
        return self.getDisplayStringForState(s), s

    def loadState(self, state : SimpleNamespace):
        self.beginResetModel()
        self.names = state.names[:]
        self.endResetModel()
        # self.dataChanged.emit(
        #     self.index(0), self.index(len(self.names) - 1),
        #     [Qt.EditRole]
        # )

    def disableSaving(self):
        self.__saveDisabled = True

    def enableSaving(self):
        self.__saveDisabled = False


#TODO: Finish this