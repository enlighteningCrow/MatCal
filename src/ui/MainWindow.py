from PySide6.QtWidgets import QMainWindow, QDialog
from generated.designer.ui_MainWindow import Ui_MainWindow

from PySide6.QtGui import QIcon, QImage, QPixmap

from src.ui.CommWidg import CommWidg

from src.ui.models.MatrixListModel import MatrixListModel, MatrixPair

from typing import List

import logging

from PySide6.QtCore import QModelIndex, QSettings, QFile

from generated.resources import rcc_resources

from src.ui.dialogs.PreferencesDialog import PreferencesDialog

# rcc_resources.initResources()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        # self.setupUi(self)
        self.settings = QSettings()
        matrixList: List[MatrixPair] = []
        try:
            matrixList = self.settings.value('matrixList', [])
            if not isinstance(matrixList, list):
                raise RuntimeError("Settings for matrixList has invalid type")
        except Exception as e:
            logging.error(str(e))
            logging.error("Resetting value of matrixList to", [])
            self.settings.clear()
            matrixList = []
        # matrixList = []
        self.matrixListModel = MatrixListModel(matrixList, self.__ui.listView)
        # self.matrixList = ListModel(matrixList, self.__ui.listView)
        self.__ui.listView.setModel(self.matrixListModel)
        self.pixmap = QPixmap(":/icons/MatCalIcon.png")
        self.icon = QIcon(self.pixmap)
        self.setWindowIcon(self.icon)
        self.tabDict = dict()
        self.tabList = [self.__ui.tabWidget.widget(j)
                        for j in range(self.__ui.tabWidget.tabBar().count())]
        for i in self.tabList:
            if isinstance(i, CommWidg):
                i.setMainWindow(self)
            self.tabDict[i.objectName()] = i
        self.matrixListModel.dataChanged.connect(self.saveSettings)

    def getTabWidget(self):
        return self.__ui.tabWidget

    def getTabList(self):
        return self.tabList

    def getTabDict(self):
        return self.tabDict

    def saveSettings(self):
        print("Saved settings")
        self.settings.setValue(
            'matrixList', self.matrixListModel.getMatrixList())
# In PySide6, demonstrate how to save the state of a subclass of QAbstractListModel

    def showPreferencesDialog(self):
        print("showPreferencesDialog")
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
        logging.info("added matrix:", matrix)
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
