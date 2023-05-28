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
        self._ui = Ui_SolvingEquationsTab()
        self._ui.setupUi(self)
        # equationsModel =
        self._varModel = VariableNamesListModel(0, self)
        self._eqModel = EquationSolverModel(0, self)
        # self.eqModel.setVarNamesList(self.varModel.getVarNamesList())
        self._ui.variableNamesList.setModel(self._varModel)
        self._ui.equationsTable.setModel(self._eqModel)
        self._lock_changed = False
        # self.varModel.addObservee(self.eqModel)
        def onVarModelChanged(a, b, c):
            if self._lock_changed:
                return
            # self.__lock_changed = True
            self._eqModel.setVarNamesList(a, b)
            self.isChanged.emit(self)
            # self.__lock_changed = False
        self._varModel.dataChanged.connect(onVarModelChanged)
        def onEqModelChanged(a, b, c):
            if self._lock_changed:
                return
            # self.__lock_changed = True
            self.isChanged.emit(self)
            # self.__lock_changed = False
        self._eqModel.dataChanged.connect(onEqModelChanged)
        # self._varModel.dataChanged.connect(lambda: self.isChanged.emit(self))
        self._varModel.rowsInserted.connect(
            lambda a, b, c: self._eqModel.
            insertVarNamesList(self._varModel, b, c)
        )
        # self._varModel.rowsInserted.connect(lambda: self.isChanged.emit(self))
        self._varModel.rowsRemoved.connect(
            lambda a, b, c: self._eqModel.removeVarNamesList(b, c)
        )
        # self._varModel.rowsRemoved.connect(lambda: self.isChanged.emit(self))
        self._ui.variableNamesList.setItemDelegate(VariableDelegate(self))
        self._ui.equationsTable.setItemDelegate(EquationDelegate(self))

        self._resultsModel = ResultsModel(self)
        self._ui.resultsTable.setModel(self._resultsModel)

        setMaxWidth(self._ui.variableNamesWidget, self._ui.variableNamesList)

        # self.varModel.dataChanged.emit(self.varModel.index(0), self.varModel.index(1))
        self.__mainwindow = None

        self._ui.variableNamesList

    def changeSpinBoxValue(self, value: int):
        if self._lock_changed:
            return 
        self._varModel.setUnknownsCount(value)
        self._eqModel.setUnknownsCount(value)
        self.isChanged.emit(self)

    def setMainWindow(self, mainwindow) -> None:
        self.__mainwindow = mainwindow
        # return super().setMainWindow(mainwindow)

    def calculate(self):
        self._resultsModel.calculate(
            self._varModel.getVarNamesList(), self._eqModel.getEquations()
        )
        self.isChanged.emit(self)

    def getMainWindow(self):
        return self.__mainwindow

    def needsTensorsTab(self) -> bool:
        return False

from types import SimpleNamespace

class EquationSolverPersistent(EquationSolver, CommWidgPersistent):

    def __init__(self, parent: Union['MainWindow', None] = None):
        super().__init__(parent)

    # Return an object containing all the information that has to be saved to be able to restore the state of the widget and all of the models and views of the widget
    def saveState(self):
        # return {
        #     "varModel": self._varModel.saveState(),
        #     "eqModel": self._eqModel.saveState(),
        #     "resultsModel": self._resultsModel.saveState()
        # }
        s = SimpleNamespace()
        s_var, s.varModel = self._varModel.saveState()
        s_eq, s.eqModel = self._eqModel.saveState()
        s_rs, s.resultsModel = self._resultsModel.saveState()
        s.numVars = self._ui.spinBox.value()
        return " ;; ".join([s_var, s_eq, s_rs]), s

    # Restore the state of the widget and all of the models and views of the widget
    def loadState(self, state: SimpleNamespace):
        # self._varModel.loadState(state["varModel"])
        # self._eqModel.loadState(state["eqModel"])
        # self._resultsModel.loadState(state["resultsModel"])
        self._lock_changed = True
        self._resultsModel.disableSaving()
        self._varModel.disableSaving()
        self._eqModel.disableSaving()
        self._resultsModel.loadState(state.resultsModel)
        self._varModel.loadState(state.varModel)
        self._eqModel.loadState(state.eqModel)
        self._ui.spinBox.setValue(state.numVars)
        self._eqModel.enableSaving()
        self._varModel.enableSaving()
        self._resultsModel.enableSaving()
        self._lock_changed = False
        # self.isChanged.emit(self)
