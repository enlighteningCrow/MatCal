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

# rcc_resources.initResources()

if 0 != 0:
    from accounts.AccountCreation import Account 

class MainWindow(QMainWindow):

    def __init__(self, account : 'Account'):
        super().__init__()
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        
        # self.__matrixListModel = MatrixListModel(self.__ui.listView)
        # self.matrixList = ListModel(matrixList, self.__ui.listView)
        # self.__ui.listView.setModel(self.__matrixListModel)
        self.pixmap = QPixmap(":/icons/MatCalIcon.png")
        self.icon = QIcon(self.pixmap)
        self.setWindowIcon(self.icon)
        self.tabDict : TypedDict[str, CommWidg] = dict()
        self.tabList = [
            self.__ui.tabWidget.widget(j)
            for j in range(self.__ui.tabWidget.tabBar().count())
        ]
        # TODO: (Urgent) Look at the bottom TODO; make it connect to this list or make it contain the list in itself.
        self.__statesListModel = StatesListModel(account.states, self)
        for i in self.tabList:
            if isinstance(i, CommWidg):
                i.setMainWindow(self)
                i.isChanged.connect(
                    #TODO: This, and implement a method for loading the state and setting the active tab when double clicked
                    #TODO: Make this add the tab widget (or index) and the state as a simple namespace
                    lambda x: self.__statesListModel.insertState(x.objectName(), *x.saveState())
                )
            else:
                logging.warning(f"Tab {i} is not a CommWidg")
            self.tabDict[i.objectName()] = i
        self.__matrixListModel.dataChanged.connect(self.saveList)

        self.__ui.tabWidget.currentChanged.connect(
            # lambda x: self.__ui.listView.show() if self.__ui.tabWidget.
            # widget(x).needsTensorsTab() else self.__ui.listView.hide()
        )
        self.__ui.tabWidget.currentChanged.emit(
            self.__ui.tabWidget.currentIndex()
        )

        #TODO: Make a class inheriting from the

        self.__ui.StatesList.setModel(self.__statesListModel)
        #TODO: Check if this is correct
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
            #asdfg
            print(self.tabList[c], i.objectName())
        # for i in account.getTabs():


    def getTabWidget(self):
        return self.__ui.tabWidget

    def getTabList(self):
        return self.tabList

    def getTabDict(self):
        return self.tabDict

    def saveList(self):
        logging.info("Saved settings")
        # self.settings.setValue(
        #     'matrixList', self.matrixListModel.getMatrixList())
# In PySide6, demonstrate how to save the state of a subclass of QAbstractListModel

    def showPreferencesDialog(self):
        # print("showPreferencesDialog")
        diag = PreferencesDialog(self)
        diag.exec()
        # diag.
        # diag.show()
        # diag.exec()

    # def connectSelectionChangedSignal(self, slot):
    #     # self.__ui.listView.selectionChanged.connect(slot)
    #     self.__ui.listView.getListView().selectionModel(
    #     ).selectionChanged.connect(slot)

    # def getSelectedMatrix(self) -> List[QModelIndex]:
    #     return self.__ui.listView.getListView().selectedIndexes()
        # self.

    def addMatrix(self, matrix: MatrixPair):
        logging.info(f"added matrix: {matrix}")
        # self.matrixList.addMatrix(matrix)
        # self.matrixList.layoutChanged.emit()
        # self.__ui.listView.updateEditorData()
        # self.matrixList.
        # self.matrixList.insertRow(0, matrix)
        self.__matrixListModel.addMatrix(matrix)

    def setStateList(self, account : 'Account' ):
        self.__statesList = (account.states)

    def getMatrixListModel(self):
        return self.__matrixListModel

    def clearHistory(self):
        self.__statesListModel.clear()


# -TODO: (PRIORITY): Try removing the current MatrixEditor.py altogether,
# and replace it with the current MatrixEditor.py. Also consider making
# the matrix editor only pop up when the list is clicked, such that the user
# makes an action to modify an existing matrix in the list or create a new one.

#TODO: (PRIORITY): Make the listView on the right of all screens to be a subclass of listview, and set its model such that it goes to whatever widget the item was created in
#TODO: (PRIORITY): Make the CommViews all store the data everytime anything is changed. Maybe make a signal in all of the CommWidgs, and make the CommWidgs the subclass of QWidget instead of all the others.