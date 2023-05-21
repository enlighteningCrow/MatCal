from generated.designer.ui_EquationSolver import Ui_SolvingEquationsTab

from ui.CommWidg import CommWidg
from PySide6.QtWidgets import QWidget, QMessageBox

from PySide6.QtCore import QModelIndex, QSortFilterProxyModel

from typing import *

from ui.models.EquationSolverModel import EquationSolverModel, EquationDelegate
from ui.models.VariableNamesListModel import VariableNamesListModel, VariableDelegate
from ui.models.ResultsModel import ResultsModel

if 0 != 0:
    from MainWindow import MainWindow


class EquationSolver(QWidget, CommWidg):

    def __init__(self, parent: Optional['MainWindow'] = None):
        super().__init__()
        self.__ui = Ui_SolvingEquationsTab()
        self.__ui.setupUi(self)
        # equationsModel =
        self.varModel = VariableNamesListModel(0, self)
        self.eqModel = EquationSolverModel(0, self)
        # self.eqModel.setVarNamesList(self.varModel.getVarNamesList())
        self.__ui.variableNamesList.setModel(self.varModel)
        self.__ui.equationsTable.setModel(self.eqModel)
        # self.varModel.addObservee(self.eqModel)
        self.varModel.dataChanged.connect(self.eqModel.setVarNamesList)
        self.varModel.rowsInserted.connect(
            lambda a, b, c: self.eqModel.
            insertVarNamesList(self.varModel, b, c)
        )
        self.varModel.rowsRemoved.connect(
            lambda a, b, c: self.eqModel.removeVarNamesList(b, c)
        )
        self.__ui.variableNamesList.setItemDelegate(VariableDelegate(self))
        self.__ui.equationsTable.setItemDelegate(EquationDelegate(self))

        self.__resultsModel = ResultsModel(self)
        self.__ui.resultsTable.setModel(self.__resultsModel)
        # self.varModel.dataChanged.emit(self.varModel.index(0), self.varModel.index(1))
        self.__mainwindow = None

        self.__ui.variableNamesList

    def changeSpinBoxValue(self, value: int):
        self.varModel.setUnknownsCount(value)
        self.eqModel.setUnknownsCount(value)

    def setMainWindow(self, mainwindow) -> None:
        self.__mainwindow = mainwindow
        # return super().setMainWindow(mainwindow)

    def calculate(self):
        self.__resultsModel.calculate(
            self.varModel.getVarNamesList(), self.eqModel.getEquations()
        )
