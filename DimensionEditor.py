# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QSpinBox, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QTableView

from PySide6.QtCore import QTimer, QModelIndex, Qt

from PySide6.QtGui import QStandardItem, QStandardItemModel

from FrameEditor import FrameEditor
from DIndexEditor import DIndexEditor
import torch

from typing import List, Tuple, Union

# from ui_DIndexLabels import Ui_Form
from ui_DimensionEditor import Ui_Form

from NNIntSI import NNIntSI, NNIntSIM
from SpinBoxDelegate import SpinBoxDelegate, IndexSpinBoxDelegate

import logging

#- TODO: Use a stackedwidget or something to swap between with 0 dimensions (1 lineedit), 1 dimension (1 row/column of lineedit), 2 dimensions (matrix of lineedits), 3+ dimensions (matrix of lineedits in selectable dimensions for columns and rows, with other dimensions selected with the spinboxes)
# TODO: Make all the hardcoded values of the columns size and selection, and replace them with an attribute


class SizeBinding:

    def __init__(self, dimEdit: 'DimensionEditor', dim: int) -> None:
        self.dimEdit = dimEdit
        self.dim = dim

    def updateSize(self, val: int) -> None:
        # TODO: Make this change the dimensions
        if val < self.dimEdit.matrix.shape[self.dim]:
            self.dimEdit.matrix = self.dimEdit.matrix[tuple(
                (slice(None, None) if i != self.dim else slice(None, val))
                for i in range(self.dim)
            )]
        elif val < self.dimEdit.matrix.shape[self.dim]:
            shape = list(self.dimEdit.matrix.shape)
            shape[self.dim] = self.dimEdit.matrix.shape[self.dim] - val
            self.dimEdit.matrix = torch.cat(
                (
                    self.dimEdit.matrix,
                    torch.ones(shape, device = self.dimEdit.matrix.device)
                ), self.dim
            )

    def __call__(self, val: int) -> None:
        return self.updateSize(val)


