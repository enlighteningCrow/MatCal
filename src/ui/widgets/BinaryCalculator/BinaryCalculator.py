#TODO: Make the Operation class hold all the operations instead of the presentation layer

from types import SimpleNamespace
from typing import Optional, Tuple
import PySide6.QtCore
from PySide6.QtWidgets import QWidget

from ui.CommWidg import CommWidg, CommWidgPersistent

from generated.designer.ui_BinaryCalculator import Ui_Form

from app.BinaryOperation import BinaryOperationMenu, BinaryOperation

# This is the class Ui_Form that is imported
"""
class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lNum0 = QLabel(Form)
        self.lNum0.setObjectName(u"lNum0")

        self.gridLayout.addWidget(self.lNum0, 0, 0, 1, 1)

        self.sbNum0 = QSpinBox(Form)
        self.sbNum0.setObjectName(u"sbNum0")
        self.sbNum0.setMinimum(-1000000000)
        self.sbNum0.setMaximum(1000000000)

        self.gridLayout.addWidget(self.sbNum0, 0, 1, 1, 1)

        self.bNum0 = QLabel(Form)
        self.bNum0.setObjectName(u"bNum0")

        self.gridLayout.addWidget(self.bNum0, 0, 2, 1, 1)

        self.lNum1 = QLabel(Form)
        self.lNum1.setObjectName(u"lNum1")

        self.gridLayout.addWidget(self.lNum1, 1, 0, 1, 1)

        self.sbNum1 = QSpinBox(Form)
        self.sbNum1.setObjectName(u"sbNum1")
        self.sbNum1.setMinimum(-1000000000)
        self.sbNum1.setMaximum(1000000000)

        self.gridLayout.addWidget(self.sbNum1, 1, 1, 1, 1)

        self.bNum1 = QLabel(Form)
        self.bNum1.setObjectName(u"bNum1")

        self.gridLayout.addWidget(self.bNum1, 1, 2, 1, 1)

        self.lOpr = QLabel(Form)
        self.lOpr.setObjectName(u"lOpr")

        self.gridLayout.addWidget(self.lOpr, 2, 0, 1, 1)

        self.cbOpr = QComboBox(Form)
        self.cbOpr.setObjectName(u"cbOpr")

        self.gridLayout.addWidget(self.cbOpr, 2, 1, 1, 1)

        self.pbCal = QPushButton(Form)
        self.pbCal.setObjectName(u"pbCal")

        self.gridLayout.addWidget(self.pbCal, 2, 2, 1, 1)

        self.lRes = QLabel(Form)
        self.lRes.setObjectName(u"lRes")

        self.gridLayout.addWidget(self.lRes, 3, 0, 1, 1)

        self.sbNumRes = QSpinBox(Form)
        self.sbNumRes.setObjectName(u"sbNumRes")
        self.sbNumRes.setReadOnly(True)

        self.gridLayout.addWidget(self.sbNumRes, 3, 1, 1, 1)

        self.lNumRes = QLabel(Form)
        self.lNumRes.setObjectName(u"lNumRes")

        self.gridLayout.addWidget(self.lNumRes, 3, 2, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lNum0.setText(QCoreApplication.translate("Form", u"First Number:", None))
        self.bNum0.setText(QCoreApplication.translate("Form", u"Binary Representation", None))
        self.lNum1.setText(QCoreApplication.translate("Form", u"Second Number:", None))
        self.bNum1.setText(QCoreApplication.translate("Form", u"Binary Representation", None))
        self.lOpr.setText(QCoreApplication.translate("Form", u"Operation", None))
        self.pbCal.setText(QCoreApplication.translate("Form", u"Calculate", None))
        self.lRes.setText(QCoreApplication.translate("Form", u"Results:", None))
        self.lNumRes.setText(QCoreApplication.translate("Form", u"TextLabel", None))
"""


class BinaryCalculator(CommWidg):
    def __init__(self, parent = None) -> None:
        super().__init__()
        self._ui = Ui_Form()
        self._ui.setupUi(self)
        self._binaryOperationMenu = BinaryOperationMenu()
        self._ui.pbCal.clicked.connect(self.calculate)
        self._ui.sbNum0.valueChanged.connect(self._updateBinaryRepresentation)
        self._ui.sbNum1.valueChanged.connect(self._updateBinaryRepresentation)
        self._updateBinaryRepresentation()
        self._ui.cbOpr.addItems(self._binaryOperationMenu.getOperations().keys())
        self.__mainWindow = None

    def _updateBinaryRepresentation(self):
        self._ui.bNum0.setText(bin(self._ui.sbNum0.value()))
        self._ui.bNum1.setText(bin(self._ui.sbNum1.value()))


    def calculate(self):
        operation = BinaryOperation(self._ui.sbNum0.value(), self._ui.sbNum1.value(), self._binaryOperationMenu.getOperations()[self._ui.cbOpr.currentText()])
        # self._ui.sbNumRes.setValue(self._binaryOperationMenu.calculate(self._ui.cbOpr.currentText(), self._ui.sbNum0.value(), self._ui.sbNum1.value()))
        operation.performOperation()
        result = operation.getResult()
        self._ui.sbNumRes.setValue(result)
        self._ui.lNumRes.setText(bin(self._ui.sbNumRes.value()))
        self.isChanged.emit(self)

    def setMainWindow(self, mainwindow):
        self.__mainWindow = mainwindow

    def getMainWindow(self):
        return self.__mainWindow

    def needsTensorsTab(self) -> bool:
        return False

    
        

class BinaryCalculatorPersistent(BinaryCalculator, CommWidgPersistent):
    def __init__(self) -> None:
        super().__init__()
        self.__savingDisabled = False

    def saveState(self) -> Tuple[str, SimpleNamespace]:
        s = SimpleNamespace()
        s.num0 = self._ui.sbNum0.value()
        s.num1 = self._ui.sbNum1.value()
        s.opr = self._ui.cbOpr.currentText()[:]
        return "BinaryCalculator", s
    
    def loadState(self, state: SimpleNamespace):
        self.__savingDisabled = True
        self._ui.sbNum0.setValue(state.num0)
        self._ui.sbNum1.setValue(state.num1)
        self._ui.cbOpr.setCurrentText(state.opr)
        self.__savingDisabled = False

    def enableSaving(self):
        self.__savingDisabled = False

    def disableSaving(self):
        self.__savingDisabled = True