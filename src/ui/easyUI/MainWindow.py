from PySide6.QtWidgets import QMainWindow
from generated.designer.easyUI.ui_MainWindow import Ui_MainWindow

from PySide6.QtGui import QIcon, QPixmap

from ui.CommWidg import CommWidg, CommWidgPersistent

from ui.models.MatrixListModel import MatrixListModel, MatrixPair

from typing import List, TypedDict

import logging

from PySide6.QtCore import QModelIndex

from ui.dialogs.PreferencesDialog import PreferencesDialog

from ui.models.StatesListModel import State, StatesListModel

if 0 != 0:
    from accounts.AccountCreation import Account 

class MainWindow(QMainWindow):

    def __init__(self, account : 'Account'):
        super().__init__()
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        
        self.pixmap = QPixmap(":/icons/MatCalIcon.png")
        self.icon = QIcon(self.pixmap)
        self.setWindowIcon(self.icon)
        self.tabDict : TypedDict[str, CommWidg] = dict()
        self.tabList = [
            self.__ui.tabWidget.widget(j)
            for j in range(self.__ui.tabWidget.tabBar().count())
        ]
        self.__statesListModel = StatesListModel(account.states, self)
        for i in self.tabList:
            if isinstance(i, CommWidg):
                i.setMainWindow(self)
                i.isChanged.connect(
                    lambda x: self.__statesListModel.insertState(x.objectName(), *x.saveState())
                )
            else:
                logging.warning(f"Tab {i} is not a CommWidg")
            self.tabDict[i.objectName()] = i
        self.__matrixListModel.dataChanged.connect(self.saveList)

        self.__ui.tabWidget.currentChanged.emit(
            self.__ui.tabWidget.currentIndex()
        )

        self.__ui.StatesList.setModel(self.__statesListModel)
        def loadCommWidgState(x : QModelIndex):
            s : StatesListModel = x.model()
            stateData = s.getState(x)
            commWidg = self.tabDict[stateData.tabName]
            commWidg.loadState(stateData.value)
            self.__ui.tabWidget.setCurrentWidget(commWidg)
        self.__ui.StatesList.doubleClicked.connect(loadCommWidgState)

        self.__matrixListModel.dataChanged.connect(self.__ui.MatrixCalculation.updateOptions)
        self.__matrixListModel.rowsInserted.connect(self.__ui.MatrixCalculation.updateOptions)
        self.__matrixListModel.rowsRemoved.connect(self.__ui.MatrixCalculation.updateOptions)

        for c, i in enumerate(self.tabList):
            self.__ui.tabWidget.setTabVisible(c, i.objectName() in account.getTabs())
            print(self.tabList[c], i.objectName())

    def getTabWidget(self):
        return self.__ui.tabWidget

    def getTabList(self):
        return self.tabList

    def getTabDict(self):
        return self.tabDict

    def saveList(self):
        logging.info("Saved settings")

    def showPreferencesDialog(self):
        diag = PreferencesDialog(self)
        diag.exec()

    def addMatrix(self, matrix: MatrixPair):
        logging.info(f"added matrix: {matrix}")
        self.__matrixListModel.addMatrix(matrix)

    def setStateList(self, account : 'Account' ):
        self.__statesList = (account.states)

    def getMatrixListModel(self):
        return self.__matrixListModel

    def clearHistory(self):
        self.__statesListModel.clear()