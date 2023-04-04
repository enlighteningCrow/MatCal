from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QApplication, QStyledItemDelegate, QItemDelegate, QDoubleSpinBox, QTableView, QWidget, QVBoxLayout
from PySide6.QtGui import QStandardItemModel, QStandardItem
from NNIntSI import NNIntSI, NNIntSIM

from math import inf

import logging


class DoubleSpinBoxDelegate(QStyledItemDelegate):

    def __init__(
        self, parent = None, minVal: float = -inf, maxVal: float = inf
    ):
        super().__init__(parent)
        self.minVal = minVal
        self.maxVal = maxVal

    def createEditor(self, parent, option, index):
        editor = QDoubleSpinBox(parent)
        editor.setMinimum(self.minVal)
        editor.setMaximum(self.maxVal)
        return editor

    def setEditorData(self, editor, index):
        #TODO: (PROBABLY) Implement the setData or some other method in the MatrixModel to support this operation
        value = index.model().data(index, Qt.EditRole)
        editor.setValue(float(value))

    def setModelData(self, editor, model, index):
        value = editor.value()
        logging.info("Model data set on", index, "to", value)
        model.setData(index, value, Qt.EditRole)

    def setMax(self, maxVal: float):
        self.maxVal = maxVal

    def setMin(self, minVal: float):
        self.minVal = minVal