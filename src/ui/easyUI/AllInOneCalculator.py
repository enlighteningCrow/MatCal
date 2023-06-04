from generated.designer.easyUI.ui_AllInOneCalculator import Ui_Form

from ui.CommWidg import CommWidg, CommWidgPersistent

import logging

from PySide6.QtWidgets import QWidget, QApplication, QLineEdit, QSpinBox, QDoubleSpinBox, QMessageBox

from types import SimpleNamespace

from app.TensorOperation import TensorOperation
from app.UnaryOperation import TensorUnaryOperation, BinaryUnaryOperation, UnaryOperation

import torch

class AllInOneCalculator(CommWidg):
    def __init__(self, parent = None):
        CommWidg.__init__(self, parent)
        self._ui = Ui_Form()
        self._ui.setupUi(self)

        self.__mainwindow = None
        for i in ['int', 'Tensor', 'float', 'binary']:
            self._ui.opr0Type.addItem(i)
            self._ui.opr1Type.addItem(i)

        self._ui.opr0Type.currentTextChanged.connect(self.__opr0TypeChanged)
        self._ui.opr1Type.currentTextChanged.connect(self.__opr1TypeChanged)
        QApplication.instance().focusChanged.connect(self.__focusChanged)
        self.__opr0TypeChanged(self._ui.opr0Type.currentText())
        self.__opr1TypeChanged(self._ui.opr1Type.currentText())

    def __focusChanged(self, a, b):
        print("Changed input to", b)
        for i in range(self._ui.numpad.count()):
            self._ui.numpad.widget(i).setInputLine(b)

    def __opr0TypeChanged(self, text):
        self._ui.opr0Widg.promptData(text)
        if text == 'Tensor':
            self._ui.opr0Unary.setCurrentIndex(1)
            if self._ui.opr1Type.currentText() == 'Tensor':
                self._ui.pbMatmul.show()
                self._ui.pbDistance.show()
            else:
                self._ui.pbMatmul.hide()
                self._ui.pbDistance.hide()
        else:
            self._ui.pbMatmul.hide()
            self._ui.pbDistance.hide()
            self._ui.opr0Unary.setCurrentIndex(0)
            if text == 'float':
                self._ui.BinaryNot.hide()
            else:
                self._ui.BinaryNot.show()

        if text == 'binary':
            self._ui.numpad.setCurrentIndex(1)
        else:
            self._ui.numpad.setCurrentIndex(0)
    
    def __opr1TypeChanged(self, text):
        self._ui.opr1Widg.promptData(text)
        if text == 'Tensor':
            self._ui.opr1Unary.setCurrentIndex(1)
            if self._ui.opr0Type.currentText() == 'Tensor':
                self._ui.pbMatmul.show()
                self._ui.pbDistance.show()
            else:
                self._ui.pbMatmul.hide()
                self._ui.pbDistance.hide()
        else:
            self._ui.pbMatmul.hide()
            self._ui.pbDistance.hide()
            self._ui.opr1Unary.setCurrentIndex(0)
            if text == 'float':
                self._ui.BinaryNot_2.hide()
            else:
                self._ui.BinaryNot_2.show()
        if text == 'binary':
            self._ui.numpad.setCurrentIndex(1)
        else:
            self._ui.numpad.setCurrentIndex(0)

    def distance(self):
        assert(self._ui.opr0Type.currentText() == 'Tensor' and self._ui.opr1Type.currentText() == 'Tensor')
        result = None
        try:
            operation = TensorOperation(self._ui.opr0Widg.getData(), self._ui.opr1Widg.getData(), torch.dist)
            operation.performOperation()
            result = operation.getResult()
            self._ui.resWidg.showData(result)
            self.isChanged.emit(self)

        except Exception as e:
            logging.exception(e)
            QMessageBox.critical(self, "Error", str(e) + "; Please try again.")

    def matmul(self):
        assert(self._ui.opr0Type.currentText() == 'Tensor' and self._ui.opr1Type.currentText() == 'Tensor')
        result = None
        try:
            operation = TensorOperation(self._ui.opr0Widg.getData(), self._ui.opr1Widg.getData(), torch.matmul)
            operation.performOperation()
            result = operation.getResult()
            self._ui.resWidg.showData(result)
            self.isChanged.emit(self)

        except Exception as e:
            logging.exception(e)
            QMessageBox.critical(self, "Error", str(e) + "; Please try again.")

    def plus(self):
        result = None
        try:
            operation = TensorOperation(self._ui.opr0Widg.getData(), self._ui.opr1Widg.getData(), lambda x, y: x + y)
            operation.performOperation()
            result = operation.getResult()
            self._ui.resWidg.showData(result)
            self.isChanged.emit(self)

        except Exception as e:
            logging.exception(e)
            QMessageBox.critical(self, "Error", str(e) + "; Please try again.")

    def minus(self): 
        result = None
        try:
            operation = TensorOperation(self._ui.opr0Widg.getData(), self._ui.opr1Widg.getData(), lambda x, y: x - y)
            operation.performOperation()
            result = operation.getResult()
            self._ui.resWidg.showData(result)
            self.isChanged.emit(self)

        except Exception as e:
            logging.exception(e)
            QMessageBox.critical(self, "Error", str(e) + "; Please try again.")

    def multiply(self):
        result = None
        try:
            operation = TensorOperation(self._ui.opr0Widg.getData(), self._ui.opr1Widg.getData(), lambda x, y: x * y)
            operation.performOperation()
            result = operation.getResult()
            self._ui.resWidg.showData(result)
            self.isChanged.emit(self)

        except Exception as e:
            logging.exception(e)
            QMessageBox.critical(self, "Error", str(e) + "; Please try again.")

    def divide(self):
        result = None
        try:
            operation = TensorOperation(self._ui.opr0Widg.getData(), self._ui.opr1Widg.getData(), lambda x, y: x / y)
            operation.performOperation()
            result = operation.getResult()
            self._ui.resWidg.showData(result)
            self.isChanged.emit(self)

        except Exception as e:
            logging.exception(e)
            QMessageBox.critical(self, "Error", str(e) + "; Please try again.")

    def inverse0(self):
        result = None
        try:
            operation = TensorUnaryOperation(self._ui.opr0Widg.getData(), torch.inverse)
            operation.performOperation()
            result = operation.getResult()
            self._ui.resWidg.showData(result)
            self.isChanged.emit(self)

        except Exception as e:
            logging.exception(e)
            QMessageBox.critical(self, "Error", str(e) + "; Please try again.")

    def inverse1(self):
        result = None
        try:
            operation = TensorUnaryOperation(self._ui.opr1Widg.getData(), torch.inverse)
            operation.performOperation()
            result = operation.getResult()
            self._ui.resWidg.showData(result)
            self.isChanged.emit(self)

        except Exception as e:
            logging.exception(e)
            QMessageBox.critical(self, "Error", str(e) + "; Please try again.")

    def transpose0(self):
        result = None
        try:
            operation = TensorUnaryOperation(self._ui.opr0Widg.getData(), torch.transpose)
            operation.performOperation()
            result = operation.getResult()
            self._ui.resWidg.showData(result)
            self.isChanged.emit(self)

        except Exception as e:
            logging.exception(e)
            QMessageBox.critical(self, "Error", str(e) + "; Please try again.")

    def transpose1(self):
        result = None
        try:
            operation = TensorUnaryOperation(self._ui.opr1Widg.getData(), torch.transpose)
            operation.performOperation()
            result = operation.getResult()
            self._ui.resWidg.showData(result)
            self.isChanged.emit(self)

        except Exception as e:
            logging.exception(e)
            QMessageBox.critical(self, "Error", str(e) + "; Please try again.")

    def negative0(self):
        result = None
        try:
            operation = BinaryUnaryOperation(self._ui.opr0Widg.getData(), lambda x: -x)
            operation.performOperation()
            result = operation.getResult()
            self._ui.resWidg.showData(result)
            self.isChanged.emit(self)

        except Exception as e:
            logging.exception(e)
            QMessageBox.critical(self, "Error", str(e) + "; Please try again.")

    def negative1(self):
        result = None
        try:
            operation = BinaryUnaryOperation(self._ui.opr1Widg.getData(), lambda x: -x)
            operation.performOperation()
            result = operation.getResult()
            self._ui.resWidg.showData(result)
            self.isChanged.emit(self)

        except Exception as e:
            logging.exception(e)
            QMessageBox.critical(self, "Error", str(e) + "; Please try again.")

    def not0(self):
        result = None
        try:
            operation = BinaryUnaryOperation(self._ui.opr0Widg.getData(), lambda x: ~x)
            operation.performOperation()
            result = operation.getResult()
            self._ui.resWidg.showData(result)
            self.isChanged.emit(self)
            
        except Exception as e:
            logging.exception(e)
            QMessageBox.critical(self, "Error", str(e) + "; Please try again.")

    def not1(self):
        result = None
        try:
            operation = BinaryUnaryOperation(self._ui.opr1Widg.getData(), lambda x: ~x)
            operation.performOperation()
            result = operation.getResult()
            self._ui.resWidg.showData(result)
            self.isChanged.emit(self)

        except Exception as e:
            logging.exception(e)
            QMessageBox.critical(self, "Error", str(e) + "; Please try again.")


    def setMainWindow(self, mainwindow):
        self.__mainwindow = mainwindow

    def getMainWindow(self):
        return self.__mainwindow

    def needsTensorsTab(self):
        return False

class AllInOneCalculatorPersistent(AllInOneCalculator, CommWidgPersistent):
    def __init__(self, parent = None):
        AllInOneCalculator.__init__(self, parent)
        self.__enableSaving = True

    def saveState(self):
        if self.__enableSaving:
            state = SimpleNamespace()
            state.opr0Type = self._ui.opr0Type.currentIndex()
            state.opr1Type = self._ui.opr1Type.currentIndex()
            state.opr0Value = self._ui.opr0Widg.getData()
            state.opr1Value = self._ui.opr1Widg.getData()
            state.resWidg = self._ui.resWidg.getData()
            return "Result: " + str(state.resWidg), state


    def loadState(self, state):
        self._ui.opr0Type.setCurrentIndex(state.opr0Type)
        self._ui.opr1Type.setCurrentIndex(state.opr1Type)
        self._ui.opr0Widg.loadData(state.opr0Value)
        self._ui.opr1Widg.loadData(state.opr1Value)
        self._ui.resWidg.showData(state.resWidg)

    def disableSaving(self):
        self.__enableSaving = False

    def enableSaving(self):
        self.__enableSaving = True