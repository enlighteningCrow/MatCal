from PySide6.QtWidgets import QMainWindow, QAbstractItemView
from ui_MainWindow import Ui_MainWindow

from PySide6.QtGui import QStandardItem, QStandardItemModel, QIcon, QPixmap

from CommWidg import CommWidg

from MatrixListModel import DuplicateValueError, MatrixListModel, MatrixPair

from typing import Tuple, List

from torch import Tensor

import logging

from PySide6.QtCore import QModelIndex, QSettings


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        # self.setupUi(self)
        matrixList = []
        self.matrixListModel = MatrixListModel(matrixList, self.__ui.listView)
        # self.matrixList = ListModel(matrixList, self.__ui.listView)
        self.__ui.listView.setModel(self.matrixListModel)
        # for i in [QStandardItem("ajsio"), QStandardItem("bsdf09h"),
        #           QStandardItem("cjoasidg0")]:
        #     self.matrixList.appendRow(i)
        self.pixmap = QPixmap('resources/MatCalIcon.png')
        self.icon = QIcon(self.pixmap)
        self.setWindowIcon(self.icon)
        for i in (self.__ui.tabWidget.widget(j)
                  for j in range(self.__ui.tabWidget.tabBar().count())):
            if isinstance(i, CommWidg):
                i.setMainWindow(self)

# In PySide6, demonstrate how to save the state of a subclass of QAbstractListModel
        self.settings = QSettings()

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


#-TODO: (PRIORITY): Try removing the current MatrixEditor.py altogether,
# and replace it with the current MatrixEditor.py. Also consider making
# the matrix editor only pop up when the list is clicked, such that the user
# makes an action to modify an existing matrix in the list or create a new one.
