from PySide6.QtWidgets import QMainWindow
from ui_MainWindow import Ui_MainWindow

from PySide6.QtGui import QStandardItem, QStandardItemModel


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        # self.setupUi(self)
        self.matrixList = QStandardItemModel()
        self.__ui.listView.setModel(self.matrixList)
        for i in [QStandardItem("ajsio"), QStandardItem("bsdf09h"),
                  QStandardItem("cjoasidg0")]:
            self.matrixList.appendRow(i)
        # self.


#-TODO: (PRIORITY): Try removing the current MatrixEditor.py altogether,
# and replace it with the current MatrixEditor.py. Also consider making
# the matrix editor only pop up when the list is clicked, such that the user
# makes an action to modify an existing matrix in the list or create a new one.
