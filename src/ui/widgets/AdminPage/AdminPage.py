from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QModelIndex, QAbstractListModel
from generated.designer.ui_AdminPage import Ui_Form

from ui.CommWidg import CommWidg, CommWidgPersistent
from BTrees.OOBTree import OOBTree

from persistent.list import PersistentList as plist

from db.Storage import getProperty
if 0 != 0:
    from ui.MainWindow import MainWindow

class OOBTreeModel(QAbstractListModel):
    def __init__(self, tree: OOBTree, parent=None):
        super().__init__()
        self.__tree = tree
        self.__keys = list(tree.keys())
        self.__values = list(tree.values())

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.__tree)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self.__values[index.row()].username

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.__keys[section]
            else:
                return section

    def removeRows(self, row: int, count: int, parent: QModelIndex = QModelIndex()) -> bool:
        self.beginRemoveRows(parent, row, row + count - 1)
        for i in range(count):
            self.__tree.pop(self.__keys[row + i])
        self.endRemoveRows()
        return True

class PListModel(QAbstractListModel):
    def __init__(self, history : plist = plist(), parent=None):
        super().__init__(parent)
        self.__list = history

    def setHistory(self, history : plist):
        self.beginResetModel()
        self.__list = history
        self.endResetModel()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.__list)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self.__list[index.row()]

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.__keys[section]
            else:
                return section

    def removeRows(self, row: int, count: int, parent: QModelIndex = QModelIndex()) -> bool:
        self.beginRemoveRows(parent, row, row + count - 1)
        for i in range(count):
            self.__list.pop(row + i)
        self.endRemoveRows()
        return True

class AdminPage(CommWidg):
    def __init__(self, parent=None):
        super().__init__()
        self.__ui = Ui_Form()
        self.__ui.setupUi(self)
        self.__mainWindow = None
        self.__accounts = getProperty('accounts', OOBTree())
        self.__accountsModel = OOBTreeModel(self.__accounts)
        self.__historyModel = PListModel()
        self.__accountsModel.beginResetModel()
        self.__historyModel.beginResetModel()
        self.__historyModel.endResetModel()
        self.__accountsModel.endResetModel()
        # self.__ui.accoun
        self.__ui.lvAccounts.setModel(self.__accountsModel)
        self.__ui.gbHistory.setVisible(False)
        #TODO: Reset the model and see if it works

    def deleteSelectedAccount(self):
        index = self.__ui.lvAccounts.currentIndex()
        if index.isValid():
            self.__accountsModel.removeRows(index.row(), 1)

    def selectAccount(self, index : QModelIndex):
        account = self.__accountsModel.data(index)
        self.__historyModel.setHistory(account.states)

    def setMainWindow(self, mainwindow : 'MainWindow'):
        # self.__accounts = mainwindow.getAccounts()
        self.__mainWindow = mainwindow

    def getMainWindow(self):
        return self.__mainWindow

    def needsTensorsTab(self):
        return False
