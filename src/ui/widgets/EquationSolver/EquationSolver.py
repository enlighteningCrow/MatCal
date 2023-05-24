from typing import Optional
from generated.designer.ui_EquationSolver import Ui_SolvingEquationsTab

from ui.CommWidg import CommWidg, CommWidgPersistent
from PySide6.QtWidgets import QWidget, QMessageBox

from PySide6.QtCore import QModelIndex, QSortFilterProxyModel

from typing import *

from ui.models.EquationSolverModel import EquationSolverModel, EquationDelegate
from ui.models.VariableNamesListModel import VariableNamesListModel, VariableDelegate
from ui.models.ResultsModel import ResultsModel

from ui.utils import setMaxWidth

if 0 != 0:
    from src.ui.MainWindow import MainWindow
    # from MainWindow import MainWindow


class EquationSolver(CommWidg):

    def __init__(self, parent: Optional['MainWindow'] = None):
        super().__init__()
        self.__ui = Ui_SolvingEquationsTab()
        self.__ui.setupUi(self)
        # equationsModel =
        self.__varModel = VariableNamesListModel(0, self)
        self.__eqModel = EquationSolverModel(0, self)
        # self.eqModel.setVarNamesList(self.varModel.getVarNamesList())
        self.__ui.variableNamesList.setModel(self.__varModel)
        self.__ui.equationsTable.setModel(self.__eqModel)
        # self.varModel.addObservee(self.eqModel)
        self.__varModel.dataChanged.connect(self.__eqModel.setVarNamesList)
        self.__varModel.dataChanged.connect(lambda: self.isChanged.emit(self))
        self.__varModel.rowsInserted.connect(
            lambda a, b, c: self.__eqModel.
            insertVarNamesList(self.__varModel, b, c)
        )
        self.__varModel.rowsInserted.connect(lambda: self.isChanged.emit(self))
        self.__varModel.rowsRemoved.connect(
            lambda a, b, c: self.__eqModel.removeVarNamesList(b, c)
        )
        self.__varModel.rowsRemoved.connect(lambda: self.isChanged.emit(self))
        self.__ui.variableNamesList.setItemDelegate(VariableDelegate(self))
        self.__ui.equationsTable.setItemDelegate(EquationDelegate(self))

        self.__resultsModel = ResultsModel(self)
        self.__ui.resultsTable.setModel(self.__resultsModel)

        setMaxWidth(self.__ui.variableNamesWidget, self.__ui.variableNamesList)

        # self.varModel.dataChanged.emit(self.varModel.index(0), self.varModel.index(1))
        self.__mainwindow = None

        self.__ui.variableNamesList

    def changeSpinBoxValue(self, value: int):
        self.__varModel.setUnknownsCount(value)
        self.__eqModel.setUnknownsCount(value)
        self.isChanged.emit(self)

    def setMainWindow(self, mainwindow) -> None:
        self.__mainwindow = mainwindow
        # return super().setMainWindow(mainwindow)

    def calculate(self):
        self.__resultsModel.calculate(
            self.__varModel.getVarNamesList(), self.__eqModel.getEquations()
        )
        self.isChanged.emit(self)

    def getMainWindow(self):
        return self.__mainwindow

    def needsTensorsTab(self) -> bool:
        return False


class EquationSolverPersistent(EquationSolver, CommWidgPersistent):

    def __init__(self, parent: Union['MainWindow', None] = None):
        super().__init__(parent)

    # Return an object containing all the information that has to be saved to be able to restore the state of the widget and all of the models and views of the widget
    def saveState(self):
        return {
            "varModel": self.__varModel.saveState(),
            "eqModel": self.__eqModel.saveState(),
            "resultsModel": self.__resultsModel.saveState()
        }

    # Restore the state of the widget and all of the models and views of the widget
    def loadState(self, state: dict):
        self.__varModel.loadState(state["varModel"])
        self.__eqModel.loadState(state["eqModel"])
        self.__resultsModel.loadState(state["resultsModel"])