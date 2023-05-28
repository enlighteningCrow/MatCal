# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QWidget, QMessageBox

from PySide6.QtCore import QModelIndex, QSortFilterProxyModel

import torch
from torch import Tensor

from typing import Tuple, Union, Optional

# from ui_DIndexLabels import Ui_Form
from generated.designer.ui_MatrixEditor import Ui_Form
# from src.ui.MainWindow import MainWindow

from ui.models.NNIntSI import NNIntSI, NNIntSIM
from ui.delegates.SpinBoxDelegate import SpinBoxDelegate, IndexSpinBoxDelegate

import logging

from ui.CommWidg import CommWidg, CommWidgPersistent

from ui.models.MatrixListModel import MatrixListModel

from ui.views.SearchListView import NameProxy

from ui.dialogs.MatrixListDialogs import saveMatrix

from ui.utils import setMaxWidth

from types import SimpleNamespace

# - TODO: Use a stackedwidget or something to swap between with 0 dimensions (1 lineedit), 1 dimension (1 row/column of lineedit), 2 dimensions (matrix of lineedits), 3+ dimensions (matrix of lineedits in selectable dimensions for columns and rows, with other dimensions selected with the spinboxes)
# TODO: Make all the hardcoded values of the columns size and selection, and replace them with an attribute

if 0 != 0:
    from src.ui.MainWindow import MainWindow
    # from MainWindow import MainWindow

from generated.designer.ui_MatrixCalculation import Ui_Form

from app.Operation import Operation

from ui.dialogs.MatrixListDialogs import saveMatrix

from app.TensorOperation import TensorOperation, TensorOperationMenu

class MatrixCalculation(CommWidg):

    def __init__(self, parent: Optional['MainWindow'] = None):
        super().__init__()
        self._ui = Ui_Form()
        self._ui.setupUi(self)
        self._ui.pbCal.clicked.connect(self.calculate)
        self.result = torch.empty((0))
        self.menu = TensorOperationMenu()

    def getOperands(self):
        return self.mainwindow.getMatrixListModel().getMatrices()

    def updateOptions(self):
        self._ui.cbOp1.clear()
        self._ui.cbOp2.clear()
        self._ui.cbOpt.clear()
        self.operands = self.getOperands()
        self.operations = self.menu.getOperations()
        # Make the operations and operands available in the combobox from the operands and operations, which are both dictionaries.
        # Make the combo boxes have the name of the operation/operand as the text, and the value of the operation/operand as the real data,
        # where the 
        self._ui.cbOp1.addItems(list(self.operands.keys()))
        self._ui.cbOp2.addItems(list(self.operands.keys()))
        self._ui.cbOpt.addItems(self.operations.keys())

    def setMainWindow(self, mainwindow: 'MainWindow') -> None:
        self.mainwindow = mainwindow
        self.updateOptions()

    def getMainWindow(self):
        return self.mainwindow

    def needsTensorsTab(self) -> bool:
        return True

    def calculate(self):
        self.result = None
        # shouldExit = False
        # while not shouldExit:
        #     shouldExit = False
        try:
            #Modify this line to get the correct operands (tensors) and operations (functions) from the ui combo boxes together with the self.operands and self.operations dictionaries
            op = Operation(self.operands[self._ui.cbOp1.currentText()], self.operands[self._ui.cbOp2.currentText()], self.operations[self._ui.cbOpt.currentText()])
            op.performOperation()
            self.result = op.getResult()
            # shouldExit = True
        except Exception as e:
            logging.exception(e)
            QMessageBox.critical(self, "Error", str(e) + "; Please try again.")
            # shouldExit = False

        if isinstance(self.result, torch.Tensor) and self.result.dim() < 3:
            self._ui.tvRes.setTensor(self.result)
            self._ui.stackedWidget.setCurrentIndex(0)
            # self.result = self.result.item()
        else:
            self._ui.stackedWidget.setCurrentIndex(1)

        self.isChanged.emit(self)
        return self.result



    def saveMatrix(self):
        if self.result is None:
            return
        if self.mainwindow is None:
            return
        saveMatrix(self.result, self.mainwindow, self)
        # self.mainwindow.saveMatrixList(self.result)


class MatrixCalculationPersistent(MatrixCalculation, CommWidgPersistent):
    def __init__(self, parent= None):
        super().__init__()
        self.__savingDisabled = False


    def disableSaving(self):
        self.__savingDisabled = True

    def enableSaving(self):
        self.__savingDisabled = False

    def saveState(self) -> Tuple[str, SimpleNamespace]:
        if self.__savingDisabled:
            return None
        state = SimpleNamespace()
        # state.op1 = self.__ui.cbOp1.currentText()
        # state.op2 = self.__ui.cbOp2.currentText()
        # state.opt = self.__ui.cbOpt.currentText()
        state.result = self.result
        state.stackedWidgetIndex = self._ui.stackedWidget.currentIndex()

        return state

    def loadState(self, state: SimpleNamespace):
        self.result = state.result
        self._ui.stackedWidget.setCurrentIndex(state.stackedWidgetIndex)
        if isinstance(self.result, torch.Tensor) and self.result.dim() < 3:
            self._ui.tvRes.setTensor(self.result)
