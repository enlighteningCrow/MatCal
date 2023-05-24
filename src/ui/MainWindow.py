from PySide6.QtWidgets import QMainWindow
from generated.designer.ui_MainWindow import Ui_MainWindow

from PySide6.QtGui import QIcon, QPixmap

from ui.CommWidg import CommWidg

from ui.models.MatrixListModel import MatrixListModel, MatrixPair

from typing import List

import logging

from PySide6.QtCore import QModelIndex

from ui.dialogs.PreferencesDialog import PreferencesDialog

# rcc_resources.initResources()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        # self.setupUi(self)
        # self.settings = QSettings()
        # matrixList: List[MatrixPair] = []
        # TODO: ZODB for matrixList
        # try:
        #     matrixList = self.settings.value('matrixList', [])
        #     if not isinstance(matrixList, list):
        #         raise RuntimeError("Settings for matrixList has invalid type")
        # except Exception as e:
        #     logging.error(str(e))
        #     logging.error("Resetting value of matrixList to", [])
        #     self.settings.clear()
        #     matrixList = []
        # matrixList = []
        self.matrixListModel = MatrixListModel(self.__ui.listView)
        # self.matrixList = ListModel(matrixList, self.__ui.listView)
        self.__ui.listView.setModel(self.matrixListModel)
        self.pixmap = QPixmap(":/icons/MatCalIcon.png")
        self.icon = QIcon(self.pixmap)
        self.setWindowIcon(self.icon)
        self.tabDict = dict()
        self.tabList = [
            self.__ui.tabWidget.widget(j)
            for j in range(self.__ui.tabWidget.tabBar().count())
        ]
        # TODO: (Urgent) Look at the bottom TODO; make it connect to this list or make it contain the list in itself.
        self.__statesListModel = StatesListModel
        for i in self.tabList:
            if isinstance(i, CommWidg):
                i.setMainWindow(self)
            self.tabDict[i.objectName()] = i
            i.isChanged.connect(
                #TODO: This, and implement a method for loading the state and setting the active tab when double clicked
                lambda x: self.__statesListModel.insertState(x.saveState())
            )
        self.matrixListModel.dataChanged.connect(self.saveList)

        self.__ui.tabWidget.currentChanged.connect(
            lambda x: self.__ui.listView.show() if self.__ui.tabWidget.
            widget(x).needsTensorsTab() else self.__ui.listView.hide()
        )
        self.__ui.tabWidget.currentChanged.emit(
            self.__ui.tabWidget.currentIndex()
        )

        #TODO: Make a class inheriting from the

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

    def connectSelectionChangedSignal(self, slot):
        # self.__ui.listView.selectionChanged.connect(slot)
        self.__ui.listView.getListView().selectionModel(
        ).selectionChanged.connect(slot)

    def getSelectedMatrix(self) -> List[QModelIndex]:
        return self.__ui.listView.getListView().selectedIndexes()
        # self.

    def addMatrix(self, matrix: MatrixPair):
        logging.info(f"added matrix: {matrix}")
        # self.matrixList.addMatrix(matrix)
        # self.matrixList.layoutChanged.emit()
        # self.__ui.listView.updateEditorData()
        # self.matrixList.
        # self.matrixList.insertRow(0, matrix)
        self.matrixListModel.addMatrix(matrix)


# -TODO: (PRIORITY): Try removing the current MatrixEditor.py altogether,
# and replace it with the current MatrixEditor.py. Also consider making
# the matrix editor only pop up when the list is clicked, such that the user
# makes an action to modify an existing matrix in the list or create a new one.

#TODO: (PRIORITY): Make the listView on the right of all screens to be a subclass of listview, and set its model such that it goes to whatever widget the item was created in
#TODO: (PRIORITY): Make the CommViews all store the data everytime anything is changed. Maybe make a signal in all of the CommWidgs, and make the CommWidgs the subclass of QWidget instead of all the others.