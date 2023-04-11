from PySide6.QtWidgets import QWidget
from ui_SearchListView import Ui_Form

from PySide6.QtCore import QAbstractListModel, QSortFilterProxyModel, Qt, QIdentityProxyModel

from MatrixListModel import MatrixPair


class NameProxy(QIdentityProxyModel):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            pair: MatrixPair = self.sourceModel().data(
                self.mapToSource(index), role
            )
            assert (isinstance(pair, MatrixPair))
            return pair.name


class SearchListView(QWidget):

    def __init__(self, parent=None):
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

    def setModel(self, model: QAbstractListModel):
        self.__model = model
        self.__proxyName.setSourceModel(model)
        self.__proxyFilter.setSourceModel(self.__proxyName)
        self.__ui.listView.setModel(self.__proxyFilter)

    def getListView(self):
        return self.__ui.listView

    def updateSearch(self, text):
        self.__proxyFilter.setFilterFixedString(text)