class DimensionEditor(QWidget):

    def __init__(self, parent: 'MatrixEditor' = None):
        super().__init__(parent)
        self.initialized = False
        # self.dimensions = 0
        # self.dindEditors: List[DIndexEditor] = []
        self.matrix = torch.zeros(())
        self.__ui = Ui_Form()
        self.__ui.setupUi(self)
        self.frameEditor = FrameEditor(self.matrix, self)
        self.__ui.scrollAreaFE.setWidget(self.frameEditor)
        self.dim0 = None
        self.dim1 = None

        self.xDimLabel = self.__ui.selectionXLabel
        self.xDimSpin = self.__ui.selectionXSpinbox
        self.xDimSpin.valueChanged.connect(self.updateDimensions_t)
        self.yDimLabel = self.__ui.selectionYLabel
        self.yDimSpin = self.__ui.selectionYSpinbox
        self.yDimSpin.valueChanged.connect(self.updateDimensions_t)

        self.__ui.dimensionsTable.horizontalHeader().geometriesChanged.connect(
            self.udtmsImpl
        )
        self.__ui.dimensionsTable.verticalHeader().geometriesChanged.connect(
            self.udtmsImpl
        )
        """
        TODO: Make the assertions/exceptions inisde fo the NNIntSI.py such that 
        nonnegative integers from the setter throw an exception, which should be catched 
        by this class or somewhere else
        TODO: Set the below changeDimensions to not use inc, dec; use the below to clone the items needed, and connect them
        """
        self.model = NNIntSIM(self)
        # self.model = QStandardItemModel(self)
        self.__ui.dimensionsTable.setModel(self.model)
        self.model.setColumnCount(2)
        self.model.setHorizontalHeaderLabels(["Size", "Selection"])

        self.changeDimensions(parent.getDimensions())
        spbidIndex = IndexSpinBoxDelegate(self.__ui.dimensionsTable)
        spbidSize = SpinBoxDelegate(self.__ui.dimensionsTable, 1)
        self.__ui.dimensionsTable.setItemDelegateForColumn(0, spbidSize)
        self.__ui.dimensionsTable.setItemDelegateForColumn(1, spbidIndex)

        self.updateDimensionsCount(self.model.rowCount())
        # self.model.dataChanged.connect(
        #     lambda x: self.model.itemFromIndex(x).setValue()
        # )
        # self.model.dataChanged.connect(lambda x: logging.info(self.model.data(x)))
        # self.__ui.dimensionsTable.edi
        # self.model.dataChanged.connect(lambda x: logging.info(type(self.model.data(x))))
        self.model.dataChanged.connect(self.modelUpdateHandler)

        self.frameEditor.matrixModel.dataChanged.connect(self.logMatrix)

        self.modelUpdatesEnabled = True
        self.initialized = True

    def logMatrix(self):
        logging.info(self.matrix)

    def modelUpdateHandler(
        self, index0: QModelIndex, index1: QModelIndex, li: list
    ):
        if not self.modelUpdatesEnabled:
            return
        # logging.info(index0, index1, li)
        # logging.info(index0.column())
        # assert (
        #     index0.column() == index1.column() and index0.row() == index1.row()
        # )
        for i in range(index0.row(), index1.row() + 1):
            # if index0.column() == 0:
            self.updateSize(i, self.model.item(i, 0).getValue())
        # for i in range(self.model.columnCount()):
        #     if self.model.item(index0.row(), i) is None:
        #         return
        self.updateFrameMatrix()

    def udtmsImpl(self):
        margins = self.__ui.dimensionWidget.layout().contentsMargins()
        # logging.info("width =", self.__ui.dimensionsTable.verticalHeader().width())
        # logging.info(margins)
        self.__ui.dimensionWidget.setMaximumWidth(
            self.__ui.dimensionsTable.horizontalHeader().length() +
            self.__ui.dimensionsTable.verticalHeader().width() +
            self.__ui.dimensionsTable.frameWidth() * 2 + margins.left() +
            margins.right() + 6 + (
                self.__ui.dimensionsTable.verticalScrollBar().width() if
                self.__ui.dimensionsTable.verticalScrollBar().isVisible() else 0
            )
            # margins.left() + margins.right() + 2
        )

    def getCurrentFrame(self) -> Tuple[Union[int, slice]]:
        currentFrame = []
        for i in range(self.model.rowCount()):
            if self.dim0 is not None and self.dim0 == i or self.dim1 is not None and self.dim1 == i:
                currentFrame.append(slice(None, None))
            else:
                currentFrame.append(self.model.item(i, 1).getValue() - 1)
        logging.info(tuple(currentFrame))
        return tuple(currentFrame)

    def updateFrameMatrix(self, empty: bool = False, transpose: bool = False):
        # logging.info(self.matrix)
        # logging.info(self.matrix.shape)
        if empty:
            #TODO: Maybe make this do the same as the below; remove the if empty completely
            self.frameEditor.updateMatrix(torch.zeros(()))
        else:
            # logging.info(self.getCurrentFrame())
            logging.info(self.getCurrentFrame())
            logging.info(self.matrix)
            matrix = self.matrix[self.getCurrentFrame()]
            self.frameEditor.updateMatrix(matrix.T if transpose else matrix)

    def changeDimensions(self, dim):
        currentDimensions = self.model.rowCount()

        if currentDimensions == dim:
            return

        self.modelUpdatesEnabled = False

        self.model.setRowCount(dim)
        if currentDimensions < dim:
            # self.model.beginInsertRows()
            #TODO: Fix this code and the below else code; find why it does not work
            logging.info("From:", self.matrix)
            self.matrix = self.matrix.reshape(
                self.matrix.shape +
                tuple((1 for i in range(self.matrix.dim(), dim)))
            )
            logging.info("To:", self.matrix)
            for i in range(currentDimensions, dim):
                self.model.setItem(i, 0, NNIntSI(1))
                self.model.setItem(i, 1, NNIntSI(1))
        else:
            self.matrix = self.matrix.reshape(self.matrix.shape[: dim])

        # self.frameEditor.updateDimensionsCount(dim)
        logging.info(currentDimensions, dim)
        self.updateDimensionsCount(dim)

        self.modelUpdatesEnabled = True

    def updateDimensions_t(self, _):
        return self.updateDimensions(self.model.rowCount())

    def updateDimensions(self, dimensions: int):
        setHide = set()
        setShow = set()

        if self.dim0 is not None and self.dim0 < dimensions:
            setShow.add(self.dim0)

        if self.dim1 is not None and self.dim1 < dimensions:
            setShow.add(self.dim1)

        if dimensions >= 1:
            setHide.add(self.xDimSpin.value())
            self.dim0 = self.xDimSpin.value()

        if dimensions >= 2:
            setHide.add(self.yDimSpin.value())
            self.dim1 = self.yDimSpin.value()

        for i in setHide.difference(setShow):
            self.model.item(i, 1).setVisibility(False)

        for i in setShow.difference(setHide):
            self.model.item(i, 1).setVisibility(True)

        #TODO: Refactor this function call out of this function; this function is doing too much
        self.updateFrameMatrix(
            self.dim0 == self.dim1,
            (self.dim0 is not None and self.dim1 is not None) and
            self.dim0 > self.dim1
        )

    def updateDimensionsCount(self, dimensions: int):
        self.xDimSpin.setMaximum(max(0, dimensions - 1))
        self.yDimSpin.setMaximum(max(0, dimensions - 1))
        if dimensions >= 2:
            self.yDimLabel.show()
            self.yDimSpin.show()
            self.xDimLabel.show()
            self.xDimSpin.show()
        else:
            self.yDimLabel.hide()
            self.yDimSpin.hide()
            if dimensions >= 1:
                self.xDimLabel.show()
                self.xDimSpin.show()
            else:
                self.xDimLabel.hide()
                self.xDimSpin.hide()
            # pass
        if self.initialized:
            self.updateDimensions(dimensions)

    def updateSize(self, dim: int, val: int) -> None:
        # TODO: Make this change the dimensions
        if val < self.matrix.size(dim):
            self.matrix = self.matrix[tuple(
                (slice(None, None) if i != dim else slice(None, val))
                for i in range(val)
            )]
        elif val > self.matrix.size(dim):
            shape = list(self.matrix.shape)
            shape[dim] = val - self.matrix.size(dim)
            self.matrix = torch.cat(
                (self.matrix, torch.zeros(shape, device = self.matrix.device)),
                dim
            )
