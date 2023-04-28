from PySide6.QtWidgets import QWidget, QMenu
from generated.designer.ui_SearchListView import Ui_Form

from PySide6.QtCore import QAbstractListModel, QSortFilterProxyModel, Qt, QIdentityProxyModel
from PySide6.QtGui import QAction

from src.ui.models.MatrixListModel import MatrixPair
from typing import Union, Optional

from types import SimpleNamespace

from src.ui.dialogs.MatrixListDialogs import saveMatrix

import logging

if 1 < 0:
    from MainWindow import MainWindow


class NameProxy(QIdentityProxyModel):

    def __init__(self, parent = None) -> None:
        super().__init__(parent)

    def data(self, index, role = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            pair: MatrixPair = self.sourceModel().data(
                self.mapToSource(index), role
            )
            assert (isinstance(pair, MatrixPair))
            return pair.name


if 1 < 0:
    from src.ui.MainWindow import MainWindow


class SearchListView(QWidget):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.__ui = Ui_Form()
        self.__ui.setupUi(self)
        self.__model = None
        # self.__proxyFilter = None
        # self.__proxyName = None
        self.__proxyFilter = QSortFilterProxyModel(self.__ui.listView)
        self.__proxyName = NameProxy(self.__ui.listView)
        self.__proxyFilter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.__ui.searchBar.textChanged.connect(self.updateSearch)

        # self.mainWindow: MainWindow = parent
        self.mainWindow: Optional["MainWindow"] = None
        # while self.mainWindow is not None and not isinstance(self.mainWindow, MainWindow):

        # Add actions
        # self.__ui.listView.addAction(self.__ui.actionEdit)
        # self.__ui.listView.addAction(self.__ui.actionDelete)
        # self.__ui.listView.addAction(self.__ui.actionDuplicate)
        # self.__ui.listView.addAction(self.__ui.actionSave)
        # self.__ui.listView.addAction(self.__ui.actionOpen)
        # self.__ui.listView.addAction(self.__ui.actionDelete)
        # self.__ui.listView.addAction(self.__ui.actionRename)
        # self.__ui.listView.addAction(self.__ui.actionClear)
        # self.__ui.listView.addAction(self.__ui.actionCalculate_First_Operand)
        # self.__ui.listView.addAction(self.__ui.actionCalculate_Second_Operand)
        # self.__ui.listView.addAction(self.__ui.actionCalculate_Single_Operand)
        # print(locals(self.__u))
        # print(self.__ui.__dict__)
        self.contextMenu = QMenu(self.__ui.listView)
        for i, j in self.__ui.__dict__.items():
            if type(j) is QAction:
                logging.info(f"Action name: {i}")
                self.__ui.listView.addAction(j)
                self.contextMenu.addAction(j)
                # print(i, j)
            # print(i)

    def getActionArguments(self):
        # print(self.__ui.listView.currentIndex())
        # print(self.__ui.listView.model())
        # print(self.__proxyName.mapToSource(self.__ui.listView.currentIndex()))
        # print(self.__proxyFilter.mapToSource(
        #     self.__ui.listView.currentIndex()))
        # print(self.__proxyName.mapToSource(
        #     self.__proxyFilter.mapToSource(self.__ui.listView.currentIndex())))
        # print(self.__proxyName.sourceModel())
        # print(self.__proxyFilter.sourceModel())
        # assert (self.__proxyName.sourceModel() == self.__model)
        # print(
        #     self.__ui.listView.currentIndex(),
        #     self.__ui.listView.model(),
        #     self.__proxyName.mapToSource(
        #         self.__proxyFilter.mapToSource(
        #             self.__ui.listView.currentIndex()
        #         )
        #     ),
        #     self.__proxyName.sourceModel(), sep='\n'
        # )
        # assert (isinstance(self.parent(), MainWindow))
        from src.ui.MainWindow import MainWindow
        if self.mainWindow is None:
            self.mainWindow = self
            while self.mainWindow is not None and not isinstance(
                    self.mainWindow, MainWindow):
                self.mainWindow = self.mainWindow.parent()
        if self.mainWindow is None:
            return
        # parent: MainWindow = self.parent()

        # index, model, sourceIndex, sourceModel, mainWindow, tabWidget, tabDict

        sn = SimpleNamespace(
            index = self.__ui.listView.currentIndex(),
            model = self.__ui.listView.model(),
            sourceIndex = self.__proxyName.mapToSource(
                self.__proxyFilter.mapToSource(
                    self.__ui.listView.currentIndex()
                )
            ),
            sourceModel = self.__proxyName.sourceModel(),
            mainWindow = self.mainWindow,
            tabWidget = self.mainWindow.getTabWidget(),
            tabDict = self.mainWindow.getTabDict(),
            tabList = self.mainWindow.getTabList()
        )
        return sn

    def actionEditSlot(self):
        args = self.getActionArguments()
        args.tabWidget.setCurrentIndex(args.tabDict["MatrixEditor"])
        # args.mainWindow.getMatrixEditor().setModel(args.sourceModel)
        # TODO: This: Look from line 123 from MatrixEditor.py
        args.mainWindow.getMatrixEditor().setMatrix(
            args.sourceModel.data(args.sourceIndex)
        )

    def actionDeleteSlot(self):
        args = self.getActionArguments()
        args.sourceModel.removeRow(args.sourceIndex.row())

    def actionDuplicateSlot(self):
        args = self.getActionArguments()
        saveMatrix(
            args.sourceModel.data(args.sourceIndex), args.mainWindow, self
        )

    def actionSaveSlot(self):
        args = self.getActionArguments()

    def actionOpenSlot(self):
        args = self.getActionArguments()

    def actionRenameSlot(self):
        args = self.getActionArguments()

    def actionCalculate_Single_OperandSlot(self):
        args = self.getActionArguments()

    def actionCalculate_First_OperandSlot(self):
        args = self.getActionArguments()

    def actionCalculate_Second_OperandSlot(self):
        args = self.getActionArguments()

    def actionClearSlot(self):
        args = self.getActionArguments()

    # def
    def eventFilter(self, obj, event):
        if obj == self.__ui.listView and event.type() == QEvent.ContextMenu:
            index = self.__ui.listView.indexAt(event.pos())
            if index.isValid():
                self.contextMenu.exec(event.globalPos())
                return True
        return super().eventFilter(obj, event)

    def setModel(self, model: QAbstractListModel):
        self.__model = model
        self.__proxyName.setSourceModel(model)
        self.__proxyFilter.setSourceModel(self.__proxyName)
        self.__ui.listView.setModel(self.__proxyFilter)

    def getListView(self):
        return self.__ui.listView

    def updateSearch(self, text):
        self.__proxyFilter.setFilterFixedString(text)
