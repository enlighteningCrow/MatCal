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

class MatrixCalculation(CommWidg):

    def __init__(self, parent: Optional['MainWindow'] = None):
        super().__init__()
        self.__ui = Ui_Form()
        self.__ui.setupUi(self)
        self.__ui.pbCal.clicked.connect(self.calculate)
        self.result = torch.empty((0))

    def getOperands(self):
        return self.mainwindow.getMatrixListModel().getMatrices()

    def getOperations(self):
        # Return a dictionary of all the operations that can be performed on two tensors with the result being a tensor in the pytorch library
        # The key is the name of the operation, and the value is the function in the pytorch library that performs the operation on two tensors

        import torch

        # operations = {
        #     'Addition': torch.add,
        #     'Subtraction': torch.sub,
        #     'Multiplication': torch.mul,
        #     'Element-wise Division': torch.div,
        #     'Matrix Multiplication': torch.matmul,
        #     'Element-wise Maximum': torch.max,
        #     'Element-wise Minimum': torch.min,
        #     'Element-wise Exponentiation': torch.pow,
        #     'Element-wise Square Root': torch.sqrt,
        #     'Element-wise Absolute': torch.abs,
        #     'Element-wise Round': torch.round,
        #     'Element-wise Trigonometric Functions': torch.sin,
        #     'Element-wise Arc Trigonometric Functions': torch.arcsin,
        #     'Element-wise Hyperbolic Trigonometric Functions': torch.sinh,
        #     'Element-wise Logarithm': torch.log,
        #     'Element-wise Logarithm (base 2)': torch.log2,
        #     'Element-wise Logarithm (base 10)': torch.log10,
        #     'Element-wise Natural Exponential': torch.exp,
        #     'Element-wise Dot Product': torch.dot,
        #     'Element-wise Modulo': torch.fmod,
        #     'Element-wise Remainder': torch.remainder,
        #     'Element-wise Clamp': torch.clamp,
        #     'Element-wise Power': torch.pow,
        #     'Element-wise Reciprocal': torch.reciprocal,
        #     'Element-wise Truncation': torch.trunc,
        #     'Element-wise Ceil': torch.ceil,
        #     'Element-wise Floor': torch.floor,
        #     'Element-wise Sign': torch.sign,
        #     'Element-wise Erf': torch.erf,
        #     'Element-wise Bessel Functions': torch.bessel,
        #     'Element-wise Log Sum Exp': torch.logsumexp,
        #     'Element-wise Log Add Exp': torch.logaddexp,
        #     'Element-wise Log Cumulative Sum Exp': torch.logcumsumexp,
        #     'Element-wise Logical And Operations': torch.logical_and,  # Example of a logical operation
        #     'Element-wise Logical Or Operations': torch.logical_or,  # Example of a logical operation
        #     'Element-wise Bitwise And Operations': torch.bitwise_and,  # Example of a bitwise operation
        #     'Element-wise Sorting': torch.sort,
        #     'Element-wise Argmax': torch.argmax,
        #     'Element-wise Argmin': torch.argmin,
        #     'Element-wise Softmax': torch.softmax,
        #     'Element-wise Sigmoid': torch.sigmoid,
        #     'Element-wise ReLU': torch.relu,
        #     'Element-wise Leaky ReLU': torch.leaky_relu,
        #     'Element-wise Softplus': torch.softplus,
        #     'Element-wise Softsign': torch.softsign,
        #     'Element-wise Hardtanh': torch.hardtanh,
        #     'Element-wise Log Sigmoid': torch.logsigmoid,
        #     'Element-wise Tanh': torch.tanh,
        #     'Element-wise GELU': torch.gelu,
        #     'Element-wise ELU': torch.elu,
        #     'Element-wise SELU': torch.selu,
        #     'Element-wise CELU': torch.celu,
        #     'Element-wise Hardswish': torch.hardswish,
        #     'Element-wise Log Softmax': torch.log_softmax,
        #     'Element-wise Pairwise Distance': torch.pairwise_distance,
        #     'Element-wise Kullback-Leibler Divergence': torch.kl_div,
        #     'Element-wise Cosine Similarity': torch.nn.functional.cosine_similarity,
        #     'Element-wise L1 Loss': torch.nn.functional.l1_loss,
        #     'Element-wise MSE Loss': torch.nn.functional.mse_loss,
        #     'Element-wise Cross-Entropy Loss': torch.nn.functional.cross_entropy,
        #     'Element-wise Binary Cross-Entropy Loss': torch.nn.functional.binary_cross_entropy,
        #     'Element-wise Triplet Margin Loss': torch.nn.functional.triplet_margin_loss,
        # }

    #     operations = {
    #         torch.add,
    # torch.sub,
    # torch.mul,
    # torch.div,
    # torch.true_divide,
    # torch.floor_divide,
    # torch.remainder,
    # torch.fmod,
    # torch.pow,
    # torch.lt,
    # torch.le,
    # torch.gt,
    # torch.ge,
    # torch.eq,
    # torch.ne,
    # torch.max,
    # torch.min,
    # torch.maximum,
    # torch.minimum,
    # torch.copysign,
    # torch.atan2,
    # torch.lerp,
    # torch.renorm,
    # torch.cross,
    # torch.dist,
    # torch.dot,
    # torch.einsum,
    # torch.ger,
    # torch.inner,
    # torch.kron,
    # torch.outer,
    # torch.mm,
    # torch.mv,
    # torch.bmm,
    # torch.baddbmm,
    # torch.addmm,
    # torch.addmv,
    # torch.matmul,
    # torch.chain_matmul,
    # torch.cdist,
    # torch.pdist,
    # torch.tensordot,
    #     }
        operations = {
            'Addition': torch.add,
            'Subtraction': torch.sub,
            'Multiplication': torch.mul,
            'Division': torch.div,
            'True Division': torch.true_divide,
            'Floor Division': torch.floor_divide,
            'Remainder': torch.remainder,
            'Modulo': torch.fmod,
            'Power': torch.pow,
            'Less Than': torch.lt,
            'Less Than or Equal To': torch.le,
            'Greater Than': torch.gt,
            'Greater Than or Equal To': torch.ge,
            'Equal': torch.eq,
            'Not Equal': torch.ne,
            'Maximum': torch.max,
            'Minimum': torch.min,
            'Element-wise Maximum': torch.maximum,
            'Element-wise Minimum': torch.minimum,
            'Copysign': torch.copysign,
            'Arc Tangent 2': torch.atan2,
            'Euclidean Distance': torch.dist,
            'Inner Product': torch.inner,
            'Kronecker Product': torch.kron,
        }

        return operations


    def updateOptions(self):
        self.__ui.cbOp1.clear()
        self.__ui.cbOp2.clear()
        self.__ui.cbOpt.clear()
        self.operands = self.getOperands()
        self.operations = self.getOperations()
        # Make the operations and operands available in the combobox from the operands and operations, which are both dictionaries.
        # Make the combo boxes have the name of the operation/operand as the text, and the value of the operation/operand as the real data,
        # where the 
        self.__ui.cbOp1.addItems(list(self.operands.keys()))
        self.__ui.cbOp2.addItems(list(self.operands.keys()))
        self.__ui.cbOpt.addItems(self.operations.keys())

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
            op = Operation(self.operands[self.__ui.cbOp1.currentText()], self.operands[self.__ui.cbOp2.currentText()], self.operations[self.__ui.cbOpt.currentText()])
            self.result = op.performOperation()
            # shouldExit = True
        except Exception as e:
            logging.exception(e)
            QMessageBox.critical(self, "Error", str(e) + "; Please try again.")
            # shouldExit = False

        if isinstance(self.result, torch.Tensor) and self.result.dim() < 3:
            self.__ui.tvRes.setTensor(self.result)
            self.__ui.stackedWidget.setCurrentIndex(0)
            # self.result = self.result.item()
        else:
            self.__ui.stackedWidget.setCurrentIndex(1)

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
        state.stackedWidgetIndex = self.__ui.stackedWidget.currentIndex()

        return state

    def loadState(self, state: SimpleNamespace):
        self.result = state.result
        self.__ui.stackedWidget.setCurrentIndex(state.stackedWidgetIndex)
        if isinstance(self.result, torch.Tensor) and self.result.dim() < 3:
            self.__ui.tvRes.setTensor(self.result)
